from datetime import datetime, timedelta
from random import randint, choice
from typing import List, Dict, Any

from faker import Faker


class PromotionModel:
    faker = Faker()
    __TYPES = ["PACK"]

    def __init__(self) -> None:

        self._external_id: str = ""
        self._name: str = ""
        self._label: str = "PACK"
        self._promotional_price: float = 0.0
        self._description: str = ""
        self._promotion_initial_date: str = ""
        self._promotion_due_date: str = ""
        self._type: str = choice(self.__TYPES)
        self._products: List[Dict[str, Any]] = []
        self._enabled: bool = False

    # Properties
    @property
    def external_promotion_id(self) -> str:
        return self._external_id

    @external_promotion_id.setter
    def external_promotion_id(self, external_id: str) -> None:
        self._external_id = external_id

    @property
    def external_id(self) -> str:
        return self._external_id

    @external_id.setter
    def external_id(self, external_id: str) -> None:
        self._external_id = external_id

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, enabled: bool) -> None:
        self._enabled = enabled

    @property
    def label(self) -> str:
        return self._label

    @label.setter
    def label(self, label: str) -> None:
        self._label = label

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def promotional_price(self) -> float:
        return self._promotional_price

    @promotional_price.setter
    def promotional_price(self, promotional_price: float) -> None:
        self._promotional_price = promotional_price

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str) -> None:
        self._description = description

    @property
    def promotion_initial_date(self) -> str:
        return self._promotion_initial_date

    @promotion_initial_date.setter
    def promotion_initial_date(self, promotion_initial_date: str) -> None:
        self._promotion_initial_date = promotion_initial_date

    @property
    def promotion_due_date(self) -> str:
        return self._promotion_due_date

    @promotion_due_date.setter
    def promotion_due_date(self, promotion_due_date: str) -> None:
        self._promotion_due_date = promotion_due_date

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, promotion_type: str) -> None:
        self._type = promotion_type

    @property
    def products(self) -> List[Dict[str, Any]]:
        return self._products

    @products.setter
    def products(self, products: List[Dict[str, Any]]) -> None:
        self._products = products

    def get_promotion(self) -> dict:
        return {
            "externalId": self.external_promotion_id,
            "externalPromotionId": self.external_promotion_id,
            "name": self.name,
            "description": self.description,
            "promotionInitialDate": self.promotion_initial_date,
            "promotionDueDate": self.promotion_due_date,
            "type": self.type,
            "label": self.label,
            "productPromotionsDetails": self.products,
            "enabled": self.enabled,
            "promotionalPrice": self.promotional_price
        }

    def create_promotion_kit(self):
        self.external_id = f'A{randint(100000, 999999)}'
        self.name = self.faker.word().capitalize()
        self.description = f"Automation {self.type} promotion"
        self.promotion_initial_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        self.promotion_due_date = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%dT%H:%M:%S')
        self.enabled = False
        for product in self.products:
            if not self.products:
                break
            self.promotional_price += round(float(product["unitPrice"]) * int(product["requiredQuantity"]), 2)

    def set_promotion_kit(self, **promotion):
        self.label = promotion.get("label", self.label)
        self.name = promotion.get("name", self.name)
        self.external_promotion_id = promotion.get("externalId", self.external_promotion_id)
        self.promotional_price = promotion.get("promotionalPrice", self.promotional_price)
        self.description = promotion.get("description", self.description)
        self.promotion_initial_date = promotion.get("promotionInitialDate", self.promotion_initial_date)
        self.promotion_due_date = promotion.get("promotionDueDate", self.promotion_due_date)
        self.type = promotion.get("type", self.type)
        self.products = promotion.get("products", self.products)
        self.enabled = promotion.get("enabled", self.enabled)
