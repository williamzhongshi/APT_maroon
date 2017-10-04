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

from google.appengine.api import app_identity, mail, users, search
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



class SearchStreams(webapp2.RequestHandler):
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
        template = JINJA_ENVIRONMENT.get_template('SearchStream.html')
        self.response.write(template.render(template_values))
    #
    # def __get_tag(tags):
    #     return __sanitize_str(tags).split(',')
    #
    # def __get_subs(subs):
    #     return __sanitize_str(subs).split(',')
    #
    # def __sanitize_str(s):
    #     return s.strip()
    def search_terms(index):
        # search for documents with pianos that cost less than $5000
        index.search("product = piano AND price < 5000")

    def post(self):
        user = users.get_current_user()

        search_text = self.request.get('txtName')

        #target_query

        # IF USE GOOGLE SEARCH API
        # index = search.Index(name="streamsearch")
        # target_query = Stream.query()
        # targets = target_query.fetch()
        # for target in targets:
        #     fields = [
        #         search.TextField(name="name", value=target.name)
        #     ]
        #     for tag in target.tags:
        #         fields.append(search.TextField(name="tags", value=tag))
        #     d = search.Document(fields=fields, language='en')
        #     search.Index(name="streamsearch").put(d)
        #
        # index = search.Index("streamsearch")
        #
        # search_results = index.search("%s in name OR %s in tags" % (search_text, search_text))
        #
        # #logging.info("%s", dir(search_results))
        # logging.info("Found %d number of results" % len(search_results.results))
        #
        # for i in search_results:
        #     logging.info("Found %s", i)
        #     logging.info("Found %s", dir(i))
        #
        # final_targets = []


        #
        #
        # user_obj = User()
        # user_obj.username =users.get_current_user()
        # user_obj.email = users.get_current_user().email()

        # stream = Stream(parent=user_key('abc'))
        # stream.name = stream_name
        # stream.cover_image = pic_url
        # stream.tags = [tags]
        # stream.subs = [subscriber_list]

        #stream.put()

        # Just try to retrieve from NDB

        # WORKS BUT NOT USING SEARCH API
        target_query = Stream.query()
        targets = target_query.fetch()
        final_targets = []

        for target in targets:
            logging.info("target name %s, tags: %s, search text %s " % (target.name, target.tags, search_text))
            if search_text in target.name or search_text in str(target.tags):
                final_targets.append(target)

        for i in final_targets:
            logging.info("found %s", i.name)

        template_values = {
            'stream': final_targets,
        }

        template = JINJA_ENVIRONMENT.get_template('SearchStream.html')
        self.response.write(template.render(template_values))
        

# [START app]
app = webapp2.WSGIApplication([
    #('/', MainPage),
    ('/searchstream', SearchStreams)
    # ('/sign', Guestbook),
], debug=True)
# [END app]
