#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  15 5:04:05 2018

@author: Alejandro Guevara
"""

from os import listdir, chdir
from os.path import isdir, join, isfile

chdir('..')
pins_dir = r'data/pinterest/'
data_dir = r'data/pinterest_dataset/'
pins_routes = r'all_pins_routes.txt'
usernames_list = r'usernames_list.txt'

# Create a list with user's names
usernames  = []
with open(data_dir+usernames_list) as users:
    for user in users.read().split():
        usernames.append(user.strip())

i = 0
with open(data_dir+pins_routes, 'w') as outfile:
    for user in usernames:
        p = 0
        completePath = pins_dir + user + "/per_board/"
        if not isdir(completePath):
            continue
        #Storage all the boards of the user in "folderList"
        boards_list = [folder for folder in listdir(completePath) if isdir(
                join(completePath, folder))]
        #Open each board 
        for board in boards_list:
            #Add every pin to a new list
            pins_list = [folder for folder in listdir(completePath+board) if isdir(
                    join(completePath+board, folder))]
            for pin in pins_list:
                if not isfile(completePath+board+"/"+pin+'/pin_closeup_image.jpg'):
                    continue
                if not isfile(completePath+board+"/"+pin+'/pin_dict.txt'):
                    continue
                i += 1; p += 1
                outfile.write(user+'/per_board/'+board+"/"+pin+"\n")
        if(p == 0):
            continue
    
