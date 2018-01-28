import requests
import time
import progressbar
import copy
import sys
from analyze import find_unique_communities


v = '5.69'
access_token = '5dfd6b0dee902310df772082421968f4c06443abecbc082a8440cb18910a56daca73ac8d04b25154a1128'


def get_id_by_short_name(short_name):
    user_id = requests.get('https://api.vk.com/method/users.get', params={
        'v': v,
        'access_token': access_token,
        'user_ids': short_name
    }).json()['response'][0]['id']

    return user_id


def get_communities(users):
    communities = []
    with progressbar.ProgressBar(max_value=len(users)) as bar:
        for i, user in enumerate(users):
            try:
                communities.extend(requests.get('https://api.vk.com/method/groups.get', params={
                    'v': v,
                    'user_id': user,
                    'access_token': access_token
                }).json()['response']['items'])
                time.sleep(1)
                bar.update(i)
            except:
                continue

    print('\n')
    return set(communities)


def communities_get_info(communities):
    if not communities:
        return []

    communities_str = ''
    with progressbar.ProgressBar(max_value=len(communities)) as bar:
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
    communities = list()
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


class User:
    def __init__(self):
        self.short_name = ''
        self.id = -1
        self.friends = list()
        self.communities = list()
        self.friends_communities = set()
        self.unique_groups = list()

    def input_user_id(self):
        self.short_name = input('Введите id или короткое имя (screen name) пользователя: ')
        if not str(self.short_name).isdigit():
            self.id = get_id_by_short_name(self.short_name)

    def get_friends(self):
        self.friends = requests.get('https://api.vk.com/method/friends.get', params={
            'v': v,
            'user_id': self.id,
            'access_token': access_token
        }).json()['response']['items']

    def get_user_communities(self):
        print('Получение сообществ пользователя', file=sys.stderr)
        self.communities = get_communities([self.id])

    def get_friends_communities(self):
        print('Получение сообществ друзей пользователя', file=sys.stderr)
        self.friends_communities = get_communities(self.friends)

    def find_unique_groups(self):
        print('Анализ сообществ пользователя и поиск уникальных, получение информации о сообществах', file=sys.stderr)
        self.unique_groups = communities_get_info(find_unique_communities(self.communities, self.friends_communities))
