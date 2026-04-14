# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

from src.config import DEFAULT_HEADER_DESKTOP, DEFAULT_TIMEOUT_CONNECTION
from src.scripts.common.common import refresh_feed as common_refresh_feed


def scrap_railwaygazette(url):
    list_of_articles = []

    pagedesktop = requests.get(url, headers=DEFAULT_HEADER_DESKTOP, timeout=DEFAULT_TIMEOUT_CONNECTION)
    soupdesktop = BeautifulSoup(pagedesktop.text, "html.parser")

    article = 15

    for h2 in soupdesktop.find_all("h2"):
        try:
            a = h2.find("a", href=True)
            if a is None:
                continue

            href = a["href"]

            if ".article" not in href:
                continue

            # Skip sponsored content, white papers, tenders
            if any(s in href for s in ["/sponsored-", "/white-papers/", "/tenders-and-jobs/"]):
                continue

            # Normalize to full URL
            if href.startswith("/"):
                href = "https://www.railwaygazette.com" + href

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
        base_url="https://www.railwaygazette.com/news",
        article_url="",
        scrapping_function=scrap_railwaygazette,
        feed_title="Railway Gazette RSS Feed",
        feed_description="RSS feed of the latest articles published by Railway Gazette",
        feed_generator="Railway Gazette (from RSS Feed Generator)"
    )
