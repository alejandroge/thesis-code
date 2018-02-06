#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 16:12:33 2018

@author: Alejandro Guevara
"""
import tensorflow as tf
import collections

data_dir = r'/home/alejandro/Documents/thesis/data/'
users_file = r'users_rel.txt'
cates_file = r'cates_rel.txt'
pinid_file = r'names_rel.txt'
vocab_file = r'vocab_rel_decoded.txt'
vocab      = r'vocab.txt'

def read_data(filename):
    with open(data_dir+filename, 'r') as d:
        data = d.read().split(' ')
    return data

vocabulary = read_data(vocab);
print('Data size', len(vocabulary))

# Builds the dictionary and replace rare words with UNK token.
vocabulary_size = 50000
embedding_size = 128

def build_dataset(words, n_words):
  """Process raw inputs into a dataset."""
  count = [['UNK', -1]]
  count.extend(collections.Counter(words).most_common(n_words - 1))
  dictionary = dict()
  for word, _ in count:
    dictionary[word] = len(dictionary)
  data = list()
  unk_count = 0
  for word in words:
    index = dictionary.get(word, 0)
    if index == 0:  # dictionary['UNK']
      unk_count += 1
    data.append(index)
  count[0][1] = unk_count
  reversed_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
  return data, count, dictionary, reversed_dictionary

data, count, dictionary, reverse_dictionary = build_dataset(vocabulary,
                                                            vocabulary_size)
del vocabulary  # Hint to reduce memory

# Loads feature vectors and labels into lists
def load_data():
    train_labels = []
    train_features = []
    with open(data_dir+cates_file) as c:
        for item in c:
            train_labels.append(int(item.strip('\n')))
    return ( train_features, train_labels )

features, labels = load_data()

word_embeddings = tf.Variable(
        tf.random_uniform([vocabulary_size, embedding_size], -1.0, 1.0))
embedded_word_ids = tf.nn.embedding_lookup(word_embeddings, data)
