# src/utils.py
from datetime import datetime, timezone

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def iso_to_dt(iso: str):
    from datetime import datetime
    return datetime.fromisoformat(iso)
