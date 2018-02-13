# -*- coding: utf8 -*-

from slacker import Slacker
import config 
import websockets
import json
import re
import streaming
import asyncio

targetWords = []

print(config.slack_token)
slack = Slacker(config.slack_token)

async def execute_bot(sock_endpoint):
    global targetWords
    ws = await websockets.connect(sock_endpoint)
    while True:
        try:
          message_json = json.loads(await ws.recv())
          if(message_json["type"] == "message"):
            if("bot_id" in message_json):
              print("bot")
            else:
              text = message_json["text"]
              if(text.split()[0] == "시고"):  
                if(text.split()[1] == "검색어"):
                  targetWords = []
                  targetWord = ""
                  post_message("시고테스트", "검색 시작")                      
                  streaming.streamingStart(False, None)                                 
                  targetWords = text[6:].replace('[', '').replace(']', '').strip().replace(" ", "").split(',')
                  print(targetWords)
                  streaming.streamingStart(True, targetWords)
                elif(text.split()[1] == "중지"):
                  post_message("시고테스트", "검색 종료")                            
                  streaming.streamingStart(False, None)                
        except:
          post_message("시고테스트", "다시 입력해주세요.")
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
  message = find_match_word(message)
  print(message)
  attachments_dict = dict()
  attachments_dict['title'] = name + " - " + date
  attachments_dict['title_link'] = "https://twitter.com/"+username+"/status/"+str(_id)
  attachments_dict['text'] = message
  attachments_dict['mrkdwn_in'] = ["text", "pretext"]
  attachments_dict['color'] = 'good'
  attachments = [attachments_dict]
  slack.chat.post_message(channel="#"+channel, text=None, attachments=attachments, as_user=True)

def find_match_word(message):
  print(targetWords)
  for word in targetWords:
    message = message.replace(word, "*"+word+"*")
  return message

  