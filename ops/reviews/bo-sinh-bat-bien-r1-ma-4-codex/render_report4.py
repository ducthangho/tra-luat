from pathlib import Path
import json
w=Path(__file__).resolve().parent;load=lambda n:json.loads((w/n).read_text());d=load('VERDICT.json');s=load('results-summary.json');md=(w/'report.template.md').read_text()
gates=['| Phép đo | rc | Bằng chứng dương / trạng thái |','|---|---:|---|']
for label in ['base-A-1','head-A-1','base-B-1','head-B-1','head-land','head-ci','base-selftest','head-selftest','base-ruff','head-ruff']:
 x=next(x for x in s['gates'] if x['label']==label)
 positive=x['positive']
 if label.endswith('selftest'):positive=[v for v in positive if '== tl selftest' in v]
 if label=='head-land':positive=[v for v in (w/'head-land.log').read_text().splitlines() if v.startswith('land_evidence_nguon:') or v.startswith('TỔNG:')]
 gates.append(f"| {label} | {x['rc']} | {'; '.join(positive) or 'Xem log'} |")
times=['| Bộ | Cặp | Base (s) | Head (s) | Delta (s) | Trần |','|---|---:|---:|---:|---:|---:|']
for x in s['pairs']:times.append(f"| {x['kind']} | {x['sample']} | {x['base']:.2f} | {x['head']:.2f} | {x['delta']:+.2f} | +{x['limit']} |")
cost=[]
for ca in ['a135','a136','c40']:
 rows=[x for x in load('measure.json') if x['label'].startswith('head-'+ca+'-')];cost.append(ca+': '+', '.join(f"{x['seconds']:.3f}s" for x in rows))
combined=[x['combined_seconds'] for x in load('new-code-cost.json') if 'combined_seconds' in x]
cost='Chạy riêng (ba mẫu, đều rc 0): '+'; '.join(cost)+'. a135+a136 cùng tiến trình, không profiler: '+', '.join(f'{x:.3f}s' for x in combined)+'.'
failed=s['selftest_failed'];same=s['selftest_failed_same'];selftext=f"Selftest **{d['selftest']['status']}**; tập ID đỏ base/head giống nhau: {same}. Delta mới bằng 0 không được đổi thành N/N passed. Không sửa credential/signer/tổ tiên `/tmp` để làm xanh."
if failed['base']:selftext+='\n\nCác ID đỏ ở cả hai vế:\n\n'+ '\n'.join('- '+x.strip().replace('[FAIL] ','') for x in failed['base'])
snap=load('snapshot-final.json');snaptext=f"Snapshot đầu/cuối: {snap['files_before']}→{snap['files_after']} tệp, 0 delta; HEAD/tree không đổi, tracked/untracked/index sạch; ignored `.codex/` có sẵn. Sandbox `workspace-write`, không phải mount read-only. Snapshot chỉ chứng minh hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. Repo nguồn ngoài checkout được cấp không nằm trong phạm vi quan sát. Mọi clone/log/đột biến nằm dưới `work/`."
for key,value in {'FINDINGS':(w/'findings.md').read_text(),'GATES':'\n'.join(gates),'SELFTEST':selftext,'TIMES':'\n'.join(times),'COST':cost,'SNAPSHOT':snaptext}.items():md=md.replace('@@'+key+'@@',value)
assert '@@' not in md and md.rstrip().endswith('KET_LUAN: changes_requested')
(w/'VERDICT.md').write_text(md)
print('Readable report rendered')
