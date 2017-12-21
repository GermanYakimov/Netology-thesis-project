import progressbar
import time


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
