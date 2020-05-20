"""
Get all data on sweater patterns
"""
import cauldron as cd
import pandas as pd

import ravelry_playground

auth_info = cd.shared.auth_info
save_info = cd.shared.save_info

# Pull data for all sweater patterns. Search limits us to 100k patterns, so
# splitting up the search to pull free patterns and then all other patterns
# except free
availability_search_option = {
    'free': 'free',
    # 'everything but free': ['online', 'inprint', 'ravelry', 'discontinued']
}

pattern_data = []
pattern_sources = []
total_patterns = 0
for option_name, options in availability_search_option.items():
    # First get number of result pages that will need to be pulled:
    results_stats = ravelry_playground.get_num_pattern_search_results(
        auth_info,
        pc='sweater',
        availability=options
    )

    num_results_pages = results_stats.get('last_page')
    num_patterns = results_stats.get('results')
    total_patterns += num_patterns

    cd.display.text(
        f'Search brings back {num_results_pages} pages of results, for a '
        f'total of {num_patterns} patterns'
    )

    # Add 1 to num results pages to handle python going up to, but not
    # including, last number
    pages = range(1, (num_results_pages + 1))

    for page in pages:
        results = ravelry_playground.pattern_search(
            auth_info,
            page=page,
            sort='name',
            pc='sweater',
            availability=['free']
        )

        pattern_data.append(results.get('patterns'))
        pattern_sources.append(results.get('pattern_sources'))

        print(f'Done with page {page}')

        # ToDo: Add sleep function if needed

    cd.display.header(
        f'All pages of pattern data pulled for {option_name} option!',
        level=3
    )

df_sweater_pattern_data: pd.DataFrame = pd.concat(pattern_data)
df_sweater_pattern_sources: pd.DataFrame = pd.concat(pattern_sources)

if len(df_sweater_pattern_data) != total_patterns:
    cd.display.text(
        f'Check Data - Num patterns was {total_patterns} but '
        f'length of pattern data is {len(df_sweater_pattern_data)}'
    )
else:
    cd.display.header(
        f'Number of patterns records: {len(df_sweater_pattern_data)}',
        level=2
    )

cd.display.header('Sample of pattern data: ', level=4)
cd.display.table(df_sweater_pattern_data.head())

cd.display.header('Sample of pattern sources data: ', level=4)
cd.display.table(df_sweater_pattern_sources.head())

# Data to save includes the table or file name as the key the data as the value
data_to_save = {
    'sweater_pattern_data': df_sweater_pattern_data,
    'sweater_pattern_sources': df_sweater_pattern_sources
}

# Save data out - save_info includes all needed info on where/how to save
ravelry_playground.save_data(data_to_save, save_info)
