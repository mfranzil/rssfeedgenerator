# -*- coding: utf-8 -*-
from src.scripts.common.fipcommon import refresh_feed as refresh_feed_common


def refresh_feed(rss_folder):
    request = {
        "url": f"https://www.fip.it/cia/Comunicato.asp",
        "section": "cia",
        "mode": "comunicato",
        "required_url_substring": None,
        "sentences": {
            "new_object": "un nuovo comunicato",
            "feed_title": "FIP - CIA - Comunicati",
            "feed_description": "RSS feed dei comunicati di FIP CIA",
            "feed_generatore": "FIP - CIA - Comunicati (from RSS Feed Generator)"
        }
    }
    refresh_feed_common(rss_folder, request)


if __name__ == "__main__":
    refresh_feed(".")
