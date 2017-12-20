import requests
from pprint import pprint


def get_friends(id):
    v = '5.69'
    access_token = '5dfd6b0dee902310df772082421968f4c06443abecbc082a8440cb18910a56daca73ac8d04b25154a1128'
    if not id.isdigit():
        id = requests.get('https://api.vk.com/method/users.get', params={
            'v': v,
            'access_token': access_token,
            'user_ids': id
        }).json()['response'][0]['id']

    user_friends = requests.get('https://api.vk.com/method/friends.get', params={
        'v': v,
        'user_id': id,
        'access_token': access_token
    }).json()['response']['items']

    return user_friends


id = 'german_yakimov'
pprint(get_friends(id))
