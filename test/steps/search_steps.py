from random import choice

from behave import *  # NOSONAR
from features.helpers.search_helper import search_products, assert_search_products

from src.lib.api.qry_catalog_api import QryCatalogClient


@When('el usuario "{user}" busca productos por categoria "{category}"')
def when_the_user_searches_products_by_category(context, user, category):
    search_products(context, user, category)


@Then('se muestran los productos para la busqueda por "{keyword}"')
def assert_when_the_user_searches_products_by_category(context, keyword):
    assert_search_products(context, keyword)


@Step('el usuario "{user}" busca el producto "{product}"')
def when_the_user_search_a_product(context, user, product):
    search_products(context, user, product)
    assert_search_products(context, product)
    context.app_user.find_product(product, context.store_user.store.products)
    context.VALUES["USER_DATA"].update(context.app_user.get_user())

@Then('se retorna el producto "{product}" para el usuario "{user}"')
def assert_contained_products(context, product, user):
    if context.app_user.selected_product != {}:
        assert product == context.app_user.selected_product.label, (
            f'[ERROR] El producto buscado no es el esperado'
            f'\n [Expected Product]: {product}'
            f'\n [Received Product]: {context.app_user.selected_product.label}'
        )
    else:
        assert False, (
            f'[ERROR] No se encontro el producto buscado'
            f'\n [Expected Product]: {product}'
            f'\n [Received Products]: {[f"{prod.sku} - {prod.label}" for prod in context.store_user.store.products]}'
        )


@When('el usuario "{user}" realiza una busqueda por "{search}"')
def search_with_autocomplete(context, user, search):
    qry_catalog_client = QryCatalogClient(f'{context.HOST}/{context.PATHS["private"]}',
                                          application=context.APPLICATION,
                                          access_token=context.VALUES["USER_DATA"][user]["session"]["access_token"],
                                          user_id=context.VALUES["USER_DATA"][user]["session"]["userId"],
                                          app_version=context.APP_VERSION,
                                          platform=context.PLATFORM)
    response = qry_catalog_client.get_autocomplete_suggestions(
        context.VALUES["USER_DATA"]["usuario_tienda"]["session"]["user"]["storeId"],
        context.VALUES["USER_DATA"]["usuario_tienda"]["selected_hub"]['storeSubsidiaryId'],
        search)

    assert response.status_code == 200, '[ERROR] No se pudo obtener las sugerencias para la busqueda' \
                                        f'[Expected Status Code]: 200' \
                                        f'\n [Received Status Code]: {response.status_code}' \
                                        f'\n [Search]: {search}'
    context.suggestions = response.body


@Then('se retornan las distintas sugerencias para dicha busqueda')
def assert_search_with_autocomplete(context):
    assert len(context.suggestions) > 0, '[ERROR] No se encontraron sugerencias para la busqueda' \
                                         f'\n [Received Suggestions]: {context.suggestions}'


@When('el usuario "{user}" selecciona una de las sugerencias')
def select_suggestion(context, user):
    context.picked_suggestion = choice(context.suggestions)
    search_products(context, user, context.picked_suggestion)


@Then('se retornan los productos relacionados a la misma')
def assert_product_list_by_suggestion(context):
    assert_search_products(context, context.picked_suggestion)


@When('el usuario "{user}" busca el producto inexistente "{non_existent_product}"')
def search_non_existent_product(context, user, non_existent_product):
    search_products(context, user, non_existent_product)


@Then('el sistema devuelve un mensaje de error indicando que el producto "{non_existent_product}" no existe')
def assert_non_existent_product_error_message(context, non_existent_product):
    assert context.search_response.status_code == 200, (
        f'[ERROR] Ha ocurrido un error no esperado al buscar el producto {non_existent_product} '
        f'\n [Expected Status Code]: 200'
        f'\n [Received Status Code]: {context.search_response.status_code}'
    )

    assert context.search_response.body["result"] == [], (
        f'[ERROR] Se encontraron resultados para la busqueda por {non_existent_product}'
        '[Expected Result]: 0'
        f'[Received Result]: {context.search_response.body["result"]}'
    )
