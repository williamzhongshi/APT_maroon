import os
import urllib
import logging
import cloudstorage as gcs

from google.appengine.api import app_identity, mail, users, search
from google.appengine.ext import ndb
from entities_def import User, Photo, Stream
from all_stream_api import serializeStream, get_char_set
from flask import Flask, jsonify, abort, request, make_response, url_for

import jinja2
import webapp2
import json

app = Flask(__name__)
 
# def get_char_set(word):
#     char_set = set()
#     for c in word.lower():
#         char_set.add(c)
#     return char_set
#
#
# def serializeStream(stream):
#     re = {}
#     l = []
#     for s in stream:
#         item = {}
#         item['name'] = s.name
#         item['cover_image'] = s.cover_image
#         l.append(item)
#     re['body'] = l
#     return re
#@app.route('/api/search_stream', methods=['POST'])
#class SearchStream(webapp2.RequestHandler):

#@app.route('/api/search_stream', methods=['POST'])
@app.route('/api/search_stream/<name>', methods=['POST'])

def post(name = None):
    logging.info("name %s" % name)
    logging.info("Search Streams!!!")
    logging.info("%s", dir(webapp2.RequestHandler.request))

    #TODO: not sure how to get the stream sent by volley
    #search_text = webapp2.RequestHandler.request.get('search_string')
    search_text = name

    logging.info("Got search text: %s", search_text)

    # target_query

    # IF USE GOOGLE SEARCH API
    index = search.Index(name="search_stream")
    target_query = Stream.query()
    targets = target_query.fetch()
    for target in targets:
        fields = [
            search.TextField(name="name", value=target.name)
        ]
        for tag in target.tags:
            fields.append(search.TextField(name="tags", value=tag))
        d = search.Document(fields=fields, language='en')
        search.Index(name="search_stream").put(d)

    # index = search.Index()

    # search_results = index.search("%s in name OR %s in tags" % (search_text, search_text))
    search_results = index.search(search_text)
    # logging.info("%s", dir(search_results))
    logging.info("Found %d number of results" % len(search_results.results))

    final_targets = []
    counter = 0
    for i in search_results:
        found_name = i.field("name".encode('utf-8')).value.decode('utf-8')
        logging.info("Found %s" % found_name)
        # if counter < 5:
        target_query = Stream.query(Stream.name == found_name)
        target = target_query.fetch()[0]
        final_targets.append(target)
            # counter += 1
        # else:
        #     break
    logging.info("Listing %d of streams" % len(final_targets))
    for i in final_targets:
        logging.info("found %s", i.name)
    # remove all indexes
    while True:
        # until no more documents, get a list of documents,
        # constraining the returned objects to contain only the doc ids,
        # extract the doc ids, and delete the docs.
        document_ids = [document.doc_id for document in index.get_range(ids_only=True)]
        if not document_ids:
            break
        index.delete(document_ids)


    # target_query = Stream.query()#.order(-last_picture_date)
    # targets = target_query.fetch()

    for s in final_targets:
        logging.info("*********picture:" + s.cover_image)
    re = serializeStream(final_targets)

    return json.dumps(re)

# #
# # #
# # # [START app]
# app = webapp2.WSGIApplication([
#     #('/', MainPage),
#     ('/spi/search_stream', SearchStream)
#     # ('/sign', Guestbook),
# ], debug=True)
# # # [END app]
