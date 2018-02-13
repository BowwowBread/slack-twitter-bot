# -*- coding: utf8 -*-

import streaming
import slack

if __name__ == '__main__' :
  try:
    slack.rtmStart()
  except:
    print("except err")
    

