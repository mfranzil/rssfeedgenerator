from src.server import *
from waitress import serve

if __name__ == '__main__':
    # Set up thread for refreshing feeds
    refresh_thread = threading.Thread(target=refresh_all_feeds)
    refresh_thread.start()

    # Start the server
    serve(app, host="0.0.0.0", port=LOCAL_PORT)
