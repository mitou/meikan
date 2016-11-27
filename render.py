# -*- coding: utf-8 -*-

import pykintone
from mymodel import Person
from kagura.myjoblib import load, dump
from cache import get_all

from jinja2.environment import Environment
from jinja2 import Template, FileSystemLoader
import codecs
import os
import argparse
import unicodecsv as csv
from cStringIO import StringIO

OUTPUT_DIR = './output'
# OUTPUT_DIR = '../mitou/webtools/mitou.github.io/people'
env = Environment()
env.loader = FileSystemLoader('.')

def output(x):
    data = x.__dict__
    t = env.get_template('template_v01.html')
    html = t.render(data)
    fo = codecs.open(os.path.join(OUTPUT_DIR, '%s.html' % x.name), 'w', 'utf-8')
    fo.write(html)
    fo.close()


def assure_length(xs, length):
    if args.non_strict:
        if len(xs) != length:
            print 'length mismatch:', length, ','.join(xs)
        xs += [''] * length
    else:
        if len(xs) != length:
            raise RuntimeError(u'length mismatch: {} and {}'.format(length, u','.join(xs)).encode('utf-8'))


def process_tags(x):
    resume_list = []
    activity_list = []
    mitou_list = []
    photo = None

    rows = csv.reader(StringIO(x.tags.strip('\n').encode('utf8')), encoding='utf8')
    for items in rows:
        if not items: continue
        if items[0] == u'所属':
            # syntax: 所属,where,when,note
            # whenは「20xx-xx-xx時点」や「2014-2016」などのフリーフォーマット
            assure_length(items, 4)
            if items[1] in [u"", u"フリー", u"フリーランス"]: continue

            resume_list.append(dict(
                where=items[1],
                when=items[2],
                who=[],  # be filled by collect_tags
                note=items[3],
                ref_id=''
            ))
            # TODO when note include '#1' etc, put it in ref_id

        elif items[0] == u'未踏採択':
            # e.g. 未踏採択,2014,未踏,SC,任意キャラクターへの衣装転写システム,首藤 一幸
            assure_length(items, 6)
            mitou_list.append(dict(
                when=items[1],
                kubun=items[2],
                members=[],  # be filled by collect_tags
                sc=items[3],
                theme=items[4],
                pm=items[5]
            ))

        elif items[0] == u'Photo':
            photo = ':'.join(items[1:]).strip(':')

        elif items[0] == u'講演':
            activity_list.append(dict(
                type=items[0],
                title=u"{}「{}」".format(items[1], items[2]),
                when=items[3],
                who=[],
                note=items[4],
                ref_id=''
            ))
        else:
            assure_length(items, 4)
            activity_list.append(dict(
                type=items[0],
                title=items[1],
                when=items[2],
                who=[],
                note=items[3],
                ref_id=''
            ))

    x.activity_list = activity_list
    x.resume_list = resume_list
    x.mitou_list = mitou_list
    x.photo = photo
    return x


def put_all():
    for x in get_all(args.use_cache):
        x = process_tags(x)
        output(x)


def collect_tags():
    from collections import defaultdict

    mitou_theme = defaultdict(set)
    mitou_kubun = defaultdict(set)
    affiliation = defaultdict(set)
    event = defaultdict(set)

    xs = get_all(args.use_cache)
    for x in xs:
        x = process_tags(x)
        for m in x.mitou_list:
            if m['theme']:
                # PMs don't have `theme`
                mitou_theme[m['theme']].add(x)
            m['pretty_kubun'] = pretty(m['when'], m['kubun'])
            mitou_kubun[m['pretty_kubun']].add(x)
        for m in x.resume_list:
            affiliation[m['where']].add(x)
        for m in x.activity_list:
            event[m['title']].add(x)

    for x in xs:
        me = set([x])
        for m in x.mitou_list:
            m['members'] = sorted(mitou_theme[m['theme']] - me)
        for m in x.resume_list:
            m['who'] = sorted(affiliation[m['where']] - me)
        for m in x.activity_list:
            m['who'] = sorted(event[m['title']] - me)

    if not(args.index_only):
        for x in xs:
            output(x)

    t = env.get_template('template_list.html')
    print 'output kubun'
    data = list(sorted((k, mitou_kubun[k]) for k in mitou_kubun))
    html = t.render(title=u'採択区分別一覧', data=data)
    fo = codecs.open(os.path.join(OUTPUT_DIR, 'kubun.html'), 'w', 'utf-8')
    fo.write(html)
    fo.close()

    print 'output affiliation'
    data = list(sorted(
        ((k, affiliation[k])
         for k in affiliation),
        key=lambda x:-len(x[1])))
    html = t.render(title=u'所属別一覧', data=data)
    fo = codecs.open(os.path.join(OUTPUT_DIR, 'affiliation.html'), 'w', 'utf-8')
    fo.write(html)
    fo.close()

    print 'output index.html'
    t = env.get_template('template_index.html')
    html = t.render(title=u'未踏名鑑')
    fo = codecs.open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', 'utf-8')
    fo.write(html)
    fo.close()



def find_links(s):
    'convert name to link'
    assert isinstance(s, basestring)
    import re
    def make_link(m):
        name = m.groups()[0]
        return to_link(name)
    s = re.sub('\[(.+?)\]', make_link, s)
    return s
env.filters['find_links'] = find_links


def to_link(name):
    'get a name and make it to link'
    assert isinstance(name, basestring)
    return u'<nobr><a href="{0}.html">[{0}]</a></nobr>'.format(name)
env.filters['to_link'] = to_link


def abbrev_people(people):
    if len(people) < 8:
        return show_people(people)

    # 情報量の多い順に表示
    rest = len(people) - 7
    people = sorted(
        people,
        key=lambda p: len(p.tags) + len(p.note),
        reverse=True)
    from itertools import islice
    people = islice(people, 7)
    return ' '.join(to_link(p.name) for p in people) + u'他{}人'.format(rest)
env.filters['abbrev_people'] = abbrev_people


def show_people(people):
    return ' '.join(map(to_link, sorted(p.name for p in people)))
env.filters['show_people'] = show_people


def pretty(when, kubun=None):
    if '.' in when:
        year, ki = when.split('.')
        result = u'{}年{}期'.format(year, ki)
    else:
        result = when + u'年'
    if kubun:
        if kubun == u'ユース':
            kubun = u'未踏ユース'
        elif kubun == u'本体':
            kubun = u'未踏本体'
        elif kubun == u'未踏':
            pass  # do nothing
        else:
            raise RuntimeError(u'{} should be in ユース, 本体, 未踏'.format(kubun))
        result += kubun
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--use-cache', '-c',  action='store_true', help='use local cache for input instead of reading from kintone')
    parser.add_argument('--index-only', action='store_true', help='render index only')
    parser.add_argument('--non-strict', action='store_true', help='skip strict format check')
    args = parser.parse_args()
    collect_tags()
