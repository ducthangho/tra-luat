from pathlib import Path
import sys,os,subprocess,json,collections,unicodedata,inspect
O=Path(__file__).resolve().parent;P=O/'prototype';R=O.parent/'cay-kho'
os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.dont_write_bytecode=True;sys.path.insert(0,str(P/'.claude/dev'));os.chdir(P)
import packet_loop_test as t, packet_loop_test_manh as m
names=[n for n,f in t.CASES];new=[n for n in names if n.startswith('doctrine_inv_')];mu={k:v for k,v in t.MUTANTS.items() if k.startswith(('inv_','t1466_'))}
print('REGISTRY',len(names),len(set(names)),len(m.ca_dang_ky(t)),len(t.MUTANTS));print('NEW',len(new),'MUTANTS',len(mu),'SOURCE',len(set(mu)-t.MUTANTS_NHAM_TEST),'TEST',len(set(mu)&t.MUTANTS_NHAM_TEST));targets={n for v in mu.values() for n in v[2]};print('ALL_NEW_TARGETED',set(new)<=targets,'MISSING',sorted(set(new)-targets))
for k,v in mu.items():
 src=(P/'.claude/dev'/('packet_loop_test.py' if k in t.MUTANTS_NHAM_TEST else 'packet_loop.py')).read_text();print('MARKER',k,src.count(v[0]))
print('LINUX_EXCLUDED',sorted(set(names)-set(m.ca_dang_ky(t))))
for f in ['packet_loop.py','packet_loop_test.py']:
 vals=[]
 for root in [O/'base',P]:
  s=(root/'.claude/dev'/f).read_text();counts=collections.Counter(f'U+{ord(c):04X}' for c in s if (unicodedata.category(c) in ['Cc','Cf','Zl','Zp'] and c!='\n') or unicodedata.category(c)=='Zs' and c!=' ');vals.append(counts)
 print('UNUSUAL',f,[sum(v.values()) for v in vals],vals[0]==vals[1])
# Snapshot lease count at the exact author clock, and after the fixture of current snapshot expired.
sys.path.insert(0,str(R/'ops'));import lease_publish as lp,datetime
rows=lp._quet_lease_toan_kho(R,doi_chieu_ref=False)
for stamp in ['2026-11-21T02:57:49+00:00','2026-11-21T03:24:55+00:00',datetime.datetime.now(datetime.timezone.utc).isoformat()]:
 now=datetime.datetime.fromisoformat(stamp);live=[r for r in rows if lp._phan_loai_lease(r['lease'],now)=='CÒN_HẠN'];dead=[r for r in live if lp._bia_mo_doi_xung(r['lease'],rows) is True];active=[r for r in live if r not in dead];print('LEASE_AT',stamp,len(rows),len(live),len(dead),len(active));print('ACTIVE_IDS',[r['lease']['lease_id'] for r in active])
for r in rows:
 if r['lease'].get('lease_id')=='wp433-r9-g5-claude':
  z=subprocess.run(['git','-C',str(R),'log','-1','--format=%H %cI %s',r['ref'],'--',r['path']],capture_output=True,text=True);print('NEW_LEASE_ORIGIN',r['ref'],r['path'],z.stdout.strip());break
print('S8_ADAPTERS',sum('doctrine-scan --root .' in p.read_text() for base in [P/'.claude/skills',P/'.agents/skills'] for p in base.rglob('*.md')))
print('S8_WORKFLOW',(P/'.github/workflows/ci.yml').read_text().count('doctrine-scan --root .'))
print('S8_CLI_IN_TEST',sum('"doctrine-scan"' in l for l in (O/'base/.claude/dev/packet_loop_test.py').read_text().splitlines()))
