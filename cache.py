"""
library to get all data and cache them

If this is called as a script, it refresh local cache
"""
import pykintone
from pykintone import model
from mymodel import Person
import secret
import unicodecsv

def load(filename):
    rd = unicodecsv.reader(file(filename), encoding='utf-8')
    return [Person().from_tuple(args) for args in rd]

def dump(people, filename):
    wr = unicodecsv.writer(file(filename, 'w'), encoding='utf-8')
    for p in people:
        wr.writerow(p.to_tuple())

def get_app():
    app = pykintone.app('mitou', secret.JINZAI_APPID, secret.JINZAI_TOKEN)
    return app

def get_all(cache=False, name='all_data'):
    """
    cache: use local cache (default: False)
    """
    if cache:
        return load(name)

    app = get_app()
    result = []
    offset = 0
    while True:
        q = 'limit 500 offset {}'.format(offset)
        r = app.select(q).models(Person)
        result.extend(r)
        print len(r)
        print r[-1].name
        if len(r) == 500:
            offset += 500
            continue
        break
    dump(result, name)
    return result

if __name__ == '__main__':
    get_all(cache=False)
