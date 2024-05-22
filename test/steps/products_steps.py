from behave import *  # NOSONAR
from features.helpers.library_helper import get_child_categories, assert_get_child_categories
from features.helpers.products_helper import get_categories_by_store, assert_get_categories_by_store
from features.helpers.campaigns_helper import get_campaigns_by_hub, assert_get_campaigns_by_hub
from src.lib.api.qry_catalog_api import QryCatalogClient


@When('el usuario "{user}" visualiza el listado de categorias para la tienda "{hub}"')
def when_the_user_visualize_the_category_list(context, user, hub=None):
    get_categories_by_store(context, user)


@Then('se retornan las categorias para la tienda "{hub}" para el usuario "{user}"')
def assert_when_the_user_visualize_the_category_list(context, hub, user):
    assert_get_categories_by_store(context)


@Step('sus categorias hijas')
def step_impl(context):
    for category in context.store_user.store.categories:
        get_child_categories(context, category["categoryId"])
        assert_get_child_categories(context)
        context.store_user.store.categories[context.store_user.store.categories.index(category)][
            "childCategories"] = context.child_categories


@When('el usuario "{user}" ingresa a la categoria "{category}" para el hub "{hub}"')
def get_category(context, user, category, hub):
    categories_client = QryCatalogClient(f'{context.HOST}/{context.PATHS["private"]}',
                                         application=context.APPLICATION,
                                         access_token=context.VALUES["USER_DATA"][user]["session"]["access_token"],
                                         app_version=context.APP_VERSION, platform=context.PLATFORM)
    context.app_user.find_category(category, context.store_user.store.categories)
    context.get_category_detail_response = categories_client.get_products_by_category(
        context.app_user.selected_category["categoryId"], context.APP_ENV_VARS["STORE"]["HUBS"][hub]["SUBSIDIARY_ID"])


@Then('se listan los productos relacionados a la categoria "{category}" para el usuario "{user}"')
def assert_category_products(context, category, user):
    assert context.get_category_detail_response.status_code == 200, (
        f'[ERROR] No se pudo obtener los productos para la categoria "{category}"'
        '\n [Expected Status Code]: 200'
        f'\n [Received Status Code]: {context.get_category_detail_response.status_code}'
    )
    assert len(context.get_category_detail_response.body["result"]) > 0, (
        '[ERROR] La lista de productos para esa categoria esta vacia'
        f'\n [Category]: {category}'
        f'\n [Received products]: {context.get_category_detail_response.body["result"]}')
    if not context.store_user.store.products:
        context.store_user.store.products = []
    context.store_user.store.products = context.get_category_detail_response.body["result"]


# // PRODUCTOS POR CAMPAÑA //
@When('el usuario "{user}" visualiza el listado de campañas para el hub "{hub}"')
def when_the_user_access_the_campaign_list(context, user, hub):
    get_campaigns_by_hub(context, user, hub)


@Then('se retornan las campañas  para el hub "{hub}" para el usuario "{user}"')
def assert_when_the_user_access_the_campaign_list(context, hub, user):
    assert_get_campaigns_by_hub(context, hub, user)


@When('el usuario "{user}" ingresa a la campaña "{campaign}"')
def get_campaign_data(context, user, campaign):
    # This is just a step to complete the presentational test case
    pass


@Then('se retorna el listado de productos para la campaña "{campaign}" para el usuario "{user}"')
def assert_campaigns_products_list(context, campaign, user):
    campaigns = context.store_user.campaigns_by_hub[campaign]
    if not isinstance(campaigns, list):
        campaigns = [campaigns]

    for banner in campaigns:
        if banner:
            assert len(banner['productResponseList']) > 0, (
                f'[ERROR] El listado de productos para la campaña "{banner["title"]}" esta vacio'
                f'\n [Received Products]: {banner["productResponseList"]}'
            )
