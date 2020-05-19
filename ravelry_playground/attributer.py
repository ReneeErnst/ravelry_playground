"""Functions for getting data from Ravelry"""
import pandas as pd

from ravelry_playground import puller


def get_color_attributes(user, pwd):
    colors = puller.ravelry_get_data(
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
    yarn_attributes = puller.ravelry_get_data(
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
