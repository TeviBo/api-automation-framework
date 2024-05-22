import datetime
import os.path
from typing import Dict, Any, List

from src.lib.adapters.response_adapter import Response
from src.lib.api.base_api import BaseClient
from src.utils.decorators import retry_on_error
from src.utils.decorators import log_request
from src.utils.utils import go_up_n_dirs


class OTPLib(BaseClient):
    def __init__(self, host, **kwargs):
        super().__init__(host, **kwargs)
        self.headers.update({
            'Host': 'api-qa.agora.pe',
            'User-Agent': 'Apache-HttpClient/4.5.12 (Java/1.8.0_251)',
            'Connection': 'keep-alive'
        })

    # @log_request
    def get_otp_code(self, phone_number: int) -> Response:
        """
        Gets the otp code sent to the user's phone
        :param phone_number: phone number of the registered user
        :return: response object
        """
        service = 'us-ux-customer-register-service'
        device_id = '438e9e341b92876a'
        endpoint = f'agora-quality/automation/otp?service={service}&identifier={phone_number},{device_id}&type=null'
        response = self.get(endpoint=endpoint, headers=self.headers)
        return response


class BackofficeLib(BaseClient):
    def __init__(self, host, **kwargs):
        super().__init__(host, application="BOF", user_id="821c1d65-43c3-4017-b404-811d700e2c88", platform="WEB",
                         device_id="BACK_OFFICE_USER_EXPRESS", **kwargs)
        self.get_keyboard_position = lambda keyboard, requested_position: keyboard.index(requested_position)
        self.get_data_from_body = lambda body, key: body[key]

    # @log_request
    @retry_on_error(exp_status_code=201, retries=5)
    def login(self, identifier: str) -> Response:
        """
        Log in a user using the identifier and the keyboard positions
        :param identifier: user phone number
        :return: response object
        """
        keyboard_response = self.get_random_keyboard()
        position_of_one = self.get_keyboard_position(keyboard_response.body["keyboard"], 1)
        password = [position_of_one, position_of_one, position_of_one, position_of_one, position_of_one,
                    position_of_one]
        endpoint = "agora-public/management/login"
        payload = {
            "identifier": identifier,
            "positions": password
        }
        response = self.post(endpoint=endpoint, payload=payload)
        return response

    # @log_request
    def get_categories(self, store_id: str) -> Response:
        query_params = "pageNumber=1&pageSize=10&name=&root=true"
        endpoint = f"management/category/store/{store_id}?{query_params}"
        response = self.get(endpoint=endpoint)
        return response

    # @log_request
    def get_child_categories(self, store_id: str, category_id: str) -> Response:
        endpoint = f"management/category/store/{store_id}/category/{category_id}"
        response = self.get(endpoint=endpoint)
        return response

    # @log_request
    def get_random_keyboard(self) -> Response:
        """
        Get random keyboard
        :return: response object
        """
        endpoint = "agora-public/management/randomkeyboard"
        response = self.get(endpoint=endpoint)
        return response

    # @log_request
    def get_hubs(self, store_id: str) -> Response:
        endpoint = f'management/subsidiary/store/{store_id}?pageNumber=1&pageSize=10&name='
        response = self.get(endpoint=endpoint)
        return response

    # @log_request
    def bulk_new_products(self, store_id: str) -> Response:
        """
        Uploads a bulk new products file to the system.

        Parameters:
            - store_id (str): The ID of the store to upload the products to.

        Returns:
            - Response: The response from the server.

        Example:
            >>> bulk_new_products("12345")
            <Response [200]>
        """
        endpoint = f"management/product/store/{store_id}/upload"
        root_path = go_up_n_dirs(os.path.abspath(__file__), 3)
        file_path = os.path.join(root_path, 'data', 'xlsx')
        files = [('file', ('Bulk new products.xlsx',
                           open(f'{file_path}/Bulk new products.xlsx', 'rb'),
                           'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))]

        response = self.post(endpoint=endpoint, payload={}, content_type='form-data', files=files)
        return response

    # @log_request
    def update_stock_price_new_products(self, store_id: str, subsidiary_id: str) -> Response:
        """
        :param store_id:
        :param subsidiary_id:
        :return:
        """
        endpoint = f"agora-backoffice-shop/management/product/store/{store_id}/subsidiary/{subsidiary_id}/upload"
        root_path = go_up_n_dirs(os.path.abspath(__file__), 3)
        file_path = os.path.join(root_path, 'data', 'xlsx')
        files = [
            ('file', ('BO edit new products.xlsx',
                      open(f'{file_path}/Update new product stock.xlsx', 'rb'),
                      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
        ]
        response = self.post(endpoint=endpoint, payload={}, headers=self.headers, content_type='form-data', files=files)
        return response

    # @log_request
    def get_all_products(self, store_id: str, subsidiary_id: str, quantity: int) -> Response:
        """
        Get n products from a store based on quantity value
        :type store_id: str
        :param store_id: store where to perform the update
        :type subsidiary_id: str
        :param subsidiary_id: subsidiary id from where retrieve the products
        :type quantity: int
        :param quantity: Quantity of products to get
        :return: response object
        """
        query_params = f"pageNumber=1&pageSize={quantity}&name="
        endpoint = f"management/product/store/{store_id}/subsidiary/{subsidiary_id}?{query_params}"
        response = self.get(endpoint=endpoint, headers=self.headers)
        return response

    # @log_request
    def get_products_by_sku(self, store_id: str, sku, store_subsidiary_id: str = None, ) -> Response:
        q_par = f"pageNumber=1&pageSize=10&sku={sku}"
        if store_subsidiary_id is not None:
            endpoint = (f"management/product/store/{store_id}/subsidiary/{store_subsidiary_id}"
                        f"?{q_par}")
        else:
            endpoint = f"management/product/store/{store_id}?{q_par}"
        response = self.get(endpoint=endpoint)
        return response


class HaertLib(BaseClient):
    def __init__(self, host, **kwargs):
        super().__init__(host, **kwargs)
        self.get_keyboard_position = lambda keyboard, requested_position: keyboard.index(requested_position)
        self.get_data_from_body = lambda body, key: body[key]
        self.headers.update({
            'X-Device-Id': 'BACK_OFFICE_USER_EXPRESS',
            'X-Platform': 'WEB',
            'X-User-ID': 'bo-user',
            'origin': 'https://wapp-jokr-operations-qa.web.app',
        })

    # @log_request
    def get_random_keyboard(self) -> Response:
        """
        Get random keyboard
        :return: response object
        """
        endpoint = "agora-public/management/randomkeyboard"
        response = self.get(endpoint=endpoint, headers=self.headers)
        return response

    # @log_request
    @retry_on_error(exp_status_code=201, retries=5)
    def login(self, identifier: str) -> Response:
        """
        Log in to the system using a provided identifier.

        This method generates a password based on keyboard positions and sends a POST request to the login endpoint
        with the identifier and password. It then returns the response from the server.

        @param identifier: A string representing the identifier of the user.
        @return: A Response object representing the server's response.

        Example usage:
            response = login("user123")
        """
        keyboard_response = self.get_random_keyboard()
        position_of_one = self.get_keyboard_position(keyboard_response.body["keyboard"], 1)
        password = [position_of_one, position_of_one, position_of_one, position_of_one, position_of_one,
                    position_of_one]
        endpoint = "agora-public/management/login"
        payload = {
            "identifier": identifier,
            "positions": password
        }
        response = self.post(endpoint=endpoint, headers=self.headers, payload=payload)
        return response

    # @log_request
    def get_all_promotions(self, store_id: str):
        endpoint = f'stores/{store_id}/products/combo?disabled=false'
        response = self.get(endpoint=endpoint, headers=self.headers)
        return response

    # @log_request
    def get_promotion_detail(self, store_id: str, pack_id: str) -> Response:
        endpoint = f"stores/{store_id}/products/combo/{pack_id}"
        response = self.get(endpoint=endpoint, headers=self.headers)
        return response

    # @log_request
    def upload_promotion_kit(self, store_id: str, promotion_kits: List[Dict[str, Any]]) -> Response:
        endpoint = f"/stores/{store_id}/products/combo/bulk"
        payload = [promotion_kits]
        response = self.post(endpoint=endpoint, payload=payload, headers=self.headers)
        return response

    # @log_request
    def upload_pack_product(self, store_id: str, pack: Dict[str, Any]) -> Response:
        endpoint = f"stores/{store_id}/products/combo/bulk/productKits"
        payload = [pack]
        response = self.post(endpoint=endpoint, payload=payload, headers=self.headers)
        return response

    # @log_request
    def edit_promotion_pack(self, store_id: str, promotion_to_edit: Dict[str, Any]) -> Response:
        endpoint = f"stores/{store_id}/products/combo/{promotion_to_edit['externalId']}"
        if "productPromotionsDetails" in promotion_to_edit:
            promotion_to_edit["products"] = promotion_to_edit.pop("productPromotionsDetails")
        payload = promotion_to_edit
        response = self.put(endpoint=endpoint, payload=payload, headers=self.headers)
        return response


class DADLib(BaseClient):

    def __init__(self, host, **kwargs):
        super().__init__(host, **kwargs)
        if kwargs.get("username"):
            self.headers.update({'username': kwargs.get("username")})
        if kwargs.get("company_code"):
            self.headers.update({'companyCode': kwargs.get("company_code")})

    # @log_request
    def login(self, username: str, password: str) -> Response:
        """
        Login
        :type username: str
        :param username: Username for login
        :type password: str
        :param password: Password for login
        :return: (obj) Response
        """
        endpoint = "auth/login"
        payload = {
            "username": username,
            "password": password
        }
        response = self.post(endpoint=endpoint, payload=payload, headers=self.headers)
        return response

    # @log_request
    @retry_on_error(exp_status_code=200, retries=10, condition="response.body.get('totalRecords') > 0")
    def get_id_dispatch(self, entity_id: str, ean_number: str) -> Response:
        """
        Get the order dispatch id to assign to a picker
        :param entity_id:
        :param ean_number:
        :return:
        """
        endpoint = f'orders/consolidation/dispatch/paginated?' \
                   f'entityId={entity_id}&orderNumber={ean_number}' \
                   '&isPendingPrint=false&hasCdOrigin=false&limit=20&offset=0'

        response = self.get(endpoint=endpoint, headers=self.headers)
        return response

    # @log_request
    @retry_on_error(exp_status_code=201, condition="response.body.get('totalRecords')>=1", retries=10)
    def get_products_ids(self, id_order_dispatch: str) -> Response:
        """
        Get the order products ids for picking
        :param id_order_dispatch: Order dispatch ID
        :return:
        """
        endpoint = f"labelled/detail/{id_order_dispatch}"
        response = self.get(endpoint=endpoint, headers=self.headers)
        return response

    # @log_request
    @retry_on_error(exp_status_code=200, retries=10)
    def assign_order_to_picker(self, products_ids: list[dict]):
        """
        Assign the order to a picker user
        :param products_ids: Products IDs to pick
        :return:
        """
        endpoint = "api/business-irdgco-picking/v1/orders/assign/999/PENDIENTE_PICKING"

        payload = []
        for p_id in products_ids:
            payload.append({"orderId": p_id["id"]})
        response = self.put(endpoint=endpoint, headers=self.headers, payload=payload)
        return response

    # @log_request
    def manual_picking(self, company_code: str, entity_id: str, serial_number: str, sku_code: str, username: str,
                       amount) -> Response:
        """
        This method is used to perform a manual picking operation in the DaD system.

        Parameters:
        - company_code (str): The code of the hub. Example: SPSA-1432
        - entity_id (str): ?
        - serial_number (str): The serial number of the item to be picked.
        - sku_code (str): The code of the SKU (Stock Keeping Unit) to be picked.
        - username (str): The username of the user performing the picking.
        - amount (int): The amount of the item to be picked.

        Returns:
        - Response: The response object containing the result of the manual picking operation.

        Example Usage:
        response = manual_picking('ABC', '123', '98765', 'SKU123', 'john.doe', 5)
        """
        endpoint = 'api/business-irdgco-picking/v1/pick-manual'
        payload = {"companyCode": company_code, "entityId": entity_id, "type": "NO_BAR_CODE_OPTION",
                   "serialNumber": serial_number, "skuCode": sku_code, "amount": amount, "username": username}
        response = self.post(endpoint=endpoint, headers=self.headers, payload=payload)
        return response

    # @log_request
    def synchronize_orders(self, dispatch_id: str, ean_number: str, items: list[dict]) -> Response:
        """
        Synchronizes orders with the Jokr system.

        This method sends a request to the DaD API to synchronize the orders with the provided dispatch ID,
        EAN number, and list of items. The method returns a response object.

        Parameters:
        - dispatch_id (str): The dispatch ID for the orders.
        - ean_number (str): The EAN number for the orders.
        - items (list[dict]): A list of dictionaries representing the items in the order. Each dictionary should contain the following keys:
            - "amountRequested" (int): The requested amount of the item.
            - "amount_to_pick" (int): The amount to be picked for the item.
            - "id" (str): The ID of the order picking.
            - Other optional keys as required.

        Returns:
        - response (Response): The response object from the DaD API request.
        """
        endpoint = "api/business-irdgco-picking/v1/orders/jokr/synchronize"
        jokr_items = []
        for prod in items:
            jokr_items.append({
                "amountMissing": int(prod["amountRequested"]) - prod["amount_to_pick"],
                "amountPicked": str(prod["amount_to_pick"]),
                "amountRequested": prod["amountRequested"],
                "idOrderPicking": prod["id"],
                "reasonCode": "NOT_THE_PRODUCT" if prod["amount_to_pick"] == int(
                    prod["amountRequested"]) else "WITHOUT_STOCK"
            })
        payload = {
            "bags": [
                {
                    "orderDispatchId": dispatch_id,
                    "quantity": 1,
                    "typeBag": "MEDIUM"
                }
            ],
            "dispatchNumber": f"{ean_number}-1",
            "datePackingInit": f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "datePickingFinish": f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "datePickingInit": f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "jokrItems": jokr_items,
            "orderDispatchId": dispatch_id
        }

        response = self.post(endpoint=endpoint, headers=self.headers, payload=payload)
        return response


class BeetrackLib(BaseClient):
    def __init__(self, host, **kwargs):
        super().__init__(host, **kwargs)
        self.headers.update({
            'Content-Type': 'application/json',
            'X-Auth-Token': f'{self.token}'
        })
        del self.headers["Authorization"]

    # @log_request
    def list_routes(self, truck_identifier: str) -> Response:
        """
        List routes
        :param truck_identifier: Truck license plate (Ej.: TEST-123)
        :return: response object
        """
        endpoint = f"routes?date={datetime.datetime.now().strftime('%Y-%m-%d')}&truck_identifier={truck_identifier}"
        response = self.get(endpoint=endpoint, headers=self.headers)
        return response

    # @log_request
    def filter_dispatches(self, customer_identifier: str) -> Response:
        """
        Filter dispatches by customer identifier
        :param customer_identifier: Customer document number
        :return: response object
        """
        endpoint = f"dispatches?i={customer_identifier}"
        response = self.get(endpoint=endpoint, headers=self.headers)
        return response

    # @log_request
    def create_route(self, dispatches: list[dict], truck_identifier: str, driver_identifier: str) -> Response:
        """
        Create a route
        :param dispatches: Dispatch object with delivery data
        :param truck_identifier: Truck license plate (Ej.: TEST-123)
        :param driver_identifier: Truck driver data
        :return: response object
        """
        dispatch_list = []
        for dispatch in dispatches:
            dispatch_list.append(
                {
                    "identifier": dispatch["identifier"],
                    "contact_name": dispatch["contact_name"],
                    "contact_address": dispatch["contact_address"],
                    "contact_phone": dispatch["contact_phone"],
                    "contact_id": dispatch["contact_id"],
                    "contact_email": dispatch["contact_email"],
                    "latitude": dispatch["latitude"],
                    "longitude": dispatch["longitude"],
                    "items": dispatch["items"],
                    "tags": dispatch["tags"]
                })
        endpoint = "/routes"
        payload = {
            "truck_identifier": truck_identifier,
            "date": datetime.datetime.now().strftime('%Y-%m-%d'),
            "driver_identifier": driver_identifier,
            "dispatches": dispatch_list
        }
        response = self.post(endpoint=endpoint, payload=payload, headers=self.headers)
        return response

    # @log_request
    def update_route(self, route_id: str, truck_id: str, dispatches: list[dict], substatus: dict) -> Response:
        """
        Update route status
        :param truck_id: Truck license plate (Ej.: TEST-123)
        :param route_id: Route ID to be updated
        :param dispatches: Dispatch list with dispatch orders data
        :param substatus: Sub status dictionary to update order status
        :return: Response object
        """
        lst_dispatches = []
        for dispatch in dispatches:
            lst_dispatches.append({
                "identifier": dispatch["identifier"],
                "contact_name": dispatch["contact_name"],
                "contact_address": dispatch["contact_address"],
                "contact_phone": dispatch["contact_phone"],
                "contact_id": dispatch["contact_id"],
                "contact_email": dispatch["contact_email"],
                "latitude": dispatch["latitude"],
                "longitude": dispatch["longitude"],
                "status": substatus["status_id"],
                "substatus": substatus["name"],
                "substatus_code": substatus["code"],
                "items": dispatch["items"],
            })
        endpoint = f"routes/{route_id}"
        payload = {
            "truck_id": truck_id,
            "started_at": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "ended_at": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "dispatches": lst_dispatches
        }

        response = self.put(endpoint=endpoint, payload=payload, headers=self.headers)
        return response
