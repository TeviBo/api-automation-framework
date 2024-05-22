from random import randint, choice
from typing import Dict, Any, List

from faker import Faker

from src.utils.data_manager import generate_random_image_url


class ProductModel:

    def __init__(self, **kwargs):
        self._product = kwargs
        self.FAKER = Faker()

    #  // *** Properties *** //

    @property
    def product_id(self) -> str:
        return self._product.get('productId')

    @product_id.setter
    def product_id(self, product_id: str) -> None:
        self._product['productId'] = product_id

    @property
    def sku(self) -> str:
        return self._product.get('sku')

    @sku.setter
    def sku(self, sku: str) -> None:
        self._product['sku'] = sku

    @property
    def external_id(self) -> str:
        return self._product.get('externalId')

    @external_id.setter
    def external_id(self, external_id: str) -> None:
        self._product['externalId'] = external_id

    @property
    def ean(self) -> str:
        return self._product.get('ean')

    @ean.setter
    def ean(self, ean: str) -> None:
        self._product['ean'] = ean

    @property
    def plu(self) -> str:
        return self._product.get('plu')

    @plu.setter
    def plu(self, plu: str) -> None:
        self._product['plu'] = plu

    @property
    def label(self) -> str:
        return self._product.get('label')

    @label.setter
    def label(self, label: str) -> None:
        self._product['label'] = label

    @property
    def short_description(self) -> str:
        return self._product.get('shortDescription')

    @short_description.setter
    def short_description(self, short_description: str) -> None:
        self._product['shortDescription'] = short_description

    @property
    def keywords(self) -> str:
        return self._product.get('keywords')

    @keywords.setter
    def keywords(self, keywords: str) -> None:
        self._product['keywords'] = keywords

    @property
    def suggested_keywords(self) -> str:
        return self._product.get('suggestedKeywords')

    @suggested_keywords.setter
    def suggested_keywords(self, suggested_keywords: str) -> None:
        self._product['suggestedKeywords'] = suggested_keywords

    @property
    def is_age_restricted(self) -> bool:
        return self._product.get('isAgeRestricted')

    @is_age_restricted.setter
    def is_age_restricted(self, is_age_restricted: bool) -> None:
        self._product['isAgeRestricted'] = is_age_restricted

    @property
    def ranking_term(self) -> str:
        return self._product.get('rankingTerm')

    @ranking_term.setter
    def ranking_term(self, ranking_term: str) -> None:
        self._product['rankingTerm'] = ranking_term

    @property
    def featured_product_ordinal_number(self) -> int:
        return self._product.get('featuredProductOrdinalNumber')

    @featured_product_ordinal_number.setter
    def featured_product_ordinal_number(self, featured_product_ordinal_number: int) -> None:
        self._product['featuredProductOrdinalNumber'] = featured_product_ordinal_number

    @property
    def brand_label(self) -> str:
        return self._product.get('brandLabel')

    @brand_label.setter
    def brand_label(self, brand_label: str) -> None:
        self._product['brandLabel'] = brand_label

    @property
    def logistic_measurement_unit(self) -> str:
        return self._product.get('logisticMeasurementUnit')

    @logistic_measurement_unit.setter
    def logistic_measurement_unit(self, logistic_measurement_unit: str) -> None:
        self._product['logisticMeasurementUnit'] = logistic_measurement_unit

    @property
    def measurement_unit_label_a(self) -> str:
        return self._product.get('measurementUnitLabelA')

    @measurement_unit_label_a.setter
    def measurement_unit_label_a(self, measurement_unit_label_a: str) -> None:
        self._product['measurementUnitLabelA'] = measurement_unit_label_a

    @property
    def measure_increment_value_a(self) -> int:
        return self._product.get('measureIncrementValueA')

    @measure_increment_value_a.setter
    def measure_increment_value_a(self, measure_increment_value_a: int) -> None:
        self._product['measureIncrementValueA'] = measure_increment_value_a

    @property
    def measurement_unit_label_b(self) -> str:
        return self._product.get('measurementUnitLabelB')

    @measurement_unit_label_b.setter
    def measurement_unit_label_b(self, measurement_unit_label_b: str) -> None:
        self._product['measurementUnitLabelB'] = measurement_unit_label_b

    @property
    def measure_increment_value_b(self) -> int:
        return self._product.get('measureIncrementValueB')

    @measure_increment_value_b.setter
    def measure_increment_value_b(self, measure_increment_value_b: int) -> None:
        self._product['measureIncrementValueB'] = measure_increment_value_b

    @property
    def product_image_url(self) -> str:
        return self._product.get('productImageUrl')

    @product_image_url.setter
    def product_image_url(self, product_image_url: str) -> None:
        self._product['productImageUrl'] = product_image_url

    @property
    def categories(self) -> List[Dict[str, Any]]:
        return self._product.get('categories')

    @categories.setter
    def categories(self, categories: List[Dict[str, Any]]) -> None:
        self._product['categories'] = categories

    @property
    def related_name(self) -> str:
        return self._product.get('relatedName')

    @related_name.setter
    def related_name(self, related_name: str) -> None:
        self._product['relatedName'] = related_name

    @property
    def replacement_name(self) -> str:
        return self._product.get('replacementName')

    @replacement_name.setter
    def replacement_name(self, replacement_name: str) -> None:
        self._product['replacementName'] = replacement_name

    @property
    def related_products(self) -> List[Dict[str, Any]]:
        return self._product.get('relatedProducts', [])

    @related_products.setter
    def related_products(self, related_products: List[Dict[str, Any]]) -> None:
        self._product['relatedProducts'] = related_products

    @property
    def replacement_products(self) -> List[Dict[str, Any]]:
        return self._product.get('replacementProducts', [])

    @replacement_products.setter
    def replacement_products(self, replacement_products: List[Dict[str, Any]]) -> None:
        self._product['replacementProducts'] = replacement_products

    @property
    def nutritional_information(self) -> Dict[str, Any]:
        return self._product.get('nutritionalInformation')

    @nutritional_information.setter
    def nutritional_information(self, nutritional_information: Dict[str, Any]) -> None:
        self._product["nutritionalInformation"] = nutritional_information

    @property
    def config(self) -> List[Dict[str, Any]]:
        return self._product.get('config')

    @config.setter
    def config(self, config: List[Dict[str, Any]]) -> None:
        self._product['config'] = config

    @property
    def product_subsidiary(self) -> List[Dict[str, Any]]:
        return self._product.get('productSubsidiary')

    @product_subsidiary.setter
    def product_subsidiary(self, product_subsidiary: List[Dict[str, Any]]) -> None:
        self._product['productSubsidiary'] = product_subsidiary

    @property
    def promotions(self) -> List[Dict[str, Any]]:
        return self._product.get('promotions')

    @promotions.setter
    def promotions(self, promotions: List[Dict[str, Any]]) -> None:
        self._product['promotions'] = promotions

    @property
    def images(self) -> List[Dict[str, Any]]:
        return self._product.get('images')

    @images.setter
    def images(self, images: List[Dict[str, Any]]) -> None:
        self._product['images'] = images

    @property
    def kit(self) -> bool:
        return self._product.get('kit')

    @kit.setter
    def kit(self, kit: bool) -> None:
        self._product['kit'] = kit

    @property
    def store_id(self) -> str:
        return self._product.get('storeId')

    @store_id.setter
    def store_id(self, store_id: str) -> None:
        self._product['storeId'] = store_id

    # // *** Methods *** //
    def get_product(self) -> Dict[str, Any]:
        return {
            'productId': self.product_id,
            'sku': self.sku,
            'externalId': self.sku,
            'ean': self.ean,
            'plu': self.plu,
            'label': self.label,
            'shortDescription': self.short_description,
            'keywords': self.keywords,
            'rankingTerm': self.ranking_term,
            'featuredProductOrdinalNumber': self.featured_product_ordinal_number,
            'brandLabel': self.brand_label,
            'logisticMeasurementUnit': self.logistic_measurement_unit,
            'measurementUnitLabelA': self.measurement_unit_label_a,
            'measureIncrementValueA': self.measure_increment_value_a,
            'measurementUnitLabelB': self.measurement_unit_label_b,
            'measureIncrementValueB': self.measure_increment_value_b,
            'productImageUrl': self.product_image_url,
            'categories': self.categories,
            'relatedProducts': {
                'related': {
                    'name': self.related_name if self.related_products != [] else "",
                    'products': self.related_products
                },
                'replacements': {
                    'name': self.replacement_name if self.replacement_products != [] else "",
                    'products': self.replacement_products
                }
            },
            'nutritionalInformation': self.nutritional_information,
            'config': self.config,
            'productSubsidiary': self.product_subsidiary,
            'promotions': self.promotions,
            'images': self.images,
            'storeId': self.store_id,
        }

    def create_product(self, category: str, child_category: str, related_products=None, replacement_products=None):
        if related_products is None:
            related_products = []
        if replacement_products is None:
            replacement_products = []
        self.sku = f"K{randint(100000, 999999)}"
        self.ean = ""
        self.plu = self.sku
        self.label = self.FAKER.word().capitalize()
        self.short_description = "Automation Product"
        self.keywords = "automation"
        self.ranking_term = "test"
        self.featured_product_ordinal_number = 1
        self.brand_label = self.FAKER.company()
        self.product_image_url = generate_random_image_url()
        self.logistic_measurement_unit = "und"
        self.measurement_unit_label_a = "und"
        self.measure_increment_value_a = 1
        self.measurement_unit_label_b = None
        self.measure_increment_value_b = None
        self.categories = [{"categoryExternalId": category}, {"categoryExternalId": child_category}]
        self.related_name = "Productos Relacionados"
        self.replacement_name = "Productos de Reemplazo"
        self.related_products = related_products
        self.replacement_products = replacement_products
        self.nutritional_information = {
            "highSodium": choice([True, False]),
            "highInSugar": choice([True, False]),
            "highInSaturatedFat": choice([True, False]),
            "containTransFats": choice([True, False]),
            "avoidExcessiveConsumption": choice([True, False]),
            "avoidItsConsumption": choice([True, False]),
        }
