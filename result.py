from moviepy.editor import *
import cv2
import sys
import time

### 실행 인자 해석
# 강의 원본 파일
stime = time.time()

LECTURE_PATH = sys.argv[1]
if '.mp4'not in LECTURE_PATH:
    raise AssertionError('video file must be mp4.')
SAVE_PATH = LECTURE_PATH.split('.')[0] + "_result.mp4"

# 선택 결과 리스트
f = open(sys.argv[2])
RES_LST = f.read().strip().split('\n')
f.close()

temp = []
for i in range(len(RES_LST)):
    RES_LST[i] = RES_LST[i].split()
    if RES_LST[i][4] == "True":
        RES_LST[i][1], RES_LST[i][2] = map(int, (RES_LST[i][1], RES_LST[i][2]))
        temp.append(RES_LST[i])
RES_LST = temp

temp = []
for i in range(len(RES_LST)):
    if RES_LST[i][0] == "silence":
        sf = RES_LST[i][1]
        ef = RES_LST[i][2]
        frame_middle = int((ef+sf)/2)
        frame_cut = int((ef-sf)/4)
        temp.append([RES_LST[i][0], sf, frame_middle - frame_cut, RES_LST[i][3], RES_LST[i][4]])
        temp.append([RES_LST[i][0], frame_middle + frame_cut, ef, RES_LST[i][3], RES_LST[i][4]])
    else:
        temp.append(RES_LST[i])
RES_LST = temp

# 초기화
original_lecture = VideoFileClip(LECTURE_PATH)
c = cv2.VideoCapture(LECTURE_PATH)

FPS = original_lecture.fps
LECTURE_LEGNTH = ((c.get(cv2.CAP_PROP_FRAME_COUNT))/FPS)
LST_LENGTH = len(RES_LST)

for i in range(LST_LENGTH): 
    RES_LST[i][1] = RES_LST[i][1]/FPS
    RES_LST[i][2] = RES_LST[i][2]/FPS

if LST_LENGTH == 0:
    raise AssertionError("No actual list for cliping")

clip_lst = []

for i in range(LST_LENGTH): print(RES_LST[i])

if RES_LST[0][1] == 0:
    clip_lst.append(original_lecture.subclip(0, RES_LST[0][1]))

for i in range(LST_LENGTH-1):
    clip_start = RES_LST[i][2]
    clip_end = RES_LST[i+1][1]
    clip_lst.append(original_lecture.subclip(clip_start, clip_end))

if LST_LENGTH-1 == 0: pass
elif RES_LST[LST_LENGTH-1][2] != LECTURE_LEGNTH:
    clip_lst.append(original_lecture.subclip(RES_LST[LST_LENGTH-1][2], LECTURE_LEGNTH))

print(len(clip_lst))

RES_VID = concatenate_videoclips(clip_lst)
RES_VID.write_videofile(SAVE_PATH)

etime = time.time() - stime
print("Time: %d" %etime)
