import hashlib, json, pathlib, re, subprocess
R=pathlib.Path(__file__).resolve().parent;root=R.parent
suite=json.loads((R/'suite.json').read_text());output=(R/'suite.stdout.txt').read_text()
assert suite['rc']==0,(suite,output[-1000:])
assert all(x in output for x in ('CA: 52/52 dat','DOT BIEN: 288/288 bi giet dung ly do','TU KIEM PHAN HANG: DAT (2 dot bien)','TONG: DAT')),output
start=json.loads((R/'snapshot-start.json').read_text());end=json.loads((R/'snapshot-end.json').read_text())
assert start['files']==end['files'],'root file content changed'
for key in ('head','tree','diff','index'):
    assert start['git'][key]==end['git'][key],key
status=subprocess.run(['git','status','--porcelain=v1','--untracked-files=all'],cwd=root,capture_output=True)
assert status.returncode==0 and not status.stdout,status.stdout
comparison={'start_count':len(start['files']),'end_count':len(end['files']),'content_equal':start['files']==end['files'],'git_identity_equal':all(start['git'][k]==end['git'][k] for k in ('head','tree','diff','index')),'status_rc':status.returncode,'status':status.stdout.decode(),'ignored_status_equal':start['git']['status']==end['git']['status']}
(R/'snapshot-comparison8.json').write_text(json.dumps(comparison,ensure_ascii=False,indent=2))
assert comparison['ignored_status_equal']
text=(R/'verdict8-template.md').read_text().replace('{{AST_TABLE}}',(R/'ast-table8.md').read_text().strip())
passed='passed, rc0: `CA: 52/52 dat`, `DOT BIEN: 288/288 bi giet dung ly do`, `TU KIEM PHAN HANG: DAT (2 dot bien)`, `TONG: DAT`.'
text=text.replace('{{SUITE_STATUS}}',passed)
snapshot=f'`snapshot-start.json` / `snapshot-end.json` / `snapshot-comparison8.json` kiểm HEAD/tree/diff/index và **{len(start["files"])} tệp tracked, untracked, ignored ngoài `.review/`** bằng nội dung/SHA-256: không có delta quan sát được; ignored status cũng bằng nhau; `git status --porcelain=v1 --untracked-files=all` rc0, output rỗng. HEAD/tree cuối vẫn đúng SHA/tree đầu verdict. Chỉ chứng minh hai mốc và phạm vi checkout được giao, không chứng minh chưa từng ghi rồi hoàn nguyên; repo nguồn ngoài checkout không thuộc phạm vi quan sát. Các writer test đã kết thúc trước manifest evidence cuối. `evidence-manifest8.json` giữ path/size/SHA-256 hiện vật ổn định, gồm verdict; không tự chứng nhận rollout hay transport sau khi run kết thúc.'
text=text.replace('{{SNAPSHOT_STATUS}}',snapshot)
assert '{{' not in text or '${{' in text
assert not any(x in text for x in ('{{AST_TABLE}}','{{SUITE_STATUS}}','{{SNAPSHOT_STATUS}}'))
(R/'VERDICT.md').write_text(text,encoding='utf-8')
files={}
for p in sorted(R.rglob('*')):
    if not p.is_file() or p.name=='evidence-manifest8.json':continue
    data=p.read_bytes();files[str(p.relative_to(R))]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
(R/'evidence-manifest8.json').write_text(json.dumps({'reviewed_sha':'431681270298ffab8edcd316bdf26670157b4b4e','files':files},ensure_ascii=False,indent=1))
print('VERDICT_FINAL',len(text.encode()),hashlib.sha256(text.encode()).hexdigest(),'artifacts',len(files))
