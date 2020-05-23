"""
Get all data on sweater patterns
"""
import datetime as dt
import time

import cauldron as cd

import ravelry_playground

auth_info = cd.shared.auth_info
save_info = cd.shared.save_info

# Note that some duplicate pattern IDs occur when pulling data this way.
# It happens when the pattern is tagged as free, but also has one of the
# other tags. Could work on a method to prevent this, but for now just
# remove dups.

# Pull data for all sweater patterns. Search limits us to 100k patterns, so
# splitting up the search to pull free patterns and then all other patterns
# except free
availability_search_option = {
    'free': 'free',
    'everything but free': ['online', 'inprint', 'ravelry', 'discontinued']
}

pattern_results = []
total_patterns = 0

# Track start time of data pull
start_time = time.monotonic()

for option_name, options in availability_search_option.items():
    cd.display.text(f'Starting with search option {option_name}')

    # First get number of result pages that will need to be pulled:
    results_stats = ravelry_playground.get_num_pattern_search_results(
        auth_info,
        page_size=1000,
        sort='name',
        pc='sweater',
        availability=options
    )

    num_results_pages = results_stats.get('last_page')
    num_patterns = results_stats.get('results')
    total_patterns += num_patterns

    cd.display.text(
        f'Search for option {option_name} brings back {num_results_pages} '
        f'pages of results, for a total of {num_patterns} patterns'
    )

    # Add 1 to num results pages to handle python going up to, but not
    # including, last number
    pages = range(1, (num_results_pages + 1))

    for page in pages:
        patterns = ravelry_playground.pattern_search(
            auth_info,
            page=page,
            page_size=1000,
            sort='name',
            pc='sweater',
            availability=options
        )

        if len(patterns) == 0:
            print(f'Uh oh, no pattern results for page {page}')

        len_before = len(pattern_results)
        pattern_results += patterns
        len_after = len(pattern_results)
        expected_len = len_before + len(patterns)

        if len_after != expected_len:
            cd.display.text(
                f'Something went wrong! Length of pattern results before '
                f'adding patterns was {len_before}, it is now {len_after}, '
                f'but length now should be {expected_len}'
            )

        # Display done with page every 10 pages
        if page % 10 == 0:
            print(f'Done with page {page}')

    cd.display.header(
        f'All pages of pattern data pulled for {option_name} option!',
        level=3
    )

# Output how long data pull took:
end_time = time.monotonic()
cd.display.header(
    f'Time to pull data was: {dt.timedelta(seconds=end_time - start_time)}')

df_sweater_patterns = ravelry_playground.clean_pattern_search_results(
    pattern_results
)
df_sweater_patterns = df_sweater_patterns.drop_duplicates()

df_patterns_source_data = ravelry_playground.create_pattern_source_data(
    pattern_results
)
df_patterns_source_data = df_patterns_source_data.drop_duplicates()

cd.display.header(
    f'Number of patterns records: {len(df_sweater_patterns)}',
    level=2
)

cd.display.header('Sample of pattern data: ', level=4)
cd.display.table(df_sweater_patterns.head())

cd.display.header('Sample of pattern sources data: ', level=4)
cd.display.table(df_patterns_source_data.head())
cd.display.text(
    f'Length of patterns source data: {len(df_patterns_source_data)}')

# Data to save includes the table or file name as the key the data as the value
data_to_save = {
    'sweater_pattern_data': df_sweater_patterns,
    'sweater_pattern_sources': df_patterns_source_data
}

for table_name, df in data_to_save.items():
    # Save data out - save_info includes all needed info on where/how to save
    ravelry_playground.save_table(df, table_name, save_info)
