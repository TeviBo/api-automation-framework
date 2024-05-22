from behave import *  # NOSONAR
from features.helpers.address_helper import get_addresses, assert_get_addresses
from features.helpers.campaigns_helper import get_campaigns_by_hub, assert_get_campaigns_by_hub
from features.helpers.shopping_cart_helper import get_cart, assert_get_cart
from features.helpers.login_helper import generate_user, login, assert_login
from features.helpers.products_helper import get_categories_by_store, assert_get_categories_by_store

from src.lib.api.campaign_hub_api import CampaignHubClient
from src.lib.api.customer_profile_api import CustomerProfileClient
from src.lib.api.qry_catalog_api import QryCatalogClient


@Then('el sistema retorna un mensaje de error indicando que los datos son incorrectos')
def assert_wrong_login(context):
    assert context.login_response.status_code == 422, \
        '[ERROR] el status code recibido no es el esperado.' \
        f'\n [Expected Status Code]: 422\n' \
        f'\n [Received Code]: {context.login_response.status_code}'

    assert context.login_response.body['title'] == 'Tus datos son incorrectos', \
        '[ERROR] el titulo recibido no es el esperado.' \
        '\n[Expected Message]: Tus datos son incorrectos' \
        f'\n[Received Message]:{context.login_response.body["title"]}'


@Given('el usuario "{user}" con identificador "{identifier}" y contraseña "{password}"')
def given_the_user_data_for_registration(context, user, identifier, password):
    generate_user(context, user, identifier, password)


@Step('con direccion en rango del hub "{hub}"')
def step_impl(context, hub):
    """This scenario is just decorative, it does not require any action."""
    pass


@When('el usuario "{user}" inicia sesion con sus credenciales')
def when_the_user_logs_in(context, user):
    login(context, user)


@Then('el usuario "{user}" accede a la aplicacion')
def assert_when_the_user_logs_in(context, user):
    assert_login(context)


@Step('se valida si el usuario "{user}" acepto los terminos y condiciones')
def get_and_assert_user_flags(context, user):
    customer_profile_client = CustomerProfileClient(f'{context.HOST}/{context.APP_ENV_VARS["paths"]["private"]}',
                                                    application=context.APPLICATION,
                                                    user_id=context.VALUES["USER_DATA"][user]["session"]["userId"],
                                                    access_token=context.VALUES["USER_DATA"][user]["session"][
                                                        "access_token"],
                                                    app_version=context.APP_VERSION, platform=context.PLATFORM)
    context.flags_response = customer_profile_client.get_flags()

    assert context.flags_response.status_code == 200, ('[ERROR] No se obtuvieron las flags'
                                                       '\n [Expected Status Code]: 200'
                                                       f'\n [Actual Status Code]: {context.flags_response.status_code}')

    if context.APPLICATION == "JKR":
        assert context.flags_response.body["agoraJOKRTermCondition"], (
            '[ERROR] El usuario no acepto los terminos y condiciones'
            '\n [Expected Value]: True'
            f'\n [Actual Value]: {context.flags_response.body["agoraJOKRTermCondition"]}')
    else:
        assert context.flags_response.body["merkaoTermCondition"], (
            '[ERROR] El usuario no acepto los terminos y '
            'condiciones de Merkao'
            '\n [Expected Value]: True'
            f'\n [Actual Value]: {context.flags_response.body["merkaoTermCondition"]}')

    assert context.flags_response.body["expressTermCondition"], (
        '[ERROR] El usuario no acepto los terminos y '
        'condiciones de Express'
        '\n [Expected Value]: True'
        f'\n [Actual Value]: {context.flags_response.body["expressTermCondition"]}')


@Step('se verifica si el usuario "{user}" completo el registro')
def get_user_registration_verification(context, user):
    customer_profile_client = CustomerProfileClient(f'{context.HOST}/{context.APP_ENV_VARS["paths"]["private"]}',
                                                    application=context.APPLICATION,
                                                    user_id=context.VALUES["USER_DATA"][user]["session"]["userId"],
                                                    access_token=context.VALUES["USER_DATA"][user]["session"][
                                                        "access_token"],
                                                    app_version=context.APP_VERSION, platform=context.PLATFORM)
    context.registration_verification_response = customer_profile_client.get_registration_verification()

    assert context.registration_verification_response.status_code == 200, (
        '[ERROR] No se obtuvo la verificacion de registro'
        '\n [Expected Status Code]: 200'
        f'\n [Actual Status Code]: {context.registration_verification_response.status_code}')


@Step('se obtiene el perfil del usuario "{user}"')
def get_user_profile(context, user):
    customer_profile_client = CustomerProfileClient(f'{context.HOST}/{context.APP_ENV_VARS["paths"]["private"]}',
                                                    application=context.APPLICATION,
                                                    user_id=context.VALUES["USER_DATA"][user]["session"]["userId"],
                                                    access_token=context.VALUES["USER_DATA"][user]["session"][
                                                        "access_token"],
                                                    app_version=context.APP_VERSION, platform=context.PLATFORM)
    context.user_profile_response = customer_profile_client.get_user_profile()

    assert context.registration_verification_response.status_code == 200, (
        '[ERROR] No se obtuvo la verificacion de registro'
        '\n [Expected Status Code]: 200'
        f'\n [Actual Status Code]: {context.registration_verification_response.status_code}')


@Step('se obtienen las direcciones del usuario "{user}"')
def step_impl(context, user):
    get_addresses(context, user)
    assert_get_addresses(context)


@Step('se obtiene la informacion del hub "{hub}" para el usuario "{user}"')
def step_impl(context, hub, user):
    qry_catalog_client = QryCatalogClient(f'{context.HOST}/{context.APP_ENV_VARS["paths"]["private"]}',
                                          application=context.APPLICATION,
                                          access_token=context.VALUES["USER_DATA"][user]["session"]["access_token"],
                                          user_id=context.VALUES["USER_DATA"][user]["session"]["userId"],
                                          app_version=context.APP_VERSION, platform=context.PLATFORM)
    context.store_subsidiary_information_response = qry_catalog_client.get_store_subsidiary_by_location(
        context.APP_ENV_VARS["addresses"][hub]["latitude"],
        context.APP_ENV_VARS["addresses"][hub]["longitude"])

    assert context.store_subsidiary_information_response.status_code == 200, (
        '[ERROR] No se obtuvo la ubicacion del hub'
        '\n [Expected Status Code]: 200'
        f'\n [Actual Status Code]: {context.store_subsidiary_information_response.status_code}')

    assert (context.store_subsidiary_information_response.body[0]["storeSubsidiaryId"] ==
            context.APP_ENV_VARS["STORE"]["HUBS"][hub]["SUBSIDIARY_ID"]), (
        '[ERROR] El id del hub no es el esperado'
        f'\n [Expected Value]: {context.APP_ENV_VARS["STORE"]["HUBS"][hub]["SUBSIDIARY_ID"]}'
        f'\n [Actual Value]: {context.store_subsidiary_information_response.body[0]["storeSubsidiaryId"]}')

    assert context.store_subsidiary_information_response.body[0]["name"] == context.APP_ENV_VARS["STORE"]["NAME"], (
        '[ERROR] El nombre de la tienda no es el esperado'
        f'\n [Expected Value]: {context.APP_ENV_VARS["STORE"]["NAME"]}'
        f'\n [Actual Value]: {context.store_subsidiary_information_response.body[0]["name"]}'

    )


@Step('se obtienen los segmentos del usuario "{user}"')
def step_impl(context, user):
    path = context.PATHS["private"]
    if context.APPLICATION == "MRK":
        path += f'/{context.PATHS["campaign-hub"]}'
    else:
        path += '/campaign-hub'

    campaign_hub_client = CampaignHubClient(
        f'{context.HOST}/{path}',
        application=context.APPLICATION,
        access_token=context.VALUES["USER_DATA"][user]["session"]["access_token"],
        app_version=context.APP_VERSION, platform=context.PLATFORM)
    context.segments_response = campaign_hub_client.get_segments()

    assert context.segments_response.status_code == 200, (
        f'[ERROR] No se obtuvieron los segmentos del usuario con id: '
        f'{context.VALUES["USER_DATA"][user]["session"]["userId"]}'
        '\n [Expected Status Code]: 200'
        f'\n [Actual Status Code]: {context.segments_response.status_code}')

    assert context.segments_response.body[0] is not None, '[ERROR] Los segmentos son nulos'
    context.app_user.segments = context.segments_response.body


@Step('se obtiene el carrito de compras del usuario "{user}"')
def step_impl(context, user):
    get_cart(context, user)
    assert_get_cart(context)


@Step('se obtienen las campañas del home para el usuario "{user}" en el hub "{hub}"')
def step_impl(context, user, hub):
    get_campaigns_by_hub(context, user, hub)
    assert_get_campaigns_by_hub(context, hub, user)


@Step('se obtienen las categorias de la tienda para el usuario "{user}"')
def step_impl(context, user):
    get_categories_by_store(context, user)
    assert_get_categories_by_store(context)


@Then('el usuario "{user}" accede al home de la aplicacion')
def home_access(context, user):
    """This scenario is just decorative, it does not require any action."""
    pass


@When('el usuario "{user}" inicia sesion con sus credenciales 3 veces y contraseña incorrecta')
def block_account_due_to_invalid_credentials(context, user):
    generate_user(context, user, context.app_user.identifier, "144444")
    for _ in range(2):
        login(context, user)
        assert_wrong_login(context)
    login(context, "usuario_app")


@Then('el sistema bloquea la cuenta del usuario "usuario_app" por 24 horas')
def assert_block_account_due_to_invalid_credentials(context):
    assert context.login_response.status_code == 422, (
        '[ERROR] el status code recibido no es el esperado.'
        f'\n [Expected Status Code]: 422\n'
        f'\n [Received Code]: {context.login_response.status_code}'
    )
    err_code = 'USE_LOG_02'
    err_title = 'Superaste el límite de intentos'
    err_message = ('Por seguridad, tu cuenta permanecerá bloqueada durante 24 horas. '
                   'Para volver a ingresar puedes recuperar tu clave.')

    assert context.login_response.body['code'] == err_code, (
        '[ERROR] el codigo recibido no es el esperado.'
        f'\n [Expected Code]: {err_code}'
        f'\n [Received Code]: {context.login_response.body["code"]}')

    assert context.login_response.body['title'] == err_title, (
        '[ERROR] el titulo recibido no es el esperado.'
        f'\n [Expected Message]: {err_title}'
        f'\n [Received Message]: {context.login_response.body["title"]}')

    assert context.login_response.body['detail']['text'] == err_message, (
        '[ERROR] el mensaje recibido no es el esperado.'
        f'\n [Expected Message]: {err_message}'
        f'\n [Received Message]: {context.login_response.body["message"]}')
