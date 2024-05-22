from src.lib.adapters.response_adapter import Response
from src.lib.api.base_api import BaseClient
from src.utils.decorators import log_request


class Products(BaseClient):
    def __init__(self, host: str, **kwargs):
        super().__init__(host, **kwargs)
        if kwargs.get("access_token"):
            self.headers.update({"Authorization": f"Bearer {kwargs.get('access_token')}"})
            del self.headers["access_token"]

    # @log_request
    def pmm_loading(self, store_id: str, subsidiary_id: str, products_to_update: list[dict]) -> Response:
        endpoint = f"v2/stores/{store_id}/store-subsidiaries/{subsidiary_id}/product-stock-price/bulk"
        payload = []
        for product in products_to_update:
            payload.append({
                "externalProductId": product['sku'],
                "unitAvailable": product['unit_available'],
                "price": product['price']
            })
        response = self.post(endpoint=endpoint, payload=payload, headers=self.headers)
        return response
