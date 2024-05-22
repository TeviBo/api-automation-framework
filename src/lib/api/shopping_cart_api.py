from typing import Dict, Any

from src.lib.adapters.response_adapter import Response
from src.lib.api.base_api import BaseClient
from src.utils.decorators import retry_payment_on_422
from src.utils.decorators import log_request
from src.utils.logger import logger


class ShoppingCartClient(BaseClient):
    def __init__(self, host, **kwargs):
        super().__init__(host, **kwargs)

    # @log_request
    def add_item_to_cart(self, product, quantity: str) -> Response:
        """
        Add an item to the cart.
            :type product: dict
            :param product: contains all the needed product's data of the item to add (id, stock_price_id, quantity)
            :type quantity: str
            :param quantity: quantity of the product to add
            :return: response object
        """
        store_subsidiary_id = None
        product_stock_price_id = None
        logistic_measurement_unit = None
        url = "ux/shopping-cart/v2/addItem"
        for item in product['productSubsidiary']:
            store_subsidiary_id = item['storeSubsidiaryId']
            product_stock_price_id = item['storeSubsidiaryProductId']
            logistic_measurement_unit = item['logisticMeasurementUnit']
        payload = {
            "storeId": product['storeId'],
            "storeSubsidiaryId": store_subsidiary_id,
            "productId": product['productId'],
            "logisticMeasurementUnit": logistic_measurement_unit,
            "measurementUnitLabel": None,
            "measureIncrementValue": None,
            "productStockPriceId": product_stock_price_id,
            "unitCount": int(quantity)
        }
        response = self.post(endpoint=url, payload=payload)
        return response

    def decrement_cart_item_quantity(self, product, quantity: str) -> Response:
        return self.add_item_to_cart(product, quantity)

    # @log_request
    def get_user_cart(self) -> Response:
        """
        Get the user's cart
            :return: (obj) Response
        """
        endpoint = "ux/shopping-cart/v2/drafted"
        response = self.get(endpoint=endpoint)
        return response

    # @log_request
    def remove_item_from_cart(self, store_id: str, store_subsidiary_id: str, product: dict) -> Response:
        """
        Remove an item from the cart.
        :type store_id: dict
        :param store_id: contains all the needed store's data of the item to remove
        :type store_subsidiary_id: dict
        :param store_subsidiary_id: contains all the needed store subsidiary's data of the item to remove
        :type product: dict
        :param product: contains all the needed product's data of the item to remove (id, stock_price_id, quantity)
        :return: response object
        """
        product_stock_price_id = None
        endpoint = "ux/shopping-cart/v2/removeItem"
        for item in product['productStockPrice']:
            product_stock_price_id = item['productStockPriceId']
        payload = {
            "storeId": store_id,
            "storeSubsidiaryId": store_subsidiary_id,
            "productId": product['product']['productId'],
            "productStockPriceId": product_stock_price_id,
            "unitCount": 1
        }
        response = self.delete(endpoint=endpoint, payload=payload)
        return response

    # @log_request
    def empty_cart(self, store_id: str, store_subsidiary_id: str) -> Response:
        """
        Empty the user's cart.
            :type store_id: str
            :param store_id: ID of the store
            :type store_subsidiary_id: str
            :param store_subsidiary_id: ID of the store subsidiary
            :return:
        """
        endpoint = "ux/shopping-cart/remove"
        payload = {
            "storeId": store_id,
            "storeSubsidiaryId": store_subsidiary_id,
        }
        response = self.delete(endpoint=endpoint, payload=payload)
        return response

    def get_full_data(self, shopping_cart_id: str):
        endpoint = f'/cmd/shopping-cart/full-data/{shopping_cart_id}'
        response = self.get(endpoint=endpoint)
        return response

    # @log_request
    @retry_payment_on_422()
    def checkout(self, action: str, store_id: str, store_subsidiary_id: str, shopping_cart_id: str,
                 shipping_address_id: str = None, payment: (Dict[str, Any], str) = None,
                 coupon: str = None) -> Response:
        """
        Used to update checkout
            :type action: str
            :param action: Action type
            :type store_id: str
            :param store_id: Store id
            :type store_subsidiary_id: str
            :param store_subsidiary_id: Store subsidiary id
            :type shopping_cart_id: str
            :param shopping_cart_id: Shopping cart id
            :type shipping_address_id: str
            :param shipping_address_id: Shipping address id
            :type payment: dict
            :param payment: Dictionary with a card data
            :type coupon: str
            :param coupon: Discount coupon code
            :return: Response object
        """
        action_types = {
            'change_address': ('ADDRESS', {"shippingAddressesId": f"{shipping_address_id}"}),
            'change_payment': (
                'PAYMENT',
                {"paymentId": f"{payment['cardId'] if isinstance(payment, dict) else None}",
                 "paymentTitle": f"{payment['branch'] if isinstance(payment, dict) else None}"}
            ),
            'apply_coupon': ('COUPON', {"couponCode": coupon}),
        }
        endpoint = "ux/shopping-cart/v2/checkout"
        payload = {
            "storeId": store_id,
            "storeSubsidiaryId": store_subsidiary_id,
            "shoppingCartId": shopping_cart_id,
            "promotions": True,
            "isPaymentFailed": False,
            "actionType": action_types[action][0],
            "changeAddress": action_types[action][1] if action == 'change_address' else None,
            "changePayment": action_types[action][1] if action == 'change_payment' else None,
            "changeSlotTime": None,
            "changeInvoice": None,
            "changeCoupon": action_types[action][1] if action == 'apply_coupon' else None
        }
        response = self.put(endpoint=endpoint, payload=payload)
        return response

    # TODO: REVISAR EL PAYLOAD QUE SE ENVIA DESDE MOBILE PARA MERKAO, DUDA CON timeSlotId y timeData
    # @log_request
    @retry_payment_on_422()
    def complete(self, **kwargs) -> Response:
        """
        Complete the checkout by calling the API endpoint "ux/shopping-cart/v2/complete" with the provided parameters.

        :param kwargs: A dictionary containing the following parameters:
            - 'store_id' (str): The ID of the store.
            - 'store_subsidiary_id' (str): The ID of the store subsidiary.
            - 'shopping_cart_id' (str): The ID of the shopping cart.
            - 'shipping_addresses_id' (str): The ID of the shipping address.
            - 'payment_id' (str): The ID of the payment.
            - 'exception_test' (bool): A flag indicating if running in exception test mode.

        :return: The API response as a Response object.
        """
        endpoint = "ux/shopping-cart/v2/complete"
        payload = {
            "storeId": kwargs.get('store_id'),
            "storeSubsidiaryId": kwargs.get('store_subsidiary_id'),
            "shoppingCartId": kwargs.get('shopping_cart_id'),
            "shippingAddressesId": kwargs.get('shipping_addresses_id'),
            "timeSlotId": "JOKR_SLOT_TIME",
            "paymentId": kwargs.get('payment_id'),
            "timeData": "15-25 mins"
        }
        if kwargs.get('payment_id') == "":
            payload["paymentMethod"] = "CASH_ON_DELIVERY"
        if kwargs.get('exception_test'):
            logger.info('Running in exception test mode, PAY_01 errors will not be retried.')
        response = self.post(endpoint=endpoint, payload=payload, headers=self.headers)
        return response

    # @log_request
    def get_orders(self, page: str = 0) -> Response:
        """
        Used to get user orders
        :type page: str
        :param page: Page number to retrieve orders
        :return: (obj) - Response
        """
        endpoint = f"ux/shopping-cart/v2/jobs?pageNumber={page}"
        response = self.get(endpoint=endpoint, headers=self.headers)
        return response
