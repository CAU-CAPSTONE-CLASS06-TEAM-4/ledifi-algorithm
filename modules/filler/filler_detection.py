from pydub import AudioSegment
from pydub.audio_segment import AUDIO_FILE_EXT_ALIASES
from pydub.silence import detect_nonsilent
from keras.models import load_model
import librosa
import numpy as np
import os


def lst_to_HMS(lst, fps):

    ahour, bhour, amin, bmin = 0, 0, 0, 0
    asec = (lst[0]/fps)
    bsec = (lst[1]/fps)
    
    while asec > 60: 
        asec -= 60
        amin += 1

    while bsec > 60:
        bsec -= 60
        bmin += 1

    while amin > 60:
        amin -= 60
        ahour += 1

    while bmin > 60:
        bmin -= 60
        bhour += 1

    if type(asec) == type(0.1):
        asec = str(asec).split('.')
        asec = asec[0] + "," + asec[1][0]

    if type(bsec) == type(0.1):
        bsec = str(bsec).split('.')
        bsec = bsec[0] + "," + bsec[1][0]
    
    astring = str(ahour) + "," + str(amin) + "," + str(asec)
    bstring = str(bhour) + "," + str(bmin) + "," + str(bsec)
    res = astring + "~" + bstring
        
    return res

def get_bounded(nonsilents, n, m):
    res = []
    for line in nonsilents:
        if n <= line[1] - line[0] <= m: res.append(line)
    return res

pad2d = lambda a, i: a[:,0:i] if a.shape[1] > i else np.hstack((a, np.zeros((a.shape[0], i-a.shape[1]))))

def is_filler(audio: AudioSegment, model):
    audio.export("temp.wav", format='wav')

    wav, _ = librosa.load("temp.wav", sr=16000)
    mfcc = librosa.feature.mfcc(wav, sr=16000, n_mfcc=100, n_fft=400, hop_length=160)
    padded_mfcc = pad2d(mfcc, 80)
    padded_mfcc = np.expand_dims(padded_mfcc, 0)

    predict_result = model.predict(padded_mfcc)
    try: os.remove("temp.wav")
    except: pass    

    return predict_result

def predicting(nonsilents, LECTURE_PATH, MODEL_PATH, make_result_txt):
    # 초기화
    model = load_model(MODEL_PATH)
    lecture_pydub = AudioSegment.from_wav(LECTURE_PATH+".wav")

    res = []
    result_txtfile = []
    result_true_txtfile = []
    i = 1
 
    # predicting 시작
    print("filler: start predicting")
    print("length of nonsilents = %d" %(len(nonsilents)))
    print("-----------------------------------------------------")
    for nonsilent in nonsilents:
        sliced_audio = lecture_pydub[nonsilent[0]:nonsilent[1]]
        predict_result = is_filler(sliced_audio, model)

        p_true = predict_result[0][0] + predict_result[0][1]
        p_false = predict_result[0][2] + predict_result[0][3]

        if   (predict_result[0][0]>0.95): filler = True
        elif (predict_result[0][1]>0.95): filler = True
        else                           : filler = False

        if filler: res.append(nonsilent)
   
        i+=1
        if i%50 == 0: print('now in %d' %i)
        if make_result_txt: 
            result_txtfile.append(lst_to_HMS(nonsilent, 1000) + " - " +str(filler) +": [" +  
                str(predict_result[0][0]) + ", " +  
                str(predict_result[0][1]) + ", " +  
                str(predict_result[0][2]) + ", " +  
                str(predict_result[0][3]) + "]\n")

            if filler: 
                result_true_txtfile.append(lst_to_HMS(nonsilent, 1000) + ": [" +  
                str(predict_result[0][0]) + ", " +  
                str(predict_result[0][1]) + ", " +  
                str(predict_result[0][2]) + ", " +  
                str(predict_result[0][3]) + "]\n")

    if make_result_txt:
        p = LECTURE_PATH+"_predict_result.txt"
        f = open(p, 'w')
        for line in result_txtfile: f.write(line)
        f.close()

        p = LECTURE_PATH+"_predict_result_True.txt"
        f = open(p, 'w')
        for line in result_true_txtfile: f.write(line)
        f.close()

    return res

def result_to_fps(fillers, fps):
    res = []
    for line in fillers:
        r1 = line[0]
        r2 = line[1]
        r1 = int((r1/1000)*fps)
        r2 = int((r2/1000)*fps)+1
        res.append(['filler', r1,r2])
    return res
###

def fd(LECTURE_PATH, MODEL_PATH, fps, msl, st, bound_bigger_than, bound_less_than):
    lecture_wav = AudioSegment.from_wav(LECTURE_PATH+".wav")
    nonsilents = detect_nonsilent(lecture_wav, min_silence_len=msl, silence_thresh=st)
    nonsilents = get_bounded(nonsilents, bound_bigger_than, bound_less_than)
    fillers = predicting(nonsilents, LECTURE_PATH, MODEL_PATH, False)
    return result_to_fps(fillers, fps)

