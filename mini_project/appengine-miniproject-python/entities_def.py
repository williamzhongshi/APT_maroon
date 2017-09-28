
from google.appengine.ext import ndb

class User(ndb.Model):
    username = ndb.StringProperty(indexed=True)
    email = ndb.StringProperty(indexed=False)
#
class Photo(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    url = ndb.StringProperty(indexed=True, repeated=True)

class Stream(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    tags = ndb.StringProperty(indexed=True, repeated=True)
    cover_image = ndb.StringProperty(indexed=False)
    subscribers = ndb.StructuredProperty(User, repeated=True)
    view_count = ndb.IntegerProperty(indexed=True)
    photos = ndb.StructuredProperty(Photo)