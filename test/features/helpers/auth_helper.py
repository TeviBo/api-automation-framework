from src.lib.api.library_api import OTPLib
from src.lib.api.oauth_api import OAuth


def get_oauth_token(context) -> None:
    oauth_api = OAuth(context.HOST, application=context.APPLICATION,
                      token=context.APP_ENV_VARS["oauth_credentials"]["register"])
    context.get_oauth_access_token_otp_response = oauth_api.get_access_token()


def assert_get_oauth_token(context):
    assert context.get_oauth_access_token_otp_response.status_code == 200, (
        '[ERROR] No se pudo obtener el token de acceso.'
        '\n[Expected Status Code]: 200'
        f'\n[Response Status Code]: {gcontext.et_oauth_access_token_otp_response.status_code}'
        f'\n[Error Message]: {context.get_oauth_access_token_otp_response.body["Error"]}'
    )
    context.app_user.session = {**context.VALUES["USER_DATA"][user]["session"],
                                "access_token": context.get_oauth_access_token_otp_response.body["access_token"]}
    context.VALUES["USER_DATA"].update(context.app_user.get_user())


def get_otp_code(context, user):
    otp_client = OTPLib(context.HOST, application=context.APPLICATION,
                        token=context.VALUES["USER_DATA"][user]["session"]["access_token"])
    context.get_otp_code_response = otp_client.get_otp_code(context.VALUES["USER_DATA"][user]["identifier"])


def assert_get_otp_code(context):
    err_msg = context.get_otp_code_response.body["title"] if context.get_otp_code_response.status_code == 422 else None
    err_code = context.get_otp_code_response.body["code"] if context.get_otp_code_response.status_code == 422 else None
    assert context.get_otp_code_response.status_code == 200, ('[ERROR] No se pudo obtener el codigo de activacion.'
                                                              f'\n[Expected Status Code]: 200'
                                                              f'\n[Response Status Code]: {context.get_otp_code_response.status_code}'
                                                              f'\n[Error Code]: {err_code}'
                                                              f'\n[Error Message]: {err_msg}\n')
    assert context.get_otp_code_response.body["code"] is not None, '[ERROR] El codigo de activacion es nulo.'
    assert context.get_otp_code_response.body["code"] != "", '[ERROR] El codigo de activacion es vacio.'
    context.otp_code = context.get_otp_code_response.body["code"]
