"""Aggregate statistics only. No coordinates or site IDs in output."""
from pathlib import Path
import sys,json
from collections import OrderedDict
root=Path(__file__).resolve().parents[1]
source=root/'reports/private'
out=root/'reports/public'
out.mkdir(exist_ok=True,parents=True)
files=['01_inventario.json','02_grillas_recalculadas.json']
results={}
for f in files:
    p=source/f
    if not p.exists():continue
    d=json.loads(p.read_text(encoding='utf-8'))
    if f.startswith('01'):
        results['inventory']={k:d.get(k) for k in ['n_prior_points','n_unique_xy','coord_inconsistencies','candidate_near_mincul_100m','not_matched_100m']}
    else:
        results['grids']={r:{k:g.get(k) for k in ['resolution_m','grid_cell_count','study_area_as_grid_km2','recorded_point_in_cell_count','legacy_30m_centroid_buffer_count','DEM_missing_or_edge_count']} for r,g in d['grids'].items()}
# aggregated counts can still be sensitive in particular circumstances: check institutional clearance before GitHub commit.
(out/'summary_DRAFT_REVIEW_BEFORE_PUBLICATION.json').write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding='utf-8')
print('Borrador agregado para revisión de permisos, NO publicar automáticamente.')
