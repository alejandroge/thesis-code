# -*- coding: utf-8 -*-
"""
Created on Mon May  8 10:59:09 2017

@author: JC
"""
import re
import time
import numpy as np
from nltk.corpus import stopwords
from sklearn import metrics
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer

def read_label(file, label, label_set):
    with open(file) as content_file:
        for line in content_file:
            category = line.rstrip()
            label.append(label_set.index(category))
                
def read_data(file, data):
    cachedStopWords = stopwords.words('spanish')
    with open(file, encoding='utf-8') as content_file:
        for line in content_file:
            line= line.rstrip().lower()
            words = re.findall('[a-záéíóúñ]+',line)
            text = ' '.join(word for word in words if word not in cachedStopWords and len(word)>2 and len(word)<35)
            data.append(text)

main_dir = 'C:/Users/JC/Documents/UG/Cursos/2018/ene_jun/Mineria de datos/data/fb_posts/'
data_train_file = main_dir+'data_train.txt'
data_val_file = main_dir+'data_val.txt'
data_test_file = main_dir+'data_test.txt'
labels_train_file = main_dir+'labels_train.txt'
labels_val_file = main_dir+'labels_val.txt'
labels_test_file = main_dir+'labels_test.txt'

labels_names = ['juan', 'luis', 'pedro']

# Read training data
# For svm there is the parameter C to optimize
corpus_train = []
labels_train = []
read_data(data_train_file, corpus_train)
read_label(labels_train_file, labels_train, labels_names)
labels_train = np.array(labels_train)

vectorizer = TfidfVectorizer(norm='l2')
data_trans_train = vectorizer.fit_transform(corpus_train)

# Read validation data
corpus_val = []
labels_val = []
read_data(data_val_file, corpus_val)
read_label(labels_val_file, labels_val, labels_names)
labels_val = np.asarray(labels_val)

data_trans_val = vectorizer.transform(corpus_val)

# Use a validation set to find optimal C
best_acc = 0.0
best_c = 0
c_list = {0.1, 1, 10, 100}
for c in c_list:
    print('Validating model with C = '+str(c))
    clf_svm = svm.LinearSVC(C=c).fit(data_trans_train, labels_train)
    predicted_svm = clf_svm.predict(data_trans_val)
    acc = np.mean(labels_val == predicted_svm)
    print('\tAccuracy = '+str(acc))
    if (acc>best_acc):
        best_c = c
        best_acc = acc
print('\n')
print('Best C for the model = '+str(best_c))

# Load training and validation data together
corpus_train = []
labels_train = []
read_data(data_train_file, corpus_train)
read_label(labels_train_file, labels_train, labels_names)
read_data(data_val_file, corpus_train)
read_label(labels_val_file, labels_train, labels_names)
labels_train = np.array(labels_train)

vectorizer = TfidfVectorizer(norm='l2')
data_trans_train = vectorizer.fit_transform(corpus_train)

# Load final test data
corpus_test = []
labels_test = []
read_data(data_test_file, corpus_test)
read_label(labels_test_file, labels_test, labels_names)
labels_test = np.array(labels_test)

data_trans_test = vectorizer.transform(corpus_test)

start = time.time()
clf_svm = svm.LinearSVC(C=best_c).fit(data_trans_train, labels_train)
predicted_svm = clf_svm.predict(data_trans_test)
stop = time.time()

print('\n\n')
print('Accuracy = '+str(np.mean(labels_test == predicted_svm)))
print('\nPerformance:')
print(metrics.classification_report(labels_test, predicted_svm, target_names=labels_names))
print('\nConfusion matrix:')
print(metrics.confusion_matrix(labels_test, predicted_svm))
print('\n\n\n')
print('Training + test time = '+str(stop - start))