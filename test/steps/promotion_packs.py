from datetime import datetime, timedelta
from random import choice

from behave import *  # NOSONAR
from features.helpers.library_helper import get_categories, assert_get_categories
from features.helpers.products_helper import (search_product_by_sku, assert_search_product_by_sku,
                                              get_all_products, assert_get_all_products)

from src.lib.api.library_api import HaertLib


@When('el usuario "{user}" el usuario accede al modulo de promociones')
def list_all_pack_promotions(context, user):
    haert_client = HaertLib(f'{context.HOST}/{context.PATHS["haert"]}', application=context.APPLICATION,
                            client_id=context.VALUES["USER_DATA"][user]["session"]["client_id"],
                            firebase_token=context.VALUES["USER_DATA"][user]["session"]["firebase_token"],
                            identity_token=context.VALUES["USER_DATA"][user]["session"]["identity_token"],
                            token=context.VALUES["USER_DATA"][user]["session"]["token"])
    context.list_all_pack_promotions_response = haert_client.get_all_promotions(
        context.store_user.session["user"]["storeId"])


@Then('se listan en una tabla todas las promociones para el usuario "{user}"')
def assert_list_all_pack_promotions(context, user):
    assert context.list_all_pack_promotions_response.status_code == 200, (
        '[ERROR] No se pudo obtener las promociones'
        '\n [Expected Status Code]: 200'
        f'\n [Received Status Code]: {context.list_all_pack_promotions_response.status_code}'
    )
    assert len(context.list_all_pack_promotions_response.body) > 0, '[ERROR] No se obtuvieron promociones.'
    context.store_user.promotions = context.list_all_pack_promotions_response.body


@When('el usuario "{user}" ingresa al detalle del pack "{pack_id}"')
def get_pack(context, user, pack_id):
    haert_client = HaertLib(f'{context.HOST}/{context.PATHS["haert"]}', application=context.APPLICATION,
                            client_id=context.VALUES["USER_DATA"][user]["session"]["client_id"])
    context.get_pack_response = haert_client.get_promotion_detail(
        context.VALUES["USER_DATA"][user]["session"]["user"]["storeId"], pack_id)


@Then('se retorna la informacion de la promocion pack "{pack_id}" para el usuario "{user}"')
def assert_get_pack(context, pack_id, user):
    err_code = context.get_pack_response.body[
        'code'] if context.get_pack_response.status_code == 422 else None
    err_msg = context.get_pack_response.body[
        'exceptionMessage'] if context.get_pack_response.status_code == 422 else None
    assert context.get_pack_response.status_code == 200, (
        '[ERROR] No se pudo obtener la informacion del pack'
        '\n [Expected Status Code]: 200'
        f'\n [Received Status Code]: {context.get_pack_response.status_code}'
        f'\n [Error Code]: {err_code}'
        f'\n [Error Message]: {err_msg}'
    )

    assert context.get_pack_response.body["externalId"] == pack_id, (
        '[ERROR] El id del pack no coincide con el esperado'
        f'\n [Expected Pack Id]: {pack_id}'
        f'\n [Received Pack Id]: {context.get_pack_response.body["externalId"]}'
    )

    assert len(context.get_pack_response.body["productPromotionsDetails"]) > 0, (
        '[ERROR] El pack no tiene productos asociados'
        f'\n [Received Products]: {context.get_pack_response.body["productPromotionsDetails"]}'
    )

    assert context.get_pack_response.body["name"] is not None, '[ERROR] El pack no tiene nombre'
    assert context.get_pack_response.body["promotionalPrice"] > 0, '[ERROR] El precio del pack es negativo'

    context.app_user.selected_pack_product = context.get_pack_response.body


@Given('un set de productos para crear un kit de promocion')
def get_products_for_kit(context):
    context.products_for_kit = []
    for row in context.table:
        search_product_by_sku(context, row["sku"])
        assert_search_product_by_sku(context)
        product = {
            "productSku": context.product["sku"],
            "productLabel": context.product["label"],
            "requiredQuantity": row["requiredQuantity"],
            "unitPrice": row["unitPrice"]
        }
        context.store_user.promotion.products.append(product)


@When('el usuario "{user}" crea un nuevo kit de promociones con productos')
def create_promotion_kit(context, user):
    context.store_user.promotion.create_promotion_kit()
    context.store_user.promotions.append(context.store_user.promotion)


@Then('el kit de promociones es creado exitosamente por el usuario "{user}"')
def assert_create_promotion_kit(context, user):
    assert context.store_user.promotion is not None, '[ERROR] El kit de promociones no se creo correctamente'


@When('el usuario "{user}" realiza la carga del kit de promociones')
def upload_promotion_kit(context, user):
    haert_client = HaertLib(f'{context.HOST}/{context.PATHS["haert"]}', application=context.APPLICATION,
                            client_id=context.VALUES["USER_DATA"][user]["session"]["client_id"],
                            token=context.store_user.session["token"],
                            access_token=context.store_user.session["access_token"],
                            firebase_token=context.store_user.session["firebase_token"],
                            identity_token=context.store_user.session["identity_token"])
    promotion = context.store_user.promotion.get_promotion()
    promotion["products"] = promotion.pop("productPromotionsDetails")
    context.bulk_promotion_kit_response = haert_client.upload_promotion_kit(
        context.store_user.session["user"]["storeId"], promotion)


@Then('el kit de promocion es cargado exitosamente por el usuario "{user}"')
def assert_upload_promotion_kit(context, user):
    assert context.bulk_promotion_kit_response.status_code == 201, (
        '[ERROR] No se pudo crear el kit de promociones'
        '\n [Expected Status Code]: 201'
        f'\n [Received Status Code]: {context.bulk_promotion_kit_response.status_code}'
    )
    for promotion in context.bulk_promotion_kit_response.body:
        assert promotion["storeId"] == context.VALUES["USER_DATA"][user]["session"]["user"][
            "storeId"], (
            '[ERROR] El id de la tienda no coincide con el esperado'
            f'\n [Expected Store Id]: {context.VALUES["USER_DATA"][user]["session"]["user"]["storeId"]}'
            f'\n [Received Store Id]: {context.bulk_promotion_kit_response.body["storeId"]}'
        )
        assert len(promotion["productPromotionsDetails"]) > 0, (
            '[ERROR] El pack no tiene productos asociados'
            f'\n [Expected Products]: {context.promotions[0].products}'
            f'\n [Received Products]: {context.bulk_promotion_kit_response.body["productPromotionsDetails"]}'
        )
        assert promotion["externalId"] == context.store_user.promotions[0].external_promotion_id, (
            '[ERROR] El id del pack no coincide con el esperado'
            f'\n [Expected Pack Id]: {context.store_user.promotions[0].external_promotion_id}'
            f'\n [Received Pack Id]: {context.bulk_promotion_kit_response.body["externalId"]}'
        )
        assert promotion["promotionalPrice"] == context.store_user.promotions[0].promotional_price, (
            '[ERROR] El precio del pack no coincide con el esperado'
            f'\n [Expected Pack Price]: {context.store_user.promotions[0].promotional_price}'
            f'\n [Received Pack Price]: {context.bulk_promotion_kit_response.body["promotionalPrice"]}'
        )

        assert promotion["promotionInitialDate"] == context.store_user.promotions[0].promotion_initial_date, (
            '[ERROR] La fecha de inicio de la promocion no coincide con la esperada'
            f'\n [Expected Initial Date]: {context.store_user.promotions[0].promotion_initial_date}'
            f'\n [Received Initial Date]: {context.bulk_promotion_kit_response.body["promotionInitialDate"]}'
        )
        assert promotion["promotionDueDate"] == context.store_user.promotions[0].promotion_due_date, (
            '[ERROR] La fecha de vencimiento de la promocion no coincide con la esperada'
            f'\n [Expected Due Date]: {context.store_user.promotions[0].promotion_due_date}'
            f'\n [Received Due Date]: {context.bulk_promotion_kit_response.body["promotionDueDate"]}'
        )
        assert promotion["promotionInitialDate"] < promotion["promotionDueDate"], (
            '[ERROR] La fecha de inicio de la promocion es mayor a la fecha de finalizacion'
            f'\n [Initial Date]: {context.bulk_promotion_kit_response.body["promotionInitialDate"]}'
            f'\n [Due Date]: {context.bulk_promotion_kit_response.body["promotionDueDate"]}'
        )
        assert not promotion["enabled"], '[ERROR] La promocion esta habilitada sin tener pack asociado'
        assert promotion["type"] == context.store_user.promotions[0].type, (
            '[ERROR] El tipo de promocion no coincide con el esperado'
            f'\n [Expected Type]: {context.store_user.promotions[0].type}'
            f'\n [Received Type]: {context.bulk_promotion_kit_response.body["type"]}'
        )


@When('el usuario de tienda "{user}" visualiza el listado de categorias para la tienda "{hub}"')
def get_categories_by_store(context, user, hub):
    get_categories(context, user)


@Then('se retornan las categorias para la tienda "{hub}" para el usuario de tienda "{user}"')
def assert_get_categories_by_store(context, hub, user):
    assert_get_categories(context)


@When('el usuario "{user}" crea un nuevo producto pack para la categoria "{category}" subcategoria "{'
      'child_category}"')
def create_product_pack(context, user, category, child_category):
    context.store_user.find_category(category, context.store_user.store.categories)
    context.store_user.find_child_category(child_category, context.store_user.selected_category["childCategories"])
    get_all_products(context, 10, context.store_user.selected_hub["storeSubsidiaryId"])
    assert_get_all_products(context, 10)
    related_products = [{"productExternalId": product.external_id} for product in
                        context.store_user.store.products[:5]]
    replacement_products = [{"productExternalId": product.external_id} for product in
                            context.store_user.store.products[5:]]
    context.store_user.pack_product.create_product(context.store_user.selected_category["externalId"],
                                                   context.store_user.selected_child_category["externalId"],
                                                   related_products, replacement_products,
                                                   promotion_ext_id=context.store_user.promotion.external_promotion_id)


@When('el usuario "{user}" realiza la carga del pack')
def upload_product_pack(context, user):
    product_client = HaertLib(f'{context.HOST}/{context.PATHS["haert"]}', application=context.APPLICATION,
                              client_id=context.VALUES["USER_DATA"][user]["session"]["client_id"],
                              firebase_token=context.VALUES["USER_DATA"][user]["session"]["firebase_token"],
                              identity_token=context.VALUES["USER_DATA"][user]["session"]["identity_token"],
                              token=context.VALUES["USER_DATA"][user]["session"]["token"])
    context.bulk_product_pack_response = product_client.upload_pack_product(
        context.VALUES["USER_DATA"][user]["session"]["user"]["storeId"],
        context.store_user.pack_product.get_product())


@Then('el pack es cargado exitosamente por el usuario "{user}"')
def assert_upload_product_pack(context, user):
    assert context.bulk_product_pack_response.status_code == 201, (
        '[ERROR] No se pudo crear el pack'
        '\n [Expected Status Code]: 201'
        f'\n [Received Status Code]: {context.bulk_product_pack_response.status_code}'
    )

    assert len(context.bulk_product_pack_response.body["productResponses"]) > 0, (
        '[ERROR] No se pudo crear el pack'
        f'\n [Expected Products]: {context.store_user.pack_products}'
        f'\n [Received Products]: {context.bulk_product_pack_response.body["productResponses"]}'
    )
    for pack in context.bulk_product_pack_response.body["productResponses"]:
        assert pack["storeId"] == context.VALUES["USER_DATA"][user]["session"]["user"]["storeId"], (
            '[ERROR] El id de la tienda no coincide con el esperado'
            f'\n [Expected Store Id]: {context.VALUES["USER_DATA"][user]["session"]["user"]["storeId"]}'
            f'\n [Received Store Id]: {pack["storeId"]}'
        )
        assert pack["sku"] == context.store_user.pack_product.sku, (
            '[ERROR] El sku del pack no coincide con el esperado'
            f'\n [Expected Pack Sku]: {context.store_user.pack_products[0].sku}'
            f'\n [Received Pack Sku]: {pack["sku"]}'
        )
        assert len(pack["categories"]) > 0, (
            '[ERROR] El pack no tiene categorias asociadas'
            f'\n [Expected Categories]: {context.store_user.pack_products[0].categories}'
            f'\n [Received Categories]: {pack["categories"]}'
        )
        assert pack["imageUrl"] == context.store_user.pack_product.image_url, (
            '[ERROR] El pack no tiene imagen asociada'
            f'\n [Expected Image Url]: {context.store_user.pack_product.image_url}'
            f'\n [Received Image Url]: {pack["imageUrl"]}'
        )
        assert pack["label"] == context.store_user.pack_product.label, (
            '[ERROR] El pack no tiene nombre'
            f'\n [Expected Name]: {context.store_user.pack_product.label}'
            f'\n [Received Name]: {pack["label"]}'
        )
        assert pack["enabled"], '[ERROR] El pack no esta habilitado'


@Given('el usuario "{user}" selecciona una promocion pack vigente')
def get_active_random_pack_promotion(context, user):
    list_all_pack_promotions(context, user)
    assert_list_all_pack_promotions(context, user)
    active_promotions = context.store_user.filter_active_promotion_packs()
    assert len(active_promotions) > 0, '[ERROR] No hay promociones packs vigentes'
    context.store_user.selected_promotion_pack = choice(active_promotions)
    context.promotion_pack_to_edit = context.store_user.selected_promotion_pack.copy()

    context.promotion_pack_to_edit.update({
        "name": f"Promocion {context.promotion_pack_to_edit['name']} edited",
        "promotionInitialDate": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
        "promotionDueDate": (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%dT%H:%M:%S'),
    })


@When('el usuario "{user}" edita la promocion pack')
def edit_promotion_pack(context, user):
    haert_client = HaertLib(f'{context.HOST}/{context.PATHS["haert"]}', application=context.APPLICATION,
                            client_id=context.VALUES["USER_DATA"][user]["session"]["client_id"],
                            firebase_token=context.VALUES["USER_DATA"][user]["session"]["firebase_token"],
                            identity_token=context.VALUES["USER_DATA"][user]["session"]["identity_token"],
                            token=context.VALUES["USER_DATA"][user]["session"]["token"])

    context.edit_promotion_pack_response = haert_client.edit_promotion_pack(context.store_user.session["user"][
                                                                                "storeId"],
                                                                            context.promotion_pack_to_edit)


@Then('la promocion pack es editado exitosamente por el usuario "{user}"')
def step_impl(context, user):
    assert context.edit_promotion_pack_response.status_code == 200, (
        '[ERROR] No se pudo editar la promocion pack'
        '\n [Expected Status Code]: 200'
        f'\n [Received Status Code]: {context.edit_promotion_pack_response.status_code}'
    )
    assert context.edit_promotion_pack_response.body["name"] == context.promotion_pack_to_edit["name"], (
        '[ERROR] El nombre de la promocion pack no coincide con el enviado para la edicion'
        f'\n [Expected Name]: {context.promotion_pack_to_edit["name"]}'
        f'\n [Received Name]: {context.edit_promotion_pack_response.body["name"]}'
    )

    assert context.edit_promotion_pack_response.body["promotionInitialDate"] == context.promotion_pack_to_edit[
        "promotionInitialDate"], (
        '[ERROR] La fecha de inicio de la promocion pack no coincide con la enviada para la edicion'
        f'\n [Expected Initial Date]: {context.promotion_pack_to_edit["promotionInitialDate"]}'
        f'\n [Received Initial Date]: {context.edit_promotion_pack_response.body["promotionInitialDate"]}'
    )

    assert context.edit_promotion_pack_response.body["promotionDueDate"] == context.promotion_pack_to_edit[
        "promotionDueDate"], (
        '[ERROR] La fecha de vencimiento de la promocion pack no coincide con la enviada para la edicion'
        f'\n [Expected Due Date]: {context.promotion_pack_to_edit["promotionDueDate"]}'
        f'\n [Received Due Date]: {context.edit_promotion_pack_response.body["promotionDueDate"]}'
    )

    assert context.edit_promotion_pack_response.body["name"] != context.store_user.selected_promotion_pack["name"], (
        '[ERROR] El nombre de la promocion pack no coincide con el esperado'
        f'\n [Expected Name]: {context.store_user.selected_promotion_pack["name"]}'
        f'\n [Received Name]: {context.edit_promotion_pack_response.body["name"]}'
    )

    assert (context.edit_promotion_pack_response.body["promotionInitialDate"] !=
            context.store_user.selected_promotion_pack["promotionInitialDate"]), (
        '[ERROR] La fecha de inicio de la promocion pack no se edito correctamente'
        f'\n [Expected Initial Date]: {context.store_user.selected_promotion_pack["promotionInitialDate"]}'
        f'\n [Received Initial Date]: {context.edit_promotion_pack_response.body["promotionInitialDate"]}'
    )

    assert context.edit_promotion_pack_response.body["promotionDueDate"] != context.store_user.selected_promotion_pack[
        "promotionDueDate"], (
        '[ERROR] La fecha de vencimiento de la promocion pack no se edito correctamente'
        f'\n [Expected Due Date]: {context.store_user.selected_promotion_pack["promotionDueDate"]}'
        f'\n [Received Due Date]: {context.edit_promotion_pack_response.body["promotionDueDate"]}'
    )
