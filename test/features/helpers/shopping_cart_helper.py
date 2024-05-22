from features.helpers.search_helper import search_products, assert_search_products
from src.lib.api.shopping_cart_api import ShoppingCartClient


def get_cart(context, user):
    shopping_cart_api = ShoppingCartClient(f'{context.HOST}/{context.PATHS["private"]}',
                                           application=context.APPLICATION,
                                           access_token=context.VALUES["USER_DATA"][user]["session"]["access_token"],
                                           user_id=context.VALUES["USER_DATA"][user]["session"]["userId"],
                                           app_version=context.APP_VERSION, platform=context.PLATFORM)
    context.get_shopping_cart_response = shopping_cart_api.get_user_cart()


def assert_get_cart(context):
    assert context.get_shopping_cart_response.status_code == 201, (
        '[ERROR] No se pudo obtener el carrito'
        '\n [Expected Status Code]: 201'
        f'\n [Received Status Code]: {context.get_shopping_cart_response.status_code}')

    if len(context.get_shopping_cart_response.body) > 0:
        context.app_user.cart = context.get_shopping_cart_response.body[0]
        context.VALUES["USER_DATA"].update(context.app_user.get_user())


def get_user_orders(context, user):
    shopping_cart_client = ShoppingCartClient(f'{context.HOST}/{context.PATHS["private"]}',
                                              application=context.APPLICATION,
                                              access_token=context.VALUES["USER_DATA"][user]["session"]["access_token"],
                                              app_version=context.APP_VERSION,
                                              user_id=context.VALUES["USER_DATA"][user]["session"]["userId"],
                                              platform=context.PLATFORM)
    context.orders_response = shopping_cart_client.get_orders()


def assert_get_user_orders(context):
    assert context.orders_response.status_code == 201, (
        '[ERROR] No se pudo obtener los pedidos del usuario'
        f' \n[Expected Status Code]: 201'
        f' \n[Received Status Code]: {context.orders_response.status_code}')

    if context.APPLICATION == "JKR":
        assert len(context.orders_response.body["result"]) > 0, (
            '[ERROR] El usuario no cuenta con pedidos'
            f' \n[Expected Len]: >0'
            f' \n[Received Len]: {len(context.orders_response.body["result"])}')
    context.app_user.orders = context.orders_response.body["result"]
    context.VALUES["USER_DATA"].update(context.app_user.get_user())


def add_product_to_cart(context, user, quantity, product_to_add):
    cart_api = ShoppingCartClient(f'{context.HOST}/{context.PATHS["private"]}',
                                  application=context.APPLICATION,
                                  access_token=context.VALUES["USER_DATA"][user]["session"]["access_token"],
                                  user_id=context.VALUES["USER_DATA"][user]["session"]["userId"],
                                  app_version=context.APP_VERSION, platform=context.PLATFORM)
    assert context.app_user.selected_product.label == product_to_add.label, (
        '[ERROR] el producto a agregar no coincide con el seleccionado'
        f'\n [To Add]: {product_to_add}.'
        f'\n [Selected]: {context.app_user.selected_product.label}'
    )
    context.add_product_to_cart_response = cart_api.add_item_to_cart(
        context.app_user.selected_product.get_product(), quantity)


def assert_add_product_to_cart(context, quantity, product):
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
        if prod["product"]["productLabel"] == product:
            assert prod['product']['unitCount'] == float(quantity), (
                '[ERROR] La cantidad de items agregados no es la esperada'
                f'\n [Expected Quantity]: {int(quantity)}'
                f'\n [Received Quantity]: {prod["product"]["unitCount"]}'
            )
            break
    context.app_user.selected_product.quantity_purchased = float(quantity)
    context.app_user.purchased_products.append(context.app_user.selected_product)
    context.app_user.cart = context.add_product_to_cart_response.body
    context.VALUES["USER_DATA"].update(context.app_user.get_user())


def create_cart(context, user: str):
    for row in context.table:
        search_products(context, user=user, keyword=row["product"])
        assert_search_products(context, keyword=row["product"])
        context.app_user.find_product(row["product"], context.store_user.store.products)
        context.VALUES["USER_DATA"].update(context.app_user.get_user())
        add_product_to_cart(context, user, row["quantity"], context.app_user.selected_product)
        assert_add_product_to_cart(context, row["quantity"], row["product"])


def get_shopping_cart_full_data(context, user):
    cart_client = ShoppingCartClient(f'{context.HOST}/{context.PATHS["private"]}', application=context.APPLICATION,
                                     access_token=context.VALUES["USER_DATA"][user]["session"]["access_token"],
                                     user_id=context.VALUES["USER_DATA"][user]["session"]["userId"],
                                     app_version=context.APP_VERSION)
    context.cart_get_full_data_response = cart_client.get_full_data(context.app_user.cart.shopping_cart_id)


def assert_get_shopping_cart_full_data(context):
    assert context.cart_get_full_data_response.status_code == 200, (
        '[ERROR] No se pudo obtener los datos del carrito'
        '\n [Expected Status Code]: 200'
        f'\n [Received Status Code]: {context.cart_get_full_data_response.status_code}')

    assert context.cart_get_full_data_response.body["shoppingCart"]["externalOrderNumber"], (
        '[ERROR] el campo nota de venta viene vacio'
        '\n [Expected Value]: id con la nota de venta en la propiedad "externalOrderNumber"'
        f'\n [Received Value]: {context.cart_get_full_data_response.body["shoppingCart"].get(["externalOrderNumber"])}'
    )

    context.app_user.selected_order.external_order_number = \
        context.cart_get_full_data_response.body["shoppingCart"]["externalOrderNumber"]
    context.VALUES["USER_DATA"].update(context.app_user.get_user())
