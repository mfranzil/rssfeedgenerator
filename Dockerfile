FROM python:3.11.3-slim
COPY . /usr/local/src/rssfeed
WORKDIR /usr/local/src/rssfeed
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "app.py"]
