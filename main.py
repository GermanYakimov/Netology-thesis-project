import json
from get_data import User


user = User()
user.input_user_id()
user.get_friends()
user.get_user_communities()
user.get_friends_communities()
user.find_unique_groups()

if user.unique_groups:
    with open('result_%s.json' % user.short_name, 'w') as file:
        json.dump(user.unique_groups, file, indent=4, ensure_ascii=False)
else:
    print('У пользователя нет уникальных сообществ')
