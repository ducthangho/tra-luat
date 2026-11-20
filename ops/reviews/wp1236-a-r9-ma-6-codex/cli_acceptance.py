import pathlib,importlib.util,json,sys
w=pathlib.Path(__file__).resolve().parent;r=w.parent/'repo';s=importlib.util.spec_from_file_location('tests',r/'ops/gate_output_doi_chieu_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
calls=[];original=t.cli
def wrap(*a):
 rc,ra=original(*a);calls.append({'args':a,'rc':rc,'output':ra});return rc,ra
t.cli=wrap;rc,msg=t.chay_ca('a210_cli');p=r/'ops/land/pr1130-wp1122-provenance/danh-gia-gate-output-41365578430.txt';c=original('kiem-tep',str(p),'--provenance',str(p.parent))
result={'test_rc':rc,'test_message':msg,'calls':calls,'sixth_fixture_called':any(str(p) in x['args'] for x in calls),'sixth_cli_rc':c[0],'sixth_cli_output':c[1]};(w/'cli_acceptance.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print('a210_rc',rc,'real_fixtures',len([x for x in calls if x['args'][0]=='kiem-tep' and '/ops/land/' in x['args'][1]]),'sixth_called',result['sixth_fixture_called'],'sixth_direct_rc',c[0]);sys.exit(rc)
