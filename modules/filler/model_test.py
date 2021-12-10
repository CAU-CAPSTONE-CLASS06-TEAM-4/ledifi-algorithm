import librosa
from keras.models import load_model
import numpy as np
import os

pad2d = lambda a, i: a[:, 0:i] if a.shape[1] > i else np.hstack((a, np.zeros((a.shape[0], i-a.shape[1]))))
model = load_model("ledifi-algorithm/modules/filler/filler_detection_model_new_epoch100.h5")
testpath = "C:/Users/Master/Desktop/model_testing"

for filename in os.listdir(testpath):
    audio, sr = librosa.load(testpath+'/'+filename, sr=16000)
    mfcc = librosa.feature.mfcc(audio, sr=16000, n_mfcc=100, n_fft=400, hop_length=160)
    padded_mfcc = pad2d(mfcc, 80)
    padded_mfcc= np.expand_dims(padded_mfcc, 0)
    y = model.predict(padded_mfcc)
    print(filename, ":", y)
