# -*- coding: utf-8 -*-
'''
Created on Fri Sep  1 09:42:30 2023

@author: Kiiro Tenshi
'''

import networkx as nx
import matplotlib.pyplot as plt
from modules import get_margin

def find_cheapest_way(materials_dict, target_item, target_world, verbose=False):
    #split dictionary
    crafted_quantity = materials_dict['crafted_quantity']
    materials_dict = {key: value for key, value in materials_dict.items() if key not in ['crafted_quantity']}
    #get dictionary of world to buy the items
    world_dict = {}
    for item, sub_dict in materials_dict.items():
        for sub_item, source_info in sub_dict.items():
            source = source_info[0]  # Extract the source (the first element in the list)
            world_dict[sub_item] = source
            
    G = nx.DiGraph()
    # Create the directed graph as before
    for material, ingredients in materials_dict.items():
        for ingredient, cost in ingredients.items():
            if material != target_item:
                G.add_edge(ingredient, material, cost=0)
            else:
                G.add_edge(ingredient, material, cost=cost[1])
            G.add_edge(ingredient, target_item, cost=cost[1])

    # Find the cheapest way to make the target item
    smallest_node = [node for node in G.nodes() if G.in_degree(node) == 0]
    results = {'groceries_list': {}}
    total_cost = 0
    for node in smallest_node:
        cheapest_way = nx.shortest_path(G, source=node, target=target_item, weight='cost')               
        cost = nx.shortest_path_length(G, source=node, target=target_item, weight='cost')
        #determine what to buy
        for i in range(len(cheapest_way)-1):
            edge_data = G.get_edge_data(cheapest_way[i], cheapest_way[i+1])
            if edge_data['cost'] != 0:
                results['groceries_list'][cheapest_way[i]] = {'cost': cost,'step': cheapest_way[i:],
                                                              'world': world_dict[cheapest_way[i]]}  
        total_cost += cost

    results['total_cost_per_craft'] = total_cost
    results['crafted_quantity'] = crafted_quantity
    results['expected_margin'] = get_margin(target_item, target_world, total_cost/crafted_quantity)
    # Visualization
    if verbose:
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_size=800, node_color='skyblue', font_size=10, font_color='black')
        labels = nx.get_edge_attributes(G, 'cost')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.show()

    return results

if __name__ == '__main__':
    materials_dict = {'Baked Eggplant': {'Dark Eggplant': ['Faerie', 962], 'Garlean Cheese': ['Gilgamesh', 990], 'Frantoio Oil': ['Gilgamesh', 523], 'Giant Popoto': ['Jenova', 229], 'Blood Tomato': ['Midgardsormr', 282], 'Earthbreak Aethersand': ['Gilgamesh', 931]}, 'Garlean Cheese': {'Ovibos Milk': ['Faerie', 405]}, 'Frantoio Oil': {'Frantoio': ['Midgardsormr', 286],},
                      'crafted_quantity': 3}
    target_item = 'Baked Eggplant'
    target_world = 'Jenova'
    results = find_cheapest_way(materials_dict, target_item, target_world, verbose=True)
    # print(results)