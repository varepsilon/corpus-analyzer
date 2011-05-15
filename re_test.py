#! /usr/bin/env python
# coding=utf-8
import re

string = u'Шла Маша по шоссе и сосала сушку и ещё что-то там делала. А сушка была твёрдой?'
expr = re.compile(u'(?ui)(сушк(?:у|а))|(и)')
matches = expr.findall(string)
for m in matches:
    print m[0], m[1]
