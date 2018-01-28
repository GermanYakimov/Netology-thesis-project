import progressbar
import time


def find_unique_communities(user_communities, user_friends_communities):
    unique_groups = []

    with progressbar.ProgressBar(max_value=len(user_communities)) as bar:
        for i, group in enumerate(user_communities):
            if group not in user_friends_communities:
                unique_groups.append(group)
            bar.update(i)
            time.sleep(0.2)

    return unique_groups
