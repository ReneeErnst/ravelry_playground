"""Pull data from Ravelry"""
import requests
import pandas as pd


def ravelry_get_data(user, pwd, path, ids=None, data=None):
    """
    Get response with basic authentication
    :param user:
    :param pwd:
    :param path:
    :param data:
    :return:
    """
    if not ids:
        url = f'https://api.ravelry.com/{path}.json'
        result = requests.get(
            url,
            data=data,
            auth=requests.auth.HTTPBasicAuth(user, pwd)
        )
    else:
        url = f'https://api.ravelry.com/{path}.json?ids={ids}'
        result = requests.get(
            url,
            auth=requests.auth.HTTPBasicAuth(user, pwd)
        )

    if result.status_code != 200:
        raise RuntimeError(f'Error status: {result.status_code}')
    else:
        return result.json()


def basic_json_normalize(
        data: dict,
        record_path: str,
        create_id: str,
        override_id: str
):
    df = pd.json_normalize(
        data=data,
        record_path=record_path
    )
    df[create_id] = create_id
    df = df.rename(
        columns={'id': override_id})

    return df
