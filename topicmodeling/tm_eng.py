'''
This script will run a topic model for us
'''

import gensim, nltk, os

# create an object that filters files I want to ignore
ignore_files = {'.DS_Store', '.txt'}

# contains input corpus
texts = []
labels = []

# iterate through all files in the corpus folder
for root, dirs, files in os.walk('fedpapers'):
    for file_name in files:
        if file_name not in ignore_files:
            with open(os.path.join(root, file_name),encoding='utf8') as rf:
                text = rf.read()
                # here I need to switch my tokenization methodology.
                tokens = nltk.word_tokenize(text)
                cleaned = [word for word in tokens if word.isalnum()]
                texts.append(cleaned)
                labels.append(file_name[:-4])

# transform the corpus to run in gensim
corpus_dictionary = gensim.corpora.Dictionary(texts)
corpus_dictionary.filter_extremes(no_below=5)
# transform corpus text list into list of bags of words
processed_corpus = [corpus_dictionary.doc2bow(text) for text in texts]

# number of topics
number_of_topics = 10

# specify where mallet lives
mallet_path = 'C:\\mallet\\bin\\mallet'

# create the mallet modeling object
lda_model = gensim.models.wrappers.ldamallet.LdaMallet(
    mallet_path,
    corpus=processed_corpus,
    id2word=corpus_dictionary,
    num_topics=number_of_topics,
    optimize_interval=10,
    prefix='fed_'
)

# save the model object to file for reuse later
# uses pickle to save the file
lda_model.save("topicmodel.p")

# we can now reconstitute the mode with load
# lda_model = gensim.utils.SaveLoad.load('topicmodel.p')

topics = lda_model.show_topics(num_topics=number_of_topics, num_words=20)

for topic in topics:
    print(f"Topic #{topic[0]}: {topic[1]}...\n\n")











