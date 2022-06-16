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


def scrap_fip(url, is_delibera, regione):
    pagedesktop = requests.get(url, headers=header_desktop, timeout=timeout_connection)
    soupdesktop = BeautifulSoup(pagedesktop.text, "html.parser")

    for div in soupdesktop.find_all("a"):
        if (link := div["href"]):
            if is_delibera:
                if "deliber" not in link.lower():
                    continue
            else:
                if "comunicat" not in link.lower():
                    continue
            # Exclude bad articles
            # admissible = True
            # for item in bad_articles:
            #    if item.lower() in link.lower() or item.lower() == link.lower():
            #        admissible = False
            # if not admissible:
            #    continue

            if not link.startswith("https://www.fip.it"):
                link = "https://www.fip.it" + str(link)

            list_of_articles.append(link)


def refresh_feed(rss_folder, is_delibera, regione):
    url = f"https://www.fip.it/Regioni/{regione}/Comunicati/Comunicati?delibera={is_delibera}"
    rss_file = os.path.join(rss_folder, FEED_FILENAME)

    # Acquisisco l'articolo principale
    scrap_fip(url, is_delibera, regione)

    # Se non esiste localmente un file XML procedo a crearlo.
    if os.path.exists(rss_file) is not True:
        sentence_repr2 = 'Delibere' if is_delibera else 'Comunicati'
        sentence_repr3 = 'delle delibere' if is_delibera else 'dei comunicati ufficiali'

        make_feed(
            rss_file=rss_file,
            feed_title=f"FIP - {regione.capitalize()} - {sentence_repr2}",
            feed_description=f"RSS feed {sentence_repr3} di FIP {regione.capitalize()}",
            feed_generator=f"FIP - {regione.capitalize()} - {sentence_repr2}"
        )

    # Analizzo ogni singolo articolo rilevato
    for urlarticolo in sorted(list_of_articles):
        response = requests.get(urlarticolo, headers=header_desktop, timeout=timeout_connection)

        modified_url = urlarticolo.split("/")[-1].replace("%20", " ")

        if "pdf" in urlarticolo:
            if is_delibera:
                sentence_repr = 'una nuova delibera'
                if "deliber" not in urlarticolo.lower():
                    continue
            else:
                sentence_repr = 'un nuovo comunicato ufficiale'
                if "comunicat" not in urlarticolo.lower():
                    continue

            if regione.lower() == "trentinoaltoadige" and "public/24" not in urlarticolo.lower():
                continue
            elif regione.lower() == "veneto" and "public/11" not in urlarticolo.lower():
                continue

            description = f"E' disponibile {sentence_repr}" \
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
