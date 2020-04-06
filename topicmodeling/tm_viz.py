'''
This script visualizes the output of our topic model
'''

import matplotlib.pyplot as plt

with open('fed_topickeys.txt') as rf:
    topic_info = rf.read().split("\n")

topic_info = [item for item in topic_info if item != ""]

topics = {}

for line in topic_info:
    data = line.split("\t")

    # topic number
    topic_num = data[0]

    # get topic weight
    topic_weight = float(data[1])

    # get the words in the topic
    topic_words = data[2].split(" ")

    # save the information to the topics dictionary
    topics[topic_num] = [topic_weight, topic_words]

# let's visualize all this information as a barchart
index = [i for i in range(len(topics))]

# get the weight of each topic
weights = [topics[str(i)][0] for i in range(len(topics))]

# create labels for each bar
labels = [f"Topic {i + 1}" for i in range(len(topics))]

# visualize the results
plt.bar(index, weights)

# add some labels
plt.xticks(index, labels, rotation=90)
plt.xlabel("Topic")
plt.ylabel("Weight")
plt.title("Corpus Topic Weights")
plt.tight_layout()
plt.show()