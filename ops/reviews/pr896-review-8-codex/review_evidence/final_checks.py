from measure import *
checks=json.loads((OUT/'checks.json').read_text()); lines=[]; ok=True
for t in ['t26','t27','t138']:
 s=(OUT/(t+'.stdout')).read_text();m=re.search(r'^lease_publish: (\d+)/(\d+) đạt; đã chạy=(\d+), bỏ qua=(\d+)$',s,re.M); good=bool(m) and m[1]==m[2] and int(m[1])>0 and int(m[3])>0 and m[4]=='0' and (OUT/(t+'.rc')).read_text()=='0';ok &= good;lines.append(f'{t}: rc={(OUT/(t+".rc")).read_text()} conclusion={m[0] if m else "MISSING"} positive_equal_counts={good}')
doc=json.loads((OUT/'doc_claims.stdout').read_text());lines.append(f'doc_claims rc={(OUT/"doc_claims.rc").read_text()} parsed_ok_is_true={doc.get("ok") is True}');ok &= doc.get('ok') is True
pairs=[]
for p in (ROOT/'ops/reviews').glob('*.receipt.yaml'):
 d=yaml.safe_load(p.read_text());orig=ROOT/'ops/reviews'/p.name.removesuffix('-verdict.receipt.yaml')/'VERDICT.md'
 if orig.exists():pairs.append((str(orig.relative_to(ROOT)),orig.read_bytes()==(ROOT/d['verdict_path']).read_bytes()))
lines.append(f'flat_original_pairs={len(pairs)} all_byte_match={all(v for p,v in pairs)}');ok &= all(v for p,v in pairs)
for cmd in [('rev-parse','HEAD'),('rev-parse','HEAD^{tree}'),('diff','--exit-code'),('status','--porcelain=v1','--untracked-files=all')]:
 p=subprocess.run(['git','-C',str(ROOT),*cmd],capture_output=True,text=True);lines.append(f'$ git -C cay-kho {" ".join(cmd)}\nrc={p.returncode}\n{p.stdout}{p.stderr}');ok &= p.returncode==0
lines.append('required_checks_all_pass='+str(ok and all(c['rc']==0 for c in checks)))
record(13,'Kết luận dương N/N và giữ nguyên cây được review','Ca báo đạt nhưng thiếu tổng dương, hoặc cây nguồn đã bị đổi trong khi đo.','python3 review_evidence/final_checks.py',lines)
