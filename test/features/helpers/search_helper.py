from src.lib.api.qry_catalog_api import QryCatalogClient


def search_products(context, user, keyword):
    qry_catalog_client = QryCatalogClient(f'{context.HOST}/{context.PATHS["private"]}',
                                          application=context.APPLICATION,
                                          access_token=context.VALUES["USER_DATA"][user]["session"]["access_token"],
                                          app_version=context.APP_VERSION,
                                          user_id=context.VALUES["USER_DATA"][user]["session"]["userId"],
                                          platform=context.PLATFORM)

    context.search_response = qry_catalog_client.search_products(
        context.VALUES["USER_DATA"]["usuario_tienda"]["session"]["user"]["storeId"],
        context.VALUES["USER_DATA"]["usuario_tienda"]["selected_hub"]["storeSubsidiaryId"], keyword)


def assert_search_products(context, keyword):
    assert context.search_response.status_code == 200, (
        f'[ERROR] No se pudo obtener los productos para la busqueda por {keyword}'
        f'\n [Expected Status Code]: 200'
        f'\n [Received Status Code]: {context.search_response.status_code}'
    )
    assert len(context.search_response.body['result']) > 0, (
        f'[ERROR] No se encontraron productos para la busqueda por {keyword}'
        f'\n [Received Products]: {context.search_response.body["result"]}'
    )
    context.store_user.store.products = context.search_response.body['result']
    context.VALUES["USER_DATA"].update(context.store_user.get_user())
