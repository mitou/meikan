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
    return x.rstrip('\n') + '\n' + y


def add_a_tag(tags, a_tag, length=None):
    assert not '\n' in a_tag
    if length:
        assert len(a_tag[1:].split(a_tag[0])) == length
    tags.append(a_tag)


def convert(xs):
    return xs

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
    args = parser.parse_args()

    if args.real:
        dumpdir = time.strftime('backup_%m%d_%H%M')
        xs = get_all(cache=False, name=dumpdir)
    elif args.from_backup:
        xs = get_all(cache=True, name=args.from_backup)
    else:
        xs = get_all(cache=True)

    if not args.converter:
        xs = convert(xs)
    else:
        import imp
        info = imp.find_module('converter/' + args.converter)
        m = imp.load_module('m', *info)
        xs = m.convert(xs)

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
