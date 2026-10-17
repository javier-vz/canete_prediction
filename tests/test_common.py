from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import unittest
import numpy as np
from canete_rebuild.common_support import fine_within_coarse
class CommonMaskTests(unittest.TestCase):
    def test_inside_coarse_square(self):
        inside,indices=fine_within_coarse(np.array([[50.,50.],[124.,124.],[126.,126.],[400.,400.]]),np.array([[0.,0.]]),250)
        self.assertEqual(inside.tolist(),[True,True,False,False])
