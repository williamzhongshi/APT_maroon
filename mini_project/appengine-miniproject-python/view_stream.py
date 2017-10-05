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
def user_key(name):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('user', name)


class View_Stream(webapp2.RequestHandler):


    def get(self):
        user = users.get_current_user()

        stream_name = self.request.get('name')
        subscriber_list = self.request.get('subs')
        pic_url = self.request.get('pic_url')
        tags = self.request.get('tags')

        #user_obj = User()
        #user_obj.username = user._User__email
        #user_obj.email = user._User__email

        #stream = Stream(parent=user_key(user.email))
        stream_name = self.request.get('name')
        current_stream = Stream.query(Stream.name == stream_name).fetch()
        #Update the view count
        current_count = current_stream.view_count
        current_count += 1
        current_stream.view_count = current_count
        current_stream.put()


        # Just try to retrieve from NDB
        target_query = Photo.query(ancestor=stream_name)
        targets = target_query.fetch(4)

        template_values = {
            'photos': targets,
        }

        template = JINJA_ENVIRONMENT.get_template('ViewStream.html')
        self.response.write(template.render(template_values))

    def post(self):
        user = users.get_current_user()

        # print(user._User__email)
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        # stream = Stream(parent=user_key('abc'))
        logging.info("Hello")
        # user_obj = User.query(User.email == user._User__email)
        # user_obj = User()
        # user_obj.username = users.get_current_user()

        name = self.request.get('txtName')


# [START app]
app = webapp2.WSGIApplication([
    # ('/', MainPage),
    ('/view_stream', View_Stream)
    # ('/sign', Guestbook),
], debug=True)
# [END app]
