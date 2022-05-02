# -*- coding: utf-8 -*-

import logging as log

from src.config import CONFIG_URL

from lxml import etree as ET
from time import gmtime, strftime


def make_feed(rss_file, feed_title, feed_description, feed_generator):
    root = ET.Element("rss")
    root.set("version", "2.0")

    channel = ET.SubElement(root, "channel")

    title = ET.SubElement(channel, "title")
    title.text = feed_title

    date = ET.SubElement(channel, "updatedate")
    date.text = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

    link = ET.SubElement(channel, "link")
    link.text = CONFIG_URL

    description = ET.SubElement(channel, "description")
    description.text = feed_description

    language = ET.SubElement(channel, "language")
    language.text = "it-IT"

    generator = ET.SubElement(channel, "generator")
    generator.text = feed_generator

    tree = ET.ElementTree(root)

    log.info(f"Saving RSS file to {rss_file}")
    tree.write(rss_file, pretty_print=True, xml_declaration=True, encoding="UTF-8")


def add_feed(rss_file, feed_title, feed_description, feed_link):
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
