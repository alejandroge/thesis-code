# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 18:18:26 2018

@author: Alejandro Guevara
"""
from os import chdir
from os.path import isfile
import html, json

chdir('..')
pins_dir = r'data/pinterest/'
data_dir = r'data/pinterest_dataset/'

# In
pins_routes = r'all_pins_routes.txt'

# Out
pins_text = r'all_pins_text.txt'

# Reads the whole list of pins routes
routes_list = []
with open(data_dir+pins_routes, 'r') as pins_list:
    for route in pins_list:
        routes_list.append(route.strip())

error_routes = []; i = 0
with open(data_dir+pins_text, 'w') as out_text:
    for route in routes_list:
        if not isfile(pins_dir+route+'/pin_dict.txt'):
            error_routes.append(route)
            continue
        with open(pins_dir+route+'/pin_dict.txt', 'r') as pin_dict:
            json_text = pin_dict.read().replace("'", '"').strip()
            bytes_text = bytes(json_text, 'utf-8')
            unescaped_unicode_text = bytes_text.decode(
                'unicode-escape').encode('iso-8859-1').decode('utf-8')
            json_obj = json.loads(unescaped_unicode_text, strict=False)
            pin_descr = json_obj['description']
        i += 1
        out_text.write(pin_descr+'\n')