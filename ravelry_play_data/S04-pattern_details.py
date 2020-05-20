import cauldron as cd

import ravelry_playground

auth_info = cd.shared.auth_info

# ToDo: Sample ID - will add code for processing on a set of ids to create
#  data for a table
ids = [237330]
data = {'ids': ravelry_playground.serialized_list(ids, ' ')}
pattern_details = ravelry_playground.get_pattern_data(
    auth_info,
    data
)

# Display a sample of data for each output dataframe
for key, value in pattern_details.items():
    print('Sample data for: ', key)
    cd.display.table(value.head())
