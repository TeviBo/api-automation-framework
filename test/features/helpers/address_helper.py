from src.lib.api.customer_profile_api import CustomerProfileClient


def get_addresses(context, user):
    customer_profile_client = CustomerProfileClient(f'{context.HOST}/{context.PATHS["private"]}',
                                                    application=context.APPLICATION,
                                                    access_token=context.VALUES["USER_DATA"][user]["session"][
                                                        "access_token"],
                                                    user_id=context.VALUES["USER_DATA"][user]["session"]["userId"],
                                                    app_version=context.APP_VERSION, platform=context.PLATFORM)
    context.get_addresses_response = customer_profile_client.get_addresses()


def assert_get_addresses(context):
    assert context.get_addresses_response.status_code == 200, (
        '[ERROR] No se pudo obtener las direcciones'
        '\n [Expected Status Code]: 200'
        f'\n [Received Status Code]: {context.get_addresses_response.status_code}')
    assert len(context.get_addresses_response.body) > 0, (
        '[ERROR] la lista de direcciones esta vacia'
        f'[Received Addresses]: {context.get_addresses_response.body}')
    context.app_user.addresses = context.get_addresses_response.body
    context.VALUES["USER_DATA"].update(context.app_user.get_user())


def select_address(context, user, selected_address):
    address = context.app_user.get_address(selected_address)
    address_api = CustomerProfileClient(f'{context.HOST}/{context.PATHS["private"]}',
                                        application=context.APPLICATION,
                                        access_token=context.VALUES["USER_DATA"][user]["session"]["access_token"],
                                        user_id=context.VALUES["USER_DATA"][user]["session"]["userId"],
                                        app_version=context.APP_VERSION, platform=context.PLATFORM)
    context.get_address_detail_response = address_api.get_address_detail(address["shippingAddressesId"])


def assert_select_address(context, user, selected_address):
    assert context.get_address_detail_response.status_code == 200, (
        '[ERROR] No se pudo obtener el detalle de la direccion'
        '\n [Expected Status Code]: 200'
        f'\n [Received Status Code]: {context.get_address_detail_response.status_code}'
    )
    assert context.get_address_detail_response.body is not None, (
        '[ERROR] No se pudo obtener el detalle de la direccion'
        f'\n [Received Address]: {context.VALUES["USER_DATA"][user]["selected_address"]}')
    context.app_user.selected_address = context.get_address_detail_response.body
    assert context.app_user.selected_address["title"] == selected_address, (
        '[ERROR] el nombre de la direccion seleccionada no coincide con el esperado.'
        f'\n [Expected]: {selected_address}'
        f'\n [Received]: {context.app_user.selected_address["title"]}'
    )
    context.VALUES["USER_DATA"].update(context.app_user.get_user())
