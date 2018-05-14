#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  15 5:04:05 2018

@author: Alejandro Guevara

@description: This module returns the list of pins that are going to be used
              as dataset for the model, based on the provided selected users
              lists, and the existence of pin image and text.
"""

from os import listdir, chdir
from os.path import isdir, join, isfile

chdir('..')
pins_dir = r'data/pinterest/'
data_dir = r'data/pinterest_dataset/'

# In
usernames_list = r'usernames_list.txt'

# Out
pins_routes = r'all_pins_routes.txt'

# Load users list from 'usernames_list' file
users_list  = []
with open(data_dir+usernames_list, 'w') as users:
    for user in users.read().split():
        users_list.append(user.strip())
        
i = 0
# Open ‘all_pins_routes.txt’ file as output
with open(data_dir+pins_routes, 'w') as outfile:
    for user in users_list:
        p = 0
        completePath = pins_dir + user + "/per_board/"
        if not isdir(completePath):
            continue
        # Get a list with all directories in the corresponding
        # ‘per_board’ directory, each one represents a board
        boards_list = [folder for folder in listdir(completePath) if isdir(
                join(completePath, folder))]
        for board in boards_list:
            # Get a list with all directories, each one represents a pin
            pins_list = [folder for folder in listdir(completePath+board) if 
                         isdir(join(completePath+board, folder))]
            for pin in pins_list:
                # If ‘pin_closeup_image’ doesn’t exists, continue to next pin
                if not isfile(completePath+board+"/"+pin+'/pin_closeup_image.jpg'):
                    continue
                # If ‘pin_dict’ doesn’t exists, continue to next pin
                if not isfile(completePath+board+"/"+pin+'/pin_dict.txt'):
                    continue
                i += 1; p += 1
                # Else, write pin route to ‘all_pins_routes.txt’ file
                outfile.write(user+'/per_board/'+board+"/"+pin+"\n")
        if(p == 0):
            continue
    
