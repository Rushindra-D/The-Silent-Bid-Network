# src/dao/bid_dao.py
from typing import Dict, List, Optional
from decimal import Decimal
from .supabase_client import get_client

class BidDAO:
    def __init__(self):
        self.sb = get_client()

    def create_sealed(self, auction_id: str, bidder_id: str, commitment: str) -> Dict:
        payload = {
            "auction_id": auction_id,
            "bidder_id": bidder_id,
            "commitment": commitment,
            "amount": None,
            "revealed": False
        }
        resp = self.sb.table("bids").insert(payload).execute()
    
        return resp.data[0]

    def reveal(self, bid_id: str, amount: Decimal) -> Dict:
        resp = self.sb.table("bids").update({"amount": str(amount), "revealed": True}).eq("id", bid_id).execute()
        
        return resp.data[0]

    def get(self, bid_id: str) -> Optional[Dict]:
        resp = self.sb.table("bids").select("*").eq("id", bid_id).limit(1).execute()
        
        return resp.data[0] if resp.data else None

    def list_public(self, auction_id: str) -> List[Dict]:
        # public: ids only (no amounts)
        resp = self.sb.table("bids").select("id, bidder_id, created_at").eq("auction_id", auction_id).execute()
    
        return resp.data

    def list_revealed(self, auction_id: str) -> List[Dict]:
        resp = self.sb.table("bids").select("*").eq("auction_id", auction_id).eq("revealed", True).order("amount", desc=True).execute()
        
        return resp.data
