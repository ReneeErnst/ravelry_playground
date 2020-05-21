import cauldron as cd
from google.cloud import bigquery

import ravelry_playground

auth_info = cd.shared.auth_info
save_info = cd.shared.save_info

project = save_info.get('project')
dataset = save_info.get('dataset')
# Get pattern details for sweater patterns pulled in previous step

# Get pattern ids
# noinspection SqlNoDataSourceInspection
query = f"""
    SELECT pattern_id
      FROM `{project}.{dataset}.sweater_pattern_data`
"""
client = bigquery.Client()
query_job = client.query(query)

df = query_job.to_dataframe()

pattern_ids = df['pattern_id'].tolist()

pattern_details_data = []

nested_data_types = {
    'pattern_needle_sizes': [],
    'packs': [],
    'pattern_categories': [],
    'pattern_attributes': [],
    'photos': [],
}

chunk_size = 2
# for patterns in range(0, len(pattern_ids), chunk_size):
for patterns in range(0, 10, chunk_size):
    chunk = pattern_ids[patterns: patterns + chunk_size]

    # Pass in chunk of pattern ids to get pattern details for those patterns
    data = {'ids': ravelry_playground.serialized_list(chunk, ' ')}
    pattern_details = ravelry_playground.get_pattern_data(
        auth_info,
        data
    )
    pattern_details_data += pattern_details

    for nested_data_type, output in nested_data_types.items():
        nested_data = ravelry_playground.get_nested_pattern_details_data(
            pattern_details,
            nested_data_type
        )
        output += nested_data

df_pattern_details_data = ravelry_playground.clean_pattern_details_data(
    pattern_details_data
)
cd.display.table(df_pattern_details_data)

# ToDo: Create the Dataframes from nested_data_types

# ToDo: Save to GCP BigQuery
