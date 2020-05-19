import cauldron as cd

import ravelry_playground

user = cd.shared.user
pwd = cd.shared.pwd

# ToDo: Get IDs first
ids = [26, 27]

# Get yarns data
df_yarn_info, df_yarn_fiber, df_yarn_photos = ravelry_playground.get_yarns(
    user, pwd, ids)

cd.display.header('Yarn Info Data: ', level=2)
cd.display.table(df_yarn_info)

cd.display.header('Yarn Fiber Data: ', level=2)
cd.display.table(df_yarn_fiber)

cd.display.header('Yarn Photos Data: ', level=2)
cd.display.table(df_yarn_photos)
