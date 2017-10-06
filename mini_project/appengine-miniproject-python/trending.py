import os
import urllib
import logging
import cloudstorage as gcs

from google.appengine.api import app_identity, mail, users
from google.appengine.ext import ndb

from entities_def import User, Photo, Stream, Trending_stream_entity, CronJobFrequency

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

class Trending(webapp2.RequestHandler):
    def get(self):
        trendings = Trending_stream_entity.query().order(-Trending_stream_entity.ts,Trending_stream_entity.rank).fetch(3)

        streams = []

        for trending in trendings:
            stream = trending.stream_item
            stream.view_count = len(stream.views_ts)
            streams.append(stream)
            

        template_values = {
            'streams': streams,
        }

        template = JINJA_ENVIRONMENT.get_template('Trending.html')
        self.response.write(template.render(template_values))

    def post(self):
        frequencies = self.request.get_all('frequency')
        #logging.info("**************frequency:" + str(frequencies))

        if "noreports" in frequencies:
            #logging.info("**************noreport:")
            cron_flags = CronJobFrequency.query().fetch()
            for flag in cron_flags:
                flag.key.delete()
        else:
            for freq in frequencies:
                #logging.info("**************freq:" + str(freq))
                flag = CronJobFrequency()
                flag.frequency = freq
                flag.put()

        logging.info("********db:" + str(CronJobFrequency.query().fetch()))

        self.redirect("/trending")

app = webapp2.WSGIApplication([
    ('/trending', Trending)
], debug=True)
