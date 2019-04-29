from . import webapi


def login(username, password):
    return webapi.post('/login/login', json={
        'Username': username,
        'Password': password,
        'AppInstalled': False,
        'AutoLogin': False,
        'CheckForExistingProducts': True,
        'DoMerge': True,
    })
