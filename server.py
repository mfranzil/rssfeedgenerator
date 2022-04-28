# -*- coding: utf-8 -*-
import logging as log
import os
from urllib import response
import importlib

from flask import Flask, send_from_directory, request

app = Flask(__name__)
port = 2005

script_position = 'scripts.'


def get_feed_list():
    feeds = []
    feed_folder = 'feeds'
    for item in os.listdir(feed_folder):
        if os.path.isdir(os.path.join(feed_folder, item)):
            feeds.append(item)
    return feeds


@app.route('/', methods=['GET'])
def index():
    html = '<h1>RSS dumb server</h1>'
    html += '<h2>Available API</h2>'
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
    }, {
        'name': 'refresh_feed',
        'description': 'Refresh the feed',
        'url': '/refresh/:feed',
        'method': 'GET'
    }]

    for item in api_list:
        html += '<li>'
        html += '<h3>' + item['name'] + '</h3>'
        html += '<p>' + item['description'] + '</p>'
        html += '<p>' + item['url'] + '</p>'
        html += '<p>' + item['method'] + '</p>'
        html += '</li>'

    html += '</ul>'

    return html, 200


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


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

    feed_folder = os.path.join(app.root_path, 'feeds', feed)
    feed_file = os.path.join(feed_folder, 'feed.xml')
    if not os.path.isfile(feed_file):
        return 'Feed found, but without a feed.xml file. Please fix.', 404

    return send_from_directory(feed_folder, 'feed.xml'), 200


@app.route('/refresh/<feed>/', methods=['GET'])
def refresh_feed(feed):
    refresher = importlib.import_module(script_position + feed)
    refresher.main()

    return 'Feed refreshed', 200


if __name__ == '__main__':
    print(f"RSS server listening on port {port}")
    print(f"List of currently offered feeds:")
    feeds = get_feed_list()
    for feed in feeds:
        print('- ' + feed)
    print()
    app.run(host='0.0.0.0', port=port)
