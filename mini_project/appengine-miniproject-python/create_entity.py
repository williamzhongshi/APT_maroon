# [START imports]
import os
import urllib
import logging
import cloudstorage as gcs

from google.appengine.api import blobstore, users
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images

from entities_def import User, Photo, Stream

import jinja2
import time
import webapp2
import logging, pdb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Create_Entity(webapp2.RequestHandler):
    def get(self):
        sandy = Stream()
        sandy.name = 'Cats'

        sandy_key = sandy.put()

        self.response.out.write("Entity created")

        photo1 = Photo()
        photo1.name = "Cat-Image1"
        photo1.comment = "Comment"
        photo1_key = photo1.put()
        self.response.out.write("Photo created")


app = webapp2.WSGIApplication([
    # ('/', MainPage),
    ('/create_entity', Create_Entity),
    # ('/sign', Guestbook),
], debug=True)


