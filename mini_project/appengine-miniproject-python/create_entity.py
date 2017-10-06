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



sandy = Stream()
sandy.name = 'Dogs'
sandy.tags = 'Dogs, puppy'
sandy_key = sandy.put()



