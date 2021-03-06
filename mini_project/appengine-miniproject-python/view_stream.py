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

stream_name = None
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
        stream_name = self.request.get('name')
        offset = self.request.get('offset')
        offset_int = 0

        stream = Stream.query(Stream.name==stream_name).fetch()[0]
        if offset:
            offset_int = int(offset)


        now = int(time.time())
        if stream.views_ts is None:
            stream.views_ts = [now]
        else:
            stream.views_ts.append(now)

        stream.put()

        logging.info("**********stream:"+ str(stream.views_ts))

        user = users.get_current_user()

        user_obj = User()
        #user_obj.username = user._User__email
        if user:
            user_obj.email = user._User__email

        #stream = Stream(parent=user_key(user.email))
        #stream_name = self.request.get('name')
        #current_stream = Stream.query(Stream.name == stream_name).fetch()
        #Update the view count
        logging.info("Stream name: %s" % stream_name)
        target = Stream.query(Stream.name == stream_name).fetch()[0]

        if target.view_count is None:
            target.view_count = 0
        logging.info("Before %d" % target.view_count)
        target.view_count += 1
        logging.info("After %d" % target.view_count)
        target.put()

        # Just try to retrieve from NDB
        targets, next_cursor, more = Photo.query().order(-Photo.uploaddate).fetch_page(4, offset=offset_int)
        #targets = Photo.query().order(-Photo.uploaddate).fetch(4)

        next_ = True if more else False
        next_offset = ''
        if next_:
            offset = offset_int + 4



        #upload_url = blobstore.create_upload_url('/view_stream/upload')
        upload_url = '/view_stream/upload'

        template_values = {
            'photos': targets,
            'upload_url': upload_url,
            'stream_name': stream_name,
            'offset': offset,
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
            stream_name = self.request.get("txtStream")
            photo_name = self.request.get("txtName")
            photo_comment = self.request.get("txtComments")
            offset = self.request.get("txtOffset")
            #upload = self.get_uploads()[0]

            avatar = self.request.get('img')

            # #logging.info("%s", dir(upload))
            # for i in upload:
            #     logging.info("%s", dir(i))
            #     logging.info("Hello %s", i.key())
            logging.info("Uploading to stream %s using name %s with comment %s" % (stream_name, photo_name,
                                                                                   photo_comment))
            # user_email = users.get_current_user().email()
            # stream = Stream(parent=user_key(user_email))


            user_photo = Photo()
            user_photo.name = photo_name
            user_photo.comment = photo_comment
            user_photo.photo_image = avatar
            user_photo.put()
            self.redirect('/view_stream?name=%s' % stream_name)
        except Exception as e:
            logging.error(e)
            self.response.out.write(e)
            #self.error(500)

class Image(webapp2.RequestHandler):
    def get(self):
        #photo_key = ndb.Key(urlsafe=self.request.get('img_id'))
        #photo = photo_key.get()

        photo_id = int(self.request.get('img_id'))
        photo = Photo.get_by_id(photo_id)
        #avatar = images.resize(photo.photo_image, 5, 5)
        if photo.photo_image:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(photo.photo_image)
        else:
            self.response.out.write('No image')

class Subscribe(webapp2.RequestHandler):
    def get(self):
        sub_stream = self.request.get('stream')
        user = users.get_current_user()

        # print(user._User__email)
        if user:
            target = Stream.query(Stream.name == sub_stream).fetch()[0]
            id = user.user_id()
            self.response.out.write(id)
            target.subscribers.append(id)
            target.put()
            self.redirect('/view_stream?name=%s' % sub_stream)
        else:
            err_msg = "You are not logged in. Please <a href='/'>login</a> to subscribe."
            self.response.out.write(err_msg)
            #self.redirect('/view_stream?name=%s' % sub_stream)

app = webapp2.WSGIApplication([
    # ('/', MainPage),
    ('/view_stream', View_Stream),
    ('/view_stream/upload', PhotoUploadHandler),
    ('/view_stream/image', Image),
    ('/view_stream/subscribe', Subscribe),
    # ('/sign', Guestbook),
], debug=True)

# [END app]
