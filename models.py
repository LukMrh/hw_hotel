from google.appengine.ext import ndb


class Post(ndb.Model):
    name = ndb.StringProperty()
    surname = ndb.StringProperty()
    email = ndb.StringProperty()
    message = ndb.TextProperty()  # TextProperty is for longer inputs
    date = ndb.DateTimeProperty(auto_now_add=True)
