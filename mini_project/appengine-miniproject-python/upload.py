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

from google.appengine.api import users, images
from google.appengine.ext import ndb, blobstore
from google.appengine.ext.webapp import blobstore_handlers

from entities_def import User, Photo, Stream
from flask import Flask, jsonify, abort, request, make_response, url_for

import jinja2
import time
import webapp2
import logging, pdb, random

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

stream_name = None
# [END imports]

def stream_key(name):
    """Constructs a Datastore key for a Guestbook entity.
    We use guestbook_name as the key.
    """
    return ndb.Key('stream', name)



class upload(webapp2.RequestHandler):
    def get(self):
        stream_name = self.request.get('name')

        stream = Stream.query(Stream.name == stream_name).fetch()[0]
        offset = self.request.get('offset')
        offset_int = 0
        if offset:
            offset_int = int(offset)

        now = int(time.time())
        if stream.views_ts is None:
            stream.views_ts = [now]
        else:
            stream.views_ts.append(now)

        stream.put()

        logging.info("**********stream:" + str(stream.views_ts))

        user = users.get_current_user()

        user_obj = User()
        # user_obj.username = user._User__email
        user_obj.email = user._User__email

        # current_stream = Stream.query(Stream.name == stream_name).fetch()
        # Update the view count
        logging.info("Stream name: %s" % stream_name)
        target = Stream.query(Stream.name == stream_name).fetch()[0]

        if target.view_count is None:
            target.view_count = 0
        logging.info("Before %d" % target.view_count)
        target.view_count += 1
        logging.info("After %d" % target.view_count)
        target.put()

        # Just try to retrieve from NDB
        targets, next_cursor, more = \
            Photo.query(ancestor=stream_key(stream_name)).order(-Photo.uploaddate).fetch_page(3, offset=offset_int)

        next_ = True if more else False
        if next_:
            offset = offset_int + 3

        upload_url = blobstore.create_upload_url('/uploadfiles/upload')

        template_values = {
            'upload_url': upload_url,
            'photos': targets,
         }
        template = JINJA_ENVIRONMENT.get_template('upload1.html')
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
        stream_name = self.request.get('stream_name')
        # print(user._User__email)
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        try:
            temp_stream_name = stream_name
            target = Stream.query(Stream.name == temp_stream_name).fetch()[0]

            temp_photo_name = self.request.get("txtName")
            temp_photo_comment = self.request.get("txtComments")
            offset = self.request.get("txtOffset")
            upload = self.get_uploads()[0]
            # #logging.info("%s", dir(upload))
            # for i in upload:
            #     logging.info("%s", dir(i))
            #     logging.info("Hello %s", i.key())
            logging.info("Uploading to stream %s using name %s with comment %s" % (temp_stream_name, temp_photo_name,
                                                                                   temp_photo_comment))
            # user_email = users.get_current_user().email()
            # stream = Stream(parent=user_key(user_email))

            logging.info("Before %d" % target.num_pictures)
            target.num_pictures += 1
            logging.info("After %d" % target.num_pictures)
            target.put()

            user_photo = Photo(
                name=temp_photo_name,
                blob_key=upload.key(),
                comment=temp_photo_comment,
                parent=stream_key(temp_stream_name),
                photo_location_lat=random.uniform(-30.0, 30.0),
                photo_location_lng=random.uniform(110.0, 130.0)
                #url=upload.get_serving_url()
            )
            user_photo.put()
            self.redirect('/view_stream?name=%s' % stream_name)
        except Exception as e:
            logging.error(e)
            self.response.out.write(e)
            #self.error(500)


app = webapp2.WSGIApplication([
    # ('/', MainPage),
    ('/upload', upload),
    ('/view_stream/upload', PhotoUploadHandler),
    # ('/sign', Guestbook),
], debug=True)

# [END app]