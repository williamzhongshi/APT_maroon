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

@app.route('/autocomplete', methods = ['GET'])
def get():
    term = request.args.get('term', '')
    logging.info("**********term:" + term)
    char_set = get_char_set(term)

    re = []
    streams = Stream.query().fetch()
    for s in streams:
        logging.info("s.name:" + s.name)
        if char_set.issubset(get_char_set(s.name)):
            logging.info(s.name)
            re.append(s.name)
        for tag in s.tags:
            if char_set.issubset(get_char_set(tag)):
                re.append(tag)
                logging.info(tag)
        
        logging.info("result:" + str(re))

    out = []
    for elem in re:
        d = {}
        d['id'] = elem
        d['label'] = elem
        d['value'] = elem
        out.append(d)
    return json.dumps(out)

