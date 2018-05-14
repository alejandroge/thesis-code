#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 17:34:25 2018

@author: alejandro

@description: This module retrieves useful statistics to better understand the
              data we are working with
"""
from os import chdir
from collections import defaultdict

chdir('..')
data_dir = r'data/pinterest_dataset/'

# In
usernames_list = r'usernames_list.txt'
categories_list = r'categories_list.txt'
pins_routes = r'all_pins_routes.txt'
pins_users = r'all_pins_users.txt'
pins_cats = r'all_pins_categories.txt'
pins_text = r'all_pins_text.txt'

# Out
dataset_statistics= r'dataset_statistics.txt'

# Get users statistics

# Create a lookup-table using key as user index retrieved from usernames_list
# file order and value as username 
users_dict = defaultdict(int)
with open(data_dir+usernames_list, 'r') as users:
    for ind, user in enumerate(users.read().split()):
        users_dict[ind] = user
        
# Create user's index histogram from 'all_pins_users.txt' file
with open(data_dir+pins_users, 'r') as user_indexes_list:
    for user_index in user_indexes_list:
        user_index_num = int(user_index.strip())
        

