# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 11:21:51 2018

@author: JC
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import normalize
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from nltk.corpus import stopwords
from scipy.sparse import hstack
import numpy as np

def my_tokenizer(s):
    return s.split()

def read_labels(file, prob):
    label = []
    with open(file) as content_file:
        for line in content_file:
            clase = line.rstrip()
            if prob == 'age':
                if clase == '18-24':
                    label.append(0)
                elif clase == '25-34':
                    label.append(1)
                elif clase == '35-49':
                    label.append(2)
                else:
                    label.append(3)
            else:
                if clase == 'M':
                    label.append(0)
                else:
                    label.append(1)
    return label

def read_text_data_with_emos(lang, text_file, emo_file):
    data = []
    if lang == 'spa':
        cachedStopWords = stopwords.words('spanish')
    elif lang == 'eng':
        cachedStopWords = stopwords.words('english')
    with open(text_file, encoding='utf-8') as text_content, open(emo_file, encoding='utf-8') as emo_content:
        for text_line, emo_line in zip(text_content, emo_content):
            words = text_line.rstrip().split()
            text = ' '.join([word for word in words if len(word)>2 and len(word)<35 and word not in cachedStopWords])
            text += ' '+emo_line.rstrip()
            data.append(text)
    return data

def read_text_data(lang, file):
    data = []
    if lang == 'spa':
        cachedStopWords = stopwords.words('spanish')
    elif lang == 'eng':
        cachedStopWords = stopwords.words('english')
    with open(file, encoding='utf-8') as content_file:
        for line in content_file:
            words = line.rstrip().split()
            text = ' '.join([word for word in words if len(word)>2 and len(word)<35 and word not in cachedStopWords])
            data.append(text)
    return data

def read_extra_data(n, file):
    data = []
    with open(file, encoding='utf-8') as content_file:
        for line in content_file:
            tokens = line.rstrip().split()
            #ratio = len(tokens)/n
            ratio = len(tokens)
            data.append(ratio)
    return data

main_dir = 'C:/Users/JC/Documents/CodeandData/datasets/2018_twitter_age_gender/'
lang = 'eng'
prob = 'gender'
label_file = main_dir+'clef2015_'+lang+'_'+prob+'.txt'
words_file = main_dir+'clef2015_'+lang+'_words.txt'
hashs_file = main_dir+'clef2015_'+lang+'_hashtags.txt'
ats_file = main_dir+'clef2015_'+lang+'_ats.txt'
emo_file = main_dir+'clef2015_'+lang+'_emoticons.txt'
links_file = main_dir+'clef2015_'+lang+'_links.txt'

labels_list = read_labels(label_file, prob)
corpus = []
corpus = read_text_data(lang, words_file)
corpus = read_text_data_with_emos(lang, words_file, emo_file)

vec = TfidfVectorizer(min_df=2, norm='l2', analyzer = 'word', tokenizer=my_tokenizer)
corpus_tfidf = vec.fit_transform(corpus)
labels = np.asarray(labels_list)

clf_nb = MultinomialNB()
clf_svm = svm.LinearSVC(C=1)
clf_log = LogisticRegression(C=1, penalty='l2', solver='liblinear')
clf_rdf = RandomForestClassifier()

skf = StratifiedKFold(n_splits=10)
scores = cross_val_score(clf_log, corpus_tfidf, labels, cv=skf)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

n_text = len(corpus)
hashs = read_extra_data(n_text, hashs_file)
ats = read_extra_data(n_text, ats_file)
emoticons = read_extra_data(n_text, emo_file)
links = read_extra_data(n_text, links_file)

feat = [(a,b,c,d) for (a,b,c,d) in zip(hashs,ats,emoticons,links)]
feat = [list(a) for a in feat]

feat = np.array(feat, dtype='float')
feat = normalize(feat, norm='l2', axis=1)
scores = cross_val_score(clf_nb, feat, labels, cv=skf)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

#feat_tot = hstack([corpus_tfidf, feat])
#feat_tot = normalize(feat_tot, norm='l2', axis=1)
#scores = cross_val_score(clf_nb, feat_tot, labels, cv=skf)
#print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

#voc_file = main_dir+'vocabulary.txt'
#with open(voc_file,'w') as voc_writer:
#    for word in vec.vocabulary_:
#        voc_writer.write(word+'\n')


#for train_index, test_index in skf.split(corpus_tfidf, labels):
#    data_train, data_test = corpus_tfidf[train_index], corpus_tfidf[test_index]
#    labels_train, labels_test = labels[train_index], labels[test_index]
#    break