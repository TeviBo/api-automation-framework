import json
import os
from pathlib import Path
from random import uniform, choice, randint
from typing import Dict, Any, List

import pandas
import pandas as pd


def go_up_n_dirs(path, n):
    for _ in range(n):
        path = os.path.dirname(path)
    return path


def get_keyboard_positions(keyboard: List[int], password: str) -> List[int]:
    """
   Get positions from android keyboard for digits in the password
       :type keyboard: list[int]
       :param keyboard: keyboard to evaluate and find positions
       :type password: str
       :param password: password string containing digits
       :return: list of positions of digits in the keyboard
   """
    password_digits = [int(char) for char in password if char.isdigit()]
    password_positions = []

    for digit in password_digits:
        if digit in keyboard:
            password_positions.append(keyboard.index(digit))

    return password_positions


def update_item_in_list_by_key(items: List[dict], key: str, target: int, new_data: (Dict[str, Any], any)):
    for item in items:
        if item[key] == target:
            item.update(new_data)
            break


def clean_logs_dir(path: str) -> None:
    """
    Clean logs
        :param path: path to logs directory in the project
        :return: None
    """
    for file in Path(path).iterdir():
        if file.is_file():
            with open(file, "w", encoding="utf-8") as f:
                f.truncate(0)


def create_allure_environment_file(**kwargs: dict):
    current_file_path = os.path.realpath(__file__)
    root_path = go_up_n_dirs(os.path.dirname(current_file_path), 2)
    dir_path = f"{root_path}/reports/allure-results/"
    file_path = os.path.join(dir_path, "environment.properties")

    # Create directory if it does not exist
    os.makedirs(dir_path, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"ENVIRONMENT {kwargs.get('env')}" + os.linesep)
        file.write(f"APPLICATION {kwargs.get('application')}" + os.linesep)
        file.write(f"VERSION {kwargs.get('app_version')}" + os.linesep)
        file.write(f"PLATFORM {kwargs.get('platform')}" + os.linesep)
        file.close()


def create_allure_categories_file(path: str) -> None:
    """
    Create the categories.json file for Allure report.
        :type path: str
        :param path: path that will contain the categories.json file
        :return: None
    """
    data = [
        {"name": "Ignored tests", "matchedStatuses": ["skipped"]},
        {"name": "Infrastructure problems", "matchedStatuses": ["broken", "failed"], "messageRegex": ".*bye-bye.*"},
        {"name": "Outdated tests", "matchedStatuses": ["broken"], "traceRegex": ".*FileNotFoundException.*"},
        {"name": "Product defects", "matchedStatuses": ["failed"]},
        {"name": "Test defects", "matchedStatuses": ["broken"]},
    ]
    # Write the data to the categories.json file
    with open(f"{path}/categories.json", "w") as file:
        json.dump(data, file, indent=4)


# Generate .xlsx file for new products bulk upload
def generate_new_products_bulk_upload_file(products: List[Dict[str, Any]]) -> None:
    """
    Generate .xlsx file for new products bulk upload
    :param products: list of dictionaries containing product data
    :return: None
    """
    columns = ['externalId', 'sku', 'label', 'shortDescription', 'keywords', 'KEYWORDSUGERIDO', 'isAgeRestricted',
               'featuredProductOrdinalNumber', 'brandLabel', 'rankingTerm', 'category1', 'category2', 'category3',
               'category4', 'category5', 'nameReplacement', 'replacement1', 'replacement2', 'replacement3',
               'replacement4', 'replacement5', 'nameRelated', 'related1', 'related2', 'related3', 'related4',
               'related5', 'imageUrl', 'ean', 'plu', 'logisticMeasurementUnit', 'measurementUnitLabelA',
               'measureIncrementValueA', 'measurementUnitLabelB', 'measureIncrementValueB', 'highSodium', 'highInSugar',
               'highInSaturatedFat', 'containTransFats', 'avoidExcessiveConsumption', 'avoidItsConsumption', 'toDelete']
    root_path = go_up_n_dirs(os.path.abspath(__file__), 2)
    file_path = os.path.join(root_path, 'data', 'xlsx')
    body = []
    for product in products:
        body.append([
            product['externalId'], product['sku'], product['label'], product['shortDescription'], product['keywords'],
            product['KEYWORDSUGERIDO'], product['isAgeRestricted'], product['featuredProductOrdinalNumber'],
            product['brandLabel'], product['rankingTerm'], product['category1'], product['category2'],
            product['category3'], product['category4'], product['category5'], product['nameReplacement'],
            product['replacement1'], product['replacement2'], product['replacement3'], product['replacement4'],
            product['replacement5'], product['nameRelated'], product['related1'], product['related2'],
            product['related3'], product['related4'], product['related5'], product['imageUrl'], product['ean'],
            product['plu'], product['logisticMeasurementUnit'], product['measurementUnitLabelA'],
            product['measureIncrementValueA'], product['measurementUnitLabelB'], product['measureIncrementValueB'],
            product['highSodium'], product['highInSugar'], product['highInSaturatedFat'], product['containTransFats'],
            product['avoidExcessiveConsumption'], product['avoidItsConsumption'], product['toDelete']
        ])
    df = pd.DataFrame(body, columns=columns)
    df.to_excel(f'{file_path}/Bulk new products.xlsx', sheet_name='Hoja1',
                engine='xlsxwriter', index=False)


def get_xlsx_file(xlsx_file_path: str):
    """
    Takes the path of a xlsx file, reads and return it.
        :type xlsx_file_path: str
        :param xlsx_file_path: Path to the file from where we the data will be consumed
        :return:
        """
    source_df = pd.read_excel(xlsx_file_path)
    return source_df


def generate_edit_new_products_stock_price_file(source_df: pandas.DataFrame):
    """
    Takes a data frame where the data will be taken and generates a new one
    to be uploaded for product stock and price update.
    :type source_df: DataFrame
    :param source_df: The data frame where the data will be taken
    :return: None
    """
    columns = ['externalId', 'price', 'isVisible', 'isInStock', 'useUnitAvailable',
               'unitAvailable', 'maxUnitSale']
    body = []
    for _, row in source_df.iterrows():
        body.append([
            row['externalId'], round(uniform(5.00, 50.90), 2), choice(["Si", "No"]), "Si", "Si",
            randint(10, 3000), "5"
        ])
    root_path = go_up_n_dirs(os.path.abspath(__file__), 2)
    file_path = os.path.join(root_path, 'data', 'xlsx')
    df = pd.DataFrame(body, columns=columns)
    df.to_excel(f'{file_path}/Update new product stock.xlsx', engine='xlsxwriter',
                sheet_name='Hoja1', index=False)
