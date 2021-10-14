from skimage.metrics import structural_similarity as compare_ssim
import cv2

### 프레임 추출 ### 

def video_slice(start_frame:int, end_frame:int, path: str):     
    capture = cv2.VideoCapture(path)    #경로 파일의 비디오캡쳐 객체 생성
    frame_list = []
    
    capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame) #현재 프레임을 시작 프레임으로 변경
    end_frame -= start_frame

    while end_frame>0:                      #엔드 프레임 다할때까지
        success, image = capture.read()      #캡쳐 읽어오기
        if success: frame_list.append(image) #성공시 frame_list에 저장
        else:                                #실패
            print("vrc.video_slice: error")
            return
        end_frame-=1

    capture.release()   #캡쳐 끝났으니 릴리즈
    return frame_list

### 프레임 재생(테스팅용) ###

def video_play(start_frame:int, end_frame: int, path: str, waitkey: int):
    frame_list = video_slice(start_frame, end_frame, path)
    for i in range(len(frame_list)):
        cv2.imshow('video_play_testing', frame_list[i])
        cv2.waitKey(waitkey)
    cv2.destroyAllWindows()

### 극값 유사도 측정 ###

def get_extream_similarity(start_frame:int, end_frame: int, path: str, imshow: bool):
    frame_list = video_slice(start_frame, end_frame, path)  
    grayS = cv2.cvtColor(frame_list[0], cv2.COLOR_BGR2GRAY)
    grayE = cv2.cvtColor(frame_list[len(frame_list)-1], cv2.COLOR_BGR2GRAY)

    score, diff = compare_ssim(grayS, grayE, full=True)
    diff = (diff * 255).astype('uint8')
    print('양극단 유사도 : %.6f' %score)

    if imshow:
        cv2.imshow('start', grayS)
        cv2.imshow('end', grayE)
        cv2.imshow('diff', diff)
        while not (cv2.waitKey(1) & 0xFF == ord('q')):
            pass
        cv2.destroyAllWindows()

    return score

### 평균 유사도 측정 ###

def get_average_similarity(start_frame:int, end_frame: int, path: str, tic: int, imshow: bool):  
    if tic < 1: 
        print("tic must be bigger than 0")
        return

    frame_list = video_slice(start_frame, end_frame, path)  
    sliced_frame = []
    for i in range(0, len(frame_list), tic):
        sliced_frame.append(frame_list[i])

    avg = 0

    for i in range(len(sliced_frame)-1):
        i1 = sliced_frame[i]
        i2 = sliced_frame[i+1]
        gray1 = cv2.cvtColor(i1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(i2, cv2.COLOR_BGR2GRAY)

        score, diff = compare_ssim(gray1, gray2, full=True)
        diff = (diff * 255).astype('uint8')
        avg+=score

        if imshow:
            print('similarity of %dth loop: %.6f' %(i, score))
            cv2.imshow(str(i) + "th image", i1)
            cv2.imshow(str(i+1) + "th image", i2)
            cv2.imshow('diff between '+str(i)+'th and ' + str(i+1) + 'th', diff)
            while not (cv2.waitKey(1) & 0xFF == ord('q')):
                pass
            cv2.destroyAllWindows()
    avg /= (len(sliced_frame)-1)
    print('평균 유사도 : %.6f' %avg)

    return avg

### 판서 추적 결과 ###

def note_track():    
    pass