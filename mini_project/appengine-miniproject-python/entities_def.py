
from google.appengine.ext import ndb



class Photo(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    url = ndb.StringProperty(indexed=True)
    #photo_id
    #stream = ndb.ReferenceProperty(Stream)

class User(ndb.Model):
    username = ndb.StringProperty(indexed=True)
    email = ndb.StringProperty(indexed=False)
    #owned_streams = ndb.StructuredProperty()

class Stream(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    tags = ndb.StringProperty(indexed=True, repeated=True)
    cover_image = ndb.StringProperty(indexed=False)
    subscribers = ndb.StructuredProperty(User, repeated=True)
    view_count = ndb.IntegerProperty(indexed=True)
    num_pictures = ndb.IntegerProperty()
    last_picture_date = ndb.DateProperty(auto_now=True)

    #photos = ndb.StructuredProperty(Photo, repeated=True)
    #owner = ndb.ReferenceProperty(User)


    #stream_id
    #photos = []


