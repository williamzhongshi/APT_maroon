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
        index = search.Index(name="search_stream")
        target_query = Stream.query()
        targets = target_query.fetch()
        for target in targets:
            fields = [
                search.TextField(name="name", value=target.name)
            ]
            for tag in target.tags:
                fields.append(search.TextField(name="tags", value=tag))
            d = search.Document(fields=fields, language='en')
            search.Index(name="search_stream").put(d)

        #index = search.Index()

        #search_results = index.search("%s in name OR %s in tags" % (search_text, search_text))
        search_results = index.search(search_text)
        #logging.info("%s", dir(search_results))
        logging.info("Found %d number of results" % len(search_results.results))

        final_targets = []
        counter = 0
        for i in search_results:
            found_name = i.field("name".encode('utf-8')).value.decode('utf-8')
            logging.info("Found %s" % found_name)
            if counter < 5:
                target_query = Stream.query(Stream.name == found_name)
                target = target_query.fetch()[0]
                final_targets.append(target)
                counter += 1
            else:
                break
        logging.info("Listing %d of streams" % len(final_targets))
        for i in final_targets:
            logging.info("found %s", i.name)
        # remove all indexes
        while True:
            # until no more documents, get a list of documents,
            # constraining the returned objects to contain only the doc ids,
            # extract the doc ids, and delete the docs.
            document_ids = [document.doc_id for document in index.get_range(ids_only=True)]
            if not document_ids:
                break
            index.delete(document_ids)

        # Just try to retrieve from NDB
        # # WORKS BUT NOT USING SEARCH API
        # target_query = Stream.query()
        # targets = target_query.fetch()
        # final_targets = []
        #
        # for target in targets:
        #     logging.info("target name %s, tags: %s, search text %s " % (target.name, target.tags, search_text))
        #     if search_text in target.name or search_text in str(target.tags):
        #         final_targets.append(target)
        #
        # for i in final_targets:
        #     logging.info("found %s", i.name)

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
