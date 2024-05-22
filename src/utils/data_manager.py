import random
from random import randint, choice
from typing import List, Dict, Any

from faker import Faker

FAKE = Faker()


def generate_random_image_url():
    width = random.randint(200, 800)  # Adjust the range as needed
    height = random.randint(200, 800)  # Adjust the range as needed
    image_id = random.randint(1, 1000)  # Adjust the range as needed

    return f"https://picsum.photos/{width}/{height}/?image={image_id}"


def generate_random_phone(valid: bool = True, len_valid: bool = True):
    if valid:
        if len_valid:
            return f"9{randint(11111111, 99999999)}"
        return f"9{randint(1111111, 9999999)}"
    return f"7{randint(111111111, 999999999)}"


def generate_random_name():
    return FAKE.first_name()


def generate_random_last_name():
    return FAKE.last_name()


def generate_random_complete_name():
    return f'{FAKE.first_name()} {FAKE.last_name()}'


def generate_random_email():
    return FAKE.email()


def generate_random_dni(length: int = 8) -> str:
    return str(randint(11111111, 99999999))[:length]


def products_generator(quantity: int, category: str,
                       child_category: str, to_delete: str = "No") -> List[Dict[str, Any]]:
    """
    Generate a list of products with given quantity, category, child category, and deletion option.

    Parameters:
    - quantity: An integer representing the number of products to generate.
    - category: A string representing the category of the products.
    - child_category: A string representing the child category of the products.
    - to_delete: (optional) A string indicating whether the products should be marked for deletion. Default is "No".

    Returns:
    A list of dictionaries, where each dictionary represents a product.
    """
    products = []
    logistic_measurement_unit = choice(['und', 'kg'])
    for _ in range(quantity):
        sku_external_id = randint(100000, 999999)
        product = {'externalId': sku_external_id, 'sku': sku_external_id, 'label': FAKE.word().capitalize(),
                   'shortDescription': FAKE.paragraph(), 'keywords': FAKE.word(), 'KEYWORDSUGERIDO': FAKE.word(),
                   'featuredProductOrdinalNumber': randint(1, 10), 'brandLabel': FAKE.company(), 'rankingTerm': "",
                   'category1': category, 'category2': child_category, 'category3': "", 'category4': "",
                   'category5': "",
                   'nameReplacement': "", 'replacement1': "", 'replacement2': "", 'replacement3': "",
                   'replacement4': "", 'replacement5': "", 'nameRelated': "", 'related1': "", 'related2': "",
                   'related3': "", 'related4': "", 'related5': "", 'imageUrl': generate_random_image_url(), 'ean': "",
                   'plu': "", 'logisticMeasurementUnit': logistic_measurement_unit,
                   'measurementUnitLabelA': logistic_measurement_unit,
                   'measureIncrementValueA': choice([1, 3, 5]) if logistic_measurement_unit == 'und' else choice(
                       [0.5, 1, 1.5, 2]), 'measurementUnitLabelB': None, 'measureIncrementValueB': None,
                   'highSodium': choice(['Si', 'No']), 'highInSugar': choice(['Si', 'No']),
                   'highInSaturatedFat': choice(['Si', 'No']), 'containTransFats': choice(['Si', 'No']),
                   'avoidExcessiveConsumption': choice(['Si', 'No']), 'avoidItsConsumption': choice(['Si', 'No']),
                   'toDelete': to_delete, 'isAgeRestricted': choice(['Si', 'No'])}
        products.append(product)
    return products
