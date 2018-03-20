#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 16:39:22 2018

@author: luismiguells
"""


import re
#instalar con pip install emoji-unicode
import emoji_unicode

#Encuentra los emoticons junto con texto
emoticon_pattern = r"([0-9A-Za-z'\&\-\/\(\)=:;]+)|((?::|;|=)(?:-)?(?:\)|D|P))"

emoji_pattern = emoji_unicode.RE_PATTERN_TEMPLATE

#Encuentra emojis junto con texto
regex = r'[A-z]+|'+emoticon_pattern+'+|'+emoji_pattern+'+'
texto = "hola si. mi :(:) vida ❤holi"
#texto = "claro que si =) :9"

for match in re.finditer(regex, texto):
    print(match.group(0))



