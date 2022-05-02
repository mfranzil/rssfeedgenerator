# -*- coding: utf-8 -*-
import os
from src.config import FEED_PATH

import pathlib
import requests

from bs4 import BeautifulSoup
from readability import Document

from src.scripts.common.common import make_feed, add_feed

FEED_NAME = "domani"

header_desktop = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:80.0) Gecko/20100101 Firefox/80.0",
    "Accept-Language": "it,en-US;q=0.7,en;q=0.3"
}

timeoutconnection = 120

rss_folder = os.path.join(FEED_PATH, FEED_NAME)
pathlib.Path(rss_folder).mkdir(parents=True, exist_ok=True)
rss_file = os.path.join(rss_folder, "feed.xml")

# Niente articoli editoriali o video
disallowed_ids = ["video", "idee"]

list_of_articles = []


def scrap_domani(url):
    pagedesktop = requests.get(url, headers=header_desktop, timeout=timeoutconnection)
    soupdesktop = BeautifulSoup(pagedesktop.text, "html.parser")

    # Ottengo i primi 30 articoli di rilievo
    article = 30

    for div in soupdesktop.find_all("div", attrs={"class": "teaser-content"}):
        __id = div.find("h3", attrs={"class": "teaser-title"}).find("a")["href"].split("/")[1]
        if __id not in disallowed_ids and article > 0:
            list_of_articles.append(div.find("h3", attrs={"class": "teaser-title"}).find("a")["href"])
            article -= 1


def main():
    url = "https://www.editorialedomani.it/"

    # Acquisisco l'articolo principale
    scrap_domani(url)

    # Se non esiste localmente un file XML procedo a crearlo.
    if os.path.exists(rss_file) is not True:
        make_feed(
            rss_file=rss_file,
            feed_title="Domani RSS Feed",
            feed_description="RSS feed degli articoli principali pubblicati da Domani",
            feed_generator="Domani (from RSS Feed Generator)"
            )

    # Analizzo ogni singolo articolo rilevato
    for urlarticolo in list_of_articles:
        response = requests.get(url[:-1] + urlarticolo, headers=header_desktop, timeout=timeoutconnection)

        description = Document(response.text).summary()
        title = Document(response.text).short_title()
        add_feed(
            rss_file=rss_file,
            feed_title=title,
            feed_description=description,
            feed_link=url[:-1] + urlarticolo)


if __name__ == "__main__":
    main()
