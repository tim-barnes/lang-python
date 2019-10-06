from mongoengine import *

connect(
  db='tracr',
  host='cache',
  port=27017,
  username='root',
  password='JT7n1r8f50RqPOhuwfIXsJxq',
  authentication_source='admin'
)

class Kitten(Document):
    name = StringField(required=True)
    colour = StringField(required=True)

silence = Kitten(name='silence', colour='tabby').save()
