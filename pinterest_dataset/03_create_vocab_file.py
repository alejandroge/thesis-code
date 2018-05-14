#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 16:34:32 2018

@author: alejandro
"""
import html
import ast
from os import chdir

chdir('..')
#pins_dir = r'data/pinterest/'
pins_dir = r'/media/alejandro/LMData/pinterest/'
data_dir = r'data/pinterest_dataset/'

# In
pins_routes = r'ss_pins_routes.txt'

# Out
pins_text_outfile = r'ss_pins_text.txt'
pins_text_file    = r'pin_dict.txt'

# Read the whole list of pins routes
routes_list = []
with open(data_dir+pins_routes, 'r') as pins_list:
    for route in pins_list:
        routes_list.append(route.strip())

i = 0
err = 0
with open(data_dir+pins_text_outfile, 'w') as voca_out:
    for route in routes_list:
        user, filler, board, pin = route.split('/')
        board_route = user+'/'+filler+'/'+board
        with open(pins_dir+route+'/pin_dict.txt', 'r') as pin_text:
            data_obj = ast.literal_eval(pin_text.read().strip())
            html_text = html.unescape(data_obj['description'])
            try:
                pin_description = html_text.encode().decode(
                        'unicode-escape').replace("\n", " ")
            except:
                pin_description = ''
                err += 1
            #bytes_text = bytes(html_text, 'utf-8')
            #pin_description = bytes_text.decode(
            #    'unicode-escape').encode('iso-8859-1').decode('utf-8')
        voca_out.write(pin_description+'\n')
        i += 1