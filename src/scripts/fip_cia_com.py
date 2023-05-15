# -*- coding: utf-8 -*-
from src.scripts.common.fipcommon import refresh_feed as refresh_feed_common


def refresh_feed(rss_folder):
    request = {
        "url": f"https://cia.fip.it/comunicati/",
        "sentences": {
            "feed_title": "FIP - CIA - Comunicati",
            "feed_description": "RSS feed dei comunicati di FIP CIA",
            "feed_generator": "FIP - CIA - Comunicati (from RSS Feed Generator)"
        }
    }
    refresh_feed_common(rss_folder, request)


if __name__ == "__main__":
    refresh_feed(".")
