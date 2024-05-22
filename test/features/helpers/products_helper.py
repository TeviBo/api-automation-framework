from src.lib.api.library_api import BackofficeLib
from src.lib.api.qry_catalog_api import QryCatalogClient


def get_all_products(context, products_quantity, subsidiary_id):
    bo_lib_client = BackofficeLib(f'{context.HOST}/{context.BASE_ENV_VARS["paths"]["shop"]["backoffice"]}',
                                  token=context.store_user.session["token"],
                                  access_token=context.store_user.session["access_token"],
                                  client_id=context.store_user.session["client_id"],
                                  firebase_token=context.store_user.session["firebase_token"],
                                  identity_token=context.store_user.session["identity_token"])
    context.get_all_products_response = bo_lib_client.get_all_products(context.store_user.store.store_id, subsidiary_id,
                                                                       products_quantity)


def assert_get_all_products(context, products_quantity_requested):
    assert context.get_all_products_response.status_code == 200, (
        '[ERROR] No se pudo obtener los productos'
        '\n [Expected Status Code]: 200'
        f'\n [Received Status Code]: {context.get_all_products_response.status_code}'
    )
    assert context.store_user.selected_hub["storeSubsidiaryId"] in context.get_all_products_response.endpoint, (
        '[ERROR] No se obtuvieron los productos de la sucursal seleccionada'
        f'\n [Expected Subsidiary Id]: {context.store_user.selected_hub["storeSubsidiaryId"]}'
        f'\n [Received Subsidiary Id]: {context.get_all_products_response.endpoint}'
    )
    assert len(context.get_all_products_response.body["result"]) == int(products_quantity_requested)

    context.store_user.store.products = context.get_all_products_response.body["result"]


def search_product_by_sku(context, sku, hub=None):
    bo_client = BackofficeLib(f'{context.HOST}/{context.BASE_ENV_VARS["paths"]["shop"]["backoffice"]}',
                              token=context.VALUES["USER_DATA"]["usuario_tienda"]["session"]["token"],
                              client_id=context.VALUES["USER_DATA"]["usuario_tienda"]["session"]['client_id'],
                              access_token=context.VALUES["USER_DATA"]["usuario_tienda"]["session"]["access_token"],
                              firebase_token=context.VALUES["USER_DATA"]["usuario_tienda"]["session"]["firebase_token"],
                              identity_token=context.VALUES["USER_DATA"]["usuario_tienda"]["session"]["identity_token"])
    context.get_product_by_sku_response = bo_client.get_products_by_sku(
        context.VALUES["USER_DATA"]["usuario_tienda"]["session"]["user"]["storeId"], sku,
        store_subsidiary_id=context.store_user.selected_hub["subsidiaryId"] if hub else None)


def assert_search_product_by_sku(context):
    assert context.get_product_by_sku_response.status_code == 200, (
        '[ERROR] No se pudo obtener los productos'
        '\n [Expected Status Code]: 200'
        f'\n [Received Status Code]: {context.get_product_by_sku_response.status_code}')

    context.product = context.get_product_by_sku_response.body['result'][0]


def get_categories_by_store(context, user, hub=None):
    qry_catalog_client = QryCatalogClient(f'{context.HOST}/{context.PATHS["private"]}',
                                          application=context.APPLICATION,
                                          access_token=context.VALUES["USER_DATA"][user]["session"]["access_token"],
                                          app_version=context.APP_VERSION,
                                          user_id=context.VALUES["USER_DATA"][user]["session"]["userId"],
                                          platform=context.PLATFORM)
    context.get_categories_by_store_response = qry_catalog_client.get_categories_by_store(
        context.APP_ENV_VARS["STORE"]["STORE_ID"])


def assert_get_categories_by_store(context):
    assert context.get_categories_by_store_response.status_code == 200, (
        f'[ERROR] No se pudo obtener las categorias para la tienda {context.store_user.store.store_name} con id: '
        f'{context.store_user.store.store_id}'
        '\n [Expected Status Code]: 200'
        f'\n [Received Status Code]: {context.get_categories_by_store_response.status_code}'
    )

    context.store_user.store.categories = context.get_categories_by_store_response.body
