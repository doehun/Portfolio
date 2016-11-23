import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import nltk

import re

df = pd.read_csv("concatenated.csv", header = 0)
#print df.head(10)


def clean_words(text, remove_stopwords = False):
    text = re.sub("[^a-zA-Z]", " ", text)
    words = text.lower().split()
    if remove_stopwords:
        stops = set(stopwords.words('english'))
        words = [w for w in words if not w in stops]
    return words

def clean_sentences(text, tokenizer, remove_stopwords = False):
    raw_sentences = tokenizer.tokenize(text.decode('utf8').strip())

    # 2. Loop over each sentence
    sentences = []
    for raw_sentence in raw_sentences:
        # If a sentence is empty, skip it
        if len(raw_sentence) > 0:
            # Otherwise, call review_to_wordlist to get a list of words
            sentences.append( clean_words( raw_sentence, \
              remove_stopwords ))
    #
    # Return the list of sentences (each sentence is a list of words,
    # so this returns a list of lists
    return sentences



clean_train_reviews = []
for i in xrange(0, len(df['text'])):
    clean_train_reviews.append(" ".join(clean_words(df['text'][i], True)))

vectorizer = CountVectorizer(analyzer = "word",
                             tokenizer = None,
                             preprocessor= None,
                             stop_words = None,
                             max_features=5000)

train_data_features = vectorizer.fit_transform(clean_train_reviews)
train_data_features = train_data_features.toarray()


print sum(train_data_features)
print sum(sum(train_data_features))