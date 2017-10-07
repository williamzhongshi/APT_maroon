#!/usr/bin/env python

# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START imports]
import os
import urllib
import logging
import cloudstorage as gcs

from google.appengine.api import app_identity, mail, users
from google.appengine.ext import ndb

from entities_def import User, Photo, Stream

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

class Subscribe(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            # TODO: do something
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        user_obj = User.query(User.email== users.get_current_user().email()).fetch()[0]

        stream_name = self.request.get('stream_name')

        if len(user_obj.subscribe_stream) == 0:
            user_obj.subscribe_stream = []

        user_obj.subscribe_stream.append(stream_name)
        user_obj.put()

        logging.info("**************subscribe_stream:" + str(user_obj.subscribe_stream))

        self.redirect("/view_stream?name=" + stream_name)

# [START app]
app = webapp2.WSGIApplication([
    ('/subscribe', Subscribe)
], debug=True)
# [END app]
