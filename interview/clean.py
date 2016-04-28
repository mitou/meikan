# -*- coding: utf-8 -*-
fi = file('t.csv')
fo = file('t2.csv', 'w')
for line in fi:
    s = line.strip()
    if not s: continue
    if s.startswith('#,#'): continue
    #if s.startswith('## 創造的'): continue
    if all(c in u',○'for c in s.decode('utf-8', 'ignore')):
        continue
    fo.write(line)
fo.close()


