"""Pull data from Ravelry"""
import requests
import pandas as pd


def serialized_list(source: list, delimiter: str) -> str:
    return delimiter.join([str(s) for s in source])


def ravelry_get_data(
        token,
        path,
        data=None
):
    """
    Get response with basic authentication
    :param token: API Auth info
    :param path: path to pull data from (e.g., patterns)
    :param data: additional parameters used when pulling data
    :return: request result when successful, error w/status code when not
    """
    url = f'https://api.ravelry.com/{path}.json'

    result = requests.get(
        url,
        data=data,
        # auth=requests.auth.HTTPBasicAuth(user, pwd)
        headers={
            'Authorization': f'Bearer {token}'
        }
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
    """
    Convert JSON data nested 1 level deep to pd.DataFrame
    :param data: data to use for df
    :param record_path: path in data to where records wanted are
    :param create_id: id to create in data
    :param override_id: id to rename
    :return: pd.DataFrame with needed data
    """
    df = pd.json_normalize(
        data=data,
        record_path=record_path
    )
    df[create_id] = create_id
    df = df.rename(
        columns={'id': override_id})

    return df
