## ccsv, climate change spiral visualization

FROM python:3.9

WORKDIR /workspace

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Jupyter SSL 인증서 복사
COPY ssl /root/.jupyter/ssl

# 작업 디렉토리 복사
COPY . .

# 포트 개방
EXPOSE 8888

# CSV 변환 후 Jupyter 실행 (쉘 방식)
CMD bash -c "python convert_csv.py && jupyter lab \
  --allow-root \
  --ip=0.0.0.0 \
  --port=8888 \
  --no-browser \
  --NotebookApp.token='' \
  --certfile=/root/.jupyter/ssl/cert.pem \
  --keyfile=/root/.jupyter/ssl/key.pem"