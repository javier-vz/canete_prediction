"""Fresh covariates and presence observations on explicitly documented study masks."""
from __future__ import annotations
from pathlib import Path
import os
import warnings
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.features import rasterize
from scipy.ndimage import distance_transform_edt, minimum_filter
from scipy.spatial import cKDTree
from shapely import contains_xy, union_all
from .common import ROOT, config, source, derived, reportdir, dump_json, sha256, required_columns


def extract_grid_xy(csvpath, resolution):
    """Use ONLY historical cell centres as spatial mask; NEVER labels or old predictors."""
    if not Path(csvpath).exists():
        raise FileNotFoundError(f'Falta la grilla histórica para definir la máscara: {csvpath}')
    cols=['X','Y'] if resolution==250 else ['x','y']
    xy=pd.read_csv(csvpath,usecols=cols)
    xy.columns=['x','y']
    xy=xy.astype(float)
    if xy.isna().any().any() or xy.duplicated().any():
        raise ValueError('Celdas duplicadas o coordenadas vacías en plantilla histórica')
    diffs=[]
    for col in ('x','y'):
        xx=np.sort(xy[col].unique()); d=np.diff(xx); d=d[d>0.01];
        if len(d): diffs.append(float(np.min(d)))
    if diffs and abs(min(diffs)-resolution)>0.5:
        raise ValueError(f'Espaciado de grilla inesperado: {diffs}, resolución solicitada {resolution} m')
    return xy


def grid_xy_polygon(study_polygon,resolution):
    g=gpd.read_file(study_polygon)
    if g.crs is None: raise ValueError('Polígono del área de estudio sin CRS')
    g=g.to_crs(32718)
    geoms=list(g.geometry.dropna())
    if not geoms: raise ValueError('No hay geometrías en polígono de estudio')
    geom=union_all(geoms)
    lo_x,lo_y,hi_x,hi_y=geom.bounds
    # Anchor to global UTM multiples of resolution to align scales exactly.
    xx=np.arange(np.floor(lo_x/resolution)*resolution+resolution/2,hi_x,resolution)
    yy=np.arange(np.floor(lo_y/resolution)*resolution+resolution/2,hi_y,resolution)
    if len(xx)*len(yy)>12_000_000: raise ValueError('Área demasiado grande: revisar CRS y máscara')
    X,Y=np.meshgrid(xx,yy)
    mask=contains_xy(geom,X,Y)
    return pd.DataFrame({'x':X[mask],'y':Y[mask]})


def build_label_arrays(cell_x,cell_y,point_x,point_y,resolution,buffer_m):
    """Label observed point-in-cell separately from legacy centre-buffer rule.

    Unvisited / unrecorded locations remain UNLABELLED, never certified absence.
    """
    cx=np.asarray(cell_x,float);cy=np.asarray(cell_y,float)
    px=np.asarray(point_x,float);py=np.asarray(point_y,float)
    if len(cx)==0 or len(px)==0:
        raise ValueError('Se requieren celdas y puntos de registro previo')
    cells=np.column_stack((cx,cy));points=np.column_stack((px,py))
    cell_tree=cKDTree(cells)
    center_has_point=np.zeros(len(cells),dtype=np.int8)
    # All nearby candidates, not just nearest: boundary-touching points can intersect 2+ cells.
    k=min(16,len(cells))
    dd,ix=cell_tree.query(points,k=k)
    ix=np.asarray(ix).reshape(len(points),-1)
    for point, neighbours in zip(points,ix):
        good=np.abs(cells[neighbours]-point)<=resolution/2+1e-7
        selected=neighbours[good.all(axis=1)]
        center_has_point[selected]=1
    distances=cKDTree(points).query(cells,k=1,workers=-1)[0]
    buffer_flag=(distances<=buffer_m+1e-8).astype(np.int8)
    # Do NOT add distance-to-sites as predictor; return only for diagnostic consistency.
    return center_has_point,buffer_flag,distances


def dem_surface(dem_path):
    with rasterio.open(dem_path) as ds:
        if ds.crs is None: raise ValueError('DEM sin CRS')
        if ds.crs.to_epsg()!=32718:
            raise ValueError(f'DEM debe estar en EPSG:32718, está en {ds.crs}; reproyectar previamente')
        a=ds.read(1).astype('float64')
        valid=np.isfinite(a)
        if ds.nodata is not None:valid &= (a!=ds.nodata)
        valid &= (a>-1000) & (a<9000)
        arr=a.copy(); arr[~valid]=np.nan
        dy,dx=abs(ds.transform.e),abs(ds.transform.a)
        # Local slope derivatives only when entire 3x3 is valid; avoid NoData spikes.
        filled=np.where(valid,arr,0)
        grad_y,grad_x=np.gradient(filled,dy,dx)
        sl=np.degrees(np.arctan(np.hypot(grad_x,grad_y)))
        neighbourhood=minimum_filter(valid.astype('uint8'),size=3,mode='constant',cval=0)>0
        sl[~neighbourhood]=np.nan
        return arr,sl,ds.transform,ds.crs,ds.nodata


def source_vector_distances(path,dem_transform,shape,coords):
    """Approximate nearest mapped vector distance through native ~31m DEM raster.
    Is not an exact vector distance; error is of order the raster pixel diagonal.
    """
    p=Path(path)
    if not p.exists(): return None,'missing'
    os.environ['SHAPE_RESTORE_SHX']='YES'
    try:
        v=gpd.read_file(p)
        if v.crs is None:return None,'no_crs'
        v=v.to_crs(32718)
        valid=v.geometry[v.geometry.notna() & ~v.geometry.is_empty]
        if len(valid)==0:return None,'empty'
        vecmask=rasterize(((geom,1) for geom in valid),out_shape=shape,transform=dem_transform,fill=0,dtype='uint8',all_touched=True)
        if not vecmask.any():return None,'no_lines_in_dem_extent'
        dist=distance_transform_edt(vecmask==0,sampling=(abs(dem_transform.e),abs(dem_transform.a)))
        return dist,'ok_approx_raster_distance'
    except Exception as exc:
        return None,f'ERROR_{type(exc).__name__}: {str(exc)[:180]}'


def raster_sample(arr,transform,x,y):
    from rasterio.transform import rowcol
    x=np.asarray(x);y=np.asarray(y)
    rr,cc=rowcol(transform,x,y)
    rr=np.asarray(rr,dtype=int);cc=np.asarray(cc,dtype=int)
    valid=(rr>=0)&(cc>=0)&(rr<arr.shape[0])&(cc<arr.shape[1])
    out=np.full(len(x),np.nan)
    out[valid]=arr[rr[valid],cc[valid]]
    return out


def make_grid(xy,points,resolution,buffer_m,dem_data=None,hydrology=None):
    cell=xy.copy();cell.columns=['x','y']
    cell['cell_id']=['G'+str(resolution)+'_'+str(i).zfill(7) for i in range(1,len(cell)+1)]
    # Do not fit to field findings; input points MUST be prior inventory only.
    observed,buffered,nearest=build_label_arrays(cell.x,cell.y,points.x,points.y,resolution,buffer_m)
    cell['recorded_point_in_cell']=observed
    cell['legacy_30m_centroid_buffer']=buffered
    cell['background_status']='UNLABELLED_NOT_CONFIRMED_ABSENCE'
    if dem_data is not None:
        altitude,slope,transform,_,_=dem_data
        cell['altitud_m']=raster_sample(altitude,transform,cell.x,cell.y)
        cell['pendiente_grados']=raster_sample(slope,transform,cell.x,cell.y)
        for name,distarr in (hydrology or {}).items():
            cell[name]=raster_sample(distarr,transform,cell.x,cell.y) if distarr is not None else np.nan
    # Leakage proof: no distance-to-known-sites column in modelling dataset.
    return cell, nearest


def main(root=ROOT):
    root=Path(root);cfg=config(root/'configs/project.yml')
    master_file=derived(root)/'inventario_maestro_previo_PRIVADO.csv'
    if not master_file.exists():
        raise FileNotFoundError('Ejecutar antes scripts/01_reconstruir_inventario.py')
    pts=pd.read_csv(master_file)
    pts=pts[pts.coordinate_valid.astype(bool) & pts.coordinate_consistent.astype(bool)]
    if pts.empty: raise ValueError('Sin puntos de inventario previo válidos')
    mode=cfg['analysis']['grid_mode']
    demsource=source('dem',cfg,root)
    dem=None;hydrology={};hydro_status={}
    if demsource.exists():
        dem=dem_surface(demsource)
        for short,filekey in [('dist_acequia_m_aprox','acequias'),('dist_rio_m_aprox','rios')]:
            dat,status=source_vector_distances(source(filekey,cfg,root),dem[2],dem[0].shape,pts[['x','y']])
            hydrology[short]=dat;hydro_status[short]=status
    else:
        raise FileNotFoundError(f'Falta DEM original en {demsource}; no generar variables con valores inventados')
    results={'grid_mode':mode,'dem_source_sha256':sha256(demsource),
      'chronology':'PRE_DINA_FIELDWORK_USER_CONFIRMED','hydrology_raster_distance_status':hydro_status,
      'distance_source_warning':'Hydrological distances approx based on native DEM pixels, not exact vector distances.',
      'labels':'recorded_point_in_cell is observed registry incidence; legacy_30m_centroid_buffer diagnostic; unrecorded != surveyed absence',
      'models_run':False,'grids':{}}
    for res in (250,50):
        if mode=='historical_mask':
            historical=source('grid_250m' if res==250 else 'grid_50m',cfg,root)
            xy=extract_grid_xy(historical,res)
            mask_source=historical.name
        elif mode=='polygon':
            study=cfg['analysis']['approved_study_polygon']
            if not study:raise ValueError('Definir approved_study_polygon para grid_mode=polygon')
            path=(root/study).resolve()
            if not path.exists():raise FileNotFoundError(path)
            xy=grid_xy_polygon(path,res);mask_source=str(path.relative_to(root))
        else:
            raise ValueError('grid_mode debe ser historical_mask o polygon')
        out,nearest=make_grid(xy,pts,res,cfg['analysis']['historical_buffer_m'],dem,hydrology)
        outpath=derived(root)/f'grilla_recalculada_{res}m_PRIVADA.csv.gz'
        out.to_csv(outpath,index=False,compression='gzip',float_format='%.6f')
        stats={'resolution_m':res,'grid_cell_count':len(out),
              'study_area_as_grid_km2':len(out)*res*res/1e6,
              'mask_source_type':mode,'mask_source':mask_source,
              'recorded_point_in_cell_count':int(out.recorded_point_in_cell.sum()),
              'legacy_30m_centroid_buffer_count':int(out.legacy_30m_centroid_buffer.sum()),
              'DEM_missing_or_edge_count':int(out.altitud_m.isna().sum()),
              'slope_missing_or_edge_count':int(out.pendiente_grados.isna().sum()),
              'maximum_valid_slope_deg':float(out.pendiente_grados.max()),
              'output_file':str(outpath.relative_to(root)),
              'predictor_columns':[c for c in out if c in ('altitud_m','pendiente_grados','dist_acequia_m_aprox','dist_rio_m_aprox')],
              'warning':'Cell centres inherited only for spatial support' if mode=='historical_mask' else 'New lattice from approved polygon'}
        results['grids'][str(res)]=stats
        print(res,'m:',stats['grid_cell_count'],'cells, presence cells',stats['recorded_point_in_cell_count'],'legacy buffer',stats['legacy_30m_centroid_buffer_count'])
    dump_json(reportdir(root)/'02_grillas_recalculadas.json',results)
    return results
