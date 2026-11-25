import ast,json,os,subprocess,sys,time
from review_measure import W,R,C,save,sha
D=R/'ops/reviews/wp1236-r10-soan'; Q=D/'quet_dot_bien.py'; src=(C/'ops/gate_output_doi_chieu.py').read_text()
# Harmless documentation-only change: same line count and all runtime statements unchanged.
lines=src.splitlines(keepends=True);assert lines[1].startswith('"""');lines[1]=lines[1].rstrip('\n')+' [Đối chứng nguồn mới của reviewer.]\n';doccopy=''.join(lines)
a,b=ast.parse(src),ast.parse(doccopy);a.body=a.body[1:];b.body=b.body[1:];assert ast.dump(a)==ast.dump(b)
p=W/'doc_only_original.py';p.write_text(doccopy);env=dict(os.environ,TMPDIR=str(W/'tmp'),PYTHONDONTWRITEBYTECODE='1')
cmd=[sys.executable,'-B',str(Q),'sinh',str(p),'--ra',str(W/'doc_only_m.jsonl')];r=subprocess.run(cmd,capture_output=True,env=env,cwd=W);assert r.returncode==0
new={x['id']:x for x in map(json.loads,(W/'doc_only_m.jsonl').read_text().splitlines())};old={x['id']:x for x in map(json.loads,(W/'m1.jsonl').read_text().splitlines())}
k=next(x for x in map(json.loads,(D/'pilot_c2d606b_kq.jsonl').read_text().splitlines()) if x['id'] in new and x['giet'])
(W/'doc_only_subset.jsonl').write_text(json.dumps(new[k['id']])+'\n');(W/'doc_only_kq.jsonl').write_text(json.dumps(k)+'\n')
cmd2=[sys.executable,'-B',str(Q),'chay',str(W/'doc_only_subset.jsonl'),str(C/'ops/gate_output_doi_chieu_test.py'),'--ra',str(W/'doc_only_kq.jsonl'),'--song-song','1'];r2=subprocess.run(cmd2,capture_output=True,env=env,cwd=W)
result=json.loads((W/'doc_only_kq.jsonl').read_text());out={'only_docstring_changed':True,'runtime_ast_equal':True,'generator_command':cmd,'generator_rc':r.returncode,'generator_stdout':r.stdout.decode(),'same_ids':set(old)==set(new),'same_id_different_sha_count':sum(old[k]['sha256']!=new[k]['sha256'] for k in new),'run_command':cmd2,'run_rc':r2.returncode,'stdout':r2.stdout.decode(),'result':result,'input_sha256':new[k['id']]['sha256'],'result_sha_matches_input':result['sha256']==new[k['id']]['sha256']}
save('resume_real_manifest.json',out);print('REAL_MANIFEST_RESUME_COMPLETE',json.dumps({k:v for k,v in out.items() if k not in ['generator_command','run_command']},ensure_ascii=False))
