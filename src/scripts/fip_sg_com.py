# -*- coding: utf-8 -*-
from src.scripts.common.fipcommon import refresh_feed as refresh_feed_common


def refresh_feed(rss_folder):
    request = {
        "url": f"https://segreteriagenerale.fip.it/comunicati/",
        "sentences": {
            "feed_title": "FIP - Segreteria Generale - Comunicati",
            "feed_description": "RSS feed dei comunicati della Segreteria Generale di FIP",
            "feed_generator": "FIP - Segreteria Generale - Comunicati (from RSS Feed Generator)"
        }
    }
    refresh_feed_common(rss_folder, request)


if __name__ == "__main__":
    refresh_feed(".")
