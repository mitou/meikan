# -*- encoding: utf-8 -*-
import re
import codecs
import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input-file', action='store', )
parser.add_argument('--event-suffix', action='store', default='')
args = parser.parse_args()

title_file = args.input_file.replace('.txt', '_title.csv')
affiliation_file = args.input_file.replace('.txt', '_affiliation.csv')
fi = codecs.open(args.input_file, 'r', 'utf-8')
writer = csv.writer(file(title_file, 'w'))
writer2 = csv.writer(file(affiliation_file, 'w'))

def to_utf8(*xs):
    return [x.encode('utf-8') for x in xs]

title = ''
for lineno, line in enumerate(fi):
    print lineno, line.strip()
    if line.startswith('!'):
        continue
    if line.startswith('##'):
        items = line.strip().split()
        #print items
        try:
            _tag, event, start, _tag, _end = items
        except:
            _tag, event, start = items
        event = event + args.event_suffix
    elif line.startswith('#'):
        items = line.strip().split(' ', 1)
        #print line
        #print items
        _tag, title = items
    elif title:
        assert re.match('([^,()]+) \(([^()]*)\)(, ([^,()]+) \(([^()]*)\))*$', line)
        items = re.findall('([^,()]+) \(([^()]*)\)', line)
        for item in items:
            name, affil = item
            name = name.strip()
            writer.writerow(to_utf8(name, event, title, start))
            for a in affil.split(','):
                writer2.writerow(to_utf8(name, a.strip(), start))
        #print line
        #print items

        title = ''
    #print line
