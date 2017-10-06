import os
import urllib
import logging
import cloudstorage as gcs

from google.appengine.api import app_identity, mail, users
from google.appengine.ext import ndb

from entities_def import User, Photo, Stream, Trending_stream_entity

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

def send_approved_mail(sender_address, dest_address, subject_str, body_str):

    mail.send_mail(sender=sender_address,
                   to="<{}>".format(dest_address),
                   subject=subject_str,
                   body=body_str)

def filterbyvalue(seq, one_hour_before):
   for el in seq:
      if el >= one_hour_before: yield el

class Trending_cron(webapp2.RequestHandler):

    def get(self):

        for entity in Trending_stream_entity.query().fetch():
            entity.key.delete()

        streams = Stream.query().fetch()
        
        logging.info("*************now:" + str(time.time()));

        streams_one_hour = []
        now = int(time.time())

        for stream in streams:
            stream.views_ts = filterbyvalue(streams.views_ts, now - 3600)
            streams_one_hour.append(stream)
            stream.put()

        sorted(streams_one_hour, key=lambda stream : -len(stream.views_ts))

        for i in range(1, 4)
            trending = Trending_stream_entity()
            trending.stream_item = streams_one_hour[i-1]
            trending.rank = i
            trending.put()
            logging.info("************trend:" + str(trending))

        email_body = "\nTeam Maroom Stream Rank:\n"

        trendings = Trending_stream_entity.query().fetch(3)


        for trend in trendings:
            email_body += "\tRank: {} Name {} View count:{}\n".format(trend.rank, trend.stream.name, len(trend.stream.view_ts))
        email_body += "Thanks,\nTeam Maroom\n"

        logging.info("************trend:" + email_body)

        send_approved_mail('example@gmail.com', "cheng1024mail@gmail.com", "Team Maroon Trending", email_body)
        self.response.content_type = 'text/plain'
        self.response.write('Sent an emails.')

app = webapp2.WSGIApplication([
    ('/trending_cron', Trending_cron)
], debug=True)
