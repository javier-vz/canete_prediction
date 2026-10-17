from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from canete_prediction.inventory import inventory, write_report

if __name__ == "__main__":
    source = ROOT / "data" / "private" / "raw"
    dest = ROOT / "reports" / "private" / "inventory.json"
    source.mkdir(parents=True, exist_ok=True)
    output = inventory(source)
    write_report(output, dest)
    print(f"Archivos: {output['count']} | Duplicados exactos: {len(output['duplicates_by_sha256'])}")
    print(f"Informe privado: {dest}")
    if not output['count']:
        print("Carpeta sin datos originales. Copia primero los ZIP/CSV/XLSX en data/private/inbox y ejecuta 00_organizar_fuentes.py")
