from modules import video

import time

s = time.time()
print(s)
a = [i for i in range(10000000)]
e = time.time()
print(e-s)




SAMPLE1_PATH = "C:/Users/Master/Desktop/캡스톤깃허브/sample1.mp4"
SAMPLE2_PATH = "C:/Users/Master/Desktop/캡스톤깃허브/sample2.mp4"


SAMPLE1_LST = [[10, 16], [63, 69], [213, 218], [631, 635], [930, 934], [1173, 1177], [3197, 3200], [3311, 3315], [3876, 3880], [4023, 4027], [4048, 4051]]

'''
for i in range(len(SAMPLE1_LST)):
    SAMPLE1_LST[i] = ['silence'] + SAMPLE1_LST[i]

a = video.video_chk(SAMPLE1_PATH, SAMPLE1_LST, 0.9)
for item in a: print(item)
'''

sample1_sf = {'장면전환1':300, '장면전환2': 120690, '장면전환3': 126000, '장면전환4':103290,
                '판서1': 42000, '판서2': 76140, '판서3': 104250,
                '무변화1': 0, '무변화2': 4740, '무변화3': 29100}

sample1_ef = {'장면전환1':420, '장면전환2': 120840, '장면전환3': 126300, '장면전환4':103430,
                '판서1': 42300, '판서2': 76350, '판서3': 104550,
                '무변화1': 300, '무변화2': 4890, '무변화3': 29250}
'''
tc = '판서1'
print(tc + ' 양극단 검사')
video.get_extream_similarity_MSE(sample1_sf[tc], sample1_ef[tc], SAMPLE1_PATH, True, True)
video.get_extream_similarity_SSIM(sample1_sf[tc], sample1_ef[tc], SAMPLE1_PATH, True, True)
video.get_extream_absdiff(sample1_sf[tc], sample1_ef[tc], SAMPLE1_PATH, True, True)
print()

tc = '장면전환1'
print(tc + ' 양극단 검사')
video.get_extream_similarity_MSE(sample1_sf[tc], sample1_ef[tc], SAMPLE1_PATH, True, True)
video.get_extream_similarity_SSIM(sample1_sf[tc], sample1_ef[tc], SAMPLE1_PATH, True, True)
video.get_extream_absdiff(sample1_sf[tc], sample1_ef[tc], SAMPLE1_PATH, True, True)
print()

tc = '무변화1'
print(tc + ' 양극단 검사')
video.get_extream_similarity_SSIM(sample1_sf[tc], sample1_ef[tc], SAMPLE1_PATH, True, True)
video.get_extream_similarity_MSE(sample1_sf[tc], sample1_ef[tc], SAMPLE1_PATH, True, True)
video.get_extream_absdiff(sample1_sf[tc], sample1_ef[tc], SAMPLE1_PATH, True, True)
print()

'''


'''
f = open('sample2.txt','r')
sample2_tc = f.read().strip().split('\n')
for i in range(len(sample2_tc)):
    sample2_tc[i] = sample2_tc[i].strip().split()
for i in range(len(sample2_tc)):
    sample2_tc[i][1] = int(sample2_tc[i][1])*30
    sample2_tc[i][2] = int(sample2_tc[i][2])*30

tc = '판서1'
print(tc + ' 양극단 검사')
video.get_extream_similarity_MSE(sample2_tc[0][1], sample2_tc[0][2], PATH, True, True)
video.get_extream_similarity_SSIM(sample2_tc[0][1], sample2_tc[0][2], PATH, True, True)
video.get_extream_absdiff(sample2_tc[0][1], sample2_tc[0][2], PATH, True, True)
print()
'''
