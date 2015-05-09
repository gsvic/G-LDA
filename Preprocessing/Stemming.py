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
__author__ = 'gsvic'

import json
import ast
from requests  import request

url = "http://localhost:9200/greek_stemmer/_analyze?analyzer=greek&pretty=true"

"""
Greek text stemming using elasticsearch-skroutz-greek-stemmer
URL: https://github.com/skroutz/elasticsearch-skroutz-greekstemmer
"""

class Stemmer():
    def stem(self, data):
        r = request(method="XGET", url=url, **{'data': data})
        data = ast.literal_eval(r.text)
        tokens = [token['token'] for token in data['tokens']]
        return tokens

    def prepareInput(self, input_json, output_json):
        data = json.load(open(input_json))
        text_data = [d['6'] for d in data]
        cleaned = dict()
        for i, text in enumerate(text_data):
            try:
                cleaned[i] = self.stem(text.encode('utf-8'))
            except Exception as e:
                print e.message, e.args
            print "Finished %d/%d"%(i, len(text_data))

        with open(output_json, "w+") as out_file:
            json.dump(cleaned, out_file)
