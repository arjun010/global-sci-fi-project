from __future__ import unicode_literals
import spacy
spacy.load('en')
from spacy.lang.en import English
parser = English()
def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens

import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet as wn
def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma
    
from nltk.stem.wordnet import WordNetLemmatizer
def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)

nltk.download('stopwords')
en_stop = set(nltk.corpus.stopwords.words('english'))

def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens

import csv
text_data = []
reader = csv.reader(open('data.csv','rb'))
header = reader.next()
for line in reader:
    body = line[0].replace('\n',' ')
    tokens = prepare_text_for_lda(body)
    text_data.append(tokens)

# print text_data
# print len(text_data)

from gensim import corpora
import gensim
dictionary = corpora.Dictionary(text_data)


topicsList = []

for text in text_data:
    corpus = [dictionary.doc2bow(text)]
    NUM_TOPICS = 5
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
    ldamodel.save('model5.gensim')
    # topics = ldamodel.print_topics(num_words=8)
    lda_result = ldamodel.show_topics(num_topics=12, num_words=5,formatted=False)
    topics_words = [(tp[0], [wd[0] for wd in tp[1]]) for tp in lda_result]
    curPostTopics = []
    for topic,words in topics_words:
        # print ", ".join(words)
        for word in words:
            if word not in curPostTopics:
                curPostTopics.append(word)

    topicsList.append(curPostTopics)
    print "=========="

reader = csv.reader(open("data.csv",'rb'))
header = reader.next()
idToTopicsMap = {}

idx = 0

for line in reader:
    postId = line[header.index('id')]
    idToTopicsMap[postId] = topicsList[idx]
    idx += 1

import json
with open('idToTopicsMap.json', 'w') as outfile:
    json.dump(idToTopicsMap, outfile, indent=1)

# corpus = [dictionary.doc2bow(text) for text in text_data]
# import pickle
# pickle.dump(corpus, open('corpus.pkl', 'wb'))
# dictionary.save('dictionary.gensim')


# NUM_TOPICS = 5
# ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
# ldamodel.save('model5.gensim')
# topics = ldamodel.print_topics(num_words=8)
# for topic in topics:
#     print(topic)