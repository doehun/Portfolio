
# coding: utf-8

# In[2]:

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import os

# In[3]:

filenames = [os.getcwd()+"/txt_data/"+filename for filename in os.listdir("txt_data")]
vectorizer = CountVectorizer(input = 'filename', stop_words = 'english', min_df=1)
dtm = vectorizer.fit_transform(filenames)   #document term matrix in sparse matrix form
vocab = vectorizer.get_feature_names()      #vocab list


# In[119]:

dtm = dtm.toarray()  #document term matrix into numpy arrays


# In[120]:

vocab = np.array(vocab)


# In[121]:

john_idx = list(vocab).index('john') #index where john is
#for i in range(len(dtm)):  #how many johns each document contain
#    print dtm[i, john_idx]
#dtm[0, vocab == 'john']


# In[1]:

n, _ = dtm.shape
dist = np.zeros((n,n))
for i in range(n):
    for j in range(n):
        x, y = dtm[i, :], dtm[j,:]
        dist[i, j] = np.sqrt(np.sum(x-y)**2)
print dist


# In[124]:

from sklearn.metrics.pairwise import euclidean_distances

dist = euclidean_distances(dtm)
np.round(dist,1)


# In[125]:

from sklearn.metrics.pairwise import cosine_similarity

dist = 1 - cosine_similarity(dtm)
np.round(dist, 2)


# In[126]:

import matplotlib.pyplot as plt
from sklearn.manifold import MDS
get_ipython().magic(u'matplotlib inline')
mds = MDS(n_components = 2, dissimilarity = "precomputed", random_state = 1)
pos = mds.fit_transform(dist)  #share (n_components, n_samples)


# In[127]:

xs, ys = pos[:, 0], pos[:,1]
names = [os.path.basename(fn).replace('.txt', '') for fn in filenames]
plt.figure(figsize=(20,10))
for x, y, name in zip(xs, ys, names):
    plt.scatter(x, y)
    plt.text(x,y,name)


# In[128]:

mds = MDS(n_components = 3, dissimilarity = "precomputed", random_state = 1)
pos = mds.fit_transform(dist)


# In[129]:

from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure(figsize = (20, 10))
ax = fig.add_subplot(111, projection = '3d')
ax.scatter(pos[:,0], pos[:,1], pos[:,2])
for x, y, z, s in zip(pos[:,0], pos[:,1], pos[:,2], names):
    ax.text(x,y,z,s)
plt.show()


# In[130]:

from scipy.cluster.hierarchy import ward, dendrogram
linkage_matrix = ward(dist)

plt.figure(figsize=(10,20))
dendrogram(linkage_matrix, orientation = "right", labels = names)
plt.tight_layout()
plt.show()


# In[ ]:



