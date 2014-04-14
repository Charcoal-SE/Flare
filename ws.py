import websocket
import threading
import json,os,sys,getpass,time
import HTMLParser

ws = websocket.create_connection("ws://qa.sockets.stackexchange.com/")
ws.send("155-questions-active")

while True:
  a=ws.recv()
  d=json.loads(json.loads(a)["data"])
  h = HTMLParser.HTMLParser()
  print h.unescape(d["titleEncodedFancy"])