#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  19 22:53:05 2018

@author: Alejandro Guevara
"""
from os import chdir
from os.path import isfile
from collections import defaultdict

chdir('..')
pins_dir = r'data/pinterest/'
data_dir = r'data/pinterest_dataset/'

# In
usernames_list = r'usernames_list.txt'
categories_list = r'categories_list.txt'
pins_routes = r'all_pins_routes.txt'

# Out
pins_cats = r'all_pins_categories.txt'
pins_users = r'all_pins_users.txt'

# returns the board cat, dev to improve performance
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

# Create a dictionary to access easily to user or cat indexes using string form
users_dict = defaultdict(int)
with open(data_dir+usernames_list) as users:
    for ind, user in enumerate(users.read().split()):
        users_dict[user] = ind

cats_dict = defaultdict(int)
with open(data_dir+categories_list) as categories:
    for ind, cat in enumerate(categories.read().split()):
        cats_dict[cat] = ind
        
# Reads the whole list of pin routes
routes_list = []
with open(data_dir+pins_routes, 'r') as pins_list:
    for route in pins_list:
        routes_list.append(route.strip())

i = 0; board_route=''; cat_ind = -1
with open(data_dir+pins_users, 'w') as users_out:
    with open(data_dir+pins_cats, 'w') as cats_out:
        for route in routes_list:
            user, filler, board, pin = route.split('/')
            users_out.write(str(users_dict[user])+'\n')
            cat_ind, board_route = get_board_cat(board_route,
                    user+'/'+filler+'/'+board, cat_ind)
            cats_out.write(str(cat_ind)+'\n')
            i += 1