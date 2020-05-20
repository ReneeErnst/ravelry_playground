import cauldron as cd

import ravelry_playground

auth_info = cd.shared.auth_info

# ToDo: Sample ID - will add code for processing on a set of ids to create
#  data for a table
pattern_id = 173188

data = {
    'photoless': 1
}

ravelry_playground.get_pattern_project_data(
    auth_info,
    pattern_id,
    data=data
)
