#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 09:36:40 2017

@author: juancarlos
"""

import os
import html

main_dir = r'/Users/juancarlos/Documents/data/text-treatment/'
users_rel = r'users_rel.txt'
cates_rel = r'cates_rel.txt'
pinid_rel = r'names_rel.txt'
vocab_rel = r'vocab_rel.txt'
output = r'vocab.txt'

os.chdir(main_dir)

i = 1
with open(output, 'w') as out:
    with open(vocab_rel, 'r') as vocab:
        for line in vocab:
            dline = html.unescape(line.strip())
            b = bytes(dline, 'utf-8')
            words = b.decode('unicode-escape').encode('iso-8859-1').decode('utf-8').lower()
            out.write(words+' ')
            i += 1
        