import cauldron as cd

import ravelry_playground

auth_info = cd.shared.auth_info

# ToDo: Use this to eventually get yarn info from projects

# ToDo: Get IDs first
ids = [26, 27]
data = {
    'ids': ravelry_playground.serialized_list(ids, ' ')
}

# Get dict of yarns data
yarn_info = ravelry_playground.get_yarns(auth_info, data)

cd.display.header('Yarn Info Data: ', level=2)
cd.display.table(yarn_info.get('yarn_info'))

cd.display.header('Yarn Fiber Data: ', level=2)
cd.display.table(yarn_info.get('yarn_fiber_info'))

cd.display.header('Yarn Photos Data: ', level=2)
cd.display.table(yarn_info.get('yarn_photo_info'))
