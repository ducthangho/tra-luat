import pathlib,subprocess,re,json,types,datetime,sys
ROOT=pathlib.Path.cwd(); O=ROOT/'out'; C=O/'snapshot-clone'
def git(*a):
 p=subprocess.run(['git',*a],cwd=C,capture_output=True);assert p.returncode==0,(a,p.stderr);return p.stdout
print('UTC',datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
server={(x.split()[1].decode().removeprefix('refs/heads/'),x.split()[0].decode()) for x in git('ls-remote','--heads','origin').splitlines()}
cache={(x.split()[0].decode().removeprefix('refs/remotes/origin/'),x.split()[1].decode()) for x in git('for-each-ref','--format=%(refname) %(objectname)','refs/remotes/origin').splitlines() if not x.split()[0].endswith(b'/HEAD')}
print('SNAPSHOT_REF_PAIRS',len(server),len(cache),'missing',len(server-cache),'extra',len(cache-server),flush=True)
print('POLICY_PATHS',[x.decode() for x in git('ls-tree','-r','-z','--name-only','origin/master','--','.github/coordination').split(b'\0') if b'change-impact' in x],flush=True)
refs=[x.decode() for x in git('for-each-ref','--format=%(refname)','refs/remotes/origin').splitlines()]
print('ADR_MASTER',sum(bool(re.match(rb'docs/adr/[0-9]{4}-',x)) for x in git('ls-tree','--name-only','origin/master','docs/adr/').splitlines()),flush=True)
hits=[]
for ref in refs:
 paths=git('ls-tree','-r','-z','--name-only',ref,'--','docs/adr').split(b'\0')
 h=[p.decode() for p in paths if re.match(rb'docs/adr/[0-9]{4}-',p) and int(p.split(b'/')[-1][:4])>=68]
 if h:hits.append([ref,h])
print('REFS_ADR_GE_0068',len(hits),hits,flush=True)
ws=['.claude/dev/packet_loop.py','.claude/dev/packet_loop_test.py','docs/PROTOCOL_DA_PHIEN.md','docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md']
for i,path in enumerate(ws):
 cmd=['/usr/bin/python3','-B','ops/lease_publish.py','ai-dang-giu',path,'--root','.'];p=subprocess.run(cmd,cwd=C,capture_output=True,text=True)
 (O/f'lease-path-{i}.log').write_text('COMMAND '+repr(cmd)+'\nrc='+str(p.returncode)+'\n'+p.stdout+p.stderr)
 print('LEASE',path,'rc',p.returncode,'LAST',p.stdout.strip().splitlines()[-1] if p.stdout.strip() else 'EMPTY',flush=True)
 print('ACTIVE_LINES',[l for l in p.stdout.splitlines() if l.startswith('CÒN_HẠN') and 'ĐÃ_BỊ_THAY_THẾ' not in l],flush=True)
lp=types.ModuleType('lp');exec(compile((C/'ops/lease_publish.py').read_bytes(),str(C/'ops/lease_publish.py'),'exec'),lp.__dict__)
cac=lp._quet_lease_toan_kho(C);fixed=datetime.datetime(2026,11,21,5,41,51,tzinfo=datetime.timezone.utc)
for label,now in [('S18_TIME',fixed),('NOW',datetime.datetime.now(datetime.timezone.utc))]:
 con=[m for m in cac if lp._phan_loai_lease(m['lease'],now)=='CÒN_HẠN'];live=[m for m in con if lp._bia_mo_doi_xung(m['lease'],cac) is not True]
 print(label,'RECORDS',len(cac),'NOT_EXPIRED',len(con),'TOMBSTONED',len(con)-len(live),'LIVE_RECORDS',len(live),'LIVE_IDS',sorted({m['lease']['lease_id'] for m in live}),flush=True)
(O/'leases-snapshot.json').write_text(json.dumps(cac,ensure_ascii=False,default=str))
