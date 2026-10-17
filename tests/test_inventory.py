import csv
from pathlib import Path
import tempfile
import sys
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from canete_prediction.inventory import inventory, csv_profile, zip_profile
from canete_prediction.staging import stage

class InventoryTests(unittest.TestCase):
    def test_csv_labels(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/"synthetic.csv"
            p.write_text("x,y,label\n1,1,0\n2,2,1\n3,3,\n",encoding="utf8")
            r=csv_profile(p)
            self.assertEqual(r["rows"],3)
            self.assertEqual(r["labels"]["label:1"],1)
            self.assertEqual(r["missing_by_column"]["label"],1)
    def test_staging_dedupes(self):
        with tempfile.TemporaryDirectory() as temp:
            a=Path(temp)/"inbox";a.mkdir()
            (a/"grilla_1.csv").write_text("foo",encoding="utf8")
            (a/"grilla_2.csv").write_text("foo",encoding="utf8")
            raw=Path(temp)/"raw"
            logs=stage(a,raw)
            self.assertEqual(sum(x['action']=='moved_to_private_raw' for x in logs),1)
            self.assertEqual(sum(x['action']=='duplicate_not_moved' for x in logs),1)
    def test_zip_index_does_not_extract(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/"a.zip"
            with zipfile.ZipFile(p,'w') as z:z.writestr('a.txt','sample')
            self.assertEqual(zip_profile(p)['member_count'],1)
            self.assertFalse((Path(temp)/'a.txt').exists())

if __name__ == '__main__': unittest.main()
