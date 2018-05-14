#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 16:21:03 2018

@author: alejandro
"""

from os import chdir
from collections import defaultdict

chdir('..')
pins_dir = r'data/pinterest/'
data_dir = r'data/pinterest_dataset/'

# In
usernames_list = r'usernames_list.txt'
pins_cats  = r'all_pins_categories.txt'
pins_users = r'all_pins_users.txt'

# Read whole list of users
users_list = []
with open(data_dir+pins_users, 'r') as users:
    for user in users:
        users_list.append(int(user.strip()))

# Read whole lists of cats
cats_list = []
with open(data_dir+pins_cats, 'r') as cats:
    for cat in cats:
        cats_list.append(int(cat.strip()))
        
# Create a lookup-table using key as user index retrieved from usernames_list
# file order and value as username 
users_dict = defaultdict(int)
with open(data_dir+usernames_list, 'r') as users:
    for ind, user in enumerate(users.read().split()):
        users_dict[ind] = user

curr_usr = -1
num_pins = 0
none_cat_pins = 0
useless_usrs = 0
for user, cat in zip(users_list, cats_list):
    if user != curr_usr:
        print("{} has {} pins\n{} of them have 'None' cat\n".format(
            users_dict[curr_usr], num_pins, none_cat_pins))
        if num_pins == none_cat_pins:
            useless_usrs += 1
        num_pins = 0
        none_cat_pins = 0
        curr_usr = user
    if cat == 0:
        none_cat_pins += 1
    num_pins += 1