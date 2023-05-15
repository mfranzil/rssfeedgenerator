# -*- coding: utf-8 -*-
import logging as log

import requests
from bs4 import BeautifulSoup

from src.config import DEFAULT_HEADER_DESKTOP, DEFAULT_TIMEOUT_CONNECTION
from src.scripts.common.common import refresh_feed as common_refresh_feed


def scrap_fip(url):
    pagedesktop = requests.get(url, headers=DEFAULT_HEADER_DESKTOP, timeout=DEFAULT_TIMEOUT_CONNECTION)
    soupdesktop = BeautifulSoup(pagedesktop.text, "html.parser")

    articles = 20

    list_of_articles = []
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
            continue

        # if section not in link:
        #     # if not link.startswith("/".join(url.split('/')[:-2])):
        #    log.warning(f"Invalid URL format: {link}")
        #   continue

        # if mode not in link:
        #    log.warning(f"Possible unwanted article found: {link}")

        list_of_articles.append(link)

    return list_of_articles


def refresh_feed(rss_folder, request):
    url = request["url"]

    return common_refresh_feed(
        rss_folder=rss_folder,
        base_url=url,
        article_url='/'.join(url.split('/')[:-1]),
        scrapping_function=scrap_fip,
        feed_title=request["sentences"]["feed_title"],
        feed_description=request["sentences"]["feed_description"],
        feed_generator=request["sentences"]["feed_generator"]
    )
