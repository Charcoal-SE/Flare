import threading
import json,os,sys,getpass,time
import HTMLParser
import nltk
import itertools
import mysql.connector

import config #Where we keep our passwords and stuff

cnx = mysql.connector.connect(user=config.MySQLUsername(), password=config.MySQLPassword(), host=config.MySQLHost(), database=config.MySQLDatabase(), buffered=True)
cursor = cnx.cursor()
query = ("SELECT Title, Id FROM " + sys.argv[1] + " LIMIT 100");
cursor.execute(query)

for (Title, Id) in cursor:
	print Title
	tokens = nltk.word_tokenize(Title)
	tagged = nltk.pos_tag(tokens)

	tags = []

	for word in tagged:
		tags.append(word[1])

	tags = sorted(tags)

	print tags

	cmd = "UPDATE " + sys.argv[1] + "SET wordTags='%s' WHERE Id=%s"

	cursor.execute(cmd, (tags, Id, ))

	print cursor.lastrowid

cnx.commit()
sys.exit()

while True:

	tokens = nltk.word_tokenize(title)
	tagged = nltk.pos_tag(tokens)

	tags = []

	for word in tagged:
		tags.append(word[1])

	groupedtags = [list(g) for k, g in itertools.groupby(sorted(tags))]

	tags = ""

	for taggroup in groupedtags:

		description = ""
		if taggroup[0] in code_to_descriptions.keys():
			description = code_to_descriptions[taggroup[0]]
		else:
			description = "unknown";

		print str(len(taggroup)) + " x " + taggroup[0] + " (" + description + ")"

		tags = tags + ','.join(taggroup) + ','

	cmd = "INSERT INTO titles(title, site, url, wordTags) VALUES(%s, %s, %s, %s)"

	cursor.execute(cmd, (title, site, link, tags))
	cnx.commit()

cnx.close()