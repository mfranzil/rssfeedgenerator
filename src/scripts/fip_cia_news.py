# -*- coding: utf-8 -*-
from src.scripts.common.fipcommon import refresh_feed as refresh_feed_common


def refresh_feed(rss_folder):
    request = {
        "url": f"https://www.fip.it/cia/Documento.asp?IsSearch=1",
        "section": "cia",
        "mode": "news",
        "required_url_substring": None,
        "sentences": {
            "new_object": "una nuova notizia",
            "feed_title": "FIP - CIA - News",
            "feed_description": "RSS feed delle news di FIP CIA",
            "feed_generatore": "FIP - CIA - News (from RSS Feed Generator)"
        }
    }
    refresh_feed_common(rss_folder, request)


if __name__ == "__main__":
    refresh_feed(".")
