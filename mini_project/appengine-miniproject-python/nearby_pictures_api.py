import os
import urllib
import logging
import cloudstorage as gcs

from google.appengine.api import app_identity, mail, users, search
from google.appengine.ext import ndb
from entities_def import User, Photo, Stream
from flask import Flask, jsonify, abort, request, make_response, url_for
from math import sin, cos, sqrt, atan2, radians
# import geopy.distance

import jinja2
import webapp2
import json
from view_stream import stream_key

app = Flask(__name__)

def serializePhoto(photos):
    re = {}
    l = []
    for s in photos:
        item = {}
        item['name'] = s.name
        item['url'] = s.url
        item['distance'] = s.distance
        item['parent'] = s.parent
        l.append(item)
    re['body'] = l
    return re


def calculate_distance (lat0, lng0, lat1, lng1):
    # approximate radius of earth in km
    R = 6373.0

    lat0 = radians(lat0)
    lng0 = radians(lng0)
    lat1 = radians(lat1)
    lng1 = radians(lng1)

    dlon = lng1 - lng0
    dlat = lat1 - lat0

    a = sin(dlat / 2) ** 2 + cos(lat0) * cos(lat1) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    logging.info("Result: %f " % distance)
    return distance


@app.route('/api/nearby_pictures/<position>', methods=['POST'])

def post(position = None):
    logging.info("Nearby pictures!!!")

    #TODO: not sure how to get the stream sent by volley
    #search_text = webapp2.RequestHandler.request.get('search_string')
    search_text = position

    logging.info("Got position text: %s", position)
    str_lat, str_lng = position.split("_")

    lat = float(str_lat)
    lng = float(str_lng)

    logging.info("position %f %f" % (lat, lng))

    # target_query

    photos_list = []

    target_query = Photo.query()
    targets = target_query.fetch()
    for target in targets:
        if target.photo_location_lat is None:
            photo_location_lat = 0
        else:
            photo_location_lat = target.photo_location_lat
        if target.photo_location_lng is None:
            photo_location_lng = 0
        else:
            photo_location_lng = target.photo_location_lng
	    distance = calculate_distance(lat, lng, photo_location_lat, photo_location_lng)

	    stream_query = Stream.query()
	    streams = stream_query.fetch()
	    # tmp_stream
	    tmp_stream = streams[0]
	    for s in streams:
		logging.info("Looking in Stream %s " % s.name)
		photo_query = Photo.query(ancestor=stream_key(s.name))
		photos = photo_query.fetch()
		for i in photos:
		    logging.info("photo %s %s" % (i.name, target.name))
		if target in photos:
		    logging.info("Found!!!!!! %s " % target.name)
		    tmp_stream = s
		    break

	    target.parent = target.key.parent().get()
	    #logging.info("target %s" % dir(target))
	    target.distance = distance
	    # target.parent_name = Stream.query(children=target.key.parent()).fetch()[0].name
	    logging.info("target distance %s" % target.distance)
	    logging.info("target parent %s" % tmp_stream.name)
	    photos_list.append((distance, target))


    photos_list = sorted(photos_list)

    final_targets = []
    counter = 0
    for i in photos_list:
        final_targets.append(i[1])
        logging.info("Found photo %s with distance %f km" % (i[1].name, i[0]))

    logging.info("Listing %d of streams" % len(final_targets))

    re = serializePhoto(final_targets)

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
