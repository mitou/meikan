# -*- coding: utf-8 -*-
"""
updater.py の中で使われたconvertの例
使い捨てで書き換えて使ってきたので、古いものはサンプル代わりにここに残す。

再利用するものは別途わかりやすい名前を付けて切り出し、--converter=...オプションで指定して使う。
"""

def convert(xs):
    """
    行頭にタグをつけ忘れた問題の修正
    """
    for x in xs:
        x.tags = '\n'.join(u"#未踏採択" + line for line in x.tags.strip('\n').split('\n'))
        print x.tags
        print
    return xs


def convert(xs):
    "採択時所属のデータをアプリに追記"
    import csv
    from collections import defaultdict
    tags = defaultdict(list)
    for items in csv.reader(file('all_mitou_creator_151112_1128cleaned.csv')):
        when = items[2].decode('utf-8')
        when = pretty(when)
        name = items[6].decode('utf-8')
        wheres = items[7].decode('utf-8')
        for where in wheres.split('/'):
            tag = u"#所属#{}#{}時点#".format(where, when)
            add_a_tag(tags[name], tag, 4)

    num_added_tags = 0
    for x in xs:
        if x.name in tags:
            print x.name
            print '\n'.join(tags[x.name])
            x.tags = concat_lines(x.tags, '\n'.join(tags[x.name]))
            num_added_tags += len(tags[x.name])

    print 'add', num_added_tags, 'tags'
    return xs


csv_prefix = '../mitou_meikan/summer_prosym_kanji'
def convert(xs):
    "プロシンおよび情報科学若手の会の過去のデータを基に所属と共著を入力"
    import csv
    from collections import defaultdict
    tags = defaultdict(list)
    for name, affil, when in csv.reader(file(csv_prefix + '_affiliation.csv')):
        name = name.decode('utf-8')
        tags[name].append(
            "所属:{}:{}時点".format(affil, when).decode('utf-8'))
    for name, event, title, when in csv.reader(file(csv_prefix + '_title.csv')):
        name = name.decode('utf-8')
        title = title.replace(':', '：')
        tags[name].append(
            "講演:{}「{}」:{}".format(event, title, when).decode('utf-8'))

    num_updated_people = 0
    num_added_tags = 0
    for x in xs:
        if x.name in tags:
            print x.name
            print '\n'.join(tags[x.name])
            x.tags = concat_lines(x.tags, '\n'.join(tags[x.name]))
            num_updated_people += 1
            num_added_tags += len(tags[x.name])

    print 'update', num_updated_people, 'people,',
    print 'add', num_added_tags, 'tags'
    return xs


def convert(xs):
    """
    デリミタ明記フォーマットをCSVに変換する際に使ったコード
    """
    import unicodecsv as csv
    import cStringIO

    for x in xs:
        f = cStringIO.StringIO()
        tags = []
        for line in x.tags.strip('\n').split('\n'):
            tags.append(line[1:].split(line[0]))
        csv.writer(f, encoding='utf-8').writerows(tags)
        #print x.name
        #print x.tags
        #print
        #print f.getvalue()
        x.tags = f.getvalue()
    return xs
