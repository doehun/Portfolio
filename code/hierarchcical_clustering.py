import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import os
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from sklearn.manifold import MDS
from scipy.cluster.hierarchy import ward, dendrogram

filenames = [os.getcwd()+"/hourly/"+filename for filename in os.listdir("hourly/")]
channel_names = [filename.replace(".txt", "") for filename in os.listdir("hourly/")]


vectorizer = CountVectorizer(input='filename')
dtm = vectorizer.fit_transform(filenames)

vocab = vectorizer.get_feature_names()

dtm = dtm.toarray()
vocab = np.array(vocab)

n, m = dtm.shape


dist = 1- cosine_similarity(dtm)


mds = MDS(n_components = 2, dissimilarity = "precomputed", random_state=1)
pos = mds.fit_transform(dist)

xs, ys = pos[:, 0], pos[:, 1]


linkage_matrix = ward(dist)

dendrogram(linkage_matrix, p = 1, orientation='left',
           labels = channel_names)

plt.tight_layout()
plt.show()



