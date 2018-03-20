#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 10:05:50 2017

@author: juancarlos
"""

import os
import re

# get the index of an element in a list
def get_index(element, list):
    i = 0
    for i in range(0, len(list)):
        if(list[i] == element):
            return i
    return None
        

# it saves a list to a file
def save_to_file(list, file_name):
    with open(file_name, 'w') as output:
        for item in list:
            output.write(item+ '\n')

# Is used to split the data in each row of the nonempty_boards file
def split_board_data(board):
    b_info = board.strip('\n').split()
    route = b_info[0].split('/')
    user = route[0]
    board_name = route[2]
    cat = b_info[1]
    n_pins = int(b_info[2])
    return [user, board_name, cat, n_pins]
    
# Is used to retrieve data from data file
def read_data(file):
    boards = []
    cats = set()
    users = set()
    n_pins = 0
    with open(file, 'r') as boards_cat:
        for line in boards_cat:
            items = split_board_data(line)
            boards += [items]
            cats.add(items[2])
            users.add(items[0])
            n_pins += items[3]
        return boards, sorted(list(cats)), sorted(list(users)), n_pins            

main_dir = r'/Users/juancarlos/Documents/data/categories'
data_dir = r'/Users/juancarlos/Documents/data/pinterest'
output_dir = r'/Users/juancarlos/Documents/data/text-treatment/'
os.chdir(main_dir)

data_file = r'nonempty_boards.txt'
pin_file = r'pin_dict.txt'
output_file = r'all_pins_routes.txt'
user_output_file = r'all_users.txt'
categories_output_file = r'all_categories.txt'
not_valid_indexes = r'not_valid_indexes.txt'

# it retrieves the info of each line of the data file
# categories and users are sorted list
# boards keeps the order readed in the data file (user sorted)
boards, categories, users, n_pins = read_data(data_file)

save_to_file(users, user_output_file)
save_to_file(categories, categories_output_file)

print('** Data info: There is ' + str(len(boards)) + ' boards ready to be processed.')
print('** Data info: There is ' + str(len(users)) + ' different users.')
print('** Data info: There is ' + str(len(categories)) + ' different categories.')
print('** Data info: There is ' + str(n_pins) + ' different pins.')

regex = re.compile(r'[0-9]+')
c_pins = 0  

with open(not_valid_indexes, 'w') as ind:
    with open(output_dir+output_file, 'w') as output:
        for user in users:
            u_index = get_index(user, users)
            for cat in categories:
                c_index = get_index(cat, categories)
                for board in boards:
                    if(board[0] != user):
                        continue
                    if(board[2] != cat):
                        continue
                    board_route = '/'.join([data_dir, 'pinterest',user, 'per_board', board[1]])
                    os.chdir(board_route)
                    pins = list(filter(regex.search, os.listdir()))
                    for pin in pins:
                        if (pin_file in os.listdir(pin)):
                            c_pins += 1
                            # report as format (user, category, pin_route, pin_text)
                            if not os.path.isfile('./'+pin+'/pin_closeup_image.jpg'):
                                print(board_route+'/'+pin)
                                ind.write(str(c_pins-1)+'\n')
                                continue
                            pin_route = '/'.join([board_route, pin])
                            print ("\r ... Progress: "+str(c_pins)+' out of '+str(n_pins)+' '+str(int(c_pins/n_pins*100))+'% ...', end="")
                            output.write(pin_route + '\n')