# src/models.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    id: str
    name: str
    email: str
    created_at: Optional[datetime] = None

@dataclass
class Auction:
    id: str
    title: str
    description: Optional[str]
    reserve_price: float
    start_time: str
    end_time: str
    created_by: Optional[str]
    is_closed: bool = False
    created_at: Optional[str] = None

@dataclass
class Bid:
    id: str
    auction_id: str
    bidder_id: Optional[str]
    commitment: Optional[str]
    amount: Optional[float]
    revealed: bool = False
    created_at: Optional[str] = None
