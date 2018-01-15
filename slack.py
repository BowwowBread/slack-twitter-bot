# -*- coding: utf8 -*-

from slacker import Slacker
import config 
import websockets
import json
import re
import streaming
import asyncio

print(config.slack_token)
slack = Slacker(config.slack_token)

async def execute_bot(sock_endpoint):
    ws = await websockets.connect(sock_endpoint)
    while True:
        message_json = json.loads(await ws.recv())
        if(message_json["type"] == "message"):
          if("bot_id" in message_json):
            print("bot")
          else:
            text = message_json["text"]
            if(text.split()[0] == "시고"):  
              if(text.split()[1] == "검색어"):
                post_message("시고테스트", "검색 시작")                      
                streaming.streamingStart(False, None)                                
                targetWords = text[6:].replace('[', '').replace(']', '').strip().split(',')
                streaming.streamingStart(True, targetWords)
              elif(text.split()[1] == "중지"):
                post_message("시고테스트", "검색 종료")                            
                streaming.streamingStart(False, None)                
def rtmStart():
  response = slack.rtm.start()
  sock_endpoint = response.body['url']
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  asyncio.get_event_loop().run_until_complete(execute_bot(sock_endpoint))
  asyncio.get_event_loop().run_forever()

def post_message(channel, message):
  slack.chat.post_message(channel="#"+channel, text=message, as_user=True)
  
def post_tweet(channel, date, message, name, username, _id):
  print("post")
  attachments_dict = dict()
  attachments_dict['title'] = name + " - " + date
  attachments_dict['title_link'] = "https://twitter.com/"+username+"/status/"+str(_id)
  attachments_dict['text'] = message
  attachments_dict['mrkdwn_in'] = ["text", "pretext"]
  attachments = [attachments_dict]
  slack.chat.post_message(channel="#"+channel, text=None, attachments=attachments, as_user=True)
  