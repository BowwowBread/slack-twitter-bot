# -*- coding: utf8 -*-

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import config
import json
import slack
import time

class TwitterListener(StreamListener):
  
    def __init__(self, targetWords):
        auth = OAuthHandler(config.ckey, config.csecret)
        auth.set_access_token(config.atoken,  config.asecret)
        self.__stream = Stream(auth, listener=self)
        self.__stream.filter(track=targetWords, async=True)

    def disconnect(self):
        self.__stream.disconnect()

    def on_data(self, data):
        if(json.loads(data)["text"].find("RT @") != -1):
          pass
        else:
          date = json.loads(data)["created_at"]
          message = json.loads(data)["text"]
          name = json.loads(data)["user"]["name"]
          username = "(@" + json.loads(data)["user"]["screen_name"] + ")"
          _id = json.loads(data)["id"]
          slack.post_tweet("시고테스트", date, message, name, username, _id)

    def on_error(self, status_code):
        print(status_code)
        print("error")      

listener = None
def streamingStart(start, targetWords):
    global listener
    if(start):
      print("start")
      listener = TwitterListener(targetWords)
    else:
      print("end")
      if(listener != None):
        listener.disconnect()
        time.sleep(3)
