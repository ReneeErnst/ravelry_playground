# ravelry_play_data
import os
import cauldron as cd
import ravelry_playground

directory = os.path.dirname(__file__)

with open(os.path.realpath(os.path.join(directory, '..', 'user.txt'))) as f:
    user = f.read().strip()
    cd.shared.user = user

with open(os.path.realpath(os.path.join(directory, '..', 'pwd.txt'))) as f:
    pwd = f.read().strip()
    cd.shared.pwd = pwd

# Color attribute data
df_color_attributes = ravelry_playground.get_color_attributes(user, pwd)

cd.display.header('Color Attributes Data: ', level=2)
cd.display.table(df_color_attributes.head())

# Yarn attribute data
df_yarn_attributes = ravelry_playground.get_yarn_attributes(user, pwd)

cd.display.header('Yarn Attributes Data: ', level=2)
cd.display.table(df_yarn_attributes)
