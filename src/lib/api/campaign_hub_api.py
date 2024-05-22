from src.lib.adapters.response_adapter import Response
from src.lib.api.base_api import BaseClient
from src.utils.decorators import log_request


class CampaignHubClient(BaseClient):
    def __init__(self, host: str, **kwargs):
        super().__init__(host, **kwargs)

    # @log_request
    def get_campaign_layout(self, store_id: str, store_subsidiary_id: str) -> Response:
        """
        Get campaigns by hub
        :param store_id: id of the required store
        :param store_subsidiary_id: id of the required store subsidiary
        :return: response object
        """
        query_params = f"storeId={store_id}&storeSubsidiaryId={store_subsidiary_id}&segmentIds=249"
        endpoint = f"campaign-layout?{query_params}"
        response = self.get(endpoint=endpoint, headers=self.headers)
        return response

    # @log_request
    def get_segments(self) -> Response:
        endpoint = "segment"
        response = self.get(endpoint=endpoint, headers=self.headers)
        return response
