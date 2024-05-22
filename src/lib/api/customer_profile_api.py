from src.lib.adapters.response_adapter import Response
from src.lib.api.base_api import BaseClient
from src.utils.decorators import log_request


class CustomerProfileClient(BaseClient):
    def __init__(self, host, **kwargs):
        super().__init__(host, **kwargs)

    # @log_request
    def get_addresses(self) -> Response:
        """
        Get all addresses from user
        :return: response object
        """
        endpoint = "customer-profile/shipping/addresses"
        response = self.get(endpoint=endpoint, headers=self.headers)
        return response

    # @log_request
    def add_new_address(self, new_address: dict) -> Response:
        """
        Add a new address to the user
        :type new_address: dict
        :param new_address: dictionary with all the address data
        :return: response object
        """
        endpoint = "customer-profile/shipping/addresses"
        payload = new_address
        response = self.post(endpoint=endpoint, headers=self.headers, payload=payload)
        return response

    # @log_request
    def get_address_detail(self, address_id: str) -> Response:
        """
        Gets the address detail
        :param address_id: Address id
        :return: response object
        """
        endpoint = f"customer-profile/shipping/addresses/{address_id}"

        response = self.get(endpoint=endpoint, headers=self.headers)
        return response

    # @log_request
    def delete_address(self, address_id: str) -> Response:
        """
        Delete an address
        :type address_id: str
        :param address_id: address id
        :return: response object
        """
        endpoint = f"customer-profile/shipping/addresses/{address_id}"
        response = self.delete(endpoint=endpoint, headers=self.headers)
        return response

    # @log_request
    def get_flags(self):
        """
        Get the flags for the user
        :return: Response object
        """
        endpoint = "customer-profile/flags"
        response = self.get(endpoint=endpoint, headers=self.headers)
        return response

    # @log_request
    def get_registration_verification(self) -> Response:
        endpoint = 'customer-profile/registration/verification'
        response = self.get(endpoint=endpoint, headers=self.headers)
        return response

    # @log_request
    def get_user_profile(self) -> Response:
        endpoint = '/customer-profile/v3/data'
        response = self.get(endpoint=endpoint, headers=self.headers)
        return response
