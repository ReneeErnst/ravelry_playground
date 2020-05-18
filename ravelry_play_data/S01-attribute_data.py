# ravelry_play_data
import os
import cauldron as cd
import puller

directory = os.path.dirname(__file__)

with open(os.path.realpath(os.path.join(directory, '..', 'user.txt'))) as f:
    user = f.read().strip()
    cd.shared.user = user

with open(os.path.realpath(os.path.join(directory, '..', 'pwd.txt'))) as f:
    pwd = f.read().strip()
    cd.shared.pwd = pwd

# Color attribute data
df_color_attributes = puller.get_color_attributes(user, pwd)

cd.display.header('Color Attributes Data: ', level=2)
cd.display.table(df_color_attributes.head())

# Yarn attribute data
df_yarn_attributes = puller.get_yarn_attributes(user, pwd)

cd.display.header('Yarn Attributes Data: ', level=2)
cd.display.table(df_yarn_attributes)

# ToDo: Figure out how to get list of valid yarn_ids
start_yarn_id = 26
ids = []
for yarn_id in range(start_yarn_id, start_yarn_id + 20):
    ids.append(str(yarn_id))

# Get yarns data
df_yarn_info, df_yarn_fiber, df_yarn_photos = puller.get_yarns(user, pwd, ids)

cd.display.header('Yarn Info Data: ', level=2)
cd.display.table(df_yarn_info)

cd.display.header('Yarn Fiber Data: ', level=2)
cd.display.table(df_yarn_fiber)

cd.display.header('Yarn Photos Data: ', level=2)
cd.display.table(df_yarn_photos)
