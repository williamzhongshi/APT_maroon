import os
import urllib
import logging
import cloudstorage as gcs

from google.appengine.api import app_identity, mail, users, search
from google.appengine.ext import ndb, blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.blobstore import BlobKey
from google.appengine.api import images

from entities_def import User, Photo, Stream
from flask import Flask, jsonify, abort, request, make_response, url_for
from werkzeug.http import parse_options_header

import jinja2
import webapp2
import json


app = Flask(__name__)



# get the current folder
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def stream_key(name):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('stream', name)

@app.route('/uploadfiles/upload', methods=['POST'])
def upload():

    # loop over files since we allow multiple files
    #upload = request.get_uploads()
    f = request.files['file']

    header = f.headers['Content-Type']

    parsed_header = parse_options_header(header)
    blob_key = parsed_header[1]['blob-key']
    name = f.filename,
    logging.info("name %s", name)
    logging.info("%s", parsed_header)
    logging.info("%s", blob_key)
    # blob_key = f.key()
    logging.info("Blob key %s", blob_key)

    temp_stream_name = "Cats"

    user_photo = Photo(
        name= name,
        blob_key= BlobKey(blob_key),
        comment="",
        parent=stream_key(temp_stream_name),
        #photo_location_lat=random.uniform(-30.0, 30.0),
        #photo_location_lng=random.uniform(110.0, 130.0)
        # url=upload.get_serving_url()
    )
    user_photo.put()

    return 'OK'


