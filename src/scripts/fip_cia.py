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


def scrap_cia(url):
    pagedesktop = requests.get(url, headers=header_desktop, timeout=timeout_connection)
    soupdesktop = BeautifulSoup(pagedesktop.text, "html.parser")

    # Ottengo i primi 8 articoli di rilievo
    article = 8

    for div in soupdesktop.find_all("div", attrs={"class": "listBkg"}):
        if div['onclick']:
            try:
                url = div['onclick'].split("'")[1].replace(" ", "%20")
            except Exception as e:
                continue

            list_of_articles.append(url)
            article -= 1

            if article == 0:
                break


def refresh_feed(rss_folder):
    url = f"https://www.fip.it/cia/Comunicato.asp"
    rss_file = os.path.join(rss_folder, FEED_FILENAME)

    # Acquisisco l'articolo principale
    scrap_cia(url)

    # Se non esiste localmente un file XML procedo a crearlo.
    if os.path.exists(rss_file) is not True:
        make_feed(
            rss_file=rss_file,
            feed_title=f"FIP - CIA - CU Nazionali",
            feed_description=f"RSS feed dei comunicati ufficiali del CIA (FIP)",
            feed_generator=f"FIP - CIA - CU Nazionali(from RSS Feed Generator)"
            )

    # Analizzo ogni singolo articolo rilevato
    for urlarticolo in list_of_articles:
        response = requests.get(urlarticolo, headers=header_desktop, timeout=timeout_connection)

        modified_url = urlarticolo.split("/")[-1].replace("%20", " ")

        if "pdf" in urlarticolo:
            description = f"E' disponibile un nuovo comunicato ufficiale per il download.\n" \
                + f"<a href=\"{urlarticolo}\">{modified_url}</a>"
        else:
            description = Document(response.text).summary()

        title = Document(response.text).short_title()
        if not title or title is None or title == "":
            title = modified_url

        add_feed(
            rss_file=rss_file,
            feed_title=title,
            feed_description=description,
            feed_link=urlarticolo)
