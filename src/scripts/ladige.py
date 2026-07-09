# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

from src.config import DEFAULT_HEADER_DESKTOP, DEFAULT_TIMEOUT_CONNECTION
from src.scripts.common.common import refresh_feed as common_refresh_feed

# Niente articoli editoriali o video
disallowed_ids = ["video", "idee"]


def _is_article_path(path, subcategory):
    parts = [p for p in path.split("/") if p]
    if subcategory == "cronaca":
        return len(parts) == 2
    if subcategory == "territori":
        return len(parts) >= 3
    return False


def scrap_ladige(url):
    list_of_articles = []

    for subcategory in ["territori", "cronaca"]:
        pagedesktop = requests.get(url + "/" + subcategory,
                                   headers=DEFAULT_HEADER_DESKTOP,
                                   timeout=DEFAULT_TIMEOUT_CONNECTION)
        soupdesktop = BeautifulSoup(pagedesktop.text, "html.parser")

        # Ottengo i primi 10 articoli di rilievo
        article = 10

        for teaser in soupdesktop.find_all(
            "div",
            class_=lambda c: c and "teaser" in c and "teaser-type-news" in c
        ):
            if article <= 0:
                break

            link = teaser.find("a", href=True)
            if not link:
                continue

            href = link["href"].split("#")[0].rstrip("/")
            if href.startswith(url.rstrip("/")):
                __id = href[len(url.rstrip("/")):]
            elif href.startswith("/"):
                __id = href
            else:
                continue

            if any(d in __id.lower().split("/") for d in disallowed_ids):
                continue

            if not _is_article_path(__id, subcategory):
                continue

            if __id not in list_of_articles:
                list_of_articles.append(__id)
                article -= 1

    return list_of_articles


def refresh_feed(rss_folder):
    url = "https://www.ladige.it/"
    return common_refresh_feed(
        rss_folder=rss_folder,
        base_url=url,
        article_url=url[:-1],
        scraping_function=scrap_ladige,
        feed_title="L'Adige RSS Feed",
        feed_description="RSS feed degli articoli principali pubblicati da L'Adige",
        feed_generator="L'Adige (from RSS Feed Generator)"
    )
