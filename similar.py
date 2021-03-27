import json

import gensim
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

def retrieve_ontology():
    filepath = "sortedDOS.json"
    with open(filepath) as fp:
        ontologyData = json.load(fp)
    return ontologyData #ontology JSON containing keywords

def write_to_json(data):
    filename = "groupedDOS.json"
    with open(filename, "w", encoding = "utf-8") as file:
        json.dump(data, file, indent = 4)


ontologyData = retrieve_ontology()
newData = {}
newData["diseases"] = []

for disease in ontologyData["diseases"]:
    file_docs = []
    seen = []
    name = disease["name"]
    print(name)
    keywords = disease["keywords"]

    if len(keywords) == 0:
        newData["diseases"].append({
            "name": name,
            "keywords": []
        })

    else: 
        for keyword in keywords:
            file_docs.append(keyword.lower())
            seen.append(False)




        gen_docs = [[w.lower() for w in word_tokenize(text)] 
                    for text in file_docs]

        dictionary = gensim.corpora.Dictionary(gen_docs)
        corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
        tf_idf = gensim.models.TfidfModel(corpus)

        # building the index
        sims = gensim.similarities.Similarity('Desktop', tf_idf[corpus], num_features = len(dictionary))

        for line in file_docs:
            query_doc = [w.lower() for w in word_tokenize(line)]
            query_doc_bow = dictionary.doc2bow(query_doc) #update an existing dictionary and create bag of words

        # perform a similarity query against the corpus
        query_doc_tf_idf = tf_idf[query_doc_bow]

        # for line in query documents
        index = 0
        keywordData = []
        for keyword in file_docs:
            if seen[index] == False:
                keywords = [keyword]
                seen[index] = True
                # tokenize words
                query_doc = [w.lower() for w in word_tokenize(keyword)]
                # create bag of words
                query_doc_bow = dictionary.doc2bow(query_doc)
                # find similarity for each document
                query_doc_tf_idf = tf_idf[query_doc_bow]

                for match_percent in sims[query_doc_tf_idf]:
                    if match_percent > 0.25:
                        index_match = list(sims[query_doc_tf_idf]).index(match_percent)
                        if index_match != index:
                            if seen[index_match] == False:
                                seen[index_match] = True
                                keywords.append(file_docs[index_match])
                keywordData.append({
                    "group ID": str(index),
                    "keywords": keywords
                })
            index += 1

        newData["diseases"].append({
            "name": name,
            "data": keywordData
        })

write_to_json(newData)












