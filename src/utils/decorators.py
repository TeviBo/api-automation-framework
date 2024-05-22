import time
from functools import wraps
from time import sleep

from asteval import Interpreter

from src.utils.logger import logger


def log_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"Calling {func.__name__} with url: {args[0].host}, headers: {args[0].headers}")
        response = func(*args, **kwargs)
        logger.debug(f"{func.__name__} status_code: {response.status_code} - body: {response.body}")
        return response

    return wrapper


def retry_payment_on_422(retries: int = 5, wait_interval: int = 5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = None
            if kwargs.get('exception_test', False):
                return func(*args, **kwargs)
            for _ in range(retries):
                try:
                    response = func(*args, **kwargs)
                    if response.status_code != 422 or response.body.get('code') != 'PAY_01':
                        return response
                    logger.info('Error PAY_01 received, retrying...')
                    time.sleep(wait_interval)
                except Exception as e:
                    logger.error(f"Unhandled Exception occurred: {str(e)}")
            return response

        return wrapper

    return decorator


def check_condition(response, condition):
    aeval = Interpreter()
    try:
        aeval.symtable['response'] = response
        # Replace eval with a safer alternative if possible
        return aeval(condition)
    except Exception as e:
        logger.error(f"Error evaluating condition: {e}")
        return False


def is_expected_status(response, exp_status_code):
    return response.status_code == exp_status_code


def has_specific_error_code(response):
    return response.body.get("code") == "USE_LOG_03"


def should_return(response, exp_status_code, condition=None):
    if isinstance(response.body, list):
        if condition and is_expected_status(response, exp_status_code):
            logger.debug(f"Checking if response met condition. Condition: {condition}")
            return check_condition(response, condition)
    elif not has_specific_error_code(response):
        return is_expected_status(response, exp_status_code)


def retry_on_error(exp_status_code: int, condition: str = None, retries: int = 3, wait_interval: int = 5):
    """
    Decorator to retry a function call on error.

    Parameters:
    exp_status_code (int): The expected status code that the function should return.
    condition (str): Optional condition to check against the response. If provided,
                        the function should return True for the condition to be met.
    retries (int): Number of retries before giving up. Defaults to 3.
    wait_interval (int): Time in seconds to wait between retries. Defaults to 5.

    Returns:
    The result of the function call or the last response encountered if the desired conditions are never met.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = None
            for attempt in range(1, retries + 1):
                try:
                    response = func(*args, **kwargs)
                    if should_return(response, exp_status_code, condition):
                        return response
                except Exception as e:
                    logger.error(f"Error during function execution: {e}. Attempt {attempt} of {retries}.")
                logger.info(f"Desired response conditions not met. Retrying in {wait_interval} seconds...")
                time.sleep(wait_interval)
            logger.error("All retries exhausted without meeting the desired conditions.")
            return response

        return wrapper

    return decorator


def check_status_type(response, desired_status):
    if isinstance(desired_status, str):
        status_list = response.body.get("statusList", [])
        if not any(status_obj.get("name") == desired_status for status_obj in status_list):
            raise AssertionError(f"Desired status '{desired_status}' not achieved. \nStatus list: {status_list}")
        return response


def retry_until_order_status_change(desired_status, max_attempts=3, wait_interval=2):
    """

    This method, retry_until, is a decorator function that can be used to wrap another method/function.

    Parameters:
    - desired_status (str): The desired status that the wrapped method/function should return.
    - max_attempts (int): The maximum number of attempts to retry the wrapped method/function. Default value is 3.
    - wait_interval (int): The number of seconds to wait between each retry attempt. Default value is 2.

    Returns:
    The decorator function.

    Usage:
    @retry_until(desired_status='success', max_attempts=5, wait_interval=3)
    def some_function(...):
        ...

    The decorator function, retry_until, checks if the wrapped method/function returns a response with a
    status code of 200 and a status object that has the specified desired_status.
    If the condition is met, it returns the response.
    If not, it logs a message, waits for the specified wait_interval, and retries the wrapped method/function again
    for the specified max_attempts.
    If the desired_status is not achieved after all retry attempts, it raises an AssertionError.

    Note: This method requires the 'wraps' and 'logger' objects to be imported, and the 'last_exception' variable to be
    defined before using the decorator.

    """

    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            for _ in range(max_attempts):
                response = func(*args, **kwargs)
                if response.status_code == 200 and any(
                        status_obj.get("name") == desired_status for status_obj in response.body.get("statusList")):
                    return response
                else:
                    logger.info(f"Order status not achieved yet. Retrying in {wait_interval} seconds...")
                    sleep(wait_interval)
            raise AssertionError(f"Desired status '{desired_status}' not achieved after "
                                 f"{max_attempts * wait_interval} seconds. \n[Last exception]: \n{last_exception}")

        return wrapped

    return decorator
