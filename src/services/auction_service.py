# src/services/auction_service.py
from typing import Dict, Optional, List
from decimal import Decimal
from datetime import datetime, timezone
from src.dao.auction_dao import AuctionDAO
from src.dao.audit_dao import AuditDAO

class AuctionError(Exception):
    pass

class AuctionService:
    def __init__(self):
        self.dao = AuctionDAO()
        self.audit = AuditDAO()

    def create(self, title: str, description: str, reserve_price: float, start: datetime, end: datetime, creator_id: str) -> Dict:
        if end <= start:
            raise AuctionError("end must be after start")
        payload = {
            "title": title,
            "description": description,
            "reserve_price": str(reserve_price),
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
            "created_by": creator_id
        }
        auction = self.dao.create(payload)
        self.audit.log("auction", auction["id"], "create", {"title": title})
        return auction

    def get(self, auction_id: str) -> Optional[Dict]:
        return self.dao.get(auction_id)

    def list_open(self) -> List[Dict]:
        return self.dao.list_open()

    def close(self, auction_id: str) -> Dict:
        closed = self.dao.close(auction_id)
        self.audit.log("auction", auction_id, "close", {})
        return closed
