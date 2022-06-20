# -*- coding: utf-8 -*-

from src.scripts.common.fipcommon import refresh_feed as refresh_feed_common


def refresh_feed(rss_folder):
    request = {
        "url": f"https://www.fip.it/Regioni/veneto/Comunicati/Comunicati?delibera=False",
        "section": "veneto",
        "mode": "comunicato",
        "required_url_substring": "public/11",
        "sentences": {
            "new_object": "un nuovo comunicato",
            "feed_title": "FIP - Veneto - Comunicati",
            "feed_description": "RSS feed dei comunicati di FIP Veneto",
            "feed_generatore": "FIP - Veneto - Comunicati (from RSS Feed Generator)"
        }
    }
    refresh_feed_common(rss_folder, request)


if __name__ == "__main__":
    refresh_feed(".")
