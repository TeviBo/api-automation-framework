from behave import *  # NOSONAR

from src.lib.api.library_api import BackofficeLib
from src.lib.api.oauth_api import OAuth
from src.utils.logger import logger


# // *** Backoffice login steps *** //
@Given('el usuario de tienda "{store_user}"')
def set_store_user(context, store_user):
    context.store_user.user_type = store_user
    context.store_user.email = context.APP_ENV_VARS["STORE"]["USERNAME"]
    context.VALUES["USER_DATA"].update(context.store_user.get_user())


@When('el usuario de tienda "{store_user}" inicia sesion con sus credenciales')
def login_backoffice_shop(context, store_user):
    library_client = BackofficeLib(context.HOST)
    context.login_bo_response = library_client.login(context.VALUES["USER_DATA"][store_user]["email"])
    while context.login_bo_response.status_code == 422 and context.login_bo_response.body["code"] == 'USE_LOG_03':
        logger.info("User was blocked. Retrying with another user")
        for user in context.APP_ENV_VARS["STORE"]["users"]:
            context.login_bo_response = library_client.login(user)
            break


@Then('el usuario de tienda "{store_user}" inicia sesion exitosamente')
def assert_login_backoffice_shop(context, store_user):
    assert context.login_bo_response.status_code == 201, (
        '[ERROR] No se pudo iniciar sesión en el backoffice'
        '\n [Expected Status Code]: 201'
        f'\n [Received Status Code]: {context.login_bo_response.status_code}'
        f'\n [Response]: {context.login_bo_response.body}')
    login_data = {
        "access_token": context.login_bo_response.body["access_token"],
        "client_id": context.login_bo_response.body["client_id"],
        "firebase_token": context.login_bo_response.body["firebase_token"],
        "identity_token": context.login_bo_response.body["identity_token"],
        "user": context.login_bo_response.body["user"],
        "token": context.login_bo_response.body["token"]
    }

    assert login_data['access_token'] is not None, '[ERROR] El access token es nulo'
    assert login_data['access_token'] != "", '[ERROR] El access token es vacio'
    context.store_user.session = login_data
    context.store_user.store.store_id = context.login_bo_response.body["user"]["storeId"]
    context.store_user.store.store_name = context.login_bo_response.body["user"]["storeName"]
    context.VALUES["USER_DATA"].update(context.store_user.get_user())


@When('el usuario de tienda "{store_user}" ingresa al listado de hubs')
def get_hubs(context, store_user):
    library_client = BackofficeLib(f'{context.HOST}/{context.BASE_ENV_VARS["paths"]["shop"]["backoffice"]}',
                                   token=context.store_user.session["token"],
                                   access_token=context.store_user.session["access_token"],
                                   client_id=context.store_user.session["client_id"],
                                   firebase_token=context.store_user.session["firebase_token"],
                                   identity_token=context.store_user.session["identity_token"])
    context.get_hubs_response = library_client.get_hubs(
        context.VALUES["USER_DATA"][store_user]["session"]["user"]["storeId"])


@Then('el usuario de tienda "{store_user}" visualiza el listado de hubs')
def assert_get_hubs(context, store_user):
    assert context.get_hubs_response.status_code == 200, (
        '[ERROR] No se pudo obtener los hubs'
        '\n [Expected Status Code]: 200'
        f'\n [Received Status Code]: {context.get_hubs_response.status_code}')
    assert context.get_hubs_response.body['result'] is not None, '[ERROR] El resultado de los hubs es nulo'
    assert len(context.get_hubs_response.body['result']) > 0, '[ERROR] El resultado de los hubs es vacio'
    context.store_user.store.hubs = context.get_hubs_response.body['result']
    context.VALUES["USER_DATA"].update(context.store_user.get_user())


@Step('el usuario de tienda "{store_user}" selecciona el hub "{selected_hub}"')
def select_hub(context, store_user, selected_hub):
    context.store_user.get_hub(selected_hub)
    context.VALUES["USER_DATA"].update(context.store_user.get_user())


@Then('el hub "{hub}" es seleccionado por el usuario de tienda "{user}"')
def assert_selected_hub(context, hub, user):
    assert context.store_user.selected_hub != {}, '[ERROR] No se selecciono ningun hub'


@When('el usuario de pmm "{user}" inicia sesion con sus credenciales')
def get_oauth2_token_pmm(context, user):
    oauth_client = OAuth(context.HOST, token=context.APP_ENV_VARS["oauth_credentials"]["pmm"])
    context.oauth_response = oauth_client.get_access_token()


@Then('el usuario de pmm "{user}" inicia sesion exitosamente')
def assert_get_oauth2_token_pmm(context, user):
    assert context.oauth_response.status_code == 200, (
        '[ERROR] No se pudo obtener el token OAuth'
        '\n [Expected Status Code]: 200'
        f'\n [Received Status Code]: {context.oauth_response.status_code}')
    context.VALUES["USER_DATA"][user]["session"]["access_token"] = context.oauth_response.body["access_token"]
