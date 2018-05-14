#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 16:11:17 2018

@author: alejandro
"""
from os import chdir

chdir('..')
pins_dir = r'data/pinterest/'
data_dir = r'data/pinterest_dataset/'

# In
pins_cats = r'all_pins_categories.txt'

None_cats_num = 0
pins_num = 0
with open(data_dir+pins_cats, 'r') as pins_cat:
    for cat in pins_cat:
        pins_num += 1
        if int(cat) == 0:
            None_cats_num += 1