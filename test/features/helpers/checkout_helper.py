from features.helpers.address_helper import get_addresses, assert_get_addresses, select_address, assert_select_address
from features.helpers.cards_helper import get_user_cards, assert_get_user_cards
from src.lib.api.shopping_cart_api import ShoppingCartClient
from src.utils.logger import logger


def checkout_address(context, user, selected_address):
    get_addresses(context, user)
    assert_get_addresses(context)
    select_address(context, user, selected_address)
    assert_select_address(context, user, selected_address)
    shopping_cart_client = ShoppingCartClient(f'{context.HOST}/{context.PATHS["private"]}',
                                              application=context.APPLICATION,
                                              access_token=context.VALUES["USER_DATA"][user]["session"]["access_token"],
                                              user_id=context.VALUES["USER_DATA"][user]["session"]["userId"],
                                              app_version=context.APP_VERSION, platform=context.PLATFORM)
    context.update_address_checkout_response = shopping_cart_client.checkout(
        "change_address", context.app_user.cart.store["storeId"],
        context.app_user.cart.store_subsidiary["storeSubsidiaryId"], context.app_user.cart.shopping_cart_id,
        shipping_address_id=context.app_user.selected_address["shippingAddressesId"]
    )


def assert_checkout_address(context):
    err_title = context.update_address_checkout_response.body[
        "title"] if context.update_address_checkout_response.status_code == 422 else None
    err_code = context.update_address_checkout_response.body[
        "code"] if context.update_address_checkout_response.status_code == 422 else None
    err_msg = context.update_address_checkout_response.body["detail"][
        "text"] if context.update_address_checkout_response.status_code == 422 else None
    assert context.update_address_checkout_response.status_code == 201, (
        '[ERROR] No se pudo actualizar el checkout con los datos de la direccion.'
        '\n [Expected Status Code]: 201'
        f'\n [Response Status Code]: {context.update_address_checkout_response.status_code}'
        f'\n [Error Title]: {err_title}'
        f'\n [Error Code]: {err_code}'
        f'\n [Error Message]: {err_msg}'
    )
    assert context.update_address_checkout_response.body["address"]["deliveryAddressId"] == \
           context.app_user.selected_address["shippingAddressesId"], (
        '[ERROR] La direccion de entrega no coincide con la seleccionada.'
        f'\n [Expected Address]: {context.app_user.selected_address["shippingAddressesId"]}'
        f'\n [Received Address]: {context.update_address_checkout_response.body["address"]["deliveryAddressId"]}'
    )

    assert context.update_address_checkout_response.body["status"] == "En curso", (
        '[ERROR] El estado del pedido no es el esperado'
        f'\n [Expected Status]: En curso'
        f'\n [Received Status]: {context.update_address_checkout_response.body["status"]}')

    context.app_user.cart = context.update_address_checkout_response.body
    context.VALUES["USER_DATA"].update(context.app_user.get_user())


def checkout_payment(context, user, card_branch, last_4_digits):
    get_user_cards(context, user)
    assert_get_user_cards(context)
    payment_method = {
        'branch': card_branch,
        'last_4_digits': last_4_digits
    }
    context.app_user.select_payment_method(payment_method)
    context.VALUES["USER_DATA"].update(context.app_user.get_user())
    shopping_cart_client = ShoppingCartClient(f'{context.HOST}/{context.PATHS["private"]}',
                                              application=context.APPLICATION,
                                              access_token=context.VALUES["USER_DATA"][user]["session"]["access_token"],
                                              user_id=context.VALUES["USER_DATA"][user]["session"]["userId"],
                                              app_version=context.APP_VERSION, platform=context.PLATFORM)
    context.checkout_update_payment_response = shopping_cart_client.checkout(
        "change_payment",
        context.app_user.cart.store["storeId"],
        context.app_user.cart.store_subsidiary["storeSubsidiaryId"],
        context.app_user.cart.shopping_cart_id,
        payment=context.app_user.selected_payment_method)


def assert_checkout_payment(context, user, card_branch, last_4_digits):
    assert context.checkout_update_payment_response.status_code == 201, (
        '[ERROR] No se pudo actualizar el checkout con los datos del pago.'
        '\n [Expected Status Code]: 201'
        f'\n [Response Status Code]: {context.checkout_update_payment_response.status_code}'
    )
    assert context.checkout_update_payment_response.body["address"]["deliveryAddressId"] == \
           context.app_user.selected_address["shippingAddressesId"]

    assert context.checkout_update_payment_response.body["status"] == "En curso", (
        '[ERROR] El estado del pedido no es el esperado'
        f'\n [Expected Status]: En curso'
        f'\n [Received Status]: {context.checkout_update_payment_response.body["status"]}')

    assert context.app_user.selected_payment_method is not None, (
        '[ERROR] No se pudo seleccionar la tarjeta.'
        f'\n [Expected Card]: {card_branch}'
        f'\n [Cards]: {context.VALUES["USER_DATA"][user]["cards"]}')

    received_card_branch = context.checkout_update_payment_response.body["payment"]["title"].split(" ")[1].upper()
    assert context.app_user.selected_payment_method["branch"].upper() == received_card_branch, (
        '[ERROR] No se pudo seleccionar la tarjeta.'
        f'\n [Expected Card]: {card_branch}'
        f'\n [Received Card]: {context.app_user.selected_payment_method["branch"]}'
        f'\n [Cards]: {context.VALUES["USER_DATA"][user]["cards"]}'
    )

    received_last_4_digits = context.checkout_update_payment_response.body["payment"]["description"].split(" ")[-1]

    assert context.app_user.selected_payment_method["pan"].split(" ")[-1] == received_last_4_digits, (
        '[ERROR] No se pudo seleccionar la tarjeta.'
        f'\n [Expected Card]: {last_4_digits}'
        f'\n [Received Card]: {context.app_user.selected_payment_method["pan"].split(" ")[:-1]}'
        f'\n [Cards]: {context.VALUES["USER_DATA"][user]["cards"]}'
    )
    context.app_user.cart = context.checkout_update_payment_response.body
    context.VALUES["USER_DATA"].update(context.app_user.get_user())


def complete_checkout(context, user, exception_test=False):
    shopping_cart_client = ShoppingCartClient(f'{context.HOST}/{context.PATHS["private"]}',
                                              application=context.APPLICATION,
                                              access_token=context.VALUES["USER_DATA"][user]["session"][
                                                  "access_token"],
                                              user_id=context.VALUES["USER_DATA"][user]["session"]["userId"],
                                              app_version=context.APP_VERSION, platform=context.PLATFORM)
    context.complete_checkout_response = shopping_cart_client.complete(
        store_id=context.store_user.session["user"]["storeId"],
        store_subsidiary_id=context.store_user.selected_hub["storeSubsidiaryId"],
        shopping_cart_id=context.app_user.cart.shopping_cart_id,
        shipping_addresses_id=context.app_user.selected_address["shippingAddressesId"],
        payment_id=context.app_user.cart.payment["paymentId"], exception_test=exception_test)


def assert_complete_checkout(context):
    err_code = None
    err_msg = None
    if hasattr(context.complete_checkout_response, "status_code"):
        err_code = context.complete_checkout_response.body[
            "code"] if context.complete_checkout_response.status_code == 422 else None
        err_msg = context.complete_checkout_response.body["detail"][
            "text"] if context.complete_checkout_response.status_code == 422 else None
    assert context.complete_checkout_response.status_code == 200, (
        '[ERROR] No se pudo completar el checkout.'
        '\n [Expected Status Code]: 200'
        f'\n [Response Status Code]: {context.complete_checkout_response.status_code}'
        f'\n [Error Code]: {err_code}'
        f'\n [Error Message]: {err_msg}'
    )
    assert context.complete_checkout_response.body is not None, (
        '[ERROR] No se pudo completar el checkout. El body de la respuesta es nulo.'
        f'\n [Response]: {context.complete_checkout_response.body}')

    assert context.complete_checkout_response.body["orderNumber"] is not None, (
        '[ERROR] El numero de orden es nulo.'
        f'\n [Received Order Number]: {context.complete_checkout_response.body["orderNumber"]}')

    assert context.complete_checkout_response.body["orderNumber"] != "", (
        '[ERROR] El numero de orden es vacio.'
        f'\n [Received Order Number]: {context.complete_checkout_response.body["orderNumber"]}')

    assert context.app_user.cart.assert_cart_total_amount_with_discount(context.complete_checkout_response.body,
                                                                        "equals"), (
        '[ERROR] El monto total no coincide con el esperado.'
        f'\n [Expected Total Amount]: {context.app_user.cart.expected_total_amount}'
        f'\n [Received Total Amount]: {context.complete_checkout_response.body["totalAmount"]}'
    )
    logger.debug(f'Order created successfully. Order number: {context.complete_checkout_response.body["orderNumber"]}')
    context.app_user.selected_order = context.complete_checkout_response.body
    context.VALUES["USER_DATA"].update(context.app_user.get_user())


def complete_order(context, user, selected_address, card_branch, last_4_digits):
    checkout_address(context, user, selected_address)
    assert_checkout_address(context)
    checkout_payment(context, user, card_branch, last_4_digits)
    assert_checkout_payment(context, user, card_branch, last_4_digits)
    assert context.app_user.cart.assert_cart_total_amount(context.checkout_update_payment_response.body), (
        '[ERROR] El monto total no coincide con el esperado.'
        f'\n [Expected Total Amount]: {context.app_user.cart.expected_total_amount}'
        f'\n [Received Total Amount]: {context.checkout_update_payment_response.body["bill"]["totalAmount"]}'
    )
    complete_checkout(context, user)
