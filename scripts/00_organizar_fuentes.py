from pathlib import Path
import json
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from canete_prediction.staging import stage

if __name__ == "__main__":
    inbox = ROOT / "data" / "private" / "inbox"
    raw = ROOT / "data" / "private" / "raw"
    inbox.mkdir(parents=True, exist_ok=True)
    changes = stage(inbox, raw)
    out = ROOT / "reports" / "private" / "staging_log.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(changes, ensure_ascii=False, indent=2), encoding='utf-8')
    for c in changes: print(f"{c['action']}: {c['source']}")
    print(f"Log privado: {out}")
