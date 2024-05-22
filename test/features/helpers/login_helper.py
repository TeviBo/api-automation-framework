from src.lib.api.identity_api import IdentityClient


def generate_user(context, user, identifier, password):
    if identifier.lower() == "random_phone":
        identifier = context.DATA_MANAGER.generate_random_phone()
    if context.VALUES["USER_DATA"].get("identifier") is None:
        context.app_user.user_type = user
        context.app_user.identifier = identifier
        context.app_user.password = password
        context.VALUES["USER_DATA"].update(context.app_user.get_user())
    login_client = IdentityClient(f'{context.HOST}/{context.BASE_ENV_VARS["paths"]["identity"]}',
                                  application=context.APPLICATION, app_version=context.APP_VERSION,
                                  platform=context.PLATFORM)
    keyboard_response = login_client.get_keyboard()
    assert keyboard_response.status_code == 200, ('[ERROR] No se obtuvo el teclado'
                                                  '\n [Expected Status Code]: 200'
                                                  f'\n [Actual Status Code]: {keyboard_response.status_code}')
    context.PASSWORD_POSITIONS = context.UTILS.get_keyboard_positions(keyboard_response.body["keyboard"], password)
    context.app_user.password = context.PASSWORD_POSITIONS


def login(context, user):
    login_client = IdentityClient(f'{context.HOST}/{context.APP_ENV_VARS["paths"]["identity"]}',
                                  application=context.APPLICATION, app_version=context.APP_VERSION,
                                  platform=context.PLATFORM)
    context.login_response = login_client.login(context.VALUES["USER_DATA"][user]["identifier"],
                                                context.PASSWORD_POSITIONS,
                                                context.APP_ENV_VARS["register_tokens"]["engagementId"],
                                                context.APP_ENV_VARS["register_tokens"]["token"])


def assert_login(context):
    assert context.login_response.status_code == 201, (
        '[ERROR] No se pudo loguear el usuario'
        '\n [Expected Status Code]: 201'
        f'\n [Actual Status Code]: {context.login_response.status_code}'
    )
    assert context.login_response.body['access_token'] is not None, '[ERROR] El access token es nulo'
    assert context.login_response.body["access_token"] != "", '[ERROR] El access token es vacio'

    assert context.login_response.body['userId'] is not None, '[ERROR] El "userId" es nulo'
    assert context.login_response.body["userId"] != "", '[ERROR] El "userId" es vacio'

    assert context.login_response.body['operationToken'] is not None, '[ERROR] El "operationToken" es nulo'

    assert context.login_response.body['firebaseToken'] is not None, '[ERROR] El "firebaseToken" es nulo'
    assert context.login_response.body["firebaseToken"] != "", '[ERROR] El "firebaseToken" es vacio'

    context.app_user.session = context.login_response.body
    context.VALUES["USER_DATA"].update(context.app_user.get_user())
