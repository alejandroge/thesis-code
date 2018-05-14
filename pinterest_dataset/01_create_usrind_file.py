#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 16:49:42 2018

@author: alejandro

@description: The module returns 1-to-1 correspondence to ‘all_pins_routes.txt’
              list of user indexes. User indexes correspond directly to its 
              position in user lists file.
"""

from os import chdir
from os.path import isfile
from collections import defaultdict

chdir('..')
pins_dir = r'data/pinterest/'
data_dir = r'data/pinterest_dataset/'

# In
usernames_list = r'usernames_list.txt'
pins_routes = r'all_pins_routes.txt'

# Out
pins_users = r'all_pins_users.txt'

# Create a lookup-table using key as username and value as user index 
# retrieved from usernames_list file order
users_dict = defaultdict(int)
with open(data_dir+usernames_list, 'r') as users:
    for ind, user in enumerate(users.read().split()):
        users_dict[user] = ind

# Load routes list from file
routes_list = []
with open(data_dir+pins_routes, 'r') as pins_list:
    for route in pins_list:
        routes_list.append(route.strip())

# Open ‘all_users_ind.txt’ file as output
with open(data_dir+pins_users, 'w') as users_out:
    for route in routes_list:
        # Get username by splitting the route to its elements
        user, filler, board, pin = route.split('/')
        # Get owner user index using lookup-table
        user_index = users_dict[user]
        # Write owner user to ‘all_users_ind.txt’
        users_out.write(str(user_index)+'\n')
# Close ‘all_users_ind.txt’

