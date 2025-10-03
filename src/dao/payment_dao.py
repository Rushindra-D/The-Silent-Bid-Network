# src/dao/payment_dao.py
from typing import Dict
from .supabase_client import get_client

class PaymentDAO:
    def __init__(self):
        self.sb = get_client()

    def record_payment(self, auction_id: str, bid_id: str, payer_id: str, amount: float) -> Dict:
        resp = self.sb.table("payments").insert({
            "auction_id": auction_id,
            "bid_id": bid_id,
            "payer_id": payer_id,
            "amount_paid": amount
        }).execute()
        return resp.data[0]
