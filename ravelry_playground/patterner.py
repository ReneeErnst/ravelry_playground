import os

import pandas as pd
from google.cloud import storage

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

    return result.get('patterns')


def clean_pattern_search_results(pattern_results):

    df_patterns = pd.json_normalize(
        data=pattern_results
    )

    df_patterns = df_patterns.rename(columns={'id': 'pattern_id'})

    df_patterns = df_patterns.drop([
        'pattern_sources',
        'designer.users',
        'pattern_author.users'
    ], axis=1)

    # Rename columns in data to match needs for BigQuery (remove '.' character)
    df_patterns = ravelry_playground.clean_column_names(df_patterns)

    return df_patterns


def create_pattern_source_data(pattern_results: list):
    source_data_results = []
    for pattern in pattern_results:
        pattern_id = pattern.get('id')
        source_data = pattern.get('pattern_sources')

        # Add pattern_id to source data
        for source in source_data:
            source.update({'pattern_id': pattern_id})
            source_data_results.append(source)

    df_pattern_source_data = pd.json_normalize(
        data=source_data_results
    )
    return df_pattern_source_data


def get_pattern_data(auth_info: dict, data: dict) -> list:
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

    for pattern_id, data in pattern_details.items():
        data.update({'pattern_id': pattern_id})
        pattern_data.append(data)

    return pattern_data


def clean_pattern_details_data(pattern_details_data: list) -> pd.DataFrame:
    df_pattern_details_data = pd.json_normalize(
        data=pattern_details_data
    )

    df_pattern_details_data = df_pattern_details_data.drop([
        'pattern_needle_sizes',
        'packs',
        'printings',
        'pattern_categories',
        'pattern_attributes',
        'photos',
        'pattern_author.users'
    ], axis=1)

    # Rename columns in data to match needs for BigQuery (remove '.' character)
    df_pattern_details_data = ravelry_playground.clean_column_names(
        df_pattern_details_data)

    return df_pattern_details_data


def get_nested_pattern_details_data(
        pattern_details_data: list,
        nested_info: str
) -> list:
    """
    Pull the columns with nested data out of pattern_details data and
    format to usable form
    :param pattern_details_data: List of all the detailed patterns data
    :param nested_info: The type of nested info to pull out
    :return: List with nested data of the given type for all patterns in
    pattern_details_data
    """
    nested_data = []
    for pattern in pattern_details_data:
        pattern_id = pattern.get('pattern_id')
        pattern_nested_info = pattern.get(nested_info)
        for item in pattern_nested_info:
            item.update({'pattern_id': pattern_id})
            item[f'{nested_info}_id'] = item.pop('id')
            nested_data.append(item)

    return nested_data


def previous_pattern_details_pulls(
        save_loc: str,
        pattern_ids: list,
        local_save_path: str = None,
        bucket_name: str = None,
        bucket_path: str = None,
        client: storage.client = None
) -> dict:
    """
    Check directory to see if previous chunks of pattern details have been
    pulled, and if so, adjust pattern_ids to reflect what should be pulled next
    :param save_loc:
    :param pattern_ids: List of pattern ids to pull data for
    :param local_save_path: Path to save items if running locally
    :param bucket_name:
    :param bucket_path: location in bucket for files
    :param client:
    :return: stats on previously completed chunks, patterns complete, and
    pattern_ids to now pull for
    """
    if save_loc == 'local':
        results_file_names = [
            f for f in os.listdir(local_save_path) if os.path.isfile(
                os.path.join(local_save_path, f))
        ]
    else:
        results_file_names = []
        bucket = client.bucket(bucket_name)
        blobs = list(bucket.list_blobs(prefix=bucket_path))
        for blob in blobs:
            object_name = blob.name
            if object_name != bucket_path:
                object_name = object_name.replace(bucket_path, '')
                results_file_names.append(object_name)

    if len(results_file_names) == 0:
        max_complete_chunk = 0
        patterns_complete = 0
    else:
        complete_chunks = [
            int(chunk.split('_')[0]) for chunk in results_file_names]
        max_complete_chunk = max(complete_chunks)
        patterns_complete = max_complete_chunk * 200
        # Pattern IDs to start on now
        pattern_ids = pattern_ids[patterns_complete:]

    result = {
        'max_complete_chunk': max_complete_chunk,
        'patterns_complete': patterns_complete,
        'pattern_ids': pattern_ids
    }

    return result


def get_pattern_project_data(auth_info: dict, pattern_id: int, data: dict):
    """
    Project related data for given pattern
    :param auth_info: auth for ravelry API
    :param pattern_id: pattern ID to get project data for
    :param data:
    :return:
    """
    # ToDo In Progress
    pattern_project_info = ravelry_playground.ravelry_get_data(
        auth_info,
        f'patterns/{pattern_id}/projects',
        data=data
    )
    import json
    print(json.dumps(pattern_project_info, indent=2))
