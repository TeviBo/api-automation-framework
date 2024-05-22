from src.lib.api.campaign_hub_api import CampaignHubClient


def get_campaigns_by_hub(context, user, hub):
    path = context.PATHS["private"]
    if context.APPLICATION == "MRK":
        path += f'/{context.PATHS["campaign-hub"]}'
    else:
        path += '/campaign-hub'

    campaign_hub_client = CampaignHubClient(f'{context.HOST}/{path}', application=context.APPLICATION,
                                            access_token=context.VALUES["USER_DATA"][user]["session"]["access_token"],
                                            app_version=context.APP_VERSION, platform=context.PLATFORM)
    context.get_campaigns_by_hub_response = campaign_hub_client.get_campaign_layout(
        context.APP_ENV_VARS["STORE"]["STORE_ID"],
        context.APP_ENV_VARS["STORE"]["HUBS"][hub]["SUBSIDIARY_ID"])


def assert_get_campaigns_by_hub(context, hub, user):
    assert context.get_campaigns_by_hub_response.status_code == 200, (
        f'[ERROR] No se pudo obtener las campañas para el hub {hub}'
        '\n [Expected Status Code]: 200'
        f'\n [Received Status Code]: {context.get_campaigns_by_hub_response.status_code}')
    assert context.get_campaigns_by_hub_response is not None, (
        f'[ERROR] No se encontraron campañas para el hub {hub}'
        f'\n [Received Campaigns]: {context.store_user.campaigns_by_hub}')
    context.store_user.campaigns_by_hub = context.get_campaigns_by_hub_response.body
