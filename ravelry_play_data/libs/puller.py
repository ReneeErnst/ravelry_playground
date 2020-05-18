import numpy as np
import pandas as pd
import requests


def _ravelry_get_data(user, pwd, path, query=None, ids=None):
    """
    Get response with basic authentication
    :param user:
    :param pwd:
    :param path:
    :param query:
    :return:
    """
    if query:
        url = f'https://api.ravelry.com/{path}/{query}.json'
    elif ids:
        url = f'https://api.ravelry.com/{path}.json?ids={ids}'
    else:
        url = f'https://api.ravelry.com/{path}.json'

    result = requests.get(
        url,
        auth=(user, pwd)
    )

    if result.status_code != 200:
        raise RuntimeError(f'Error status: {result.status_code}')
    else:
        return result.json()


def get_color_attributes(user, pwd):
    colors = _ravelry_get_data(
        user,
        pwd,
        'color_families'
    )

    color_data = colors.get('color_families')

    df_color_attributes: pd.DataFrame = pd.DataFrame(color_data)

    # Drop color column since it has no values
    df_color_attributes = df_color_attributes.drop('color', axis=1)

    return df_color_attributes


def get_yarn_attributes(user, pwd):
    yarn_attributes = _ravelry_get_data(
        user,
        pwd,
        '/yarn_attributes/groups'
    ).get('yarn_attribute_groups')

    yarn_attribute_dfs = []
    for attribute in yarn_attributes:
        yarn_attribute = attribute

        yarn_attribute_type = yarn_attribute.get('name')
        attribute_data = yarn_attribute.get('yarn_attributes')

        df_attribute: pd.DataFrame = pd.DataFrame(attribute_data)
        df_attribute['yarn_attribute_type'] = yarn_attribute_type
        yarn_attribute_dfs.append(df_attribute)

    df_yarn_attributes = pd.concat(yarn_attribute_dfs)

    df_yarn_attributes = df_yarn_attributes[[
        'yarn_attribute_group_id',
        'yarn_attribute_type',
        'name',
        'description',
        'id',
        'permalink',
        'sort_order'
    ]]

    return df_yarn_attributes


def get_yarns(user: str, pwd: str, ids: list):
    yarn_ids = ' '
    yarn_ids = yarn_ids.join(ids)
    yarn_ids = yarn_ids.replace(' ', '+')

    yarns = _ravelry_get_data(
        user,
        pwd,
        'yarns',
        ids=yarn_ids
    ).get('yarns')

    yarn_info = []
    yarn_fiber_content = []
    yarn_photos = []

    for yarn_id, data in yarns.items():
        yarn = yarns.get(yarn_id)

        df_yarn = pd.json_normalize(yarn)
        df_yarn = df_yarn.rename(columns={'id': 'yarn_id'})
        df_yarn = df_yarn.drop(['yarn_fibers', 'photos'], axis=1)
        yarn_info.append(df_yarn)

        df_fibers = pd.json_normalize(
            data=yarn,
            record_path='yarn_fibers'
        )
        df_fibers['yarn_id'] = yarn_id
        df_fibers['used_fiber'] = np.arange(len(df_fibers))
        df_fibers['total_used_fibers'] = len(df_fibers)
        df_fibers = df_fibers.rename(columns={'id': 'fiber_id'})
        yarn_fiber_content.append(df_fibers)

        df_photos = pd.json_normalize(
            data=yarn,
            record_path='photos'
        )
        df_photos['yarn_id'] = yarn_id
        df_photos['total_photos'] = len(df_photos)
        df_photos = df_photos.rename(
            columns={'id': 'photo_id', 'sort_order': 'photo_sort_order'})
        yarn_photos.append(df_photos)

    df_yarn_info = pd.concat(yarn_info)
    df_fiber_info = pd.concat(yarn_fiber_content)
    df_photo_info = pd.concat(yarn_photos)

    return df_yarn_info, df_fiber_info, df_photo_info


# def get_pattern_search_data():
#     # ToDo: Add function that can search patterns
#     print('')
#
#
# def get_user_data(name, username, password):
#     result = ravelry_get('people', name, username, password)
#     return result
#
#
# def get_yarn_data():
#     # ToDo: Get data on different yarns in Ravelry
#     print('')
#
#
# def get_user_stash(user):
#     # ToDo: Get data on user's stash
#     print('')
#
#
# def get_user_lib(user):
#     # ToDo: Get data on what patterns user has
#     print('')
