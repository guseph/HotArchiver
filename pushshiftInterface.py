import requests
import pprint
import time

class HTTPError(Exception):
    def __init__(self, http_error_code):
        self.http_error_code = http_error_code

    def error_code(self):
        return self.http_error_code

def get_request(ext_url:str, params:dict={})->requests.models.Response:
    base_url = 'https://api.pushshift.io'
    use_headers = {"User-Agent": 'pushshift tester:1.0'}
    use_response = requests.get(f"{base_url}{ext_url}", headers=use_headers, params=params)
    # return use_response

    if use_response.status_code == 200:
        use_response_dict = dict(use_response.json())
        # pprint.pprint(use_response_dict)
        return use_response_dict
    else:
        print(use_response.status_code)
        raise HTTPError(use_response.status_code)
