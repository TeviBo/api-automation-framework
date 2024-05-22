from src.lib.adapters.response_adapter import Response
from src.lib.api.base_api import BaseClient
from src.utils.decorators import log_request


class CustomerRegisterClient(BaseClient):
    def __init__(self, host, **kwargs):
        super().__init__(host, **kwargs)
        if self.token:
            self.headers.update({'Authorization': self.token})

    # @log_request
    def generate_code(self, phone_number: int, email: str, engagement_id: str, token: str) -> Response:
        """
        Register a new user in the app.
        :param engagement_id: engagement id for registration
        :param token: token for registration
        :param phone_number: user's phone number for registration
        :param email: user email for registration
        :return: response object
        """
        endpoint = 'customer-register/v4/generate-code'
        application_prefix = "agoraJOKR"
        if self.headers.get('X-Application') == 'MRK':
            application_prefix = "merkao"
        payload = {
            "phone": phone_number,
            "email": email,
            f"{application_prefix}TermCondition": True,
            f"{application_prefix}PromotionsOffer": False,
            "engagementId": f"{engagement_id}",
            "token": f"{token}"
        }

        response = self.post(endpoint=endpoint, headers=self.headers, payload=payload)
        return response

    # @log_request
    def validate_code(self, otp_code: str) -> Response:
        """
        Validates the otp code sent to the user's phone
        :param otp_code: otp code for registered phone
        :return: response object
        """
        endpoint = 'customer-register/v3/validate-code'
        payload = {
            "code": otp_code
        }
        response = self.post(endpoint=endpoint, headers=self.headers, payload=payload)
        return response

    # @log_request
    def register_user_password(self, positions: list) -> Response:
        """
        Registers the user password
        :param positions: positions obtained from the keyboard endpoint
        :return: response object
        """
        endpoint = 'customer-register/v3/register-user-password'
        payload = {
            "positions": positions
        }
        response = self.post(endpoint=endpoint, headers=self.headers, payload=payload)
        return response

    # @log_request
    def register_data(self, first_name: str, last_name: str, document: str) -> Response:
        """
        Register the user data
        :param first_name: user first name
        :param last_name: user last name
        :param document: user document number
        :return: response object
        """
        endpoint = 'customer-profile/v7/register-data'
        payload = {
            "name": first_name,
            "lastName": last_name,
            "documentType": "DNI",
            "documentNumber": document,
            "nationality": "Peru",
            "nationalityCode": "pe"
        }
        response = self.post(endpoint=endpoint, headers=self.headers, payload=payload)
        return response
