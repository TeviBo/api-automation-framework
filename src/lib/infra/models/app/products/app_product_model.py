from typing import List, Dict, Any

from src.lib.infra.models.base.base_product_model import ProductModel


class AppProductModel(ProductModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._data = kwargs
        self._data["quantityPurchased"] = 0

    # Getters & Setters
    @property
    def product_subsidiary(self) -> List[Dict[str, Any]]:
        return self._data.get("productSubsidiary")

    @product_subsidiary.setter
    def product_subsidiary(self, product_subsidiary: List[Dict[str, Any]]) -> None:
        self._data["productSubsidiary"] = product_subsidiary

    @property
    def promotions(self) -> List[Dict[str, Any]]:
        return self._data.get("promotions")

    @promotions.setter
    def promotions(self, promotions: List[Dict[str, Any]]) -> None:
        self._data["promotions"] = promotions

    @property
    def kit_information(self) -> Dict[str, Any]:
        return self._data.get("kitInformation")

    @kit_information.setter
    def kit_information(self, kit_information: Dict[str, Any]) -> None:
        self._data["kitInformation"] = kit_information

    @property
    def explain(self) -> Dict[str, Any]:
        return self._data.get("explain")

    @explain.setter
    def explain(self, explain: Dict[str, Any]) -> None:
        self._data["explain"] = explain

    @property
    def kit(self) -> bool:
        return self._data.get("kit")

    @kit.setter
    def kit(self, kit: bool) -> None:
        self._data["kit"] = kit

    @property
    def quantity_purchased(self) -> int:
        return self._data.get("quantityPurchased")

    @quantity_purchased.setter
    def quantity_purchased(self, quantity_purchased: int) -> None:
        self._data["quantityPurchased"] = quantity_purchased

    def get_product(self) -> Dict[str, Any]:
        base_prod_data = super().get_product().copy()
        product_data = {key: value for key, value in base_prod_data.items() if value is not None}
        app_product_data = {
            "productSubsidiary": self.product_subsidiary,
            "promotions": self.promotions,
            "kitInformation": self.kit_information,
            "explain": self.explain,
            "kit": self.kit,
            "quantityPurchased": self.quantity_purchased,
        }
        product_data.update(app_product_data)
        return product_data
