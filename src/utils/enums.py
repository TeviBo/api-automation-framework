from enum import Enum


class EventType(Enum):
    SALE_NOTE = "ORDER_CREATED"
    PAYMENT_AUTHORIZATION = "authorize"
    PAYMENT_CAPTURE = "CAPTURE_PAYMENT"
    ORDER_INVOICE = "INVOICE"
