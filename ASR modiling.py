# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yAVSeHnubEUO-o61ki1GvXnSWokuGz-q
"""

import os
from scipy.io import wavfile
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

!pip install keras
!pip install utils
!pip insatall mfcc
!pip install python.speech.features

from keras.layers import Conv2D, MaxPool2D,Flatten, LSTM
from keras.layers import Dropout, Dense, TimeDistributed
from keras.models import Sequential
from tensorflow.keras.utils import to_categorical 
from sklearn.utils.class_weight import compute_class_weight

from tqdm import tqdm
from python_speech_features import mfcc

df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Medical Speech, Transcription, and Intent/overview-of-recordings.csv')

def build_rand_feat():
  X = []
  y = []
  _min, _max = float('inf'), -float('inf')
  for _ in tqdm(range(n_samples)):
    rand_class = np.random.choice(class_dist.index, p=prob_dist)
    file = np.random.choice(df[df.label==rand_class].index)
    rate, wav = wavfile.read('clean/'+file)
    label = df.at[file, 'label']
    rand_index=np.random.randint(0, wav.shape[0]-config.step)
    sample = wav[rand_index:rand_index+config.step]
    X_sample = mfcc (sample, rate, 
                     numcep=config.nfeat,nfilt=config.nfilt, nfft=config.nfft).T
    _min = min(np.amin(X_sample), _min)
    _max = max(np.amax(X_sample), _max)
    X.append(X_sample if config.mode == 'conv' else X_sample.T)
    y.append(classes.index(label))
  X,y = np.array(X), np.array(y)
  X  (X - _min) / (_max - _min)
  if config.mode == 'conv':
     X = X.reshape(X.shape[0], X.shape[1], X.shape[2], 1)
  elif config.mode == 'time':
     X = X.reshape(X.shape[0], X.shape[1], X.shape[2])
  y = to_categorical(y, num_classes=39)
  return X, y

!pip install tensorflow

def get_conv_model():
  model = Sequential()
  model.add(Conv2D(16, (3,3), activation='relu', strides=(1,1),
                   pedding='same', input_shape=input_shape))
  model.add(Conv2D(32, (3,3), activation='relu', strides=(1,1),
                   pedding='same'))
  model.add(Conv2D(64, (3,3), activation='relu', strides=(1,1),
                   pedding='same'))
  model.add(Conv2D(128, (3,3), activation='relu', strides=(1,1),
                   pedding='same'))
  model.add(MaxPool2D(6,2))
  model.add(Dropout(0.5))
  model.add(Flatten())
  model.add(Dense(128, activation='relu'))
  model.add(Dense(64, activation='relu'))
  model.add(Dense(39, activation='softmax'))
  model.summary()
  model.complile(loss='categorical_crossentropy',
                 optimizer='abm',
                 metrics=['acc'])

  return model

class Config:
    def _init_(self, mode=('conv'), nflit=8 , nfeat=150, nfft = 80, rate=1000):
      self.mode = mode
      self.nfilt = nfilt
      self.nfeat = nfeat
      self.nfft = nfft
      self.rate = rate
      self.step = int(rate/11)

df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Medical Speech, Transcription, and Intent/overview-of-recordings.csv')
df.set_index('file_name', inplace=True)

!ls = '/content/drive/MyDrive/Colab Notebooks/Medical Speech, Transcription, and Intent/recordings'

!ls = '/content/drive/MyDrive/Colab Notebooks/Medical Speech, Transcription, and Intent/recordings'
for f in df.index:
  rate, signal = wavfile.read('audio_clipping'+f)
  df.at[f, 'length'] = signal.shape[0]/rate

classes = list(np.unique(df.phrase))
class_dist = df.groupby(['phrase'])['overall_quality_of_the_audio'].mean()
n_samples = 2 * int(df['overall_quality_of_the_audio'].sum()/0.1)
prob_dist = class_dist / class_dist.sum()
choices = np.random.choice(class_dist.index, p=prob_dist)

fig, ax = plt.subplots()
ax.set_title('ASR Modeling Distribution', y= 1.08)
ax.pie(class_dist, labels=class_dist.index, autopcts='%1.1f%%',
       shadow=False, startangel=90)
ax.axis('equal')
plt.show()

config = Config(mode='conv')

config = Config(mode='conv')
if config.mode == 'conv':
  X, y = build_rand_feat()
  y_flat = np.argmax(y, axis=1)
  input_shape = (X.shape[1], X.shape[2])
  model = get_conv_model()
elif config.mode == 'time':
  X, y = build_rand_feat()
  y_flat = np.argmax(y, axis=1)
  input_shape = (X.shape[1], X.shape[2])
  model = get_recurrent_model()
class_weight = compute_class_weight('balance',
                                    np.unique(y_flat),
                                    y_flat)
model.fit(X, y, epochs=25, batch_size=1000, 
          shuffle=True, 
          class_weight=class_weight)

