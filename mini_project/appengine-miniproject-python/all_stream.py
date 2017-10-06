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


class All_Stream(webapp2.RequestHandler):

    def get(self):
        logging.info("Show All Streams!!!")
        user = users.get_current_user()

        # print(user._User__email)
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        user_obj = User.query(User.email== user.email()).fetch()[0]
        target_query = Stream.query()
        targets = target_query.fetch()

        template_values = {
            'stream': targets,
        }

        template = JINJA_ENVIRONMENT.get_template('AllStreams.html')
        self.response.write(template.render(template_values))

    #
    # def post(self):
    #
    #
    #     # assume logged in
    #     user_obj = User.query(User.email == users.get_current_user().email()).fetch()[0]
    #
    #     # print(user._User__email)
    #     # if user:
    #     #     url = users.create_logout_url(self.request.uri)
    #     #     url_linktext = 'Logout'
    #     # else:
    #     #     url = users.create_login_url(self.request.uri)
    #     #     url_linktext = 'Login'
    #
    #
    #     #stream = Stream(parent=user_key('abc'))
    #     #logging.info("Hello")
    #     #user_obj = User.query(User.email == user._User__email)
    #     #user_obj = User()
    #     #user_obj.username = users.get_current_user()
    #
    #     all_checkboxes = self.request.get('chkDelete')
    #     logging.info("%s", all_checkboxes)
    #     logging.info("%s", dir(all_checkboxes))
    #
    #     check = self.request.get_all('chkDelete')
    #
    #     # logging.info("checked: %s" % str(check))
    #     for i in check:
    #         stream_to_delete = i.split('/')
    #         logging.info("User selected deleting %s", stream_to_delete)
    #         found_stream = Stream.query(Stream.name == stream_to_delete, ancestor=user_key(user_obj.email))
    #         for j in found_stream.fetch():
    #             # TODO, the clean way is to delete pictures too
    #             logging.info("Removing stream: %s ", j.name)
    #             j.key.delete()
    #
    #     sub_check = self.request.get_all('sub_chkDelete')
    #
    #     target_query = Stream.query(ancestor=user_key(user_obj.email))
    #     targets = target_query.fetch()
    #     for i in sub_check:
    #         stream_to_unsub = i.strip('/')
    #         logging.info("stream to unsub %s" % stream_to_unsub)
    #         logging.info("User currently subscribes to %s" % user_obj.subscribe_stream)
    #         logging.info("User selected to remove subscription %s", stream_to_unsub.encode('utf-8'))
    #         user_obj.subscribe_stream.remove(stream_to_unsub.encode('utf-8'))
    #         logging.info("User now subscribe to %s" % user_obj.subscribe_stream)
    #         user_obj.put()
    #
    #     sub_target = []
    #
    #     logging.info("User subscribed for %d of streams" % len(user_obj.subscribe_stream))
    #
    #     for stream_name in user_obj.subscribe_stream:
    #         logging.info("Query for %s in stream names" % stream_name)
    #         stream_query = Stream.query(Stream.name == stream_name)
    #         # assuming no repeated stream names
    #         sub_target.append(stream_query.fetch()[0])
    #     for sub in sub_target:
    #         logging.info("%s" % sub.name)
    #
    #     template_values = {
    #         'stream': targets,
    #     }
    #
    #
    #     template_values = {
    #         'stream': targets,
    #         'stream_subs': sub_target
    #     }
    #
    #     template = JINJA_ENVIRONMENT.get_template('AllStreams.html')
    #     self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    # ('/', MainPage),
    ('/all_stream', All_Stream)
    # ('/sign', Guestbook),
], debug=True)
