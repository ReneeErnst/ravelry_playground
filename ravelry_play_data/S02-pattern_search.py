import cauldron as cd
import ravelry_playground

token = cd.shared.token

# Looks like the number of patterns that we can get back is numbered, so will
# need to narrow the search
pages = [1]
for page in pages:
    df_pattern_data, df_pattern_sources = ravelry_playground.pattern_search(
        token,
        page=page,
        sort='name',
        pc='sweater',
        # availability=['online', 'free']
    )

    cd.display.table(df_pattern_data)
    cd.display.table(df_pattern_sources)
