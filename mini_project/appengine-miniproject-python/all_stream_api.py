import os
import urllib
import logging
import cloudstorage as gcs

from google.appengine.api import app_identity, mail, users, search
from google.appengine.ext import ndb
from entities_def import User, Photo, Stream
from flask import Flask, jsonify, abort, request, make_response, url_for

import jinja2
import webapp2
import json

app = Flask(__name__)
 
def get_char_set(word):
    char_set = set()
    for c in word.lower():
        char_set.add(c)
    return char_set


def serializeStream(stream):
    re = {}
    l = []
    for s in stream:
        item = {}
        item['name'] = s.name
        item['cover_image'] = s.cover_image
        l.append(item)
    re['body'] = l
    return re

@app.route('/api/all_stream', methods = ['GET'])
def get():
    logging.info("Show All Streams!!!")
    user = users.get_current_user()

    target_query = Stream.query()#.order(-last_picture_date)
    targets = target_query.fetch()

    for s in targets:
        logging.info("*********picture:"+ s.cover_image)
    re = serializeStream(targets)

    return json.dumps(re)
