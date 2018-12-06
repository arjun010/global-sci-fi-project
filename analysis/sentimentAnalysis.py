import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import names
import csv
 
def word_feats(words):
    return dict([(word, True) for word in words])
 
positive_vocab = [ 'awesome', 'outstanding', 'fantastic', 'terrific', 'good', 'nice', 'great', ':)' ]
negative_vocab = [ 'bad', 'terrible','useless', 'hate', ':(' ]
neutral_vocab = [ 'movie','the','sound','was','is','actors','did','know','words','not' ]
 
positive_features = [(word_feats(pos), 'pos') for pos in positive_vocab]
negative_features = [(word_feats(neg), 'neg') for neg in negative_vocab]
neutral_features = [(word_feats(neu), 'neu') for neu in neutral_vocab]
 
train_set = negative_features + positive_features + neutral_features
 
classifier = NaiveBayesClassifier.train(train_set) 

reader = csv.reader(open("data.csv",'rb'))
header = reader.next()

# writer = csv.writer(open("temp.csv","wb"))
# writer.writerow(['Title','Pos','Neg'])

idToSentimentMap = {}

for line in reader:
	body = line[header.index('body')]
	title = line[header.index('title')]
	body = body.replace('\n',' ')
	postId = line[header.index('id')]
	# Predict
	neg = 0
	pos = 0
	sentence = body.lower()
	words = sentence.split(' ')
	for word in words:
	    classResult = classifier.classify( word_feats(word))
	    if classResult == 'neg':
	        neg = neg + 1
	    if classResult == 'pos':
	        pos = pos + 1

	idToSentimentMap[postId] = {
		'positive': float(pos)/len(words),
		'negative': float(neg)/len(words)
	}
	# print 'Positive: ' + str(float(pos)/len(words))
	# print 'Negative: ' + str(float(neg)/len(words))
	# writer.writerow([title,str(float(pos)/len(words)),str(float(neg)/len(words))])
	print "======================="

import json
with open('idToSentimentMap.json', 'w') as outfile:
    json.dump(idToSentimentMap, outfile, indent=1)