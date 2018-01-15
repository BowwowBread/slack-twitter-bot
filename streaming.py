# -*- coding: utf8 -*-

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import config
import json
import slack
import time


# class MyStreamListener(StreamListener):
  
#     def on_data(self, data):
#         if(json.loads(data)["text"].find("RT @") != -1):
#           pass
#         else:
#           date = json.loads(data)["created_at"]
#           message = json.loads(data)["text"]
#           name = json.loads(data)["user"]["name"] + "(@" + json.loads(data)["user"]["screen_name"] + ")"
#           _id = json.loads(data)["id"]
#           slack.post_tweet("시고테스트", date, message, name, _id)
#           time.sleep(5)

#     def on_error(self, status_code):
#         if(status_code == 406):
#           return False
#         print(status_code)
#     def disconnect(self):
#         self.__stream.disconnect()

        
# myStreamListener = MyStreamListener()
# auth = OAuthHandler(config.ckey, config.csecret)
# auth.set_access_token(config.atoken,  config.asecret)
# myStream = Stream(auth, myStreamListener)
# def streamingStart(start, words):
#     if(start):
#       print("start")
#       myStream.filter(track=words, async=True)
#     else:
#       print("end")
#       myStream.disconnect()
#       time.sleep(3)

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
          name = json.loads(data)["user"]["name"] + "(@" + json.loads(data)["user"]["screen_name"] + ")"
          _id = json.loads(data)["id"]
          slack.post_tweet("시고테스트", date, message, name, _id)

    def on_error(self, status_code):
        print(status_code)
        print("error")      
        if(status_code == 406):
          return False
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
