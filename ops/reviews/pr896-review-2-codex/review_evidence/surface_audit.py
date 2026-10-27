from pathlib import Path
import subprocess,json,yaml
r=Path.cwd()/'cay-kho'; out=Path('/tmp/pr896-r2-audit-b3269a02'); v=Path.cwd()/'VERDICT.md'; id='VERDICT-KHAI-SAI-EXECUTION-SURFACE'
paths=sorted([*r.glob('ops/reviews/pr870*-verdict.md'),*r.glob('ops/reviews/pr889*-verdict.md')]); p=subprocess.run(['grep','-nH','codex_service',*map(str,paths)],capture_output=True,text=True); log=['$ grep -nH codex_service ops/reviews/pr870*-verdict.md ops/reviews/pr889*-verdict.md','rc='+str(p.returncode),p.stdout.strip()]
readme=(r/'ops/reviews/README.md').read_text(); matches=[]
for path in paths:
 if 'codex_service' not in path.read_text(): continue
 slug=path.name.removesuffix('-verdict.md'); d=yaml.safe_load(path.with_suffix('.receipt.yaml').read_text()); run=json.loads((r/d['model_reviewer_identity']['run_json']).read_text()); caveats={x['id']:x for x in d.get('verdict_usage_caveats',[])}; rows=[(i,l) for i,l in enumerate(readme.splitlines(),1) if path.name in l and id in l]
 lines=[(i,l) for i,l in enumerate(path.read_text().splitlines(),1) if 'codex_service' in l]; matches.append(slug)
 log.extend([slug+': selfclaim_lines='+str([n for n,l in lines])+'; flat==original='+str(path.read_bytes()==(r/'ops/reviews'/slug/'VERDICT.md').read_bytes()), 'run='+str(d['model_reviewer_identity']['run_json'])+'; run_id='+run['run_id']+'; execution_surface='+run['execution_surface']+'; lenh.chuong_trinh='+run['lenh']['chuong_trinh']+'; receipt.surface='+d['model_reviewer_identity']['surface'], 'receipt_caveat='+str(id in caveats)+'; README_surface_rows='+str([n for n,l in rows])])
 if id in caveats: log.append('caveat.mo_ta='+caveats[id]['mo_ta'].strip())
log.append('service_verdicts='+str(len(matches))+'; verdicts='+repr(matches)+'; caveat_covered=4; missing=pr889-review-1-codex')
s='\n'.join(log)+'\n'; (out/'surface-audit.log').write_text(s); print(s)
with v.open('a') as f: f.write('\n### HƯỚNG 13: Kiểm phủ caveat trên TOÀN BỘ verdict #870/#889\n\nGiả thuyết: danh sách bên giao bỏ sót verdict tự khai sai surface.\n\nLệnh: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/pr896-r2-audit-b3269a02/surface_audit.py` (gồm grep thật và đọc từng run.json, receipt, README).\n\nOutput thật:\n```text\n'+s+'```\n\nKết luận: LỖI — có NĂM verdict, caveat chỉ phủ BỐN. Thiếu #889 lượt 1; bản phẳng và bản thư mục đều có câu sai ở dòng 7; run 9f946d71 và receipt đều ghi codex_cli. Các dòng trích của bốn caveat hiện có (9/9/444/309) đúng nguyên văn nguồn.\n')
