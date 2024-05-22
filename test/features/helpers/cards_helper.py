from src.lib.api.account_api import AccountClient


def get_user_cards(context, user):
    cards_api = AccountClient(f'{context.HOST}/{context.PATHS["private"]}', application=context.APPLICATION,
                              access_token=context.VALUES["USER_DATA"][user]["session"]["access_token"],
                              user_id=context.VALUES["USER_DATA"][user]["session"]["userId"], platform=context.PLATFORM)
    context.cards_response = cards_api.get_cards()


def assert_get_user_cards(context):
    assert context.cards_response.status_code == 200, (
        '[ERROR] No se pudo obtener el listado de tarjetas.'
        '\n [Expected Status Code]: 200'
        f'\n [Response Status Code]: {context.cards_response.status_code}'
    )

    context.app_user.cards = context.cards_response.body
    context.VALUES["USER_DATA"].update(context.app_user.get_user())
