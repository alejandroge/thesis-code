#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 23:41:15 2018

@author: alejandro
"""

from os import chdir

def count_words(dictionary, words):
    for word in words.split():
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary[word] = 1
    

chdir('..')
data_dir = r'data/data/'

# In
words_file = data_dir+'pins_words.txt'
emo_file   = data_dir+'pins_emoticons.txt'
hash_file  = data_dir+'pins_hashtags.txt'
at_file    = data_dir+'pins_ats.txt'
link_file  = data_dir+'pins_links.txt'

# Out
vocab_file = data_dir+'ss_pins_vocab.txt'

words_dict = {}
# Count words reptition through documents ( pins )
# Words appearing in at least 5 pins, will be added to the vocab file
with open(vocab_file, 'w') as vocab, open(words_file, 'r') as words:
    i = 0
    for line in words:
        i += 1
        count_words(words_dict, line)
    print(i)

sorted_words = sorted(words_dict.items(), key=lambda word: word[1])
sorted_words = list(filter(lambda words: words[1] >= 5, sorted_words))