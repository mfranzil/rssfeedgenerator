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

bad_articles = [
    "#",
    "sportello/fiscale-legale",
    "https://servizi.fip.it",
    "/Regioni/trentinoaltoadige/Home/CookiesPolicy",
    "/Regioni/trentinoaltoadige/Home/PrivacyPolicy",
    "http://www.sendoc.it/",
    "Dolomitiacanestro",
    "/Regioni/trentinoaltoadige"
]


def scrap_fip(url, is_delibera):
    pagedesktop = requests.get(url, headers=header_desktop, timeout=timeout_connection)
    soupdesktop = BeautifulSoup(pagedesktop.text, "html.parser")

    # Ottengo i primi 8 articoli di rilievo
    article = 8

    for div in soupdesktop.find_all("a"):
        if div['href']:
            if is_delibera:
                if "delibere" not in div['href'].lower() and "delibera" not in div['href'].lower():
                    continue
            else:
                if "comunicati" not in div['href'].lower() and "comunicato" not in div['href'].lower():
                    continue
            print(div['href'])
            # Exclude bad articles
            #admissible = True
            #for item in bad_articles:
            #    if item.lower() in div["href"].lower() or item.lower() == div["href"].lower():
            #        admissible = False
            #if not admissible:
            #    continue

            if not div["href"].startswith("https://www.fip.it"):
                div["href"] = "https://www.fip.it" + str(div["href"])
            list_of_articles.append(div["href"])
            article -= 1


def refresh_feed(rss_folder, is_delibera, regione):
    url = f"https://www.fip.it/Regioni/{regione}/Comunicati/Comunicati?delibera={is_delibera}"
    print(url)
    rss_file = os.path.join(rss_folder, FEED_FILENAME)

    # Acquisisco l'articolo principale
    scrap_fip(url, is_delibera)

    # Se non esiste localmente un file XML procedo a crearlo.
    if os.path.exists(rss_file) is not True:
        make_feed(
            rss_file=rss_file,
            feed_title=f"fip_{regione}_{'del' if is_delibera else 'com'}",
            feed_description=f"RSS feed {'delle delibere' if is_delibera else 'dei comunicati ufficiali'} "
            + f"di fip-{regione}",
            feed_generator=f"fip_{regione}_{'del' if is_delibera else 'com'} (from RSS Feed Generator)"
            )

    # Analizzo ogni singolo articolo rilevato
    for urlarticolo in list_of_articles:
        response = requests.get(urlarticolo, headers=header_desktop, timeout=timeout_connection)

        if "pdf" in urlarticolo:
            description = urlarticolo.split("/")[-1]
        else:
            description = Document(response.text).summary()

        title = Document(response.text).short_title()
        add_feed(
            rss_file=rss_file,
            feed_title=title,
            feed_description=description,
            feed_link=urlarticolo)
