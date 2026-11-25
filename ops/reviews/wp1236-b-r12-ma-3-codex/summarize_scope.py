from pathlib import Path
import json,lzma,re,collections,importlib.util
R=Path.cwd();W=R.parent/'work'
rows=[json.loads(x) for x in lzma.open(W/'adapter-rows.jsonl.xz','rt')]
summary={'calls':len(rows),'positions':{}};values={k:collections.Counter() for k in ['header_free_text','skip_old_name','skip_v3_name','labels']}
def scan(text):
 for d in text.split('\n'):
  if d.startswith('# Danh gia ') and ' — ' in d and '(danh_gia_gate.py sha256 ' in d:
   v=d.split(' — ',1)[1].split('(danh_gia_gate.py sha256 ',1)[0];values['header_free_text'][v]+=1
  if d.startswith('JOB ') and ': skipped' in d:
   before,after=d.rsplit(': skipped',1);parts=before.split(' ',2)
   if len(parts)==3:values['skip_v3_name' if '-> not_measured' in after else 'skip_old_name'][parts[2]]+=1
  if d.startswith('JOB ') and (m:=re.search(r'\[([^\]]*)\] conclusion=',d)):values['labels'][m[1]]+=1
for row in rows:
 for name,txt in row['files'].items():
  if name.endswith('.txt') and 'danh-gia-gate-output' in name:scan(txt)
s=importlib.util.spec_from_file_location('b',R/'ops/land_evidence_nguon_test.py');b=importlib.util.module_from_spec(s);s.loader.exec_module(b)
old=b.chay;count=[0];raw=[0]
def chay(hs,prov,**kw):
 for name,txt in (prov or {}).items():
  if 'danh-gia-gate-output' in name:
   count[0]+=1
   if isinstance(txt,bytes):
    try:txt=txt.decode()
    except UnicodeDecodeError:raw[0]+=1;continue
   scan(txt)
 return old(hs,prov,**kw)
b.chay=chay
rc,msg=b.chay_ca(next(k for k in b.CA if k.startswith('c35')));assert rc==0,(rc,msg)
for k,v in values.items():
 summary['positions'][k]={'distinct':len(v),'values':dict(v),'empty_count':v.get('',0),'non_ascii_values':[x for x in v if not x.isascii()]}
summary|={'c35_files':count[0],'c35_invalid_utf8':raw[0],'c35_rc':rc}
# Exact replay of executor ledger, independently compared after execution.
a=json.loads((W/'ledger-o.json').read_text());e=json.loads((R.parent/'bang_chung/ledger/ledger-o-8782e25.json').read_text());assert a==e
c=[json.loads(x) for x in (W/'ledger-c36.jsonl').read_text().splitlines()]
e=[json.loads(x) for x in lzma.open(R.parent/'bang_chung/ledger/ledger-c36-8782e25.jsonl.xz','rt')];assert c==e
summary['ledger_equal']={'b':len(a),'c36':len(c)}
summary['a125_grammar_positive']=sum(any(':bo_sinh_la' in y for y in x['l8']) for x in c if x['ca_a'].startswith('a125'))
(W/'scope-summary.json').write_text(json.dumps(summary,ensure_ascii=True,indent=2));print(json.dumps(summary,ensure_ascii=True,indent=2))
