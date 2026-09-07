from pathlib import Path
import subprocess,json,hashlib,datetime as dt,re
R=Path(__file__).resolve().parents[1];T=R/'cay-kho';O=R/'do-review10'
def git(*a):return subprocess.check_output(['git','-C',str(T),*a],text=True).strip()
v=(R/'VERDICT.md').read_text();pro=json.loads((R/'goi-y/hint_provenance.json').read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
result={'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'head':git('rev-parse','HEAD'),'tree':git('rev-parse','HEAD^{tree}'),'status':git('status','--porcelain'),'tracked_diff':git('diff','--stat'),'index_diff':git('diff','--cached','--stat'),'new_commits_after_reviewed':int(git('rev-list','--count','c43347d..HEAD')),'abbrev':git('config','--get','core.abbrev'),'shallow':git('rev-parse','--is-shallow-repository'),
    'verdict_sha256':sha(v.encode()),'findings':re.findall(r'^### ([a-z0-9-]+)  \[(P[123])\]',v,re.M),
    'hint_files':len(pro['files']),'hint_hunks':sum(len(f['hunks']) for f in pro['files']),
    'hint_sources_valid':all(not f['source_path'] or sha((T/f['source_path']).read_bytes())==f['source_sha256'] for f in pro['files']),
    'hint_targets_valid':all(sha((R/'goi-y/cay'/f['path']).read_bytes())==f['hint_sha256'] for f in pro['files']),
    'initial_launch_log':(R/'nhat-ky.txt').read_text()}
assert result['head']=='c43347d1e2c2f76bb21dc2d9d28bd6bfa153d355'
assert result['status']==result['tracked_diff']==result['index_diff']==''
assert result['new_commits_after_reviewed']==0
assert result['findings']==[('bia-mo-mot-ref-khong-thu-hoi-moi-ban','P1'),('manifest-luot8-liet-ke-hien-vat-khong-duoc-giao','P2')]
assert result['hint_sources_valid'] and result['hint_targets_valid']
assert 'sẽ bổ sung' not in v and 'Bản đang cập nhật' not in v
slugs=['bia-mo-mot-ref-khong-thu-hoi-moi-ban','a2-neo-nen-cu-trai-write-set-hien-tai','bien-do-khac-head-khong-phai-nhieu-runner','quyet-dinh-tiep-h-con-bi-phu-dinh','manifest-luot8-liet-ke-hien-vat-khong-duoc-giao']
result['round9_classifications']={slug:re.search(r'^- `'+slug+r'`: \*\*([^*]+)\*\*',v,re.M).group(1) for slug in slugs}
(O/'final-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
