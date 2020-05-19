"""Pull data from Ravelry"""
import requests


def ravelry_get_data(user, pwd, path, data=None):
    """
    Get response with basic authentication
    :param user:
    :param pwd:
    :param path:
    :param data:
    :return:
    """
    url = f'https://api.ravelry.com/{path}.json'

    result = requests.get(
        url,
        data=data,
        auth=requests.auth.HTTPBasicAuth(user, pwd)
    )

    if result.status_code != 200:
        raise RuntimeError(f'Error status: {result.status_code}')
    else:
        return result.json()
