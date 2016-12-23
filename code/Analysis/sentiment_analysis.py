# coding: utf-8

import pandas as pd
import gensim
import nltk
import re
import string
from code.anew_module import anew



# read in data set as pandas dataframe

data = pd.read_csv('All_Data.csv', header = 0)
#print data


# Remove punctuation, then tokenize documents

punc = re.compile( '[%s]' % re.escape( string.punctuation ) )
term_vec = []

for d in data['text']:
    d = d.lower()
    d = punc.sub( '', d )
    term_vec.append( nltk.word_tokenize( d ) )

# create stop words list

stop_words = nltk.corpus.stopwords.words( 'english' )


# Remove stop words from term vectors

for i in range( 0, len( term_vec ) ):
    term_list = [ ]

    for term in term_vec[ i ]:
        if term not in stop_words:
            term_list.append( term )

        term_vec[ i ] = term_list



anew.sentiment('security')['arousal']


# Calculate valence and arousal sentiment
arousal = []
valence = []
for vec in term_vec:
    for words in vec:
        arousal_score  = 0
        valence_score = 0

        arousal_score += anew.sentiment(words)['arousal']
        valence_score += anew.sentiment(words)['valence']

    arousal.append(arousal_score)
    valence.append(valence_score)

data['arousal'] = arousal
data['valence'] = valence

data.to_csv("sentiment_x.csv")