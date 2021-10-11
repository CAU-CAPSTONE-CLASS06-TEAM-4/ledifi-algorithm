from collections import deque
import subprocess
import librosa
import matplotlib.pyplot as plt         #그래프
import os

SAMPLE1_PATH = "C:/capstone/ledifi-algorithm/vrc/sample3.mp4"
SAMPLE1_PATH2 = "C:/capstone/ledifi-algorithm/vrc/sample3.wav"

def convert_to_wav(Path):
    if Path[-3:] != 'mp4':
        print('file is not mp4')
        return False
    Convertpath = Path[:-3]+'wav'
    command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(Path,os.path.join(Convertpath))
    subprocess.call(command,shell=True)

def check_mute(path,second):    #second -> 정적 탐지 기준 시간
    if path[-3:] != 'wav':
        print('file is not wav')
        return False
    y, sr = librosa.load(path,sr = 10000)    

    count = 0
    mute_count = 0
    start = -1
    mute = []
    for i in y:
        if i == 0:
            if start == -1: #시작 위치를 설정
                start = count
            mute_count += 1

        else:
            if start != -1 and mute_count > sr*second:
                mute += [[start,count]]
            start = -1
            mute_count = 0
        count+=1
    for k in range(len(mute)):
        print(mute[k])
    
def make_graph(path):
    if path[-3:] != 'wav':
        print('file is not wav')
        return False
    y, sr = librosa.load(path,sr = 10000)   
    num = len(y)
    x = range(num)
    plt.plot(x,y)
    plt.show()

convert_to_wav(SAMPLE1_PATH)
check_mute(SAMPLE1_PATH2,2)
make_graph(SAMPLE1_PATH2)
