# ravelry_play_data
import os
import cauldron as cd
import ravelry_playground

directory = os.path.dirname(__file__)

with open(os.path.realpath(os.path.join(directory, '..', 'token.txt'))) as f:
    token = f.read().strip()
    cd.shared.token = token

# Color attribute data
df_color_attributes = ravelry_playground.get_color_attributes(token)

cd.display.header('Color Attributes Data: ', level=2)
cd.display.table(df_color_attributes.head())

# Yarn attribute data
df_yarn_attributes = ravelry_playground.get_yarn_attributes(token)

cd.display.header('Yarn Attributes Data: ', level=2)
cd.display.table(df_yarn_attributes)
