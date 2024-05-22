from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from src.utils.enums import EventType
from src.utils.log_verifier.utils.verifier_decorators import retry_decorator
from src.utils.logger import GoogleCloudLoggingClient


class LogVerifier(ABC):
    _google_client: GoogleCloudLoggingClient = Optional[GoogleCloudLoggingClient]
    _sale_note_log_gateway_dad: str = Optional[str]
    _sale_note_log_shopping_cart: str = Optional[str]

    @abstractmethod
    def __init__(self, *args, **kwargs):
        if not self._google_client:
            raise AssertionError("Google Cloud Logging Client is not initialized. "
                                 "Take a look at your environment.py file it should be initialized there.")
        self.__app_user = kwargs.get('app_user')
        self.__store_user = kwargs.get('store_user')
        self.__container_name = kwargs.get('container_name')

    @property
    def app_user(self):
        return self.__app_user

    @property
    def store_user(self):
        return self.__store_user

    @property
    def container_name(self):
        return self.__container_name

    @abstractmethod
    def validate(self, event_log: Dict[str, Any]):
        pass

    @abstractmethod
    def fetch_logs(self) -> Dict[str, Any]:
        pass

    @retry_decorator(max_retries=20, delay=3)
    def make_request(self, event_type: EventType):
        if not self.__app_user and not self.__container_name:
            raise AttributeError(f"A query required value is None.\n [EVENT]: {event_type.value.upper()}"
                                 f"\n [ORDER NUMBER]: {self.__app_user.selected_order.order_number}"
                                 f"\n [CONTAINER NAME]: {self.__container_name}"
                                 f"\n [APP USER IDENTIFIER]: {self.__app_user.identifier}"
                                 f"\n [APPLICATION]: {self.__app_user.application.upper()}")
        query = (f'textPayload:"{self.__app_user.identifier}" '
                 f'AND textPayload: "{self.__app_user.selected_order.order_number}" '
                 f'AND textPayload:"{event_type.value}" '
                 f'AND textPayload: "{self.__app_user.application.upper()}" ')
        if event_type == EventType.ORDER_INVOICE:
            query += 'AND NOT textPayload: "invoiceRuc" '
        log_entry = self._google_client.filter_logs(filter_string=query, container_name=self.__container_name)
        return log_entry
