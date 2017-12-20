import requests
from pprint import pprint
import time

v = '5.69'
access_token = '5dfd6b0dee902310df772082421968f4c06443abecbc082a8440cb18910a56daca73ac8d04b25154a1128'


def get_id(short_name):
    id = requests.get('https://api.vk.com/method/users.get', params={
        'v': v,
        'access_token': access_token,
        'user_ids': short_name
    }).json()['response'][0]['id']

    return id


def get_friends(id):
    if not id.isdigit():
        id = get_id(id)

    user_friends = requests.get('https://api.vk.com/method/friends.get', params={
        'v': v,
        'user_id': id,
        'access_token': access_token
    }).json()['response']['items']

    return user_friends


def get_communities(users):
    communities = dict()
    for user in users:
        print('#', end='')
        communities[user] = requests.get('https://api.vk.com/method/groups.get', params={
            'v': v,
            'user_id': id,
            'access_token': access_token
        }).json()['response']['items']
        time.sleep(1)

    return communities


id = '361170104'
user_friends = get_friends(id)
pprint(user_friends)
user_communities = get_communities([id])
pprint(user_communities)

user_friends_communities = get_communities(user_friends)
pprint(user_friends_communities)
