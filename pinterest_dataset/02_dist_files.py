#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 16:25:17 2018

@author: Alejandro Guevara

@description: Distribute vocab, users and categories into different files
"""
import html
import json

#data_dir = r'/Users/juancarlos/Documents/data/pinterest_dataset/'
#pins_dir = r'/Users/juancarlos/Documents/data/pinterest/pinterest/'
pins_dir = r'/home/alejandro/Documents/thesis/data/pinterest/'
data_dir = r'/home/alejandro/Documents/thesis/data/pinterest_dataset/'
pins_routes = r'all_pins_routes.txt'
vocab_file = r'vocab_file.txt'

# Reads the whole list of pins
routes_list = []
with open(data_dir+pins_routes, 'r') as pins_list:
    for route in pins_list:
        routes_list.append(route.strip())

with open(data_dir+vocab_file, 'w') as voca_out:
    for route in routes_list:
        user, filler, board, pin = route.split('/')
        board_route = user+'/'+filler+'/'+board
        with open(pins_dir+route+'/pin_dict.txt', 'r') as pin_text:
            pin_json_obj = json.loads(pin_text.read().replace("'", '"').strip())
            html_text = html.unescape(pin_json_obj['description'])
            bytes_text = bytes(html_text, 'utf-8')
            unicode_text = bytes_text.decode(
                'unicode-escape').encode('iso-8859-1').decode('utf-8').lower()
        voca_out.write(unicode_text+'\n')
