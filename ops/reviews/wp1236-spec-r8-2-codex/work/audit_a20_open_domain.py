import copy, importlib.util, json, os, sys, tempfile, types
from pathlib import Path
W=Path(__file__).resolve().parent;R=W.parent/'repo'
sys.dont_write_bytecode=True;sys.path.insert(0,str(W))
os.environ['GATE_OUTPUT_DOI_CHIEU_GOC']=str(R);tempfile.tempdir=str(W/'tmp')
import gate_output_doi_chieu_test as t
src=(W/'gate_output_doi_chieu.py').read_text()
guard='loi += ["mien_mo_khac_1"] * (sum(m[1] is None for m in mien) != 1)'
assert src.count(guard)==1
def module(mutant=False):
    m=types.ModuleType('open_domain_review');m.__file__=str(W/'gate_output_doi_chieu.py')
    exec(compile(src.replace(guard,'pass') if mutant else src,m.__file__,'exec'),m.__dict__)
    return m
def install(m,case):
    a=copy.deepcopy(m.LUAT_v1)
    if case=='f':a['JOB_BAT_BUOC'].append(a['JOB_BAT_BUOC'][0])
    if case=='g':a['JOB_BAT_BUOC'].remove(m.CHECK_BAT_BUOC[0])
    if case=='h':a['JOB_BAT_BUOC'].append('unmatched (ubuntu-latest)')
    if case=='i':a['MUC'].append(copy.deepcopy(a['MUC'][0]))
    if case=='i_prime':a['JOB_BAT_BUOC'].remove(m.CHECK_BAT_BUOC[0])
    k=m.bam(a);m.LUAT_PHIEN_BAN={k:a};m.MIEN_HIEU_LUC={k:(1,None)}
    if case=='c':m.LUAT_PHIEN_BAN={'0'*64:a};m.MIEN_HIEU_LUC={'0'*64:(1,None)}
    if case in ('d','e','i_prime'):
        b=copy.deepcopy(m.LUAT_v1);b['ghi_chu']='v2';kb=m.bam(b)
        m.LUAT_PHIEN_BAN[kb]=b
        m.MIEN_HIEU_LUC={k:(1,10 if case=='d' else None if case=='e' else 5),kb:(6,None)}
    if case=='zero_open':m.MIEN_HIEU_LUC={k:(1,99999999999)}
    return m
text,p=t.f_ok();g=t.goc();result={}
for case in ['a','b','c','d','e','f','g','h','i','i_prime','zero_open']:
    a=install(module(),case);b=install(module(True),case)
    aa=a.kiem_so_luat();bb=b.kiem_so_luat()
    api_a=a.kiem(text,p,g);api_b=b.kiem(text,p,g)
    # The specified A20 checks only that the negative API reason contains so_luat_hong;
    # positive ledger cases require a sound ledger. No full subreason equality is specified.
    accept_a=not aa if case in ['a','b','i_prime'] else 'so_luat_hong' in api_a[1]
    accept_b=not bb if case in ['a','b','i_prime'] else 'so_luat_hong' in api_b[1]
    result[case]={'baseline_ledger':aa,'mutant_ledger':bb,'specified_case_passes':[accept_a,accept_b]}
    if case!='zero_open':assert accept_a and accept_b,(case,result[case])
assert result['zero_open']['baseline_ledger']==['mien_mo_khac_1']
assert result['zero_open']['mutant_ledger']==[]
print(json.dumps(result,ensure_ascii=False,indent=2))
(W/'a20_open_domain.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
