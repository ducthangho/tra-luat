import json,subprocess,hashlib
from pathlib import Path
from review_measure import W,R,C,save,sha
p=W/'VERDICT.json';d=json.loads(p.read_text());a=json.loads((W/'snapshot_before.json').read_text());b=json.loads((W/'snapshot_after.json').read_text());snap={}
for k in a:
 changes=[x for x in set(a[k]['files'])|set(b[k]['files']) if a[k]['files'].get(x)!=b[k]['files'].get(x)]
 same=a[k]['git']==b[k]['git'];assert not changes and same,(k,changes,same)
 snap[k]={'files_before':len(a[k]['files']),'files_after':len(b[k]['files']),'changed_paths':changes,'git_equal':same,'head_tree':b[k]['git']['rev-parse HEAD HEAD^{tree}']['out'].splitlines()}
d['read_only_snapshot']={'scope':'Mọi file thường dưới repo và ma_r9_git trừ .git, có hash/mode; symlink có đích. Có cả ignored/untracked; Git HEAD/tree/index/diff/status đo riêng. Không chứng minh lịch sử không từng ghi rồi hoàn nguyên.','before_file':str(W/'snapshot_before.json'),'after_file':str(W/'snapshot_after.json'),'results':snap}
d['review_state']='complete'
extra='resume_real_manifest.json: thêm đối chứng bằng manifest sinh THẬT trên bản chỉ đổi docstring, runtime AST giữ nguyên. Sinh lại rc0:800 ID giống cũ nhưng800 hash nguồn khác. Chay với một kết quả cũ vẫn rc0/GIET1, hash output d71103ba… khác input07582c86…. Không cần tự đặt ID để tạo collision khi đổi head.'
d['findings'][0]['bang_chung'].insert(2,extra)
d['execution_receipts'].append({'command':['python3','-B',str(W/'resume_real_manifest.py')],'rc':0,'positive_evidence':'REAL_MANIFEST_RESUME_COMPLETE:800 same IDs/different hashes;result_sha_matches_input=false','script_sha256':sha((W/'resume_real_manifest.py').read_bytes())})
d['evidence_files']+=['resume_real_manifest.json','snapshot_after.json','kiem_verdict.txt']
d['validation_scope']['passed']=[x for x in d['validation_scope']['passed'] if not x.startswith('schema')]+['read-only snapshot đầu/cuối không delta','schema HOP_LE (§8.3):1 finding,1 lớp']
d['validation_scope']['limits'].append('Khác biệt cú pháp giữa một số toán tử và nhãn docstring được khai trong operator_audit; không suy từ tên toán tử rằng regex AST/ngữ nghĩa mọi site đã được bao phủ.')
validator=W.parent/'kiem_verdict_lop.py';cmd=['python3',str(validator),str(p),'--vong','6']
d['schema_validation']={'command':cmd,'output_file':str(W/'kiem_verdict.txt'),'meaning':'Validator chỉ kiểm schema; không chứng minh phép đo hay approval.'}
save('VERDICT.json',d)
r=subprocess.run(cmd,capture_output=True);(W/'kiem_verdict.txt').write_bytes(r.stdout+r.stderr);assert r.returncode==0,r.stdout
assert b'HOP_LE' in r.stdout
d['schema_validation'].update(rc=r.returncode,positive_evidence=r.stdout.decode().strip(),stdout_sha256=sha(r.stdout))
save('VERDICT.json',d)
# Validate the actual final bytes once more, after recording validation metadata.
r=subprocess.run(cmd,capture_output=True);(W/'kiem_verdict.txt').write_bytes(r.stdout+r.stderr);assert r.returncode==0
md=(W/'VERDICT.md').read_text()
md=md.replace('Không nhận đã chạy lại toàn bộ927.','Không nhận đã chạy lại toàn bộ927.')
md=md.replace('KET_LUAN: changes_requested','Đối chứng resume bổ sung dùng manifest sinh thật từ thay đổi chỉ ở docstring: **800 ID giữ nguyên / 800 hash thay đổi**, tool vẫn nhận một kết quả cũ sai hash. [Bằng chứng](resume_real_manifest.json).\n\nSnapshot cuối: repo **17.387** tệp, mã r9 **17.333** tệp, **0 delta** nội dung/mode/HEAD/tree/index/status so đầu. Validator rc0: **`HOP_LE (§8.3): 1 finding, 1 lop`** ([kết quả](kiem_verdict.txt)).\n\nKET_LUAN: changes_requested')
(W/'VERDICT.md').write_text(md)
files=['VERDICT.json','VERDICT.md','kiem_verdict.txt',*d['evidence_files'],'generation_receipts.json','pilot_subset_receipt.json','m1.jsonl','m2.jsonl','h.jsonl','pilot_subset.jsonl','native_target_replays.json','reconstruction_audit.json','baseline.stdout','baseline.stderr']
manifest={n:{'bytes':(W/n).stat().st_size,'sha256':sha((W/n).read_bytes())} for n in sorted(set(files))}
save('EVIDENCE_MANIFEST.json',manifest)
assert (W/'VERDICT.md').read_text().splitlines()[-1]=='KET_LUAN: changes_requested'
print(r.stdout.decode().strip());print('FINAL_ARTIFACTS',json.dumps({k:manifest[k] for k in ['VERDICT.json','VERDICT.md','kiem_verdict.txt']}));print('READ_ONLY_CHECK',json.dumps(snap))
