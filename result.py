from moviepy.editor import *
import cv2

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

for i in range(len(RES_LST)):
    if RES_LST[i][0] == "silence":
        sf = RES_LST[i][1]
        ef = RES_LST[i][2]
        frame_middle = int((ef+sf)/2)
        frame_cut = int((ef-sf)/4)
        RES_LST[i][1] = frame_middle - frame_cut
        RES_LST[i][2] = frame_middle + frame_cut

# 초기화
original_lecture = VideoFileClip(LECTURE_PATH)
c = cv2.VideoCapture(LECTURE_PATH)

FPS = c.get(cv2.CAP_PROP_FPS)
LECTURE_LEGNTH = c.get(cv2.CAP_PROP_FRAME_COUNT)

for i in range(len(RES_LST)):
    RES_LST[i][1] /= FPS
    RES_LST[i][2] /= FPS

boundary = []
for line in RES_LST:
    boundary.append(line[1])
    boundary.append(line[2])

actual_clip = []
if boundary[0] != 0: actual_clip.append([0, boundary[0]])
for i in range(1, len(boundary)-2, 2): actual_clip.append([boundary[i], boundary[i+1]])
actual_clip.append([boundary[len(boundary)-1], LECTURE_LEGNTH/FPS])

if len(actual_clip) == 0:
    raise AssertionError("No actual list for cliping")

clip_lst = []
for i in actual_clip:
    clip_lst.append(original_lecture.subclip(i[0], i[1]))

RES_VID = concatenate_videoclips(clip_lst)
RES_VID.write_videofile(SAVE_PATH)
