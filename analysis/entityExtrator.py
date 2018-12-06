from __future__ import unicode_literals
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
from pprint import pprint
import csv

nlp = en_core_web_sm.load()


reader = csv.reader(open("data.csv",'rb'))
header = reader.next()

idToEntityMap = {}

for line in reader:
	body = line[header.index('body')]
	body = body.replace('\n',' ')
	postId = line[header.index('id')]
	doc = nlp(body)
	idToEntityMap[postId] = {}
	for X in doc.ents:
		# print X.text, X.label_
		if X.label_ in ['NORP','ORDINAL']:
			continue
		if X.label_ in idToEntityMap[postId]:
			if X.text not in idToEntityMap[postId][X.label_]['values']:
				idToEntityMap[postId][X.label_]['count'] += 1
				idToEntityMap[postId][X.label_]['values'].append(X.text)
		else:
			idToEntityMap[postId][X.label_] = {
				'count' : 1,
				'values' : [X.text]
			}
	# pprint([(X.text, X.label_) for X in doc.ents])
	print "=============="

import json
with open('idToEntityMap.json', 'w') as outfile:
    json.dump(idToEntityMap, outfile, indent=1)

# doc = nlp('European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices')