import sys
import cv2
from modules import video
from modules.silence_detection import sd_librosa
from modules.filler.filler_detection import fd

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

SETTING_FD_MIN_SILENCE_LEN = 70
SETTING_FD_SILENCE_THRESH = -43
SETTING_FD_BIGGER_THAN = 100
SETTING_FD_LESS_THAN = 1000
MODEL_PATH = "ledifi-algorithm/modules/filler/filler_detection_model_epoch100.h5"

### init
res = []
cap = cv2.VideoCapture(LECTURE_PATH+'.mp4')
LECTURE_FPS = cap.get(cv2.CAP_PROP_FPS)

## 정적 감지 ##
print("### detecting silence ###")
sd_res = sd_librosa(LECTURE_PATH, LECTURE_FPS, OPTION_SD_SECOND, SETTING_SD_SAMPLE_SLICE, SETTING_SD_SILENCE_THRES)

for i in range(len(sd_res)):
    sd_res[i] = ['silence'] + sd_res[i]
res = sd_res

## 간투사 검출 ##
print("### detecting filler ###")
temp = fd(LECTURE_PATH, MODEL_PATH, LECTURE_FPS, SETTING_FD_MIN_SILENCE_LEN, SETTING_FD_SILENCE_THRESH, SETTING_FD_BIGGER_THAN, SETTING_FD_LESS_THAN)
res += temp

## 영상 판독 ##
print("### video checking ###")
res.sort(key=lambda a: a[1])
res = video.video_chk(LECTURE_PATH, res, SETTING_VID_TRANSITION_THRES, SETTING_VID_WRITING_THRES, False)

## 파일 저장 ##
f = open(LECTURE_PATH+'.txt','w')
f.write('FPS: %.6f\n' %LECTURE_FPS)
for i in range(len(res)):
    f.write('%s %d %d %s\n' %(res[i][0], res[i][1], res[i][2], res[i][3]))
    f.write('%s %d %d %s\n' %('filler', res[i][1], res[i][2], res[i][3]))
f.close()
