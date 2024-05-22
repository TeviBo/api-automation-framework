import json
import os

from behave import fixture, use_fixture

from src.lib.infra.models.app.app_user_model import AppUserModel
from src.lib.infra.models.store.store_user_model import StoreUserModel
from src.utils import utils, data_manager
from src.utils.log_verifier.log_verifier_factory.verifiers.base_verifier import LogVerifier
from src.utils.logger import GoogleCloudLoggingClient, logger

BASE_DIR = utils.go_up_n_dirs(os.path.abspath(__file__), 2)
ENV_DIR = os.path.join(BASE_DIR, 'src', 'data', 'environments')


@fixture
def behave_fixture(context):
    logger.info("Setting up Behave fixture")
    logger.info('Loading Environment and Tests Data')
    context.VALUES = {"USER_DATA": {}}
    context.UTILS = utils

    # Critical Test Variables Debugging control
    logger.debug(f'ENVIRONMENT: {os.getenv("ENV").upper()}')
    logger.debug(f'APPLICATION: {context.config.userdata.get("application").upper()}')
    logger.debug(f'PLATFORM: {context.config.userdata.get("platform").upper()}')
    logger.debug(f'TAGS TO RUN: {context.config.tags}')
    logger.debug(f'LOG_LEVEL: {os.getenv("LOG_LEVEL").upper()}')

    context.ACTUAL_ENVIRONMENT = os.getenv("ENV")
    context.APPLICATION = context.config.userdata.get("application").upper()
    context.PLATFORM = context.config.userdata.get("platform").upper()
    try:
        base_env_file = f'{ENV_DIR}/{context.ACTUAL_ENVIRONMENT.lower()}.json'
        app_env_file = f'{ENV_DIR}/{context.APPLICATION.lower()}-{context.ACTUAL_ENVIRONMENT.lower()}.json'

        # Debugging output
        logger.debug(f"Looking for base environment file: {base_env_file}")
        logger.debug(f"Looking for app environment file: {app_env_file}")

        with open(base_env_file, 'rb') as f:
            context.BASE_ENV_VARS = json.load(f)
        with open(app_env_file) as f:
            context.APP_ENV_VARS = json.load(f)
    except FileNotFoundError as e:
        logger.error(f"Environment file not found: {e.filename}")
        raise
    except Exception as e:
        logger.error(f"Unhandled exception occurred: {str(e)}")

    logger.debug("Creating context variables...")
    context.HOST = context.BASE_ENV_VARS['host']
    context.APP_VERSION = context.BASE_ENV_VARS["app_version"]
    context.PATHS = context.APP_ENV_VARS['paths']
    context.STORE_USERNAME = context.APP_ENV_VARS["STORE"]["USERNAME"]
    logger.debug("Variables created successfully !")

    logger.debug("Creating GCP instance...")
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(ENV_DIR, 'resources',
                                                                'google_cloud_credentials.json')
    credentials = GoogleCloudLoggingClient.get_credentials()
    LogVerifier._google_client = GoogleCloudLoggingClient(credentials=credentials)
    logger.debug("GCP instance created successfully")
    logger.info("Environment and Test Data loaded succesfully")
    yield context
    logger.info("Tearing down Behave fixture")


def before_all(context):
    logger.info("\t[STARTING] BACKEND AUTOMATION\t".center(100, '*'))
    use_fixture(behave_fixture, context)
    utils.clean_logs_dir(os.path.join(BASE_DIR, 'test', 'reports', 'logs'))
    logger.info(
        f"\t[RUNNING] BACKEND AUTOMATION FOR {context.APPLICATION} APPLICATION\t".center(
            100, '*'))


def before_feature(context, feature):
    logger.info(f'\t[RUNNING FEATURE] {feature.name}\t'.center(100, '-'))
    context.app_user = AppUserModel()
    context.app_user.application = context.APPLICATION
    context.store_user = StoreUserModel()
    context.DATA_MANAGER = data_manager
    if feature.name.upper() in ['CHECKOUT', 'SMOKE TESTS']:
        if context.APPLICATION == "JKR":
            context.BEETRACK_API_KEY = context.BASE_ENV_VARS["beetrack"]["api_key"]
            context.BEETRACK_DRIVER_IDENTIFIER = context.BASE_ENV_VARS["beetrack"]["driver_identifier"]
            context.BEETRACK_TRUCK_IDENTIFIER = context.BASE_ENV_VARS["beetrack"]["truck_identifier"]
            context.BEETRACK_SUB_STATUSES = context.BASE_ENV_VARS["beetrack"]["sub_statuses"]


def before_scenario(context, scenario):
    logger.info(f'\t[RUNNING SCENARIO] {scenario.name}\t'.center(100, '-'))
    if "RESET_VALUES" in scenario.tags:
        if context.VALUES["USER_DATA"].get("usuario_app"):
            context.app_user.clean()
            context.store_user.clean()
            context.VALUES["USER_DATA"].update(context.app_user.get_user())
            context.VALUES["USER_DATA"].update(context.store_user.get_user())


def after_scenario(context, scenario):
    logger.info(f'\t[END SCENARIO] {scenario.name}\t'.center(100, '-'))


def after_feature(context, feature):
    logger.info(f'\t[END FEATURE] {feature.name}\t'.center(100, '-'))


def after_all(context):
    logger.info("\t[GENERATING REPORTS]\t".center(100, '*'))
    logger.info("Creating allure environment.properties file")
    utils.create_allure_environment_file(
        env=context.ACTUAL_ENVIRONMENT.upper(),
        application=context.APPLICATION,
        app_version=context.APP_VERSION,
        platform=context.PLATFORM
    )
    logger.info("Allure environment.properties file created successfully")

    logger.info("Creating allure categories.json file...")
    utils.create_allure_categories_file(os.path.join(BASE_DIR, 'reports', 'allure-results'))
    logger.info("Allure categories.json file created successfully")

    logger.info("\t[END] BACKEND AUTOMATION\t".center(100, '*'))
