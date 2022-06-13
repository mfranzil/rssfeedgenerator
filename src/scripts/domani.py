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

# Niente articoli editoriali o video
disallowed_ids = ["video", "idee"]


def scrap_domani(url):
    pagedesktop = requests.get(url, headers=header_desktop, timeout=timeout_connection)
    soupdesktop = BeautifulSoup(pagedesktop.text, "html.parser")

    # Ottengo i primi 8 articoli di rilievo
    article = 8

    for div in soupdesktop.find_all("div", attrs={"class": "teaser-content"}):
        try:
            __id = div.find("h3", attrs={"class": "teaser-title"}).find("a")["href"].split("/")[1]
        except KeyError:
            continue
        if __id not in disallowed_ids and article > 0:
            list_of_articles.append(div.find("h3", attrs={"class": "teaser-title"}).find("a")["href"])
            article -= 1


def refresh_feed(rss_folder):
    url = "https://www.editorialedomani.it/"
    rss_file = os.path.join(rss_folder, FEED_FILENAME)

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
        response = requests.get(url[:-1] + urlarticolo, headers=header_desktop, timeout=timeout_connection)

        description = Document(response.text).summary()
        title = Document(response.text).short_title()
        add_feed(
            rss_file=rss_file,
            feed_title=title,
            feed_description=description,
            feed_link=url[:-1] + urlarticolo)
