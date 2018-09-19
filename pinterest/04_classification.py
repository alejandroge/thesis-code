# -*- coding: utf-8 -*-
"""
Created on Mon May  8 10:59:09 2017

@author: JC
"""
import re
import time
import numpy as np
from nltk.corpus import stopwords
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn import metrics
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from os import chdir
                
def read_data(file):
    data = []
    cachedStopWords = stopwords.words('english')
    with open(file, encoding='utf-8') as content_file:
        for line in content_file:
            line= line.rstrip().lower()
            words = re.findall('[a-záéíóúñ]+',line)
            text = ' '.join(word for word in words if word not in cachedStopWords and len(word)>2 and len(word)<35)
            data.append(text)
    return data

def read_file(file_route):
    file_list = []
    with open(file_route, 'r') as f:
        for line in f:
            file_list.append(line.strip())
    return file_list

def read_simple_indexes_file(file_route):
    file_list = []
    with open(file_route, 'r') as f:
        for line in f:
            file_list.append(int(line.strip()))
    return file_list

def read_list_indexes_file(file_route):
    file_list = []
    with open(file_route, 'r') as f:
        for line in f:
            idxs = line.strip()
            if idxs != '':                    
                file_list.append([int(x) for x in idxs.split()])
            else:
                file_list.append([])
    return file_list

def read_labels_from_indexes(file, indexes_list):
    labels = []
    categories = read_file(r"data/pinterest/ss_pins_{}.txt".format(file))
    for idx in indexes_list:
        labels.append(categories[idx])
    return labels

def read_text_from_indexes(indexes_list):
    texts = []
    pins_text = read_data(r"data/pinterest/pins_eng_words.txt")
    for idx in indexes_list:
        texts.append(pins_text[idx])
    return texts

def read_labels_from_indexes_list(file, indexes_list):
    labels = []
    categories = read_file(r"data/pinterest/ss_pins_{}.txt".format(file))
    for l in indexes_list:
        c = []
        for idx in l:
            c.append(categories[idx])
        labels.append(list(set(c)))
    return labels

def read_text_from_indexes_list(indexes_list):
    texts = []
    pins_text = read_data(r"data/pinterest/pins_eng_words.txt")
    for l in indexes_list:
        t = ''
        for idx in l:
            t += ' ' + pins_text[idx]
        texts.append(t)
    return texts

def recall_at(real_labels, predicted_labels, n):
    scores = []
    for r_labels, p_labels in zip(real_labels, predicted_labels):
        top_probs = { x + 1 for x in p_labels.argsort()[-n:][::-1] }
        r_labels = { int(x) for x in r_labels }
        r_labels.intersection(top_probs)
        scores.append(float(len(r_labels.intersection(top_probs)))/float(
                len(r_labels.union(top_probs))))
        print(scores)
    return sum(scores)/float(len(scores))

# moves to the main directory
chdir('..')
data_dir = r'data/pinterest/'
sorted_dir = r'data/pinterest/sorted/'

# In
data_train_file = sorted_dir+'train_indexes_.txt'
data_val_file = sorted_dir+'validate_indexes_.txt'
data_test_file = sorted_dir+'tests_indexes_.txt'
labels_train_file = sorted_dir+'labels_train.txt'
labels_val_file = sorted_dir+'labels_val.txt'
labels_test_file = sorted_dir+'labels_test.txt'

# Reads the names for the cats and users
cats_label_names = read_file(data_dir+'categories_list.txt')
users_label_names = read_file(data_dir+'usernames_list.txt')

# Reads training, validate and tests indexes
train_indexes = read_simple_indexes_file(data_train_file)
val_indexes   = read_simple_indexes_file(data_val_file)
test_indexes  = read_list_indexes_file(data_test_file)

# Read training data
# For svm there is the parameter C to optimize
corpus_train = read_text_from_indexes(train_indexes)
labels_train = read_labels_from_indexes('categories', train_indexes)
print("Longitud de corpus {}".format(len(corpus_train)))
print("Longitud de labels {}".format(len(labels_train)))
labels_train = np.array(labels_train)

vectorizer = TfidfVectorizer(norm='l2')
data_trans_train = vectorizer.fit_transform(corpus_train)

# Read validation data
corpus_val = read_text_from_indexes(val_indexes)
labels_val = read_labels_from_indexes('categories', val_indexes)
print("Longitud de corpus {}".format(len(corpus_val)))
print("Longitud de labels {}".format(len(labels_val)))
labels_val = np.asarray(labels_val)

data_trans_val = vectorizer.transform(corpus_val)

# Use a validation set to find optimal C
best_acc = 0.0
best_c = 0
c_list = {0.1, 1, 10, 100}
for c in c_list:
    print('Validating model with C = '+str(c))
    clf_svm = svm.SVC(C=c, probability=True).fit(data_trans_train, labels_train)
    predicted_svm = clf_svm.predict_proba(data_trans_val)
    acc = recall_at(labels_val, predicted_svm, 5)
    print('\tAccuracy = '+str(acc))
    if (acc>best_acc):
        best_c = c
        best_acc = acc
print('\n')
print('Best C for the model = '+str(best_c))

#############################################################
# Load training and validation data together
corpus_train = read_text_from_indexes(train_indexes) + read_text_from_indexes(val_indexes)
labels_train = read_labels_from_indexes(
        'categories', train_indexes) + read_labels_from_indexes('categories', val_indexes)
print("Longitud de corpus {}".format(len(corpus_train)))
print("Longitud de labels {}".format(len(labels_train)))

vectorizer = TfidfVectorizer(norm='l2')
data_trans_train = vectorizer.fit_transform(corpus_train)

# Load final test data
corpus_test = read_text_from_indexes_list(test_indexes)
labels_test = read_labels_from_indexes_list('categories', test_indexes)
print("Longitud de corpus {}".format(len(corpus_test)))
print("Longitud de labels {}".format(len(labels_test)))
labels_test = np.array(labels_test)

data_trans_test = vectorizer.transform(corpus_test)

start = time.time()
print("Started fitting modelfor C=", best_c)
clf_svm = svm.SVC(C=best_c, probability=True).fit(data_trans_train, labels_train)
print('Predictions started for C=', best_c)
predicted_svm = clf_svm.predict_proba(data_trans_test)
stop = time.time()

print('\n\n')
print('\nPerformance:')
print(recall_at(labels_test, predicted_svm, 5))
print('\n\n\n')
print('Training + test time = '+str(stop - start))

# metrics.recall_at
# R n P / R U P