from src.lib.adapters.response_adapter import Response
from src.lib.api.base_api import BaseClient
from src.utils.decorators import log_request


class OrdersClient(BaseClient):
    def __init__(self, host, **kwargs):
        super().__init__(host, **kwargs)

    # @log_request
    def tracking(self, order_number: str) -> Response:
        """
        Used to get order detail
        :type order_number: str
        :param order_number: Order number generated from checkout
        :return: (obj) - Response
        """
        endpoint = f"ux/orders/tracking?orderNumber={order_number}"
        response = self.get(endpoint=endpoint, headers=self.headers)
        return response
