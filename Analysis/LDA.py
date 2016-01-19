# -*- coding: utf-8 -*-
"""
The MIT License (MIT)

Copyright (c) 2015 Victor Giannakouris - Salalidis

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
__author__ = 'Victor Giannakouris Salalidis'

from gensim import models, corpora, matutils, similarities
import numpy as np
import scipy.stats as stats
import json
import os.path

from Preprocessing.Stemming import Stemmer



class ModelTrainer():
    def __init__(self, input_documets=None, working_dir=None):
        self.input_documents = input_documets


    """
    LDA(Latent Dirichlet Allocation) training
    """
    def train(self, number_of_topics, input_docs=None):
        if input_docs:
            data = input_docs
            if not os.path.isfile(data):
                raise IOError("File '%s' does not exist" % str(data))
        else:
            data = json.load(open(self.input_documents))

        stop_words = json.load(open("Analysis/ModelData/stop-words.json"))


        text_data = [d for d in data.values()]
        tokenized_texts = [[word for word in doc
                            if (word not in stop_words and word != u'κερκυρ')] for doc in text_data]

        self.my_corpus = tokenized_texts



        self.dictionary = corpora.Dictionary(tokenized_texts)
        self.corpus = [self.dictionary.doc2bow(text) for text in tokenized_texts]


        self.model = models.LdaModel(num_topics=number_of_topics,
                                     corpus=self.corpus,
                                     id2word=self.dictionary)

    def update(self, doc):
        final_docs = []
        stemmer = Stemmer()

        tokenized = stemmer.stem(doc.encode('utf-8'))
        tokenized = self.dictionary.doc2bow(tokenized)
        self.model.update([tokenized])
        self.save()
        print self.model.num_terms

    """
    Saves the model and it's
    dictionary for future use
    """
    def save(self):
        self.model.save("Analysis/ModelData/lda")
        self.dictionary.save("Analysis/ModelData/dictionary")

    """
    Returns the set of topics with the
    highest score(distribution) for a
    new, unseen document
    """
    def query(self, text):
        stemmer = Stemmer()
        tokenized = stemmer.stem(text)
        tokenized = self.dictionary.doc2bow(tokenized)
        #tokenized = self.tfidf[tokenized]
        return self.model[tokenized]

    """
    Prints the top-k words describing a topic
    """
    def print_topic(self, topic):
        return self.model.show_topic(topic)

    """
    Loads a saved model and the corresponding dictionary
    """
    def load(self, lda_path, dictionary_path):
        model = models.LdaModel.load(lda_path)
        self.model = model
        self.dictionary = corpora.Dictionary.load(dictionary_path)
