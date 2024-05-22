import string

from src.lib.infra.models.base.base_user_model import UserModel
from src.lib.infra.models.external.dad.dad_order_model import DADOrderModel
from src.lib.infra.models.external.dad.dad_product_model import DADProductModel


class DADUserModel(UserModel):
    def __init__(self, **kwargs):
        super().__init__()
        self.password: str = "Aa38796212$"
        self.first_name: str = kwargs.get("name")
        self.last_name: str = kwargs.get("lastName")
        self._data = kwargs
        self.session = {
            'access_token': kwargs.get('access_token'),
            'refresh_token': kwargs.get('refresh_token'),
            'token_type': kwargs.get('token_type'),
            'expires_in': kwargs.get('expires_in'),
        }
        self._order: (DADOrderModel, dict) = {}
        self._products_to_pick: list[(DADProductModel, dict)] = []
        self._selected_product: (DADProductModel, dict) = {}
        self.picked_products: list[(DADProductModel, dict)] = []

    # Properties
    @property
    def picked_products(self) -> list[(DADProductModel, dict)]:
        return self._picked_products

    @picked_products.setter
    def picked_products(self, products: list[(DADProductModel, dict)]) -> None:
        self._picked_products = [DADProductModel(**product) for product in products]

    @property
    def products_to_pick(self) -> list[(DADProductModel, dict)]:
        return self._products_to_pick

    @products_to_pick.setter
    def products_to_pick(self, products: list[(DADProductModel, dict)]) -> None:
        self._products_to_pick = [DADProductModel(**product) for product in products]

    @property
    def selected_product(self) -> (DADProductModel, dict):
        return self._selected_product

    @selected_product.setter
    def selected_product(self, product: (DADProductModel, dict)) -> None:
        if isinstance(product, DADProductModel):
            self._selected_product = product
        else:
            self._selected_product = DADProductModel(**product)

    @property
    def username(self) -> str:
        return self._data.get('username')

    @username.setter
    def username(self, value: str) -> None:
        self._data['username'] = value

    @property
    def roles(self) -> list[str]:
        return self._data.get('roles')

    @roles.setter
    def roles(self, value: list) -> None:
        self._data['roles'] = value

    @property
    def entity(self) -> dict:
        return self._data.get('entity')

    @entity.setter
    def entity(self, value: dict) -> None:
        self._data['entity'] = value

    @property
    def entities(self) -> list[dict]:
        return self._data.get('entities')

    @entities.setter
    def entities(self, value: list) -> None:
        self._data['entities'] = value

    @property
    def permissions(self) -> list[str]:
        return self._data.get('permissions')

    @permissions.setter
    def permissions(self, value: list) -> None:
        self._data['permissions'] = value

    @property
    def order_to_pick(self) -> (DADOrderModel, dict):
        return self._order

    @order_to_pick.setter
    def order_to_pick(self, value: dict) -> None:
        self._order = DADOrderModel(**value)

    def get_user(self) -> dict:
        user_data = super().get_user()
        dad_user_data = {
            'username': self.username,
            'roles': self.roles,
            'entity': self.entity,
            'entities': self.entities,
            'permissions': self.permissions,
            'order_to_pick': self.order_to_pick.get_order() if type(
                self.order_to_pick) is DADOrderModel else self.order_to_pick,
            'products_to_pick': [product.get_product() if type(product) is DADProductModel else product for product in
                                 self.products_to_pick],
            'selected_product': self.selected_product.get_product() if type(
                self.selected_product) is DADProductModel else self.selected_product,
            'picked_products': [product.get_product() if type(product) is DADProductModel else product for product in
                                self.picked_products],

        }
        user_data[self.user_type].update(dad_user_data)
        return user_data

    def find_category(self, category: str, categories: list[dict]) -> dict:
        # Find category in the list of categories
        pass

    def find_child_category(self, child_category: str, child_categories: list[dict]) -> dict:
        # Find child category in the list of child categories
        pass

    def find_product(self, product_to_find: str, products: list[(DADProductModel, dict)]) -> None:
        for prod in products:
            if isinstance(prod, dict):
                if prod["label"] == product_to_find:
                    self.selected_product = DADProductModel(**prod)
                    break
            else:
                if prod.label == product_to_find:
                    self.selected_product = prod
                    break

    def validate_products_to_pick(self, products: list[dict]) -> bool:
        def normalize_string(s):
            # Convert to lowercase and remove punctuation
            translator = str.maketrans("", "", string.punctuation)
            return s.replace("Bolsa ", "").lower().translate(translator)

        def compare_strings(str1: str, str2: str):
            return normalize_string(str1) == normalize_string(str2)

        for product in products:
            found = False
            for item in self.products_to_pick:
                if (
                        product["product"]["productSku"] == item.sku
                        and str(int(product["product"]["unitCount"])) == item.amount_requested
                        and compare_strings(product["product"]["productLabel"], item.label)
                ):
                    found = True
                    break  # Exit inner loop if a match is found for the current product
            if not found:
                return False  # If no match found for any product, return False
        return True  # If all products have a match, return True

    def clean(self) -> None:
        super().clean()
        self.username = ""
        self.roles = []
        self.entity = {}
        self.entities = []
        self.permissions = []
        self.order_to_pick = {}
        self.products_to_pick = []
        self.selected_product = {}
