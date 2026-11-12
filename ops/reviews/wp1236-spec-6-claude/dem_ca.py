"""Dem ca/ve/dot bien cua bang dot A1 trong r5 va r6 (proxy kich thuoc test)."""
import re, sys
def bang(path, dau, het):
    t = open(path, encoding='utf-8').read()
    i = t.index(dau); j = t.index(het, i)
    return t[i:j]
for f in ('SPEC_R5.md', 'SPEC.md'):
    b = bang(f, '### Đợt A1 —', '### Đợt A2 —')
    rows = [l for l in b.splitlines() if l.startswith('| A')]
    ve = sum(len(re.findall(r'\(([a-n]|f′|i|j)\)', r.split('|')[2])) or 1 for r in rows)
    mut = sum(len(re.findall(r'm-A\d+[a-z]?', r)) for r in rows)
    mut += len(re.findall(r'm-A\d+[a-z]?…[a-z]', b))  # dang a…h
    doi = len(re.findall(r'đối chứng \(\d\)|\(\d\) `', b))
    print(f, 'hang', len(rows), 've~', ve, 'dot bien (dem ten)', mut, 'so ky tu bang', len(b), 'doi chung A22', len(re.findall(r'đối chứng|\(\d\) `', b)))
