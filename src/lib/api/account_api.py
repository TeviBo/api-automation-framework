from src.lib.adapters.response_adapter import Response
from src.lib.api.base_api import BaseClient
from src.utils.decorators import log_request


class AccountClient(BaseClient):
    def __init__(self, host, **kwargs):
        super().__init__(host, **kwargs)

    # @log_request
    def get_cards(self) -> Response:
        """
        Get credit cards from user
            :return: (obj) response
        """
        endpoint = "account/cards/bbr"
        response = self.get(endpoint=endpoint, headers=self.headers)
        return response
