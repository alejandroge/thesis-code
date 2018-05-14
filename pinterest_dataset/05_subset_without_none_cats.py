#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 16:51:08 2018

@author: alejandro
"""

from os import chdir

def read_file_into_list(file_path):
    std_list = []
    with open(file_path, 'r') as items:
        for item in items:
            std_list.append(item.strip())
    return std_list

chdir('..')
data_dir = r'data/pinterest_dataset/'

# In
usernames_list  = r'usernames_list.txt'
categories_list = r'categories_list.txt'
pins_routes     = r'all_pins_routes.txt'
pins_users      = r'all_pins_users.txt'
pins_cats       = r'all_pins_categories.txt'

# Out
ss_pins_routes = r'ss_pins_routes.txt'
ss_pins_users  = r'ss_pins_users.txt'
ss_pins_cats   = r'ss_pins_categories.txt'

# Read whole list of users, cats, routes and descriptions
users_list = read_file_into_list(data_dir+pins_users)
cats_list = read_file_into_list(data_dir+pins_cats)
routes_list = read_file_into_list(data_dir+pins_routes)

# Convert users and cats to numbers
users_list = [int(user_ind) for user_ind in users_list]
cats_list  = [int(cat_ind)  for cat_ind  in cats_list ]

ss_routes_file = open(data_dir+ss_pins_routes, 'w')
ss_users_file  = open(data_dir+ss_pins_users,  'w')
ss_cats_file   = open(data_dir+ss_pins_cats,   'w')

c_none = 0
for u, c, r in zip(users_list, cats_list, routes_list):
    if c == 0:
        c_none += 1
        continue
    ss_routes_file.write(r+'\n')
    ss_users_file.write(str(u)+'\n')
    ss_cats_file.write(str(c)+'\n')

ss_routes_file.close()
ss_users_file.close()
ss_cats_file.close()