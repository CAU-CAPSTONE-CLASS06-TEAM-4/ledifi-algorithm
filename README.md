# ledifi-algorithm: 작업 공유용 README

## 1. 실행 환경 세팅

### 1) 폴더 다운로드

https://github.com/CAU-CAPSTONE-CLASS06-TEAM-4/ledifi-algorithm</br>

페이지에서 Code->Download ZIP

### 2) 라이브러리 세팅

개발환경의 cmd에서 __'pip install -r {ledifi-algorithm/requirements.txt의 경로}'__ 입력하여 라이브러리 설치</br>

__만약 librosa 설치 중 numba와 numpy 버전 이슈가 발생할 경우 'pip install numpy==1.20.3'__ 으로 하위버전 numpy 설치

## 2. 실행 및 동작

### 1) 소스코드 실행

cmd에서 __'python {ledifi-algorithm/main_filter.py의 경로} {영상의 경로} {setting.txt의 경로} '__ 입력

ex) python main_filter.py C:\\Users\\Master\\Desktop\\testpath\\sample01.mp4 C:\\Users\\Master\\Desktop\\testpath\\setting.txt 

### 2) 실행에 따른 경과

입력한 영상의 경로에, {영상파일이름}.wav 파일과 {영상파일이름}.txt로 결과가 출력됨.

ex) 결과 예시

FPS: 30
silence 327 501 transition
silence 1902 2088 transition
silence 6393 6531 transition
silence 18951 19059 no_change
silence 27924 28017 transition
silence 35217 35316 transition
silence 95934 96024 no_change
silence 99339 99459 writing
silence 116304 116430 transition
silence 120717 120825 transition