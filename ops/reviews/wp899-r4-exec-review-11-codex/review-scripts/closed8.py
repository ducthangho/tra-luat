import concurrent.futures, contextlib, hashlib, importlib.util, io, json, os, pathlib, random, re, subprocess, sys, time
R=pathlib.Path(__file__).resolve().parent;root=R.parent
def load():
    s=importlib.util.spec_from_file_location('test8',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t);return t
if len(sys.argv)>1 and sys.argv[1]=='child':
    t=load();t.MA=pathlib.Path(sys.argv[2]);func=sys.argv[3]
    first={'_env_chan':['c46','c29','c31','c48'], 'doc_wf':['c52','c32'], 'ghep_job':['c39','c52','c47','c48'], 'ten_du_kien':['c37','c52','c47','c48'], '_gio':['c38','c51','c49'], 'ghep_buoc':['c52','c44','c36','c37','c38','c39','c45','c48'], 'chan_buoc':['c46','c42','c31','c28','c48'], 'tach_buoc':['c52','c35','c40','c47','c48'], 'do_dau_duong':['c52','c51','c27','c46','c48']}.get(func,[])
    order=[]
    for p in first:
        order += [c for c in t.CA if c.split('_')[0]==p and c not in order]
    order += [c for c in t.CA if c not in order]
    rows=[];buf=io.StringIO()
    with contextlib.redirect_stdout(buf),contextlib.redirect_stderr(buf):
        for c in order:
            rc,d=t.chay_ca(c);rows.append([c,rc,d])
            if rc==3 and d.startswith(f'DO:{c}:'):break
    print(json.dumps({'cases':rows,'other_output':buf.getvalue()},ensure_ascii=False));sys.exit(0)
if __name__=='__main__':
    t=load();src=(root/'ops/ci_provenance.py').read_text();ds=t.sinh_dot_bien_dong(src)
    out=R/'closed8';out.mkdir(exist_ok=True)
    old=[]
    if (R/'closed8-results.json').exists():old=json.loads((R/'closed8-results.json').read_text())
    initial=re.findall(r'\[KQ\] (\S+) ([0-9a-f]{16}) (GIET|SONG|TIN_DUNG_GIA)',(root/'.review-input/dot-bien-dong-luot-dau.txt').read_text())
    frontier={m for m,_,h in initial if h!='GIET'}
    buckets={f:[] for f in t.HAM_DONG}
    for item in ds:
        if item[0] not in frontier:buckets[item[0].split('#')[0]].append(item)
    rng=random.Random(899008)
    for b in buckets.values():rng.shuffle(b)
    sample=[]
    while len(sample)<150:
        for f in t.HAM_DONG:
            if buckets[f] and len(sample)<150:sample.append(buckets[f].pop())
    requested={m for m,_ in sample}|frontier|set(t.TUONG_DUONG)
    selected=[z for z in ds if z[0] in requested]
    # Interleave functions so every function is observed early. Retain exact-source, current-run positive receipts.
    groups={f:[z for z in selected if z[0].split('#')[0]==f] for f in t.HAM_DONG};ordered=[]
    while any(groups.values()):
        for f in t.HAM_DONG:
            if groups[f]:ordered.append(groups[f].pop(0))
    hashes={m:hashlib.sha256(v.encode()).hexdigest() for m,v in ds}
    old=[z for z in old if hashes.get(z['id'])==z['source_sha256']]
    have={z['id'] for z in old};ds=[z for z in ordered if z[0] not in have]
    (R/'closed8-selection.json').write_text(json.dumps({'sample_seed':899008,'sample':[m for m,_ in sample],'initial_records':len(initial),'initial_not_killed':sorted(frontier),'equivalences':list(t.TUONG_DUONG),'requested':sorted(requested),'reuse_own_current_run':sorted(have),'remaining':[m for m,_ in ds]},ensure_ascii=False,indent=2))
    # Baseline all cases, with the repository's own runner. No resume or inherited mutant ranks.
    baseline=t._tat_ca_ca(root/'ops/ci_provenance.py');assert len(baseline)==52 and all(x[1]==0 for x in baseline),baseline
    (out/'baseline.json').write_text(json.dumps(baseline,ensure_ascii=False,indent=1))
    def one(item):
        mid,source=item;p=out/(mid.replace('#','_').replace(':','_').replace('>','')+'.py');p.write_text(source)
        cmd=[sys.executable,'-B',str(R/'closed8.py'),'child',str(p),mid.split('#')[0]];start=time.time();z=subprocess.run(cmd,capture_output=True,timeout=1800)
        log=out/(p.stem+'.json')
        try:
            val=json.loads(z.stdout);rows=val['cases'];kills=[c for c,rc,d in rows if rc==3 and d.startswith(f'DO:{c}:')]
            rank='GIET' if kills else 'TIN_DUNG_GIA' if any(rc for _,rc,_ in rows) else 'SONG'
            if not kills and len(rows)!=52:rank='HONG'
        except (ValueError,KeyError):val={};rows=[];kills=[];rank='HONG'
        detail={'id':mid,'source_sha256':hashlib.sha256(source.encode()).hexdigest(),'command':cmd,'process_rc':z.returncode,'elapsed':time.time()-start,'rank':rank,'kill_cases':kills,'stdout':z.stdout.decode('utf8','replace'),'stderr':z.stderr.decode('utf8','replace')}
        log.write_text(json.dumps(detail,ensure_ascii=False,indent=1))
        return {k:detail[k] for k in ('id','source_sha256','process_rc','elapsed','rank','kill_cases')}|{'cases_measured':len(rows),'evidence':str(log.relative_to(R))}
    results=list(old)
    with concurrent.futures.ThreadPoolExecutor(8) as ex:
        futures=[ex.submit(one,z) for z in ds]
        for future in concurrent.futures.as_completed(futures):
            v=future.result()
            results.append(v);(R/'closed8-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=1));print(v['id'],v['rank'],v['kill_cases'],flush=True)
    bad=[v for v in results if v['rank']!='GIET' and v['id'] not in t.TUONG_DUONG or v['rank']=='GIET' and v['id'] in t.TUONG_DUONG]
    print('CLOSED8',len(results),'bad',len(bad),flush=True)
    sys.exit(bool(bad))
