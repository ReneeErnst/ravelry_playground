import cauldron as cd
import pandas as pd

import ravelry_playground

auth_info = cd.shared.auth_info

# Looks like the number of patterns that we can get back is numbered, so will
# need to narrow the search
pages = [1, 2]

pattern_data = []
pattern_sources = []
for page in pages:
    results = ravelry_playground.pattern_search(
        auth_info,
        page=page,
        sort='name',
        pc='sweater',
        # availability=['online', 'free']
    )

    pattern_data.append(results.get('patterns'))
    pattern_sources.append(results.get('pattern_sources'))

df_pattern_data: pd.DataFrame = pd.concat(pattern_data)
df_pattern_sources: pd.DataFrame = pd.concat(pattern_sources)

cd.display.header('Sample of pattern data: ')
cd.display.table(df_pattern_data.head())
print('Number of patterns records: ', len(df_pattern_data))

cd.display.header('Sample of pattern sources data: ')
cd.display.table(df_pattern_sources.head())
