"""Conservatively organize incoming original files into private source folders."""
from __future__ import annotations
from pathlib import Path
import shutil
from .inventory import sha256_file

def category(name: str) -> str:
    s=name.lower()
    if "grilla" in s and name.lower().endswith('.csv'):
        return "original_grids"
    if "primera salida" in s or "puntos l_l" in s:
        return "field_records"
    if "mapas" in s:
        return "cartography"
    if "código" in s or "codigo" in s or "agua y putnos" in s:
        return "historical_code"
    if "cuerpos de agua" in s:
        return "hydrology_bundle"
    return "unclassified"

def stage(inbox: Path, raw: Path):
    inbox, raw = Path(inbox), Path(raw)
    raw.mkdir(parents=True, exist_ok=True)
    logs=[]
    # Hash once, retain duplicate version paths as entries in private manifest, do not overwrite.
    existing={sha256_file(p):p for p in raw.rglob('*') if p.is_file()}
    for src in sorted(inbox.iterdir()):
        if not src.is_file(): continue
        digest=sha256_file(src)
        if digest in existing:
            logs.append({"source":src.name,"action":"duplicate_not_moved", "same_content_as":existing[digest].relative_to(raw).as_posix(),"sha256":digest})
            continue
        destdir=raw/category(src.name);destdir.mkdir(parents=True,exist_ok=True)
        dest=destdir/src.name
        if dest.exists():
            logs.append({"source":src.name,"action":"name_collision_manual_review","sha256":digest})
            continue
        shutil.move(str(src),str(dest))
        existing[digest]=dest
        logs.append({"source":src.name,"action":"moved_to_private_raw","destination":dest.relative_to(raw).as_posix(),"sha256":digest})
    return logs
