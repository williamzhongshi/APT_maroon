import os
import urllib
import logging
import cloudstorage as gcs

from google.appengine.api import app_identity, mail, users
from google.appengine.ext import ndb

from entities_def import User, Photo, Stream

import jinja2
import webapp2
import logging



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)



def user_key(name):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('user', name)


class Management(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()

        user_obj = User()
        user_obj.email = user._User__email
        # print(user._User__email)
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        target_query = Stream.query(ancestor=user_key(user_obj.email))
        targets = target_query.fetch(10)

        # logging.info("hello")
        # logging.info(dir(targets))
        # for i in targets:
        #     print user._User__email, dir(targets)

        template_values = {
            'stream': targets,
        }

        template = JINJA_ENVIRONMENT.get_template('Management.html')
        self.response.write(template.render(template_values))

    # def post(self):
    #     user = users.get_current_user()
    #
    #     stream_name = self.request.get('name')
    #     subscriber_list = self.request.get('subs')
    #     pic_url = self.request.get('pic_url')
    #     tags = self.request.get('tags')
    #
    #     user_obj = User()
    #     user_obj.username ='abc' #users.get_current_user()
    #     user_obj.email = 'abc@gmail.com' #users.get_current_user().email()
    #
    #     stream = Stream(parent=user_key('abc'))
    #     stream.name = stream_name
    #     stream.cover_image = pic_url
    #     stream.tags = [tags]
    #     stream.subs = [subscriber_list]
    #
    #     stream.put()
    #
    #     # Just try to retrieve from NDB
    #     target_query = Stream.query(ancestor=user_key('abc'))
    #     targets = target_query.fetch(10)
    #
    #     template_values = {
    #         'stream': targets,
    #     }
    #
    #     template = JINJA_ENVIRONMENT.get_template('show_stream.html')
    #     self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    # ('/', MainPage),
    ('/management', Management)
    # ('/sign', Guestbook),
], debug=True)