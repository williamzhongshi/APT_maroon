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

def stream_key(name):
    return ndb.Key('stream', name)

@app.route('/api/uploadfile', methods = ['GET'])
def get(stream_name = None):
    logging.info("Get Blob URI!!!"+ str(stream_name))

    upload_url = blobstore.create_upload_url('/api/uploadfile')
    re = {}
    re['url'] = upload_url

    return json.dumps(re)

