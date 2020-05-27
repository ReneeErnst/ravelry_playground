import cauldron as cd

import ravelry_playground

# Config - Set your chosen auth type and save loc here
auth_type = 'basic'  # Set to basic or oauth
save_loc = 'gcp'  # Set to gcp or local, or adjust code for another location
run_loc = 'gcp'  # set to gcp or local, or adjust code for another location

# Note for save_loc, for saving data locally rather than in the cloud, I
# created a folder at the top level of the repo called output_data and
# added that to the .gitignore. If you configure the code to save data
# somewhere else, make sure it does not end up in git as that would violate
# the terms of service for Ravelry (do not publicly share the data).

cd.display.header(
    f'Running with {auth_type} authentication and saving to {save_loc}')

# Assumes that credentials info is stored in text files at the top level of
# the repo (make sure they are in gitignore if naming them differently!
# If Basic Auth one file called user.txt an one called pwd.txt. If OAuth
# one file called token.txt. Adjust this code as needed if setting these
# variables differently, such as using environment variables.

# dict with authentication related info
auth_info = ravelry_playground.create_auth_info(auth_type)

# dict with info on where to save data
save_info = ravelry_playground.create_save_info(save_loc)

# Save variables for use in other steps
cd.shared.save_info = save_info
cd.shared.auth_info = auth_info
