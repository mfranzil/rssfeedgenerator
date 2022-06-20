# -*- coding: utf-8 -*-
import os
import requests

from bs4 import BeautifulSoup
from readability import Document

from src.scripts.common.common import DEFAULT_HEADER_DESKTOP, DEFAULT_TIMEOUT_CONNECTION, make_feed, add_feed
from src.config import FEED_FILENAME

list_of_articles = []
header_desktop = DEFAULT_HEADER_DESKTOP
timeout_connection = DEFAULT_TIMEOUT_CONNECTION


def scrap_fip(url, mode, section):
    pagedesktop = requests.get(url, headers=header_desktop, timeout=timeout_connection)
    soupdesktop = BeautifulSoup(pagedesktop.text, "html.parser")

    tmp = []
    print(url)
    if "Regioni" in url:
        for div in soupdesktop.find_all("a"):
            if (link := div["href"].replace(" ", "%20")):
                tmp.append(link)
    else:
        if "Documento.asp" in url:
            subclass = "NewsBox LIST"
        elif "Comunicato.asp" in url:
            subclass = "listBkg"
        else:
            raise ValueError("Cannot look for subclass in this url")

        for div in soupdesktop.find_all("div", attrs={"class": subclass}):
            if div['onclick']:
                try:
                    link = div['onclick'].split("'")[1].replace(" ", "%20")
                    print(link)
                except Exception as e:
                    continue

                tmp.append(link)

    for link in tmp:
        if mode == "delibera":
            if "deliber" not in link.lower():
                continue
        elif mode == "comunicato":
            if "comunicat" not in link.lower():
                continue

        if not link.startswith("/") and not link.startswith("http"):
            link = "/" + section + "/" + link

        if not link.startswith("https://www.fip.it"):
            link = "https://www.fip.it" + link
        
        list_of_articles.append(link)


def refresh_feed(rss_folder, request):
    url = request["url"]
    mode = request["mode"]
    section = request["section"]
    if request["required_url_substring"] and request["required_url_substring"] is not None:
        required_url_substring = request["required_url_substring"].lower()
    else:
        required_url_substring = None

    rss_file = os.path.join(rss_folder, FEED_FILENAME)

    # Acquisisco l'articolo principale
    scrap_fip(url, mode, section)

    # Se non esiste localmente un file XML procedo a crearlo.
    if os.path.exists(rss_file) is not True:
        make_feed(
            rss_file=rss_file,
            feed_title=request["sentences"]["feed_title"],
            feed_description=request["sentences"]["feed_description"],
            feed_generator=request["sentences"]["feed_generatore"]
        )

    # Analizzo ogni singolo articolo rilevato
    for urlarticolo in sorted(list_of_articles):
        response = requests.get(urlarticolo, headers=header_desktop, timeout=timeout_connection)

        modified_url = urlarticolo.split("/")[-1].replace("%20", " ")

        if "pdf" in urlarticolo:
            if mode == "delibera" and "deliber" not in urlarticolo.lower():
                continue
            elif mode == "comunicato" and "comunicat" not in urlarticolo.lower():
                continue

            if required_url_substring is not None and required_url_substring not in urlarticolo.lower():
                continue

            description = f"E' disponibile {request['sentences']['new_object']}" \
                + f" per il download.\n<a href=\"{urlarticolo}\">{modified_url}</a>"
        else:
            description = Document(response.text).summary()

        title = Document(response.text).short_title()
        if not title or title is None or title == "":
            title = modified_url

        add_feed(
            rss_file=rss_file,
            feed_title=title,
            feed_description=description,
            feed_link=urlarticolo
        )
