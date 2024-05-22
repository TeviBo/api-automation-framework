from behave import *  # NOSONAR
from features.helpers.shopping_cart_helper import get_cart, assert_get_cart
from features.helpers.search_helper import search_products, assert_search_products

from src.lib.api.shopping_cart_api import ShoppingCartClient


@Step('el usuario "{user}" no tiene carrito')
def step_impl(context, user):
    get_cart(context, user)
    assert_get_cart(context)
    if context.app_user.cart != {} and context.app_user.purchased_products == []:
        empty_cart(context, user)
        assert_empty_cart(context, user)
        context.app_user.delete_cart()


@When('el usuario "{user}" agrega "{quantity}" unidades del producto "{product_to_add}" al carrito')
def add_product_to_cart(context, user, quantity, product_to_add):
    cart_api = ShoppingCartClient(f'{context.HOST}/{context.PATHS["private"]}', application=context.APPLICATION,
                                  access_token=context.VALUES["USER_DATA"][user]["session"]["access_token"],
                                  user_id=context.VALUES["USER_DATA"][user]["session"]["userId"],
                                  app_version=context.APP_VERSION, platform=context.PLATFORM)
    context.add_product_to_cart_response = cart_api.add_item_to_cart(
        context.app_user.selected_product.get_product(), quantity)


@Then('se agrega "{quantity}" unidades del producto "{product_to_add}" al carrito del usuario "{user}"')
def assert_add_product_to_cart(context, quantity, product_to_add, user):
    err_code = context.add_product_to_cart_response.body["code"] \
        if context.add_product_to_cart_response.status_code == 422 else None
    err_msg = context.add_product_to_cart_response.body["detail"]["text"] \
        if context.add_product_to_cart_response.status_code == 422 else None

    assert context.add_product_to_cart_response.status_code == 201, (
        '[ERROR] No se pudo agregar el item al carrito'
        '\n [Expected Status Code]: 201'
        f'\n [Received Status Code]: {context.add_product_to_cart_response.status_code}'
        f'\n [Error Code]: {err_code}'
        f'\n [Error Message]: {err_msg}'
        f'\n [Added Product]: {context.app_user.selected_product.get_product()}'
    )

    for prod in context.add_product_to_cart_response.body["items"]:
        if prod["product"]["productId"] == int(quantity):
            assert prod['product']['unitCount'] == context.app_user.selected_product.quantity_purchased, (
                '[ERROR] La cantidad de items agregados no es la esperada'
                f'\n [Expected Quantity]: {int(quantity)}'
                f'\n [Received Quantity]: {prod["product"]["unitCount"]}'
            )
            break
    context.app_user.selected_product.quantity_purchased = float(quantity)
    context.app_user.purchased_products.append(context.app_user.selected_product)
    context.app_user.cart = context.add_product_to_cart_response.body
    context.VALUES["USER_DATA"].update(context.app_user.get_user())


@Step('la cantidad de items agregados coincide con la cantidad de items en el carrito del usuario "{user}"')
def assert_cart_items_length(context, user):
    assert context.app_user.cart.product_count == len(context.app_user.purchased_products), (
        '[ERROR] La cantidad de items recibida no coincide con la esperada'
        f'\n [Expected Items Count]: {len(context.app_user.purchased_products)}'
        f'\n [Received Items Count]: {context.add_product_to_cart_response.body["productCount"]}'
    )
    assert context.app_user.cart.assert_items_quantity_added(context.app_user.purchased_products), (
        '[ERROR] La cantidad de items agregados no coincide con la esperada'
        f'\n [Expected Items Count]: {context.VALUES["USER_DATA"][user]["selectedProduct"]["quantityPurchased"]}'
        f'\n [Received Items Count]: {context.add_product_to_cart_response.body["productCount"]}'
    )


@Step('el subtotal del carrito coincide con la sumatoria de precios de los productos del carrito del usuario "{user}"')
def assert_cart_subtotal(context, user):
    assert context.app_user.cart.assert_cart_subtotal(context.app_user.purchased_products), (
        '[ERROR] El subtotal del carrito no coincide con el esperado'
        f'\n [Expected Subtotal]: {context.app_user.cart.expected_subtotal_amount}'
        f'\n [Received Subtotal]: {context.VALUES["USER_DATA"][user]["cart"]["subTotalAmount"]}'
    )
    context.VALUES["USER_DATA"].update(context.app_user.get_user())


@When('el usuario "{user}" abre el carrito')
def when_the_user_gets_the_cart(context, user):
    get_cart(context, user)


@Then('se obtiene el carrito del usuario "{user}"')
def assert_when_the_user_gets_the_cart(context, user):
    assert_get_cart(context)


@When('el usuario "{user}" vacia el carrito')
def empty_cart(context, user):
    cart_client = ShoppingCartClient(f'{context.HOST}/{context.PATHS["private"]}', application=context.APPLICATION,
                                     access_token=context.VALUES["USER_DATA"][user]["session"]["access_token"],
                                     user_id=context.VALUES["USER_DATA"][user]["session"]["userId"],
                                     app_version=context.APP_VERSION, platform=context.PLATFORM)
    context.empty_cart_response = cart_client.empty_cart(
        context.VALUES["USER_DATA"][user]["cart"]["store"]["storeId"],
        context.VALUES["USER_DATA"][user]["cart"]["storeSubsidiary"]["storeSubsidiaryId"])


@Then('el carrito del usuario "{user}" queda vacio')
def assert_empty_cart(context, user):
    assert context.empty_cart_response.status_code == 204, (
        '[ERROR] No se pudo vaciar el carrito'
        '\n [Expected Status Code]: 204'
        f'\n [Received Status Code]: {context.empty_cart_response.status_code}')
    assert context.empty_cart_response.body == "", ('[ERROR] El carrito no quedo vacio'
                                                    f'\n [Response]: {context.empty_cart_response.body}')
    context.app_user.delete_cart()
    context.VALUES["USER_DATA"].update(context.app_user.get_user())


@When('el usuario "{user}" elimina el carrito')
def step_impl(context, user):
    empty_cart(context, user)


@Then('el carrito del usuario "{user}" es eliminado')
def step_impl(context, user):
    assert context.empty_cart_response.status_code == 204, (
        '[ERROR] No se pudo vaciar el carrito'
        '\n [Expected Status Code]: 204'
        f'\n [Received Status Code]: {context.empty_cart_response.status_code}')
    assert context.empty_cart_response.body == "", ('[ERROR] El carrito no quedo vacio'
                                                    f'\n [Response]: {context.empty_cart_response.body}')


@When('el usuario "{user}" elimina el product "{product_to_remove}" del carrito')
def remove_product_from_cart(context, user, product_to_remove):
    cart_client = ShoppingCartClient(f'{context.HOST}/{context.PATHS["private"]}', application=context.APPLICATION,
                                     access_token=context.VALUES["USER_DATA"][user]["session"]["access_token"],
                                     user_id=context.VALUES["USER_DATA"][user]["session"]["userId"],
                                     app_version=context.APP_VERSION, platform=context.PLATFORM)
    context.app_user.find_product_in_cart(product_to_remove)
    context.remove_product_from_cart_response = cart_client.remove_item_from_cart(
        context.VALUES["USER_DATA"][user]["cart"]["store"]["storeId"],
        context.VALUES["USER_DATA"][user]["cart"]["storeSubsidiary"]["storeSubsidiaryId"],
        context.app_user.selected_product.get_cart_item())


@Then('el producto es eliminado del carrito del usuario "{user}"')
def assert_remove_product_from_cart(context, user):
    assert context.remove_product_from_cart_response.status_code == 201, (
        '[ERROR] No se pudo eliminar el item del carrito'
        '\n [Expected Status Code]: 201'
        f'\n [Received Status Code]: {context.remove_product_from_cart_response.status_code}')

    assert context.remove_product_from_cart_response.body["shoppingCartId"] == \
           context.VALUES["USER_DATA"][user]["cart"][
               "shoppingCartId"], (
        '[ERROR] El carrito no es el esperado'
        f'\n [Expected Cart]: {context.VALUES["USER_DATA"][user]["cart"]["shoppingCartId"]}'
        f'\n [Received Cart]: {context.remove_product_from_cart_response.body["shoppingCartId"]}'
    )
    assert context.remove_product_from_cart_response.body["productCount"] == context.VALUES["USER_DATA"][user]["cart"][
        "productCount"] - 1, (
        '[ERROR] El producto no fue eliminado del carrito'
        f'\n [Expected Product Count]: {context.VALUES["USER_DATA"][user]["cart"]["productCount"] - 1}'
        f'\n [Received Product Count]: {context.remove_product_from_cart_response.body["productCount"]}'
    )
    assert context.app_user.selected_product.get_cart_item()["product"]["productId"] not in [
        product["product"]["productId"] for product in context.remove_product_from_cart_response.body["items"]], (
        '[ERROR] El producto no fue eliminado del carrito'
        f'\n [Expected Product ID]: {context.app_user.selected_product.get_cart_item()["product"]["productId"]}'
        f'''\n [Received Product ID]: {[product["product"]["productId"] for product in
                                        context.remove_product_from_cart_response.body["items"]]}'''
    )
    for product in context.app_user.purchased_products:
        if product.product_id == context.app_user.selected_product.get_cart_item()["product"]["productId"]:
            context.app_user.purchased_products.pop(context.app_user.purchased_products.index(product))
            break

    context.app_user.cart = context.remove_product_from_cart_response.body
    context.VALUES["USER_DATA"].update(context.app_user.get_user())


# // EXCEPTIONS

# Empty Cart
@When('el usuario "{user}" intenta eliminar nuevamente el carrito')
def empty_non_existent_cart(context, user):
    empty_cart(context, user)


@Then('el sistema devuelve un error indicando que el carrito no existe')
def assert_empty_non_existent_cart(context):
    assert context.empty_cart_response.status_code == 422, (
        '[ERROR] El carrito fue borrado exitosamente y se esperaba error'
        '\n [Expected Status Code]: 422'
        f'\n [Received Status Code]: {context.empty_cart_response.status_code}'
    )


# Product without stock

@Then('el sistema devuelve un error indicando que no hay stock suficiente')
def assert_product_max_stock_error(context):
    assert context.add_product_to_cart_response.status_code == 422, (
        '[ERROR] El producto se ha agregado exitosamente y se esperaba error por falta de stock'
        '\n [Expected Status Code]: 422'
        f'\n [Received Status Code]: {context.add_product_to_cart_response.status_code}'
    )
    assert context.add_product_to_cart_response.body["code"] == 'SHP_ADD_04', (
        '[ERROR] El codigo de error no es el esperado'
        '\n [Expected Code]: SHP_ADD_04'
        f'\n [Received Code]: {context.add_product_to_cart_response.body["code"]}'
    )
    expected_message = 'La cantidad de unidades solicitadas no puede ser reservada debido a que se excedio el stock'
    assert context.add_product_to_cart_response.body["detail"]["text"] == expected_message, (
        '[ERROR] El mensaje de error no es el esperado'
        f'\n [Expected Message]: {expected_message} '
        'stock'
        f'\n [Received Message]: {context.add_product_to_cart_response.body["detail"]["text"]}')


# Product purchase limit

@Then('el sistema devuelve un error indicando que se excedio la cantidad maxima de producto por compra')
def assert_product_limit_purchase_error(context):
    assert context.add_product_to_cart_response.status_code == 422, (
        '[ERROR] El producto se ha agregado exitosamente y se esperaba error por falta de stock'
        '\n [Expected Status Code]: 422'
        f'\n [Received Status Code]: {context.add_product_to_cart_response.status_code}'
    )
    assert context.add_product_to_cart_response.body["code"] == 'SHP_ADD_01', (
        '[ERROR] El codigo de error no es el esperado'
        '\n [Expected Code]: SHP_ADD_04'
        f'\n [Received Code]: {context.add_product_to_cart_response.body["code"]}')
    expected_message = 'Se ha excedido el limite maximo del producto por compra'
    assert context.add_product_to_cart_response.body["detail"][
               "text"] == expected_message, (
        '[ERROR] El mensaje de error no es el esperado'
        f'\n [Expected Message]: {expected_message} '
        'stock'
        f'\n [Received Message]: {context.add_product_to_cart_response.body["detail"]["text"]}')
