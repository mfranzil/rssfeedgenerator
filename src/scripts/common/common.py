# -*- coding: utf-8 -*-
from __future__ import annotations

import logging as log
import os
import threading
from time import gmtime, strftime
from typing import Callable

import requests
from lxml import etree as et
from readability import Document

from src.config import SEEN_FILENAME, FEED_FILENAME, \
    DEFAULT_HEADER_DESKTOP, DEFAULT_TIMEOUT_CONNECTION, \
    MAX_DOWNLOAD_RETRIES


def fetch_info(url: str, mapping: dict[str, tuple[str, str]]) -> tuple[str | None, str | None]:
    try:
        response = requests.get(url,
                                headers=DEFAULT_HEADER_DESKTOP,
                                timeout=DEFAULT_TIMEOUT_CONNECTION)
    except Exception as e:
        log.error(f"Failed to fetch {url}: {e}")
        return None, None

    if response.status_code % 400 == 0:
        log.error(f"Client-side error, failed to fetch {url}: {response}")
        return None, None
    elif response.status_code % 500 == 0:
        log.error(f"Server-side error, failed to fetch {url}: {response}")
        return None, None
    elif response.status_code != 200:
        log.warning(f"Unexpected response code {response.status_code} for {url}")
        return None, None

    description = Document(response.text).summary()
    title = Document(response.text).short_title()

    mapping[url] = title, description
    return title, description


def refresh_feed(rss_folder: str,
                 base_url: str,
                 article_url: str,
                 scrapping_function: Callable[[str], list[str]],
                 feed_title: str,
                 feed_description: str,
                 feed_generator: str):
    rss_file = os.path.join(rss_folder, FEED_FILENAME)

    # Acquisisco l'articolo principale
    list_of_articles = []
    for i in range(MAX_DOWNLOAD_RETRIES):
        try:
            list_of_articles = scrapping_function(base_url)
        except requests.exceptions.ReadTimeout:
            log.error(f"Timeout while fetching {base_url}, " +
                      f"retrying ({MAX_DOWNLOAD_RETRIES - i - 1} attemps left)...")
            continue
        except Exception as e:
            log.error(f"Encountered exception while fetching {base_url}: {e}")
            continue
        break

    if not list_of_articles:
        log.error(f"Failed to fetch {base_url}, aborting...")
        return

    list_of_articles = [article_url + article for article in list_of_articles]

    log.info(f"Obtained {len(list_of_articles)} articles from {base_url}.")

    make_feed(
        rss_file=rss_file,
        feed_title=feed_title,
        feed_description=feed_description,
        feed_generator=feed_generator
    )

    # fetch title and description in parallel
    data = {}
    for entry_link in list_of_articles:
        data[entry_link] = None, None

    t = []
    for entry_link in list_of_articles:
        if "pdf" in entry_link:
            entry_title = entry_link.split("/")[-1]
            entry_description = f"Nuovo documento disponibile per il download." \
                                f"\n<a href=\"{entry_link}\">{entry_link}</a>"
            data[entry_link] = entry_title, entry_description
            # description = f"E' disponibile un nuovo bollettino per il download." + \
            #                       f"\n<a href=\"{urlarticolo}\">{urlarticolo}</a>"
            #         title = "Nuovo bollettino AeroBA!"
            # description = f"E' disponibile {request['sentences']['new_object']}" \
            #              + f" per il download.\n<a href=\"{urlarticolo}\">{urlarticolo}</a>"
            # title = urlarticolo.split("/")[-1]
        else:
            thread = threading.Thread(target=fetch_info,
                                      args=(entry_link, data))
            t.append(thread)
            thread.start()

    for thread in t:
        thread.join()

    original_len = feed_len(rss_file)

    for entry_link in list_of_articles:
        entry_title, entry_description = data[entry_link]

        ok = add_entry(rss_file, entry_link, entry_title, entry_description)
        if ok == 0:
            log.debug(f"Added new entry {entry_link} to feed {rss_file}.")
        elif ok == 1:
            log.debug(f"Entry {entry_link} already present in feed {rss_file}.")
        elif ok == -1:
            log.debug(f"Entry {entry_link} not added to feed {rss_file}" +
                      f" because it is already present in the seen file.")
        else:
            log.error(f"Failed to add entry {entry_link} to feed {rss_file}.")

    length = feed_len(rss_file)
    new = length - original_len
    log.info(f"Feed {rss_file} refreshed. " +
             f"Added {new} new entries" +
             f" (total: {length}).")

    return new


def feed_len(rss_file: str) -> int:
    tree = et.parse(rss_file)
    channel = tree.getroot()
    return len(channel.findall("channel/item"))


def make_feed(rss_file, feed_title, feed_description, feed_generator):
    if os.path.exists(rss_file):
        log.info(f"RSS file {rss_file} already exists, skipping...")
        return

    root = et.Element("rss")
    root.set("version", "2.0")

    channel = et.SubElement(root, "channel")

    title = et.SubElement(channel, "title")
    title.text = feed_title

    date = et.SubElement(channel, "updatedate")
    date.text = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

    description = et.SubElement(channel, "description")
    description.text = feed_description

    language = et.SubElement(channel, "language")
    language.text = "it-IT"

    generator = et.SubElement(channel, "generator")
    generator.text = feed_generator

    tree = et.ElementTree(root)

    tree.write(rss_file, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    log.info(f"RSS file now available at {rss_file}")


def add_entry(feed_file: str, entry_link: str,
              entry_title: str, entry_description: str):
    # First check if the feed link has already been seen in the past
    with open(SEEN_FILENAME, "r") as f:
        seen_links = f.read().splitlines()

    if seen_links and entry_link in seen_links:
        log.debug(f"Feed link {entry_link} already seen, skipping...")
        return -1

    parser = et.XMLParser(remove_blank_text=True)
    tree = et.parse(feed_file, parser)
    channel = tree.getroot()

    # Escludo eventuali duplicati in base al link
    for i in channel.findall(".//link"):
        if i.text == entry_link:
            return 1

    item = et.SubElement(channel, "item")

    title = et.SubElement(item, "title")
    title.text = entry_title

    link = et.SubElement(item, "link")
    link.text = entry_link

    description = et.SubElement(item, "description")
    description.text = entry_description

    pub_date = et.SubElement(item, "pubDate")
    pub_date.text = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

    channel.find(".//generator").addnext(item)

    tree = et.ElementTree(channel)
    tree.write(feed_file, pretty_print=True, xml_declaration=True, encoding="UTF-8")

    with open(SEEN_FILENAME, "a") as f:
        f.write(entry_link + "\n")
        log.debug(f"Feed link {entry_link} cached.")

    return 0
