import json
from typing import List, Dict, Any

from src.utils.enums import EventType
from src.utils.log_verifier.log_verifier_factory.verifiers.base_verifier import LogVerifier


class OrderInvoiceVerifier(LogVerifier):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, event_log):
        assert event_log != {}, (
            '[ERROR] No se encontraron registros de la factura en las entradas de Google Cloud Logging.'
            f'\n [EVENT LOG]: {event_log}')

        assert event_log["idOrdenpago"] == self.app_user.selected_order.order_number, (
            f"[ERROR] El número de orden de pago no coincide con el esperado."
            f"\n [Expected Order Number]: {self.app_user.selected_order.order_number}"
            f"\n [Received Order Number]: {event_log['idOrdenpago']}"
        )

        assert event_log["ordVtexId"] == self.app_user.selected_order.order_number, (
            f"[ERROR] El vtexId de la orden no coincide con el esperado."
            f"\n [Expected Order Id]: {self.app_user.selected_order.order_number}"
            f"\n [Received Order Id]: {event_log['ordVtexId']}"
        )

        assert event_log["storeId"] == self.store_user.store.store_name, (
            f"[ERROR] El nombre de la tienda no coincide con el esperado."
            f"\n [Expected Store Name]: {self.store_user.store.store_name}"
            f"\n [Received Store Name]: {event_log['storeId']}"
        )

        address = (f'{self.app_user.selected_address["trackType"].capitalize()} '
                   f'{self.app_user.selected_address["trackName"]} '
                   f'{self.app_user.selected_address["trackNumber"]}, '
                   f'{self.app_user.selected_address["districtName"]}'
                   )

        assert event_log["address1"] == address, (
            f"[ERROR] La dirección de la factura no coincide con la esperada."
            f"\n [Expected Address]: {address}"
            f"\n [Received Address]: {event_log['address1']}"
        )

        assert event_log["clientPhone"] == self.app_user.identifier, (
            f"[ERROR] El número de teléfono del cliente no coincide con el esperado."
            f"\n [Expected Phone Number]: {self.app_user.identifier}"
            f"\n [Received Phone Number]: {event_log['clientPhone']}"
        )

        assert f'{event_log["montoTotal"]:.2f}' == f'{self.app_user.selected_order.bill["totalAmount"]:.2f}', (
            f"[ERROR] El monto total de la factura no coincide con el esperado."
            f"\n [Expected Total Amount]: {self.app_user.selected_order.bill['totalAmount']:.2f}"
            f"\n [Received Total Amount]: {event_log['montoTotal']:.2f}"
        )

        assert event_log["payCardnumber"][-4:] == self.app_user.selected_payment_method["pan"][-4:], (
            f"[ERROR] Los últimos 4 dígitos de la tarjeta de pago no coinciden con los esperados."
            f"\n [Expected Last 4 Digits]: {self.app_user.selected_payment_method['pan'][-4:]}"
            f"\n [Received Last 4 Digits]: {event_log['payCardnumber'][-4:]}"
        )
        self.validate_products(event_log["details"])

        assert event_log["details"][-1]["prdFullName"] == "DESPACHOS E-COMMERCE", (
            f"[ERROR] El nombre del producto no coincide con el esperado."
            f"\n [Expected Product Name]: DESPACHOS E-COMMERCE"
            f"\n [Received Product Name]: {event_log['details'][-1]['prdFullName']}"
        )

        assert event_log["details"][-1]["ordVtexPunit"] == self.store_user.selected_hub['deliveryCost'], (
            f"[ERROR] El costo de envío no coincide con el esperado."
            f"\n [Expected Delivery Cost]: {self.store_user.selected_hub['deliveryCost']}"
            f"\n [Received Delivery Cost]: {event_log['details'][-1]['ordVtexPunit']}"
        )

    def validate_products(self, products: List[Dict[str, Any]]):
        for item in products[:-1]:
            assert item["ordVtexId"] == self.app_user.selected_order.order_number, (
                f"[ERROR] El vtexId del producto no coincide con el esperado."
                f"\n [Expected Product Id]: {self.app_user.selected_order.order_number}"
                f"\n [Received Product Id]: {item['ordVtexId']}"
            )
            for prod in self.app_user.cart.items:
                assert any(
                    item["prdLvlNumber"] == prod["product"]["productSku"] for prod in self.app_user.cart.items), (
                    f"[ERROR] El producto con SKU '{item['prdLvlNumber']}' no se encuentra en la orden."
                )
                if item["prdLvlNumber"] == prod["product"]["productSku"]:
                    assert item["prdFullName"] == prod["product"]["productLabel"], (
                        f"[ERROR] El nombre del producto no coincide con el esperado."
                        f"\n [Expected Product Name]: {prod['product']['productLabel']}"
                        f"\n [Received Product Name]: {item['prdFullName']}"
                    )
                    assert item["ordVtexQty"] == int(prod["product"]["unitCount"]), (
                        f"[ERROR] La cantidad del producto no coincide con la esperada."
                        f"\n [Expected Product Quantity]: {prod['product']['unitCount']}"
                        f"\n [Received Product Quantity]: {item['ordVtexQty']}"
                    )

    def fetch_logs(self):
        try:
            entries = self.make_request(EventType.ORDER_INVOICE)
            parsed_input = json.loads(entries[0].split('body: ')[1])
            return parsed_input
        except (AttributeError, IndexError):
            raise AssertionError(
                'No se encontraron registros de la factura en las entradas de Google Cloud Logging.'
            )
