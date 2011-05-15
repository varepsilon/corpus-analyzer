#!/usr/bin/python
#coding=utf-8

import os
import sys
import codecs
import re

dataDir = 'data'

def printTF(terms, tf):
    for term in terms:
        print term,
        if not tf.has_key(term):
            print
            continue
        freqs = tf[term]
        for corp, freq in freqs.items():
            print corp, freq,
        print

def handle_terms(terms):
    tf = {}
    totals = {}
    docs = os.listdir(dataDir)
    for doc_name in docs:
        with open(os.path.join(dataDir, doc_name)) as doc:
            for line in doc:
                line = unicode(line, "utf-8")
                for term in terms:
                    if term != "" and line.find(" " + term) != -1:
                        if not tf.has_key(term):
                            tf[term] = {}
                        if tf[term].has_key(doc_name):
                            tf[term][doc_name] += 1
                        else:
                            tf[term][doc_name] = 1
    return tf

def main():
    if len(sys.argv) != 2:
        print >>sys.stderr, "Incorrect number of arguments!"\
            "Usage: %s file_with words" % sys.argv[0]
    with open(sys.argv[1]) as f:
        terms = map(lambda x : unicode(x, "utf-8").strip(), f)
    tf = handle_terms(terms)
    printTF(terms, tf)

if __name__ == '__main__':
    main()

