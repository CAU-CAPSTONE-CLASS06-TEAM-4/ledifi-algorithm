import video

SAMPLE1_PATH = "C:/Users/Master/Desktop/캡스톤 깃허브/sample1.mp4"
SAMPLE2_PATH = "C:/Users/Master/Desktop/캡스톤 깃허브/sample2.mp4"

sample1_sf = {'장면전환1':300, '장면전환2': 120690, '장면전환3': 126000, '장면전환4':103290,
                '판서1': 42000, '판서2': 76140, '판서3': 104250,
                '무변화1': 0, '무변화2': 4740, '무변화3': 29100}

sample1_ef = {'장면전환1':420, '장면전환2': 120840, '장면전환3': 126300, '장면전환4':103430,
                '판서1': 42300, '판서2': 76350, '판서3': 104550,
                '무변화1': 300, '무변화2': 4890, '무변화3': 29250}

def sample1_testing(text, slice):
    print(text)
    #video.video_play(sample1_sf[text], sample1_ef[text], SAMPLE1_PATH, 2)
    video.get_extream_similarity(sample1_sf[text], sample1_ef[text], SAMPLE1_PATH, True)
    #video.get_average_similarity(sample1_sf[text], sample1_ef[text], SAMPLE1_PATH, int((sample1_ef[text]-sample1_sf[text])/slice), False)
    print()

slice = 5
#sample1_testing('장면전환1', slice)
#sample1_testing('장면전환2', slice)
#sample1_testing('장면전환3', slice)
#sample1_testing('장면전환4', slice)
#sample1_testing('판서1', slice)
#sample1_testing('판서2', slice)
#sample1_testing('판서3', slice)
sample1_testing('무변화1', slice)
#sample1_testing('무변화2', slice)
#sample1_testing('무변화3', slice)