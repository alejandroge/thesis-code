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
from sklearn.neighbors import KNeighborsClassifier
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
# For k-nn there is the parameter k to optimize
corpus_train = []
labels_train = []
read_data(data_train_file, corpus_train)
read_label(labels_train_file, labels_train, labels_names)
labels_train = np.array(labels_train)
                                 # esto es una ele
vectorizer = TfidfVectorizer(norm='l2')
data_trans_train = vectorizer.fit_transform(corpus_train)

# Read validation data
corpus_val = []
labels_val = []
read_data(data_val_file, corpus_val)
read_label(labels_val_file, labels_val, labels_names)
labels_val = np.array(labels_val)

data_trans_val = vectorizer.transform(corpus_val)

# Use a validation set to find optimal K
best_acc = 0.0
best_k = 0
k_list = [1, 3, 5, 10]
for k in k_list:
    print('Validating model with k = '+str(k))
    clf_knn = KNeighborsClassifier(n_neighbors=k, algorithm = 'brute', metric='cosine').fit(data_trans_train, labels_train)
    predicted_knn = clf_knn.predict(data_trans_val)
    acc = np.mean(labels_val == predicted_knn)
    print('\tAccuracy = '+str(acc))
    if (acc>best_acc):
        best_k = k
        best_acc = acc
print('\n')
print('Best k for the model = '+str(best_k))

# Load training and validation data together
corpus_train = []
labels_train = []
read_data(data_train_file, corpus_train)
read_label(labels_train_file, labels_train, labels_names)
read_data(data_val_file, corpus_train)
read_label(labels_val_file, labels_train, labels_names)
labels_train = np.array(labels_train)
                                # esto es otra ele
vectorizer = TfidfVectorizer(norm='l2')
data_trans_train = vectorizer.fit_transform(corpus_train)

# Load final test data
corpus_test = []
labels_test = []
read_data(data_test_file, corpus_test)
read_label(labels_test_file, labels_test, labels_names)
labels_test = np.array(labels_test)

data_trans_test = vectorizer.transform(corpus_test)

# Train and test the model
start = time.clock()
clf_knn = KNeighborsClassifier(n_neighbors=best_k, algorithm = 'brute', metric='cosine').fit(data_trans_train, labels_train)
predicted_knn = clf_knn.predict(data_trans_test)
stop = time.clock()

print('\n\n')
print('\nAccuracy = '+str(np.mean(labels_test == predicted_knn)))
print('\nPerformance:')
print(metrics.classification_report(labels_test, predicted_knn, target_names=labels_names))
print('\nConfusion matrix:')
print(metrics.confusion_matrix(labels_test, predicted_knn))
print('\nTraining + test time = '+str(stop - start))