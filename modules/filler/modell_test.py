'''
import pydub

f = open('s1filler.txt', 'r')
lines = f.read().strip().split('\n')
f.close()

ps = []
for line in lines: 
    p = line.split()
    ps.append([int(p[0]), int(p[1])])

for p in ps: print(p)

audio = pydub.AudioSegment.from_wav('sample01.wav')
for i in range(len(ps)):

    seg = audio[ps[i][0]:ps[i][1]]
    seg.export(str(i) + '.wav', format='wav')
'''
'''
from keras.models import load_model
import librosa
import numpy as np

pad2d = lambda a, i: a[:,0:i] if a.shape[1] > i else np.hstack((a, np.zeros((a.shape[0], i-a.shape[1]))))
MODEL_PATH = "ledifi-algorithm/modules/filler/filler_detection_model.h5"
model = load_model(MODEL_PATH)

for i in range(14):
    filename = str(i)+'.wav'

    wav, sr = librosa.load(filename, sr=16000)
    frame_length = 0.025
    mfcc = librosa.feature.mfcc(wav, n_fft = int(round(sr*frame_length)))
    padded_mfcc = pad2d(mfcc, 40)
    padded_mfcc = np.expand_dims(padded_mfcc, 0)

    res = model.predict(padded_mfcc)
    print(res)
'''
import librosa
from keras.models import load_model
import numpy as np

pad2d = lambda a, i: a[:, 0:i] if a.shape[1] > i else np.hstack((a, np.zeros((a.shape[0], i-a.shape[1]))))
model = load_model("ledifi-algorithm/modules/filler/filler_detection_model.h5")
DATA_PATH = "C:/Users/Master/Desktop/dataset/"
testings = ['그003', '그080', '그201', '어279', '어285', '어303', '외210', '외711', '외729', '음609', '음717', '음821']

for testing in testings:
    audio, sr = librosa.load(DATA_PATH+testing+'.wav')
    mfcc = librosa.feature.mfcc(audio)
    padded_mfcc = pad2d(mfcc, 40)
    padded_mfcc= np.expand_dims(padded_mfcc, 0)
    y = model.predict(padded_mfcc)
    print(testing, ":", y)