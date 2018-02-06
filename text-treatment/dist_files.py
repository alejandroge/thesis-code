#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 09:12:52 2017

@author: juancarlos
"""
import os

main_dir = r'/Users/juancarlos/Documents/data/text-treatment/'
pins_info = r'all_pins_text_cat.txt'
not_valid_indexes = r'not_valid_indexes.txt'
users_rel = r'users_rel.txt'
cates_rel = r'cates_rel.txt'
pinid_rel = r'names_rel.txt'
vocab_rel = r'vocab_rel.txt'

os.chdir(main_dir);

not_valid = []
with open(not_valid_indexes, 'r') as input:
    for item in input:
        not_valid += [int(item.strip())]
# The data in the input file will be splitted
# in these four different files
users_data = []
cates_data = []
pinid_data = []
vocab_data = []

i=0
# Data loaded into the lists
with open(pins_info, 'r') as pins:
    for pin in pins:
        i += 1
        if(i-1 in not_valid):
            continue
        elements = pin.split()
        users_data += [elements[0]]
        cates_data += [elements[1]]
        pinid_data += [elements[2]]
        vocab_data += [elements[3:]]

with open(users_rel, 'w') as output:
    for user in users_data:
        output.write(user+'\n');
with open(cates_rel, 'w') as output:
    for cate in cates_data:
        output.write(cate+'\n');
with open(pinid_rel, 'w') as output:
    for pin in pinid_data:
        output.write(pin+'\n');
with open(vocab_rel, 'w') as output:
    for desc in vocab_data:
        output.write(' '.join(desc)+'\n');                   
