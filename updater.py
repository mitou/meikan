# -*- coding: utf-8 -*-
"""
kintone上のデータを、バックアップを取ってから一括アップデートするスクリプト

オプション指定なし→ローカルキャッシュを用いてDry Run
-r(--real) →最新のデータを取得してバックアップし、更新
-f(--from-backup) →-rで問題が起きたとき用。バックアップを指定して、そのデータを元に更新する。
"""

from cache import get_all, get_app
import time
import argparse
from render import pretty


def concat_lines(x, y):
    if isinstance(y, str): y = y.decode('utf-8')
    return x.rstrip('\n') + '\n' + y


def add_a_tag(tags, a_tag, length=None):
    assert not '\n' in a_tag
    if length:
        assert len(a_tag[1:].split(a_tag[0])) == length
    tags.append(a_tag)


def rows_to_csv(rows):
    import cStringIO
    import unicodecsv as csv
    f = cStringIO.StringIO()
    csv.writer(f, encoding='utf-8').writerows(rows)
    return f.getvalue()


def convert(xs, args):
    "add new creators from 2015_creators_170113.csv"
    import unicodecsv as csv
    name2x = dict((x.name, x) for x in xs)
    to_update = []
    to_add = []

    rd = csv.reader(file('2015_creators_170113.csv'), encoding='utf-8')
    for row in rd:
        year = row[2]
        kubun = row[3]
        sc = row[4]
        theme = row[5]
        name = row[6]
        pm = row[9]
        affil1 = row[7]
        affil2 = row[8]

        if name in name2x:
            x = name2x[name]
            to_update.append(x)
        else:
            from mymodel import Person
            x = Person()
            x.name = name
            to_add.append(x)

        tags = [
            ["未踏採択", year, kubun, sc, theme, pm],
            ["所属", affil1, "{}年時点".format(year), affil2]]
        tags = rows_to_csv(tags)
        x.tags = concat_lines(x.tags, tags)
        print name
        print tags

    return to_add, to_update




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--real', '-r',
        action='store_true', help='read from kintone and write to kintone')
    parser.add_argument(
        '--from-backup', '-f',
        action='store', help='read from backup and write to kintone')
    parser.add_argument(
        '--converter', '-c',
        action='store', help='use specific converter')
    parser.add_argument(
        '--infile', '-i',
        action='store', help='input file')
    args = parser.parse_args()

    if args.real:
        dumpdir = time.strftime('backup_%m%d_%H%M')
        xs = get_all(cache=False, name=dumpdir)
    elif args.from_backup:
        xs = get_all(cache=True, name=args.from_backup)
    else:
        xs = get_all(cache=True)

    if not args.converter:
        to_add, to_update = convert(xs, args)
    else:
        import imp
        info = imp.find_module('converter/' + args.converter)
        m = imp.load_module('m', *info)
        to_add, to_update = m.convert(xs, args)
    print "{} items to update, {} items to add".format(len(to_update), len(to_add))

    # when recover from backup we need to ignore revision
    if args.from_backup:
        for x in xs:
            x.revision = -1  # ignore revision

    if args.real or args.from_backup:
        app = get_app()

        result = app.batch_create(to_add)
        assert result.ok

        for i in range(0, len(to_update), 100):
            print i, to_update[i].name
            result = app.batch_update(to_update[i:i + 100])
            assert result.ok

    else:
        # for debug: Run this script with `ipython -i`
        globals()['xs'] = xs


if __name__ == '__main__':
    main()
