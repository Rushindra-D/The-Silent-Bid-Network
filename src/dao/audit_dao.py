# src/dao/audit_dao.py
from typing import Dict
from .supabase_client import get_client

class AuditDAO:
    def __init__(self):
        self.sb = get_client()

    def log(self, entity: str, entity_id: str, action: str, details: Dict) -> Dict:
        resp = self.sb.table("audit_log").insert({
            "entity": entity,
            "entity_id": entity_id,
            "action": action,
            "details": details
        }).execute()
    
        return resp.data[0]
