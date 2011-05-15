#!/usr/bin/python
#coding=utf-8

import os
import sys
import codecs
import re

DATA_DIRECTORY = 'data'
CHUNK_SIZE = 100 * 1024 * 1024  # 100 Mb

SPECIAL_CHARS = re.compile(u'(?u)[\'\"\\«\\»\\.\\,\\:\\!\\?\\-\\—\\;\\(\\)\\n]')
WHITESPACES = re.compile(u'(?u)\\s+')

class StatsItem:
    def __init__(self):
        self.dict = {}
        self.total = 0

def processStreamChuked(stream, regex, termsList, currentStatsItem):
    chunk = '(empty)'
    currentStatsItem.total = 1
    fileSize = os.path.getsize(stream.name)
    print >>sys.stderr, 'Processing %s...' % (stream.name)
    processedSize = 0
    while chunk:
        chunk = ''.join(stream.readlines(CHUNK_SIZE))
        if not chunk:
            break
        processedSize += len(chunk)
        print >>sys.stderr, '%.2f' % (float(processedSize) / fileSize * 100)
        chunk = unicode(chunk, 'utf-8')
        chunk = SPECIAL_CHARS.sub(u' ', chunk)
        for m in regex.finditer(chunk):
            for idx, term in enumerate(termsList):
                currentStatsItem.dict.setdefault(term, 0)
                if m.groups()[idx]:
                    currentStatsItem.dict[term] += 1
        for m in WHITESPACES.finditer(chunk):
            currentStatsItem.total += 1


def processData(dataDir, terms, termsRegex):
    docs = os.listdir(dataDir)
    byDocsStatistics = {}
    for docName in docs:
        with open(os.path.join(dataDir, docName)) as doc:
            curItem = StatsItem()
            processStreamChuked(doc, termsRegex, terms, curItem)
            byDocsStatistics[docName] = curItem
    print '\t'.join(['term'] + docs)
    for term in terms:
        curString = [term]
        for docName in docs:
            curString.append(str(float(byDocsStatistics[docName].dict.get(term, 0))
                    / byDocsStatistics[docName].total
            ))
        print '\t'.join(curString)

def readWordsFile(fname):
    bigRegexRaw = u'(?ui)' # unicode, case-insensitive
    wordRegexs = []
    terms = []
    with open(fname) as f:
        for l in f:
            l = unicode(l.strip(), 'utf-8')
            terms.append(l)
            # do not represent this sub-group in resulting match
            wordRegex = l.replace('(', '(?:')
            wordRegexs.append(u'(\\ %s\\ )' % wordRegex)
    bigRegexRaw += u'|'.join(wordRegexs)
    return terms, re.compile(bigRegexRaw)

def main():
    if len(sys.argv) != 2:
        print >>sys.stderr, "Incorrect number of arguments!"\
            "Usage: %s file_with words" % sys.argv[0]
        sys.exit(1)
    terms, termsRegex = readWordsFile(sys.argv[1])
    processData(DATA_DIRECTORY, terms, termsRegex)

if __name__ == '__main__':
    main()

