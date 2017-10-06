import os
import urllib
import logging
import cloudstorage as gcs

from google.appengine.api import app_identity, mail, users
from google.appengine.ext import ndb

from entities_def import User, Photo, Stream, Trending_stream_entity, CronJobFrequency
from trending_cron import Trending_cron

import jinja2
import webapp2
import logging
import time
from google.appengine.api import app_identity
from google.appengine.api import mail

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Hour1Cron(webapp2.RequestHandler):
    def get(self):
        freq = CronJobFrequency.query().fetch()
        logging.info("**********crondb"+ str(freq))
        for f in freq:
            if f.frequency == "hour1":
                Trending_cron.get()

app = webapp2.WSGIApplication([
    ('/hour1_cron', Hour1Cron)
], debug=True)
