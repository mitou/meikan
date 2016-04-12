# -*- coding: utf-8 -*-
"""
バックアップを取ってから一括アップデートするスクリプト

オプション指定なし→ローカルキャッシュを用いてDry Run
-r(--real) →最新のデータを取得してバックアップし、更新
-f(--from-backup) →-rで問題が起きたとき用。バックアップを指定して、そのデータを元に更新する。

"""

from cache import get_all, get_app
import time
import argparse
from render import pretty


def concat_lines(x, y):
    return x.rstrip('\n') + '\n' + y


def add_a_tag(tags, a_tag, length=None):
    assert not '\n' in a_tag
    if length:
        assert len(a_tag[1:].split(a_tag[0])) == length
    tags.append(a_tag)


def convert(xs):
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--real', '-r',
        action='store_true', help='read from kintone and write to kintone')
    parser.add_argument(
        '--from-backup', '-f',
        action='store', help='read from backup and write to kintone')
    args = parser.parse_args()

    if args.real:
        dumpdir = time.strftime('backup_%m%d_%H%M')
        xs = get_all(cache=False, name=dumpdir)
    elif args.from_backup:
        xs = get_all(cache=True, name=args.from_backup)
    else:
        xs = get_all(cache=True)

    xs = convert(xs)

    # when recover from backup we need to ignore revision
    if args.from_backup:
        for x in xs:
            x.revision = -1  # ignore revision

    if args.real or args.from_backup:
        app = get_app()
        for i in range(0, len(xs), 100):
            print i, xs[i].name
            app.batch_update(xs[i:i + 100])
    else:
        # for debug: Run this script with `ipython -i`
        globals()['xs'] = xs


if __name__ == '__main__':
    main()
