import cauldron as cd
import os
import ravelry_playground

results_files = [
    f for f in os.listdir('pattern_details') if os.path.isfile(
        os.path.join('pattern_details', f)
    )
]

print(type(results_files))
print(len(results_files))
print(results_files[0])

# df_pattern_details_data = ravelry_playground.clean_pattern_details_data(
#     pattern_details_data
# )
#
# cd.display.text('Sample of pattern details data: ')
# cd.display.table(df_pattern_details_data.head())
#
# ravelry_playground.save_table(df, 'sweater_pattern_details', save_info)
# cd.display.header('Pattern Details Data Saved to GCP!')
#
# nested_data_types = {
#     'pattern_needle_sizes': [],
#     'packs': [],
#     'pattern_categories': [],
#     'pattern_attributes': [],
#     'photos': []
# }
#
# # Pull out the nested data from pattern_details data
# for nested_data_type, output in nested_data_types.items():
#     nested_data = ravelry_playground.get_nested_pattern_details_data(
#         pattern_details_data,
#         nested_data_type
#     )
#     output += nested_data
#
# for nested_data_type, output in nested_data_types.items():
#     df = pd.json_normalize(
#         data=output
#     )
#     # Rename columns in data to match needs for BigQuery (remove '.' character)
#     df = ravelry_playground.clean_column_names(df)
#
#     table_name = nested_data_type.replace('pattern_', '')
#     table_name = f'sweater_pattern_details_{table_name}'
#
#     cd.display.text(f'Sample of {table_name} data')
#     cd.display.table(df.head())
#
#     ravelry_playground.save_table(df, table_name, save_info)
#
# cd.display.header('Nested Pattern Details Data Saved to GCP!')
