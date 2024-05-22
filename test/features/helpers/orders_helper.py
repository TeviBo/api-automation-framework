from random import choice

from src.lib.api.orders_api import OrdersClient


def get_order_detail(context, user):
    client = OrdersClient(f'{context.HOST}/{context.PATHS["private"]}', application=context.APPLICATION,
                          access_token=context.VALUES["USER_DATA"][user]["session"]["access_token"],
                          app_version=context.APP_VERSION,
                          user_id=context.VALUES["USER_DATA"][user]["session"]["userId"], platform=context.PLATFORM)
    if not context.app_user.selected_order:
        context.app_user.get_order(choice(context.app_user.orders).order_number)
        context.VALUES["USER_DATA"].update(context.app_user.get_user())
    context.order_detail_response = client.tracking(context.app_user.selected_order.order_number)


def assert_get_order_detail(context):
    assert context.order_detail_response.status_code == 200, (
        '[ERROR] No se pudo obtener el detalle del pedido'
        '\n[Expected Status Code]: 200'
        f'\n[Received Status Code]: {context.order_detail_response.status_code}'
    )
    assert context.order_detail_response.body is not None, (
        '[ERROR] El detalle del pedido esta vacio'
        f'\n[Received Body]: {context.order_detail_response.body}')

    context.app_user.selected_order_detail = context.order_detail_response.body
    context.VALUES["USER_DATA"].update(context.app_user.get_user())
