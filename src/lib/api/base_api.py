from typing import Dict, Any, Optional

import requests

from src.lib.adapters.response_adapter import Response
from src.utils.logger import logger


class BaseClient:
    TIMEOUT: int = 10  # Timeout in seconds
    CONTENT_TYPE: str = "application/json"

    def __init__(self, host: str, **kwargs):
        self.host = host
        self.token = kwargs.get("token")
        self.headers = {
            'X-Application': kwargs.get("application"),
            'access_token': kwargs.get("access_token") if kwargs.get(
                "application") != 'BOF' else f'Bearer {kwargs.get("access_token")}',
            'Authorization': f'Bearer {self.token}' if self.token else None,
            'X-User-Id': kwargs.get("user_id"),
            'X-App-Version': kwargs.get("app_version"),
            'Firebase_token': kwargs.get("firebase_token"),
            'Identity_token': kwargs.get("identity_token"),
            'client_id': kwargs.get("client_id"),
            'X-Platform': kwargs.get("platform"),
            'X-Device-Id': kwargs.get("device_id", '438e9e341b92876a'),
            'X-Device-UUID': kwargs.get("device_uuid", '438e9e341b92876a')
        }

    def _request(self, **kwargs) -> Response:
        headers = self._prepare_headers(kwargs.get('headers'))
        url = f"{self.host}/{kwargs.get('endpoint')}"
        if kwargs.get('headers'):
            del kwargs['headers']
        if kwargs.get('endpoint'):
            del kwargs['endpoint']
        try:
            response = self._execute_request(**kwargs, url=url, headers=headers)
            logger.debug(f"Response status_code: {response.status_code} - body: {response.body}")
            return response
        except requests.RequestException as e:
            logger.error(f"Failed to execute {method} request to {url}: {e}")
            raise

    def _prepare_headers(self, headers: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        if not headers:
            return self.headers
        else:
            headers.update(self.headers)
            return headers

    # # @log_request
    def _execute_request(self, **kwargs) -> Response:
        # Prepare the common parameters for the request
        request_params = {
            'method': kwargs.get('method'),
            'url': kwargs.get('url'),
            'headers': kwargs.get('headers'),
            'files': kwargs.get('files'),
            'timeout': self.TIMEOUT,
            'auth': (kwargs.get('auth').get('client_id'), kwargs.get('auth').get('secret')) if kwargs.get(
                'auth') else None
        }

        # Add the payload based on the content type
        if kwargs.get('content_type', self.CONTENT_TYPE) == self.CONTENT_TYPE:
            request_params['json'] = kwargs.get('payload')
        else:
            request_params['data'] = kwargs.get('payload')

        payload_log = kwargs.get("payload") if isinstance(kwargs.get("payload"), dict) else "File"
        logger.debug(f"Calling endpoint with url: {kwargs.get('url')}, headers: {kwargs.get('headers')} and payload: "
                     f"{payload_log}")
        response = requests.request(**request_params)
        return Response(response)

    def get(self, **kwargs) -> Response:
        return self._request(method="GET", **kwargs)

    def post(self, **kwargs) -> Response:
        return self._request(method="POST", **kwargs)

    def put(self, **kwargs) -> Response:
        return self._request(method="PUT", **kwargs)

    def delete(self, **kwargs) -> Response:
        return self._request(method="DELETE", **kwargs)
