import ast, collections, difflib, hashlib, json, pathlib, re, shutil, subprocess
import yaml
from run_checks import ROOT,OUT,run
RAW=pathlib.Path('/tmp/do650')
prov=ROOT/'ops/land/pr666-wp650-provenance.yaml'
land=ROOT/'ops/land/pr666-wp650-land-evidence.yaml'
err=ROOT/'ops/specs/LAND-DOC-RECEIPT-THU-HOI-C1a1a-r5.ERRATA.md'
v=yaml.safe_load(prov.read_bytes()); l=yaml.safe_load(land.read_bytes())
old=lambda p: subprocess.check_output(['git','show','d535cf6:'+str(p.relative_to(ROOT))],cwd=ROOT).decode()
src=(ROOT/'ops/land/pr666-wp650-provenance/doi_chieu_buoc.py').read_text()
# Lượt 1 N1: exact skip text + same AST functions; order of the YAML list is immaterial.
lines=(RAW/'log-108815209421.txt').read_text().splitlines()
reasons=[x.split(' BO QUA ',1)[1] for x in lines if re.match(r'^\S+Z +BO QUA [A-Za-z0-9_]+:',x)]
assert len(reasons)==17 and collections.Counter(reasons)==collections.Counter(v['windows_bo_qua']['ca'])
assert len(set(reasons))==17 and v['windows_bo_qua']['so_ca']==17
old_note=yaml.safe_load(old(prov))['bon_moc'][2]['gate_output'][0]['ghi_chu']
new_note=v['bon_moc'][2]['gate_output'][0]['ghi_chu']
print('N1_WINDOWS_REASONS_EXACT=17/17; old_false_classification='+str('la ca chi-Linux' in old_note)+'; current_false_classification='+str('la ca chi-Linux' in new_note))
for n,x in enumerate(lines,1):
    if ' BO QUA ' in x or '172/172 ca DA CHAY QUA' in x: print(f'WINDOWS_LOG:{n}: '+x.split('Z ',1)[1])
code=subprocess.check_output(['git','show','f8a7829:.claude/dev/launcher_test.py'],cwd=ROOT,text=True)
for fn in ast.parse(code).body:
    if isinstance(fn,ast.FunctionDef) and fn.name.startswith(('t28_','t50_')):
        print('AST_SOURCE',fn.name,'line='+str(fn.lineno))
        for n in ast.walk(fn):
            if isinstance(n,ast.Return) and isinstance(n.value,ast.Constant) and isinstance(n.value.value,str): print('AST_SKIP_REASON',n.value.value)
# N2: same ref-discrimination measurement as r1.
assert src.count("'f8a7829:'+p")==1
alt=OUT/'doi_chieu_base_definition.py'; alt.write_text(src.replace("'f8a7829:'+p","'ceb1a3f:'+p"))
p=run('alternative-source-commit',['python3','-B',str(alt)]); assert p.returncode==0
assert json.loads(p.stdout)==json.loads((OUT/'doi-chieu-baseline.stdout').read_bytes())
print('N2_DEFINITION_REF_DISCRIMINATION: f8a7829 vs ceb1a3f; JSON_EQUAL=True; all_in_order=10/10 both')
for entry in v['bon_moc']:
    w=entry['workflow_definition']; assert w['commit_nguon_chinh_xac']=='not_measured'; assert 'commit' not in w and 'trang_thai' not in w
    print('N2_WORKFLOW_CURRENT',entry['run']['id'],'bytes='+w['bytes'],'commit_nguon_chinh_xac='+w['commit_nguon_chinh_xac'])
print('N2_SUMMARY_SCOPE:')
for n,x in enumerate(land.read_text().splitlines(),1):
    if 150<=n<=159: print(f'{land.relative_to(ROOT)}:{n}: {x}')
print('N2_BROAD_SUMMARY_REMAINS='+str('bon moc da do tu log/artifact/REST' in l['provenance_ghi_chu']))
# N3 same old status string, now explicitly anchored in historical erratum.
print('N3_OLD_UNANCHORED='+str('Trạng thái packet là\n`merged`, CHƯA `landed`' in old(err)))
print('N3_CURRENT_UNANCHORED='+str('Trạng thái packet là\n`merged`, CHƯA `landed`' in err.read_text()))
assert 'Lúc ghi erratum này (PR #667)' in err.read_text()
assert 'trạng thái HIỆN HÀNH xem' in err.read_text()
assert l['trang_thai_packet']['landed'] is True and 'merge commit cua PR' in l['trang_thai_packet']['landed_hieu_luc_tu']
print('N3_CURRENT_HISTORICAL_ANCHOR=True; landed_effective_on_merge=True')
for n,x in enumerate(err.read_text().splitlines(),1):
    if 15<=n<=17: print(f'{err.relative_to(ROOT)}:{n}: {x}')
# Own r2 mutant: alter just the ANSI body for Windows launcher test invocation.
mut=OUT/'r2-windows-mutant'; mut.mkdir(exist_ok=True)
for pth in RAW.glob('log-*.txt'): shutil.copyfile(pth,mut/pth.name)
target='108815209421'; path=mut/f'log-{target}.txt'; b=path.read_bytes()
needle=b'\x1b[36;1mpython .claude/dev/launcher_test.py\x1b[0m'
assert b.count(needle)==1
path.write_bytes(b.replace(needle,b'\x1b[36;1mpython .claude/dev/launcher_test.py --reviewer-r2-mutant\x1b[0m'))
mut_script=OUT/'doi_chieu_r2_windows_mutant.py'; mut_script.write_text(src.replace('/tmp/do650/',str(mut)+'/'))
p=run('r2-windows-mutant',['python3','-B',str(mut_script)]); d=json.loads(p.stdout)
assert p.returncode==0 and d[target]['all_in_order'] is False and d[target]['runs_in_log']==11
assert hashlib.sha256((RAW/path.name).read_bytes()).hexdigest()==hashlib.sha256(b).hexdigest()
print('R2_OWN_MUTANT',json.dumps(d[target]),'original_log_unchanged=True')
# Scan all current prose, not just the patched lines; output is navigation, not a semantic validator.
scan=[]
for pth in (prov,land,err):
    for n,x in enumerate(pth.read_text().splitlines(),1):
        if re.search(r'workflow|definition|measured|moc|do duoc|da do|land|merge|skipp|BO QUA|chi-Linux|CHƯA|đã đo|Windows',x,re.I): scan.append(f'{pth.relative_to(ROOT)}:{n}: {x}')
(OUT/'claims-scan.txt').write_text('\n'.join(scan)+'\n')
print('CLAIMS_SCAN',len(scan),'lines; all three files read in full')
# Prior review artifacts preserved byte-for-byte; surrounding transport wrapper is separate.
for target,source in [('luot1-verdict-day-du.md','VERDICT.md'),('luot1-audit_facts.py','audit_facts.py'),('luot1-audit_extra.py','audit_extra.py'),('luot1-mutations.py','mutations.py'),('luot1-reproduce_findings.py','reproduce_findings.py')]:
    a=(ROOT/'ops/reviews/bookkeeping-650-pr670'/target).read_bytes(); b=(pathlib.Path('/tmp/review670-r1-output')/source).read_bytes(); assert a==b
    print('R1_ARTIFACT_BYTE_EXACT',target,len(a),hashlib.sha256(a).hexdigest())
print('ROUND2_FACT_MEASUREMENTS_COMPLETE')
