from dataclasses import dataclass
from datetime import datetime


@dataclass
class Payment:
    amount: int
    order_id: int
    session_id: str
    payment_url: str
    status_code: str
    order_description: str
    currency: str
    language_code: str


@dataclass
class PaymentStatus:
    order_id: int
    status_code: str
    state: str


@dataclass
class PaymentInformation:
    order_id: int
    session_id: str
    order_type: str
    state: str
    amount: int
    order_description: str
    fee: int
    create_date: datetime
    pay_date: datetime or None