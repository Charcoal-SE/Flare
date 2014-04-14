import websocket
import threading
import json,os,sys,getpass,time
import HTMLParser
import nltk

ws = websocket.create_connection("ws://qa.sockets.stackexchange.com/")
ws.send("155-questions-active")

while True:
  a=ws.recv()
  d=json.loads(json.loads(a)["data"])
  h = HTMLParser.HTMLParser()
  title = h.unescape(d["titleEncodedFancy"])
  print title

  tokens = nltk.word_tokenize(title)
  tagged = nltk.pos_tag(tokens)
  print tagged[1][1]
