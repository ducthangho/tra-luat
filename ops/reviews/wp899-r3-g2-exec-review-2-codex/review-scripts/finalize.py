import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent
a=json.loads((R/'snapshot-start.json').read_text()); b=json.loads((R/'snapshot-end.json').read_text())
delta=[k for k in sorted(set(a['files'])|set(b['files'])) if a['files'].get(k)!=b['files'].get(k)]
def norm(c):
    v=dict(c)
    if c['command']==['git','ls-files','--others','--ignored','--exclude-standard']:
        v['stdout']=''.join(line+'\n' for line in c['stdout'].splitlines() if not line.startswith('.review/'))
    return v
an=[norm(c) for c in a['commands']]; bn=[norm(c) for c in b['commands']]
raw_added=sorted(set(b['commands'][-1]['stdout'].splitlines())-set(a['commands'][-1]['stdout'].splitlines()))
raw_removed=sorted(set(a['commands'][-1]['stdout'].splitlines())-set(b['commands'][-1]['stdout'].splitlines()))
comp={'start_files':len(a['files']),'end_files':len(b['files']),'file_deltas':delta,
      'git_raw_commands_identical':a['commands']==b['commands'],'git_commands_identical_excluding_review_artifact_paths':an==bn,
      'expected_ignored_artifact_paths_added':raw_added,'expected_ignored_artifact_paths_removed':raw_removed}
(R/'snapshot-comparison.json').write_text(json.dumps(comp,ensure_ascii=False,indent=2)+'\n')
assert not delta and an==bn
assert all(x.startswith('.review/') for x in raw_added+raw_removed)
text=(R/'VERDICT.md').read_text()
if '**Snapshot cuối.**' not in text:
    with (R/'VERDICT.md').open('a') as f:
        f.write(f'\n**Snapshot cuối.** snapshot-start.json/snapshot-end.json/snapshot-comparison.json so hash/size **{len(a["files"]):,} tệp** ngoài `.git/` và `.review/`, gồm ignored/untracked, `.review-input/` và `.codex/`: **0 delta**. HEAD/tree giữ exact OID đầu verdict; Git status không ignored, diff, cached diff và untracked không ignored rỗng, rc0. Raw danh sách ignored thay đổi do hiện vật được tạo trong `.review/`; sau loại đúng prefix output này, các kết quả Git đầu/cuối bằng nhau. Ignored ngoài output vẫn là `.codex/` và `.review-input/`, không có delta nội dung. `.git/` không băm toàn metadata, kiểm qua HEAD/tree/index/diff/status. Hai snapshot chỉ chứng minh không có delta quan sát tại hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. Không có repository nguồn bên ngoài được cấp/quan sát.\n')
p=R/'VERDICT.md'; text=p.read_text()
assert text.splitlines()[:4]==['verdict: changes_requested','reviewed_sha: 7f5a02c9c2ff346484e10c2f5b4e94fcb0468b8b','base_sha: dc657149941f9db3ab2afc6fb6462ba4827bf18f','Reviewed commit: 7f5a02c9c2ff346484e10c2f5b4e94fcb0468b8b']
assert all(f'| A{i}' in text for i in range(1,20)) and all(f'F{i:02}' in text for i in range(1,9))
assert 'pending' not in text
assert '| lớp | hạng | biểu hiện (tệp:dòng) | phép đo tái hiện | HINT patch | ước lượng dòng |' in text
mut=json.loads((R/'mutants/results.json').read_text()); assert len(mut)==76
assert all(x['baseline']['rc']==0 for x in mut)
for x in mut:
    if x['rank']=='GIET': assert x['mutant']['rc']==3 and f'DO:{x["case"]}:' in x['mutant']['output']
rev=json.loads((R/'review-cases.json').read_text()); assert all(z['rc']==0 for z in rev if 'mutant' not in z)
compare=json.loads((R/'r4-comparison.json').read_text()); assert all(z['gate']['trang_thai']=='not_measured' for z in compare.values() if 'gate' in z)
checks={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'verdict':'changes_requested','snapshot_delta':len(delta),'file_count':len(a['files'])}
(R/'final-artifact.json').write_text(json.dumps(checks,indent=2)+'\n'); print(json.dumps(checks))
print('probe exceptions',[(k,v['exception']) for k,v in json.loads((R/'probes.json').read_text()).items() if 'exception' in v])
