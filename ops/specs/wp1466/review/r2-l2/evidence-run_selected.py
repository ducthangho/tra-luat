import collections, inspect, json, os, pathlib, subprocess, sys, tempfile, warnings
warnings.simplefilter('ignore'); sys.dont_write_bytecode=True
OUT=pathlib.Path(__file__).resolve().parent
tree=(OUT/sys.argv[1]).resolve(); mode=sys.argv[2]
work=OUT/('test-'+sys.argv[1]+'-'+mode);work.mkdir(exist_ok=True)
os.environ['PYTHONDONTWRITEBYTECODE']='1';os.environ['TMPDIR']=str(work);tempfile.tempdir=str(work)
sys.path.insert(0,str(tree/'.claude/dev'))
import packet_loop_test as t
names={n for n,f in t.CASES if n.startswith(('doctrine_scan_','ac18_','ac19_')) or 'doctrine' in inspect.getsource(f)}
if mode=='cases':
    outcomes=t.chay_suite(t.CANONICAL,work/'cases',chi_chay=names)
    print('DOCTRINE',len(outcomes),'PASS',sum(v is None for v in outcomes.values()),'OTHER',{k:str(v) for k,v in outcomes.items() if v is not None},flush=True)
    extra={n for n,f in t.CASES if n.startswith('adr_song_')}|{'moc_dot_bien_phai_khop_DUNG_MOT_CHO'}
    outcomes2=t.chay_suite(t.CANONICAL,work/'extra',chi_chay=extra)
    print('ADR_AND_ANCHOR',len(outcomes2),'PASS',sum(v is None for v in outcomes2.values()),'OTHER',{k:str(v) for k,v in outcomes2.items() if v is not None},flush=True)
elif mode=='mutants':
    source=t.CANONICAL.read_text(); results={}
    for name,m in t.MUTANTS.items():
        targets=set(m[2]) & names
        if not targets:continue
        pairs=list(zip(m[0],m[1])) if isinstance(m[0],(tuple,list)) else [(m[0],m[1])]
        updated=source
        for old,new in pairs:
            assert updated.count(old)==1,(name,updated.count(old))
            updated=updated.replace(old,new,1)
        d=work/name;d.mkdir(exist_ok=True);script=d/'packet_loop.py';script.write_text(updated)
        # Dependencies are exact copies; no symlink payloads are constructed.
        for f in t.CANONICAL.parent.glob('*.py'):
            if f.name!='packet_loop.py':(d/f.name).write_bytes(f.read_bytes())
        result=t.chay_suite(script,d/'cases',chi_chay=targets)
        results[name]={n:t._phan_loai_giet(v) for n,v in result.items()}
        print(name,results[name],flush=True)
    (OUT/('mutants-'+sys.argv[1]+'.json')).write_text(json.dumps(results,ensure_ascii=False,indent=2))
    print('MUTANTS',len(results),collections.Counter(x for d in results.values() for x in d.values()),flush=True)
