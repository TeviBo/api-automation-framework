from src.lib.adapters.response_adapter import Response
from src.lib.api.base_api import BaseClient
from src.utils.decorators import log_request


class OAuth(BaseClient):
    def __init__(self, host, **kwargs):
        super().__init__(host, **kwargs)

    # @log_request
    def get_access_token(self) -> Response:
        """
        Gets the access token for the API
        :type: object
        :return: ResponseHandler
        """
        endpoint = "oauth/access-token"
        self.headers.update(
            {'Host': 'api-qa.agora.pe', 'Content-Length': '29', 'Content-Type': 'application/x-www-form-urlencoded'})
        payload = 'grant_type=client_credentials'

        response = self.post(endpoint=endpoint, headers=self.headers, payload=payload, auth=self.token,
                             content_type="application/x-www-form-urlencoded")
        return response
