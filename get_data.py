import requests
from pprint import pprint
import time
import progressbar
import sys
import copy
import json


v = '5.69'
access_token = '5dfd6b0dee902310df772082421968f4c06443abecbc082a8440cb18910a56daca73ac8d04b25154a1128'


def get_id(short_name):
    ID = requests.get('https://api.vk.com/method/users.get', params={
        'v': v,
        'access_token': access_token,
        'user_ids': short_name
    }).json()['response'][0]['id']

    return ID


def input_user_id():
    ID = input('Введите id или короткое имя (screen name) пользователя: ')
    if not str(ID).isdigit():
        ID = get_id(ID)

    return ID


def get_friends(ID):
    user_friends = requests.get('https://api.vk.com/method/friends.get', params={
        'v': v,
        'user_id': ID,
        'access_token': access_token
    }).json()['response']['items']

    return user_friends


def get_communities(users):
    communities = dict()

    with progressbar.ProgressBar(max_value=len(users)) as bar:
        for i, user in enumerate(users):
            try:
                communities[user] = requests.get('https://api.vk.com/method/groups.get', params={
                    'v': v,
                    'user_id': user,
                    'access_token': access_token
                }).json()['response']['items']
                time.sleep(1)
                bar.update(i)
            except:
                continue

    print('\n')
    return communities


def find_unique_communities(user_communities, user_friends_communities):
    unique_groups = dict()  # За уникальные так же считаем и такие группы, в которых состоят до 3 друзей пользователя

    with progressbar.ProgressBar(max_value=len(user_communities)) as bar:
        for i, group in enumerate(user_communities):
            counter = 0  # Счётчик друзей, состоящих в группе
            for friend_communities in user_friends_communities.values():
                if group in friend_communities:
                    counter += 1
            if counter <= 3:
                unique_groups[group] = counter
            bar.update(i)
            time.sleep(0.2)

    return unique_groups


def communities_get_info(communities):
    communities_str = ''
    with progressbar.ProgressBar(max_value=len(user_communities)) as bar:
        for i, community in enumerate(communities):
            communities_str += str(community) + ','
            bar.update(i)
        communities_str = communities_str[:len(communities_str) - 1]

        response = requests.get('https://api.vk.com/method/groups.getById', params={
            'group_ids': communities_str,
            'v': v,
            'access_token': access_token,
            'fields': 'members_count'
        })

    communities_info = response.json()['response']
    communities = []
    tmp_group = dict()
    # group = {'name': 'name', 'members_count': count}
    for group in communities_info:
        tmp_group['name'] = group['name']
        tmp_group['id'] = group['id']
        tmp_group['members_count'] = group['members_count']
        tmp_group['screen_name'] = group['screen_name']

        communities.append(tmp_group)
        communities = copy.deepcopy(communities)

    return communities


id = input_user_id()
user_friends = get_friends(id)

print('Получение сообществ пользователя', file=sys.stderr)
user_communities = get_communities([id])[id]

print('Получение сообществ друзей пользователя', file=sys.stderr)
user_friends_communities = get_communities(user_friends)

print('Анализ сообществ пользователя и поиск уникальных', file=sys.stderr)
unique_communities = find_unique_communities(user_communities, user_friends_communities)

print('Получение информации о сообществах', file=sys.stderr)
unique_communities = communities_get_info(unique_communities)
pprint(unique_communities)
print(len(unique_communities))

with open('result.json', 'w') as file:
    json.dump(unique_communities, file, indent=4)
