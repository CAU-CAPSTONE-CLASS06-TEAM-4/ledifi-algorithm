import wave
import subprocess
import librosa
import matplotlib.pyplot as plt         #그래프
import os

def convert_to_wav(Path):   
    # mp4파일 시작부터 끝까지 wav파일로 변환하는 함수
    # path는 파일이 있는 경로
    if Path[-3:] != 'mp4':
        print('file is not mp4')
        return False
    Convertpath = Path[:-3]+'wav'
    command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(Path,os.path.join(Convertpath))
    subprocess.call(command,shell=True)

def getAmplitude(Path, Sample): 
    # 주파수 분석 후 해당 결과 반환하는 함수
    # path는 파일이 있는 경로
    if Path[-3:] != 'wav':
        print('file is not wav')
        return False
    y, sr = librosa.load(Path,sr = Sample)
    return y

def check_mute(Path, fps, second, sample_slice, silence_thres):
    # path는 파일이 있는 경로, second는 정적을 판단할 시간초, Sample은 초당 sampling할 샘플의 수
    # 시작부터 끝까지 탐색하여 정적인 구간 반환하는 함수
    # 반환형은 list이고, 리스트의 각 원소 list[0] ~ 에는 정적의 시작과 끝이 리스트로 들어있는 이중리스트구조
    f = wave.open(Path, 'rb')
    sr = f.getframerate()
    fr = f.getnframes()
    f.close()

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
                    mute.append([int(start), int(end)])
                                                 
    return mute
    
def make_graph(path, Sample):   
    # wav파일 받아서 그래프 그리는 함수
    # path는 파일이 있는 경로
    if path[-3:] != 'wav':
        print('file is not wav')
        return False

    y, sr = librosa.load(path,sr = Sample)  
    num = len(y)
    print(num)
    x = range(num)
    plt.plot(x,y)
    plt.show()


def mute_sample(Path, second,checklist ,Sample):
    # Path : 원본 강의가 있는 경로 / second : 정적을 판단할 시간초 / checklist : 잘라낼 프레임 시작과 끝을 저장하는 리스트
    # 프레임을 입력받으면, 그 시간대의 음성을 보고 정적인지 아닌지 구분하는 함수
    if Path[-3:] != 'mp4':
        print('file is not mp4')
        return False
    # 프레임을 가지고 해당 영상부분 wav파일로 추출
    # checklist를 나누는 분모는 openvc의 초당 프레임 수
    start = checklist[0]/30
    end = checklist[1]/30 - start
    Convertpath = Path[:-3]+'wav'
    command = "ffmpeg -ss {} -i {} -t {} {}".format(start,Path,end,os.path.join(Convertpath))
    subprocess.call(command,shell=True)
    #추출한 wav파일로 음성분석 시작
    y, sr = librosa.load(Convertpath,sr = Sample)
    count = 0
    mute_count = 0
    startAmp = -1
    mute = []
    ismute = False
    
    for i in y:
        if i < 0.005 and i>-0.005:
            if startAmp == -1: #시작 위치를 설정
                startAmp = count
            mute_count += 1
        else:
            if start != -1 and mute_count > sr*second:
                temp1 = startAmp//Sample
                temp2 = count//Sample
                mute += [[temp1,temp2]]
                ismute = True
            start = -1
            mute_count = 0
        count+=1
        
    for k in range(len(mute)):
        print(mute[k])
    return ismute


def convert_to_wav_frame(Path, checklist):
    #프레임을 입력받으면 프레임에 해당되는 시간대만 잘라서 wav파일로 추출
    if Path[-3:] != 'mp4':
        print('file is not mp4')
        return False
    # 프레임을 가지고 해당 영상부분 wav파일로 추출
    start = checklist[0]/30
    end = checklist[1]/30 - start
    Convertpath = Path[:-3]+'wav'
    command = "ffmpeg -ss {} -i {} -t {} {}".format(start,Path,end,os.path.join(Convertpath))
    subprocess.call(command,shell=True)

###

def sd(path, fps, sec, sample_slice, silence_thres): 
    try:    # wav파일이 이미 있는지 테스트
        open(path + '.wav', 'r')
        print('wav file is already exist.')
    except FileNotFoundError:   # 없다면 wav파일 생성
        print('wav file is not exist.')
        try:
            convert_to_wav(path+'.mp4')
        except:
            print('Wrong path') # 경로가 잘못되었을 경우
            return

    path = path + '.wav'
    return check_mute(path, fps, sec, sample_slice, silence_thres)
                    