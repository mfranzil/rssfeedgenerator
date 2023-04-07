# -*- coding: utf-8 -*-
import os
import requests

from bs4 import BeautifulSoup
from readability import Document

from src.scripts.common.common import DEFAULT_HEADER_DESKTOP, DEFAULT_TIMEOUT_CONNECTION, make_feed, add_feed
from src.config import FEED_FILENAME

header_desktop = DEFAULT_HEADER_DESKTOP
timeout_connection = DEFAULT_TIMEOUT_CONNECTION


def scrap_ecleticlight(url):
    list_of_articles = []

    pagedesktop = requests.get(url, headers=header_desktop, timeout=timeout_connection)
    soupdesktop = BeautifulSoup(pagedesktop.text, "html.parser")

    # Ottengo i primi 8 articoli di rilievo
    article = 8

    for div in soupdesktop.find_all("article", attrs={"class": "post"}):
        if article > 0:
            list_of_articles.append(div.find("header", attrs={"class": "entry-header"}).find("a")["href"])
            article -= 1

    return list_of_articles


def refresh_feed(rss_folder):
    url = "https://eclecticlight.co/category/macs/"
    rss_file = os.path.join(rss_folder, FEED_FILENAME)

    # Acquisisco l'articolo principale
    list_of_articles = scrap_ecleticlight(url)

    make_feed(
        rss_file=rss_file,
        feed_title="Ecletic Light RSS Feed",
        feed_description="RSS feed degli articoli con tag 'Macs' pubblicati da Ecletic Light",
        feed_generator="Ecletic Light (from RSS Feed Generator)"
    )

    # Analizzo ogni singolo articolo rilevato
    for urlarticolo in list_of_articles:
        response = requests.get(urlarticolo, headers=header_desktop, timeout=timeout_connection)

        description = Document(response.text).summary()
        title = Document(response.text).short_title()
        add_feed(
            rss_file=rss_file,
            feed_title=title,
            feed_description=description,
            feed_link=urlarticolo)
