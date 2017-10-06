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
from google.appengine.api import app_identity
from google.appengine.api import mail

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def send_approved_mail(sender_address, dest_address, subject_str, body_str):
    # [START send_mail]
    mail.send_mail(sender=sender_address,
                   to="<{}>".format(dest_address),
                   subject=subject_str,
                   body=body_str)

class Trending_cron(webapp2.RequestHandler):

    def get(self):

        for entity in Trending_stream_entity.query().fetch():
            entity.key.delete()

        streams = Stream.query().order(-Stream.view_count).fetch(3)
        rank = 1;

        for entity in streams:
            trending = Trending_stream_entity()
            trending.stream_item = entity
            trending.rank = rank
            rank+=1
            trending.put()
            logging.info("************trend:" + str(trending))

        email_body = "\nTeam Maroom Stream Rank:\n"
        rank = 1;
        for stream in streams:
            email_body += "\tRank: {} Name {} View count:{}\n".format(rank, stream.name, stream.view_count)
            rank += 1
        email_body += "Thanks,\nTeam Maroom\n"

        logging.info("************trend:" + email_body)

        send_approved_mail('example@gmail.com', "cheng1024mail@gmail.com", "Team Maroon Trending", email_body)
        self.response.content_type = 'text/plain'
        self.response.write('Sent an emails.')

app = webapp2.WSGIApplication([
    ('/trending_cron', Trending_cron)
], debug=True)
