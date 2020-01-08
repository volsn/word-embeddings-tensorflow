import os
import sys
import numpy as np

import pickle

from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

from nltk.stem import PorterStemmer

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from keras.preprocessing.text import Tokenizer, one_hot
from keras.preprocessing.sequence import pad_sequences
from keras import layers, Sequential
from keras.utils import to_categorical
from keras.initializers import Constant

import pandas as pd

BASE_DIR = ''
GLOVE_DIR = BASE_DIR
TEXT_DATA_DIR = os.path.join(BASE_DIR, '20_newsgroup')
MAX_SEQUENCE_LENGTH = 200
MAX_NUM_WORDS = 1000
EMBEDDING_DIM = 100
VALIDATION_SPLIT = 0.2

dataset = pd.read_csv('dataset_short.txt')

texts = dataset.text.values.astype('str')
labels = dataset.category.values.astype('str')
labels_index = list(np.unique(dataset.category.values))


with open('tokenizer.pickle', 'rb') as f:
    tokenizer = pickle.load(f)
    
sequences = tokenizer.texts_to_sequences(texts)
data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)

le = LabelEncoder()
labels = le.fit_transform(labels)
labels = to_categorical(labels)


X_train, X_test, y_train, y_test \
    = train_test_split(data, labels, test_size=0.2, random_state=42)

X_train, X_val, y_train, y_val \
    = train_test_split(X_train, y_train, test_size=0.2, random_state=42)


with open('embeddings.pickle', 'rb') as f:
    embedding_matrix = pickle.load(f)
    
"""

num_words = min(MAX_NUM_WORDS, len(word_index) + 1)
embedding_matrix = np.zeros(shape=(num_words, EMBEDDING_DIM))
for word, i in word_index.items():
    if i >= MAX_NUM_WORDS:
        continue
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector

"""


model = Sequential([
    layers.Embedding(
        num_words,
        EMBEDDING_DIM,
        input_shape=(MAX_SEQUENCE_LENGTH,),
        embeddings_initializer=Constant(embedding_matrix),
        input_length=MAX_SEQUENCE_LENGTH,
        trainable=False
    ),
    layers.Conv1D(128, 5, activation='relu'),
    layers.MaxPooling1D(5),
    layers.Conv1D(128, 5, activation='relu'),
    layers.MaxPooling1D(5),
    layers.Conv1D(128, 5, activation='relu'),
    layers.GlobalMaxPooling1D(),
    layers.Dense(128, activation='relu'),
    layers.Dense(len(labels_index), activation='softmax')
])

model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['acc'])

model.fit(X_train, y_train,
          batch_size=32,
          epochs=10,
          verbose=1,
          validation_data=(X_val, y_val))

loss, acc = model.evaluate(X_test, y_test)
print('Accuracy on test dataset is', acc)

model.save('classifier.hdf5')
