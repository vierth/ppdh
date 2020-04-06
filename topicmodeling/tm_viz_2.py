'''
Vizualize the topic weights within a given document
'''

import matplotlib.pyplot as plt

import os

doc_to_viz = "1_Hamilton"

# create a set of ignore files
ignore = {".DS_Store", ".txt"}

# a list for the labels
titles = []

for root, dirs, files in os.walk("fedpapers"):
    for filename in files:
        titles.append(filename[:-4])

with open('fed_doctopics.txt','r', encoding='utf8') as rf:
    topic_info = rf.read().split("\n")
    topic_info = [item for item in topic_info if item != ""]

doc_topic_info = {}

for title, line in zip(titles, topic_info):
    info = line.split("\t")

    doc_topic_info[title] = [float(weight) for weight in info[2:]]

weights = doc_topic_info[doc_to_viz]

index = [i for i in range(len(weights))]

labels = [f"Topic {i + 1}" for i in range(len(weights))]

plt.bar(index, weights)
plt.xticks(index, labels, rotation=90)
plt.xlabel("Topic")
plt.ylabel("Weight")
plt.title(doc_to_viz)

plt.tight_layout()
plt.show()