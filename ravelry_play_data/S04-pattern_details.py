import datetime as dt
import time

import cauldron as cd
import pandas as pd
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
    'photos': []
}

# Track start time of data pull
start_time = time.monotonic()

# ToDo: Format free text fields describing patterns
# ToDo: Test different Chunk Sizes
chunk_tracker = 0  # Track what chunk we are on
chunk_size = 200  # How many records to pull at once
num_chunks = round(len(pattern_ids) / chunk_size)
cd.display.text(f'Number of Chunks to Pull: {num_chunks}')
for patterns in range(0, len(pattern_ids), chunk_size):
    chunk = pattern_ids[patterns: patterns + chunk_size]

    # Pass in chunk of pattern ids to get pattern details for those patterns
    data = {'ids': ravelry_playground.serialized_list(chunk, ' ')}
    pattern_details = ravelry_playground.get_pattern_data(
        auth_info,
        data
    )
    pattern_details_data += pattern_details

    chunk_tracker += 1
    # Display done with page every 10 pages
    if chunk_tracker % 10 == 0:
        print(f'Done with chunk {chunk_tracker}')
    # ToDo: For every so many chunks, save data out to files and pull it
    #  together later once all data is saved. Deal with loss if something
    #  fails.

# Output how long data pull took:
end_time = time.monotonic()
cd.display.header(
    f'Time to pull data was: {dt.timedelta(seconds=end_time - start_time)}')

for pattern_details in pattern_details_data:
    for nested_data_type, output in nested_data_types.items():
        nested_data = ravelry_playground.get_nested_pattern_details_data(
            pattern_details,
            nested_data_type
        )
        output += nested_data

df_pattern_details_data = ravelry_playground.clean_pattern_details_data(
    pattern_details_data
)

cd.display.text('Sample of pattern details data: ')
cd.display.table(df_pattern_details_data.head())

ravelry_playground.save_data(df, 'sweater_pattern_details', save_info)
cd.display.header('Pattern Details Data Saved to GCP!')

for nested_data_type, output in nested_data_types.items():
    df = pd.json_normalize(
        data=output
    )
    # Rename columns in data to match needs for BigQuery (remove '.' character)
    df = ravelry_playground.clean_column_names(df)

    table_name = nested_data_type.replace('pattern_', '')
    table_name = f'sweater_pattern_details_{table_name}'

    cd.display.text(f'Sample of {table_name} data')
    cd.display.table(df.head())

    ravelry_playground.save_data(df, table_name, save_info)

cd.display.header('Nested Pattern Details Data Saved to GCP!')
