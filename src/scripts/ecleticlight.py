# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

from src.config import DEFAULT_HEADER_DESKTOP, DEFAULT_TIMEOUT_CONNECTION
from src.scripts.common.common import refresh_feed as common_refresh_feed


def scrap_ecleticlight(url):
    list_of_articles = []

    pagedesktop = requests.get(url, headers=DEFAULT_HEADER_DESKTOP, timeout=DEFAULT_TIMEOUT_CONNECTION)
    soupdesktop = BeautifulSoup(pagedesktop.text, "html.parser")

    # Ottengo i primi 8 articoli di rilievo
    article = 8

    for div in soupdesktop.find_all("article", attrs={"class": "post"}):
        if article > 0:
            list_of_articles.append(div.find("header", attrs={"class": "entry-header"}).find("a")["href"])
            article -= 1

    return list_of_articles


def refresh_feed(rss_folder):
    return common_refresh_feed(
        rss_folder=rss_folder,
        base_url="https://eclecticlight.co/category/macs/",
        article_url="",
        scrapping_function=scrap_ecleticlight,
        feed_title="EcleticLight RSS Feed",
        feed_description="RSS feed degli articoli principali pubblicati da EcleticLight",
        feed_generator="EcleticLight (from RSS Feed Generator)"
    )
