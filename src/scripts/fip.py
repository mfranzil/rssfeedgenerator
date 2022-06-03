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

    for div in soupdesktop.find_all("a"):
        if div['href']:
            # Exclude bad articles
            bad_articles = [
                "#",
                "https://www.fip.it/sportello/fiscale-legale",
                "https://servizi.fip.it",
                "/Regioni/trentinoaltoadige/Home/CookiesPolicy",
                "/Regioni/trentinoaltoadige/Home/PrivacyPolicy",
                "http://www.sendoc.it/",
                "http://www.fip.it/Regioni/trentinoaltoadige/Dolomitiacanestro",
                "https://www.fip.it",
                "/Regioni/trentinoaltoadige"
            ]
            if div["href"] in bad_articles:
                continue
            if not div["href"].startswith("https://www.fip.it"):
                div["href"] = "https://www.fip.it" + str(div["href"])
            list_of_articles.append(div["href"])
            article -= 1


def refresh_feed(rss_folder):
    url = "https://www.fip.it/Regioni/trentinoaltoadige/Comunicati/Comunicati?delibera=False"
    rss_file = os.path.join(rss_folder, FEED_FILENAME)

    # Acquisisco l'articolo principale
    scrap_domani(url)

    # Se non esiste localmente un file XML procedo a crearlo.
    if os.path.exists(rss_file) is not True:
        make_feed(
            rss_file=rss_file,
            feed_title="FIP RTN CU",
            feed_description="RSS feed dei comunicati ufficiali pubblicati da FIP Trentino-Alto-Adige",
            feed_generator="FIP RTN CU (from RSS Feed Generator)"
            )

    # Analizzo ogni singolo articolo rilevato
    for urlarticolo in list_of_articles:
        response = requests.get(urlarticolo, headers=header_desktop, timeout=timeout_connection)

        if "pdf" in urlarticolo:
            description = urlarticolo.split("/")[-1]
        else:
            description = Document(response.text).summary()

        title = Document(response.text).short_title()
        add_feed(
            rss_file=rss_file,
            feed_title=title,
            feed_description=description,
            feed_link=urlarticolo)


if __name__ == "__main__":
    refresh_feed(".")
