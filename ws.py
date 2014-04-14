import websocket
import threading
import json,os,sys,getpass,time
import HTMLParser
import nltk
import itertools

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

  tags = []

  for word in tagged:
	tags.append(word[1])

  groupedtags = [list(g) for k, g in itertools.groupby(sorted(tags))]

  for taggroup in groupedtags:
  	print str(len(taggroup)) + " x " + taggroup[0]
