# -*- coding: utf-8 -*-
import os
import requests

from bs4 import BeautifulSoup
from readability import Document

from src.scripts.common.common import DEFAULT_HEADER_DESKTOP, DEFAULT_TIMEOUT_CONNECTION, make_feed, add_feed
from src.config import FEED_FILENAME

import logging as log

list_of_articles = []
header_desktop = DEFAULT_HEADER_DESKTOP
timeout_connection = DEFAULT_TIMEOUT_CONNECTION


def scrap_fip(url, mode, section):
    pagedesktop = requests.get(url, headers=header_desktop, timeout=timeout_connection)
    soupdesktop = BeautifulSoup(pagedesktop.text, "html.parser")

    articles = 25

    tmp = []
    for div in soupdesktop.find_all('h3'):
        if div.find('a'):
            tmp.append(div.find('a')['href'])
        if len(tmp) >= articles:
            break

    for link in tmp:
        if link == "" or link is None:
            continue

        if not link.startswith("http"):
            log.warning(f"Invalid URL format: {link}")

        list_of_articles.append(link)

    return list_of_articles


def refresh_feed(rss_folder, request):
    url = request["url"]
    mode = request["mode"]
    section = request["section"]
    # if request["required_url_substring"] and request["required_url_substring"] is not None:
    #    required_url_substring = request["required_url_substring"].lower()
    # else:
    #     required_url_substring = None

    rss_file = os.path.join(rss_folder, FEED_FILENAME)

    # Acquisisco l'articolo principale
    list_of_articles = scrap_fip(url, mode, section)

    # Se non esiste localmente un file XML procedo a crearlo.
    if not os.path.exists(rss_file):
        make_feed(
            rss_file=rss_file,
            feed_title=request["sentences"]["feed_title"],
            feed_description=request["sentences"]["feed_description"],
            feed_generator=request["sentences"]["feed_generatore"]
        )

    # Analizzo ogni singolo articolo rilevato
    for urlarticolo in sorted(list_of_articles):
        try:
            response = requests.get(urlarticolo, headers=header_desktop, timeout=timeout_connection)
        except Exception as e:
            log.error(f"Aborting scrapping of article {urlarticolo} because an error occurred : {e}")
            continue

        if response.status_code == 404:
            log.warning(f"The requested page does not exists: {urlarticolo}")
            continue

        if "pdf" in urlarticolo:
            description = f"E' disponibile {request['sentences']['new_object']}" \
                + f" per il download.\n<a href=\"{urlarticolo}\">{urlarticolo}</a>"
            title = urlarticolo.split("/")[-1]
        else:
            description = Document(response.text).summary()
            title = Document(response.text).short_title()

        if not title or title is None or title == "":
            title = urlarticolo

        add_feed(
            rss_file=rss_file,
            feed_title=title,
            feed_description=description,
            feed_link=urlarticolo
        )
