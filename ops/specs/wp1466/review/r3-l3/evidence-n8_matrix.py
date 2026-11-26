from pathlib import Path
import ast,subprocess,sys
O=Path(__file__).resolve().parent;P=O/'prototype';D=O/'n8-matrix';D.mkdir(exist_ok=True)
srcs={m:(P/'.claude/dev'/f).read_text() for m,f in [('ma','packet_loop.py'),('test','packet_loop_test.py')]}
def add_to_function(s,name,tail=False):
 n=next(n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef) and n.name==name)
 lines=s.splitlines(keepends=True);idx=n.end_lineno if tail else n.body[0].end_lineno
 lines.insert(idx,'    pass\n');return ''.join(lines)
def check(name,mode,s):
 p=D/(name+'.py');p.write_text(s)
 r=subprocess.run([sys.executable,'-B',str(O/'n8_spec.py'),mode,str(O/('base-packet_loop.py' if mode=='ma' else 'base-packet_loop_test.py')),str(p)],capture_output=True,text=True)
 print(name,mode,'rc',r.returncode,r.stdout.strip().replace('\n',' | '),flush=True);return r.returncode
code=srcs['ma'];test=srcs['test'];start='INV_KHOA_PROTOCOL = ('
rows=[('ma_tail_boundary','ma',add_to_function(code,'_doc_nguon_protocol',True)),('ma_adr_song','ma',add_to_function(code,'cmd_adr_song')),('ma_doctrine_tail','ma',add_to_function(code,'cmd_doctrine_scan',True)),('ma_rebind','ma',code.replace(start,'RC_ADR = 9\n'+start,1)),('ma_other_function','ma',code.replace(start,'def review_note():\n    pass\n\n'+start,1)),('ma_anonymous','ma',code.replace(start,'pass\n'+start,1))]
# Chú thích giữa hai hàm cũ và chú thích trong thân cũ.
a=next(n for n in ast.parse(code).body if isinstance(n,ast.FunctionDef) and n.name=='_doc_nguon_protocol');lines=code.splitlines(keepends=True);lines.insert(a.lineno-1,'# reviewer comment outside inserted module block\n');rows.append(('ma_detached_comment','ma',''.join(lines)))
lines=code.splitlines(keepends=True);lines.insert(a.end_lineno-1,'    # reviewer comment inside old function\n');rows.append(('ma_old_comment','ma',''.join(lines)))
fn=next(n.name for n in ast.parse(test).body if isinstance(n,ast.FunctionDef) and n.name.startswith('case_'))
rows.append(('test_old_case','test',add_to_function(test,fn,True)))
n=next(n for n in ast.parse(test).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='MUTANTS' for t in n.targets));lines=test.splitlines(keepends=True);lines.insert(n.lineno,'    # reviewer comment changes old mutant node bytes\n');rows.append(('test_old_mutant','test',''.join(lines)))
rows.extend([('test_repo_gia','test',add_to_function(test,'_repo_gia')),('test_rebind','test',test.replace('_PROTO_CO_KHOA: list = []','_doi = _doi\n_PROTO_CO_KHOA: list = []',1))])
rcs=[check(*r) for r in rows];print('NEGATIVE_MATRIX',len(rcs),sum(x!=0 for x in rcs),flush=True)
pos=[('positive_ma','ma',code.replace(start,'INV_REVIEW_NOTE = 9\n'+start,1)),('positive_test','test',test.replace('_PROTO_CO_KHOA: list = []','_REVIEW_NOTE = 9\n_PROTO_CO_KHOA: list = []',1))]
r=[check(*x) for x in pos];print('POSITIVE_MATRIX',len(r),sum(x==0 for x in r),flush=True)
