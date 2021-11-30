'''
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

lecture_pydub = AudioSegment.from_wav('C:/Users/Master/Desktop/filler_test/02.wav')
lecture_pydub = lecture_pydub.apply_gain(-20.0 - lecture_pydub.dBFS)
lecture_pydub[2485:2684].export('C:/Users/Master/Desktop/filler_test/zzz.wav')
'''
'''
import librosa
from keras.models import load_model
import numpy as np

pad2d = lambda a, i: a[:, 0:i] if a.shape[1] > i else np.hstack((a, np.zeros((a.shape[0], i-a.shape[1]))))
model = load_model("ledifi-algorithm/modules/filler/filler_detection_model.h5")

audio, sr = librosa.load('C:/Users/Master/Desktop/filler_test/nonsilents/0,0,0,9~0,0,1,8.wav')
mfcc = librosa.feature.mfcc(audio)
padded_mfcc = pad2d(mfcc, 40)
padded_mfcc = np.expand_dims(padded_mfcc, 0)
y = model.predict(padded_mfcc)
print(y)
'''
'''

import os
DATA_PATH = "C:/Users/Master/Desktop/new_dataset/"
count = 5000
for filename in os.listdir(DATA_PATH+"nodab"):
    file_oldname = os.path.join(DATA_PATH + "nodab", filename)
    newname = '외' + str(count) + '.wav'
    file_newname = os.path.join(DATA_PATH+"nodab", newname)
    count +=1
    os.rename(file_oldname, file_newname)
'''

a = [1,2,3]
b = [5,6,7]
print(a+b)