
# Copyright 2015 Google Inc. All rights reserved.
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

"""
Sample application that demonstrates how to use the App Engine Blobstore API.
For more information, see README.md.
"""

from entities_def import User, Photo, Stream

# [START all]
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
import webapp2
import logging, pdb


# This datastore model keeps track of which users uploaded which photos.
# class UserPhoto(ndb.Model):
#     user = ndb.StringProperty()
#     blob_key = ndb.BlobKeyProperty()

def stream_key(name):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('stream', name)

class PhotoUploadFormHandler(webapp2.RequestHandler):
    def get(self):
        # [START upload_url]
        upload_url = blobstore.create_upload_url('/blobstore/upload')
        # [END upload_url]
        # [START upload_form]
        # To upload files to the blobstore, the request method must be "POST"
        # and enctype must be set to "multipart/form-data".
        self.response.out.write("""
<html><body>
<form action="{0}" method="POST" enctype="multipart/form-data">
  Upload File: <input type="file" name="file"><br>
  <input type="submit" name="submit" value="Submit">
</form>
</body></html>""".format(upload_url))
        #self.redirect('/blobstore/upload')
        # [END upload_form]


# [START upload_handler]
class PhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:
            temp_stream_name = "Labrador"
            upload = self.get_uploads()[0]
            # #logging.info("%s", dir(upload))
            # for i in upload:
            #     logging.info("%s", dir(i))
            #     logging.info("Hello %s", i.key())
            user_email = users.get_current_user()._User__email
            #stream = Stream(parent=user_key(user_obj.email))
            user_photo = Photo(
                name=upload.filename,
                blob_key=upload.key(),
                parent=stream_key(temp_stream_name)
            )
            user_photo.put()

            targets = Stream.query(Stream.name==temp_stream_name).fetch()

            for target in targets:
                logging.info("Before %d", target.num_pictures)
                target.num_pictures += 1
                logging.info("After %d", target.num_pictures)
                target.put()

            self.redirect('/blobstore/view_photo/%s' % upload.key())

        except Exception as e:
            logging.error(e)
            self.error(500)
# [END upload_handler]


# [START download_handler]
class ViewPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, photo_key):
        if not blobstore.get(photo_key):
            self.error(404)
        else:
            self.send_blob(photo_key)
# [END download_handler]


app = webapp2.WSGIApplication([
    ('/blobstore', PhotoUploadFormHandler),
    ('/blobstore/upload', PhotoUploadHandler),
    ('/blobstore/view_photo/([^/]+)?', ViewPhotoHandler),
], debug=True)
# [END all]


# import cloudstorage
# from google.appengine.api import app_identity, images
# from google.appengine.ext import blobstore
# from google.appengine.ext.webapp import blobstore_handlers
# import webapp2
# import logging
#
#
# # This handler creates a file in Cloud Storage using the cloudstorage
# # client library and then reads the data back using the Blobstore API.
# class CreateAndReadFileHandler(webapp2.RequestHandler):
#     def get(self):
#         logging.info("Hello Williamz1")
#         # Get the default Cloud Storage Bucket name and create a file name for
#         # the object in Cloud Storage.
#         bucket = app_identity.get_default_gcs_bucket_name()
#
#         upload_url = blobstore.create_upload_url('/upload_photo')
#         # [END upload_url]
#         # [START upload_form]
#         # To upload files to the blobstore, the request method must be "POST"
#         # and enctype must be set to "multipart/form-data".
#         self.response.out.write("""
#         <html><body>
#         <form action="{0}" method="POST" enctype="multipart/form-data">
#           Upload File: <input type="file" name="file"><br>
#           <input type="submit" name="submit" value="Submit">
#         </form>
#         </body></html>""".format(upload_url))
#         # [END upload_form]
#
#
#         # Cloud Storage file names are in the format /bucket/object.
#         filename = '/{}/blobstore_demo'.format(bucket)
#
#         # Create a file in Google Cloud Storage and write something to it.
#         # with cloudstorage.open(filename, 'w') as filehandle:
#         #     filehandle.write('abcde\n')
#         filename = "/{}/doge.jpg".format(bucket)
#         # In order to read the contents of the file using the Blobstore API,
#         # you must create a blob_key from the Cloud Storage file name.
#         # Blobstore expects the filename to be in the format of:
#         # /gs/bucket/object
#         blobstore_filename = '/gs{}'.format(filename)
#         logging.info("Hello Williamz2")
#         logging.info("%s", blobstore_filename)
#         blob_key = blobstore.create_gs_key(blobstore_filename)
#
#         # Read the file's contents using the Blobstore API.
#         # The last two parameters specify the start and end index of bytes we
#         # want to read.
#         #fileinfo = blobstore.FileInfo(blobstore_filename)
#         if blob_key:
#             blob_info = blobstore.get(blob_key)
#
#             if blob_info:
#                 img = images.Image(blob_key=blob_key)
#                 img.resize(width=80, height=100)
#                 img.im_feeling_lucky()
#                 thumbnail = img.execute_transforms(output_encoding=images.JPEG)
#
#                 self.response.headers['Content-Type'] = 'image/jpeg'
#                 self.response.out.write(thumbnail)
#                 return
#         self.error(404)
#
#         # Delete the file from Google Cloud Storage using the blob_key.
#         blobstore.delete(blob_key)
#
#
# # This handler creates a file in Cloud Storage using the cloudstorage
# # client library and then serves the file back using the Blobstore API.
# class CreateAndServeFileHandler(blobstore_handlers.BlobstoreDownloadHandler):
#
#     def get(self):
#         # Get the default Cloud Storage Bucket name and create a file name for
#         # the object in Cloud Storage.
#         bucket = app_identity.get_default_gcs_bucket_name()
#
#         # Cloud Storage file names are in the format /bucket/object.
#         filename = '/{}/blobstore_serving_demo'.format(bucket)
#
#         # Create a file in Google Cloud Storage and write something to it.
#         with cloudstorage.open(filename, 'w') as filehandle:
#             filehandle.write('abcde\n')
#
#         # In order to read the contents of the file using the Blobstore API,
#         # you must create a blob_key from the Cloud Storage file name.
#         # Blobstore expects the filename to be in the format of:
#         # /gs/bucket/object
#         blobstore_filename = '/gs{}'.format(filename)
#         blob_key = blobstore.create_gs_key(blobstore_filename)
#
#         # BlobstoreDownloadHandler serves the file from Google Cloud Storage to
#         # your computer using blob_key.
#         self.send_blob(blob_key)
#
#
# app = webapp2.WSGIApplication([
#     ('/blobstore', CreateAndReadFileHandler),
#     ('/blobstore/read', CreateAndReadFileHandler),
#     ('/blobstore/serve', CreateAndServeFileHandler)], debug=True)