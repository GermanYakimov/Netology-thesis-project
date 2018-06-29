import json
import progressbar
import time
import copy
import sys
import requests


v = '5.69'
access_token = '5dfd6b0dee902310df772082421968f4c06443abecbc082a8440cb18910a56daca73ac8d04b25154a1128'


class User:
    def __init__(self):
        self.short_name = ''
        self.id = -1
        self.friends = list()
        self.communities = list()
        self.friends_communities = set()
        self.unique_groups = list()

    def get_id_by_short_name(self):
        self.id = requests.get('https://api.vk.com/method/users.get', params={
            'v': v,
            'access_token': access_token,
            'user_ids': self.short_name
        }).json()['response'][0]['id']

    def get_communities(self, users):
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

    def communities_get_info(self, communities):
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

    def find_unique_communities(self):
        with progressbar.ProgressBar(max_value=len(self.communities)) as bar:
            for i, group in enumerate(self.communities):
                if group not in self.friends_communities:
                    self.unique_groups.append(group)
                bar.update(i)
                time.sleep(0.2)
        self.unique_groups = self.communities_get_info(self.unique_groups)

    def input_user_id(self):
        self.short_name = input('Введите id или короткое имя (screen name) пользователя: ')
        if not str(self.short_name).isdigit():
            self.get_id_by_short_name()

    def get_friends(self):
        self.friends = requests.get('https://api.vk.com/method/friends.get', params={
            'v': v,
            'user_id': self.id,
            'access_token': access_token
        }).json()['response']['items']

    def get_user_communities(self):
        print('Получение сообществ пользователя', file=sys.stderr)
        self.communities = self.get_communities([self.id])

    def get_friends_communities(self):
        print('Получение сообществ друзей пользователя', file=sys.stderr)
        self.friends_communities = self.get_communities(self.friends)

    def find_unique_groups(self):
        self.input_user_id()
        self.get_friends()
        self.get_user_communities()
        self.get_friends_communities()

        print('Анализ сообществ пользователя и поиск уникальных, получение информации о сообществах', file=sys.stderr)
        self.find_unique_communities()


def dump_unique_communities_to_json(user):
    if user.unique_groups:
        with open('result_%s.json' % user.short_name, 'w') as file:
            json.dump(user.unique_groups, file, indent=4, ensure_ascii=False)
    else:
        print('У пользователя нет уникальных сообществ')


user = User()
user.find_unique_groups()
dump_unique_communities_to_json(user)
