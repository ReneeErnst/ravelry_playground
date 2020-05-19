import cauldron as cd

import ravelry_playground

user = cd.shared.user
pwd = cd.shared.pwd

# ToDo: Sample ID - will add code for processing on a set of ids to create
#  data for a table
pattern_id = 173188

data = {
    'photoless': 1
}

ravelry_playground.get_pattern_project_data(
    user,
    pwd,
    pattern_id,
    data=data
)
