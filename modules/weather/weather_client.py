import json
import urllib.parse
import urllib.request
import os

BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?q='


class Weather:
    def __init__(self, api_key=None):
        if api_key is not None and not isinstance(api_key, str):
            raise TypeError("riot_key must be str")
        self.api_key = api_key

    def get(self, *args):
        url = resolve(*args, key=self.api_key)
        req = urllib.request.Request(url)
        body = b''

        resp = urllib.request.urlopen(req)
        while True:
            buf = resp.read()
            if not buf:
                break
            body += buf
        return json.loads(body.decode())


def resolve(*args, key):
    url = BASE_URL + ''.join(args).replace(' ', '')
    url = url + '&appid=' + key
    return url
