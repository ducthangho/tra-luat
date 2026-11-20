import pathlib,json,collections
w=pathlib.Path(__file__).resolve().parent
def lines(n):return [json.loads(l) for l in (w/n).read_text().splitlines()]
a=lines('independent_results.jsonl');b=lines('independent_corrected_results.jsonl');c=lines('extra_results.jsonl')
assert len(a)==96 and len(b)==11 and len(c)==6,(len(a),len(b),len(c))
a=[x for x in a if x['kind']!='identity' and x['id']!='token_delimiter_40']+b+c
assert len(a)==102 and len({x['id'] for x in a})==102
for x in a:
 cs=[json.loads(l) for l in x.get('stdout','').splitlines() if l.startswith('{')];x['cases']=cs
 x['grade']='GIET' if any(y['rc']==3 for y in cs) else 'SONG' if x.get('rc')==0 and len(cs)==36 and all(y['rc']==0 for y in cs) else 'TIN_DUNG_GIA' if len(cs)==36 and any(y['rc']==4 for y in cs) else 'HONG'
 x.pop('stdout',None)
(w/'independent_final.json').write_text(json.dumps(a,ensure_ascii=False,indent=2))
print(dict(collections.Counter(x['grade'] for x in a)))
for x in a:
 if x['grade']!='GIET':print(x['id'],x['grade'])
