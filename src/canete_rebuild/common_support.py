"""Candidate overlap of 50 m and 250 m historical masks, not an approved study region."""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from .common import ROOT,derived,reportdir,dump_json


def fine_within_coarse(fine_xy,coarse_xy,coarse_size=250):
    """Return fine cells whose centres fall within ANY coarse cell square, boundaries inclusive."""
    coarse=np.asarray(coarse_xy,dtype=float)
    fine=np.asarray(fine_xy,dtype=float)
    _,ind=cKDTree(coarse).query(fine,k=1)
    # Nearest coarse centre always identifies containing square for regular nonoverlapping lattice.
    inside=(np.abs(fine-coarse[ind])<=coarse_size/2+1e-7).all(axis=1)
    return inside,ind


def main(root=ROOT):
    root=Path(root)
    folder=derived(root)
    f=pd.read_csv(folder/'grilla_recalculada_50m_PRIVADA.csv.gz')
    c=pd.read_csv(folder/'grilla_recalculada_250m_PRIVADA.csv.gz',usecols=['x','y','cell_id'])
    inside,idx=fine_within_coarse(f[['x','y']].to_numpy(),c[['x','y']].to_numpy())
    subset=f.loc[inside].copy()
    subset['parent_250m_cell_id']=c['cell_id'].iloc[idx[inside]].to_numpy()
    dest=folder/'grilla_50m_soporte_comun_802km2_CANDIDATA_PRIVADA.csv.gz'
    subset.to_csv(dest,index=False,compression='gzip',float_format='%.6f')
    rr={'status':'CANDIDATE_NOT_APPROVED','criterion':'50m cell centroid lies inside a 250m cell square of historical corridor domain',
        'coarse_cells':len(c),'coarse_area_km2':len(c)*250*250/1e6,
        'fine_cells_all':len(f),'fine_cells_common':int(inside.sum()),
        'fine_common_area_km2':float(inside.sum()*50*50/1e6),
        'fine_cells_outside':int((~inside).sum()),
        'fine_point_record_cells_inside':int(subset.recorded_point_in_cell.sum()),
        'fine_historical_buffer30_inside':int(subset.legacy_30m_centroid_buffer.sum()),
        'expected_max_25_subcells_per_coarse_cell':'not always due to mask clipping and differences in origin',
        'file':str(dest.relative_to(root))}
    dump_json(reportdir(root)/'04_soporte_comun_CANDIDATO.json',rr)
    print('Soporte común CANDIDATO:',rr['fine_cells_common'],'50m cells,',rr['fine_common_area_km2'],'km2')
    return rr
