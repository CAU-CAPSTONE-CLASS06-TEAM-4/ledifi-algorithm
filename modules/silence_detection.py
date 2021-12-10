import wave
import subprocess
import librosa
import os
from pydub import AudioSegment
from pydub.silence import detect_silence

def convert_to_wav(Path):   
    # mp4파일 시작부터 끝까지 wav파일로 변환하는 함수
    # path는 파일이 있는 경로
    if Path[-3:] != 'mp4':
        print('file is not mp4')
        return False
    Convertpath = Path[:-3]+'wav'
    command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(Path,os.path.join(Convertpath))
    subprocess.call(command,shell=True)
        

def check_mute_librosa(Path, fps, second, sample_slice, silence_thres):
    # path는 파일이 있는 경로, second는 정적을 판단할 시간초
    # 시작부터 끝까지 탐색하여 정적인 구간 반환하는 함수
    # 반환형은 list이고, 리스트의 각 원소 list[0] ~ 에는 정적의 시작과 끝이 리스트로 들어있는 이중리스트구조

    print("wav loading")
    y, sr = librosa.load(Path,sr = None)    
    print("wav loading end")

    mute = []
    silenced = False
    start = 0
    end = 0
    
    for i in range(0, len(y), int(sr/sample_slice)):
        val = y[i]
        if -silence_thres < val < silence_thres:    # 정적 감지
            if not silenced:    # 이전에 정적이 아니었다면, 정적이 시작되는 부분을 기록
                silenced = True
                start = i
                end = i
            else:               # 이전에 정적이었다면, 정적이 끝나는 부분을 갱신
                end+=int(sr/sample_slice)
        
        else:                                       # 음성 감지 
            if silenced:               # 이전에 정적이었다면, 정적이 끝난 것이므로 결과에 추가. start와 end 값은 샘플링레이트/샘플슬라이스이므로, 스케일링 필요.
                silenced = False
                start = start / sr
                end = end / sr
                
                if end-start >= second:
                    start *= fps
                    end *= fps
                    mute.append([int(start), int(end)+1])
                                                 
    return mute
    
###

def sd_librosa(path, fps, sec, sample_slice, silence_thres): 
    try:    
        open(path + '.wav', 'r')
        print('wav file is already exist.')
    except FileNotFoundError:   
        print('wav file is not exist.')
        try:
            convert_to_wav(path+'.mp4')
            scaling = AudioSegment.from_wav(path+".wav")
            scaling = scaling.apply_gain(-20.0 - scaling.dBFS)
            scaling.export(path+".wav", format = "wav")
        except:
            print('Wrong path') 
            return

    return check_mute_librosa(path+".wav", fps, sec, sample_slice, silence_thres)
                    
###

def sd_pydub(path, fps, sec):
    try:    
        open(path + '.wav', 'r')
        print('wav file is already exist.')
    except FileNotFoundError:   
        print('wav file is not exist.')
        try:
            convert_to_wav(path+'.mp4')
        except:
            print('Wrong path') 
            return

    file = AudioSegment.from_wav(path+".wav")
    file.apply_gain(-20.0 - file.dBFS)
    res = detect_silence(file, min_silence_len=sec*1000, silence_thresh=-32.64)
    for i in range(len(res)):
        res[i][0] = int(fps*res[i][0]/1000)
        res[i][1] = int(fps*res[i][1]/1000)
    return res
