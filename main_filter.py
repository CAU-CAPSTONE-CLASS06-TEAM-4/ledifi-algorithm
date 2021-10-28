from os import lstat
from modules import video
from modules import silence_detection

### 사용자로부터 입력받을 경로, 옵션
SAMPLE_PATH = "C:/Users/Master/Desktop/캡스톤깃허브/"

OPTION_SD_SECOND = 3
OPTION_SD_SAMPLING = 1000

### 테스트 세팅
SETTING_VID_TRANSITION_THRES = 0.93
SETTING_VID_WRITING_THRES = 6

### init

res = []
PATH = SAMPLE_PATH + 'sample10'

## 정적 감지 ##
import time

s = time.time()
sd_res = silence_detection.sd(PATH, OPTION_SD_SECOND, OPTION_SD_SAMPLING)
e = time.time()
print('time: ', end="")
print(e-s)

for i in range(len(sd_res)):
    sd_res[i] = ['silence'] + sd_res[i]
res = sd_res

## 간투사 검출 ##
def tempfunc():
    lst = []
    return lst
res += tempfunc()

## 영상 판독 ##
res = video.video_chk(PATH, res, SETTING_VID_TRANSITION_THRES, SETTING_VID_WRITING_THRES, False, True)

## 파일 저장 ##
n = PATH.split('/')
n = n[len(n)-1]
f = open(n+'.txt','w')

for i in range(len(res)):
    f.write(res[i][0] + " " + str(res[i][1]) + " " + str(res[i][2]) + " " + str(res[i][3]) + "\n")

f.close()
