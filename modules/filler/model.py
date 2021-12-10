from keras import Input
from keras.utils.np_utils import to_categorical
from keras import Model
from keras import layers
import librosa
import numpy as np
import os


"""
초기화
"""
DATA_PATH = "C:/Users/Master/Desktop/dataset/"

pad1d = lambda a, i: a[0: i] if a.shape[0] > i else np.hstack((a, np.zeros(i-a.shape[0])))
pad2d = lambda a, i: a[:, 0:i] if a.shape[1] > i else np.hstack((a, np.zeros((a.shape[0], i-a.shape[1]))))

"""
데이터 준비
"""
print("--load train data--")

data = []
labels = ['어', '음', '외', '절']
i = 0

for label in labels:
    PATH = DATA_PATH + label + '/'
    temp = []
    for filename in os.listdir(PATH):
        wav, sr = librosa.load(PATH + filename, sr=16000)
        mfcc = librosa.feature.mfcc(wav, sr=16000, n_mfcc=100, n_fft=400, hop_length=160)
        padded_mfcc = pad2d(mfcc, 80)
        temp.append([padded_mfcc, i])
    data.append(temp)
    i += 1

import random
random.shuffle(data)

train = []
test = []

for i in range(len(data)):
    train += data[i][0:len(data[i])-2]
    test += data[i][-2:]    

"""
데이터 텐서화
"""
train_x = [a for [a,b] in train]
train_y = [b for [a,b] in train]

test_x = [a for [a,b] in test]
test_y = [b for [a,b] in test]

train_x = np.array(train_x)
train_x = np.expand_dims(train_x, -1)
train_y = to_categorical(train_y)

test_x = np.array(test_x)
test_x = np.expand_dims(test_x, -1)
test_y = to_categorical(test_y)

"""
모델 생성
"""

ip = Input(shape=train_x[0].shape)
m = layers.Conv2D(32, kernel_size=(4,4), activation='relu')(ip)
m = layers.MaxPooling2D(pool_size=(4,4))(m)
m = layers.Conv2D(64, kernel_size=(4,4), activation='relu')(ip)
m = layers.MaxPooling2D(pool_size=(4,4))(m)
m = layers.Conv2D(96, kernel_size=(4,4), activation='relu')(ip)
m = layers.MaxPooling2D(pool_size=(4,4))(m)
m = layers.Flatten()(m)
m = layers.Dense(64, activation='relu')(m)
m = layers.Dense(32, activation='relu')(m)
op = layers.Dense(4, activation='softmax')(m)

model = Model(ip, op)
model.summary()

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(train_x, train_y, epochs=100, batch_size=32, verbose=1, validation_data=(test_x, test_y))

model.save('filler_detection_model.h5')

