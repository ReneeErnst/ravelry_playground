"""Pull data from Ravelry"""
import json
import os

import pandas as pd
import requests
from google.cloud import storage


def create_auth_info(
        auth_type: str
) -> dict:
    """
    Create authentication info. Set path to appropriate files depending on
    if running locally or remotely in GCP.
    :param auth_type: str indicating what type of auth is being used
    :return: dict with authentication info
    """
    auth_info = {}
    auth_info.update({'auth_type': auth_type})

    auth_files = {
        'user': 'user.txt',
        'pwd': 'pwd.txt',
        'token': 'token.txt'
    }

    for auth_name, auth_file in auth_files.items():
        path = os.path.join(
            os.path.dirname(__file__),
            auth_file
        )

        if os.path.exists(path):
            with open(path) as f:
                auth_item = f.read().strip()
                auth_info.update({auth_name: auth_item})

    return auth_info


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
    Replace '.' in column names with '_', then remove any duplicate column
    names
    :param df: Dataframe with columns to check
    :return: Dataframe with clean columns
    """
    for column in list(df):
        if '.' in column:
            clean_column = column.replace('.', '_')
            df = df.rename(columns={column: clean_column})

    # remove any duplicate column names
    df = df.loc[:, ~df.columns.duplicated()]
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


def get_blobs_in_gcs_loc(
        client: storage.Client,
        bucket_name: str,
        bucket_path: str
):
    """
    Downloads a blob from given bucket
    :param client: gcs client
    :param bucket_name: gcs bucket name
    :param bucket_path: name of object in bucket
    :return: results with list of data from blobs
    """
    bucket = client.bucket(bucket_name)
    # Get name of results files in bucket location
    blob_names = [
        blob.name
        for blob in bucket.list_blobs(prefix=bucket_path)
        if blob.name != bucket_path
    ]

    results = []

    for blob_name in blob_names:
        blob_contents = (
            bucket.get_blob(blob_name).download_as_string().decode('utf-8')
        )

        results += json.loads(blob_contents)

    return results
