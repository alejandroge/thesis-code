#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  19 22:53:05 2018

@author: Alejandro Guevara
"""
from os import chdir

# Paths names
#data_dir = r'/Users/juancarlos/Documents/data/pinterest_dataset/'
#pins_dir = r'/Users/juancarlos/Documents/data/pinterest/pinterest/'
pins_dir = r'data/pinterest/'
data_dir = r'data/pinterest_dataset/'
pins_routes = r'all_pins_routes.txt'

chdir('..')

# Reads the whole list of pins
routes_list = []
with open(data_dir+pins_routes, 'r') as pins_list:
    for route in pins_list:
        routes_list.append(route.strip())

i = 0
boards_dict = {}
boards_cat_dict = {}
board_route = ''

for route in routes_list:
    user, filler, board, pin = route.split('/')
    if not board_route == user+'/'+board:
        board_route = user+'/'+board
        i += 1

print(i)