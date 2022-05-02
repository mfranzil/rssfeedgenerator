# Directory preferfinita di salvataggio dei file XML (senza trailing /)
import os

# FEED_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'feeds')
FEED_PATH = "/tmp/feeds"

SCRIPT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'scripts')
SCRIPT_MODULE_POSITION = "src.scripts."

CONFIG_URL = "https://mfranzil-rssgenerator.azurewebsites.net/"
LOCAL_PORT = 2005
REFRESH_TIME = 120 * 60
