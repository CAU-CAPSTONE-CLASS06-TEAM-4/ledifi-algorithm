from skimage.metrics import structural_similarity as compare_ssim
import cv2

SAMPLE1_TC = '무변화' # 장면전환, 판서, 무변화
SAMPLE_PLAY = 0

### 프레임 추출 ###

SAMPLE1_PATH = "C:/Users/Master/Desktop/캡스톤 깃허브/sample1.mp4"
SAMPLE2_PATH = "C:/Users/Master/Desktop/캡스톤 깃허브/sample2.mp4"

capture = cv2.VideoCapture(SAMPLE1_PATH)    #테스팅용 샘플 경로로 비디오캡쳐 객체 생성하여 capture에 저장

if SAMPLE1_TC == '장면전환':
    start_frame = 300     #임의의 시작 프레임
    end_frame = 420       #임의의 끝 프레임
elif SAMPLE1_TC == '판서':
    start_frame = 42000     
    end_frame = 42300       
elif SAMPLE1_TC == '무변화':
    start_frame = 0     
    end_frame = 300       

frame_list = []         #시작부터 끝 프레임을 저장하는 리스트

capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)   #현재 프레임을 시작 프레임으로 변경
end_frame -= start_frame                 #루프 위해서 엔드 프레임 설정

while end_frame>0:                        #엔드 프레임 다할때까지

    success, image = capture.read()     #캡쳐 읽어오기.
    if success: frame_list.append(image) 
    else:
        print("뭔가 잘못됐.. 개굴!")
        break
    end_frame-=1

capture.release()   #캡쳐 끝났으니 릴리즈. 정보는 이제 frame_list에 들어있다.

### TEST CODE ###

if SAMPLE_PLAY:
    for i in range(len(frame_list)):
        cv2.imshow('wow', frame_list[i])
        cv2.waitKey(2)


### 변화율 측정 ###

# end - start
simage = frame_list[0]
eimage = frame_list[len(frame_list)-1]
grayS = cv2.cvtColor(simage, cv2.COLOR_BGR2GRAY)
grayE = cv2.cvtColor(eimage, cv2.COLOR_BGR2GRAY)

score, diff = compare_ssim(grayS, grayE, full=True)
diff = (diff * 255).astype('uint8')
print('극값 변화율 : %.6f' %score)

'''
cv2.imshow('start', grayS)
cv2.imshow('end', grayE)
cv2.imshow('diff', diff)
'''

if cv2.waitKey(0) and 0xFF == ord('q'):
    cv2.destroyAllWindows()

# average
avg = []
for i in range(len(frame_list)-1):
    i1 = frame_list[i]
    i2 = frame_list[i+1]
    gray1 = cv2.cvtColor(i1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(i2, cv2.COLOR_BGR2GRAY)

    score, idff = compare_ssim(gray1, gray2, full=True)
    diff = (diff * 255).astype('uint8')
    avg.append(score)

avg = sum(avg)/len(avg)
print('평균 변화율 : %.6f' %avg)