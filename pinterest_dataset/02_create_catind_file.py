#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 17:23:52 2018

@author: alejandro

@description: The module returns 1-to-1 correspondence to ‘all_pins_routes.txt’
              list of categories indexes. User indexes correspond directly to
              its position in categories lists file.
"""
from os import chdir
from os.path import isfile
from collections import defaultdict

chdir('..')
pins_dir = r'data/pinterest/'
data_dir = r'data/pinterest_dataset/'

# In
categories_list = r'categories_list.txt'
pins_routes = r'all_pins_routes.txt'

# Out
pins_cats = r'all_pins_categories.txt'

# this routine returns the board's cat
def get_board_cat(board_route, new_board_route, cat_ind):
    if( board_route == new_board_route ):
        return cat_ind, board_route
    board_route = new_board_route
    if not isfile(pins_dir+board_route+'/board_category.txt'):
        return cats_dict['None'], board_route
    with open(pins_dir+board_route+'/board_category.txt', 'r') as b_cat:
        category = b_cat.read().strip()
        if category == '':
            cat_ind = cats_dict['None']
        else:
            cat_ind = cats_dict[category]
    return cat_ind, board_route

# Create a lookup-table using key as category name and value as category 
# index retrieved from categories_list file order
cats_dict = defaultdict(int)
with open(data_dir+categories_list, 'r') as categories:
    for ind, cat in enumerate(categories.read().split()):
        cats_dict[cat] = ind
        
# Load routes list from file
routes_list = []
with open(data_dir+pins_routes, 'r') as pins_list:
    for route in pins_list:
        routes_list.append(route.strip())
        
i = 0; board_route=''; cat_ind = -1
with open(data_dir+pins_cats, 'w') as cats_out:
    for route in routes_list:
        user, filler, board, pin = route.split('/')
        cat_ind, board_route = get_board_cat(board_route,
                user+'/'+filler+'/'+board, cat_ind)
        cats_out.write(str(cat_ind)+'\n')
        i += 1