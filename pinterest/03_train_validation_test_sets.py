#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 21:34:16 2018

@author: alejandro
"""
from os import chdir

def read_file(file_route):
    file_list = []
    with open(file_route, 'r') as f:
        for line in f:
            file_list.append(int(line.strip()))
    return file_list

def append_to_dic(dictionary, id, els):
    if len(els) == 0:
        return
    for e in els:
        if id in dictionary:
            dictionary[id].append(e)
        else:
            dictionary[id] = [e]

def write_train_files(prefix, dic):
    with open(prefix+'.txt', "w") as f:
        for id in dic.keys():
            for e in dic[id]:
                f.write(str(e[0])+"\n")
            
def write_test_files(prefix, dic):
    with open(prefix+'.txt', "w") as f:
        for user_id in range(274):
            if user_id in dic:
                for e in dic[user_id]:
                    f.write(str(e[0])+" ")
            f.write("\n")

chdir('..')
data_dir = r'data/data/'
sorted_dir = r'data/data/sorted/'

# in
categories_file = data_dir+'all_dataset3_categories.txt'
users_file = data_dir+'all_dataset3_users.txt'
# out
indexes_file = data_dir+'all_dataset3_sorted_by_cat_indexes.txt'

# reads users and cats files and enumerates it
users_list = list(enumerate(zip(read_file(users_file),
                                read_file(categories_file))))
training_per_cats = {}
validation_per_cats = {}
test_per_user = {}

for user_id in range(274):
    user_pins = [x for x in users_list if x[1][0] == user_id]
    for cat_id in range(34):
        # takes the pins that corresponds to a certain cat from the especified user
        cat_pins = [x for x in user_pins if x[1][1] == cat_id]
        list_len = len(cat_pins)

        # splits the user's pins into 3 sets, train, eval and test
        cat_train_ = cat_pins[ 0:int(list_len * 0.6) ]
        cat_validation_ = cat_pins[ int(list_len * 0.6):int(list_len * 0.8) ]
        cat_test_ = cat_pins[ int(list_len * 0.8):list_len ]
        
        # saving the indexes for the train and validation ordered by cat
        append_to_dic(training_per_cats, cat_id, cat_train_)
        append_to_dic(validation_per_cats, cat_id, cat_validation_)
        
        # saving the index for the tests ordered by user
        append_to_dic(test_per_user, user_id, cat_test_)

write_train_files(sorted_dir+r"train_indexes_"   ,  training_per_cats)
write_train_files(sorted_dir+r"validate_indexes_",  validation_per_cats)
write_test_files( sorted_dir+r"tests_indexes_"      ,  test_per_user)