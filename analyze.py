import progressbar
import time


def find_unique_communities(user_communities, user_friends_communities):
    unique_groups = []  # За уникальные так же считаем и такие группы, в которых состоят до 3 друзей пользователя

    with progressbar.ProgressBar(max_value=len(user_communities)) as bar:
        for i, group in enumerate(user_communities):
            friends_in_community = False  # Флаг, отражающий то, состоят ли друзья в сообществе
            if group in user_friends_communities:
                friends_in_community = True
            if not friends_in_community:
                unique_groups.append(group)
            bar.update(i)
            time.sleep(0.2)

    return unique_groups
