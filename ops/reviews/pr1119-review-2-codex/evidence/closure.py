from common import *
import yaml
oldrev='a8f7470';stem='pr1114-review-1-codex';path='ops/reviews/'+stem+'/OMITTED.txt'
old=git('show',oldrev+':'+path).decode();new=(R/path).read_text();cache=[]
for p in sorted((S/'nguon/review1114a/evidence/ruff-cache-created').rglob('*')):
    if not p.is_file():continue
    rel=p.relative_to(S/'nguon/review1114a').as_posix();raw=p.read_bytes();line=f'{rel}\tsha256 {digest(raw)}\tbytes {len(raw)}\t'
    cache.append(dict(source=rel,sha256=digest(raw),bytes=len(raw),old_declared=line in old,new_declared=line in new,absent_from_archive=not(R/'ops/reviews'/stem/rel).exists()))
diffs=[]
for turn,src in [(1,'review1114a'),(2,'review1114b')]:
    stem=f'pr1114-review-{turn}-codex';path=f'ops/reviews/{stem}-verdict.receipt.yaml'
    od=yaml.safe_load(git('show',oldrev+':'+path));nd=yaml.safe_load((R/path).read_text())
    oc=next(c['mo_ta'] for c in od['verdict_usage_caveats'] if c['id']=='TEP-LON-KHONG-VAO-KHO');nc=next(c['mo_ta'] for c in nd['verdict_usage_caveats'] if c['id']=='TEP-LON-KHONG-VAO-KHO')
    raw=(R/'ops/reviews'/stem/'DIFF.patch').read_bytes();diffs.append(dict(stem=stem,old_claim=oc,new_claim=nc,bytes=len(raw),sha256=digest(raw),equal_source=raw==(S/'nguon'/src/'DIFF.patch').read_bytes(),manifest_has_diff='./DIFF.patch' in (R/'ops/reviews'/stem/'SHA256SUMS').read_text(),new_claims_present='DIFF.patch CO trong kho.' in nc,readme_same=f'| `{stem}-verdict.md` | `TEP-LON-KHONG-VAO-KHO` | {nc} |' in (R/'ops/reviews/README.md').read_text()))
data=dict(cache=cache,diffs=diffs,old_missing=sum(not c['old_declared'] for c in cache),new_missing=sum(not c['new_declared'] for c in cache))
save('closure.json',data);print(json.dumps(data,ensure_ascii=False,indent=2))
assert len(cache)==3 and data['old_missing']==3 and data['new_missing']==0
assert all(d['equal_source'] and d['manifest_has_diff'] and d['new_claims_present'] and d['readme_same'] for d in diffs)
note('ĐỐI CHIẾU LƯỢT TRƯỚC — `PYTHONDONTWRITEBYTECODE=1 python3 closure.py`: `bo-sot-cache-khong-khai`: ĐÃ VÁ THẬT, khai cache đúng 0/3 → 3/3; `caveat-loai-diff-sai`: ĐÃ VÁ THẬT, cả hai caveat/README nay ghi DIFF.patch có trong kho; tự băm hai DIFF 1913/4160 bytes khớp nguồn và manifest. Chi tiết trước/sau `evidence/closure.json`. Phép byte toàn tập và cổng/delta ở trên không phát hiện lỗi mới từ bản vá.')
