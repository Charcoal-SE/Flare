import websocket
import threading
import json,os,sys,getpass,time
import HTMLParser
import nltk
import itertools
import mysql.connector

import config #Where we keep our passwords and stuff

cnx = mysql.connector.connect(user=config.MySQLUsername(), password=config.MySQLPassword(), host=config.MySQLHost(), database=config.MySQLDatabase())
cursor = cnx.cursor()

ws = websocket.create_connection("ws://qa.sockets.stackexchange.com/")
ws.send("155-questions-active")

h = HTMLParser.HTMLParser()

code_to_descriptions = {"CC" : "Coordinating conjunction", "CD" : "Cardinal number", "DT" : "Determiner", "EX" : "Existential there", "FW" : "Foreign word", "IN" : "Preposition or subordinating conjunction", "JJ" : "Adjective", "JJR" : "Comparative adjective", "JJS" : "Superlative adjective", "LS" : "List item marker", "MD" : "Modal", "NN" : "Singular or mass noun", "NNS" : "Plural noun", "NNP" : "Singular proper noun", "NNPS" : "Plural proper noun", "PDT" : "Predeterminer", "POS" : "Possessive ending", "PRP" : "Personal pronoun", "PRP$" : "Possessive pronoun", "RB" : "Adverb", "RBR" : "Comparative adverb", "RBS" : "Superlative adverb", "RP" : "Particle", "SYM" : "Symbol", "TO" : "to", "UH" : "Interjection", "VB" : "Base form Verb", "VBD" : "Past tense verb", "VBG" : "Gerund or present participle verb", "VBN" : "Past participle verb", "VBP" : "Non-3rd person singular present verb", "VBZ" : "3rd person singular present verb", "WDT" : "Wh-determiner", "WP" : "Wh-pronoun", "WP$" : "Possessive wh-pronoun", "WRB" : "Wh-adverb", "." : "Punctuation", "," : "Punctuation"}

while True:
	a=ws.recv()
	d=json.loads(json.loads(a)["data"])
	title = h.unescape(d["titleEncodedFancy"])

	cmd = "INSERT INTO titles(title) VALUES(%s)"

	cursor.execute(cmd, (title, ))
	cnx.commit()

	print(title)

	tokens = nltk.word_tokenize(title)
	tagged = nltk.pos_tag(tokens)

	tags = []

	for word in tagged:
	tags.append(word[1])

	groupedtags = [list(g) for k, g in itertools.groupby(sorted(tags))]

	for taggroup in groupedtags:

		description = ""
		if taggroup[0] in code_to_descriptions.keys():
			description = code_to_descriptions[taggroup[0]]
		else:
			description = "unknown";

		print str(len(taggroup)) + " x " + taggroup[0] + " (" + description + ")"
