import time
import requests

API_ROOT = 'https://www.nemlig.com/webapi'

__session = requests.Session()


class NemligException(Exception):
    pass


def get(path, **kwargs):
    return __send('GET', path, **kwargs)


def post(path, **kwargs):
    return __send('POST', path, **kwargs)


def __send(method, path, **kwargs):
    time.sleep(1)  # poor mans rate limiting
    response = __session.request(method, API_ROOT + path, **kwargs)
    if response.status_code == 400:
        message = response.json()['ErrorMessage']
        raise NemligException(message)
    try:
        response.raise_for_status()
    except:
        print(response.text)
        raise
    return response.json()
