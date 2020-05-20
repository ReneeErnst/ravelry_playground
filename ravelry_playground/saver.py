import os

import pandas as pd


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


def save_data(data_to_save: dict, save_info: dict):
    """
    For each item in data to save, save data based on info in save_info
    :param data_to_save: dict of dataframes to save to gcp or locally
    :param save_info: Dict with info on where to save data to, including
    location locally or in GCP
    :return: True if function completes w/o error
    """
    for data_name, data in data_to_save.items():
        if save_info.get('save_loc') == 'gcp':
            _save_gcp(
                data,
                save_info,
                data_name
            )
            print(f'{data_name} saved to GCP!')
        elif save_info.get('save_loc') == 'local':
            _save_local(
                data,
                save_info,
                data_name
            )
            print(f'{data_name} saved locally!')
        else:
            print(f'No save location info included - not saving {data_name}')

    return True
