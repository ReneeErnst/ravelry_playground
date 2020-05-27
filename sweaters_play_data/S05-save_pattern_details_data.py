import os

import cauldron as cd
import pandas as pd
from google.cloud import storage

import ravelry_playground

auth_info = cd.shared.auth_info
save_info = cd.shared.save_info

if save_info.get('save_loc') == 'local':
    local_save_path = os.path.join(
        save_info.get('local_save_path'),
        'pattern_details'
    )

    pattern_details_results = [
        f for f in local_save_path if os.path.isfile(
            os.path.join(local_save_path, f)
        )
    ]
else:
    client = storage.Client()
    bucket = save_info.get('bucket')

    pattern_details_results = ravelry_playground.get_blobs_in_gcs_loc(
        client,
        bucket,
        'data/pattern_details/'
    )

print('Len pattern details', len(pattern_details_results))

# Clean column names
df_pattern_details = ravelry_playground.clean_pattern_details_data(
    pattern_details_results
)

# Deal with bad character issue found in pattern_author_notes and notes columns
# for a couple patterns
df_pattern_details = df_pattern_details.assign(
    pattern_author_notes=df_pattern_details['pattern_author_notes'].map(
        lambda s: (s or '').replace(chr(0), '')
    ),
    notes=df_pattern_details['notes'].map(
        lambda s: (s or '').replace(chr(0), '')
    )
)

cd.display.text('Sample of pattern details data: ')
cd.display.table(df_pattern_details.head())

ravelry_playground.save_table(
    df_pattern_details,
    'sweater_pattern_details',
    save_info
)
cd.display.header('Pattern Details Data Saved to GCP!')

nested_data_types = {
    'pattern_needle_sizes': [],
    'packs': [],
    'pattern_categories': [],
    'pattern_attributes': [],
    'photos': []
}

# Pull out the nested data from pattern_details data
for nested_data_type, output in nested_data_types.items():
    nested_data = ravelry_playground.get_nested_pattern_details_data(
        pattern_details_results,
        nested_data_type
    )
    output += nested_data

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

    ravelry_playground.save_table(df, table_name, save_info)

cd.display.header('Nested Pattern Details Data Saved to GCP!')
