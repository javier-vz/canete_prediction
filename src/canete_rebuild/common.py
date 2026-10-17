from __future__ import annotations
import hashlib
import json
from pathlib import Path
import yaml
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

def config(path=None):
    p = Path(path) if path is not None else ROOT / 'configs' / 'project.yml'
    return yaml.safe_load(p.read_text(encoding='utf-8'))

def source(key, cfg, root=ROOT):
    return root / 'data' / 'private' / 'raw' / cfg['source_files'][key]

def derived(root=ROOT):
    path = root / 'data' / 'private' / 'derived'
    path.mkdir(parents=True, exist_ok=True)
    return path

def reportdir(root=ROOT):
    path = root / 'reports' / 'private'
    path.mkdir(parents=True, exist_ok=True)
    return path

def sha256(path):
    d = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            d.update(chunk)
    return d.hexdigest()

def dump_json(path, obj):
    Path(path).write_text(json.dumps(obj, indent=2, ensure_ascii=False, default=str), encoding='utf-8')

def required_columns(df, names, which):
    missing = set(names) - set(df)
    if missing:
        raise ValueError(f'{which}: faltan columnas {sorted(missing)}')

