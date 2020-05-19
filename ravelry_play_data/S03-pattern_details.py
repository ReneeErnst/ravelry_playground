import cauldron as cd

import ravelry_playground

user = cd.shared.user
pwd = cd.shared.pwd

# ToDo: Sample ID - will add code for processing on a set of ids to create
#  data for a table
ids = [237330]

df_pattern_details = ravelry_playground.get_pattern_data(
    user,
    pwd,
    ids
)
