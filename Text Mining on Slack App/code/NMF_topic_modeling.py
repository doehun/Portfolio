
# coding: utf-8

# In[1]:

import os
import numpy as np
import sklearn.feature_extraction.text as text


# In[20]:

filenames = [os.getcwd()+"/hourly/"+filename for filename in os.listdir("hourly/")]
channel_names = [filename.replace(".txt", "") for filename in os.listdir("hourly/")]
print "channel names: ", channel_names

vectorizer = text.CountVectorizer(input = 'filename', stop_words = 'english', min_df = 2)
dtm = vectorizer.fit_transform(filenames).toarray()
vocab = np.array(vectorizer.get_feature_names())
print "vocab: ", vocab

# In[9]:

from sklearn import decomposition
num_topics = 8
num_top_words = 40
clf = decomposition.NMF(n_components = num_topics, random_state = 1)
#clf = decomposition.LatentDirichletAllocation(n_topics=num_topics)


# In[10]:

doctopic = clf.fit_transform(dtm)


# In[11]:

topic_words = []
for topic in clf.components_:
    word_idx = np.argsort(topic)[::-1][0:num_top_words]
    topic_words.append([vocab[i] for i in word_idx])


# In[12]:

doctopic = doctopic / np.sum(doctopic, axis = 1, keepdims = True)


# In[25]:

channel_names = np.asarray(channel_names)
doctopic_orig = doctopic.copy()
num_groups = len(set(channel_names))
doctopic_grouped = np.zeros((num_groups, num_topics))
for i, name in enumerate(sorted(set(channel_names))):
    doctopic_grouped[i, :] = np.mean(doctopic[channel_names == name, :], axis = 0)


# In[27]:

doctopic = doctopic_grouped


# In[31]:

for i in range(len(doctopic)):
    top_topics = np.argsort(doctopic[i,:])[::-1][0:3]
    top_topics_str = ' '.join(str(t) for t in top_topics)
    print "{}: {}".format(channel_names[i], top_topics_str)


# In[28]:

for t in range(len(topic_words)):
    print "Topic {}: {}".format(t, ' '.join(topic_words[t][:15]))




# In[ ]:



#tfidfvectorizer