"""Verifica SHA-256 del conjunto de fuentes privadas incluidas en el paquete local."""
from pathlib import Path
import hashlib, json, sys
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'metadata/input_manifest.json').read_text(encoding='utf-8'))
errors=[]
for entry in manifest['input_files']:
    p=ROOT/entry['path']
    if not p.is_file():
        errors.append(f"FALTA: {entry['path']}")
        continue
    if p.stat().st_size!=entry['size_bytes']:
        errors.append(f"TAMAÑO DIFERENTE: {entry['path']}")
        continue
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(4*1024*1024),b''):h.update(chunk)
    if h.hexdigest()!=entry['sha256']:errors.append(f"SHA256 DIFERENTE: {entry['path']}")
print(f"Comprobados {len(manifest['input_files'])} archivos originales.")
if errors:
    for e in errors:print(e)
    sys.exit(1)
print('OK: todas las fuentes coinciden con el manifiesto.')
