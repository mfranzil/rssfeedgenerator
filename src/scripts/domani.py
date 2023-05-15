# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

from src.config import DEFAULT_HEADER_DESKTOP, DEFAULT_TIMEOUT_CONNECTION
from src.scripts.common.common import refresh_feed as common_refresh_feed

# Niente articoli editoriali o video
disallowed_ids = ["video", "idee"]


def scrap_domani(url):
    list_of_articles = []

    pagedesktop = requests.get(url, headers=DEFAULT_HEADER_DESKTOP, timeout=DEFAULT_TIMEOUT_CONNECTION)
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

    return list_of_articles


def refresh_feed(rss_folder):
    url = "https://www.editorialedomani.it/"
    return common_refresh_feed(
        rss_folder=rss_folder,
        base_url=url,
        article_url=url[:-1],
        scrapping_function=scrap_domani,
        feed_title="Domani RSS Feed",
        feed_description="RSS feed degli articoli principali pubblicati da Domani",
        feed_generator="Domani (from RSS Feed Generator)"
    )
