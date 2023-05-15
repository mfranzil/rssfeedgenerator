# -*- coding: utf-8 -*-
import os
import sys
import importlib
import logging as log
import pathlib
import threading
import time

from src.config import FEED_FILENAME, FEED_PATH, \
    LOCAL_PORT, REFRESH_TIME, SCRIPT_MODULE_POSITION, \
    SCRIPT_PATH, SEEN_FILENAME

from flask import Flask, send_from_directory

cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

app = Flask(__name__)

# Initialize logging
log.basicConfig(level=log.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize folders
pathlib.Path(FEED_PATH).mkdir(parents=True, exist_ok=True)
pathlib.Path(SEEN_FILENAME).touch(exist_ok=True)


def refresh_feed(feed):
    feed_folder = os.path.join(FEED_PATH, feed)
    pathlib.Path(feed_folder).mkdir(parents=True, exist_ok=True)

    feed_file = os.path.join(feed_folder, FEED_FILENAME)
    elapsed = time.time() - os.path.getmtime(feed_file) \
        if os.path.isfile(feed_file) else REFRESH_TIME + 1

    if elapsed < REFRESH_TIME:
        log.info(f"Feed {feed} is up to date, elapsed time: {elapsed}")
        return

    log.info(f"Refreshing feed {feed}, elapsed time: {elapsed}")
    refresher = importlib.import_module(SCRIPT_MODULE_POSITION + feed)
    refresher.refresh_feed(feed_folder)


def refresh_all_feeds():
    while True:
        log.info("Refreshing all feeds...")
        feeds = get_feed_list()
        for feed in feeds:
            refresh_feed(feed)
        time.sleep(REFRESH_TIME)


def get_feed_list():
    feeds = []
    for item in os.listdir(SCRIPT_PATH):
        if os.path.isfile(os.path.join(SCRIPT_PATH, item)) and item.endswith('.py') and not \
          (item.startswith('_') or item.startswith('test_') or item.startswith('.')):
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
    for feed in sorted(feeds):
        html += '<a href="feeds/{}">{}</a><br>'.format(feed, feed)
    html += '</body></html>'
    return html, 200


@app.route('/feeds/<feed>', methods=['GET'])
def get_feed(feed):
    if feed not in get_feed_list():
        return 'Feed not found', 404

    feed_folder = os.path.join(FEED_PATH, feed)
    pathlib.Path(feed_folder).mkdir(parents=True, exist_ok=True)

    feed_file = os.path.join(feed_folder, FEED_FILENAME)
    if not os.path.exists(feed_file):
        log.info(f"Generating non-existent feed {feed}")
        refresh_feed(feed)
    else:
        el = time.time() - os.path.getmtime(feed_file)
        log.info(f"Feed {feed} is up to date, elapsed time: {el}")

    return send_from_directory(feed_folder, FEED_FILENAME), 200


# default page for 404
@app.route('/<path:dummy>')
def dummy(dummy):
    return 'Not found', 404


@app.errorhandler(404)
def page_not_found(e):
    return 'Not found', 404


if __name__ == '__main__':
    log.info(f"RSS server listening on port {LOCAL_PORT}")
    log.info(f"List of currently offered feeds: {', '.join(get_feed_list())}")
    app.run(host='0.0.0.0', port=LOCAL_PORT)
