from measure import *
lines=[]
# Check fixed historical snapshots against immutable graph targets, not against floating master.
for source,target in [('bc57bca','423b4ba'),('cc78b33','3ddda02'),('cc78b33','refs/remotes/origin/ops/cap-lease-ci-g5-cong-cu-chia-manh')]:
 p=subprocess.run(['git','-C',str(ROOT),'merge-base','--is-ancestor',source,target],capture_output=True,text=True);lines.append(f'git merge-base --is-ancestor {source} {target} rc={p.returncode} stderr={p.stderr.strip()!r}')
# Sidecars are the correction source for frozen bytes. No mutations of the historical receipts.
for f in ['pr896-review-4-legacy-caveats.yaml','pr896-review-6-legacy-caveats.yaml']:
 d=yaml.safe_load((ROOT/'ops/reviews'/f).read_text())
 for c in d['caveats']:
  if 'ANCESTRY' not in c['id']:continue
  rows=[l for l in (ROOT/'ops/reviews/README.md').read_text().splitlines() if l.startswith('| `'+Path(c['verdict_path']).name+'` | `'+c['id']+'` |')];desc=c['mo_ta'];lines.append(f'{f} => {Path(c["receipt_path"]).name} README rows={len(rows)} exact_description={len(rows)==1 and desc in rows[0]}')
# Existing no-review claim is about an independent rereview, which the stored human decision disclaims.
p='ops/land/pr714-wp710-provenance/readback-comment-6080353250.json';d=json.loads((ROOT/p).read_text());body=d.get('body','');lines.append(f'{p}: created_at={d.get("created_at")} body_sha256={hashlib.sha256(body.encode()).hexdigest()}')
for l in body.splitlines():
 if any(t in l for t in ['Reviewed commit','dò tìm','delta','review','VERDICT']):lines.append(l)
# Historical summary is not falsely read as a current assertion.
land=yaml.safe_load((ROOT/'ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-land-evidence.yaml').read_text());last=land['cap_nhat_20261026_luot7']['cross_review_moi'];lines.append(f'new land block reviewed_sha={last["reviewed_sha"]} verdict={last["verdict"]} score={last["so_lop"]}; con P1/P2 describes that historical review, with hint applied in same block')
# Distinguish paraphrase from a requirement to preserve historical verdict bytes.
fields=json.loads((OUT/'historical-anchors.json').read_text())['fields'];notexact=[x for x in fields if not x['text_matches']];lines.append(f'historical_descriptions_not_verbatim={len(notexact)}; {sum(x["path"].split("/")[-1].startswith("wp678-spec-review") for x in notexact)} wp678, {sum("pr508-review-5" in x["path"] for x in notexact)} pr508')
old=yaml.safe_load(blob('a639e48','ops/reviews/pr508-review-5-codex-verdict.receipt.yaml'));lines.append('pr508 anchor at a639e48: '+json.dumps(old['anchor'],ensure_ascii=False));lines.append(git('show','-s','--format=%H %cI %s','3c7df6d').decode().strip())
# README summaries intentionally paraphrase four ci-g5 caveats; they still state both surfaces and missing runtime.
s=json.loads((OUT/'surface-audit.json').read_text());missing=[]
for v in s['selfclaims']:
 for c in v['caveats']:
  if 'readme_rows' in c and not c['description_matches']:
   name=Path(v['path']).name;row=next(l for l in (ROOT/'ops/reviews/README.md').read_text().splitlines() if l.startswith('| `'+name+'` | `'+c['id']+'` |'));missing.append(name);lines.append(name+f' readme_rows={c["readme_rows"]} both_surface_names={"codex_service" in row and "CLI" in row} missing_run_json={"không có `run.json`" in row}')
lines.append('non_verbatim_README_caveats='+repr(missing))
record(12,'Loại trừ báo nhầm từ lời trích, quyết định land và mô tả lịch sử','Đọc câu lịch sử như trạng thái hiện hành, hoặc gọi bản tóm tắt là sai byte verdict.','python3 review_evidence/context_checks.py',lines,'KHÔNG PHẢI LỖI. Sidecar sửa lời khai v1; human decision #714 tự nói không phải lượt dò tìm độc lập; bốn hàng ci-g5 diễn giải đủ hai lời khai và giới hạn runtime. Các câu trong cap_nhat_luot7 thuộc reviewed_sha 05bc12e, không tự khai service hoặc khẳng định bản vá tại fb87110 chưa áp')
