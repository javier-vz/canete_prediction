"""Read-only checks: no original source bytes are modified or extracted."""
from __future__ import annotations
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import zipfile

SENSITIVE_TYPES = {".csv", ".xlsx", ".xls", ".kml", ".kmz", ".gpx", ".shp", ".gpkg", ".tif", ".tiff", ".jpg", ".png"}

def sha256_file(path: Path) -> str:
    hashobj = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            hashobj.update(block)
    return hashobj.hexdigest()


def csv_profile(path: Path) -> dict:
    """Read CSV once: schema, labels, row count, and missing counts; no coordinates in report."""
    with path.open("r", newline="", encoding="utf-8-sig", errors="replace") as fh:
        reader = csv.DictReader(fh)
        columns = reader.fieldnames or []
        if not columns:
            return {"rows": 0, "columns": [], "warnings": ["CSV sin cabecera"]}
        row_count = 0
        missing = Counter()
        label_counts = Counter()
        labels = [c for c in ("label", "presencia_sitio_nuevo", "presencia_sitio_total", "total_site_presence") if c in columns]
        for row in reader:
            row_count += 1
            for col in columns:
                if row.get(col, "").strip().lower() in {"", "nan", "null", "none", "na"}:
                    missing[col] += 1
            for label in labels:
                label_counts[(label, row[label])] += 1
        return {"rows": row_count, "columns": columns, "missing_by_column": dict(missing), "labels": {f"{c}:{v}": n for (c, v), n in label_counts.items()}}


def zip_profile(path: Path) -> dict:
    # Inspect member index only; never decompress or execute notebooks.
    with zipfile.ZipFile(path) as z:
        members = [i for i in z.infolist() if not i.is_dir()]
        unsafe = [i.filename for i in members if i.filename.startswith(("/", chr(92))) or ".." in Path(i.filename).parts]
        return {"member_count": len(members), "total_uncompressed_bytes": sum(i.file_size for i in members),
                "extension_counts": dict(Counter(Path(i.filename).suffix.lower() for i in members)),
                "members": [{"name": i.filename, "bytes": i.file_size, "crc32": f"{i.CRC:08x}"} for i in members],
                "unsafe_member_paths": unsafe}


def inventory(root: Path) -> dict:
    root = Path(root)
    entries = []
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        item = {"path": p.relative_to(root).as_posix(), "bytes": p.stat().st_size, "sha256": sha256_file(p), "suffix": p.suffix.lower()}
        try:
            if p.suffix.lower() == ".csv":
                item["table"] = csv_profile(p)
            elif p.suffix.lower() == ".zip":
                item["archive"] = zip_profile(p)
        except (OSError, UnicodeError, ValueError, zipfile.BadZipFile) as exc:
            item["inspection_error"] = str(exc)
        entries.append(item)
    groups = {}
    for item in entries:
        groups.setdefault(item["sha256"], []).append(item["path"])
    return {"files": entries, "count": len(entries), "duplicates_by_sha256": [v for v in groups.values() if len(v)>1],
            "notice": "Inventario privado: puede contener nombres de fuentes sensibles; no publicar."}


def write_report(report: dict, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = ["# Inventario local privado", "", f"Archivos inspeccionados: **{report['count']}**", "",
               "| Archivo | Tipo | Tamaño (MB) | SHA-256 abreviado | Registros CSV |", "|---|---|---:|---|---:|"]
    for item in report["files"]:
        rows = item.get("table", {}).get("rows", "—")
        summary.append(f"| {item['path'].replace('|', '/')} | {item['suffix']} | {item['bytes']/1e6:.2f} | {item['sha256'][:12]} | {rows} |")
    summary.extend(["", f"Grupos de duplicados exactos: **{len(report['duplicates_by_sha256'])}**", "", "No subir este informe privado a GitHub."])
    target.with_suffix('.md').write_text(chr(10).join(summary) + chr(10), encoding='utf-8')
