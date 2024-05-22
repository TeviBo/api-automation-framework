import os.path
from random import randint, uniform, choice
from time import sleep

from behave import *  # NOSONAR
from features.helpers.checkout_helper import complete_order
from features.helpers.library_helper import (get_categories, assert_get_categories, get_child_categories,
                                             assert_get_child_categories, complete_picking, assert_synchronize_order)
from features.helpers.products_helper import get_all_products, assert_get_all_products
from features.helpers.shopping_cart_helper import create_cart

from src.lib.api.library_api import BackofficeLib
from src.lib.api.products_api import Products
from src.utils.logger import logger
from src.utils.utils import go_up_n_dirs


@Given('el usuario de pmm "{user}" con permisos para cargar stock')
def get_oauth2_token(context, user):
    context.VALUES["USER_DATA"].update({user: {"session": {}}})


@Given('el usuario "{user}" crea un set de "{quantity}" productos nuevos')
def create_new_products(context, user, quantity):
    get_categories(context, user)
    assert_get_categories(context)
    selected_category = choice(context.store_user.store.categories)
    get_child_categories(context, selected_category['categoryId'])
    assert_get_child_categories(context)
    selected_child_category = choice(context.child_categories)
    context.lst_new_products = context.DATA_MANAGER.products_generator(int(quantity), selected_category['externalId'],
                                                                       selected_child_category['externalId'])


@When('el usuario "{user}" realiza la carga masiva de los productos mediante un archivo excel')
def bulk_upload_new_products(context, user):
    bo_lib_client = BackofficeLib(f'{context.HOST}/{context.BASE_ENV_VARS["paths"]["shop"]["backoffice"]}',
                                  token=context.store_user.session["token"],
                                  access_token=context.store_user.session["access_token"],
                                  client_id=context.store_user.session["client_id"],
                                  firebase_token=context.store_user.session["firebase_token"],
                                  identity_token=context.store_user.session["identity_token"])
    context.UTILS.generate_new_products_bulk_upload_file(context.lst_new_products)
    context.bulk_upload_response = bo_lib_client.bulk_new_products(context.store_user.store.store_id)


@Then('los productos deben cargarse correctamente con los datos')
def assert_bulk_upload_new_products(context):
    assert context.bulk_upload_response.status_code == 201, (
        '[ERROR] Ocurrio un error al realizar la carga'
        '\n [Expected Status Code]: 201'
        f'\n [Received Status Code]: {context.bulk_upload_response.status_code}'
    )
    assert context.bulk_upload_response.body["count"] == len(
        context.lst_new_products), "[ERROR] Los productos no fueron cargados"

    assert len(context.bulk_upload_response.body["res"]) == len(context.lst_new_products), (
        '[ERROR] No se han cargado todos los productos'
        f'\n[Expected Quantity]: {len(context.lst_new_products)}'
        f'\n[Received Quantity]: {len(context.bulk_upload_response.body["res"])}')


@Given('un set de productos para actualizar')
def get_xlsx_file(context):
    root = go_up_n_dirs(os.path.abspath(__file__), 3)
    context.source_df = context.UTILS.get_xlsx_file(f'{root}/src/data/xlsx/Bulk new products.xlsx')


@When('se realiza la actualizacion de stock y precio mediante un excel desde Backoffice para el hub "{hub}"')
def update_new_products_stock_price(context, hub):
    bo_lib_client = BackofficeLib(context.HOST, token=context.store_user.session["token"],
                                  access_token=context.store_user.session["access_token"],
                                  client_id=context.store_user.session["client_id"],
                                  firebase_token=context.store_user.session["firebase_token"],
                                  identity_token=context.store_user.session["identity_token"])
    context.UTILS.generate_edit_new_products_stock_price_file(context.source_df)
    context.store_user.get_hub(hub)
    context.update_new_products_stock_price_response = bo_lib_client.update_stock_price_new_products(
        context.store_user.store.store_id, context.store_user.selected_hub["storeSubsidiaryId"])


@Then('los productos deben actualizarse correctamente con los datos')
def step_impl(context):
    assert context.update_new_products_stock_price_response.status_code == 201, (
        '[ERROR] El archivo no ha sido cargado'
        '\n[Expected Status Code]: 201'
        f'\n[Received Status Code]: {context.update_new_products_stock_price_response.status_code}'
    )
    assert len(context.update_new_products_stock_price_response.body["errors"]) == 0, (
        '[ERROR] los productos no han sido actualizados'
        f'\n[Errors]: {context.update_new_products_stock_price_response.body["errors"]}'
    )
    assert len(context.update_new_products_stock_price_response.body["res"][0]) > 0, (
        "[ERROR] Los productos no fueron cargados"
    )


@Given(
    'un set de "{products_quantity_requested}" productos para actualizar desde PMM por el usuario "{user}" para el hub "{hub}"')
def get_products_for_pmm_bulk_upload(context, products_quantity_requested, user, hub):
    context.store_user.get_hub(hub)
    get_all_products(context, products_quantity_requested, context.store_user.selected_hub["storeSubsidiaryId"])
    assert_get_all_products(context, products_quantity_requested)
    context.products_to_update = []
    for product in context.store_user.store.products:
        if product.sku == '1058690001':
            context.store_user.store.products.remove(product)
        product_to_update = {"productId": product.product_id, "sku": product.sku,
                             "unit_available": randint(1, 9999),
                             "price": round(uniform(5.4, 99.99), 2)}
        context.products_to_update.append(product_to_update)


@When('el usuario "{user}" realiza la actualizacion de stock y precio desde PMM')
def pmm_stock_loading(context, user):
    products_client = Products(f'{context.HOST}/{context.PATHS["store_management"]}',
                               application=context.APPLICATION, platform=context.PLATFORM,
                               app_version=context.APP_VERSION,
                               access_token=context.VALUES["USER_DATA"][user]["session"]["access_token"])
    logger.info("SENDING PRODUCTS TO UPDATE".center(50, "-"))
    context.pmm_stock_loading_response = products_client.pmm_loading(
        context.store_user.store.store_id,
        context.store_user.selected_hub["storeSubsidiaryId"], context.products_to_update)


@When('el usuario "{user}" realiza la actualizacion de stock 0 y precio desde PMM')
def pmm_stock_0_bulk_upload(context, user):
    products_client = Products(f'{context.HOST}/{context.PATHS["store_management"]}',
                               application=context.APPLICATION, platform=context.PLATFORM,
                               app_version=context.APP_VERSION,
                               access_token=context.VALUES["USER_DATA"][user]["session"]["access_token"])
    for product in context.products_to_update:
        product["unit_available"] = 0
    logger.info("SENDING PRODUCTS TO UPDATE".center(50, "-"))
    context.pmm_stock_loading_response = products_client.pmm_loading(
        context.store_user.store.store_id,
        context.store_user.selected_hub["storeSubsidiaryId"], context.products_to_update)


@Then('el stock y precio de los "{products_quantity_requested}" productos debe ser el enviado desde PMM')
def assert_stock_price_changed(context, products_quantity_requested):
    err_code = context.pmm_stock_loading_response.body[
        'code'] if context.pmm_stock_loading_response.status_code == 422 else None
    err_msg = context.pmm_stock_loading_response.body[
        'exceptionMessage'] if context.pmm_stock_loading_response.status_code == 422 else None

    assert context.pmm_stock_loading_response.status_code == 201, (
        '[ERROR] La actualizacion de stock y precio de los productos no se realizo correctamente'
        '[\nExpected Status Code]: 201'
        f'\n[Received Status Code]: {context.pmm_stock_loading_response.status_code}'
        f'\n[Error Code]: {err_code}'
        f'\n[Error Message]: {err_msg}'
    )
    sleep(10)
    get_all_products(context, products_quantity_requested, context.store_user.selected_hub["storeSubsidiaryId"])
    assert_get_all_products(context, products_quantity_requested)
    result, errors = context.store_user.validate_stock_update(context.pmm_stock_loading_response.body)
    assert result, ''.join(errors)
    logger.info("PRODUCTS UPDATED".center(50, "-"))


# // E2E Stock Tests //

# Stock decrement after order delivered

@Given('el usuario "{user}" con carrito')
def given_a_user_with_a_cart(context, user):
    create_cart(context, user)


@When('el usuario "{user}" genera la orden para la direccion "{address}" con metodo de pago "{card_branch}" '
      'terminado en "{last_4_digits}"')
def when_the_user_generate_an_order(context, user, address, card_branch, last_4_digits):
    complete_order(context, user, address, card_branch, last_4_digits)


@Then('la orden es generada exitosamente por el usuario "{user}"')
def assert_when_the_user_generate_an_order(context, user):
    assert_complete_checkout(context)


@When('el usuario "{user}" con credenciales "{picker_username}", "{picker_password}" completa el picking de la orden')
def when_the_dad_user_completes_picking(context, user, picker_username, picker_password):
    complete_picking(context, user=user, picker_username=picker_username, picker_password=picker_password)


@Then('el picking es completado exitosamente')
def assert_when_the_dad_user_completes_picking(context):
    assert_synchronize_order(context)


@When('el usuario "usuario_beetrack" completa el delivery de la orden')
def when_the_beetrack_user_completes_delivery(context):
    pass


@Then('el delivery es completado exitosamente')
def assert_when_the_beetrack_user_completes_delivery(context):
    pass
