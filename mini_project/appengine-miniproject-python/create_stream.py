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


class Create_Stream(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        template_values = {
            'user': user,
        }

        # create user
       # user_obj = User()
       # user_obj.username = user._User__email
       # user_obj.email = user._User__email
       # user_obj.put()

        template = JINJA_ENVIRONMENT.get_template('CreateStream.html')
        self.response.write(template.render(template_values))

    def __sanitize_str(self, s):
        return s.strip()

    def __get_tag(self, tags):
        return self.__sanitize_str(tags).split(',')

    def __get_subs(self, subs):
        return self.__sanitize_str(subs).split(',')

    def post(self):
        user_obj = User.query(User.email== users.get_current_user().email()).fetch()[0]

        stream_name = self.request.get('name')
        subscriber_list = self.request.get('subs')
        pic_url = self.request.get('pic_url')
        tags = self.request.get('tags')
        cover_picture = self.request.get('cover_pic')

        origin_stream = Stream.query(Stream.name==stream_name).fetch()
        logging.info("*******************origin stream: " + str(origin_stream))

        if len(origin_stream) != 0:
            logging.info("!! DUPLICATE FOUND, ERROR !!")
            template_values_none = {}
            template = JINJA_ENVIRONMENT.get_template('Error.html')
            self.response.write(template.render(template_values_none))
            return

        stream = Stream(parent=user_key(user_obj.email))
        stream.name = stream_name
        stream.cover_image = pic_url
        stream.tags = self.__get_tag(tags)
        stream.subs = self.__get_subs(subscriber_list)
        stream.num_pictures = 0
        stream.put()

        for sub in stream.subs:
            target_user = User.query(User.email==sub).fetch()
            if len(target_user) == 0:
                continue
            logging.info("adding stream %s to user %s's subcription list" % (stream.name, target_user[0].email))
            target_user[0].subscribe_stream.append(stream.name)
            target_user[0].put()

        # Just try to retrieve from NDB
        target_query = Stream.query(ancestor=user_key(user_obj.email))
        targets = target_query.fetch(10)

        sub_list = []
        for subs in user_obj.subscribe_stream:
            stream_subs = Stream.query(ancestor=user_key(user_obj.email)).fetch(1)
            if len(stream_subs) == 0:
                continue
            sub_list.append(stream_subs[0])

        logging.info(str(sub_list))

        template_values = {
            'stream': targets,
            'stream_subs':sub_list,
        }

        template = JINJA_ENVIRONMENT.get_template('management.html')
        self.response.write(template.render(template_values))
        

# [START app]
app = webapp2.WSGIApplication([
    ('/create_stream', Create_Stream)
], debug=True)
# [END app]
