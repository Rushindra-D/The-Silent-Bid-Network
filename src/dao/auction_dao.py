# src/dao/auction_dao.py
from typing import Dict, Optional, List
from .supabase_client import get_client

class AuctionDAO:
    def __init__(self):
        self.sb = get_client()

    def create(self, payload: Dict) -> Dict:
        resp = self.sb.table("auctions").insert(payload).execute()
    
        return resp.data[0]

    def get(self, auction_id: str) -> Optional[Dict]:
        resp = self.sb.table("auctions").select("*").eq("id", auction_id).limit(1).execute()

        return resp.data[0] if resp.data else None

    def list_open(self) -> List[Dict]:
        resp = self.sb.table("auctions").select("*").eq("is_closed", False).execute()
    
        return resp.data

    def close(self, auction_id: str) -> Dict:
        resp = self.sb.table("auctions").update({"is_closed": True}).eq("id", auction_id).execute()
        
        return resp.data[0]
