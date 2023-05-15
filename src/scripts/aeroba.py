# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

from src.config import DEFAULT_HEADER_DESKTOP, DEFAULT_TIMEOUT_CONNECTION
from src.scripts.common.common import refresh_feed as common_refresh_feed


def scrap_aeroba(url):
    list_of_articles = []

    pagedesktop = requests.get(url, headers=DEFAULT_HEADER_DESKTOP, timeout=DEFAULT_TIMEOUT_CONNECTION)
    soupdesktop = BeautifulSoup(pagedesktop.text, "html.parser")

    # Ottengo il bollettino della settimana
    for p in soupdesktop.find_all("p"):
        try:
            pdf = p.find("a")["href"]
        except KeyError:
            continue
        except TypeError:
            continue

        if "bollettino" in pdf.lower():
            list_of_articles.append(pdf)
            break

    return list_of_articles


def refresh_feed(rss_folder):
    url = "https://aeroba.fmach.it/bollettino"
    return common_refresh_feed(
        rss_folder=rss_folder,
        base_url=url,
        article_url='/'.join(url.split('/')[:-1]),
        scrapping_function=scrap_aeroba,
        feed_title="AeroBA RSS Feed",
        feed_description="RSS feed dei bollettini pollini della Fondazione Mach",
        feed_generator="AeroBA FEM (from RSS Feed Generator)"
    )
