# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

from src.config import DEFAULT_HEADER_DESKTOP, DEFAULT_TIMEOUT_CONNECTION
from src.scripts.common.common import refresh_feed as common_refresh_feed


def scrap_sbb_news(url):
    list_of_articles = []

    pagedesktop = requests.get(url, headers=DEFAULT_HEADER_DESKTOP, timeout=DEFAULT_TIMEOUT_CONNECTION)
    soupdesktop = BeautifulSoup(pagedesktop.text, "html.parser")

    article = 10

    for card in soupdesktop.find_all("sbb-card"):
        try:
            a = card.find("a", href=True)
            if a is None:
                continue

            href = a["href"]

            if "/en/" not in href:
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
        base_url="https://news.sbb.ch/en",
        article_url="",
        scrapping_function=scrap_sbb_news,
        feed_title="SBB News RSS Feed",
        feed_description="RSS feed of the latest news published by SBB",
        feed_generator="SBB News (from RSS Feed Generator)"
    )
