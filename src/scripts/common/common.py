# -*- coding: utf-8 -*-

import logging as log
import os

from src.config import SEEN_FILENAME

from lxml import etree as ET
from time import gmtime, strftime


DEFAULT_HEADER_DESKTOP = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:80.0) Gecko/20100101 Firefox/80.0",
    "Accept-Language": "it,en-US;q=0.7,en;q=0.3"
}

DEFAULT_TIMEOUT_CONNECTION = 5


def make_feed(rss_file, feed_title, feed_description, feed_generator):
    if os.path.exists(rss_file):
        log.info(f"RSS file {rss_file} already exists, skipping...")
        return

    root = ET.Element("rss")
    root.set("version", "2.0")

    channel = ET.SubElement(root, "channel")

    title = ET.SubElement(channel, "title")
    title.text = feed_title

    date = ET.SubElement(channel, "updatedate")
    date.text = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

    description = ET.SubElement(channel, "description")
    description.text = feed_description

    language = ET.SubElement(channel, "language")
    language.text = "it-IT"

    generator = ET.SubElement(channel, "generator")
    generator.text = feed_generator

    tree = ET.ElementTree(root)

    log.info(f"Saving RSS file to {rss_file}")
    tree.write(rss_file, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    log.info("RSS file saved.")


def add_feed(rss_file, feed_title, feed_description, feed_link):
    # First check if the feed link has already been seen in the past
    with open(SEEN_FILENAME, "r") as f:
        seen_links = f.read().splitlines()

    if seen_links and feed_link in seen_links:
        log.info(f"Feed link {feed_link} already seen, skipping...")
        return

    parser = ET.XMLParser(remove_blank_text=True)
    tree = ET.parse(rss_file, parser)
    channel = tree.getroot()

    # Escludo eventuali duplicati in base al link
    for i in channel.findall(".//link"):
        if (i.text == feed_link):
            return

    item = ET.SubElement(channel, "item")

    title = ET.SubElement(item, "title")
    title.text = feed_title

    link = ET.SubElement(item, "link")
    link.text = feed_link

    description = ET.SubElement(item, "description")
    description.text = feed_description

    pubDate = ET.SubElement(item, "pubDate")
    pubDate.text = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

    channel.find(".//generator").addnext(item)

    tree = ET.ElementTree(channel)
    tree.write(rss_file, pretty_print=True, xml_declaration=True, encoding="UTF-8")

    with open(SEEN_FILENAME, "a") as f:
        f.write(feed_link + "\n")
        log.info(f"Feed link {feed_link} cached.")
