import pathlib,json,copy,importlib.util,tempfile,hashlib,re
w=pathlib.Path(__file__).resolve().parent;r=w.parent/'repo'
def load(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
g=load(r/'ops/gate_output_doi_chieu.py','g');source=r/'ops/land/pr1340-wp1315-provenance/readback-chu-kho-mien-gate-packet-loop-issuecomment-6938174089.json';raw=source.read_bytes();base=json.loads(raw);sha=re.search('[0-9a-f]{40}',base['body'])[0];url=base['html_url'];os_name=re.search(r'gate-packet-loop \(([^)]+)\)',base['body'])[1];reason=next(s for s in base['body'].splitlines() if s.startswith('Lý do:')).split(':',1)[1].strip();date=base['created_at'][:10]
# Mutate a COPY of the real fixture's first line into the frozen r9 grammar; metadata remains from the copied fixture.
base['body']=f'mien_gate_output: {sha} os={os_name} ly_do={reason} han={date}\n'+'\n'.join(base['body'].splitlines()[1:]);claim='owner_waived — '+url+' '+sha
variants={x['id']:x for name in ['independent_mutants.jsonl','extra_mutants.jsonl','order_url_mutants.jsonl'] for x in map(json.loads,(w/name).read_text().splitlines())}
rows=[]
def call(fn):
 try:return fn()
 except Exception as e:return {'exception':type(e).__name__}
for n in ['control','waiver_partial','waiver_no_strip','waiver_head_truthy','waiver_order_os_sha','waiver_order_author_url','waiver_order_line_author','waiver_order_os_date','url_zero_indexerror','url_zero_optional']:
 d=copy.deepcopy(base);head=None;v=claim
 if n=='waiver_partial':d['body']=d['body'].replace('\n',' suffix\n',1)
 if n=='waiver_no_strip':d['body']='  '+d['body'].replace('\n','  \n',1)
 if n=='waiver_head_truthy':head=''
 if n=='waiver_order_os_sha':d['body']=d['body'].replace(os_name,'windows-latest',1).replace(sha,'0'*40,1)
 if n=='waiver_order_author_url':d['html_url']+='-changed';d['author_association']='MEMBER'
 if n=='waiver_order_line_author':d['body']=d['body'].split('\n',1)[1];d['author_association']='MEMBER'
 if n=='waiver_order_os_date':d['body']=d['body'].replace(os_name,'windows-latest',1).replace('han='+date,'han=2026-02-30',1)
 if n.startswith('url_zero'):v=claim.replace(url,'')
 m=g
 if n!='control':
  p=w/'contrast_modules'/(n+'.py');p.write_text(variants[n]['src']);m=load(p,n)
 with tempfile.TemporaryDirectory() as tmp:
  tmp=pathlib.Path(tmp);(tmp/source.name).write_text(json.dumps(d,ensure_ascii=False))
  a=call(lambda:g.kiem_mien(v,tmp,head));b=call(lambda:m.kiem_mien(v,tmp,head));row={'id':n,'original':a,'mutant':b,'different':a!=b}
  if n.startswith('url_zero'):
   doc={'landed':True,'gate_output':v};row['original_consumer']=call(lambda:g.kiem_ho_so(doc,tmp));row['mutant_consumer']=call(lambda:m.kiem_ho_so(doc,tmp))
  rows.append(row);print(json.dumps(row,ensure_ascii=False),flush=True)
(w/'real_waiver_matrix.json').write_text(json.dumps({'fixture':str(source.relative_to(r)),'fixture_sha256':hashlib.sha256(raw).hexdigest(),'rows':rows},ensure_ascii=False,indent=2))
