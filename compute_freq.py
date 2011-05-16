#!/usr/bin/python
#coding=utf-8

import os
import sys
import codecs
import re
import time

#DATA_DIRECTORY = 'tst_data'
DATA_DIRECTORY = 'data_small'
CHUNK_SIZE = 100 * 1024 * 1024  # 100 Mb

SPECIAL_CHARS = re.compile(u'(?u)[\'\"\\«\\»\\.\\,\\:\\!\\?\\-\\—\\;\\(\\)\\n]')
WHITESPACES = re.compile(u'(?u)\\s+')

class StatsItem:
    def __init__(self):
        self.dict = {}
        self.total = 0

def processStreamChuked(stream, regexs, termsList, currentStatsItem):
    chunk = '(empty)'
    currentStatsItem.total = 1
    fileSize = os.path.getsize(stream.name)
    print >>sys.stderr, 'Processing %s...' % (stream.name)
    processedSize = 0
    while chunk:
        # Read integer number of lines in order to avoid problem with
        # decoding from utf-8.
        # CHUNK_SIZE is _approximate_ number of bytes to be read
        chunk = ''.join(stream.readlines(CHUNK_SIZE))
        if not chunk:
            break
        processedSize += len(chunk)
        print >>sys.stderr, '%s: %.2f' % (
            time.asctime(time.localtime()), float(processedSize) / fileSize * 100
        )
        chunk = unicode(chunk, 'utf-8')
        chunk = SPECIAL_CHARS.sub(u' ', chunk)
        for (i, term) in enumerate(termsList):
            currentStatsItem.dict.setdefault(term, 0) # count matches
            for m in regexs[i].finditer(chunk):
                currentStatsItem.dict[term] += 1
        for m in WHITESPACES.finditer(chunk):
            currentStatsItem.total += 1


def processData(dataDir, terms, termsRegexs):
    docs = os.listdir(dataDir)
    byDocsStatistics = {}
    for docName in docs:
        with open(os.path.join(dataDir, docName)) as doc:
            curItem = StatsItem()
            processStreamChuked(doc, termsRegexs, terms, curItem)
            byDocsStatistics[docName] = curItem
    print u'\t'.join(['term'] + docs)
    for term in terms:
        curString = [term]
        for docName in docs:
            curString.append(unicode(float(byDocsStatistics[docName].dict.get(term, 0))
                    / byDocsStatistics[docName].total
            ))
        print u'\t'.join(curString)

def readWordsFile(fname):
    wordRegexs = []
    terms = []
    with open(fname) as f:
        for l in f:
            l = unicode(l.strip(), 'utf-8')
            terms.append(l)
            # do not represent this sub-group in resulting match
            wordRegex = l.replace(u'(', u'(?:')
            # unicode, case-insesitive
            wordRegex = ''.join([u'(?ui)', u'(\\ ', wordRegex, u'\\ )'])
            wordRegexs.append(re.compile(wordRegex))
    return terms, wordRegexs

def main():
    if len(sys.argv) != 2:
        print >>sys.stderr, "Incorrect number of arguments!"\
            "Usage: %s file_with words" % sys.argv[0]
        sys.exit(1)
    terms, termsRegexs = readWordsFile(sys.argv[1])
    processData(DATA_DIRECTORY, terms, termsRegexs)

if __name__ == '__main__':
    main()

