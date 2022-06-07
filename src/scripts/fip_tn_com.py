# -*- coding: utf-8 -*-

from src.scripts.common.fipcommon import refresh_feed as refresh_feed_common


def refresh_feed(rss_folder):
    refresh_feed_common(rss_folder, False, "trentinoaltoadige")


if __name__ == "__main__":
    refresh_feed(".")
