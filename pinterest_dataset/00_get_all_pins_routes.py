#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  15 5:04:05 2018

@author: Alejandro Guevara
"""

from os import listdir, chdir
from os.path import isdir, join, isfile

pins_list   = []
usernames  = []
i = 0

#Paths names
#data_dir = r'/Users/juancarlos/Documents/data/pinterest_dataset/'
#pins_dir = r'/Users/juancarlos/Documents/data/pinterest/pinterest/'
chdir('..')
pins_dir = r'data/pinterest/'
data_dir = r'data/pinterest_dataset/'
pins_routes = r'all_pins_routes.txt'
users_ga = r'users_n_g.txt'

# Create a list with user's names
with open(data_dir+users_ga) as users:
    for user in users.read().split():
        usernames.append(user.strip())

with open(data_dir+pins_routes, 'w') as outfile:
    for user in usernames:
        completePath = pins_dir + user + "/per_board/"
        if not isdir(completePath):
            print(user)
            continue
        #Storage all the boards of the user in "folderList"
        boards_list = [folder for folder in listdir(completePath) if isdir(
                join(completePath, folder))]
        #Open each board 
        for board in boards_list:
            #Add every pin to a new list
            pinsList = [folder for folder in listdir(completePath+board) if isdir(
                    join(completePath+board, folder))]
            for pin in pinsList:
                if not isfile(completePath+board+"/"+pin+'/pin_closeup_image.jpg'):
                    continue
                if not isfile(completePath+board+"/"+pin+'/pin_dict.txt'):
                    continue
                i += 1
                outfile.write(user+'/per_board/'+board+"/"+pin+"\n")
