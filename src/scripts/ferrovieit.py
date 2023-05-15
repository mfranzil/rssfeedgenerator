# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

from src.config import DEFAULT_HEADER_DESKTOP, DEFAULT_TIMEOUT_CONNECTION
from src.scripts.common.common import refresh_feed as common_refresh_feed


def scrap_nuova_ss(url):
    list_of_articles = []

    pagedesktop = requests.get(url, headers=DEFAULT_HEADER_DESKTOP, timeout=DEFAULT_TIMEOUT_CONNECTION)
    soupdesktop = BeautifulSoup(pagedesktop.text, "html.parser")

    article = 10

    for div in soupdesktop.find_all("div", attrs={"class": "notizia"}):
        try:
            __id = div.find("a")["href"]

            list_of_articles.append(__id)
            article -= 1
        except TypeError:
            print("Cannot find id for article")

        if article == 0:
            break

    return list_of_articles


def refresh_feed(rss_folder):
    return common_refresh_feed(
        rss_folder=rss_folder,
        base_url="https://www.ferrovie.it/portale/index.php",
        article_url="",
        scrapping_function=scrap_nuova_ss,
        feed_title="Ferrovie.it RSS Feed",
        feed_description="RSS feed degli articoli principali pubblicati da Ferrovie.it",
        feed_generator="Ferrovie.it (from RSS Feed Generator)"
    )
