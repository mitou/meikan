# -*- coding: utf-8 -*-
import unicodecsv as csv
from collections import Counter
count = Counter()
reader = csv.reader(file('interview.csv'), encoding='utf-8')
writer_public = csv.writer(file('public.csv', 'w'), encoding='utf-8')
writer_private = csv.writer(file('private.csv', 'w'), encoding='utf-8')

def is_public(x):
    return (x == u'○')

def write(row, is_pub_col):
    if is_public(row[is_pub_col]):
        writer_public.writerow([name, section] + row)
    else:
        writer_private.writerow([name, section] + row)

for items in reader:
    if items[0].startswith('# '):
        name = items[0][2:]
        continue
    if items[0].startswith('## '):
        section = items[0][3:]
        continue
    if section == u"履歴書的経歴" and items[0] == u"受賞歴":
        section = u"受賞歴"
        continue
    if section == u"受賞歴" and items[0] == u"年":
        continue  # skip header

    if section == u"公開WEB情報":
        if not items[1]: continue
        count.update([items[2]])
        write(items, 2)

    if section == u"履歴書的経歴":
        count.update([items[7]])
        write(items, 7)

    if section == u"人物像":
        count.update([items[2]])
        write(items, 2)

    if section == u"創造的経歴":
        count.update([items[2]])
        write(items, 2)


for k in count:
    print k, count[k]
