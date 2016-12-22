import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import sys
import codecs
import os

def get_document_filenames(document_path = '/User/doehun/Portfolio/'):
    return [os.path.join(document_path, each) for each in os.listdir(document_path)]

def create_vectorizer():
    return TfidfVectorizer(input = 'content', max_features = 200, stop_words = 'english',
                         encoding = 'utf-8', ngram_range = (2,2))

def display_scores(vectorizer, tfidf_result, top_n):
    scores = zip(vectorizer.get_feature_names(),
                np.asarray(tfidf_result.sum(axis=0)).ravel())

    sorted_scores = sorted(scores, key = lambda x: x[1], reverse = True)

    for item in sorted_scores[:top_n]:
        print "{0:20} Score: {1}".format(item[0], item[1])

def main():
    vectorizer = create_vectorizer()
    data = pd.read_csv("concatenated.csv")
    top_n = 10

    channel_groups = data.groupby('channel')['text']

    for channel, text in channel_groups:
        tfidf_result = vectorizer.fit_transform(text.values.astype('U'))

        print channel
        display_scores(vectorizer, tfidf_result, top_n)
        print ""

if __name__ == '__main__':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    main()