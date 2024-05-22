from typing import List, Dict, Any

from src.lib.infra.models.app.products.pack_product import PackProductModel
from src.lib.infra.models.base.base_product_model import ProductModel


class StoreModel:
    def __init__(self):
        self._data: Dict = {}
        self._store_id: str = ""
        self._store_name: str = ""
        self._store_image: str = ""
        self._small_image_url: str = ""
        self._large_image_url: str = ""
        self._bg_color: str = ""
        self._font_color: str = ""
        self._service_cost: float = 0.0
        self._payment_token: str = ""
        self._external_payment_token: str = ""
        self._view_ranking: int = 0
        self._store_type: str = ""
        self._tags: List[str] = []
        self._commerce_code: str = ""
        self._commerce_name: str = ""
        self._delivery_cost: float = 0.0
        self._hubs: List[Dict[str, Any]] = []
        self._categories: List[Dict[str, Any]] = []
        self._products: List[(ProductModel, Dict)] = []
        self._campaigns: List[Dict[str, Any]] = []
        self._campaigns_by_hub: List[Dict[str, Any]] = []

    # Properties

    @property
    def store_id(self) -> str:
        return self._store_id

    @store_id.setter
    def store_id(self, store_id: str) -> None:
        self._store_id = store_id

    @property
    def store_name(self) -> str:
        return self._store_name

    @store_name.setter
    def store_name(self, store_name: str) -> None:
        self._store_name = store_name

    @property
    def store_image(self) -> str:
        return self._store_image

    @store_image.setter
    def store_image(self, store_image: str) -> None:
        self._store_image = store_image

    @property
    def small_image_url(self) -> str:
        return self._small_image_url

    @small_image_url.setter
    def small_image_url(self, small_image_url: str) -> None:
        self._small_image_url = small_image_url

    @property
    def large_image_url(self) -> str:
        return self._large_image_url

    @large_image_url.setter
    def large_image_url(self, large_image_url: str) -> None:
        self._large_image_url = large_image_url

    @property
    def bg_color(self) -> str:
        return self._bg_color

    @bg_color.setter
    def bg_color(self, bg_color: str) -> None:
        self._bg_color = bg_color

    @property
    def font_color(self) -> str:
        return self._font_color

    @font_color.setter
    def font_color(self, font_color: str) -> None:
        self._font_color = font_color

    @property
    def service_cost(self) -> float:
        return self._service_cost

    @service_cost.setter
    def service_cost(self, service_cost: float) -> None:
        self._service_cost = service_cost

    @property
    def payment_token(self) -> str:
        return self._payment_token

    @payment_token.setter
    def payment_token(self, payment_token: str) -> None:
        self._payment_token = payment_token

    @property
    def external_payment_token(self) -> str:
        return self._external_payment_token

    @external_payment_token.setter
    def external_payment_token(self, external_payment_token: str) -> None:
        self._external_payment_token = external_payment_token

    @property
    def view_ranking(self) -> int:
        return self._view_ranking

    @view_ranking.setter
    def view_ranking(self, view_ranking: int) -> None:
        self._view_ranking = view_ranking

    @property
    def store_type(self) -> str:
        return self._store_type

    @store_type.setter
    def store_type(self, store_type: str) -> None:
        self._store_type = store_type

    @property
    def tags(self) -> List[str]:
        return self._tags

    @tags.setter
    def tags(self, tags: List[str]) -> None:
        self._tags = tags

    @property
    def commerce_code(self) -> str:
        return self._commerce_code

    @commerce_code.setter
    def commerce_code(self, commerce_code: str) -> None:
        self._commerce_code = commerce_code

    @property
    def commerce_name(self) -> str:
        return self._commerce_name

    @commerce_name.setter
    def commerce_name(self, commerce_name: str) -> None:
        self._commerce_name = commerce_name

    @property
    def delivery_cost(self) -> float:
        return self._delivery_cost

    @delivery_cost.setter
    def delivery_cost(self, delivery_cost: float) -> None:
        self._delivery_cost = delivery_cost

    @property
    def hubs(self) -> List[Dict[str, Any]]:
        return self._hubs

    @hubs.setter
    def hubs(self, hubs: List[Dict[str, Any]]) -> None:
        self._hubs = hubs

    @property
    def categories(self) -> List[Dict[str, Any]]:
        return self._categories

    @categories.setter
    def categories(self, categories: List[Dict[str, Any]]) -> None:
        self._categories = categories

    @property
    def products(self) -> List[ProductModel]:
        return self._products

    @products.setter
    def products(self, products: List[Dict[str, Any]]) -> None:
        if isinstance(products, ProductModel):
            self._products = products
        else:
            self._products = [ProductModel(**product) for product in products]

    @property
    def campaigns(self) -> List[Dict[str, Any]]:
        return self._campaigns

    @campaigns.setter
    def campaigns(self, campaigns: List[Dict[str, Any]]) -> None:
        self._campaigns = campaigns

    @property
    def campaigns_by_hub(self) -> List[Dict[str, Any]]:
        return self._campaigns_by_hub

    @campaigns_by_hub.setter
    def campaigns_by_hub(self, campaigns_by_hub: List[Dict[str, Any]]) -> None:
        self._campaigns_by_hub = campaigns_by_hub

    def get_store(self) -> Dict[str, Any]:
        return {
            "store_id": self.store_id,
            "store_name": self.store_name,
            "store_image": self.store_image,
            "small_image_url": self.small_image_url,
            "large_image_url": self.large_image_url,
            "bg_color": self.bg_color,
            "font_color": self.font_color,
            "service_cost": self.service_cost,
            "payment_token": self.payment_token,
            "external_payment_token": self.external_payment_token,
            "view_ranking": self.view_ranking,
            "store_type": self.store_type,
            "tags": self.tags,
            "commerce_code": self.commerce_code,
            "commerce_name": self.commerce_name,
            "delivery_cost": self.delivery_cost,
            "hubs": self.hubs,
            "categories": self.categories,
            "products": self.products,
            "campaigns": self.campaigns,
            "campaigns_by_hub": self.campaigns_by_hub
        }

    def clean(self):
        self.store_id = ""
        self.store_name = ""
        self.store_image = ""
        self.small_image_url = ""
        self.large_image_url = ""
        self.bg_color = ""
        self.font_color = ""
        self.service_cost = 0.0
        self.payment_token = ""
        self.external_payment_token = ""
        self.view_ranking = 0
        self.store_type = ""
        self.tags = []
        self.commerce_code = ""
        self.commerce_name = ""
        self.delivery_cost = 0.0
        self.hubs = []
        self.categories = []
        self.products = []
        self.campaigns = []
        self.campaigns_by_hub = []
