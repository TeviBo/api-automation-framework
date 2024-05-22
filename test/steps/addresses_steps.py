from random import choice

from behave import *  # NOSONAR

from features.helpers.address_helper import get_addresses, assert_get_addresses, select_address, assert_select_address
from src.lib.api.customer_profile_api import CustomerProfileClient


@When('el usuario "{user}" solicita sus direcciones')
def step_impl(context, user):
    get_addresses(context, user)


@Then('se retornan todas las direcciones del usuario "{user}"')
def step_impl(context, user):
    assert_get_addresses(context)


@When('el usuario "{user}" añade una nueva direccion para el hub "{hub}"')
def add_new_address(context, user, hub):
    customer_profile_client = CustomerProfileClient(f'{context.HOST}/{context.PATHS["private"]}',
                                                    application=context.APPLICATION,
                                                    access_token=context.VALUES["USER_DATA"][user]["session"][
                                                        "access_token"],
                                                    user_id=context.VALUES["USER_DATA"][user]["session"]["userId"],
                                                    app_version=context.APP_VERSION, platform=context.PLATFORM)
    new_address = {
        "countryCode": context.APP_ENV_VARS["addresses"][hub]['countryCode'],
        "departmentCode": context.APP_ENV_VARS["addresses"][hub]['departmentCode'],
        "provinceCode": context.APP_ENV_VARS["addresses"][hub]['provinceCode'],
        "districtCode": context.APP_ENV_VARS["addresses"][hub]['districtCode'],
        "trackType": context.APP_ENV_VARS["addresses"][hub]['trackType'],
        "trackName": context.APP_ENV_VARS["addresses"][hub]['trackName'],
        "trackNumber": context.APP_ENV_VARS["addresses"][hub]['trackNumber'],
        "inside": None,
        "reference": context.APP_ENV_VARS["addresses"][hub]["reference"],
        "latitude": context.APP_ENV_VARS["addresses"][hub]['latitude'],
        "longitude": context.APP_ENV_VARS["addresses"][hub]['longitude'],
        "title": context.APP_ENV_VARS["addresses"][hub]['title'],
        "isPrincipal": context.APP_ENV_VARS["addresses"][hub]['isPrincipal']
    }
    context.new_address_response = customer_profile_client.add_new_address(new_address)


@Then('la direccion del usuario "{user}" es añadida exitosamente')
def assert_add_new_address(context, user):
    err_msg = context.new_address_response.body["detail"][
        "text"] if context.new_address_response.status_code == 422 else None
    err_code = context.new_address_response.body["code"] if context.new_address_response.status_code == 422 else None
    assert context.new_address_response.status_code == 201, (
        '[ERROR] No se pudo añadir la direccion'
        '\n [Expected Status Code]: 201'
        f'\n [Received Status Code]: {context.new_address_response.status_code}'
        f'\n [Error Message]: {err_msg}'
        f'\n [Error Code]: {err_code}'
    )
    assert context.new_address_response.body['shippingAddressesId'] is not None, (
        '[ERROR] No se pudo obtener el id de la direccion'
    )

    if context.VALUES["USER_DATA"][user]["addresses"]:
        context.app_user.addresses.append(context.new_address_response.body)
        context.VALUES["USER_DATA"].update(context.app_user.get_user())


def delete_address_by_id(context, address_api, address):
    context.delete_address_response = address_api.delete_address(address["shippingAddressesId"])


def delete_address_by_title(context, user, address_api, address_title):
    deleted_address = None

    def perform_address_deletion(user, address_title):
        nonlocal deleted_address
        for index, add in enumerate(context.VALUES["USER_DATA"][user]["addresses"]):
            if add['title'] == address_title:
                deleted_address = context.VALUES["USER_DATA"][user]["addresses"].pop(
                    index)
                context.delete_address_response = address_api.delete_address(add['shippingAddressesId'])
                return

    perform_address_deletion(user, address_title)

    if not deleted_address:
        add_new_address(context, user, address_title.split(' ')[2])
        assert_add_new_address(context, user)
        perform_address_deletion(user, address_title)

    if deleted_address:
        context.address_to_delete = deleted_address


@When('el usuario "{user}" elimina la direccion con nombre "{address_to_delete}"')
def delete_address(context, user, address_to_delete):
    address_api = CustomerProfileClient(f'{context.HOST}/{context.PATHS["private"]}',
                                        application=context.APPLICATION,
                                        access_token=context.VALUES["USER_DATA"][user]["session"]["access_token"],
                                        user_id=context.VALUES["USER_DATA"][user]["session"]["userId"],
                                        app_version=context.APP_VERSION, platform=context.PLATFORM)
    if isinstance(address_to_delete, dict):
        context.address_to_delete = address_to_delete
        delete_address_by_id(context, address_api, address_to_delete)
    else:
        delete_address_by_title(context, user, address_api, address_to_delete)


@Then('la direccion del usuario "{user}" es eliminada exitosamente')
def assert_delete_address(context, user):
    assert context.delete_address_response.status_code == 204, (
        '[ERROR] No se pudo eliminar la direccion'
        '\n [Expected Status Code]: 204'
        f'\n [Received Status Code]: {context.delete_address_response.status_code}'
    )
    get_addresses(context, user)
    assert_get_addresses(context)
    assert context.address_to_delete["title"] not in \
           context.VALUES["USER_DATA"][user]["addresses"], (
        '[ERROR] La direccion no fue eliminada correctamente'
        f'\n [Deleted Address]: {context.address_to_delete}'
        f'\n [Received Addresses]: {context.VALUES["USER_DATA"][f"{user}_{context.APPLICATION.lower()}"]["addresses"]}'
    )


@When('el usuario "{user}" elimina la direccion asignada como direccion principal')
def delete_unique_address(context, user):
    address_api = CustomerProfileClient(f'{context.HOST}/{context.PATHS["private"]}',
                                        application=context.APPLICATION,
                                        access_token=context.VALUES["USER_DATA"][user]["session"]["access_token"],
                                        user_id=context.VALUES["USER_DATA"][user]["session"]["userId"],
                                        app_version=context.APP_VERSION, platform=context.PLATFORM)
    for address in context.VALUES["USER_DATA"][user]["addresses"]:
        if address['isPrincipal'] is True:
            context.delete_unique_address_response = address_api.delete_address(address['shippingAddressesId'])
            context.address_id = address['shippingAddressesId']


@Then('el sistema devuelve un mensaje de error al "{user}" indicando que no puede eliminar la direccion principal')
def assert_delete_unique_address(context, user):
    assert context.delete_unique_address_response.status_code == 422, (
        '[ERROR] La direccion principal ha sido eliminada'
        '\n[Expected Status Code]: 422'
        f'\n[Received Status Code]: {context.response.status_code}'
        f'[Address ID]: {context.address_id}'
    )
    assert context.delete_unique_address_response.body['code'] == 'CUS_REG_14', (
        '[ERROR] El codigo de error no es el esperado'
        '\n[Expected Error Code]: CUS_REG_14'
        f'\n[Received Error Code]: {context.delete_unique_address_response.body["code"]}'
    )
    expected_error_message = 'Siempre tienes que tener almenos una direccion principal'
    assert context.delete_unique_address_response.body['detail']['text'] == expected_error_message, (
        '[ERROR] El mensaje de error no es el esperado'
        '\n[Expected Error Message]: Siempre tienes que tener almenos una direccion principal'
        f'\n[Received Error Message]: {context.delete_unique_address_response.body["detail"]["text"]}'
    )


@When('el usuario "{user}" alcanzo el maximo de direcciones permitidas')
def max_addresses_limit(context, user):
    count = len(context.app_user.addresses)
    for _ in range(20):
        if count == 20:
            break
        add_new_address(context, user, "LIM014")
        assert_add_new_address(context, user)
        count += 1


@Step('el usuario "{user}" desea agregar una nueva direccion')
def step_impl(context, user):
    add_new_address(context, user, choice(['LIM014', 'LIM013']))


def clean_addresses(context, user):
    addresses_to_delete = [add for add in
                           context.VALUES["USER_DATA"][user]["addresses"] if
                           add["isPrincipal"] is False]
    for i in range(len(addresses_to_delete)):
        delete_address(context, user, addresses_to_delete[i])
        assert_delete_address(context, user)


@Then('el sistema devuelve un mensaje de error al usuario "{user}" '
      'indicando que alcanzo el maximo de direcciones permitidas')
def assert_max_addresses_limit(context, user):
    assert context.new_address_response.status_code == 422, (
        '[ERROR] Se ha agregado la direccion'
        '\n [Expected Status Code]: 422'
        f'\n [Received Status Code]: {context.new_address_response.status_code}'
    )

    assert context.new_address_response.body['code'] == 'CUS_REG_12', (
        '[ERROR] El codigo de error no es el esperado'
        '\n [Expected Error Code]: CUS_REG_12'
        f'\n [Received Error Code]: {context.new_address_response.body["code"]}'
    )
    expected_msg = (
        'Tienes demasiadas direcciones registradas, intenta eliminar alguna si deseas registrar una nueva.'
    )
    assert context.new_address_response.body['detail']['text'] == expected_msg, (
        '[ERROR] El mensaje de error no es el esperado'
        f'\n [Expected Error Message]: {expected_msg}'
        f'\n [Received Error Message]: {context.new_address_response.body["detail"]["text"]}')

    clean_addresses(context, user)

    assert len(context.VALUES["USER_DATA"][user]["addresses"]) == 1, (
        '[ERROR] No se eliminaron todas las direcciones'
        '\n [Expected Addresses Length]: 1'
        f'\n [Received Addresses Length]: '
        f'{len(context.VALUES["USER_DATA"][f"{user}_{context.APPLICATION.lower()}"]["addresses"])}')
    add_new_address(context, user, "LIM014")
    assert_add_new_address(context, user)


@Step('el usuario "{user}" selecciona la direccion "{selected_address}"')
def when_the_user_selects_an_address(context, user, selected_address):
    get_addresses(context, user)
    assert_get_addresses(context)
    select_address(context, user, selected_address)


@Then('se retona el detalle de la direccion "{selected_address}" del usuario "{user}"')
def assert_when_the_user_selects_an_address(context, selected_address, user):
    assert_select_address(context, user, selected_address)
