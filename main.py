from pprint import pprint
import sys
import json
import analyze
import get_data


user_short_name, user_id = get_data.input_user_id()
user_friends = get_data.get_friends(user_id)

print('Получение сообществ пользователя', file=sys.stderr)
user_communities = get_data.get_communities([user_id])

print('Получение сообществ друзей пользователя', file=sys.stderr)
user_friends_communities = get_data.get_communities(user_friends)

print('Анализ сообществ пользователя и поиск уникальных', file=sys.stderr)
unique_communities = analyze.find_unique_communities(user_communities, user_friends_communities)

print('Получение информации о сообществах', file=sys.stderr)
unique_communities = get_data.communities_get_info(unique_communities)
pprint(unique_communities)
print(len(unique_communities))

with open('result_%s.json' % user_short_name, 'w') as file:
    json.dump(unique_communities, file, indent=4, ensure_ascii=True)
