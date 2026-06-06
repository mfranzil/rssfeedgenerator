# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

from src.config import DEFAULT_HEADER_DESKTOP, DEFAULT_TIMEOUT_CONNECTION
from src.scripts.common.common import refresh_feed as common_refresh_feed


def scrap_litra(url):
    list_of_articles = []

    pagedesktop = requests.get(url, headers=DEFAULT_HEADER_DESKTOP, timeout=DEFAULT_TIMEOUT_CONNECTION)
    soupdesktop = BeautifulSoup(pagedesktop.text, "html.parser")

    article = 10

    for div in soupdesktop.find_all("div", attrs={"class": "blog-grid__item"}):
        try:
            a = div.find("a", attrs={"class": "blog-grid__link"})
            if a is None:
                continue

            href = a["href"]

            if href not in list_of_articles:
                list_of_articles.append(href)
                article -= 1
        except (TypeError, KeyError):
            continue

        if article == 0:
            break

    return list_of_articles


def refresh_feed(rss_folder):
    return common_refresh_feed(
        rss_folder=rss_folder,
        base_url="https://www.litra.ch/fr/",
        article_url="https://www.litra.ch",
        scraping_function=scrap_litra,
        feed_title="LITRA RSS Feed",
        feed_description="RSS feed des actualités publiées par LITRA",
        feed_generator="LITRA (from RSS Feed Generator)"
    )
