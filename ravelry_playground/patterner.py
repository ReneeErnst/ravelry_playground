import pandas as pd

import ravelry_playground


def pattern_search(user, pwd, query, page=1, page_size=100, **kwargs):

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
        import cauldron as cd
        if len(df_source) > 1:
            cd.display.table(df_source)
            cd.step.stop()

    df_pattern_sources = pd.concat(pattern_sources)
    print('Length Pattern Sources Data: ', len(df_pattern_sources))

    return df_patterns, df_pattern_sources
