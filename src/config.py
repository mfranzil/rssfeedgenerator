# Directory preferfinita di salvataggio dei file XML (senza trailing /)
import os

FEED_PATH = "/tmp/feeds"
FEED_FILENAME = "feed.xml"

SEEN_FILENAME = "/tmp/feeds/seen"

SCRIPT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'scripts')
SCRIPT_MODULE_POSITION = "src.scripts."

LOCAL_PORT = 7071
REFRESH_TIME = 60 * 60
DEFAULT_HEADER_DESKTOP = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:80.0) Gecko/20100101 Firefox/80.0",
    "Accept-Language": "it,en-US;q=0.7,en;q=0.3"
}
DEFAULT_TIMEOUT_CONNECTION = 5
