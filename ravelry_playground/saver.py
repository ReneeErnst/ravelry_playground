import os

import pandas as pd
import pandas_gbq


def create_save_info(
        save_loc: str
) -> dict:
    """
    Get info on where to save data. Set path to appropriate files depending on
    if running locally or remotely in GCP
    :param save_loc: str indicating where output should be saved
    :return: dict with save info
    """
    save_info = {}
    save_info.update({'save_loc': save_loc})

    local_save_path = os.path.join(
        '..',
        'output_data'
    )
    save_info.update({'local_save_path': local_save_path})

    save_files = {
        'project': 'project.txt',
        'bucket': 'bucket.txt',
        'dataset': 'dataset.txt'
    }

    for save_name, save_file in save_files.items():
        path = os.path.join(
            os.path.dirname(__file__),
            save_file
        )

        if os.path.exists(path):
            with open(path) as f:
                save_item = f.read().strip()
                save_info.update({save_name: save_item})

    return save_info


def _save_gcp(
        df: pd.DataFrame,
        save_info: dict,
        table_name: str,
        exists_behavior: str = 'replace'):
    """
    Save dataframe to GCP BigQuery
    :param df: pandas dataframe to save
    :param save_info: dict with info on save related info
    :param table_name: name of table to save to
    :param exists_behavior: What to do if table exists - default replace
    :return: True if save completed
    """
    pandas_gbq.context.project = save_info.get('project')

    # save data to gcp
    df.to_gbq(
        f'{save_info.get("dataset")}.{table_name}',
        save_info.get('project'),
        if_exists=exists_behavior
    )
    return True


def _save_local(df, save_info: dict, save_name: str):
    """
    Save hdf file to local system
    :param df: pandas dataframe to save
    :param save_info: dict with info on save related info
    :param save_name:
    :return:
    """
    df.to_hdf(
        os.path.join(
            save_info.get('local_save_path'),
            f'{save_name}.hdf'
        ),
        f'df_{save_name}',
        format='table',
        mode='w'
    )
    return True


def save_data(df_save: pd.DataFrame, table_name: str, save_info: dict):
    """
    For each item in data to save, save data based on info in save_info
    :param df_save: dataframe to save to gcp or locally
    :param table_name: Name of table or file to save to
    :param save_info: Dict with info on where to save data to, including
    location locally or in GCP
    :return: True if function completes w/o error
    """

    if save_info.get('save_loc') == 'gcp':
        _save_gcp(
            df_save,
            save_info,
            table_name
        )
        print(f'{table_name} saved to GCP!')
    elif save_info.get('save_loc') == 'local':
        _save_local(
            df_save,
            save_info,
            table_name
        )
        print(f'{table_name} saved locally!')
    else:
        print(f'No save location info included - not saving {table_name}')

    return True
