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

from google.appengine.api import blobstore, users
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers

from entities_def import User, Photo, Stream

import jinja2
import webapp2
import logging, pdb

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


def stream_key(name):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('stream', name)

class View_Stream(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        stream_name = self.request.get('name')
        subscriber_list = self.request.get('subs')
        pic_url = self.request.get('pic_url')
        tags = self.request.get('tags')

        user_obj = User()
        #user_obj.username = user._User__email
        user_obj.email = user._User__email

        #stream = Stream(parent=user_key(user.email))
        stream_name = self.request.get('name')
        current_stream = Stream.query(Stream.name == stream_name).fetch()
        #Update the view count
        targets = Stream.query(Stream.name == stream_name, ancestor=user_key(user_obj.email)).fetch()

        for target in targets:
            logging.info("Before %d", target.num_pictures)
            target.num_pictures += 1
            logging.info("After %d", target.num_pictures)
            target.put()

        # Just try to retrieve from NDB
        target_query = Photo.query(ancestor=stream_key(stream_name))
        targets = target_query.fetch(4)

        upload_url = blobstore.create_upload_url('/view_stream/upload')

        template_values = {
            'photos': targets,
            'upload_url': upload_url,
        }

        template = JINJA_ENVIRONMENT.get_template('ViewStream.html')
        self.response.write(template.render(template_values))

    def __sanitize_str(self, s):
        return s.strip()

    def __get_tag(self, tags):
        return self.__sanitize_str(tags).split(',')

    def __get_subs(self, subs):
        return self.__sanitize_str(subs).split(',')


class PhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        user = users.get_current_user()

        # print(user._User__email)
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        try:
            temp_stream_name = "Labrador"
            temp_photo_name = "image1"
            upload = self.get_uploads()[0]
            # #logging.info("%s", dir(upload))
            # for i in upload:
            #     logging.info("%s", dir(i))
            #     logging.info("Hello %s", i.key())
            user_email = users.get_current_user()._User__email
            stream = Stream(parent=user_key(user_email))

            user_photo = Photo(
                name=temp_photo_name,
                blob_key=upload.key(),
                parent=stream_key(temp_stream_name)
            )
            user_photo.put()
            self.redirect('/view_stream?name=Labrador')
        except Exception as e:
            logging.error(e)
            self.response.out.write(e)
            #self.error(500)



app = webapp2.WSGIApplication([
    # ('/', MainPage),
    ('/view_stream', View_Stream),
    ('/view_stream/upload', PhotoUploadHandler),

    # ('/sign', Guestbook),
], debug=True)

# [END app]
