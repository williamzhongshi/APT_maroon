from google.appengine.ext import ndb

class Photo(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    url = ndb.StringProperty(indexed=True)
    blob_key = ndb.BlobKeyProperty()
    comment = ndb.StringProperty(indexed=False)
    uploaddate = ndb.DateTimeProperty(auto_now_add=True)
    photo_image = ndb.BlobProperty()
    photo_location_lat = ndb.FloatProperty()
    photo_location_lng = ndb.FloatProperty()

class User(ndb.Expando):
    username = ndb.StringProperty(indexed=True)
    email = ndb.StringProperty(indexed=True)
    subscribe_stream = ndb.StringProperty(repeated=True)

class Stream(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    tags = ndb.StringProperty(indexed=True, repeated=True)
    cover_image = ndb.StringProperty(indexed=False)
    subscribers = ndb.StringProperty(repeated=True)
    view_count = ndb.IntegerProperty(indexed=True)
    num_pictures = ndb.IntegerProperty()
    last_picture_date = ndb.DateProperty(auto_now=True)
    views_ts = ndb.IntegerProperty(repeated=True)

class Trending_stream_entity(ndb.Model):
    stream_item = ndb.StructuredProperty(Stream, repeated=False)
    rank = ndb.IntegerProperty(repeated=False)
    ts = ndb.IntegerProperty(repeated=False)

class CronJobFrequency(ndb.Model):
    frequency = ndb.StringProperty()
