import json
from typing import Dict, Any

from src.utils.enums import EventType
from src.utils.log_verifier.log_verifier_factory.verifiers.base_verifier import LogVerifier
from src.utils.log_verifier.utils.verifier_utils import validate_class_parameters, generate_repr, \
    generate_error_message


@generate_repr
@validate_class_parameters(method_name='validate')
class PaymentCaptureVerifier(LogVerifier):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, event_log: Dict[str, Any]):
        assert event_log != {}, (
            '[ERROR] No se encontraron registros de la captura de cobro en las entradas de Google Cloud Logging.'
            f'\n [EVENT LOG]: {event_log}')

        assert event_log["header"]["eventTag"] == "CAPTURE_PAYMENT", (
            f"[ERROR] El tag del evento no coincide con el esperado."
            f"\n [Expected Event Tag]: CAPTURE_PAYMENT"
            f"\n [Received Event Tag]: {event_log['header']['eventTag']}"
        )
        assert event_log["header"]["userId"] == self.app_user.session["userId"], (
            f"[ERROR] El id del usuario no coincide con el esperado."
            f"\n [Expected User Id]: {self.app_user.session['userId']}"
            f"\n [Received User Id]: {event_log['header']['userId']}"
        )
        self.validate_payment_data(event_log)
        self.validate_shopping_cart(event_log)

    def validate_payment_data(self, event_log: Dict[str, Any]):
        for data in event_log["body"]["paymentData"]:
            if len(data) > 0:
                assert data["amount"] == self.app_user.selected_order.bill["totalAmount"], (
                    f"[ERROR] El monto del pago no coincide con el esperado."
                    f"\n [Expected Amount]: {self.app_user.selected_order.total_amount}"
                    f"\n [Received Amount]: {data['amount']}"
                )

    def validate_shopping_cart(self, event_log: Dict[str, Any]):
        shopping_cart = event_log["body"].get("shoppingCart")
        assert shopping_cart["shopperPhoneNumber"] == self.app_user.identifier, (
            f"[ERROR] El número de teléfono del cliente no coincide con el esperado."
            f"\n [Expected Shopper Phone Number]: {self.app_user.identifier}"
            f"\n [Received Shopper Phone Number]: {shopping_cart['shopperPhoneNumber']}"
        )

        assert shopping_cart["status"] == "SHIPPED", (
            f"[ERROR] El estado del carrito de compras no coincide con el esperado."
            f"\n [Expected Status]: SHIPPED"
            f"\n [Received Status]: {shopping_cart['status']}"
        )
        assert shopping_cart["shoppingCartId"] == self.app_user.selected_order.cart["shoppingCartId"], (
            f'[ERROR] El id del carrito de compras no coincide con el esperado.'
            f'\n [Expected Shopping Cart Id]: {self.app_user.selected_order.cart["shoppingCartId"]}'
            f'\n [Received Shopping Cart Id]: {shopping_cart["shoppingCartId"]}'
        )

        assert f'{shopping_cart["subAmount"]:.2f}' == f'{self.app_user.selected_order.bill["subTotalAmount"]:.2f}', (
            f"[ERROR] El monto del carrito de compras no coincide con el esperado."
            f'\n [Expected Sub Amount]: {self.app_user.selected_order.bill["subTotalAmount"]:.2f}'
            f'\n [Received Sub Amount]: {shopping_cart["subAmount"]:.2f}'
        )

        assert f'{shopping_cart["totalAmount"]:.2f}' == f'{self.app_user.selected_order.bill["totalAmount"]:.2f}', (
            f'[ERROR] El monto total de la orden de compras no coincide con el esperado.'
            f'\n [Expected Total Amount]: {self.app_user.selected_order.bill["totalAmount"]:.2f}'
            f'\n [Received Total Amount]: {shopping_cart["totalAmount"]:.2f}'
        )

        assert shopping_cart["orderNumber"] == self.app_user.selected_order.order_number, (
            f'[ERROR] El número de orden de compras no coincide con el esperado.'
            f'\n [Expected Order Number]: {self.app_user.selected_order.order_number}'
            f'\n [Received Order Number]: {shopping_cart["orderNumber"]}'
        )

        assert shopping_cart["storeId"] == self.store_user.store.store_id, (
            f'[ERROR] El id de la tienda no coincide con el esperado.'
            f'\n [Expected Store Id]: {self.store_user.store.store_id}'
            f'\n [Received Store Id]: {shopping_cart["storeId"]}'
        )

        assert shopping_cart["storeSubsidiaryId"] == self.store_user.selected_hub["storeSubsidiaryId"], (
            f'[ERROR] El id de la sucursal no coincide con el esperado.'
            f'\n [Expected Store Subsidiary Id]: {self.store_user.selected_hub['storeSubsidiaryId']}'
            f'\n [Received Store Subsidiary Id]: {shopping_cart["storeSubsidiaryId"]}'
        )

        assert shopping_cart["paymentMethodId"] == self.app_user.cart.payment["paymentId"], (
            f'[ERROR] El id del método de pago no coincide con el esperado.'
            f'\n [Expected Payment Method Id]: {self.app_user.cart.payment["paymentId"]}'
            f'\n [Received Payment Method Id]: {shopping_cart["paymentMethodId"]}'
        )

        assert shopping_cart["paymentCardNumber"][-4:] == self.app_user.cart.payment["description"][-4:], (
            f'[ERROR] El número de tarjeta de crédito no coincide con el esperado.'
            f'\n [Expected Payment Card Number]: {self.app_user.cart.payment['description'].split(" ")[3]}'
            f'\n [Received Payment Card Number]: {shopping_cart["paymentCardNumber"].split(" ")[3]}'
        )

        assert shopping_cart["shippingAddressesId"] == self.app_user.selected_address["shippingAddressesId"], (
            f'[ERROR] El id de la dirección de envío no coincide con el esperado.'
            f'\n [Expected Shipping Addresses Id]: {self.app_user.selected_address["shippingAddressesId"]}'
            f'\n [Received Shipping Addresses Id]: {shopping_cart["shippingAddressesId"]}'
        )

        assert shopping_cart["addressLatitude"] == self.app_user.selected_address["latitude"], (
            f"[ERROR] La dirección de envío no coincide con la esperada."
            f"\n [Expected Address Latitude]: {self.app_user.selected_address['latitude']}"
            f"\n [Received Address Latitude]: {shopping_cart['addressLatitude']}"
        )

        assert shopping_cart["addressLongitude"] == self.app_user.selected_address["longitude"], (
            f"[ERROR] La dirección de envío no coincide con la esperada."
            f"\n [Expected Address Longitude]: {self.app_user.selected_address['longitude']}"
            f"\n [Received Address Longitude]: {shopping_cart['addressLongitude']}"
        )

        products_dict = {product["product"]["productId"]: product for product in self.app_user.cart.items}

        for item in event_log["body"]["shoppingCartItem"]:
            product = products_dict.get(item["productId"])
            if product:
                assert item["unitCount"] == product["product"]["unitCount"], generate_error_message(
                    product['product']['unitCount'], item['unitCount'], product['product']['sku'], "Unit Count"
                )
                assert item["price"] == product["productStockPrice"][0]["price"], generate_error_message(
                    product["productStockPrice"][0]["price"], item['price'], product['product']['sku'], "Price"
                )
                assert item["apportionAmount"] >= 0.0, generate_error_message(
                    ">= 0", item['apportionAmount'], product['product']['sku'], "Apportion Amount"
                )
            else:
                raise AssertionError(
                    f"[ERROR] El producto no se encontro en el carrito de compras."
                    f"\n [SKU]: {item['productId']}"
                )

    def fetch_logs(self) -> Dict[str, Any]:
        entries = self.make_request(EventType.PAYMENT_CAPTURE)
        try:
            parsed_input = json.loads(entries[0].split('[EVENT] ')[1])
        except (AttributeError, IndexError):
            raise AssertionError(
                'No se encontraron registros de la captura de cobro en las entradas de Google Cloud Logging.'
            )
        return parsed_input
