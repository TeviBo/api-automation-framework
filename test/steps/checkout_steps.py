from time import sleep

from behave import *  # NOSONAR

from features.helpers.address_helper import select_address, assert_select_address, get_addresses, assert_get_addresses
from features.helpers.checkout_helper import (complete_checkout, assert_complete_checkout, checkout_address,
                                              assert_checkout_address, checkout_payment, assert_checkout_payment)
from features.helpers.library_helper import (dad_login, assert_dad_login, get_orders_to_dispatch,
                                             assert_get_orders_to_dispatch, get_products_ids_to_dispatch,
                                             assert_get_products_ids_to_dispatch, assign_order_to_picker,
                                             assert_assign_order_to_picker, manual_picking, assert_manual_picking,
                                             synchronize_order, assert_synchronize_order)
from features.helpers.orders_helper import get_order_detail, assert_get_order_detail
from features.helpers.shopping_cart_helper import (get_shopping_cart_full_data, assert_get_shopping_cart_full_data,
                                                   get_user_orders, assert_get_user_orders)
from src.lib.api.library_api import BeetrackLib
from src.lib.api.orders_api import OrdersClient
from src.lib.api.shopping_cart_api import ShoppingCartClient
from src.utils.decorators import retry_until_order_status_change
from src.utils.log_verifier.log_verifier_factory.log_verifier_factory import validate_logs
from src.utils.logger import logger


@Step('el usuario "{user}" selecciona la direccion de entrega "{selected_address}"')
def mrk_checkout(context, user, selected_address):
    get_addresses(context, user)
    assert_get_addresses(context)
    select_address(context, user, selected_address)
    assert_select_address(context, user, selected_address)


@Step('el usuario "{user}" establece la direccion de entrega "{selected_address}"')
def when_the_user_set_the_delivery_address_jkr(context, user, selected_address):
    checkout_address(context, user, selected_address)


@Then('la direccion de entrega "{address_to_select}" es establecida por el usuario "{user}"')
def assert_when_the_user_set_the_delivery_address(context, address_to_select, user):
    assert_checkout_address(context)


@Then('la direccion de entrega "{address_to_select}" es seleccionada por el usuario "{user}"')
def when_the_user_set_the_delivery_address_mrk(context, address_to_select, user):
    checkout_address(context, user, address_to_select)


@Step('el usuario "{user}" selecciona la forma de pago "{payment_method}"')
def select_cash_on_delivery(context, user, payment_method):
    context.app_user.selected_payment_method = payment_method
    shopping_cart_client = ShoppingCartClient(f'{context.HOST}/{context.PATHS["private"]}',
                                              application=context.APPLICATION,
                                              access_token=context.VALUES["USER_DATA"][user]["session"]["access_token"],
                                              user_id=context.VALUES["USER_DATA"][user]["session"]["userId"],
                                              app_version=context.APP_VERSION, platform=context.PLATFORM)
    context.checkout_response = shopping_cart_client.checkout(
        "change_address", context.app_user.cart.store["storeId"],
        context.app_user.cart.store_subsidiary["storeSubsidiaryId"], context.app_user.cart.shopping_cart_id,
        shipping_address_id=context.app_user.selected_address["shippingAddressesId"],
        payment=payment_method
    )


@Then('la forma de pago "{payment_method}" es seleccionada por el usuario "{user}"')
def assert_select_payment_method(context, payment_method, user):
    assert context.app_user.selected_payment_method == payment_method, (
        '[ERROR] No se pudo seleccionar la tarjeta.'
        f'\n [Expected Payment Method]: {payment_method}'
        f'\n [Received Payment Method]: {context.app_user.selected_payment_method}')


@When('el usuario "{user}" selecciona la tarjeta "{card_branch}" terminada en "{last_4_digits}"')
def when_the_user_selects_the_payment_method(context, user, card_branch, last_4_digits):
    checkout_payment(context, user, card_branch, last_4_digits)


@Then('la tarjeta "{card_branch}" terminada en "{last_4_digits}" es seleccionada por el usuario "{user}"')
def assert_when_the_user_selects_the_payment_method(context, card_branch, last_4_digits, user):
    assert_checkout_payment(context, user, card_branch, last_4_digits)


@Step('el valor del pedido del usuario "{user}" es correcto')
def validate_order_amount(context, user):
    assert context.app_user.cart.assert_cart_total_amount(context.checkout_update_payment_response.body), (
        '[ERROR] El monto total no coincide con el esperado.'
        f'\n [Expected Total Amount]: {context.app_user.cart.expected_total_amount}'
        f'\n [Received Total Amount]: {context.checkout_update_payment_response.body["bill"]["totalAmount"]}'
    )


@Step('el valor del pedido del usuario "{user}" es el correcto')
def validate_order_amount(context, user):
    assert context.app_user.cart.assert_cart_total_amount(context.checkout_response.body), (
        '[ERROR] El monto total no coincide con el esperado.'
        f'\n [Expected Total Amount]: {context.app_user.cart.expected_total_amount}'
        f'\n [Received Total Amount]: {context.checkout_response.body["bill"]["totalAmount"]}'
    )


@When('el usuario "{user}" completa el checkout')
def when_the_user_completes_checkout(context, user):
    complete_checkout(context, user)


@When('el usuario "{user}" completa el checkout con el medio de pago invalido')
def when_the_user_completes_checkout_invalid_payment_method(context, user):
    complete_checkout(context, user, exception_test=True)


@Then('el pedido es generado exitosamente para el usuario "{user}"')
def assert_when_the_user_completes_checkout_valid_payment_method(context, user):
    assert_complete_checkout(context)


@Then('se muestra un mensaje de error al usuario "{user}" indicando que su revise los datos de su tarjeta')
def assert_invalid_card_error_message(context, user):
    assert context.complete_checkout_response.status_code == 422, (
        '[ERROR] la compra fue realizada correctamente'
        '\n[Expected Status Code]: 422'
        f'\n[Received Status Code]: {context.complete_checkout_response.status_code}]'
    )
    assert context.complete_checkout_response.body["code"] == "PAY_01", (
        '[ERROR] el codigo de error no coincide con el esperado'
        '\n[Expected Code]: PAY_01'
        f'\n[Received Code]: {context.complete_checkout_response.body["code"]}'
    )

    err_msg = 'No se ha podido procesar el pago. Por favor verifica el estado de tu tarjeta o consulta a tu banco'
    assert context.complete_checkout_response.body["detail"]["text"] == err_msg, (
        '[ERROR] el mensaje de error recibido no coincide con el esperado'
        f'\n[Expected Error Message]: {err_msg}'
        f'\n[Received Error Message]: {context.complete_checkout_response.body["detail"]["text"]}'
    )


@Step('el usuario "{user}" es redireccionado al detalle del pedido')
def step_impl(context, user):
    get_order_detail(context, user)
    assert_get_order_detail(context)


@Step('el estado de la orden del usuario "{user}" es "{order_status}"')
def validate_order_status(context, user, order_status, *args, **kwargs):
    client = OrdersClient(f'{context.HOST}/{context.PATHS["private"]}', application=context.APPLICATION,
                          access_token=context.VALUES["USER_DATA"][user]["session"]["access_token"],
                          app_version=context.APP_VERSION,
                          user_id=context.VALUES["USER_DATA"][user]["session"]["userId"], platform=context.PLATFORM)

    @retry_until_order_status_change(desired_status=order_status, max_attempts=20, wait_interval=5)
    def get_order_status():
        get_user_orders(context, user)
        assert_get_user_orders(context)
        external_order_number = context.app_user.selected_order.external_order_number
        orders_dict = {order.order_number: order for order in context.app_user.orders}
        context.app_user.selected_order = orders_dict[context.app_user.selected_order.order_number]
        context.app_user.selected_order.external_order_number = external_order_number
        context.VALUES["USER_DATA"].update(context.app_user.get_user())
        return client.tracking(context.app_user.selected_order.order_number)

    try:
        return get_order_status()
    except Exception as e:
        raise AssertionError(f'[ERROR] el pedido no ha cambiado de estado. \n[Exception Message]: {e}')


@Step('se valida la "{event_type}" generada por el pedido')
def assert_log_entries(context, event_type):
    sleep(15)
    assert validate_logs(event_type, app_user=context.app_user, store_user=context.store_user,
                         container_name='us-ux-shopping-cart-container')


@When('el usuario "{user}" aplica el cupon de descuento "{coupon_code}"')
def apply_coupon(context, user, coupon_code):
    shopping_cart_client = ShoppingCartClient(f'{context.HOST}/{context.PATHS["private"]}',
                                              application=context.APPLICATION,
                                              access_token=context.VALUES["USER_DATA"][user]["session"]["access_token"],
                                              user_id=context.VALUES["USER_DATA"][user]["session"]["userId"],
                                              app_version=context.APP_VERSION, platform=context.PLATFORM)
    context.coupon_checkout_response = shopping_cart_client.checkout(
        "apply_coupon", context.app_user.cart.store["storeId"],
        context.app_user.cart.store_subsidiary["storeSubsidiaryId"],
        context.app_user.cart.shopping_cart_id, coupon=coupon_code)


@Then('el cupon de descuento "{coupon_code}" es aplicado por el usuario "{user}"')
def assert_apply_coupon(context, coupon_code, user):
    assert context.coupon_checkout_response.status_code == 201, (
        f'[ERROR] El cupon de descuento  {coupon_code} no pudo ser aplicado.'
        '\n [Expected Status Code]: 201'
        f'\n [Response Status Code]: {context.coupon_checkout_response.status_code}'
        f'\n [Error Message]: {context.coupon_checkout_response.body["title"]}'
    )

    assert context.coupon_checkout_response.body["coupon"]["couponCode"] == coupon_code, (
        '[ERROR] El cupon de descuento no coincide con el esperado.'
        f'\n [Expected Coupon]: {coupon_code}'
        f'\n [Received Coupon]: {context.coupon_checkout_response.body["coupon"]["couponCode"]}'
    )
    if context.store_user.selected_hub["storeSubsidiaryId"] == "7f3d3c31-bdbe-4973-9071-9cda4e660fee":
        assert not context.coupon_checkout_response.body["invoice"]["enabled"], (
            '[ERROR] La factura no esta habilitada.'
        )
    else:
        assert context.coupon_checkout_response.body["invoice"]["enabled"], (
            '[ERROR] La factura no esta habilitada.'
        )
    context.app_user.cart = context.coupon_checkout_response.body
    context.VALUES["USER_DATA"].update(context.app_user.get_user())


@Step('la cantidad de soles a descontar al usuario "{user}" es "{discount_amount}"')
def assert_coupon_discount(context, user, discount_amount):
    discount = [discount for discount in context.app_user.cart.bill["itemPromotions"] if
                'Promoción Abierta' not in discount["itemName"]][0]

    assert int(float(discount["discountAmount"])) == int(discount_amount), (
        '[ERROR] El monto de descuento no coincide con el esperado.'
        f'\n [Expected Discount]: {discount_amount}'
        f'\n [Received Discount]: {int(float(discount["discountAmount"]))}'
        f'\n [Discount Name]: {discount["itemName"]}'
    )
    assert context.app_user.cart.assert_cart_total_amount_with_discount(context.coupon_checkout_response.body), (
        '[ERROR] El monto total es mayor o igual al precio sin descuento. El descuento parece no haber sido aplicado.'
        f'\n [Expected Total Amount]: {context.app_user.cart.expected_total_amount - float(discount["discountAmount"])}'
        f'\n [Received Total Amount]: {context.coupon_checkout_response.body["bill"]["totalAmount"]}'
    )


@Then('el sistema devuelve un mensaje de error por cupon invalido')
def assert_invalid_coupon_error_message(context):
    assert context.coupon_checkout_response.status_code == 422, (
        '[ERROR] El cupon no es invalido.'
        '\n [Expected Status Code]: 422'
        f'\n [Received Status Code]: {context.coupon_checkout_response.status_code}'
    )

    assert context.coupon_checkout_response.body["code"] == "COUPON_02", (
        '[ERROR] El codigo de error no es el esperado.'
        '\n [Expected Code]: COUPON_02'
        f'\n [Received Code]: {context.coupon_checkout_response.body["code"]}'
    )

    assert context.coupon_checkout_response.body["title"] == "Cupón no válido", (
        '[ERROR] El titulo del error no es el esperado.'
        '\n [Expected Title]: Cupón no válido'
        f'\n [Received Title]: {context.coupon_checkout_response.body["title"]}'
    )


# // DAD //

@When(
    'el usuario "{user}" picker "{picker_username}" se loguea en la app del DAD con contraseña "{picker_password}"')
def when_the_dad_user_logs_in(context, user, picker_username, picker_password):
    dad_login(context, picker_username, picker_password)


@Then('el usuario "{user}" inicia sesion exitosamente')
def assert_when_the_dad_user_logs_in(context, user):
    assert_dad_login(context, user)


@When('el usuario "{user}" captura la nota de venta generada por el pedido de JOKR')
def when_the_picker_user_captures_the_order_external_id(context, user):
    get_shopping_cart_full_data(context, user)


@Then('la nota de venta es capturada exitosamente por el usuario "{user}"')
def assert_when_the_picker_user_captures_the_order_external_id(context, user):
    assert_get_shopping_cart_full_data(context)


@When('el usuario "{user}" obtiene las ordenes de despacho del pedido generado')
def when_the_picker_user_obtains_the_order_dispatches(context, user):
    get_orders_to_dispatch(context, user)


@Then('se obtienen las ordenes de despacho a asignar por el usuario "{user}"')
def assert_when_the_picker_user_obtains_the_order_dispatches(context, user):
    assert_get_orders_to_dispatch(context)


@When('el usuario "{user}" obtiene los productos en el dad para asignarlos')
def when_the_picker_user_obtains_the_order_products_to_assign(context, user):
    get_products_ids_to_dispatch(context, user)


@Then('los productos son obtenidos exitosamente por el usuario "{user}"')
def assert_when_the_picker_user_obtains_the_order_products_to_assign(context, user):
    assert_get_products_ids_to_dispatch(context)


@When('el pedido es asignado al usuario "{user}"')
def when_the_order_is_assigned_to_the_picker_user(context, user):
    assign_order_to_picker(context, user)


@Then('el pedido es asignado exitosamente al usuario "{user}"')
def assert_when_the_order_is_assigned_to_the_picker_user(context, user):
    assert_assign_order_to_picker(context)


@When('el usuario "{user}" pickea "{amount_to_pick}" items del producto "{product_to_pick}"')
def when_the_picker_user_manually_picks_the_order_products(context, user, amount_to_pick, product_to_pick):
    manual_picking(context, user, amount_to_pick, product_to_pick)


@Then('los productos son pickeados exitosamente por el usuario "{user}"')
def assert_when_the_picker_user_manually_picks_the_order_products(context, user):
    assert_manual_picking(context)


@Step('el usuario "{user}" sincroniza el pedido de JOKR')
def when_the_picker_user_synchronize_the_order(context, user):
    synchronize_order(context, user)


@Then('el pedido es sincronizado exitosamente por el usuario "{user}"')
def assert_when_the_picker_user_synchronize_the_order(context, user):
    assert_synchronize_order(context)


# // BEETRACK //

@When('se filta el despacho para el pedido del cliente desde beetrack')
def beetrack_filter_dispatches(context):
    beetrack_client = BeetrackLib(context.BASE_ENV_VARS["beetrack"]["host"],
                                  token=context.BEETRACK_API_KEY)
    context.filter_dispatches_response = beetrack_client.filter_dispatches(
        context.dad_user.order_to_pick.customer["identityDocument"])


@Then('se retorna resultado')
def assert_beetrack_filter_dispatches(context):
    assert context.filter_dispatches_response.status_code == 200, (
        '[ERROR] no se ha podido filtrar los despachos.'
        '\n[Expected Status Code]: 200'
        f'\n [Received Status Code]: {context.filter_dispatches_response.status_code}'
    )
    dispatches = {dispatch["id"]: {
        "status": dispatch["status_id"], "tags": dispatch["tags"],
        "identifier": dispatch["identifier"], "contact_name": dispatch["contact_name"],
        "contact_address": dispatch["contact_address"],
        "contact_phone": dispatch["contact_phone"], "contact_id": dispatch["contact_id"],
        "contact_email": dispatch["contact_email"], "latitude": dispatch["latitude"],
        "longitude": dispatch["longitude"], "items": dispatch["items"]} for dispatch in
        context.filter_dispatches_response.body["response"]
    }

    # Find the dispatch with status != 2 and tag name "ECOMMERCEID" and value equal to ecommerce_id
    for dispatch_id, details in dispatches.items():
        if details["status"] != 2 and any(tag["name"] == "ECOMMERCEID" and
                                          tag["value"] == context.dad_user.order_to_pick.ecommerce_id for
                                          tag in details["tags"]):
            context.BEETRACK_DISPATCH = dispatches[dispatch_id]
            logger.info(f'[DISPATCH ID]: {dispatch_id}')
            logger.info(f'[ECOMMERCE ID]: {context.dad_user.order_to_pick.ecommerce_id}')
            break


@When('creamos la ruta de entrega')
def beetrack_create_route(context):
    context.BEETRACK_DISPATCH.update({"latitude": context.app_user.selected_address["latitude"],
                                      "longitude": context.app_user.selected_address["longitude"]})
    beetrack_client = BeetrackLib(context.BASE_ENV_VARS["beetrack"]["host"],
                                  token=context.BEETRACK_API_KEY)
    context.create_route_response = beetrack_client.create_route(
        [context.BEETRACK_DISPATCH], context.BEETRACK_TRUCK_IDENTIFIER,
        context.BEETRACK_DRIVER_IDENTIFIER)


@Then('se crea la ruta de entrega')
def assert_beetrack_create_route(context):
    assert context.create_route_response.status_code == 200, (
        '[ERROR] No se pudo crear la ruta.'
        '\n [Expected Status Code]: 200'
        f'\n [Received Status Code]: {context.create_route_response.status_code}'
        f'\n [Error Message]: {context.create_route_response.body["response"]}'
    )
    assert context.create_route_response.body["response"]["route_id"] != "" or \
           context.create_route_response.body["response"][
               "route_id"] is not None, '[ERROR] El id de la ruta es nulo o vacio.'

    context.BEETRACK_ROUTE_ID = context.create_route_response.body["response"]["route_id"]
    logger.info(f'[ROUTE ID]: {context.BEETRACK_ROUTE_ID}')


@When('el motorizado actualiza el estado de la orden a "{sub_status}"')
def beetrack_pick_order(context, sub_status):
    for status in context.BEETRACK_SUB_STATUSES:
        if sub_status == status["name"]:
            context.app_user.selected_order_STATUS = status
            break
    beetrack_client = BeetrackLib(context.BASE_ENV_VARS["beetrack"]["host"],
                                  token=context.BEETRACK_API_KEY)
    context.beetrack_update_route_response = beetrack_client.update_route(context.BEETRACK_ROUTE_ID,
                                                                          context.BEETRACK_TRUCK_IDENTIFIER,
                                                                          [context.BEETRACK_DISPATCH],
                                                                          context.app_user.selected_order_STATUS)


@Then('el estado de la orden es actualizado exitosamente a {sub_status}')
def assert_beetrack_pick_order(context, sub_status):
    assert context.beetrack_update_route_response.status_code == 200, (
        '[ERROR] No se pudo actualizar la ruta.'
        '\n [Expected Status Code]: 200'
        f'\n [Received Status Code]: {context.beetrack_update_route_response.status_code}'
        f'\n [Error Message]: {context.beetrack_update_route_response.body["response"]}')

    assert context.beetrack_update_route_response.body["response"]["route_id"] == context.BEETRACK_ROUTE_ID, (
        '[ERROR] El id de la ruta no coincide con el enviado.'
        f'\n [Expected Route ID]: {context.BEETRACK_ROUTE_ID}'
        f'\n [Received Route ID]: {context.beetrack_update_route_response.body["response"]["route_id"]}'
    )
