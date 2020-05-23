import datetime as dt
import os
import time

import cauldron as cd
from google.cloud import bigquery
from google.cloud import storage

import ravelry_playground

auth_info = cd.shared.auth_info
save_info = cd.shared.save_info

save_loc = save_info.get('save_loc')
project = save_info.get('project')
dataset = save_info.get('dataset')
bucket = save_info.get('bucket')

# where to save data locally or in bucket
local_save_path = os.path.join(
    save_info.get('local_save_path'),
    'pattern_details'
)
bucket_path = 'data/pattern_details'

# Get pattern details for sweater patterns pulled in previous step

# ToDo: Doesn't work when using a local running container - need to figure
#  out auth to GCP for that
# Get pattern ids
# noinspection SqlNoDataSourceInspection
query = f"""
    SELECT pattern_id
      FROM `{project}.{dataset}.sweater_pattern_data`
     ORDER BY pattern_id
"""
client = bigquery.Client()
query_job = client.query(query)

df = query_job.to_dataframe()

pattern_ids = df['pattern_id'].tolist()
# Random bad ID - watch out for these if you get a 500 error
pattern_ids.remove(41)

original_num_patterns = len(pattern_ids)

# Set pattern_ids to run based on any previous completed chunks
if save_loc == 'local':
    # If running locally, create directory for saving file chunks if it
    # doesn't exist
    if not os.path.exists(local_save_path):
        os.makedirs(local_save_path)

    previously_complete = ravelry_playground.previous_pattern_details_pulls(
        save_loc,
        pattern_ids,
        local_save_path=local_save_path
    )
else:
    previously_complete = ravelry_playground.previous_pattern_details_pulls(
        save_loc,
        pattern_ids,
        bucket_name=bucket,
        bucket_path=f'{bucket_path}/',
        client=storage.Client()
    )

max_complete_chunk = previously_complete.get('max_complete_chunk')
patterns_complete = previously_complete.get('patterns_complete')
if previously_complete.get('max_complete_chunk') > 0:
    cd.display.text(f'Max previously completed chunk: {max_complete_chunk}')
    cd.display.text(
        f'Number of previously completed patterns: {patterns_complete}')
    # Override pattern IDs with filtered list removing previously completed ids
    pattern_ids = previously_complete.get('pattern_ids')

# Track start time of data pull
start_time = time.monotonic()

# ToDo: Format free text fields describing patterns
chunk_tracker = 0 + max_complete_chunk  # Track what chunk we are on
chunk_size = 200  # How many records to pull at once
total_chunks = round(original_num_patterns / chunk_size)
remaining_chunks = round(len(pattern_ids) / chunk_size)

cd.display.text(f'Total chunks to pull for job: {total_chunks}')
cd.display.text(f'Remaining chunks to pull for job: {remaining_chunks}')
cd.display.text(f'Starting with pattern ID {pattern_ids[0]}')

pattern_details_data = []
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

    # Ravelry limits us to 100 requests for this method
    # After 100, stop and save the data out.
    if chunk_tracker % 100 == 0 or chunk_tracker == total_chunks:
        if save_loc == 'local':
            ravelry_playground.save_rav_files(
                save_loc,
                f'{chunk_tracker}_pattern_details',
                pattern_details_data,
                local_save_path=local_save_path
            )
        else:
            ravelry_playground.save_rav_files(
                save_loc,
                f'{chunk_tracker}_pattern_details',
                pattern_details_data,
                bucket_name=bucket,
                bucket_path=bucket_path,
                client=storage.Client()
            )
        cd.display.text('Chunks Saved')
        pattern_details_data = []

# Output how long data pull took:
end_time = time.monotonic()
time_diff = dt.timedelta(seconds=end_time - start_time)
cd.display.header(f'Time to pull data was: {time_diff}')
