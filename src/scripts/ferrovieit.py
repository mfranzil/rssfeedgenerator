# -*- coding: utf-8 -*-
import os
import requests

from bs4 import BeautifulSoup
from readability import Document

from src.scripts.common.common import DEFAULT_HEADER_DESKTOP, DEFAULT_TIMEOUT_CONNECTION, make_feed, add_feed
from src.config import FEED_FILENAME

list_of_articles = []
header_desktop = DEFAULT_HEADER_DESKTOP
timeout_connection = DEFAULT_TIMEOUT_CONNECTION


def scrap_nuova_ss(url):
    pagedesktop = requests.get(url, headers=header_desktop, timeout=timeout_connection)
    soupdesktop = BeautifulSoup(pagedesktop.text, "html.parser")

    # Ottengo i primi 20 articoli di rilievo
    article = 10

    for div in soupdesktop.find_all("div", attrs={"class": "notizia"}):
        try:
            __id = div.find("a")["href"]

            list_of_articles.append(__id)
            article -= 1
        except TypeError:
            print("Cannot find id for article")

        # if __id not in disallowed_ids and article > 0:
        #    list_of_articles.append(div.find("h3", attrs={"class": "teaser-title"}).find("a")["href"])
        #    article -= 1


def refresh_feed(rss_folder):
    url = "https://www.ferrovie.it/portale/index.php"
    rss_file = os.path.join(rss_folder, FEED_FILENAME)

    # Acquisisco l'articolo principale
    scrap_nuova_ss(url)

    make_feed(
        rss_file=rss_file,
        feed_title="Ferrovie.it RSS Feed",
        feed_description="RSS feed degli articoli principali pubblicati da Ferrovie.it",
        feed_generator="Ferrovie.it (from RSS Feed Generator)"
    )

    # Analizzo ogni singolo articolo rilevato
    for urlarticolo in list_of_articles:
        try:
            response = requests.get(
                urlarticolo,
                headers=header_desktop,
                timeout=timeout_connection)

            description = Document(response.text).summary()
            title = Document(response.text).short_title()
            add_feed(
                rss_file=rss_file,
                feed_title=title,
                feed_description=description,
                feed_link=urlarticolo)
        except Exception as e:
            print("Failed to add article: " + str(e))
