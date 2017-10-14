import os
import urllib
import logging
import cloudstorage as gcs

from google.appengine.api import app_identity, mail, users, search
from google.appengine.ext import ndb

from entities_def import User, Photo, Stream

import jinja2
import webapp2
import logging
import json
import datetime
import time


class Central_tzinfo(datetime.tzinfo):

    """Implementation of the Pacific timezone."""
    def utcoffset(self, dt):
        return datetime.timedelta(hours=-6) + self.dst(dt)

    def _FirstSunday(self, dt):
        """First Sunday on or after dt."""
        return dt + datetime.timedelta(days=(6-dt.weekday()))

    def dst(self, dt):
        # 2 am on the second Sunday in March
        dst_start = self._FirstSunday(datetime.datetime(dt.year, 3, 8, 2))
        # 1 am on the first Sunday in November
        dst_end = self._FirstSunday(datetime.datetime(dt.year, 11, 1, 1))

        if dst_start <= dt.replace(tzinfo=None) < dst_end:
            return datetime.timedelta(hours=1)
        else:
            return datetime.timedelta(hours=0)
    def tzname(self, dt):
        if self.dst(dt) == datetime.timedelta(hours=0):
            return "CDT"
        else:
            return "CDT"
#pacific_time = datetime.datetime.fromtimestamp(time.mktime(utc_time.timetuple()), Pacific_tzinfo())


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)



def user_key(name):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('user', name)
#
# class geo_point():
#     def __init__(self, lat, lng):
#         self.lat = lat
#         self.lng = lng

# class point(ndb.Model):
#     lat = ndb.FloatProperty()
#     lng = ndb.FloatProperty()

class point():
    def __init__(self, lat, lng):
        self.lat = float(lat)
        self.lng = float(lng)

# def serialize(model):
#     #all_instances = model.all()
#     item_list = []
#     for i in all_instances:
#         d = ndb.to_dict(i)
#         item_list.append(d)
#     return json.dumps(item_list)


class Geo_View(webapp2.RequestHandler):

    def get(self):
        logging.info("GEO VIEWS!!!")
        user = users.get_current_user()

        lat_data = []
        lng_data = []
        img_urls = []
        pic_dates = []

        test_point0_lat = -31.563910
        test_point0_lng = 147.154312

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        user_obj = User.query(User.email == user.email()).fetch()[0]
        target_query = Photo.query()
        targets = target_query.fetch()

        logging.info("HELLO")

        for photo in targets:
            single_lat = photo.photo_location_lat
            single_lng = photo.photo_location_lng
            if single_lat is not None and single_lng is not None:
                logging.info("%f %f" % (single_lat, single_lng))

                lat_data.append(single_lat)
                lng_data.append(single_lng)
                img_urls.append('%s' % photo.url.encode('utf_8'))
                pic_dates.append(int(str(datetime.datetime.fromtimestamp(time.mktime(photo.uploaddate.timetuple()), Central_tzinfo())).split(" ")[0].replace('-', '')))

        logging.info(" Dates %s" % pic_dates)
        logging.info(" Urls %s " % img_urls)

        template_values = {
            'stream': targets,
            'lat': lat_data,
            'lng': lng_data,
            'img_urls': img_urls,
            'dates': pic_dates,
            'sorted_dates': sorted(pic_dates)
        }

        template = JINJA_ENVIRONMENT.get_template('map_cluster.html')
        self.response.write(template.render(template_values).decode('utf-8'))


app = webapp2.WSGIApplication([
    ('/geo_view', Geo_View)
], debug=True)
