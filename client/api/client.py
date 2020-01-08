import requests
from urllib.parse import urljoin

from . import exceptions


class BaseAPIClient:
    _DOMAIN = 'http://0.0.0.0:8080'
    _MAP_ENDOINT = '/map/'
    _CHAR_ENDPOINT = '/char/'
    _USER_ENDPOINT = '/user/'

    _methods_to_ep_mapping = {
        'generate': _MAP_ENDOINT,
        'get_tile_mapping': _MAP_ENDOINT
    }

    @classmethod
    def send_request(cls, method, params=None):
        data = {
            'id': 1,
            'jsonrpc': '2.0',
            'params': params or {},
            'method': method,
        }

        url = urljoin(cls._DOMAIN, cls._methods_to_ep_mapping[method])

        r = requests.post(url, json=data)
        result = r.json()

        if 'error' in result:
            raise exceptions.ApiError(result['error'])
        return result['result']

    @classmethod
    def get_new_map(cls, params=None):
        return cls.send_request(
            'generate',
            params
        )

    @classmethod
    def get_tile_mapping(cls):
        return cls.send_request(
            'get_tile_mapping'
        )
