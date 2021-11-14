import sys
import cv2
from modules import video
from modules import silence_detection

### 실행 인자 해석
# LECTURE
LECTURE_PATH = sys.argv[1]
if '.mp4'not in LECTURE_PATH:
    raise AssertionError('video file must be mp4.')
LECTURE_PATH = LECTURE_PATH.split('.')[0]

# SETTING
SETTING_PATH = sys.argv[2]
f = open(SETTING_PATH)
OPTION_SD_SECOND = int(f.readline().split()[1])
f.close()

### threshold 세팅
SETTING_VID_TRANSITION_THRES = 0.93
SETTING_VID_WRITING_THRES = 6
SETTING_SD_SAMPLE_SLICE = 10
SETTING_SD_SILENCE_THRES = 0.005

### init

res = []
cap = cv2.VideoCapture(LECTURE_PATH+'.mp4')
LECTURE_FPS = cap.get(cv2.CAP_PROP_FPS)

## 정적 감지 ##
sd_res = silence_detection.sd(LECTURE_PATH, LECTURE_FPS, OPTION_SD_SECOND, SETTING_SD_SAMPLE_SLICE, SETTING_SD_SILENCE_THRES)

for i in range(len(sd_res)):
    sd_res[i] = ['silence'] + sd_res[i]
res = sd_res

## 간투사 검출 ##
def tempfunc():
    lst = []
    return lst
res += tempfunc()

## 영상 판독 ##
res = video.video_chk(LECTURE_PATH, res, SETTING_VID_TRANSITION_THRES, SETTING_VID_WRITING_THRES, False)

## 파일 저장 ##
f = open(LECTURE_PATH+'.txt','w')
f.write('FPS: %d\n' %LECTURE_FPS)
for i in range(len(res)):
    f.write('%s %d %d %s\n' %(res[i][0], res[i][1], res[i][2], res[i][3]))
f.close()
