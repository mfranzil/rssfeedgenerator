FROM ubuntu:jammy
RUN apt-get update && \
    apt-get install python3-pip git curl --yes && \
    pip3 install -U pip setuptools waitress
WORKDIR /usr/local/src
# copy the app
COPY . /usr/local/src/RSSFeedGenerator
WORKDIR /usr/local/src/RSSFeedGenerator
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "app.py"]
