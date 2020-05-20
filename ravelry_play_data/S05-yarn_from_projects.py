import cauldron as cd

import ravelry_playground

token = cd.shared.token

# ToDo: Get IDs first
ids = [26, 27]
data = {
    'ids': ravelry_playground.serialized_list(ids, ' ')
}

# Get yarns data
df_yarn_info, df_yarn_fiber, df_yarn_photos = ravelry_playground.get_yarns(
    token, data)

cd.display.header('Yarn Info Data: ', level=2)
cd.display.table(df_yarn_info)

cd.display.header('Yarn Fiber Data: ', level=2)
cd.display.table(df_yarn_fiber)

cd.display.header('Yarn Photos Data: ', level=2)
cd.display.table(df_yarn_photos)
