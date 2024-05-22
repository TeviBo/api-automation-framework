from datetime import datetime
from typing import List, Dict, Any, Tuple

from src.lib.infra.models.app.products.pack_product import PackProductModel
from src.lib.infra.models.app.products.promotions.promotion_model import PromotionModel
from src.lib.infra.models.base.base_user_model import UserModel
from src.lib.infra.models.store.store_model import StoreModel


class StoreUserModel(UserModel):

    def __init__(self):
        super().__init__()
        self._selected_hub: Dict[str, Any][str, Any] = {}
        self._store: StoreModel = StoreModel()
        self._pack_product: PackProductModel = PackProductModel()
        self._promotions: List[Dict[str, Any]] = []
        self._promotion: PromotionModel = PromotionModel()
        self._selected_category: Dict[str, Any] = {}
        self._selected_child_category: Dict[str, Any] = {}
        self._selected_promotion_pack: Dict[str, Any] = {}

    # // *** Properties *** //

    @property
    def selected_category(self) -> Dict[str, Any]:
        return self._selected_category

    @selected_category.setter
    def selected_category(self, selected_category: Dict[str, Any]) -> None:
        self._selected_category = selected_category

    @property
    def selected_child_category(self) -> Dict[str, Any]:
        return self._selected_child_category

    @selected_child_category.setter
    def selected_child_category(self, selected_child_category: Dict[str, Any]) -> None:
        self.selected_child_category = selected_child_category

    @property
    def promotions(self) -> List[Dict[str, Any]]:
        return self._promotions

    @promotions.setter
    def promotions(self, promotion_kits: List[Dict[str, Any]]) -> None:
        self._promotions = promotion_kits

    @property
    def promotion(self) -> PromotionModel:
        return self._promotion

    @promotion.setter
    def promotion(self, promotion_kit: PromotionModel) -> None:
        self._promotion = promotion_kit

    @property
    def pack_product(self) -> PackProductModel:
        return self._pack_product

    @pack_product.setter
    def pack_product(self, pack_product: PackProductModel) -> None:
        self._pack_product = pack_product

    @property
    def selected_hub(self) -> Dict[str, Any]:
        return self._selected_hub

    @selected_hub.setter
    def selected_hub(self, selected_hub: Dict[str, Any]) -> None:
        self._selected_hub = selected_hub

    @property
    def store(self) -> StoreModel:
        return self._store

    @store.setter
    def store(self, store: (StoreModel, Dict[str, Any])) -> None:
        self._store = store

    @property
    def selected_promotion_pack(self) -> Dict[str, Any]:
        return self._selected_promotion_pack

    @selected_promotion_pack.setter
    def selected_promotion_pack(self, selected_promotion_pack: Dict[str, Any]) -> None:
        self._selected_promotion_pack = selected_promotion_pack

    # // *** Methods *** //

    def get_user(self) -> Dict[str, Any]:
        user_data = super().get_user()
        store_user_data = {
            'selected_hub': self.selected_hub,
            'store': self.store.get_store() if self.store else "",
            'pack_product': self.pack_product.get_product() if self.pack_product else {},
            'promotions': [self.promotion for self.promotion in self.promotions] if self.promotions else [],
            'selected_category': self.selected_category,
            'selected_child_category': self.selected_child_category,
            'selected_promotion_pack': self.selected_promotion_pack
        }
        user_data[self.user_type].update(store_user_data)
        return user_data

    def get_hub(self, hub_code: str) -> None:
        for hub in self.store.hubs:
            if hub["label"] == hub_code:
                self.selected_hub = hub
                break

    def find_category(self, category: str, categories: List[Dict[str, Any]]) -> None:
        for cat in categories:
            if cat.get("name") == category or cat.get("label") == category:
                self.selected_category = cat
                break

    def find_child_category(self, child_category: str, child_categories: List[Dict[str, Any]]) -> None:
        for child_cat in child_categories:
            if child_cat["label"] == child_category:
                self._selected_child_category = child_cat
                break

    @classmethod
    def generate_error_message(cls, product, prod, error_type):
        error_message = f'\n[ERROR] La actualizacion de {error_type} no se realizo correctamente'
        error_message += f'\n [PRODUCT]: {prod.sku} - {prod.label}'

        if error_type == 'stock y precio':
            error_message += f'\n  [Store Stock]: {prod.config[0]["unitAvailable"]}'
            error_message += f'\n  [PMM Response Stock]: {product["unitAvailable"]}'
            error_message += f'\n  [Store Price]: {prod.config[0]["price"]}'
            error_message += f'\n  [PMM Response Price]: {product["price"]}'
        elif error_type == 'precio':
            error_message += f'\n  [Store Price]: {prod.config[0]["price"]}'
            error_message += f'\n  [PMM Response Price]: {product["price"]}'
        elif error_type == 'stock':
            error_message += f'\n  [Store Stock]: {prod.config[0]["unitAvailable"]}'
            error_message += f'\n  [PMM Response Stock]: {product["unitAvailable"]}'

        return error_message

    def validate_stock_update(self, received_products: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
        """
        Validates the stock updated by PMM
        :type received_products: List[Dict[str, Any]]
        :param received_products: List of products received from PMM response
        :return: A Tuple with the result of the validation and a list of errors if some assertion failed
        """

        products_update_errors = []
        store_products_dict = {prod.product_id: prod for prod in self.store.products}

        for product in received_products:
            prod = store_products_dict.get(product["productId"])
            if prod:
                error_message = self.check_product_errors(product, prod)
                if error_message:
                    products_update_errors.append(error_message)

        return not products_update_errors, products_update_errors

    def check_product_errors(self, product, prod):
        if product["unitAvailable"] != prod.config[0]["unitAvailable"] and product["price"] != prod.config[0]["price"]:
            return self.generate_error_message(product, prod, 'stock y precio')
        elif product["price"] != prod.config[0]["price"]:
            return self.generate_error_message(product, prod, 'precio')
        elif product["unitAvailable"] != prod.config[0]["unitAvailable"]:
            return self.generate_error_message(product, prod, 'stock')
        return None

    def filter_active_promotion_packs(self) -> List[Dict[str, Any]]:
        current_datetime = datetime.now().replace(microsecond=0).isoformat()
        promotion_packs = []
        for promotion in self.promotions:
            if promotion["promotionDueDate"] >= current_datetime and promotion.get("name") is not None:
                promotion_packs.append(promotion)
        return promotion_packs

    def clean(self) -> None:
        super().clean()
        self._selected_hub = {}
        self._store = StoreModel()
        self._pack_product = PackProductModel()
        self._promotions = []
        self._promotion = PromotionModel()
        self._selected_category = {}
        self._selected_child_category = {}
        self._selected_promotion_pack = {}
