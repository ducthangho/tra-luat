import ast,collections,importlib.util,json,os,subprocess,sys
from review_measure import W,R,C,save,sha
src=(C/'ops/gate_output_doi_chieu.py').read_text();d=R/'ops/reviews/wp1236-r10-soan';pairs=[json.loads(x) for x in (d/'kho_dot_bien_reviewer_luot6.jsonl').read_text().splitlines()]
# Format-only copy is the same AST. No gate logic or test oracle is modified.
formatted=ast.unparse(ast.parse(src));dest=W/'formatted_original.py';dest.write_text(formatted)
cmd=[sys.executable,'-B',str(d/'quet_dot_bien.py'),'hoi-quy',str(d/'kho_dot_bien_reviewer_luot6.jsonl'),'-',str(dest),'--ra',str(W/'formatted_h.jsonl')]
p=subprocess.run(cmd,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(W/'tmp')),cwd=W)
rows=[json.loads(x) for x in (W/'formatted_h.jsonl').read_text().splitlines()]
# Compare original AST and emitted source after any successful application; never count a substring hit alone as semantic validity.
base=ast.dump(ast.parse(src),include_attributes=False)
app=[x for x in rows if 'src' in x]
out={'command':cmd,'rc':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode(),'format_only_ast_equal':base==ast.dump(ast.parse(formatted),include_attributes=False),'pairs':len(pairs),'whole_file_anchors':sum(x['cu']==src for x in pairs),'anchor_over_100_lines':sum(len(x['cu'].splitlines())>100 for x in pairs),'applied':len(app),'not_applicable':len(rows)-len(app),'missing_ids':[x['id'] for x in rows if 'src' not in x],'replacement_source_ast_equal_old_mutant':{x['id']:ast.dump(ast.parse(x['src']),include_attributes=False)==ast.dump(ast.parse(next(y for y in map(json.loads,(W/'h.jsonl').read_text().splitlines()) if y['id']==x['id'])['src']),include_attributes=False) for x in app}}
save('regression_portability.json',out);print('REGRESSION_PORTABILITY_COMPLETE',json.dumps({k:v for k,v in out.items() if k not in ['missing_ids','replacement_source_ast_equal_old_mutant']},ensure_ascii=False))
