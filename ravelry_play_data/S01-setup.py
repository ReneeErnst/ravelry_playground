import os

import cauldron as cd

# Config - Set your chosen auth type here
auth = 'oauth'  # Set to basic or oauth

cd.display.header(f'Running with {auth} authentication')

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
            directory, '..', 'user.txt'
    ))) as f:
        user = f.read().strip()
        auth_info.update({'user': user})

    with open(os.path.realpath(os.path.join(directory, '..', 'pwd.txt'))) as f:
        pwd = f.read().strip()
        auth_info.update({'pwd': pwd})
elif auth == 'oauth':
    auth_info.update({'auth_type': 'oauth'})
    with open(os.path.realpath(os.path.join(
            directory, '..', 'token.txt'
    ))) as f:
        token = f.read().strip()
        auth_info.update({'token': token})
else:
    raise RuntimeError('Invalid auth type')

cd.shared.auth_info = auth_info
