import os,sys,pathlib,subprocess,json,shutil,datetime
ROOT=pathlib.Path.cwd(); O=ROOT/'out'; F=O/'fixtures';F.mkdir(exist_ok=True)
ENV={**os.environ,'GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':os.devnull,'GIT_CONFIG_COUNT':'0','PYTHONDONTWRITEBYTECODE':'1'}
for k in list(ENV):
 if k.startswith(('GIT_CONFIG_KEY_','GIT_CONFIG_VALUE_')): ENV.pop(k)
SOURCE=(O/'snapshot-clone/ops/lease_publish.py').read_bytes();PY='/usr/bin/python3'
commands=[]
def run(args,cwd,ok=True):
 p=subprocess.run(list(map(str,args)),cwd=cwd,env=ENV,capture_output=True,text=True)
 commands.append({'cwd':str(cwd.relative_to(ROOT)),'argv':list(map(str,args)),'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
 if ok: assert p.returncode==0,(args,p.returncode,p.stderr)
 return p

def git(c,*a,ok=True):return run(['git','-c','commit.gpgsign=false',*a],c,ok)
def make(name):
 c=F/name;c.mkdir();git(c,'init','-q','-b','master');git(c,'config','user.name','Review fixture');git(c,'config','user.email','fixture@example.invalid')
 (c/'ops').mkdir();(c/'ops/lease_publish.py').write_bytes(SOURCE);(c/'ops/leases').mkdir();(c/'README').write_text('Benign scanner fixture. No authority.\n')
 git(c,'add','.');git(c,'commit','-qm','fixture base');base=git(c,'rev-parse','HEAD').stdout.strip()
 server=F/(name+'-origin.git');git(F,'clone','--bare','-q',str(c),str(server));git(c,'remote','add','origin',str(server));git(c,'fetch','-q','origin','+refs/heads/*:refs/remotes/origin/*');git(c,'checkout','-q','--detach',base)
 return c,server,base

def save(c,name,lease):
 p=c/'ops/leases'/name;p.write_text(json.dumps(lease));git(c,'add',str(p));git(c,'commit','-qm','fixture lease data');return git(c,'rev-parse','HEAD').stdout.strip()
def publish(c,s,sha,branch='lease'):
 git(s,'fetch','-q',str(c),sha);git(s,'update-ref','refs/heads/'+branch,sha);git(c,'fetch','-q','origin','+refs/heads/*:refs/remotes/origin/*')
def scan(c,label,path='.claude/dev/packet_loop.py'):
 p=run([PY,'-B','ops/lease_publish.py','ai-dang-giu',path,'--root','.'],c,False)
 print(label,'rc',p.returncode,'LAST',(p.stdout.strip().splitlines() or ['EMPTY'])[-1], 'ERR',p.stderr.strip(),flush=True)
 return p

def lease(id='wp999901-r1-g1-claude',**kw):
 return dict(lease_id=id,lease_expires_at_utc='2030-01-01T00:00:00Z',write_set=['.claude/dev/packet_loop.py'],**kw)
def post_ok(p,id,ref,path):
 rows=[l.split('\t') for l in p.stdout.splitlines() if l.startswith('CÒN_HẠN') and 'ĐÃ_BỊ_THAY_THẾ' not in l]
 return p.returncode==11 and p.stdout.strip().splitlines()[-1]=='NGƯỜI_GIỮ 1: '+id and all(r[1]==id for r in rows) and any(r[2]==ref+':'+path for r in rows)
print('UTC',datetime.datetime.now(datetime.timezone.utc).isoformat())
# 1. Same names/count, changed object; deletion cache. Only local fixture remotes.
c,s,b=make('refs');sha=save(c,'one.yaml',lease());publish(c,s,sha,'master')
# Deliberately set old cache to measure the required pair comparison, then fetch.
git(c,'update-ref','refs/remotes/origin/master',b)
def pairs():
 a={(l.split()[1].removeprefix('refs/heads/'),l.split()[0]) for l in git(c,'ls-remote','--heads','origin').stdout.splitlines()}
 d={(l.split()[0].removeprefix('refs/remotes/origin/'),l.split()[1]) for l in git(c,'for-each-ref','--format=%(refname) %(objectname)','refs/remotes/origin').stdout.splitlines() if not l.split()[0].endswith('/HEAD')};return a,d
a,d=pairs();print('H1_SAME_NAMES', {x[0] for x in a}=={x[0] for x in d},'PAIRS_MISSING_EXTRA',len(a-d),len(d-a))
git(c,'fetch','-q','origin','+refs/heads/*:refs/remotes/origin/*');a,d=pairs();print('H1_FETCH_PAIR_EQUAL',a==d)
git(c,'update-ref','refs/remotes/origin/retired',b);git(c,'fetch','-q','origin','+refs/heads/*:refs/remotes/origin/*');a,d=pairs();print('H1_NO_PRUNE_EXTRA',len(d-a))
git(c,'fetch','-q','--prune','origin','+refs/heads/*:refs/remotes/origin/*');a,d=pairs();print('H1_PRUNE_EXTRA',len(d-a))
# 2. Policy appearance and withdrawal is distinct from current-tree check.
c,s,b=make('policy');p=c/'.github/coordination/change-impact.v1.json';p.parent.mkdir(parents=True);p.write_text('{"schema_version":1,"rules":[]}\n');git(c,'add','.');git(c,'commit','-qm','policy present');sha=git(c,'rev-parse','HEAD').stdout.strip();publish(c,s,sha,'master')
def policies():return [x for x in git(c,'ls-tree','-r','-z','--name-only','origin/master','--','.github/coordination').stdout.split('\0') if 'change-impact' in x]
print('H2_PRESENT',len(policies()));git(c,'rm','-q',str(p));git(c,'commit','-qm','policy withdrawn');publish(c,s,git(c,'rev-parse','HEAD').stdout.strip(),'master');print('H2_WITHDRAWN',len(policies()),'HISTORY_COMMITS',len(git(c,'log','--format=%H','--all','--','.github/coordination/change-impact.v1.json').stdout.splitlines()))
# 3. The before/after test is actually satisfiable using the original CLI.
c,s,b=make('post');p=scan(c,'H3_BEFORE');assert p.returncode==0
id='wp999901-r1-g1-claude';sha=save(c,'one.yaml',lease(id));publish(c,s,sha);p=scan(c,'H3_AFTER');print('H3_POST_PREDICATE',post_ok(p,id,'refs/remotes/origin/lease','ops/leases/one.yaml'));assert post_ok(p,id,'refs/remotes/origin/lease','ops/leases/one.yaml')
# Another ordinary active holder must not pass the after predicate.
sha=save(c,'two.yaml',lease('wp999902-r1-g1-claude'));publish(c,s,sha);p=scan(c,'H3_TWO');print('H3_TWO_POST_PREDICATE',post_ok(p,id,'refs/remotes/origin/lease','ops/leases/one.yaml'))
# 4. One-sided tombstone is unknown; completed pair is observable.
c,s,b=make('tombstone');old=lease(da_bi_thay_the='wp999902-r1-g1-claude');sha=save(c,'old.yaml',old);publish(c,s,sha);p=scan(c,'H4_ONE_SIDED');assert p.returncode==12
new=lease('wp999902-r1-g1-claude',thay_the_cho=['wp999901-r1-g1-claude']);sha=save(c,'new.yaml',new);publish(c,s,sha);p=scan(c,'H4_TWO_SIDED');print('H4_OLD_MARKED', 'ĐÃ_BỊ_THAY_THẾ\twp999901-r1-g1-claude' in p.stdout,'NEW_POST',post_ok(p,new['lease_id'],'refs/remotes/origin/lease','ops/leases/new.yaml'))
# 5. Benign invalid data and expired record are not indistinguishable from a live holder.
for name,obj in [('wrong_shape',[]),('wrong_time',{**lease(),'lease_expires_at_utc':'unknown'}),('expired',{**lease(),'lease_expires_at_utc':'2020-01-01T00:00:00Z'})]:
 c,s,b=make(name);sha=save(c,'data.yaml',obj);publish(c,s,sha);scan(c,'H5_'+name)
# 6. Prefix write set is normal protocol data, demonstrates declared G2.
c,s,b=make('prefix');ob=lease();ob['write_set']=['.claude/dev/'];sha=save(c,'prefix.yaml',ob);publish(c,s,sha);p=scan(c,'H6_PREFIX');print('H6_DECLARED_G2',p.returncode==0)
# 7. Provenance is first seen blob/path, and after-publish can conservatively stop.
c,s,b=make('provenance');sha=save(c,'one.yaml',lease());publish(c,s,sha);git(c,'branch','local-copy',sha);p=scan(c,'H7_LOCAL_COPY');print('H7_POST_PREDICATE',post_ok(p,'wp999901-r1-g1-claude','refs/remotes/origin/lease','ops/leases/one.yaml'));print('H7_ROWS',[l for l in p.stdout.splitlines() if l.startswith('CÒN_HẠN')])
# 8. A pre-existing repository Unicode path tests Git quoting without constructing an attack filename.
src=ROOT/'cay-kho';raw=run(['git','ls-tree','-r','-z','--name-only','HEAD'],src).stdout
path=next(x for x in raw.split('\0') if x.endswith('.log') and any(ord(ch)>127 for ch in x))
for label,args in [('DEFAULT',['ls-tree','-r','HEAD','--',path]),('NUL',['ls-tree','-r','-z','HEAD','--',path])]:
 out=run(['git',*args],src).stdout;got=out.split('\t',1)[1].rstrip('\n\0');print('H8_'+label,'PATH_EQUAL',got==path,'SUFFIX_LOG',got.endswith('.log'))
(O/'hunt-commands.json').write_text(json.dumps(commands,ensure_ascii=False,indent=2))
print('DONE',len(commands),'commands; fixture authority=NONE')
