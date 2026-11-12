import re
def bang(t, dau, het):
    i = t.index(dau); j = t.index(het, i); return t[i:j]
for f in ('work/SPEC_R4.md', 'SPEC_R5.md', 'SPEC.md'):
    t = open(f, encoding='utf-8').read()
    b = bang(t, '### Đợt A1 —', '### Đợt A2 —')
    rows = [l for l in b.splitlines() if l.startswith('| A')]
    ve = 0
    for r in rows:
        c = r.split('|')[2]
        n = len(set(re.findall(r'\(([a-n]′?|f′)\)', c)))
        ve += n or 1
    mut = len(re.findall(r'm-A\d+[a-z]?(?![…a-z])', b)) + sum(ord(m[1]) - ord(m[0]) + 1 for m in re.findall(r'm-A\d+([a-z])…([a-z])', b))
    them = b[b.index('Thêm, không hồi quy'):] if 'Thêm, không hồi quy' in b else ''
    fx = bang(t, '### Fixture chung', '### Đợt A1 —')
    m = re.search(r'\| A1 \| \d \| ([^|]+)\|', t)
    print(f'{f:18} hang={len(rows)} ve={ve} dot_bien={mut} ky_tu_bang={len(b)} ky_tu_fixture={len(fx)} uoc={m.group(1)[:60]!r}')
