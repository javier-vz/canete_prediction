from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import unittest
import numpy as np
import pandas as pd
from canete_rebuild.grids import build_label_arrays,make_grid
from canete_rebuild.inventory import make_inventory

class ArchaeologicalWorkflowTests(unittest.TestCase):
    def test_prior_chronology_unknown_institution(self):
        df=pd.DataFrame({'x':[350000.], 'y':[8550000.], 'lon':[-76.38], 'lat':[-13.12]})
        inv=make_inventory(df,threshold_m=100)
        self.assertEqual(inv.loc[0,'chronology'],'PRE_DINA_FIELDWORK_USER_CONFIRMED')
        self.assertEqual(inv.loc[0,'source_group'],'MINCUL_OR_PAVC_UNRESOLVED')
        self.assertFalse(bool(inv.loc[0,'mincul_spatial_candidate']))
    def test_point_in_cell_not_absence(self):
        # adjacent 50m cells; registry point inside one, other remains unlabelled
        x=np.array([25.,75.]);y=np.array([25.,25.])
        exact,legacy,d=build_label_arrays(x,y,[26.],[26.],50,30)
        self.assertEqual(exact.tolist(),[1,0])
        self.assertEqual(legacy.tolist(),[1,0])
        grid,_=make_grid(pd.DataFrame({'x':x,'y':y}),pd.DataFrame({'x':[26.],'y':[26.]}),50,30)
        self.assertTrue((grid.background_status=='UNLABELLED_NOT_CONFIRMED_ABSENCE').all())
        self.assertNotIn('dist_sitio_mas_cercano',grid.columns)
    def test_boundary_point_may_touch_two_cells(self):
        a,_,_=build_label_arrays([25.,75.],[25.,25.],[50.],[25.],50,30)
        self.assertEqual(a.tolist(),[1,1])

if __name__=='__main__':unittest.main()
