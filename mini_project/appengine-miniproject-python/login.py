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

# from oauth2client import client
# from oauth2client.contrib import appengine
# from googleapiclient import discovery

from entities_def import User

from google.appengine.api import memcache
from google.appengine.api import app_identity, mail, users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent. However, the write rate should be limited to
# ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)


# [START greeting]
class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)


class Greeting(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
# [END greeting]

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

#
# # Helpful message to display in the browser if the CLIENT_SECRETS file
# # is missing.
# MISSING_CLIENT_SECRETS_MESSAGE = """
# <h1>Warning: Please configure OAuth 2.0</h1>
# <p>
# To make this sample run you will need to populate the client_secrets.json file
# found at:
# </p>
# <p>
# <code>%s</code>.
# </p>
# <p>with information found on the <a
# href="https://code.google.com/apis/console">APIs Console</a>.
# </p>
# """ % CLIENT_SECRETS
#
# http = httplib2.Http(memcache)
# service = discovery.build("plus", "v1", http=http)
# decorator = appengine.oauth2decorator_from_clientsecrets(
#     CLIENT_SECRETS,
#     scope='https://www.googleapis.com/auth/plus.me',
#     message=MISSING_CLIENT_SECRETS_MESSAGE)
#
#
#
#
#


# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):

        user = users.get_current_user()
        logging.info("*************user:" + str(user))
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            target_user = User.query(User.email == user.email()).fetch()

            if len(target_user) == 0:
                logging.info("User not found, creating User entity %s" % users.get_current_user().email())
                logging.info("%s", dir(user))
                user_obj = User()
                user_obj.username = user.email()  # not sure what this is for
                user_obj.email = user.email()
                user_obj.put()
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login Using Google'

        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
            # 'url': decorator.authorize_url(),
            # 'has_credentials': decorator.has_credentials()
        }

        template = JINJA_ENVIRONMENT.get_template('Login.html')
        self.response.write(template.render(template_values))

    # def post(self):
    #     # template_values = {
    #     #     'in_email': user,
    #     #     # 'greetings': greetings,
    #     #     # 'guestbook_name': urllib.quote_plus(guestbook_name),
    #     #     'url': url,
    #     #     'url_linktext': url_linktext,
    #     # }
    #     input_email = self.request.get('txtUserName')

# class AboutHandler(webapp2.RequestHandler):
#
#   @decorator.oauth_required
#   def get(self):
#     try:
#       http = decorator.http()
#       user = service.people().get(userId='me').execute(http=http)
#       text = 'Hello, %s!' % user['displayName']
#
#       template = JINJA_ENVIRONMENT.get_template('welcome.html')
#       self.response.write(template.render({'text': text }))
#     except client.AccessTokenRefreshError:
#       self.redirect('/')


# [END main_page]


# [START guestbook]
# class Guestbook(webapp2.RequestHandler):
#
#     def post(self):
#         # We set the same parent key on the 'Greeting' to ensure each
#         # Greeting is in the same entity group. Queries across the
#         # single entity group will be consistent. However, the write
#         # rate to a single entity group should be limited to
#         # ~1/second.
#         guestbook_name = self.request.get('guestbook_name',
#                                           DEFAULT_GUESTBOOK_NAME)
#         greeting = Greeting(parent=guestbook_key(guestbook_name))
#
#         if users.get_current_user():
#             greeting.author = Author(
#                     identity=users.get_current_user().user_id(),
#                     email=users.get_current_user().email())
#         #test email
#         user_address = "williamzhongshi@gmail.com"
#
#         greeting.content = self.request.get('content')
#         # mail.send_mail(sender=user_address, to="williamzhongshi@gmail.com", subject="AppEngine Email Test",
#         #                body=greeting.content)
#
#         greeting.put()
#
#         query_params = {'guestbook_name': guestbook_name}
#         self.redirect('/?' + urllib.urlencode(query_params))
# # [END guestbook]


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    # ('/sign', Guestbook),
    #('/about/, AboutHandler'),
    #(decorator.callback_path, decorator.callback_handler()),

], debug=True)
# [END app]
