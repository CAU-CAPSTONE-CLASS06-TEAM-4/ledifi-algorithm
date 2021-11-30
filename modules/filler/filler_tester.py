import os
import numpy as np
import shutil
import librosa
from keras.models import load_model
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

import warnings
warnings.simplefilter("ignore", UserWarning)

pad2d = lambda a, i: a[:,0:i] if a.shape[1] > i else np.hstack((a, np.zeros((a.shape[0], i-a.shape[1]))))

######

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

def scale_and_detect(PATH, detect, make_txt, make_wav):

    if detect:
        lecture_pydub = AudioSegment.from_wav(PATH)
        lecture_pydub = lecture_pydub.apply_gain(-20.0 - lecture_pydub.dBFS)

        print('filler: detecting nonsilent from lecture')
        nonsilents = detect_nonsilent(lecture_pydub, min_silence_len=20, silence_thresh=-30)
        print('filler: detecting end')

        if make_wav:
            WAV_PATH = PATH.split('/')
            WAV_PATH = WAV_PATH[:len(WAV_PATH)-1]
            WAV_PATH = "/".join(WAV_PATH)
            WAV_PATH += "/nonsilents"
            os.mkdir(WAV_PATH)
            WAV_PATH += "/"

            for nonsilent in nonsilents:
                name = lst_to_HMS(nonsilent, 1000) + ".wav"
                lecture_pydub[nonsilent[0]:nonsilent[1]].export(WAV_PATH + name, format='wav')

        if make_txt:
            PATH = PATH.split('.')[0] + "_nonsilent.txt"
            f = open(PATH, 'w')
            for i in range(len(nonsilents)):
                f.write('%s %s\n' %(nonsilents[i][0], nonsilents[i][1]))
            f.close()

        return nonsilents
    else: return PATH.split('.')[0] + "_nonsilent.txt"

def get_bounded(nonsilents, n, m, make_txt, make_wav, FILE_PATH):
    if type(nonsilents) == type(""):
        f = open(nonsilents,'r')
        lines = f.read().strip().split('\n')
        nonsilents = []
        for line in lines:
            line = line.split()
            nonsilents.append([int(line[0]), int(line[1])])
        f.close()

    print("filler: collating syllables less than %d ms and bigger than %d ms" %(n, m))
    res = []
    for nonsilent in nonsilents:
        if n <= nonsilent[1]-nonsilent[0] <= m: res.append(nonsilent)
    print("filler: length of list = ", len(res))
    
    if make_txt:
        lst = []
        for re in res: lst.append(lst_to_HMS(re, 1000))
        PATH = FILE_PATH.split('.')
        PATH = PATH[0] + "_bounded_" + str(n) + "_" + str(m) + ".txt"
        f = open(PATH, 'w')
        for i in range(len(lst)): f.write(lst[i] + "\n")
        f.close()

    if make_wav:
            lecture_pydub = AudioSegment.from_wav(FILE_PATH)
            lecture_pydub = lecture_pydub.apply_gain(-20.0 - lecture_pydub.dBFS)

            WAV_PATH = FILE_PATH.split('/')
            WAV_PATH = WAV_PATH[:len(WAV_PATH)-1]
            WAV_PATH = "/".join(WAV_PATH)
            WAV_PATH += "/nonsilents_bounded"
            os.mkdir(WAV_PATH)
            WAV_PATH += "/"

            for re in res:
                name = lst_to_HMS(re, 1000) + ".wav"
                lecture_pydub[re[0]:re[1]].export(WAV_PATH + name, format='wav')

    return res

def is_filler(audio, model):
    audio.export("temp.wav", format='wav')

    wav, _ = librosa.load("temp.wav")
    mfcc = librosa.feature.mfcc(wav, sr=16000)
    padded_mfcc = pad2d(mfcc, 40)
    padded_mfcc = np.expand_dims(padded_mfcc, 0)

    res = model.predict(padded_mfcc)
    try: os.remove("temp.wav")
    except: pass
    return res

def predicting(nonsilents, FILE_PATH, MODEL_PATH, make_result_bool):
    # 초기화
    model = load_model(MODEL_PATH)
    lecture_pydub = AudioSegment.from_wav(FILE_PATH)
    lecture_pydub = lecture_pydub.apply_gain(-20.0 - lecture_pydub.dBFS)
    res = []
    txtfile = []
    predict_lst = []
    i = 1
 
    # predicting 시작
    print("filler: start predicting")
    for nonsilent in nonsilents:
        sliced_audio = lecture_pydub[nonsilent[0]:nonsilent[1]]
        result = is_filler(sliced_audio, model)
        if result[0][1] < 0.05: res.append(nonsilent)
               
        i+=1
        if i%10 == 0: print('now in %d' %i)
        if make_result_bool: 
            txtfile.append(lst_to_HMS(nonsilent, 1000) + " " + str(result[0][3] < 0.05))
            predict_lst.append(result[0])

    if make_result_bool:
        p = FILE_PATH.split('.')[0]
        p += '_predict_result.txt'
        f = open(p, 'w')
        for i in range(len(txtfile)):
            f.write(txtfile[i] + " [" + str(predict_lst[i][0]) + ", " + str(predict_lst[i][1]) + ", " + str(predict_lst[i][2]) + ", " + str(predict_lst[i][3]) + "]\n")
        f.close()

        p = FILE_PATH.split('.')[0]
        p += '_True_result_list.txt'
        f = open(p, 'w')

        WAV_PATH = FILE_PATH.split('/')
        WAV_PATH = WAV_PATH[:len(WAV_PATH)-1]
        WAV_PATH = "/".join(WAV_PATH)
        WAV_PATH += "/nonsilents_bounded_true"
        os.mkdir(WAV_PATH)
        WAV_PATH += "/"

        for i in range(len(predict_lst)):
            if predict_lst[i][1] < 0.05:
                name = lst_to_HMS(nonsilents[i],1000) + ".wav"
                lecture_pydub[nonsilents[i][0]:nonsilents[i][1]].export(WAV_PATH + name, format = 'wav')
                f.write(txtfile[i] + " [" + str(predict_lst[i][0]) + ", " + str(predict_lst[i][1]) + ", " + str(predict_lst[i][2]) + ", " + str(predict_lst[i][3]) + "]\n")
        f.close()

    print("filler: end of predicting")
    return res

def main(FILE_PATH, MODEL_PATH, BIGGER_THAN, LESS_THAN):
    nonsilents = scale_and_detect(FILE_PATH, True, False, False)
    nonsilents = get_bounded(nonsilents, BIGGER_THAN, LESS_THAN, False, False, FILE_PATH)
    res = predicting(nonsilents, FILE_PATH, MODEL_PATH, True)
    for re in res: print(re)

###

import subprocess

def convert_to_wav(Path):   
    # mp4파일 시작부터 끝까지 wav파일로 변환하는 함수
    # path는 파일이 있는 경로
    if Path[-3:] != 'mp4':
        print('file is not mp4')
        return False
    Convertpath = Path[:-3]+'wav'
    command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(Path,os.path.join(Convertpath))
    subprocess.call(command,shell=True)

FILE_PATH = "C:/Users/Master/Desktop/new_dataset/08-1/08-1"
MODEL_PATH = "ledifi-algorithm/modules/filler/filler_detection_model_nonok.h5"
BIGGER_THAN = 100
LESS_THAN = 1000

convert_to_wav(FILE_PATH+".mp4")
main(FILE_PATH+".wav", MODEL_PATH, BIGGER_THAN, LESS_THAN)
