import json
from typing import Dict, Any

from src.utils.enums import EventType
from src.utils.log_verifier.log_verifier_factory.verifiers.base_verifier import LogVerifier
from src.utils.log_verifier.utils.verifier_utils import generate_repr, validate_class_parameters


@generate_repr
@validate_class_parameters(method_name='validate')
class SaleNoteVerifier(LogVerifier):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, event_log: Dict[str, Any]) -> (AssertionError, None):
        """
        Validate if the sale note generated for the order is correct
        :param event_log: event returned from Google Cloud Logging query
        :return: AssertionError or None depending on assertions results
        """
        assert event_log != {}, (
            '[ERROR] No se encontraron registros de la nota de venta en las entradas de Google Cloud Logging.'
            f'\n [EVENT LOG]: {event_log}')
        self.validate_metadata(event_log)
        self.validate_payment(event_log)
        self.validate_delivery(event_log)
        self.validate_products(event_log)

        assert event_log["origin"]["code"] == self.store_user.selected_hub["externalId"], (
            '[ERROR] el codigo del hub no coincide con el esperado.'
            f'\n [Expected Hub Code]: {self.store_user.selected_hub["externalId"]}'
            f'\n [Received Hub Code]: {event_log["payment"]["saleEntityCode"]}'
        )

    def validate_metadata(self, event_log):
        """
        Validate metadata related fields
        """
        assert event_log["metadata"]["identifiers"][
                   "shoppingCartId"] == self.app_user.cart.shopping_cart_id, (
            '[ERROR] El id del carrito no coincide con el esperado.'
            f'\n [Expected ShoppingCartId]: {self.app_user.selected_order.shopping_cart_id}'
            f'\n [Received ShoppingCartId]: {event_log["metadata"]["identifiers"]["shoppingCartId"]}'
        )
        assert event_log["metadata"]["identifiers"]["userId"] == self.app_user.session["userId"], (
            '[ERROR] El id del usuario no coincide con el esperado.'
            f'\n [Expected UserId]: {self.app_user.session["userId"]}'
            f'\n [Received UserId]: {event_log["metadata"]["identifiers"]["userId"]}'
        )
        assert event_log["metadata"]["eventName"] == EventType.SALE_NOTE.value, (
            '[ERROR] El tipo de evento no coincide con el esperado.'
            f'\n [Expected Event Type]: ORDER_CREATED'
            f'\n [Received Event Type]: {event_log["metadata"]["eventName"]}'
        )

    def validate_payment(self, event_log):
        """Validate payment related fields"""

        # Ecommerce id es el id de la orden generada desde la app
        assert event_log["payment"]["ecommerceId"] == self.app_user.selected_order.order_number, (
            '[ERROR] El id de la orden no coincide con el esperado.'
            f'\n [Expected EcommerceId]: {self.app_user.selected_order.order_number}'
            f'\n [Received EcommerceId]: {event_log["payment"]["ecommerceId"]}'
        )
        assert event_log["payment"]["saleEntity"] == self.store_user.selected_hub["label"], (
            '[ERROR] el hub no coincide con el esperado.'
            f'\n [Expected Hub]: {self.store_user.selected_hub["label"]}'
            f'\n [Received Hub]: {event_log["payment"]["saleEntity"]}'
        )

        assert event_log["payment"]["saleEntityCode"] == self.store_user.selected_hub["externalId"], (
            '[ERROR] el codigo del hub no coincide con el esperado.'
            f'\n [Expected Hub Code]: {self.store_user.selected_hub["externalId"]}'
            f'\n [Received Hub Code]: {event_log["payment"]["saleEntityCode"]}'
        )
        if self.app_user.application.upper() == "JKR":
            assert event_log["payment"]["storeFormat"] == "JOKR", (
                '[ERROR] el formato de la tienda no coincide con el esperado.'
                f'\n [Expected Store Format]: JOKR'
                f'\n [Received Store Format]: {event_log["payment"]["storeFormat"]}'
            )
            assert event_log["payment"]["paymentMethod"] == "AGORA_SHOP", (
                '[ERROR] el metodo de pago no coincide con el esperado.'
                f'\n [Expected Payment Method]: AGORA_SHOP'
                f'\n [Received Payment Method]: {event_log["payment"]["paymentMethod"]}'
            )
        else:
            assert event_log["payment"]["storeFormat"] == "MERKAO", (
                '[ERROR] el formato de la tienda no coincide con el esperado.'
                f'\n [Expected Store Format]: LIM013'
                f'\n [Received Store Format]: {event_log["payment"]["storeFormat"]}'
            )
            payment_method = "CASH_ON_DELIVERY"
            if payment_method == "CASH_ON_DELIVERY":
                assert event_log["payment"]["paymentMethod"] == "CASH_ON_DELIVERY", (
                    '[ERROR] el metodo de pago no coincide con el esperado.'
                    f'\n [Expected Payment Method]: {payment_method}'
                    f'\n [Received Payment Method]: {event_log["payment"]["paymentMethod"]}'
                )
            else:
                assert event_log["payment"]["paymentMethod"] == "CREDIT_CARD", (
                    '[ERROR] el metodo de pago no coincide con el esperado.'
                    f'\n [Expected Payment Method]: CREDIT_CARD'
                    f'\n [Received Payment Method]: {event_log["payment"]["paymentMethod"]}'
                )

    def validate_delivery(self, event_log):
        """Validate delivery related fields"""
        assert event_log["delivery"]["deliveryAddress"]["address"] == self.app_user.selected_address["trackName"], (
            '[ERROR] la direccion de entrega no coincide con la esperada.'
            f'\n [Expected Delivery Address]: {self.app_user.selected_address["trackName"]}'
            f'\n [Received Delivery Address]: {event_log["delivery"]["deliveryAddress"]["address"]}'
        )
        assert event_log["delivery"]["deliveryAddress"]["reference"] == self.app_user.selected_address["reference"], (
            '[ERROR] la referencia de la direccion de entrega no coincide con la esperada.'
            f'\n [Expected Delivery Address Reference]: {self.app_user.selected_address["reference"]}'
            f'\n [Received Delivery Address Reference]: {event_log["delivery"]["deliveryAddress"]["reference"]}'
        )
        assert event_log["delivery"]["deliveryAddress"]["addressNumber"] == self.app_user.selected_address[
            "trackNumber"], (
            '[ERROR] el numero de la direccion de entrega no coincide con el esperado.'
            f'\n [Expected Delivery Address Number]: {self.app_user.selected_address["trackNumber"]}'
            f'\n [Received Delivery Address Number]: {event_log["delivery"]["deliveryAddress"]["addressNumber"]}'
        )
        assert event_log["delivery"]["code"] == self.store_user.selected_hub["externalId"], (
            '[ERROR] el codigo del hub no coincide con el esperado.'
            f'\n [Expected Hub Code]: {self.store_user.selected_hub["externalId"]}'
            f'\n [Received Hub Code]: {event_log["payment"]["saleEntityCode"]}'
        )

    def validate_products(self, event_log):
        """Validate products related fields"""
        assert len(event_log["products"]) == len(self.app_user.cart.items), (
            '[ERROR] la cantidad de productos no coincide con la esperada.'
            f'\n [Expected Products]: {len(self.app_user.cart.items)}'
            f'\n [Received Products]: {len(event_log["products"])}'
        )

        products_dict = {product["skuCode"]: product for product in event_log["products"]}

        for item in self.app_user.cart.items:
            product_log = products_dict.get(item["product"]["productSku"])
            if not product_log or float(item["product"]["unitPriceAmount"]) != float(product_log["price"]) or int(
                    item["product"]["unitCount"]) != int(product_log["quantity"]):
                return False
        return True

    def fetch_logs(self) -> Dict[str, Any]:
        try:
            entries = self.make_request(EventType.SALE_NOTE)
            for log in entries:
                return json.loads(log.split("body:")[1])
        except (AttributeError, IndexError):
            raise AssertionError(
                "[ERROR] No se encontraron registros de la nota de venta en las entradas de Google Cloud Logging.")
