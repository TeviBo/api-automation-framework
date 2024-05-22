from behave import *  # NOSONAR

from features.helpers.cards_helper import get_user_cards, assert_get_user_cards


@When('el usuario "{user}" desea ver el listado de tarjetas agregadas')
def when_the_user_requests_the_payment_methods_list(context, user):
    get_user_cards(context, user)


@Then('se retorna el listado de tarjetas para el usuario "{user}"')
def assert_when_the_user_requests_the_payment_methods_list(context, user):
    assert_get_user_cards(context)
