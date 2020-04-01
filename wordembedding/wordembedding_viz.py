import gensim
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

my_model = gensim.models.Word2Vec.load('my_vecs.p')

model_vocab = my_model.wv.vocab

pca = PCA(n_components=2)

my_pca = pca.fit_transform(my_model[model_vocab])

plt.scatter(my_pca[:,0], my_pca[:,1])

for i, word in enumerate(model_vocab):
    plt.annotate(word, xy=(my_pca[i,0], my_pca[i,1]))

plt.show()