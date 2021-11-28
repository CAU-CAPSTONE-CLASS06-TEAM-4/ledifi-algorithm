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

train_X  =[]
train_y = []

test_X = []
test_y = []

pad1d = lambda a, i: a[0: i] if a.shape[0] > i else np.hstack((a, np.zeros(i-a.shape[0])))
pad2d = lambda a, i: a[:, 0:i] if a.shape[1] > i else np.hstack((a, np.zeros((a.shape[0], i-a.shape[1]))))

SAMPLE_RATE = 16000
"""
학습 데이터 준비
"""
print("--load train data--")
for filename in os.listdir(DATA_PATH+"train/"):
    wav, sr = librosa.load(DATA_PATH+"train/"+filename, sr=SAMPLE_RATE)
    mfcc = librosa.feature.mfcc(wav)
    padded_mfcc = pad2d(mfcc, 40)
    train_X.append(padded_mfcc)

    if filename[0] == '외'  : train_y.append(1)
    else                    : train_y.append(0)
"""
테스트 데이터 준비
"""
print("--load test data--")
for filename in os.listdir(DATA_PATH+"test/"):
    wav, sr = librosa.load(DATA_PATH+"test/"+filename, sr=SAMPLE_RATE)
    mfcc = librosa.feature.mfcc(wav)
    padded_mfcc = pad2d(mfcc, 40)
    test_X.append(padded_mfcc)

    if filename[0] == '외'  : test_y.append(1)
    else                    : test_y.append(0)
"""
데이터 텐서화
"""
train_X = np.array(train_X)
train_y = to_categorical(np.array(train_y))

test_X = np.array(test_X)
test_y = to_categorical(np.array(test_y))

"""
모델 생성
"""
train_X = np.expand_dims(train_X, -1)
test_X = np.expand_dims(test_X, -1)

ip = Input(shape=train_X[0].shape)
m = layers.Conv2D(64, kernel_size=(4,4), activation='relu')(ip)
m = layers.MaxPooling2D(pool_size=(4,4))(m)
m = layers.Flatten()(m)
m = layers.Dense(32, activation='relu')(m)
op = layers.Dense(2, activation='sigmoid')(m)

model = Model(ip, op)
model.summary()

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(train_X, train_y, epochs=100, batch_size=32, verbose=1, validation_data=(test_X, test_y))

model.save('filler_detection_model.h5')

###

testings = ['그003', '그080', '그201', '어279', '어285', '어303', '외210', '외711', '외729', '음609', '음717', '음821']

for testing in testings:
    audio, sr = librosa.load(DATA_PATH+testing+'.wav')
    mfcc = librosa.feature.mfcc(audio)
    padded_mfcc = pad2d(mfcc, 40)
    padded_mfcc= np.expand_dims(padded_mfcc, 0)
    y = model.predict(padded_mfcc)
    print(testing, ":", y)
