# ledifi-algorithm: 작업 공유용 README

## 1. 실행 환경 세팅

### 1) 폴더 다운로드

https://github.com/CAU-CAPSTONE-CLASS06-TEAM-4/ledifi-algorithm</br>

페이지에서 Code->Download ZIP

### 2) 라이브러리 세팅

개발환경의 cmd에서 __'pip install -r {ledifi-algorithm/requirements.txt의 경로}'__ 입력하여 라이브러리 설치</br>

__만약 librosa 설치 중 numba와 numpy 버전 이슈가 발생할 경우 'pip install numpy==1.20.3'__ 으로 하위버전 numpy 설치

## 2. 실행 및 동작

### 1) main_filter.py

#### (1) 소스코드 실행 

cmd에서 __'python {ledifi-algorithm/main_filter.py의 경로} {영상의 경로} {setting.txt의 경로} '__ 입력

ex) python main_filter.py C:\\Users\\Master\\Desktop\\testpath\\sample01.mp4 C:\\Users\\Master\\Desktop\\testpath\\setting.txt 

#### (2) 실행에 따른 경과

입력한 영상의 경로에, {영상파일이름}.wav 파일과 {영상파일이름}.txt로 결과가 출력됨.

ex) 결과 예시

FPS: 30</br>
silence 327 501 transition</br>
silence 1902 2088 transition</br>
silence 6393 6531 transition</br>
silence 18951 19059 no_change</br>
silence 27924 28017 transition</br>
silence 35217 35316 transition</br>
silence 95934 96024 no_change</br>
silence 99339 99459 writing</br>
silence 116304 116430 transition</br>
silence 120717 120825 transition</br>

### 2) result.py

#### (1) 소스코드 실행 

cmd에서 __'python {ledifi-algorithm/result.py의 경로} {원본영상의 경로} {선택 결과 텍스트 파일의 경로} '__ 입력

ex) python main_filter.py C:\\Users\\Master\\Desktop\\testpath\\sample01.mp4 C:\\Users\\Master\\Desktop\\testpath\\setting.txt 

__만약 실행 중 에러 발생시, cmd에 'pip install videopy'로 라이브러리 설치 후 진행__

#### (1-1) 선택 결과 텍스트 파일 예시

silence 327 501 transition True</br>
silence 1902 2088 transition True</br>
silence 6393 6531 transition True</br>
silence 18951 19059 no_change True</br>
...</br>
silence 99339 99459 writing False</br>
silence 116304 116430 transition True</br>
silence 120717 120825 transition True</br>

#### (2) 실행에 따른 경과

입력한 원본영상의 경로에, {영상파일이름}_result.mp4 생성됨.

