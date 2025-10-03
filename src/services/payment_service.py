# src/services/payment_service.py
from src.dao.payment_dao import PaymentDAO
from src.dao.audit_dao import AuditDAO

class PaymentError(Exception):
    pass

class PaymentService:
    def __init__(self):
        self.dao = PaymentDAO()
        self.audit = AuditDAO()

    def record(self, auction_id: str, bid_id: str, payer_id: str, amount: float):
        pay = self.dao.record_payment(auction_id, bid_id, payer_id, amount)
        self.audit.log("payment", pay["id"], "record", {"auction_id": auction_id, "bid_id": bid_id, "payer_id": payer_id, "amount": amount})
        return pay
