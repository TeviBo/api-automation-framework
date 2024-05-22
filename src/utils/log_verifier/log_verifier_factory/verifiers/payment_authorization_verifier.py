import json
from typing import Dict, Any

from src.utils.enums import EventType
from src.utils.log_verifier.log_verifier_factory.verifiers.base_verifier import LogVerifier
from src.utils.log_verifier.utils.verifier_utils import generate_repr, validate_class_parameters


@generate_repr
@validate_class_parameters(method_name='validate')
class PaymentAuthorizationVerifier(LogVerifier):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, event_log) -> (AssertionError, None):
        """
        Validate if the payment authorization generated for the order amount is correct
        :param event_log: event returned from Google Cloud Logging query
        :return: AssertionError or None depending on assertions results
        """
        assert event_log != {}, (
            '[ERROR] No se encontraron registros de la autorizacion de cobro en las entradas de Google Cloud Logging.'
            f'\n [EVENT LOG]: {event_log}')
        assert event_log['amount'] == self.app_user.selected_order.bill['totalAmount'], (
            '[ERROR] El monto de la autorizacion de cobro no coincide con el esperado.'
            f'\n [Expected Amount]: {self.app_user.selected_order.bill["totalAmount"]}'
            f'\n [Received Amount]: {event_log["amount"]}'
        )
        buy_order = event_log["buyOrder"].split('_')[0]
        assert buy_order == self.app_user.selected_order.order_number, (
            '[ERROR] El id de la orden de la autorizacion de cobro no coincide con el del pedido.'
            f'\n [Expected BuyOrder]: {self.app_user.selected_order.order_number}'
            f'\n [Received BuyOrder]: {buy_order}'
        )
        assert event_log["status"] == "AUTHORIZED", ('[ERROR] la autorizacion de cobro no fue autorizada.'
                                                     f'\n[Expected Status]: AUTHORIZED'
                                                     f'\n [Received Status]: {event_log["status"]}')

        assert event_log["store"]["commerce"]["name"].split(" ")[0].upper() == self.store_user.store.store_name, (
            '[ERROR] el nombre de la tienda no coincide con el esperado.'
            f'\n [Expected Store]: {self.store_user.store.store_name}'
            f'\n [Received Store]: {event_log["store"]["name"]}'
        )

        assert event_log["trxResponse"] == "Procesada correctamente", (
            '[ERROR] la transaccion no ha sido procesada correctamente'
            f'\n [Received Transaction Response]: {event_log["trxResponse"]}'
        )

    def fetch_logs(self) -> Dict[str, Any]:
        try:
            entries = self.make_request(EventType.PAYMENT_AUTHORIZATION)
            return json.loads(entries[1].split("JSON response ")[1])
        except (AttributeError, IndexError):
            raise AssertionError(
                'No se encontraron registros de la autorizacion de cobro en las entradas de Google Cloud Logging.'
            )
