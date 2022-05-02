# -*- coding: utf-8 -*-
import os
import sys
import importlib
import logging as log
import pathlib
import time

from src.config import FEED_FILENAME, FEED_PATH, LOCAL_PORT, REFRESH_TIME, SCRIPT_MODULE_POSITION, SCRIPT_PATH

from flask import Flask, send_from_directory

cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

app = Flask(__name__)

# Initialize logging
log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize folders
pathlib.Path(FEED_PATH).mkdir(parents=True, exist_ok=True)


def get_feed_list():
    feeds = []
    for item in os.listdir(SCRIPT_PATH):
        if os.path.isfile(os.path.join(SCRIPT_PATH, item)) and item.endswith('.py') and not item.startswith('__'):
            feeds.append(item.replace(".py", ""))
    return feeds


@app.route('/', methods=['GET'])
def index():
    html = '<h1>RSS server</h1>'
    html += '<h2>Available APIs</h2>'
    html += '<ul>'

    api_list = [{
        'name': 'feeds',
        'description': 'Lists available feeds',
        'url': '/feeds',
        'method': 'GET'
    }, {
        'name': 'get_feed',
        'description': 'Get the feed',
        'url': '/feeds/:feed',
        'method': 'GET'
    }]

    for item in api_list:
        html += '<li>'
        html += '<h3>' + item['name'] + '</h3>'
        html += '<p>' + item['description'] + '</p>'
        html += '<p>' + item['method'] + " " + item['url'] + '</p>'
        html += '</li>'

    html += '</ul>'

    return html, 200


@app.route('/feeds', methods=['GET'])
def get_feeds():
    feeds = get_feed_list()

    html = '<html><head><title>RSS feeds</title></head><body>'
    for feed in feeds:
        html += '<a href="/feeds/{}">{}</a><br>'.format(feed, feed)
    html += '</body></html>'
    return html, 200


@app.route('/feeds/<feed>', methods=['GET'])
def get_feed(feed):
    if feed not in get_feed_list():
        return 'Feed not found', 404

    feed_folder = os.path.join(FEED_PATH, feed)
    pathlib.Path(feed_folder).mkdir(parents=True, exist_ok=True)
    feed_file = os.path.join(feed_folder, FEED_FILENAME)

    # Check if the feed needs to be refreshed (if the date is older than the refresh time)
    if not os.path.exists(feed_file) or os.path.getmtime(feed_file) < (time.time() - REFRESH_TIME):
        log.info(f"Refreshing feed {feed}, elapsed time:" +
                 f" {time.time() - os.path.getmtime(feed_file) if os.path.isfile(feed_file) else -1}")
        refresher = importlib.import_module(SCRIPT_MODULE_POSITION + feed)
        refresher.refresh_feed(feed_folder)
    else:
        log.info(f"Feed {feed} is up to date, elapsed time: {time.time() - os.path.getmtime(feed_file)}")

    return send_from_directory(feed_folder, FEED_FILENAME), 200


if __name__ == '__main__':
    log.info(f"RSS server listening on port {LOCAL_PORT}")
    log.info(f"List of currently offered feeds: {', '.join(get_feed_list())}")
    app.run(host='0.0.0.0', port=LOCAL_PORT)
