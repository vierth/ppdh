import gensim, os, nltk

def filter_words(sentence):
    return [word for word in nltk.word_tokenize(sentence) if word.isalnum()]

def tokenize(text):
    return [filter_words(sentence) for sentence in nltk.sent_tokenize(text.lower())]

ignore = {".DS_Store", ".txt"}

sentences = []

for root, dirs, files in os.walk("fedpapers"):
    for filename in files:
        if filename not in ignore:
            with open(os.path.join(root,filename), 'r', encoding='utf8') as rf:
                # gensim's word2vec model expects sentences that contain words 
                # so we need to do a bit of pre processing. let's write a 
                # tokenization function!
                text = rf.read()
                sentences.extend(tokenize(text))


# create the model and tune it!
word2Vec_model = gensim.models.Word2Vec(
                    sentences, # input sentences
                    sg=1, # use skip grams (0=CBOW). skip grams tend to work better on smaller corpora
                    size=100, # this is how many dimensions the vectors will be
                    min_count=1 # how many times must a word apper
                    )

# we can update the model with train
word2Vec_model.train([["four", "score", "and", "seven", "years", "ago"]], 
                    total_examples=word2Vec_model.corpus_count,
                    epochs=word2Vec_model.epochs)

# Let's save the model to file!
word2Vec_model.save('my_vecs.p')

# let's take a look at some of the methods you can use:
# most similar
print(word2Vec_model.wv.most_similar('government'))

# calculate similarity (cosine similarity)
# distance will calculate euclidean distance
print(word2Vec_model.wv.similarity('government', 'president')) 