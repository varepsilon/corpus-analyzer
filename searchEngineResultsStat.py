#! /usr/bin/env python
# coding=utf-8

import sys
import urllib
import re
import urlparse
import time

REQUEST_TYPES = {
    'consultant': u'http://xmlsearch.yandex.ru/xmlsearch?text=site%%3Aconsultant.ru+%s',
    'habr': u'http://xmlsearch.yandex.ru/xmlsearch?text=site%%3Ahabrahabr.ru+%s',
    'women':u'http://xmlsearch.yandex.ru/xmlsearch?text=%s&holdreq=женский+журнал+онлайн',
    'ngram': None,
    'yandex': u'http://xmlsearch.yandex.ru/xmlsearch?text=%s',
    'slovari': u'http://slovari.yandex.ru/%s/',
    'blogs': u'http://blogs.yandex.ru/search.xml?ft=blog&text=%s',
}

def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)

def iriToUri(iri):
    parts= urlparse.urlparse(iri)
    return urlparse.urlunparse(
        part.encode('idna') if parti==1 else urlEncodeNonAscii(part.encode('utf-8'))
        for parti, part in enumerate(parts)
    )

def ParseYandex(page):
    found = page.split('<found priority="all">', 1)
    if len(found) != 2:
        return 0
    else:
        found = found[-1].split('</found>')[0]
    return int(found)

def GetResult(text, queryType):
    if not REQUEST_TYPES[queryType]:
        return None
    fullUrl = iriToUri(REQUEST_TYPES[queryType] % text)
    doc = urllib.urlopen(fullUrl).read()
    return ParseYandex(doc)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print >>sys.stderr, "Usage: %s file_with_words_to_examine" % sys.argv[0]
        sys.exit(1)
    terms = []
    with open(sys.argv[1]) as f:
        for line in f:
            terms.append(unicode(line.strip(), 'utf-8'))
    usedTypes = ['consultant', 'habr', 'women', 'yandex']
    print '\t'.join(['term'] + usedTypes)
    for term in terms:
        resultString = [term.encode('utf-8')]
        for t in usedTypes:
            resultString.append(str(GetResult(term, t)))
            time.sleep(1)
        print '\t'.join(resultString)

