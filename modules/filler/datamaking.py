from contextlib import redirect_stderr
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import cv2
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

def get_fps(PATH):
    cap = cv2.VideoCapture(PATH+'.mp4')
    return cap.get(cv2.CAP_PROP_FPS)

def detect(PATH, msl, st):
    wave_file = AudioSegment.from_wav(PATH+'.wav')
    print("detecting nonsilent")
    res =  detect_nonsilent(wave_file, min_silence_len=msl, silence_thresh=st)
    print("done")
    return res

def bound(nonsilents, n, m):
    res = []
    for line in nonsilents:
        if n <= line[1] - line[0] <= m: res.append(line)
    return res

def makefile(PATH, nonsilents):
    wave_file = AudioSegment.from_wav(PATH+'.wav')

    print("exporting wav files")
    WAV_PATH = PATH.split('/')
    WAV_PATH = WAV_PATH[:len(WAV_PATH)-1]
    WAV_PATH = "/".join(WAV_PATH)
    WAV_PATH += "/nonsilents"
    os.mkdir(WAV_PATH)
    WAV_PATH += "/"

    for nonsilent in nonsilents:
        name = lst_to_HMS(nonsilent, 1000) + ".wav"
        wave_file[nonsilent[0]:nonsilent[1]].export(WAV_PATH + name, format='wav')

def maketxt(PATH, nonsilents):
    print("write txt")
    TXT_PATH = PATH + "_nonsilent.txt"
    f = open(TXT_PATH, 'w')
    for nonsilent in nonsilents:         
        f.write(lst_to_HMS(nonsilent, 1000)+"\n")
    f.close()

def datamaking(PATH, min_silence_len, silence_thresh, bound_bigger_than, bound_less_than):
    nonsilents = detect(PATH, min_silence_len, silence_thresh)
    nonsilents = bound(nonsilents, bound_bigger_than, bound_less_than)
    makefile(PATH, nonsilents)
    #maketxt(PATH, nonsilents)
