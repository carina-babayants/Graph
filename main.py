import matplotlib.pyplot as plt
import networkx as nx
import re
from vk.exceptions import VkAPIError
import numpy as np


TOKEN = 'ваш токен'


def show_graph(groups_out):
    set_list = {}
    for key, values in groups_out.items():
        set_list[key] = set(values['items'])

    graph = nx.Graph()

    for key, values in set_list.items():

        graph.add_node(key)
        graph.add_nodes_from(values)
        graph.add_edges_from([(key, value) for value in values])

    nx.draw(graph)
    plt.show()


def show_plot(groups_out):
    set_1 = set(groups_out['love_zozh']['items'])
    set_2 = set(groups_out['vestnik_zozh']['items'])

    np.random.seed(1)

    set_1_bounds_x = np.random.uniform(low=0, high=2, size=len(set_1 - set_2))
    set_1_bounds_y = np.random.uniform(low=0, high=10, size=len(set_1 - set_2))

    inter_bounds_x = np.random.uniform(low=2, high=6, size=len(set_2 & set_1))
    inter_bounds_y = np.random.uniform(low=0, high=10, size=len(set_2 & set_1))

    set_2_bounds_x = np.random.uniform(low=4, high=6, size=len(set_1 - set_2))
    set_2_bounds_y = np.random.uniform(low=0, high=10, size=len(set_1 - set_2))

    plt.scatter(set_1_bounds_x, set_1_bounds_y, c='r', label=f'love_zozh len={len(set_1 - set_2)}')
    plt.scatter(inter_bounds_x, inter_bounds_y, c='g', label=f'Пересечение len={len(set_2 & set_1)}')
    plt.scatter(set_2_bounds_x, set_2_bounds_y, c='b', label=f'vestnik_zozh len={len(set_1 - set_2)}')
    plt.legend(loc='upper left')
    plt.show()


def main():
    import vk

    session = vk.Session(access_token=TOKEN)
    vk_api = vk.API(session)

    # рассматриваю две группы по ЗОЖ, из которых получаю id всех участников группы
    groups_list = ['https://vk.com/love_zozh',
                   'https://vk.com/vestnik_zozh']

    groups_out = {}
    for group in groups_list:
        group_name = re.sub('https://vk.com/', '', group)
        try:
            groups_out[group_name] = vk_api.groups.getMembers(
                group_id=group_name, count=1000, offset=0, v='5.81'
            )
        except VkAPIError as error:
            print(f'Error occurred {error}')

    show_plot(groups_out)
    # show_graph(groups_out)


if __name__ == '__main__':
    main()
