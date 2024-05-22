import json


class Response:
    def __init__(self, response):
        self.status_code = response.status_code
        avoided_status_codes = [204, 401, 403, 404, 405]
        if response.status_code <= 500 and response.status_code not in avoided_status_codes:
            self.body = json.loads(response.text)
        else:
            self.body = response.text
        self.method = response.request.method
        self.endpoint = response.url
        self.request = response.request.body
        self.headers = response.request.headers
