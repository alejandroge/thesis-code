# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 21:51:49 2018

@author: Alejandro Guevara
"""
from os import listdir, chdir
from os.path import isdir, join, isfile
from collections import defaultdict

chdir('..')
pins_dir = r'data/pinterest/'
data_dir = r'data/pinterest_dataset/'
usernames_list = r'usernames_list.txt'
categories_list = r'categories_list.txt'

# Create a list with user's names
usernames  = []
with open(data_dir+usernames_list) as users:
    for user in users.read().split():
        usernames.append(user.strip())

categories_hist = defaultdict(int)
for user in usernames:
    completePath = pins_dir + user + "/per_board/"
    if not isdir(completePath):
        continue
    #Storage all the boards of the user in "folderList"
    boards_list = [folder for folder in listdir(completePath) if isdir(
            join(completePath, folder))]
    #Open each board 
    for board in boards_list:
        if not isfile(completePath+board+'/board_category.txt'):
            categories_hist['None'] += 1
            continue
        with open(completePath+board+'/board_category.txt', 'r') as b_cat:
            category = b_cat.read().strip()
            if category == '':
                categories_hist['None'] += 1
            else:
                categories_hist[category] += 1
                    
with open(data_dir+categories_list, 'w') as outfile:
    for cat in sorted(categories_hist):
        outfile.write(cat+'\n')