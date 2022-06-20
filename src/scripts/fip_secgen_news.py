# -*- coding: utf-8 -*-
from src.scripts.common.fipcommon import refresh_feed as refresh_feed_common


def refresh_feed(rss_folder):
    request = {
        "url": f"https://www.fip.it/segreteriagenerale/Documento.asp?IsSearch=1",
        "section": "segreteriagenerale",
        "mode": "news",
        "required_url_substring": None,
        "sentences": {
            "new_object": "una nuova notizia",
            "feed_title": "FIP - Segreteria Generale - News",
            "feed_description": "RSS feed delle news di FIP Segreteria Generale",
            "feed_generatore": "FIP - Segreteria Generale - News (from RSS Feed Generator)"
        }
    }
    refresh_feed_common(rss_folder, request)


if __name__ == "__main__":
    refresh_feed(".")
