# src/dao/user_dao.py
import email
from typing import Dict, Optional, List
from .supabase_client import get_client

class UserDAO:
    def __init__(self):
        self.sb = get_client()

    def create(self, name: str, email: str):
        resp = self.sb.table("users").insert({"name": name, "email": email}).execute()
        return resp.data[0] if resp.data else None


    def get_by_email(self, email: str):
        resp = self.sb.table("users").select("*").eq("email", email).execute()
        return resp.data[0] if resp.data else None


    def get_by_id(self, user_id: str) -> Optional[Dict]:
        resp = self.sb.table("users").select("*").eq("id", user_id).execute()
        
        return resp.data[0] if resp.data else None

    def list_all(self) -> List[Dict]:
        resp = self.sb.table("users").select("*").execute()
        return resp.data
