from pathlib import Path
import ast,collections,importlib.util,json,lzma,sys,unicodedata,yaml
sys.dont_write_bytecode=True
r=Path.cwd();w=r.parent/'work'
s=importlib.util.spec_from_file_location('t',r/'ops/land_evidence_nguon_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
rows=[];orig=t.ky8
# Structural oracle built from spec literals and ordered delimiter search, no imports of product regexes.
def grammar(raw):
 txt=raw.decode('utf-8');lines=(txt[:-1] if txt.endswith('\n') else txt).split('\n')
 if any(x.endswith('\r') for x in lines):
  if not all(x.endswith('\r') for x in lines):return 'xuong_dong_tron'
  lines=[x[:-1] for x in lines]
 if any('\r' in x for x in lines):return 'cr_le'
 prefix='# Danh gia Gate output run 10 attempt 20 head '+'a'*40+' — '
 suffix='(danh_gia_gate.py sha256 '+'a'*64+')'
 if not lines[0].startswith(prefix) or not lines[0].endswith(suffix):return 'dau_tep_sai'
 for line in lines[1:]:
  if line=='' or line=='MOC_GATE_OUTPUT: passed (1/2 job co dau hieu duong)':continue
  accepted=False
  for pre,tail in [('JOB 42 ',': skipped (khong tinh)'),('JOB 53 ',': skipped -> not_measured (khong suy pass)')]:
   if line.startswith(pre) and line.endswith(tail) and len(line)>len(pre)+len(tail):accepted=True
  if line.startswith('JOB 31 '):
   payload=line[len('JOB 31 '):];tail='] conclusion=success log_sha256='+'a'*64+' -> passed: x'
   # Earliest valid split: label contains no ']', while the name may contain previous candidate delimiters.
   for i in range(1,len(payload)):
    if payload[i:i+2]==' [' and payload.endswith(tail):
     label=payload[i+2:-len(tail)]
     if ']' not in label:accepted=True;break
  if not accepted:return 'dong_la'
 return 'bo_sinh_la'
def observer(hs,prov,rc,label,l8=(),*args,**kwargs):
 raw=next(iter(prov.values()));raw=raw.encode() if isinstance(raw,str) else raw
 want=grammar(raw);expected=f'$.gate_output: danh_gia_khong_passed:danh-gia-gate-output-10.txt:not_measured:{want}'
 assert l8==[expected],(label,l8,want)
 orig(hs,prov,rc,label,l8,*args,**kwargs)
 rows.append({'label':label,'independent_reason':want,'passed':True})
t.ky8=observer
rc,msg=t.chay_ca(next(k for k in t.CA if k.startswith('c37_')));assert rc==0,(rc,msg)
summary={}
all_categories={unicodedata.category(chr(i)) for i in range(0x110000)}-{'Cs'}
for vt in ['dau','nhan','cu','v3']:
 vals=[ast.literal_eval(x['label'].split(' ',1)[1]) for x in rows if x['label'].startswith(vt+' ')]
 assert set(map(chr,range(128)))<=set(vals)
 cats={unicodedata.category(c) for c in vals if len(c)==1};assert all_categories<=cats and any(len(c)==1 and ord(c)>65535 for c in vals)
 summary[vt]={'n':len(vals),'categories':sorted(cats),'ASCII':128,'reasons':dict(collections.Counter(x['independent_reason'] for x in rows if x['label'].startswith(vt+' ')))}
# Separate check of semantic split on the valid real fixture, so bo_sinh_la cannot conceal wrong identity.
p=t.prov_that();text=p[t.DG];job=next(x for x in text.splitlines() if x.startswith('JOB '));jid=int(job.split()[1]);provkey=next(k for k in p if k.endswith('.yaml'));base=yaml.safe_load(p[provkey]);origjob=next(j for j in base['moc']['gate_output']['jobs'] if j['job_id']==jid);name=origjob['name'];labs=','.join(origjob['labels']);tail=job[len(f'JOB {jid} '+name):];semantic=[]
for label,newjob,newname,newlabs,expected in [
 ('label-backtracks',f'JOB {jid} {name} [a] [b]'+tail[tail.index(' conclusion='):],name+' [a]','b',[]),
 ('label-backtracks-wrong-identity',f'JOB {jid} {name} [a] [b]'+tail[tail.index(' conclusion='):],name,'b',['job_lech:'+str(jid)]),
 ('earliest-full-suffix',job+tail,name,labs,[]),
 ('skip-invalid-delimiter',f'JOB {jid} {name} [a] nope'+tail,name+' [a] nope',labs,[])]:
 b=yaml.safe_load(p[provkey]);j=next(j for j in b['moc']['gate_output']['jobs'] if j['job_id']==jid);j['name']=newname;j['labels']=newlabs.split(',')
 actual,out=t.chay(json.dumps({'moc_gate_output':'measured — '+t.DG}),p|{t.DG:text.replace(job,newjob,1),provkey:yaml.safe_dump(b,allow_unicode=True)},doi_chieu=t.DOI_CHIEU)
 want=[f'$.moc_gate_output: danh_gia_khong_passed:{t.DG}:not_measured:{x}' for x in expected]
 assert actual==(1 if expected else 0) and t.dong_l8(out)==want,(label,actual,t.dong_l8(out),want)
 semantic.append({'label':label,'rc':actual,'l8':want,'passed':True})
o=json.loads((w/'ledger-o.json').read_text());eo=json.loads((r.parent/'bang_chung/ledger/ledger-o-bca55c1.json').read_text());assert o==eo
c=(w/'ledger-c36.jsonl').read_bytes();ec=lzma.decompress((r.parent/'bang_chung/ledger/ledger-c36-bca55c1.jsonl.xz').read_bytes());assert c==ec
result={'independent_oracle':summary,'semantic_lazy_probes':semantic,'ledger_equal':{'B':len(o),'c36':len(c.splitlines())},'rows':rows};(w/'c37-audit.json').write_text(json.dumps(result,ensure_ascii=True,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='rows'},ensure_ascii=False,indent=2))
