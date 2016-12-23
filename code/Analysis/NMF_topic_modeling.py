
# coding: utf-8


import os
import numpy as np
import sklearn.feature_extraction.text as text


filenames = [os.getcwd()+"/hourly/"+filename for filename in os.listdir("hourly/")]
channel_names = [filename.replace(".txt", "") for filename in os.listdir("hourly/")]
print "channel names: ", channel_names

vectorizer = text.CountVectorizer(input = 'filename', stop_words = 'english', min_df = 2)
dtm = vectorizer.fit_transform(filenames).toarray()
vocab = np.array(vectorizer.get_feature_names())
print "vocab: ", vocab


from sklearn import decomposition
num_topics = 8
num_top_words = 40
clf = decomposition.NMF(n_components = num_topics, random_state = 1)


doctopic = clf.fit_transform(dtm)


topic_words = []
for topic in clf.components_:
    word_idx = np.argsort(topic)[::-1][0:num_top_words]
    topic_words.append([vocab[i] for i in word_idx])



doctopic = doctopic / np.sum(doctopic, axis = 1, keepdims = True)


channel_names = np.asarray(channel_names)
doctopic_orig = doctopic.copy()
num_groups = len(set(channel_names))
doctopic_grouped = np.zeros((num_groups, num_topics))
for i, name in enumerate(sorted(set(channel_names))):
    doctopic_grouped[i, :] = np.mean(doctopic[channel_names == name, :], axis = 0)



doctopic = doctopic_grouped


for i in range(len(doctopic)):
    top_topics = np.argsort(doctopic[i,:])[::-1][0:3]
    top_topics_str = ' '.join(str(t) for t in top_topics)
    print "{}: {}".format(channel_names[i], top_topics_str)


for t in range(len(topic_words)):
    print "Topic {}: {}".format(t, ' '.join(topic_words[t][:15]))


