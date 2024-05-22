from behave import *  # NOSONAR
from features.helpers.shopping_cart_helper import get_user_orders, assert_get_user_orders
from features.helpers.orders_helper import get_order_detail, assert_get_order_detail


@When('el usuario "{user}" ingresa a la vista de pedidos')
def when_the_user_access_to_orders_screen(context, user):
    get_user_orders(context, user)


@Then('el usuario "{user}" no tiene pedidos')
def assert_first_login_orders(context, user):
    assert context.orders_response.status_code == 201, (
        '[ERROR] No se pudo obtener los pedidos del usuario'
        f' \n[Expected Status Code]: 201'
        f' \n[Received Status Code]: {context.orders_response.status_code}')

    assert len(context.orders_response.body["result"]) == 0, (
        '[ERROR] El usuario no cuenta con pedidos'
        f' \n[Expected Status Code]: 200'
        f' \n[Received Status Code]: {context.orders_response.status_code}')

    context.app_user.orders = context.orders_response.body["result"]
    context.VALUES["USER_DATA"].update(context.app_user.get_user())


@Then('se listan todos los pedidos realizados por el usuario "{user}"')
def assert_when_the_user_access_to_orders_screen(context, user):
    assert_get_user_orders(context)


@When('el usuario "{user}" ingresa al detalle del pedido')
def when_the_user_access_to_the_order_detail(context, user):
    get_order_detail(context, user)


@Then('se muestra el detalle del pedido para el usuario "{user}"')
def assert_when_the_user_access_to_the_order_detail(context, user):
    assert_get_order_detail(context)
