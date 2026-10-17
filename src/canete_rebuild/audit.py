"""Legacy-to-reconstructed label comparisons for diagnostics, NEVER for fitting models."""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from .common import ROOT,source,derived,reportdir,dump_json,config


def points_inside_grid(pts, xy,cell_size):
    coords=xy[['x','y']].to_numpy()
    dist,nearest=cKDTree(coords).query(pts[['x','y']].to_numpy(),k=1)
    nearest_xy=coords[nearest]
    inside=(np.abs(nearest_xy-pts[['x','y']].to_numpy())<=cell_size/2+1e-7).all(axis=1)
    return inside


def main(root=ROOT):
    root=Path(root);cfg=config(root/'configs/project.yml')
    if cfg['analysis']['grid_mode'] != 'historical_mask':
        raise ValueError('Auditoría celda a celda disponible solo para grid_mode=historical_mask; seleccionar primero una intersección común')
    pts=pd.read_csv(derived(root)/'inventario_maestro_previo_PRIVADO.csv')
    pts=pts.loc[pts.coordinate_valid & pts.coordinate_consistent]
    result={'purpose':'Only diagnostic of source-mask and historic label differences; no fitting','grids':{}}
    for res in (250,50):
        out=pd.read_csv(derived(root)/f'grilla_recalculada_{res}m_PRIVADA.csv.gz',usecols=['x','y','recorded_point_in_cell','legacy_30m_centroid_buffer'])
        old=source('grid_250m' if res==250 else 'grid_50m',cfg,root)
        legacy_label='presencia_sitio_nuevo' if res==250 else 'label'
        xy_cols=['X','Y'] if res==250 else ['x','y']
        raw=pd.read_csv(old,usecols=xy_cols+[legacy_label]);raw=raw.rename(columns={xy_cols[0]:'x',xy_cols[1]:'y'})
        if not np.allclose(raw[['x','y']].to_numpy(),out[['x','y']].to_numpy(),rtol=0,atol=1e-4):
            raise ValueError('Grillas fuente y salida no alineadas celda a celda: detener auditoría')
        prior=raw[legacy_label].fillna(0).astype(int).to_numpy()
        newbuff=out.legacy_30m_centroid_buffer.to_numpy().astype(int)
        obs=out.recorded_point_in_cell.to_numpy().astype(int)
        inside=points_inside_grid(pts,out,res)
        result['grids'][str(res)]={
            'source_grid_cells':len(raw),
            'prior_point_records_inside_domain':int(inside.sum()),
            'prior_point_records_outside_domain':int((~inside).sum()),
            'legacy_positive_cells':int(prior.sum()),
            'new_point_containing_cells':int(obs.sum()),
            'rebuilt_buffer30_positive_cells':int(newbuff.sum()),
            'identical_legacy_vs_buffer30':bool(np.array_equal(prior,newbuff)),
            'legacy_positive_cells_shared_with_rebuilt_point_label':int(((prior==1)&(obs==1)).sum()),
            'legacy_vs_buffer30_changed_cell_count':int((prior!=newbuff).sum()),
            'warning': 'Different site inventories/resolutions; especially 250m: do not compare AUCs before common-support remapping.'}
    dump_json(reportdir(root)/'03_revision_historicos.json',result)
    for k,v in result['grids'].items():print(k+'m:',v)
    return result
