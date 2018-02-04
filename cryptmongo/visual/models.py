# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from mongoengine import *

connect('CryptoStats',alias='rawdata')
connect('CryptoTweets',alias='tweetdata')
    
class Stats(Document):
    # Meta variables.
    meta = {
        'db_alias': 'rawdata',
        'collection': 'Stats'
    }
    currname = StringField()
    Date = StringField()
    Open = FloatField()
    High = FloatField()
    Low = FloatField()
    Close = FloatField()
    Volume = IntField()
    Market_Cap = IntField()

class Tweets(Document):
    # Meta variables.
    meta = {
        'db_alias': 'tweetdata',
        'collection': 'Tweets'
    }
    currname = StringField()
    follower_count = IntField()
    friends_count = IntField()
    listed_count = IntField()
    created = StringField()
    tweetId = StringField()
    tweetText = StringField()
    retweeted_count = IntField()
    favourite_count = IntField()
    