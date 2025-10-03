# src/services/bid_service.py
from typing import Dict, Optional, List
from decimal import Decimal
from datetime import datetime, timezone
from src.dao.bid_dao import BidDAO
from src.dao.auction_dao import AuctionDAO
from src.dao.audit_dao import AuditDAO

class BidError(Exception):
    pass

class BidService:
    def __init__(self):
        self.dao = BidDAO()
        self.auction_dao = AuctionDAO()
        self.audit = AuditDAO()

    def place_sealed(self, auction_id: str, bidder_id: str, commitment: str) -> Dict:
        if not commitment or not commitment.strip():
            raise BidError("Commitment required")
        auction = self.auction_dao.get(auction_id)
        if not auction:
            raise BidError("Auction not found")
        now = datetime.now(timezone.utc)
        start = datetime.fromisoformat(auction["start_time"])
        end = datetime.fromisoformat(auction["end_time"])
        if not (start <= now <= end):
            raise BidError("Auction not open for bidding")
        b = self.dao.create_sealed(auction_id, bidder_id, commitment)
        self.audit.log("bid", b["id"], "create_sealed", {"auction_id": auction_id, "bidder_id": bidder_id})
        return b

    def reveal(self, bid_id: str, amount: float) -> Dict:
        if amount <= 0:
            raise BidError("Amount must be positive")
        bid = self.dao.get(bid_id)
        if not bid:
            raise BidError("Bid not found")
        if bid.get("revealed"):
            raise BidError("Bid already revealed")
        revealed = self.dao.reveal(bid_id, Decimal(str(amount)))
        self.audit.log("bid", bid_id, "reveal", {"amount": amount})
        return revealed

    def list_public(self, auction_id: str) -> List[Dict]:
        return self.dao.list_public(auction_id)

    def list_revealed(self, auction_id: str) -> List[Dict]:
        return self.dao.list_revealed(auction_id)

    def declare_winner(self, auction_id: str) -> Optional[Dict]:
        auction = self.auction_dao.get(auction_id)
        if not auction:
            raise BidError("Auction not found")
        # close auction if not closed
        if not auction.get("is_closed"):
            self.auction_dao.close(auction_id)
        revealed = self.dao.list_revealed(auction_id)
        if not revealed:
            return None
        # sort: highest amount first, tie-breaker earliest created_at
        from decimal import Decimal
        def key(b):
            amt = Decimal(b["amount"])
            dt = datetime.fromisoformat(b["created_at"])
            return (-amt, dt.timestamp())
        revealed_sorted = sorted(revealed, key=key)
        top = revealed_sorted[0]
        if Decimal(str(top["amount"])) < Decimal(str(auction["reserve_price"])):
            return None
        self.audit.log("auction", auction_id, "declare_winner", {"bid_id": top["id"], "bidder_id": top["bidder_id"], "amount": top["amount"]})
        return {"bid_id": top["id"], "bidder_id": top["bidder_id"], "amount": top["amount"]}
