# Pull Color and Yarn attributes data
import cauldron as cd

import ravelry_playground

auth_info = cd.shared.auth_info
save_info = cd.shared.save_info

data_to_save = {}
# Get all possible color attribute data
df_color_attributes = ravelry_playground.get_color_attributes(auth_info)

data_to_save.update({'color_attributes': df_color_attributes})

cd.display.header('Color Attributes Data: ', level=2)
cd.display.table(df_color_attributes.head())

# Get all possible yarn attribute data
df_yarn_attributes = ravelry_playground.get_yarn_attributes(auth_info)

data_to_save.update({'yarn_attributes': df_yarn_attributes})

cd.display.header('Yarn Attributes Data: ', level=2)
cd.display.table(df_yarn_attributes)

# Save data out - save_info data indicates location to save
for name, data in data_to_save.items():
    ravelry_playground.save_table(data, name, save_info)
