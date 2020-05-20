import os

import cauldron as cd

# Config - Set your chosen auth type and save loc here
auth = 'oauth'  # Set to basic or oauth
save_loc = 'gcp'  # Set to gcp or local, or adjust code for another location

# Note for save_loc, for saving data locally rather than in the cloud, I
# created a folder at the top level of the repo called output_data and
# added that to the .gitignore. If you configure the code to save data
# somewhere else, make sure it does not end up in git as that would violate
# the terms of service for Ravelry (do not publicly share the data).

cd.display.header(
    f'Running with {auth} authentication and saving to {save_loc}')

# Assumes that credentials info is stored in text files at the top level of
# the repo (make sure they are in gitignore if naming them differently!
# If Basic Auth one file called user.txt and one called pwd.txt. If OAuth
# one file called token.txt. Adjust this code as needed if setting these
# variables differently, such as using environment variables.

auth_info = {}

directory = os.path.dirname(__file__)
if auth == 'basic':
    auth_info.update({'auth_type': 'basic'})
    with open(os.path.realpath(os.path.join(
            directory, '..', 'user.txt'))) as f:
        user = f.read().strip()
        auth_info.update({'user': user})

    with open(os.path.realpath(os.path.join(
            directory, '..', 'pwd.txt'))) as f:
        pwd = f.read().strip()
        auth_info.update({'pwd': pwd})
elif auth == 'oauth':
    auth_info.update({'auth_type': 'oauth'})
    with open(os.path.realpath(os.path.join(
            directory, '..', 'token.txt'))) as f:
        token = f.read().strip()
        auth_info.update({'token': token})
else:
    raise RuntimeError('Invalid auth type')

save_info = {}
# Create gcp related variables to have available in following steps:
if save_loc == 'gcp':
    save_info.update({'save_loc': 'gcp'})
    with open(os.path.realpath(
            os.path.join(directory, '..', 'project.txt'))) as f:
        project = f.read().strip()
        save_info.update({'project': project})

    with open(os.path.realpath(
            os.path.join(directory, '..', 'bucket.txt'))) as f:
        bucket = f.read().strip()
        save_info.update({'bucket': bucket})

    with open(os.path.realpath(
            os.path.join(directory, '..', 'dataset.txt'))) as f:
        dataset = f.read().strip()
        save_info.update({'dataset': dataset})
elif save_loc == 'local':
    # Save data to local machine
    save_info.update({'save_loc': 'local'})
    # Add path to save local data
    path = os.path.join(
        '..',
        'output_data'
    )
    save_info.update({'local_save_path': path})
else:
    # No save location indicated, no data will be saved
    save_info.update({'save_loc': None})

# Save variables for use in other steps
cd.shared.save_info = save_info
cd.shared.auth_info = auth_info
