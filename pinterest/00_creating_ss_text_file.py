#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 20:32:45 2018

@author: alejandro
"""

from os import chdir
import ast

chdir('..')
pins_dir = r'/media/alejandro/ADATA/pinterest/'
data_dir = r'data/pinterest/'

# In
routes_file = data_dir + r'ss_pins_routes.txt'

# Out
text_file = data_dir + r'ss_pins_text.txt'

with open(text_file, 'w') as text, open(routes_file, 'r') as routes:
    i = 0
    for route in routes:
        i += 1
        route = pins_dir+route.strip('\n').strip('\t')
        with open(route+'/pin_dict.txt', 'r') as pin:
            pin_ob = ast.literal_eval(pin.read())
            pin_text = pin_ob['description'].strip('\n').strip('\t')
            pin_text = pin_text.replace('\n','').replace('\t','').replace('\r', '') + '\n'
            text.write(pin_text)
    print(i)