import numpy as np
import pandas as pd

import ravelry_playground


def get_yarns(user: str, pwd: str, ids: list):
    yarn_ids = ' '.join(map(str, ids))
    yarn_ids = yarn_ids.replace(' ', '+')

    yarns = ravelry_playground.ravelry_get_data(
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
