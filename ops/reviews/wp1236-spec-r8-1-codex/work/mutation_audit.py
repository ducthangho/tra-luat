import json,pathlib,sys
BASE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/'artifacts'))
sys.dont_write_bytecode=True
import gram, probes_r8 as p, dot_bien_r8 as d
bad=[]
for label,(f,target) in d.DB.items():
    if not(gram.cp(*p.AM[target]) is not None and f(*p.AM[target]) is None):bad.append(label)
f=d.dung(phai_ong=gram.W)
prime=[n for n,c in p.DUONG.items() if f(*c) is not None]
def swapped(run,shell):
    if shell not in (None,'bash','sh'):return 'shell_ngoai_cu_phap'
    return gram.cp(run,shell)
corpus={**p.AM,**p.DUONG}
result={'mutants':len(d.DB),'not_killed':bad,'m_S12_prime_positive_failures':prime,
        'order_mutation_original_98_cases_different':[n for n,c in corpus.items() if gram.cp(*c)!=swapped(*c)],
        'order_counterexample':{'input':[None,'pwsh'],'original':gram.cp(None,'pwsh'),'swapped':swapped(None,'pwsh')}}
(BASE/'mutation_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False,indent=2))
