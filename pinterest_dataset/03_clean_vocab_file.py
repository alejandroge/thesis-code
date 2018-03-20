#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 17:18:18 2018

@author: Alejandro Guevara
"""
import re
import emoji_unicode
import os
import html

main_dir = r'/Users/juancarlos/Documents/data/pinterest_dataset/'
vocab_rel = r'model_data/vocab_rel.txt'

os.chdir(main_dir)

emoticon_pattern = r"([0-9a-z'\&\-\/\(\)=:;]+)|((?::|;|=)(?:-)?(?:\)|D|P))"
emoji_pattern = emoji_unicode.RE_PATTERN_TEMPLATE

regex = r'[a-z]+|'+emoticon_pattern+'+|'+emoji_pattern+'+'

i = 0
with open(vocab_rel, 'r') as pins_text_list:
    for pin in pins_text_list:
        if(i == 10):
            continue
        dpin = html.unescape(pin.strip())
        b = bytes(dpin, 'utf-8')
        words = b.decode('unicode-escape').encode('iso-8859-1').decode('utf-8').lower()
        print('\n')
        print(words)
        for match in re.finditer(regex, words):
            print(match.group(0))
        i+=1
