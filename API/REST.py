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

from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from Analysis.LDA import ModelTrainer
import os


cwd = os.getcwd()
app = Flask(__name__)
api = Api(app)

global model
model = ModelTrainer()
model.load(dictionary_path=cwd+"/Analysis/ModelData/dictionary",
           lda_path=cwd+"/Analysis/ModelData/lda")

"""
                                Documentation

    Parameters
    - text: The input text
    - print_topics: If set true, the api returns the list of the
                    top-k words describing the topic

    Example: http://api-url/classifier?text="Your input text"&print_topics=true
"""

class Classifier(Resource):
    """
                                Dictionary Explanation

        -topic: The topic's id (Integer)
        -words: The list of the words describing the topic(List)
        -score: The probability distribution of the input text for the resulting topic(Float)

    """

    def get(self):
        text = request.args.get('text')
        print_topics = (request.args.get('print_topics') == "true")

        if not text:
            return
        topics = model.query(text.encode('utf-8'))

        view = []
        for t in topics:
            if print_topics:
                view.append({'topic': t[0],
                             'words': model.print_topic(int(t[0])),
                             'score': t[1]})
            else:
                view.append({'topic': t[0],
                             'score': t[1]})
        return {"result": view}

class Tools(Resource):
    def get(self):
        topic =  request.args.get('print_topic')
        if not topic:
            return

        return model.print_topic(int(topic))

    def post(self):
        doc = request.args.get('doc')
        if doc:
            model.update(doc)
            return "Done!"

def startRest():
    api.add_resource(Classifier, '/classifier')
    api.add_resource(Tools, '/tools')
    app.run(debug=True, host="localhost")
