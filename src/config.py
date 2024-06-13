# Directory preferfinita di salvataggio dei file XML (senza trailing /)
import os

SCRIPT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'scripts')
SCRIPT_MODULE_POSITION = "src.scripts."

FEED_PATH = os.getenv("FEED_PATH", "/tmp/feeds")
FEED_FILENAME = os.getenv("FEED_FILENAME", "feed.xml")
SEEN_FILENAME = os.getenv("SEEN_FILENAME", "/tmp/feeds/seen")

LOCAL_PORT = os.getenv("LOCAL_PORT", 7071)
REFRESH_TIME = os.getenv("REFRESH_TIME", 60 * 60 * 2)
DEFAULT_HEADER_DESKTOP = {
    "User-Agent": os.getenv("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"),
    "Accept-Language": os.getenv("ACCEPT_LANGUAGE", "en-US,en;q=0.5"),
}
DEFAULT_TIMEOUT_CONNECTION = os.getenv("DEFAULT_TIMEOUT_CONNECTION", 10)
MAX_DOWNLOAD_RETRIES = os.getenv("MAX_DOWNLOAD_RETRIES", 4)
