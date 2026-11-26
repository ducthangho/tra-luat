import pathlib,subprocess,importlib.util,sys,json,os
R=pathlib.Path(__file__).resolve().parent.parent/'repo';W=R.parent/'work';sys.path.insert(0,str(R/'.claude/dev'))
out=[]
for label in ['base','head']:
 d=W/'legacy'/label;d.mkdir(parents=True,exist_ok=True)
 for n in ['packet_loop.py','packet_loop_test.py','launcher.py']:
  (d/n).write_bytes(subprocess.check_output(['git','show','f602325:.claude/dev/'+n]) if label=='base' else (R/'.claude/dev'/n).read_bytes())
 sp=importlib.util.spec_from_file_location('legacy_'+label,d/'packet_loop_test.py');T=importlib.util.module_from_spec(sp);sp.loader.exec_module(T);T.ROOT=R
 cases={n for n,_ in T.CASES if n=='cong_c_dong_du' or n.startswith(('cong_c_d1_','cong_c_d2_','cong_c_d3_','cong_c_d4_'))}
 result=T.chay_suite(T.CANONICAL,d/'tmp',chi_chay=cases)
 out.append({'label':label,'cases':{k:str(v) if v is not None else None for k,v in result.items()},'passed':sum(v is None for v in result.values()),'total':len(result)})
 print(label,out[-1],flush=True)
(W/'legacy_ab.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
raise SystemExit(any(x['passed']!=x['total'] for x in out))
