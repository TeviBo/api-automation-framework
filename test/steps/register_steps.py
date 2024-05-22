from time import sleep

from behave import *  # NOSONAR
from features.helpers.auth_helper import get_otp_code, assert_get_otp_code
from features.helpers.login_helper import login, generate_user, assert_login

from src.lib.api.customer_register_api import CustomerRegisterClient
from src.lib.api.identity_api import IdentityClient
from src.lib.api.oauth_api import OAuth
from src.utils.logger import logger


@Given('un nuevo usuario "{user}"')
def create_random_user(context, user):
    context.app_user.user_type = user
    context.app_user.first_name = context.DATA_MANAGER.generate_random_name()
    context.app_user.last_name = context.DATA_MANAGER.generate_random_last_name()
    context.app_user.document = context.DATA_MANAGER.generate_random_dni()
    context.app_user.identifier = context.DATA_MANAGER.generate_random_phone()
    context.app_user.email = context.DATA_MANAGER.generate_random_email()
    context.app_user.password = "122222"
    context.VALUES["USER_DATA"].update(context.app_user.get_user())


@Given('el usuario "{user}" registrado con identificador "{identifier}"')
def create_random_user_with_identifier(context, user, identifier):
    context.app_user.user_type = user
    context.app_user.identifier = identifier
    context.app_user.email = context.DATA_MANAGER.generate_random_email()
    context.VALUES["USER_DATA"].update(context.app_user.get_user())


@When('el usuario "{user}" registra un telefono valido')
def register_user_phone(context, user):
    customer_register_client = CustomerRegisterClient(f'{context.HOST}/{context.BASE_ENV_VARS["paths"]["public"]}',
                                                      application=context.APPLICATION, platform=context.PLATFORM)
    engagement_id = context.APP_ENV_VARS['register_tokens']['engagementId']
    token = context.APP_ENV_VARS['register_tokens']['token']
    context.register_response = customer_register_client.generate_code(context.VALUES["USER_DATA"][user]["identifier"],
                                                                       context.VALUES["USER_DATA"][user]["email"],
                                                                       engagement_id,
                                                                       token)


@Then('el telefono del usuario "{user}" es registrado exitosamente')
def assert_register_user_phone(context, user):
    err_message = context.register_response.body["title"] if context.register_response.status_code == 422 else None
    assert context.register_response.status_code == 201, (
        '[ERROR] No se pudo registrar el usuario.'
        f'\n[Expected Status Code]: 201'
        f'\n[Response Status Code]: {context.register_response.status_code}'
        f'\n[Error Message]: {err_message}\n'
    )
    assert context.register_response.body["operationToken"] is not None, '[ERROR] El "operationToken" es nulo.'
    assert context.register_response.body["operationToken"] != "", '[ERROR] El "operationToken" es vacio.'
    context.app_user.session = {"operation_token": context.register_response.body["operationToken"]}
    context.VALUES["USER_DATA"].update(context.app_user.get_user())


@Step('se genera un codigo otp para el usuario "{user}" que recibira por mensaje para la activacion de su cuenta')
def get_access_token_for_otp_code(context, user) -> None:
    oauth_api = OAuth(context.HOST, application=context.APPLICATION,
                      token=context.APP_ENV_VARS["oauth_credentials"]["register"], platform=context.PLATFORM)
    get_oauth_access_token_otp_response = oauth_api.get_access_token()
    assert get_oauth_access_token_otp_response.status_code == 200, (
        '[ERROR] No se pudo obtener el token de acceso.'
        '\n[Expected Status Code]: 200'
        f'\n[Response Status Code]: {get_oauth_access_token_otp_response.status_code}'
        f'\n[Error Message]: {get_oauth_access_token_otp_response.body["Error"]}'
    )
    context.app_user.session = {**context.VALUES["USER_DATA"][user]["session"],
                                "access_token": get_oauth_access_token_otp_response.body["access_token"]}
    context.VALUES["USER_DATA"].update(context.app_user.get_user())
    get_otp_code(context, user)
    assert_get_otp_code(context)


@When('el usuario "{user}" ingresa el codigo otp recibido')
def validate_otp_code(context, user):
    customer_register_client = CustomerRegisterClient(f'{context.HOST}/{context.BASE_ENV_VARS["paths"]["public"]}',
                                                      application=context.APPLICATION,
                                                      token=context.VALUES["USER_DATA"][user]["session"][
                                                          "operation_token"], platform=context.PLATFORM,
                                                      app_version=context.APP_VERSION)
    context.validate_otp_response = customer_register_client.validate_code(context.otp_code)


@Step('el codigo otp del usuario "{user}" es validado')
def assert_validate_otp_code(context, user):
    err_msg = context.validate_otp_response.body[
        "message"] if context.validate_otp_response.status_code == 500 else None
    assert context.validate_otp_response.status_code == 201, (
        '[ERROR] No se pudo validar el codigo OTP.'
        f'\n[Expected Status Code]: 201'
        f'\n[Response Status Code]: {context.validate_otp_response.status_code}'
        f'\n[OTP CODE]: {context.otp_code}'
        f'\n[Error Message]: {err_msg}'
    )
    context.app_user.session = {**context.VALUES["USER_DATA"][user]["session"],
                                "operation_token": context.validate_otp_response.body["operationToken"]}
    del context.otp_code


@When('el usuario "{user}" ingresa una contraseña de 6 digitos para su cuenta')
def register_user_password(context, user):
    keyboard_response = IdentityClient(f'{context.HOST}/{context.BASE_ENV_VARS["paths"]["identity"]}',
                                       application=context.APPLICATION, app_version=context.APP_VERSION,
                                       platform=context.PLATFORM).get_keyboard()
    assert keyboard_response.status_code == 200, '[ERROR] No se pudo obtener el teclado.'
    keyboard = keyboard_response.body['keyboard']
    customer_register_client = CustomerRegisterClient(
        f'{context.HOST}/{context.BASE_ENV_VARS["paths"]["public"]}',
        application=context.APPLICATION,
        token=context.VALUES["USER_DATA"][user]["session"]["operation_token"],
        app_version=context.APP_VERSION, platform=context.PLATFORM)
    context.register_user_password_response = customer_register_client.register_user_password(
        context.app_user.get_password_positions(keyboard))


@Then('la contraseña para el usuario "{user}" es registrada exitosamente')
def assert_register_user_password(context, user):
    err_msg = context.register_user_password_response.body[
        "message"] if context.register_user_password_response.status_code == 500 else None

    assert context.register_user_password_response.status_code == 204, (
        '[ERROR] No se pudo crear la cuenta.'
        '\n[Expected Status Code]: 204'
        f'\n[Response Status Code]: {context.register_user_password_response.status_code}'
        f'\n[Error Message]: {err_msg}'
    )
    generate_user(context, user, context.VALUES["USER_DATA"][user]["identifier"],
                  context.VALUES["USER_DATA"][user]["password"])
    login(context, user)
    assert_login(context)


@When('el usuario "{user}" completa sus datos personales')
def complete_personal_data(context, user):
    customer_register_client = CustomerRegisterClient(f'{context.HOST}/{context.PATHS["private"]}',
                                                      application=context.APPLICATION,
                                                      access_token=context.VALUES["USER_DATA"][user]["session"][
                                                          "access_token"],
                                                      user_id=context.VALUES["USER_DATA"][user]["session"]["userId"],
                                                      app_version=context.APP_VERSION,
                                                      platform=context.PLATFORM)
    context.register_data_response = customer_register_client.register_data(
        context.VALUES["USER_DATA"][user]["first_name"],
        context.VALUES["USER_DATA"][user]["last_name"],
        context.VALUES["USER_DATA"][user]["document"])


@Then('el sistema registra los datos del usuario "{user}" exitosamente')
def assert_personal_data_response(context, user):
    assert context.register_data_response.status_code == 200, (
        '[ERROR] No se pudo completar los datos personales.'
        '\n[Expected Status Code]: 200'
        f'\n[Response Status Code]: {context.register_data_response.status_code}')
    context.app_user.contact_key = context.register_data_response.body["contactKey"]
    context.VALUES["USER_DATA"].update(context.app_user.get_user())
    logger.info(f'New user created successfully. Phone: {context.VALUES["USER_DATA"][user]["identifier"]}. '
                f'Password: "122222".')


# // EXCEPTIONS //


@Step('el usuario "{user}" registra un telefono que no tiene 9 caracteres de extension')
def invalid_phone_register(context, user):
    customer_register_client = CustomerRegisterClient(f'{context.HOST}/{context.BASE_ENV_VARS["paths"]["public"]}',
                                                      application=context.APPLICATION, platform=context.PLATFORM)

    context.invalid_phone_register_response = customer_register_client.generate_code(
        context.DATA_MANAGER.generate_random_phone(valid=True, len_valid=False),
        context.VALUES["USER_DATA"][user]["email"],
        context.APP_ENV_VARS['register_tokens']['engagementId'], context.APP_ENV_VARS['register_tokens']['token'])


@Then('el sistema devuelve un mensaje indicando que el telefono debe tener 9 caracteres de extension')
def assert_invalid_phone_register(context):
    assert context.invalid_phone_register_response.status_code == 400, (
        '[ERROR] el telefono invalido ingresado fue registrado.'
        f'\n[Expected Status Code]: 400'
        f'\n[Response Status Code]: {context.invalid_phone_register_response.status_code}')
    expected_err_code = "GEN_ALL_01"
    expected_message_len_error = "length must be between 9 and 9"
    assert context.invalid_phone_register_response.body["code"] == expected_err_code, (
        '[ERROR] El codigo de error no es el esperado.'
        f'\n[Expected Error Code]: {expected_err_code}'
        f'\n[Received Error Code]: {context.invalid_phone_register_response.body["code"]}'
    )
    received_error_messages = [err["message"] for err in context.invalid_phone_register_response.body["errors"]]
    assert expected_message_len_error in received_error_messages, ('[ERROR] El mensaje de error no es el esperado.'
                                                                   f'\n[Expected Message]: {expected_message_len_error}'
                                                                   f'\n[Received Messages]: {received_error_messages}')


@When('el usuario "{user}" registra un telefono que no comienza con 9')
def register_peru_phone_not_starting_with_9(context, user):
    customer_register_client = CustomerRegisterClient(f'{context.HOST}/{context.BASE_ENV_VARS["paths"]["public"]}',
                                                      application=context.APPLICATION, platform=context.PLATFORM)

    context.invalid_phone_register_response = customer_register_client.generate_code(
        context.DATA_MANAGER.generate_random_phone(valid=False, len_valid=True),
        context.VALUES["USER_DATA"][user]["email"],
        context.APP_ENV_VARS['register_tokens']['engagementId'], context.APP_ENV_VARS['register_tokens']['token'])


@Then('el sistema devuelve un mensaje indicando que el telefono debe comenzar con 9')
def step_impl(context):
    assert context.invalid_phone_register_response.status_code == 400, (
        '[ERROR] el telefono invalido ingresado fue registrado.'
        f'\n[Expected Status Code]: 400'
        f'\n[Response Status Code]: {context.invalid_phone_register_response.status_code}')
    expected_err_code = "GEN_ALL_01"
    expecter_err_message = 'length must be between 9 and 9'
    assert context.invalid_phone_register_response.body["code"] == expected_err_code, (
        '[ERROR] El codigo de error no es el esperado.'
        f'\n[Expected Error Code]: {expected_err_code}'
        f'\n[Received Error Code]: {context.invalid_phone_register_response.body["code"]}')

    received_error_messages = [err["message"] for err in context.invalid_phone_register_response.body["errors"]]
    assert expecter_err_message in received_error_messages, (
        '[ERROR] El mensaje de error no es el esperado.'
        f'\n[Expected Error Message]: {expecter_err_message}'
        f'\n[Received Error Message]: {received_error_messages}')


@When('el usuario "{user}" ingresa un codigo invalido')
def invalid_otp_code(context, user):
    customer_register_client = CustomerRegisterClient(
        f'{context.HOST}/{context.BASE_ENV_VARS["paths"]["public"]}',
        application=context.APPLICATION,
        token=context.VALUES["USER_DATA"][user]["session"]["operation_token"],
        app_version=context.APP_VERSION, platform=context.PLATFORM)
    context.response = customer_register_client.validate_code("1234")


@Then('el sistema devuelve un mensaje indicando que el codigo es invalido')
def assert_invalid_otp_code(context):
    assert context.response.status_code == 422, '[ERROR] El codigo OTP fue aceptado por el sistema.' \
                                                f'\n[Expected Status Code]: 422' \
                                                f'\n[Response Status Code]: {context.response.status_code}'


@When('el usuario "{user}" ingresa una contraseña insegura')
def register_insecure_password(context, user):
    context.VALUES["USER_DATA"][user]["password"] = "123456"
    register_user_password(context, user)


@Then('la contraseña para el usuario "{user}" no es registrada debido a que no cumple con los requisitos de seguridad')
def assert_register_insecure_password(context, user):
    assert context.register_user_password_response.status_code == 422, (
        '[ERROR] El sistema registro el usuario correctamente.'
        f'\n[Expected Status Code]: 422'
        f'\n[Response Status Code]: {context.register_user_password_response.status_code}')
    expected_error_code = "CUS_REG_13"
    expected_error_title = "Clave Insegura"
    assert context.register_user_password_response.body["code"] == expected_error_code, (
        '[ERROR] El codigo de error no es el esperado.'
        f'\n[Expected Error Code]: {expected_error_code}'
        f'\n[Received Error Code]: {context.register_user_password_response.body["code"]}'
    )
    assert context.register_user_password_response.body["title"] == expected_error_title, (
        '[ERROR] El titulo de error no es el esperado.'
        f'\n[Expected Error Title]: {expected_error_title}'
        f'\n[Received Error Title]: {context.register_user_password_response.body["title"]}'
    )
    context.app_user.password = "122222"
    context.VALUES["USER_DATA"].update(context.app_user.get_user())


@When('el usuario "{user}" ingresa un numero de documento invalido')
def complete_data_invalid_document(context, user):
    context.VALUES["USER_DATA"][user]["document"] = context.DATA_MANAGER.generate_random_dni(7)
    complete_personal_data(context, user)


@Then('el sistema devuelve un mensaje de error para el usuario "{user}" indicando que el documento es invalido')
def assert_complete_data_invalid_document(context, user):
    assert context.register_data_response.status_code == 400, (
        '[ERROR] El sistema registro el usuario correctamente.'
        '\n[Expected Status Code]: 400'
        f'\n[Response Status Code]: {context.register_data_response.status_code}')
    expected_error_code = "GEN_ALL_01"
    expected_error_message = "Invalid document number"
    assert context.register_data_response.body["code"] == expected_error_code, (
        '[ERROR] El codigo de error no es el esperado'
        f'\n[Expected Error Code]: {expected_error_code}'
        f'\n[Received Error Code]: {context.register_data_response.body["code"]}')
    assert expected_error_message in context.register_data_response.body["errors"][0]["message"], (
        '[ERROR] El mensaje de error no es el esperado.'
        f'\n[Expected Error Message]: {expected_error_message}'
        f'\n[Received Error Message]: {context.register_data_response.body["errors"][0]["message"]}')
    context.app_user.document = context.DATA_MANAGER.generate_random_dni()
    context.VALUES["USER_DATA"].update(context.app_user.get_user())


@When('el usuario "{user}" ingresa el codigo otp vencido')
def get_otp_code_expired(context, user):
    logger.info("Waiting 1 minute until OTP code expires...")
    sleep(61)
    validate_otp_code(context, user)


@Then('el sistema devuelve un mensaje de error indicando que el otp se ha vencido')
def assert_expired_otp_code(context):
    assert context.validate_otp_response.status_code == 422, (
        '[ERROR] El otp no esta expirado.'
        f'\n[Expected Status Code]: 422'
        f'\n[Response Status Code]: {context.validate_otp_response.status_code}'
        f'\n[OTP]: {context.otp_code}')

    assert context.validate_otp_response.body["code"] == "CUS_REG_02", (
        '[ERROR] El codigo de error no es el esperado.'
        f'\n[Expected Error Code]: CUS_REG_03'
        f'\n[Received Error Code]: {context.validate_otp_response.body["code"]}')

    assert context.validate_otp_response.body["title"] == 'Tuvimos un problema con tu código', (
        '[ERROR] El titulo de error no es el esperado.'
        f'\n[Expected Error Title]: Tuvimos un problema con tu código'
        f'\n[Received Error Title]: {context.validate_otp_response.body["title"]}')

    expected_err_msg = 'Solicita nuevamente un código para validar tu celular.'
    assert context.validate_otp_response.body["detail"]["text"] == expected_err_msg, (
        '[ERROR] El mensaje de error no es el esperado.'
        f'\n[Expected Error Message]: {expected_err_msg}'
        f'\n[Received Error Message]: {context.validate_otp_response.body["detail"]["text"]}')
    del context.otp_code


@When('el usuario "{user}" registra un telefono que ya posee cuenta')
def register_phone_already_registered(context, user):
    register_user_phone(context, user)


@Then('el sistema devuelve un mensaje de error para el usuario "{user}" indicando que el telefono esta registrado')
def assert_register_phone_already_registered(context, user):
    assert context.validate_otp_response.status_code == 422, (
        '[ERROR] El sistema registro el usuario correctamente.'
        '\n[Expected Status Code]: 422'
        f'\n[Response Status Code]: {context.validate_otp_response.status_code}'
        f'\n[PHONE]: {context.VALUES["USER_DATA"][user]["identifier"]}')

    assert context.validate_otp_response.body["code"] == "CUS_REG_01", (
        '[ERROR] El codigo de error no es el esperado.'
        f'\n[Expected Error Code]: CUS_REG_01'
        f'\n[Received Error Code]: {context.register_response.body["code"]}')

    assert context.validate_otp_response.body["title"] == "El número de celular ya se encuentra registrado", (
        '[ERROR] El titulo de error no es el esperado.'
        f'\n[Expected Error Title]: El número de celular ya se encuentra registrado'
        f'\n[Received Error Title]: {context.register_response.body["title"]}'
    )

    expected_error_message = ("Como el número se encuentra en nuestra base de datos, "
                              "puedes iniciar sesión o contactar con nosotros para ayudarte.")
    assert context.validate_otp_response.body["detail"]["text"] == expected_error_message, (
        '[ERROR] El mensaje de error no es el esperado.'
        f'\n[Expected Error Message]: {expected_error_message}'
        f'\n[Received Error Message]: {context.register_response.body["detail"]["text"]}'
    )
