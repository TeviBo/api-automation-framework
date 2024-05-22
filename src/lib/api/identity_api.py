from src.lib.adapters.response_adapter import Response
from src.lib.api.base_api import BaseClient
from src.utils.decorators import log_request


class IdentityClient(BaseClient):
    def __init__(self, host: str, **kwargs):
        super().__init__(host, **kwargs)

    # @log_request
    def get_keyboard(self) -> Response:
        """
        Sends a GET request to retrieve the mobile keyboard positions.

        Returns:
            Response: The response of the request.

        """
        endpoint = 'keyboard'

        response = self.get(endpoint=endpoint, headers=self.headers)
        return response

    # @log_request
    def login(self, identifier: str, positions: list[int], engagement_id: str, token: str) -> Response:
        """
        Method: login

        This method allows a user to log in to the system using their identifier, positions, engagement ID, and token.

        Parameters:
        - identifier (str): The unique identifier of the user.
        - positions (list[int]): The list of positions associated with the user.
        - engagement_id (str): ?.
        - token (str): The authentication token.

        Returns:
        - Response: The response object containing the result of the login request.

        Example Usage:
        response = obj.login(identifier="user123", positions=[1, 2, 3], engagement_id="engagement123", token="xyz123")

        Note:
        - This method is decorated with the `log_request` decorator, which logs the request before and after execution.
        - The `endpoint`, `headers`, and `logger` properties are assumed to be defined within the class that contains this method.
        """
        endpoint = 'sign-in'
        payload = {
            "identifier": identifier,
            "positions": positions,
            "engagementId": f"{engagement_id}",
            "token": f"{token}"
        }
        response = self.post(endpoint=endpoint, payload=payload, headers=self.headers)
        return response
