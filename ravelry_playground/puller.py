"""Pull data from Ravelry"""
import pandas as pd
import requests


def serialized_list(source: list, delimiter: str) -> str:
    """
    Join items in list based on delimiter needed by Ravelry (e.g., + for ids)
    :param source: list of items to join
    :param delimiter: what to join them with
    :return: string with items joined with delimiter
    """
    return delimiter.join([str(s) for s in source])


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Replace '.' in column names with '_'
    :param df: Dataframe with columns to check
    :return: Dataframe with clean columns
    """
    for column in list(df):
        if '.' in column:
            clean_column = column.replace('.', '_')
            df = df.rename(columns={column: clean_column})
    return df


def ravelry_get_data(
        auth_info: dict,
        path: str,
        data=None
):
    """
    Get response with basic authentication
    :param auth_info: dict with authentication data
    :param path: path to pull data from (e.g., patterns)
    :param data: additional parameters used when pulling data
    :return: request result when successful, error w/status code when not
    """
    url = f'https://api.ravelry.com/{path}.json'

    if auth_info.get('auth_type') == 'basic':
        user = auth_info.get('user')
        pwd = auth_info.get('pwd')
        result = requests.get(
            url,
            data=data,
            auth=requests.auth.HTTPBasicAuth(user, pwd)
        )
    elif auth_info.get('auth_type') == 'oauth':
        token = auth_info.get('token')
        result = requests.get(
            url,
            data=data,
            headers={
                'Authorization': f'Bearer {token}'
            }
        )
    else:
        raise RuntimeError('Invalid auth type')

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
