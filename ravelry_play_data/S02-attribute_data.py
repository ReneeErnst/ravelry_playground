# Pull Color and Yarn attributes data
import cauldron as cd

import ravelry_playground

auth_info = cd.shared.auth_info
save_loc = cd.shared.save_loc

# Get all possible color attribute data
df_color_attributes = ravelry_playground.get_color_attributes(auth_info)

cd.display.header('Color Attributes Data: ', level=2)
cd.display.table(df_color_attributes.head())

# Get all possible yarn attribute data
df_yarn_attributes = ravelry_playground.get_yarn_attributes(auth_info)

cd.display.header('Yarn Attributes Data: ', level=2)
cd.display.table(df_yarn_attributes)


