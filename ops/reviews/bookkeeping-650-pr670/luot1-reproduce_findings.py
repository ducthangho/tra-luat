import ast, hashlib, json, pathlib, re, subprocess
import yaml
from run_checks import ROOT, OUT, run
prov=ROOT/'ops/land/pr666-wp650-provenance.yaml'; land=ROOT/'ops/land/pr666-wp650-land-evidence.yaml'
v=yaml.safe_load(prov.read_bytes()); l=yaml.safe_load(land.read_bytes())
src=(ROOT/'ops/land/pr666-wp650-provenance/doi_chieu_buoc.py').read_text()
alt=OUT/'doi_chieu_base_definition.py'; alt.write_text(src.replace("'f8a7829:'+p", "'ceb1a3f:'+p"))
p=run('alternative-source-commit',['python3','-B',str(alt)]); d=json.loads(p.stdout)
baseline=json.loads((OUT/'doi-chieu-baseline.stdout').read_text())
assert d==baseline
print('DEFINITION_COMMIT_DISCRIMINATION')
print('defined_source=f8a7829 vs defined_source=ceb1a3f: JSON_EQUAL=True; all_in_order=10/10 both')
for c in ('ceb1a3f','bf63bb1','511612f','f8a7829'):
    oid=subprocess.check_output(['git','rev-parse',c],cwd=ROOT,text=True).strip()
    blobs=[subprocess.check_output(['git','rev-parse',c+':'+path],cwd=ROOT,text=True).strip() for path in ('.github/workflows/ci.yml','.github/workflows/launcher-windows.yml')]
    print(oid,*blobs)
print('DECLARED_EXACT_WORKFLOW_COMMITS',[(x['run']['id'],x['workflow_definition']['commit'],x['workflow_definition']['trang_thai']) for x in v['bon_moc']])
log=pathlib.Path('/tmp/do650/log-108815209421.txt').read_text().splitlines()
print('WINDOWS_SKIP_CLAIM',v['bon_moc'][2]['gate_output'][0]['ghi_chu'])
for i,x in enumerate(log,1):
    if (' BO QUA ' in x and any(k in x for k in ('t03_','t28_','t50_','t76_'))) or '172/172 ca DA CHAY QUA' in x:
        print(f'log-108815209421.txt:{i}: {x}')
code=subprocess.check_output(['git','show','f8a7829:.claude/dev/launcher_test.py'],cwd=ROOT,text=True)
lines=code.splitlines(); tree=ast.parse(code)
for fn in tree.body:
    if isinstance(fn,ast.FunctionDef) and fn.name.startswith(('t28_','t50_')):
        print(f'CHECKED_SOURCE f8a7829:.claude/dev/launcher_test.py:{fn.lineno} '+fn.name)
        for node in ast.walk(fn):
            if isinstance(node,ast.Return) and isinstance(node.value,ast.Constant) and isinstance(node.value.value,str): print('SKIP_REASON',node.value.value)
err=ROOT/'ops/specs/LAND-DOC-RECEIPT-THU-HOI-C1a1a-r5.ERRATA.md'
print('CONFLICTING_STATUS')
for path,ranges in [(land,[(27,41)]),(err,[(15,17)])]:
    for n,line in enumerate(path.read_text().splitlines(),1):
        if any(a<=n<=b for a,b in ranges): print(f'{path.relative_to(ROOT)}:{n}: {line}')
assert l['trang_thai_packet']['landed'] is True
assert 'Trạng thái packet là\n`merged`, CHƯA `landed`' in err.read_text()
print('UNQUALIFIED_ERRATUM_CONFLICT=True')
print('OLD_NOT_MEASURED_NOTE',l['provenance_ghi_chu'])
