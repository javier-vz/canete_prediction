"""Create a chronology-safe prior inventory; KML overlap never establishes documentary source."""
from __future__ import annotations
import re
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from pyproj import Transformer
from scipy.spatial import cKDTree
from .common import ROOT,config,source,derived,reportdir,sha256,dump_json,required_columns


def load_kmz(path):
    # KML in official KMZ documents; read without changing geometry.
    path = Path(path)
    if not path.exists():
        return None
    g = gpd.read_file(f'/vsizip/{path.resolve().as_posix()}/doc.kml', driver='KML')
    if g.crs is None:
        raise ValueError(f'KMZ sin CRS: {path.name}')
    return g.to_crs('EPSG:32718')


def coordinate_quality(df, tolerance_m=5):
    required_columns(df,['x','y','lat','lon'],'sitios_previo')
    p = Transformer.from_crs('EPSG:4326','EPSG:32718',always_xy=True)
    u,v = p.transform(df.lon.to_numpy(float),df.lat.to_numpy(float))
    err = np.hypot(u-df.x.to_numpy(float),v-df.y.to_numpy(float))
    return err, err>tolerance_m


def spatial_match(sites: gpd.GeoDataFrame, official: gpd.GeoDataFrame|None, threshold_m=100):
    """Distance to any MINCUL geometry; spatial candidate only, NEVER source classification."""
    n = len(sites)
    if official is None or len(official)==0:
        return np.full(n,np.nan),np.full(n,'not_available',dtype=object)
    geoms = official.loc[official.geometry.notna() & (~official.geometry.is_empty),['geometry']]
    if len(geoms)==0:
        return np.full(n,np.nan),np.full(n,'not_available',dtype=object)
    a = gpd.sjoin_nearest(sites[['geometry']],geoms,how='left',distance_col='distance_m')
    dd = a.groupby(a.index)['distance_m'].min().reindex(sites.index).to_numpy(float)
    match = np.where(np.isclose(dd,0,atol=0.001),'intersects_official_geometry',
             np.where(dd<=threshold_m,'near_official_geometry','no_match_within_threshold'))
    return dd,match


def make_inventory(points, official_delim=None, official_decl=None, threshold_m=100, tolerance_m=5):
    pts=points.copy().reset_index(drop=True)
    required_columns(pts,['x','y','lat','lon'],'sitios_previo')
    for col in ('x','y','lat','lon'):
        pts[col]=pd.to_numeric(pts[col],errors='coerce')
    pts['original_row']=np.arange(1,len(pts)+1)
    pts['record_id']=['PRE-'+str(i).zfill(4) for i in pts.original_row]
    pts['chronology']='PRE_DINA_FIELDWORK_USER_CONFIRMED'
    pts['source_group']='MINCUL_OR_PAVC_UNRESOLVED'
    pts['source_institution_verified']=False
    pts['archaeological_observation_type']='NOT_DOCUMENTED_IN_CSV'
    pts['geometry_role']='POINT_RECORD_NOT_VALIDATED_AS_DISTINCT_SITE'
    pts['coordinate_valid']=pts[['x','y','lat','lon']].notna().all(axis=1)
    err=np.full(len(pts),np.nan)
    valid=pts.coordinate_valid.to_numpy()
    if valid.any():
        quality,_=coordinate_quality(pts.loc[valid],tolerance_m)
        err[valid]=quality
    pts['latlon_vs_utm_error_m']=np.round(err,4)
    pts['coordinate_consistent']=pts.coordinate_valid & (pts.latlon_vs_utm_error_m<=tolerance_m)
    pts['duplicate_xy']=pts.duplicated(['x','y'],keep=False)
    # A distance match cannot disambiguate a site represented only as a point in another database.
    geo = gpd.GeoDataFrame(pts[['record_id']].copy(), geometry=gpd.points_from_xy(pts.x,pts.y), crs='EPSG:32718')
    for official, stem in [(official_delim,'mincul_delimitados'),(official_decl,'mincul_declarados')]:
        dist,status=spatial_match(geo,official,threshold_m)
        pts[stem+'_distance_m']=np.round(dist,3)
        pts[stem+'_spatial_relation']=status
    near=((pts['mincul_delimitados_distance_m']<=threshold_m)|
          (pts['mincul_declarados_distance_m']<=threshold_m))
    pts['mincul_spatial_candidate']=near
    pts['provenance_action']=np.where(near,'CHECK_MINCUL_ID_AND_SOURCE','CHECK_PAVC_OR_UNDELIMITED_MINCUL')
    return pts


def main(root=ROOT):
    root=Path(root);cfg=config(root/'configs/project.yml')
    raw=source('sites',cfg,root)
    if not raw.exists():
        raise FileNotFoundError(f'Falta archivo privado: {raw}. Copia el CSV original sin modificar.')
    pts=pd.read_csv(raw)
    if len(pts)!=cfg['project']['original_points']:
        raise ValueError(f'Se esperaban 188 puntos, archivo contiene {len(pts)}; auditar antes de continuar')
    missing_official=[key for key in ('mincul_delimitados','mincul_declarados') if not source(key,cfg,root).exists()]
    if missing_official:
        raise FileNotFoundError(f'Faltan las dos fuentes MINCUL para auditoría integral: {missing_official}')
    o1=load_kmz(source('mincul_delimitados',cfg,root))
    o2=load_kmz(source('mincul_declarados',cfg,root))
    master=make_inventory(pts,o1,o2,cfg['matching']['proximity_m'],cfg['matching']['coordinate_tolerance_m'])
    dest=derived(root)/'inventario_maestro_previo_PRIVADO.csv'
    master.to_csv(dest,index=False)
    review=master.loc[(~master.coordinate_consistent)|master.duplicate_xy|(~master.mincul_spatial_candidate),
            ['record_id','original_row','coordinate_consistent','duplicate_xy','mincul_delimitados_distance_m','mincul_declarados_distance_m','provenance_action']]
    review.to_csv(derived(root)/'revision_procedencia_y_coordenadas_PRIVADO.csv',index=False)
    stats={
      'note':'All 188 are pre-field observations (user confirmation). Institutional provenance per row remains unresolved.',
      'n_prior_points':len(master),
      'n_unique_xy':int(len(master.drop_duplicates(['x','y']))),
      'coord_inconsistencies':int((~master.coordinate_consistent).sum()),
      'candidate_near_mincul_100m':int(master.mincul_spatial_candidate.sum()),
      'not_matched_100m':int((~master.mincul_spatial_candidate).sum()),
      'intersect_delimitados':int((master.mincul_delimitados_distance_m<=0.001).sum()),
      'source_sha256':sha256(raw),
      'output_private':str(dest.relative_to(root)),
      'MINCUL_layers':{'delimitados':len(o1) if o1 is not None else None,'declarados':len(o2) if o2 is not None else None},
      'caveat':'Near official geometry is not documentary proof of MINCUL provenance; far does not prove PAVC.'}
    dump_json(reportdir(root)/'01_inventario.json',stats)
    print('Inventario previo:',stats['n_prior_points'],'| revisión MINCUL ≤100m:',stats['candidate_near_mincul_100m'])
    print('Salida privada:',dest)
    return master,stats
