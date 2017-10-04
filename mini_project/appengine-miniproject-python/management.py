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


        # if all_checkboxes:
        #     logging.info("Checkbox clicked")
        # else:
        #     logging.info("Checkbox unchecked")
        #
        # if 'chkDelete' in self.request:
        #     logging.info("Checkbox chedked")
        # else:
        #     logging.info("Checkbox not checked")

        # logging.info("hello")
        # logging.info(dir(targets))
        # for i in targets:
        #     print user._User__email, dir(targets)

        template_values = {
            'stream': targets,
        }

        template = JINJA_ENVIRONMENT.get_template('Management.html')
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


        #stream = Stream(parent=user_key('abc'))
        logging.info("Hello")
        #user_obj = User.query(User.email == user._User__email)
        #user_obj = User()
        #user_obj.username = users.get_current_user()

        all_checkboxes = self.request.get('chkDelete')
        logging.info("%s", all_checkboxes)
        logging.info("%s", dir(all_checkboxes))

        check = self.request.get_all('chkDelete')

        for i in check:
            stream_to_delete = i.strip("/")
            logging.info("User selected deleting %s", stream_to_delete)
            found_stream = Stream.query(Stream.name==stream_to_delete, ancestor=user_key(user._User__email))
            for j in found_stream.fetch():
                logging.info("Removing stream: %s TODO, the clean way is to delete the pictures", j.name)
                j.key.delete()

        target_query = Stream.query(ancestor=user_key(user._User__email))
        targets = target_query.fetch(10)

        template_values = {
            'stream': targets,
        }

        template = JINJA_ENVIRONMENT.get_template('Management.html')
        self.response.write(template.render(template_values))


        #
        # if all_checkboxes:
        #     logging.info("Checkbox clicked")
        # else:
        #     logging.info("Checkbox unchecked")

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
