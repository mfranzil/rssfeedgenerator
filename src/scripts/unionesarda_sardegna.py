# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

from src.config import DEFAULT_HEADER_DESKTOP, DEFAULT_TIMEOUT_CONNECTION
from src.scripts.common.common import refresh_feed as common_refresh_feed


def scrap_nuova_ss(url):
    list_of_articles = []

    pagedesktop = requests.get(url, headers=DEFAULT_HEADER_DESKTOP, timeout=DEFAULT_TIMEOUT_CONNECTION)
    soupdesktop = BeautifulSoup(pagedesktop.text, "html.parser")

    articles = 15

    for div in soupdesktop.find_all("h3", attrs={"class": "teaser-title"}):
        try:
            __id = div.find("a")["href"]

            if not __id.startswith("/news-sardegna/"):
                continue

            list_of_articles.append(__id)
            articles -= 1

            if articles == 0:
                break
        except TypeError:
            print("Cannot find id for article")

    return list_of_articles


def refresh_feed(rss_folder):
    return common_refresh_feed(
        rss_folder=rss_folder,
        base_url="https://www.unionesarda.it/news-sardegna",
        article_url="https://www.unionesarda.it",
        scrapping_function=scrap_nuova_ss,
        feed_title="Unione Sarda RSS Feed",
        feed_description="RSS feed degli articoli principali pubblicati da Unione Sarda",
        feed_generator="Unione Sarda (from RSS Feed Generator)"
    )
