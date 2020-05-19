import json

import pandas as pd

import ravelry_playground


def pattern_search(
        user,
        pwd,
        query,
        page=1,
        page_size=100,
        **kwargs
):
    """
    Search and return pattern data. Returns data on the patterns themselves as
    well as pattern source data
    :param user:
    :param pwd:
    :param query:
    :param page:
    :param page_size:
    :param kwargs:
    :return:
    """

    query_data = {}
    query_data.update({'query': query})
    query_data.update({'page': page})
    query_data.update({'page_size': page_size})

    for key, value in kwargs.items():
        if isinstance(value, list):
            value = '|'.join(value)
        query_data.update({key: value})

    print('Query: ', query_data)
    result = ravelry_playground.ravelry_get_data(
        user,
        pwd,
        'patterns/search',
        data=query_data
    )

    patterns = result.get('patterns')

    # If pulling data from page 1 of search, also include sample data in output
    if page == 1:
        print('Sample Pattern Data: ')
        print(json.dumps(patterns[0], indent=2))

    paginator = result.get('paginator')
    print('Page: ', paginator.get('page'))
    print('Page Size: ', paginator.get('page_size'))
    print('Results: ', paginator.get('results'))

    df_patterns = pd.json_normalize(
        data=patterns
    )

    df_patterns = df_patterns.rename(columns={'id': 'pattern_id'})

    df_patterns = df_patterns.drop([
        'pattern_sources',
        'designer.users',
        'pattern_author.users'
    ], axis=1)

    print('Length Patterns Data: ', len(df_patterns))

    # Get pattern sources data
    pattern_sources = []
    for i in patterns:
        pattern_id = i.get('id')
        sources = i.get('pattern_sources')
        df_source = pd.json_normalize(
            data=sources
        )
        df_source['pattern_id'] = pattern_id

        pattern_sources.append(df_source)

    df_pattern_sources = pd.concat(pattern_sources)
    print('Length Pattern Sources Data: ', len(df_pattern_sources))

    return df_patterns, df_pattern_sources
