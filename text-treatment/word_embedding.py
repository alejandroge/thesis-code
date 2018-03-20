#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 16:12:33 2018

@author: Alejandro Guevara
"""
import tensorflow as tf

data_dir   = r'/home/alejandro/Documents/thesis/data/'
users_file = r'users_rel.txt'
cates_file = r'cates_rel.txt'
pinid_file = r'names_rel.txt'
vocab_file = r'vocab_cdecoded.txt'
vocab      = r'vocab.txt'

def read_data(filename):
    with open(data_dir+filename, 'r') as d:
        data = d.read().split(' ')
    return data

data = read_data(vocab_file)
print(len(data))