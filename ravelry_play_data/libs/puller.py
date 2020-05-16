import requests
import argparse
import sys


def ravelry_get_basic(username, password, path, query=None):
    """
    Get response with basic authentication
    :param username:
    :param password:
    :param path:
    :param query:
    :return:
    """
    if query:
        url = f'https://api.ravelry.com/{path}/{query}.json'
    else:
        url = f'https://api.ravelry.com/{path}.json'

    result = requests.get(
        url,
        auth=(username, password)
    )

    if result.status_code != 200:
        raise RuntimeError(f'Error status: {result.status_code}')
    else:
        return result.json()


# def parse_patterns():
#     """
#
#     :return:
#     """
#     parser = argparse.ArgumentParser()
#
#     parser.add_argument('pc', type=str, default='')
#     parser.add_argument('weight', type=str, default='')
#     parser.add_argument('view', type=str, default='captioned_thumbs')
#     parser.add_argument('sort', type=str, default='')
#     parser.add_argument('fit', type=str, default='')
#     parser.add_argument('craft', type=str, default='')
#     parser.add_argument(
#         'colors', type=int, default=1, help='Colors must be an integer')
#
#     return parser.parse_args(sys.argv)
#
#
# def get_users():
#     # ToDo: Add function that gets users - can we get them based on activity
#     #  date?
#     print('')
#
#
# def get_user_data(name, username, password):
#     result = ravelry_get('people', name, username, password)
#     return result
#
#
# def get_pattern_data(user, pwd):
#     args = parse_patterns()
#
#     pc = args.pc
#     weight = args.weight
#     view = args.view
#     sort = args.sort
#     fit = args.fit
#     craft = args.craft
#     colors = args.colors
#     result = requests.get(
#         f'https://api.ravelry.com/patterns/search.json?'
#         f'pc={pc}'
#         f'&weight={weight}'
#         f'&view={view}'
#         f'&sort={sort}'
#         f'&fit={fit}'
#         f'&craft={craft}'
#         f'&colors={colors}',
#         auth=requests.auth.HTTPBasicAuth(user, pwd))
#
#     return result.json()
#
#
# def get_yarn_data():
#     # ToDo: Get data on different yarns in Ravelry
#     print('')
#
#
# def get_user_stash(user):
#     # ToDo: Get data on user's stash
#     print('')
#
#
# def get_user_lib(user):
#     # ToDo: Get data on what patterns user has
#     print('')
