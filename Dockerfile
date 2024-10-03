# Python 3.12-slim 이미지 기반으로 설정 (최소한의 라이브러리 포함)
FROM python:3.12-slim

# 컨테이너 내 작업 디렉토리 설정
WORKDIR /app

# 로컬의 requirements.txt 파일을 컨테이너로 복사
COPY requirements.txt .

# 필요한 Python 패키지들을 설치
RUN pip install --no-cache-dir -r requirements.txt

# 현재 디렉토리의 모든 파일을 컨테이너 내 작업 디렉토리로 복사
COPY . .

# 컨테이너가 실행될 때 'run.py'를 실행
CMD ["python", "run.py"]
