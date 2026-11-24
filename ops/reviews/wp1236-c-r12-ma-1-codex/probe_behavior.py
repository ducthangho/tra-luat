import sys, pathlib, json, subprocess, importlib.util, tempfile
R=pathlib.Path(__file__).resolve().parent.parent/'repo'
W=R.parent/'work'
sys.path.insert(0,str(R/'.claude/dev'));import packet_loop_test as T
s=importlib.util.spec_from_file_location('godc_probe',R/'ops/gate_output_doi_chieu.py');A=importlib.util.module_from_spec(s);s.loader.exec_module(A)
out=[]
def record(label, rc,o,e,**more):
 out.append(dict(label=label,rc=rc,stdout=o.decode(),stderr=e.decode(),**more))
def context(label):
 p=W/'probes'/label;p.mkdir(parents=True,exist_ok=True);return T.Ctx(T.CANONICAL,p)
# Use only the existing fixture's symlink, whose target is a regular sibling prov.txt.
# Add an ordinary matching provenance file; never author a new link or escape path.
def existing_fixture(w,m):
 links=T._d2b_cay(w,m)
 p=w/'ops/land/lk2-provenance'
 (p/'regular.yaml').write_bytes((p/'prov.txt').read_bytes())
 return links
c=context('existing_symlink');x=T._d1106_kho(c,o=existing_fixture)
record('baseline',*T._d1106_chay(c,x))
O=x['bb']['gate_output_nguon']['oid'];thu='ops/land/lk2-provenance';tep=thu+'/'+T._D2B_F
record('existing_yaml_symlink_with_regular_provenance',*T._d1106_chay(c,x,T._NG(tep=tep)))
# Existing fixture checkout in scratch, to compare the module with the same Git tree.
T._g(x['w'],'checkout','-q','hs')
direct=A.kiem_tep(x['w']/tep,x['w']/thu)
out.append(dict(label='same_tree_direct_validator',result=direct,mode=T._g(x['w'],'ls-tree',O,'--',thu+'/p.yaml')))
# A harmless legal path component containing a newline, copied from regular fixtures.
c=context('linebreak')
def newline_fixture(w,m):
 thu='ops/land/dong\nmoi-provenance'
 T._d2b_chep(w,m,dich=thu);T._d2b_readback(w,m,thu)
x=T._d1106_kho(c,o=newline_fixture);thu='ops/land/dong\nmoi-provenance'
record('newline_passed',*T._d1106_chay(c,x,T._NG(tep=thu+'/'+T._D2B_F)))
record('newline_waived',*T._d1106_chay(c,x,T._d2b_mien(readback_thu_muc=thu)))
# Fixture adaptation: original and rewritten heads keep K1--K8 outcomes.
c=context('fixture_equivalence');x=T._d1106_kho(c,o=T._d2b_cay)
T._g(x['w'],'checkout','-q','hs')
for thu,run in [(T._D2B_PROV,T._D2B_RUN),(T._D2B_PF,44711337223)]:
 p=f'{thu}/danh-gia-gate-output-{run}.txt'
 out.append(dict(label='fixture_equivalence',path=p,original=A.kiem_tep(R/p,R/thu),adapted=A.kiem_tep(x['w']/p,x['w']/thu),header=A.doc_danh_gia((x['w']/p).read_bytes())[0]['head'],merge=x['bb']['merge_commit']))
record('C4_exact',*T._d1106_chay(c,x,lambda bb,ls:(T._NG(tep=f'{T._D2B_PF}/danh-gia-gate-output-44711337223.txt')(bb,ls),T._CI(run_id=44711337223)(bb,ls))))
(W/'behavior.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
