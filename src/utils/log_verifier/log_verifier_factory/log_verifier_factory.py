from collections import UserDict
from typing import Dict, Any

from src.utils.log_verifier.log_verifier_factory.verifiers.order_invoice_verifier import OrderInvoiceVerifier
from src.utils.log_verifier.log_verifier_factory.verifiers.payment_authorization_verifier import \
    PaymentAuthorizationVerifier
from src.utils.log_verifier.log_verifier_factory.verifiers.payment_capture_verifier import PaymentCaptureVerifier
from src.utils.log_verifier.log_verifier_factory.verifiers.sale_note_verifier import SaleNoteVerifier


class LogVerifierFactory(UserDict):
    def __init__(self):
        super().__init__({
            "NOTA DE VENTA": SaleNoteVerifier,
            "AUTORIZACION DE COBRO": PaymentAuthorizationVerifier,
            "CAPTURA DE COBRO": PaymentCaptureVerifier,
            "FACTURA DE COMPRA": OrderInvoiceVerifier
        })

    def create_validator(self, event_type, *args, **kwargs):
        event_type = event_type.upper()
        if event_type not in self:
            raise ValueError(f"Invalid event type '{event_type}' provided.")
        validator = self[event_type]
        return validator(*args, **kwargs)


def validate_logs(event_type, *args, **kwargs) -> Dict[str, Any]:
    factory = LogVerifierFactory()
    validator = factory.create_validator(event_type, *args, **kwargs)
    event_log = validator.fetch_logs()
    validator.validate(event_log)
    return event_log
