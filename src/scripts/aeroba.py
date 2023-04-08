# -*- coding: utf-8 -*-
import os
import requests

import logging as log
from bs4 import BeautifulSoup
from readability import Document

from src.scripts.common.common import DEFAULT_HEADER_DESKTOP, DEFAULT_TIMEOUT_CONNECTION, make_feed, add_feed
from src.config import FEED_FILENAME

header_desktop = DEFAULT_HEADER_DESKTOP
timeout_connection = DEFAULT_TIMEOUT_CONNECTION

def scrap_aeroba(url):
    list_of_articles = []

    pagedesktop = requests.get(url, headers=header_desktop, timeout=timeout_connection)
    soupdesktop = BeautifulSoup(pagedesktop.text, "html.parser")

    # Ottengo il bollettino della settimana
    for p in soupdesktop.find_all("p"):
        try:
            pdf = p.find("a")["href"]
        except KeyError:
            continue
        if "bollettino" in pdf.lower():
            list_of_articles.append(pdf)
            break

    return list_of_articles


def refresh_feed(rss_folder):
    url = "https://aeroba.fmach.it/bollettino"
    rss_file = os.path.join(rss_folder, FEED_FILENAME)

    # Acquisisco l'articolo principale
    list_of_articles = scrap_aeroba(url)

    make_feed(
        rss_file=rss_file,
        feed_title="AeroBA RSS Feed",
        feed_description="RSS feed dei bollettini pollini della Fondazione Mach",
        feed_generator="AeroBA FEM (from RSS Feed Generator)"
    )

    # Analizzo ogni singolo articolo rilevato
    for urlarticolo in list_of_articles:
        prefix = '/'.join(url.split('/')[:-1])
        urlarticolo = prefix + urlarticolo
        try:
            response = requests.get(urlarticolo, headers=header_desktop, timeout=timeout_connection)
        except Exception as e:
            log.error(f"Aborting scrapping of article {urlarticolo} because an error occurred : {e}")
            continue

        if response.status_code == 404:
            log.warning(f"The requested page does not exists: {urlarticolo}")
            continue

        description = f"E' disponibile un nuovo bollettino per il download." + \
            f"\n<a href=\"{urlarticolo}\">{urlarticolo}</a>"
        title = "Nuovo bollettino AeroBA!"

        add_feed(
            rss_file=rss_file,
            feed_title=title,
            feed_description=description,
            feed_link=urlarticolo)
