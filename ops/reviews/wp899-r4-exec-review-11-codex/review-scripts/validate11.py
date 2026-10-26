import collections, hashlib, json, pathlib, re
R=pathlib.Path(__file__).resolve().parent
audit=json.loads((R/'audit8-results.json').read_text())
front=json.loads((R/'frontier11.json').read_text())
raw=(R/'closed.stdout.txt').read_text()
records=re.findall(r'\[KQ\] (\S+) ([0-9a-f]{16}) (GIET|SONG|TIN_DUNG_GIA)',raw)
want={r['id']:r['sha256'] for r in audit['mutants']}
have={m:(h,rank) for m,h,rank in records}
assert len(records)==len(have)==len(want)==1009
assert set(have)==set(want)
assert all(h==want[m][:16] for m,(h,_) in have.items())
equiv=set(audit['equivalence'])
assert {m for m,(_,rank) in have.items() if rank=='SONG'}==equiv
assert not [m for m,(_,rank) in have.items() if rank=='TIN_DUNG_GIA']
assert not [m for m in equiv if have[m][1]=='GIET']
assert 'TONG DONG: DAT' in raw
assert json.loads((R/'closed.json').read_text())['rc']==0
suite=(R/'suite.stdout.txt').read_text()
for marker in ('CA: 52/52 dat','DOT BIEN: 292/292 bi giet dung ly do','TU KIEM PHAN HANG: DAT (2 dot bien)','TONG: DAT'):
    assert marker in suite, marker
assert json.loads((R/'suite.json').read_text())['rc']==0
report={'records':len(records),'unique_ids':len(have),'sha256_prefixes_match':True,'resume_used':False,
        'rank_counts':dict(collections.Counter(rank for _,rank in have.values())),
        'frontier_initial':front['frontier_count'],
        'frontier_measured':len(set(front['frontier_ids'])&have.keys()),
        'frontier_ranks':dict(collections.Counter(have[m][1] for m in front['frontier_ids'])),
        'per_function':{f:dict(collections.Counter(rank for m,(_,rank) in have.items() if m.split('#')[0]==f)) for f in audit['per_function']},
        'full_source_hashes':want,'equivalences':sorted(equiv)}
(R/'full-validation11.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='full_source_hashes'},ensure_ascii=False,indent=2))
