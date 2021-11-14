from skimage.metrics import structural_similarity as compare_ssim
import cv2
import numpy

### 영상 정보 ###

def get_length(path):
    capture = cv2.VideoCapture(path)
    return capture.get(cv2.CAP_PROP_FRAME_COUNT)

def get_fps(path):
    capture = cv2.VideoCapture(path)
    return capture.get(cv2.CAP_PROP_FPS)

### 프레임 구간 전체 추출 ### 

def video_slice_full(start_frame:int, end_frame:int, path: str):     
    capture = cv2.VideoCapture(path)    #경로 파일의 비디오캡쳐 객체 생성
    frame_list = []
    
    capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame) #현재 프레임을 시작 프레임으로 변경
    end_frame -= start_frame

    while end_frame>0:                      #엔드 프레임 다할때까지
        success, image = capture.read()      #캡쳐 읽어오기
        if success: frame_list.append(image) #성공시 frame_list에 저장
        else:                                #실패
            print("vrc.video_slice_full: error")
            return
        end_frame-=1

    capture.release()   #캡쳐 끝났으니 릴리즈
    return frame_list

### 프레임 양극단 추출
def video_slice_boundary(start_frame:int, end_frame:int, path: str):     
    capture = cv2.VideoCapture(path)    #경로 파일의 비디오캡쳐 객체 생성
    frames = []
    
    capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame) #현재 프레임을 시작 프레임으로 변경
    success, image = capture.read()
    if success: frames.append(image)

    capture.set(cv2.CAP_PROP_POS_FRAMES, end_frame) #현재 프레임을 시작 프레임으로 변경
    success, image = capture.read()
    if success: frames.append(image)

    capture.release()   #캡쳐 끝났으니 릴리즈
    return frames

### 프레임 재생(테스팅용) ###

def video_play(start_frame:int, end_frame: int, path: str, waitkey: int):
    frame_list = video_slice_full(start_frame, end_frame, path)
    for i in range(len(frame_list)):
        cv2.imshow('video_play_testing', frame_list[i])
        cv2.waitKey(waitkey)
    cv2.destroyAllWindows()

### SSIM 극값 유사도 측정 ###

def get_extream_similarity_SSIM(start_frame:int, end_frame: int, path: str, imshow: bool):
    score, diff = compare_ssim(start_frame, end_frame, full=True)
    diff = (diff * 255).astype('uint8')

    if imshow:
        print('SSIM 양극단 유사도 : %.6f' %score)
        cv2.imshow('start', start_frame)
        cv2.imshow('end', end_frame)
        cv2.imshow('diff', diff)
        while not (cv2.waitKey(1) & 0xFF == ord('q')):
            pass
        cv2.destroyAllWindows()

    return score


### MSE 극값 오차 측정 ###

def get_extream_similarity_MSE(start_frame:int, end_frame: int, path: str, imshow: bool):
    err = numpy.sum((start_frame.astype("float") - end_frame.astype("float"))**2)
    err /= float(start_frame.shape[0] * end_frame.shape[1])

    if imshow:
        print('MSE 양극단 오차 : %.6f' %err)
        cv2.imshow('start', start_frame)
        cv2.imshow('end', end_frame)
        while not (cv2.waitKey(1) & 0xFF == ord('q')):
            pass
        cv2.destroyAllWindows()

    return err

### absdiff 극값 ###
def get_extream_absdiff(start_frame:int, end_frame: int, path: str, imshow: bool):
    diff = cv2.absdiff(start_frame, end_frame)
    _, diff = cv2.threshold(diff, 30, 255, cv2. THRESH_BINARY)

    cnt, _, stats, _ = cv2.connectedComponentsWithStats(diff)
    for i in range(1, cnt):
        x, y, w, h ,s = stats[i]
        if s < 100: continue
        cv2.rectangle(start_frame, (x, y, w, h), (0, 0, 255), 2)

    val = numpy.sum((diff.astype("float")))
    if val == 0: val = False
    else: val = True

    if imshow:
        #val = (diff * 255).astype('uint8')    
        print('absdiff 양극단 검사 결과 : ' + str(val))    
        cv2.imshow('start', start_frame)
        cv2.imshow('end', end_frame)
        cv2.imshow('diff', diff)
        while not (cv2.waitKey(1) & 0xFF == ord('q')):
            pass
        cv2.destroyAllWindows()

    return val

### 메인 테스팅 ##

def video_chk(path, lst, TRANSITION_THRES, WRITING_THRES, DEBUG:bool):
    path += '.mp4'
    for i in range(len(lst)):       ## 테스트 결과에 대한 루프. 
        start = lst[i][1] 
        end = lst[i][2]

        frames = video_slice_boundary(start, end, path)  
        grayS = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
        grayE = cv2.cvtColor(frames[1], cv2.COLOR_BGR2GRAY)

        grayS = cv2.GaussianBlur(grayS, (0,0), 1.0)
        grayE = cv2.GaussianBlur(grayE, (0,0), 1.0)

        ### 장면 전환 여부 판단 ###
        if get_extream_similarity_SSIM(grayS, grayE, path, DEBUG) < TRANSITION_THRES:
            res = 'transition'
        
        ### 장면 전환은 아닌 경우, 무변화를 판단 ###
        elif int(get_extream_absdiff(grayS, grayE, path, DEBUG)) == 0:
            res = 'no_change'
        
        ### 무변화도 아닌 경우, 판서를 판단 ###
        elif get_extream_similarity_MSE(grayS, grayE, path, DEBUG) > WRITING_THRES:
            res = 'writing'

        ### 셋 다 아닌 경우, 레이저 포인터같은 아주 미세한 변화 ###
        else:
            res = 'dot'

        lst[i] += [res]

    return lst
