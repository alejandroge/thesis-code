#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  15 5:04:05 2018

@author: Alejandro Guevara
"""

from os import listdir
from os.path import isdir, join, isfile

absPaths   = []
boardsList = [] #Storage the boards
pinsList   = [] #Storage the pins
usernames  = []
i = 0

#Paths names
#data_dir = r'/Users/juancarlos/Documents/data/pinterest_dataset/'
#pins_dir = r'/Users/juancarlos/Documents/data/pinterest/pinterest/'
pins_dir = r'/home/alejandro/Documents/thesis/data/pinterest/'
data_dir = r'/home/alejandro/Documents/thesis/data/pinterest_dataset/'
pins_routes = r'all_pins_routes.txt'
users_w_ga = r'users_n_g.txt'

#Open file with the names of the users
with open(data_dir+users_w_ga) as users:
    for user in users.read().split():
        usernames.append(user.strip())

with open(data_dir+pins_routes, 'w') as outfile:
    #Iterate over the list of usernames
    for user in usernames:
        #In each iteration change the variable "user" 
        completePath = pins_dir + user + "/per_board/"
        if not isdir(completePath):
            print(user)
            continue
        #Storage all the boards of the user in "folderList"
        folderList = [folder for folder in listdir(completePath) if isdir(
                join(completePath, folder))]
        #Open each board 
        for board in folderList:
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
