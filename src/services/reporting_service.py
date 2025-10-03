# src/services/reporting_service.py
from typing import Dict
from src.dao.auction_dao import AuctionDAO
from src.dao.bid_dao import BidDAO

class ReportingService:
    def __init__(self):
        self.auction = AuctionDAO()
        self.bid = BidDAO()

    def summary(self, auction_id: str) -> Dict:
        a = self.auction.get(auction_id)
        revealed = self.bid.list_revealed(auction_id)
        total_revealed = len(revealed)
        highest = revealed[0] if revealed else None
        return {"auction": a, "total_revealed": total_revealed, "highest": highest}
