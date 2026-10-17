from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import unittest
from pathlib import Path
import tempfile
import geopandas as gpd
from shapely.geometry import box
from canete_rebuild.grids import grid_xy_polygon

class PolygonGridTests(unittest.TestCase):
    def test_generate_exact_two_scales(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'test.geojson'
            gpd.GeoDataFrame({'name':['synthetic']},geometry=[box(0,0,500,500)],crs='EPSG:32718').to_file(p,driver='GeoJSON')
            a=grid_xy_polygon(p,50)
            b=grid_xy_polygon(p,250)
            self.assertEqual(len(a),100)
            self.assertEqual(len(b),4)
