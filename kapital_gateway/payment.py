from dataclasses import dataclass


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