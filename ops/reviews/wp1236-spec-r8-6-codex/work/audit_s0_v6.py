"""Read-only audit. The wrapper only counts calls and preserves all return values."""
import ast, collections, hashlib, importlib.util, inspect, json, pathlib, re, sys, unicodedata
W=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(W))
import gram, khoa_ast_r8 as k, probes_r8 as p, sinh_r8 as s

def load(name,source):
    path=W/(name+'.py'); path.write_text(source,encoding='utf-8')
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

# Ordinary transparent instrumentation: no normalization, no changed decisions.
transparent='''
import functools
_original = cu_phap_run
_calls = 0

def counted(run, shell):
    global _calls
    _calls += 1
    return _original(run, shell)

cu_phap_run = functools.update_wrapper(counted, _original)
'''
m=load('transparent_counted',k.GOC+transparent)
result={}
result['transparent_wrapper_s0_1_to_4']=k.kiem_s0_v5(k.GOC+transparent)
f=m.cu_phap_run
result['getsource_f_equals_original']=inspect.getsource(f)==inspect.getsource(m._original)
result['getsource_code_equals_original']=inspect.getsource(f.__code__)==inspect.getsource(m._original)
result['call_before']={'result':f('python ops/x.py',None),'counter':m._calls}
records=[]
m.cu_phap_run=lambda run,shell: records.append((run,shell))
for run in k.VE_GIAN_DIEP:
    for sh in (None,'bash'): m.cu_phap_run(run,sh)
result['spy']={'calls':len(records),'counter_after':m._calls,'all_arguments_preserved':records==[(run,sh) for run in k.VE_GIAN_DIEP for sh in (None,'bash')]}
result['v4_variants_under_v5']={n:k.kiem_s0_v5(src) for n,(src,_) in k.BIEN_THE.items()}
corpus=[(run,sh) for body in s.kho() for sh in s.SHELL for run in (body,body+'\n')]
sample=[x for i,x in enumerate(corpus) if i%299==0]
result['sample']={'corpus':len(corpus),'n':len(sample),'shell':dict(collections.Counter(str(sh) for _,sh in sample)), 'accepted':sum(gram.cp(*x) is None for x in sample),'S3b_total':len(p.AM)+len(p.DUONG)+len(sample)}
# Compare inputs, without constructing a modified validator.
inputs=list(p.AM.values())+list(p.DUONG.values())
inputs=[tuple(x[:2]) for x in inputs]
result['table_n']=len(inputs)
result['NFC_changed_table']=sum(unicodedata.normalize('NFC',x)!=x for x,_ in inputs if type(x) is str)
result['NFC_changed_generated']=sum(unicodedata.normalize('NFC',x)!=x for x,_ in corpus)
kelvin='python ops/\u212a.py\n'
result['Kelvin_input_analysis']={'reference':gram.cp(kelvin,None),'NFC_then_reference':gram.cp(unicodedata.normalize('NFC',kelvin),None),'UTF8_differs':kelvin.encode()!=unicodedata.normalize('NFC',kelvin).encode()}
result['counts']={'KT':len(s.KT),'seeds':len(s.LENH)+len(s.LENH)**2+len(s.LENH),'pipe_insertions':len(s.chen('python ops/m.py w')),'sampled_pipe_insertions':sum(i%3==0 for i,_ in enumerate(s.chen('python ops/m.py w')))}
print(json.dumps(result,ensure_ascii=False,indent=2))
(W/'audit_s0_v6.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
