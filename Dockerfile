FROM ubuntu:jammy
RUN apt-get update && \
    apt-get install python3-pip git curl --yes && \
    pip3 install -U pip setuptools waitress
# clone repo
WORKDIR /usr/local/src
RUN git clone https://github.com/mfranzil/RSSFeedGenerator.git
WORKDIR /usr/local/src/RSSFeedGenerator
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "app.py"]
