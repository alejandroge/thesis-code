    #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 16:12:33 2018

@author: Alejandro Guevara
"""
import tensorflow as tf
import collections
import argparse
import pdb
from functools import reduce

data_dir   = r'/home/alejandro/Documents/thesis/data/'
users_file = r'users_rel.txt'
cates_file = r'cates_rel.txt'
pinid_file = r'names_rel.txt'
vocab_file = r'vocab_cdecoded.txt'
vocab      = r'vocab.txt'

delim = 100

parser = argparse.ArgumentParser()
parser.add_argument('--batch_size', default=100, type=int, help='batch size')
parser.add_argument('--train_steps', default=1000, type=int,
                    help='number of training steps')

def read_data(filename):
    with open(data_dir+filename, 'r') as d:
        data = d.read().split(' ')
    return data

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

# Loads feature vectors and labels into lists
def load_data(dictionary, embeddings):
    print("**** Loading features and labels.")
    train_labels = []
    train_features = []
    with open(data_dir+vocab_file) as v:
        i=0
        for line in v:
            sum = reduce( (lambda x, y: x + y) ,
                [embeddings[dictionary[idx]] for idx in line.split(' ')
                                             if idx in dictionary.keys() ] )
            i += 1
            train_features.append(sum/i)
            if(i == delim):
                break;
    with open(data_dir+cates_file) as c:
        i=0
        for item in c:
            i += 1
            train_labels.append(int(item.strip('\n')))
            if(i == delim):
                break;
    return ( train_features, train_labels )

def train_input_fn(features, labels, batch_size):
    """An input function for training"""
    # Convert the inputs to a Dataset.
    dataset = tf.data.Dataset.from_tensor_slices((dict(zip(labels, features))))

    # Shuffle, repeat, and batch the examples.
    dataset = dataset.shuffle(1000).repeat().batch(batch_size)

    # Return the read end of the pipeline.
    return dataset.make_initializable_iterator().get_next()

def main(argv):
    args = parser.parse_args(argv[1:])

    vocabulary = read_data(vocab)
    print('Data size', len(vocabulary))

    # Builds the dictionary and replace rare words with UNK token.
    vocabulary_size = 50000
    embedding_size = 128

    data, count, dictionary, reverse_dictionary = build_dataset(vocabulary,
                                                                vocabulary_size)
    del vocabulary  # Hint to reduce memory

    # Computes embeddings for each word
    word_embeddings = tf.Variable(
    tf.random_uniform([vocabulary_size, embedding_size], -1.0, 1.0))
    embedded_word_ids = tf.nn.embedding_lookup(word_embeddings, data)

    features, labels = load_data(dictionary, embedded_word_ids)

    embedding_column = tf.feature_column.embedding_column(
    categorical_column=features,
    dimension=embedding_size)

    # Build 2 hidden layer DNN with 10, 10 units respectively.
    classifier = tf.estimator.DNNClassifier(
        feature_columns=embedding_column,
        hidden_units=[10, 10],
        n_classes=len(labels),
        model_dir='models/DNN')

    # Train the Model.
    classifier.train(
        input_fn=lambda:train_input_fn(features, labels,
                                                 args.batch_size),
        steps=args.train_steps)

    pdb.set_trace()

if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run(main)
