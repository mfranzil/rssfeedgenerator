# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

from src.config import DEFAULT_HEADER_DESKTOP, DEFAULT_TIMEOUT_CONNECTION
from src.scripts.common.common import refresh_feed as common_refresh_feed


def scrap_swissinfo(url):
    list_of_articles = []

    pagedesktop = requests.get(url, headers=DEFAULT_HEADER_DESKTOP, timeout=DEFAULT_TIMEOUT_CONNECTION)
    soupdesktop = BeautifulSoup(pagedesktop.text, "html.parser")

    article = 25

    for a in soupdesktop.find_all("a", attrs={"class": "teaser-card__link"}):
        try:
            href = a["href"]

            if "/ita/" not in href or '/eng/' not in href:
                continue

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
        base_url="https://www.swissinfo.ch/ita/",
        article_url="",
        scrapping_function=scrap_swissinfo,
        feed_title="Swissinfo RSS Feed",
        feed_description="RSS feed degli articoli principali pubblicati da Swissinfo in italiano",
        feed_generator="Swissinfo (from RSS Feed Generator)"
    )
