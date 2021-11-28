import os
import numpy as np
import librosa
from keras.models import load_model
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

import warnings
warnings.simplefilter("ignore", UserWarning)

pad2d = lambda a, i: a[:,0:i] if a.shape[1] > i else np.hstack((a, np.zeros((a.shape[0], i-a.shape[1]))))

######
def scale_and_detect(PATH, DEBUG):
    lecture_pydub = AudioSegment.from_wav(PATH)
    lecture_pydub = lecture_pydub.apply_gain(-20.0 - lecture_pydub.dBFS)

    print('filler: detecting nonsilent from lecture')
    nonsilents = detect_nonsilent(lecture_pydub, min_silence_len=70, silence_thresh=-32.64)
    print('filler: detecting end')

    if DEBUG:
        f = open('testing.txt', 'w')
        for i in range(len(nonsilents)):
            f.write('%s %s\n' %(nonsilents[i][0], nonsilents[i][1]))
        f.close()

    return nonsilents

def is_filler(audio_file: AudioSegment, model):
    audio_file.export("temp.wav", format='wav')

    wav, sr = librosa.load("temp.wav", sr=16000)
    frame_length = 0.025
    mfcc = librosa.feature.mfcc(wav, n_fft = int(round(sr*frame_length)))
    padded_mfcc = pad2d(mfcc, 40)
    padded_mfcc = np.expand_dims(padded_mfcc, 0)

    res = model.predict(padded_mfcc)
    try: os.remove("temp.wav")
    except: pass
    if res[0][0] >= 0.9: return True
    else: return False

def slice_recursive(res:list, model, audio: AudioSegment, min_silence, start):
    min_silence = int(min_silence/1.2)
    if min_silence < 10: return 

    scaled_audio = audio.apply_gain(-20.0 - audio.dBFS)
    nonsilents = detect_nonsilent(scaled_audio, min_silence_len=min_silence, silence_thresh=-32.64)
    
    for nonsilent in nonsilents:
        nonsilent_audio = audio[nonsilent[0]:nonsilent[1]]
        if is_filler(nonsilent_audio, model):
            if nonsilent[1]-nonsilent[0] < 460:
                res.append([nonsilent[0]+start, nonsilent[1]+start])
            else:
                slice_recursive(res, model, nonsilent_audio, min_silence, nonsilent[0])

def get_less_than_n_msec(nonsilents, n):
    if type(nonsilents) == type(""):
        f = open(nonsilents,'r')
        lines = f.read().strip().split('\n')
        nonsilents = []
        for line in lines:
            line = line.split()
            nonsilents.append([int(line[0]), int(line[1])])
        f.close()

    print("filler: collating syllables less than %d ms" %n)
    res = []
    for nonsilent in nonsilents:
        if nonsilent[1]-nonsilent[0] < n: res.append(nonsilent)
    print("filler: length of list = ", len(res))

    return res


def predicting(nonsilents, FILE_PATH, MODEL_PATH):
    # 초기화
    model = load_model(MODEL_PATH)
    lecture_pydub = AudioSegment.from_wav(FILE_PATH)
    res = []
    tot_len = len(nonsilents)
    i = 1
 
    # predicting 시작
    print("filler: start predicting")
    for nonsilent in nonsilents:
        nonsilent_audio = lecture_pydub[nonsilent[0]:nonsilent[1]]
        if is_filler(nonsilent_audio, model):
            if nonsilent[1]-nonsilent[0] < 460:
                res.append(nonsilent)
            else:
                slice_recursive(res, model, nonsilent_audio, 70, nonsilent[0])
        i+=1
        if i%100 == 0: print('now in %d' %i)
        
    print("filler: end of predicting")
    return res

###

def main(FILE_PATH, MODEL_PATH, n):
    #nonsilents = scale_and_detect(PATH, True)
    nonsilents = get_less_than_n_msec('testing.txt', n)
    res = predicting(nonsilents, FILE_PATH, MODEL_PATH)
    for re in res: print(re)

###
FILE_PATH = "sample01.wav"
MODEL_PATH = "ledifi-algorithm/modules/filler/filler_detection_model.h5"
MSEC = 500

main(FILE_PATH, MODEL_PATH, MSEC)