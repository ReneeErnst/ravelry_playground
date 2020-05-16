# ravelry_play_data
import os
import cauldron as cd
import pandas as pd
import puller

directory = os.path.dirname(__file__)

with open(os.path.realpath(os.path.join(directory, '..', 'user.txt'))) as f:
    user = f.read().strip()

with open(os.path.realpath(os.path.join(directory, '..', 'pwd.txt'))) as f:
    pwd = f.read().strip()

result = puller.ravelry_get_basic(
    user,
    pwd,
    'color_families'
)

print(result)

color_data = result.get('color_families')

df: pd.DataFrame = pd.DataFrame(color_data)

cd.display.table(df.head())
