from src.lib.adapters.response_adapter import Response
from src.lib.api.base_api import BaseClient
from src.utils.decorators import log_request


class QryCatalogClient(BaseClient):
    def __init__(self, host: str, **kwargs):
        super().__init__(host, **kwargs)

    # @log_request
    def get_categories_by_store(self, store_id: str):
        """
        Get categories by store
        :param store_id: id of the required store
        :return: response object
        """
        endpoint = f"qry/catalog/stores/{store_id}/full-categories"

        response = self.get(endpoint=endpoint, headers=self.headers)
        return response

    # @log_request
    def get_products_by_category(self, category_id: str, store_subsidiary_id: str) -> Response:
        query_params = f"categoryId={category_id}&storeSubsidiaryId={store_subsidiary_id}&sort=DEFAULT"
        endpoint = f"qry/catalog/products/product-categories?{query_params}"
        response = self.get(endpoint=endpoint, headers=self.headers)
        return response

    # @log_request
    def get_store_subsidiary_by_location(self, latitude: float, longitude: float) -> Response:
        query_params = f"latitude={latitude}&longitude={longitude}"
        endpoint = f"qry/catalog/store-subsidiaries/location?{query_params}"
        response = self.get(endpoint=endpoint, headers=self.headers)
        return response

    # @log_request
    def search_products(self, store_id: str, store_subsidiary_id: str, word: str) -> Response:
        """
        Search products by category, name or brand depending on the word parameter.
        E.g: word = 'bebidas' -> Search products by category

            :param store_id:
            :param store_subsidiary_id:
            :param word:
            :return:
        """
        query_params = f"word={word}&storeId={store_id}&storeSubsidiaryId={store_subsidiary_id}&sort=DEFAULT"
        endpoint = f"qry/catalog/products/keyword?pageSize=30&pageNumber=1&{query_params}"
        response = self.get(endpoint=endpoint, headers=self.headers)
        return response

    # @log_request
    def get_autocomplete_suggestions(self, store_id: str, store_subsidiary_id: str, term: str) -> Response:
        """
        Get autocomplete suggestions for a given term.
            :param store_id:
            :param store_subsidiary_id:
            :param term:
            :return:
        """
        endpoint = f"qry/catalog/stores/{store_id}/storeSubsidiaries/{store_subsidiary_id}/suggest?term={term}"
        response = self.get(endpoint=endpoint, headers=self.headers)
        return response
