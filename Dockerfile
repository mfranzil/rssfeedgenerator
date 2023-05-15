FROM ubuntu:jammy
RUN apt-get update && \
    apt-get install python3-pip git curl --yes && \
    pip3 install -U pip setuptools waitress  && \
    rm -rf /usr/share/doc/* /usr/share/info/* /var/lib/apt/lists/*
COPY . /usr/local/src/RSSFeedGenerator
WORKDIR /usr/local/src/RSSFeedGenerator
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "app.py"]