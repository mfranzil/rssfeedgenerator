# -*- coding: utf-8 -*-

from src.scripts.common.fipcommon import refresh_feed as refresh_feed_common


def refresh_feed(rss_folder):
    request = {
        "url": f"https://www.fip.it/Regioni/veneto/Comunicati/Comunicati?delibera=True",
        "section": "veneto",
        "mode": "delibera",
        "required_url_substring": "public/11",
        "sentences": {
            "new_object": "una nuova delibera",
            "feed_title": "FIP - Veneto - Delibere",
            "feed_description": "RSS feed delle delibere di FIP Veneto",
            "feed_generatore": "FIP - Veneto - Delibere (from RSS Feed Generator)"
        }
    }

    refresh_feed_common(rss_folder, request)


if __name__ == "__main__":
    refresh_feed(".")
