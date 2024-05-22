from random import randint

from src.lib.infra.models.app.products.app_product_model import ProductModel


class PackProductModel(ProductModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._suggestion: str = ""
        self._suggestion_weight: int = 0
        self._to_delete: bool = False
        self._brandExternalId: str = ""
        self._enabled: bool = False

    # // *** Properties *** //
    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, enabled: bool) -> None:
        self._enabled = enabled

    @property
    def image_url(self) -> str:
        return self.product_image_url

    @property
    def brand_external_id(self) -> str:
        return self._brandExternalId

    @brand_external_id.setter
    def brand_external_id(self, brand_external_id: str) -> None:
        self._brandExternalId = brand_external_id

    @property
    def suggestion(self) -> str:
        return self._suggestion

    @suggestion.setter
    def suggestion(self, suggestion: str) -> None:
        self._suggestion = suggestion

    @property
    def suggestion_weight(self) -> int:
        return self._suggestion_weight

    @suggestion_weight.setter
    def suggestion_weight(self, suggestion_weight: int) -> None:
        self._suggestion_weight = suggestion_weight

    @property
    def to_delete(self) -> bool:
        return self._to_delete

    @to_delete.setter
    def to_delete(self, to_delete: bool) -> None:
        self._to_delete = to_delete

    # // *** Methods *** //

    def get_product(self) -> dict:
        base_prod_data = super().get_product().copy()
        del base_prod_data["productId"]
        del base_prod_data["nutritionalInformation"]
        del base_prod_data["productImageUrl"]
        del base_prod_data["relatedProducts"]
        del base_prod_data["config"]
        base_prod_data.update({
            "plu": self.plu,
            "brandExternalId": self.brand_external_id, "imageUrl": self.image_url,
            'related': {
                'related': {
                    'name': self.related_name if self.related_products != [] else "",
                    'products': self.related_products
                },
                'replacements': {
                    'name': self.replacement_name if self.replacement_products != [] else "",
                    'products': self.replacement_products
                }
            }, "toDelete": self.to_delete,
            "enabled": self.enabled,
            "nutritionalInformation": {
                "highSodium": False,
                "highInSugar": False,
                "highInSaturatedFat": False,
                "containTransFats": False,
                "avoidExcessiveConsumption": False,
                "avoidItsConsumption": False,
            }})
        return base_prod_data

    def create_product(self, category: str, child_category: str, related_products=None, replacement_products=None,
                       promotion_ext_id=None):
        super().create_product(category, child_category, related_products, replacement_products)
        self.suggestion = self.FAKER.word()
        self.suggestion_weight = randint(1, 10)
        self.to_delete = False
        self.brand_external_id = self.brand_label
        self.external_id = promotion_ext_id
        self.sku = promotion_ext_id
        self.plu = promotion_ext_id
