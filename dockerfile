FROM python:3.8 as compile-image

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN /opt/venv/bin/python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt
RUN apt-get update
RUN apt-get install -y ffmpeg libsm6 libxext6 
RUN apt-get install -y openssh-server
COPY app /app
EXPOSE 7000
CMD ["uvicorn", "app.main:app", "--port", "7000", "--host", "0.0.0.0", "--reload"]

# build docker
#   docker build -t face-reco-app .
# run docker
#   docker run -p 7000:7000 face-reco-app