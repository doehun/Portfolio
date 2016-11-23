from sklearn.feature_extraction.text import TfidfVectorizer
import os
import numpy as np

import pandas as pd


filenames = [os.getcwd()+"/txt_files/"+filename for filename in os.listdir("txt_files/")]
channel_names = [filename.replace(".txt", "") for filename in os.listdir("txt_files/")]
print "channel names: ", channel_names



tfidf = TfidfVectorizer(input = 'filename', stop_words='english', min_df=2)
dtm = tfidf.fit_transform(filenames).toarray()
vocab = np.array(tfidf.get_feature_names())
print "vocab: ", vocab
for v in vocab:
    print v



from sklearn.cluster import KMeans

num_clusters = 12
km = KMeans(n_clusters = num_clusters)

km.fit(dtm)
clusters = km.labels_.tolist()

print clusters

clusters = pd.DataFrame({'channel_names' : channel_names, 'clusters': clusters})
clusters.to_csv("12clusters.csv")
