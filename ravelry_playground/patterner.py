import pandas as pd

import ravelry_playground


def get_num_pattern_search_results(
        auth_info: dict,
        query: str = '',
        page_size: int = 100,
        **kwargs
) -> dict:
    query_data = {}
    query_data.update({'query': query})
    query_data.update({'page': 1})
    query_data.update({'page_size': page_size})

    # Add any other passed in arguments for the search
    for key, value in kwargs.items():
        if isinstance(value, list):
            value = ravelry_playground.serialized_list(value, '|')
        query_data.update({key: value})

    result = ravelry_playground.ravelry_get_data(
        auth_info,
        'patterns/search',
        data=query_data
    )

    paginator = result.get('paginator')
    return paginator


def pattern_search(
        auth_info: dict,
        query: str = '',
        page: int = 1,
        page_size: int = 100,
        **kwargs
) -> dict:
    """
    Search and return pattern data. Returns data on the patterns themselves as
    well as pattern source data
    :param auth_info: auth for ravelry API
    :param query: String with search term if wanted - use like search box on
    site in combo with any filters passed in via kwargs
    :param page: page to pull from search data
    :param page_size: Size of records per page
    :param kwargs: Any filters to add to results - can use any from ravelry
    site
    :return: dict with 2 DataFrames containing the pattern data and
    pattern source data
    """

    query_data = {}
    query_data.update({'query': query})
    query_data.update({'page': page})
    query_data.update({'page_size': page_size})

    # Add any other passed in arguments for the search
    for key, value in kwargs.items():
        if isinstance(value, list):
            value = ravelry_playground.serialized_list(value, '|')
        query_data.update({key: value})

    result = ravelry_playground.ravelry_get_data(
        auth_info,
        'patterns/search',
        data=query_data
    )

    patterns = result.get('patterns')

    df_patterns = pd.json_normalize(
        data=patterns
    )

    df_patterns = df_patterns.rename(columns={'id': 'pattern_id'})

    df_patterns = df_patterns.drop([
        'pattern_sources',
        'designer.users',
        'pattern_author.users'
    ], axis=1)

    # Rename columns in data to match needs for BigQuery (remove '.' character)
    df_patterns = ravelry_playground.clean_column_names(df_patterns)

    # Get pattern sources data
    # ToDo: Consider saving all the data pulled from Ravelry before doing
    #  transformations. It may consume fewer resources.
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

    results = {
        'patterns': df_patterns,
        'pattern_sources': df_pattern_sources
    }

    return results


def get_pattern_data(auth_info: dict, data: dict) -> dict:
    """
    Pull pattern related data for specific pattern ids included in data input
    :param auth_info: auth for ravelry API
    :param data: dict with data to include in Ravelry request, in this case
    pattern ids
    :return: dict with pandas dataframes for various pattern related info
    """
    pattern_details = ravelry_playground.ravelry_get_data(
        auth_info,
        'patterns',
        data=data
    ).get('patterns')

    pattern_data = []
    pattern_needles = []
    pattern_yarn = []
    pattern_categories = []
    pattern_attributes = []
    pattern_photos = []

    for pattern_id, data in pattern_details.items():
        pattern = pattern_details.get(pattern_id)

        df_pattern = pd.json_normalize(pattern)
        df_pattern = df_pattern.rename(columns={'id': 'pattern_id'})
        df_pattern = df_pattern.drop([
            'pattern_needle_sizes',
            'packs',
            'printings',
            'pattern_categories',
            'pattern_attributes',
            'photos',
            'pattern_author.users'
        ], axis=1)

        pattern_data.append(df_pattern)

        # Needled info for pattern
        df_pattern_needles = ravelry_playground.basic_json_normalize(
            pattern,
            'pattern_needle_sizes',
            pattern_id,
            'pattern_needle_id'
        )
        pattern_needles.append(df_pattern_needles)

        # Yarn info for pattern
        df_pattern_yarn = ravelry_playground.basic_json_normalize(
            pattern,
            'packs',
            pattern_id,
            'pattern_yarn_id'
        )
        pattern_yarn.append(df_pattern_yarn)

        # Category mapping for pattern
        df_pattern_categories = ravelry_playground.basic_json_normalize(
            pattern,
            'pattern_categories',
            pattern_id,
            'top_category_id'
        )
        pattern_categories.append(df_pattern_categories)

        # Pattern attributes
        df_pattern_attributes = ravelry_playground.basic_json_normalize(
            pattern,
            'pattern_attributes',
            pattern_id,
            'pattern_attribute_id'
        )
        pattern_attributes.append(df_pattern_attributes)

        # Photos data
        df_photos = ravelry_playground.basic_json_normalize(
            pattern,
            'photos',
            pattern_id,
            'pattern_photo_id'
        )
        pattern_photos.append(df_photos)

    results = {
        'df_pattern_data': pd.concat(pattern_data),
        'df_pattern_needles': pd.concat(pattern_needles),
        'df_pattern_yarn': pd.concat(pattern_yarn),
        'df_pattern_categories': pd.concat(pattern_categories),
        'df_pattern_attributes': pd.concat(pattern_attributes),
        'df_pattern_photos': pd.concat(pattern_photos),
    }

    return results


def get_pattern_project_data(auth_info: dict, pattern_id: int, data: dict):
    """
    Project related data for given pattern
    :param auth_info: auth for ravelry API
    :param pattern_id: pattern ID to get project data for
    :param data:
    :return:
    """
    pattern_project_info = ravelry_playground.ravelry_get_data(
        auth_info,
        f'patterns/{pattern_id}/projects',
        data=data
    )
    import json
    print(json.dumps(pattern_project_info, indent=2))
