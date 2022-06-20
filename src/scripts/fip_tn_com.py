# -*- coding: utf-8 -*-

from src.scripts.common.fipcommon import refresh_feed as refresh_feed_common


def refresh_feed(rss_folder):
    request = {
        "url": f"https://www.fip.it/Regioni/trentinoaltoadige/Comunicati/Comunicati?delibera=False",
        "section": "trentinoaltoadige",
        "mode": "comunicato",
        "required_url_substring": "public/24",
        "sentences": {
            "new_object": "un nuovo comunicato",
            "feed_title": "FIP - Trentino Alto Adige - Comunicati",
            "feed_description": "RSS feed dei comunicati di FIP Trentino Alto Adige",
            "feed_generatore": "FIP - Trentino Alto Adige - Comunicati (from RSS Feed Generator)"
        }
    }
    refresh_feed_common(rss_folder, request)


if __name__ == "__main__":
    refresh_feed(".")
