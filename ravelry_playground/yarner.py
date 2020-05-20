import numpy as np
import pandas as pd

import ravelry_playground


def get_yarns(auth_info: dict, data: dict) -> dict:
    """
    Get yarn related info for specific set of yarn IDs indicated in data input
    :param auth_info: auth for ravelry API
    :param data: data to use for api pull, in this case yarn IDs
    :return: Dict containing 3 dataframes with info on the yarn, fiber content
    for the yarn, and yarn photo info
    """
    yarns = ravelry_playground.ravelry_get_data(
        auth_info,
        'yarns',
        data=data
    ).get('yarns')

    yarn_info = []
    yarn_fiber_content = []
    yarn_photos = []

    for yarn_id, yarn_data in yarns.items():
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
    df_yarn_fiber_info = pd.concat(yarn_fiber_content)
    df_yarn_photo_info = pd.concat(yarn_photos)

    yarn_data_output = {
        'yarn_info': df_yarn_info,
        'yarn_fiber_info': df_yarn_fiber_info,
        'yarn_photo_info': df_yarn_photo_info
    }

    return yarn_data_output
