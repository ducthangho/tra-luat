from pathlib import Path
import difflib,json,re,subprocess,yaml
BASE=Path(__file__).resolve().parent.parent;R=BASE/'cay-kho';mut={}
def read(p):return mut.get(p,(R/p).read_text())
def save(p,s):mut[p]=s
README='ops/reviews/README.md';BN='ops/reviews/pr896-review-2-codex-verdict.receipt.yaml';LAND='ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-land-evidence.yaml'
def caveat(stem,ident,level,desc):
 path='ops/reviews/'+stem+'-verdict.receipt.yaml';s=read(path);assert ident not in s
 block=f'  - id: {ident}\n    muc: {level}\n    mo_ta: >-\n      {desc}\n'
 if '\nverdict_usage_caveats:\n' in s:
  # All affected lists use two-space indentation, except absent lists below.
  anchor='\nverdict_usage_caveats:\n';tail=s.split(anchor,1)[1];entry=re.search(r'(?m)^( *)- id:',tail);indent=len(entry.group(1)) if entry else 2
  if indent==0:block=''.join(l[2:] if l.startswith('  ') else l for l in block.splitlines(keepends=True))
  s=s.replace(anchor,anchor+block,1)
 else:s=s.rstrip()+'\n\nverdict_usage_caveats:\n'+block
 save(path,s);parsed=yaml.safe_load(s);assert any(c['id']==ident for c in parsed['verdict_usage_caveats'])
 row=f'| `{stem}-verdict.md` | `{ident}` | {desc} |\n';s=read(README);lines=s.splitlines(keepends=True)
 hit=next((l for l in lines if l.startswith('| `'+stem+'-verdict.md` |')),None)
 if hit:s=s.replace(hit,row+hit,1)
 else:
  # Append to the existing warning table, before its following heading.
  start=s.index('Cảnh báo đang có hiệu lực');end=s.index('\n## ',start+4);before=s[:end];pos=before.rfind('\n|')
  endrow=s.index('\n',pos+1);s=s[:endrow+1]+row+s[endrow+1:]
 save(README,s)

desc='Verdict dong 12 tu khai execution surface `codex_service`, nhung run.json 5d4f7321d9a04ee1a87934e41fcf45c8 dong 78 ghi execution_surface=codex_cli, lenh.chuong_trinh=codex; receipt cung ghi surface=codex_cli. Dinh chinh be mat thanh codex_cli; giu nguyen byte verdict. Dinh chinh nay KHONG chung thuc model/effort da phuc vu va KHONG tu nang assurance.'
caveat('wp766-r1-g1-exec-review-1-codex','VERDICT-KHAI-SAI-EXECUTION-SURFACE','P1',desc)
old='changes_requested 1 P1 (verdict-surface-bo-sot-pr889-luot1: receipt pr889-review-1 thieu caveat VERDICT-KHAI-SAI-EXECUTION-SURFACE). HINT.patch trong thu muc CHUA ap; phien dieu phoi khong va, cho chu kho quyet.'
new='Verdict lich su tren 8d56009 la changes_requested 1 P1 (verdict-surface-bo-sot-pr889-luot1). Tai moc ghi so 765ae89 va cha 578fb4b, receipt pr889-review-1/README chua co caveat; HINT.patch CHUA ap luc ay. Commit 82359c4deec90edebbaebf9ab9d094902120b567 da ap HINT.patch, them caveat va hang README. Can doi chieu verdict moi tren exact SHA ung vien; khong suy approve/land tu viec ap patch, khong doi ket qua hay byte verdict lich su.'
s=read(BN);assert s.count(old)==1;s=s.replace('id: HINT-P1-CHUA-AP','id: HINT-P1-DA-AP-CAN-VERDICT-MOI',1).replace(old,new,1);save(BN,s)
s=read(README);assert s.count(old)==1;s=s.replace('`HINT-P1-CHUA-AP`','`HINT-P1-DA-AP-CAN-VERDICT-MOI`',1).replace(old,new,1)
old='P2 luot 1 DA DONG; P1 pr915-review-1 DONG MOT PHAN: receipt pr889-review-1 (verdict dong 7 tu khai `codex_service`) chua co caveat — HINT.patch chua ap'
new='P2 luot 1 DA DONG; tai reviewed_sha 8d56009, P1 pr915-review-1 DONG MOT PHAN vi receipt pr889-review-1 chua co caveat surface; HINT.patch da ap tai 82359c4 (receipt + README), can verdict moi tren exact SHA ung vien'
assert s.count(old)==1;s=s.replace(old,new,1);save(README,s)
# Keep all prior land-record lines intact; explicitly timestamp the prior block and append current readback.
s=read(LAND);s+='''
cap_nhat_20261026_sau_82359c4:
  moc_lich_su: >-
    Khoi cap_nhat_20261026_luot2 o tren la anh chup tai moc ghi so 765ae89, chua co ban va 82359c4.
    Cac cau "receipt va README chua co caveat", "HINT.patch ... CHUA ap" va "caveat con thieu ... neu ... duoc ap"
    trong khoi do chi dung tai moc lich su ay, khong phai trang thai sau 82359c4.
  hint_da_ap_commit: 82359c4deec90edebbaebf9ab9d094902120b567
  do_duoc: >-
    Diff 578fb4b..82359c4 them 4 dong vao receipt pr889-review-1 va 1 hang README:
    caveat VERDICT-KHAI-SAI-EXECUTION-SURFACE cho verdict dong 7, run 9f946d71 ghi codex_cli.
    Byte verdict lich su giu nguyen. Viec ap patch khong tu tao verdict approve tren SHA ung vien moi.
  can_verdict_moi_tren_exact_sha: true
  reviewer_assurance_81: CHUA DAT
  don_vi_land_de_xuat: >-
    De xuat (CAN chu kho chap nhan, ho so nay KHONG tu chon): don vi land = 816f439 (head #896) +
    3bc4244 (ban va P2 qua #915), kem caveat cua a9bc934 (qua #946) va caveat pr889-review-1 da them o 82359c4;
    van can doi chieu verdict moi va dieu kien land tren exact SHA ung vien.
  landed: false
''';save(LAND,s)
# The source-only inconsistencies need a weaker caveat than a measured surface correction.
for x in json.loads((BASE/'evidence/service-spelling-candidates.json').read_text()):
 stem=x['verdict'].removesuffix('-verdict.md');desc=f'Verdict dong {x["line"]} tu mo ta be mat Codex service/API, trong khi model_reviewer_identity.surface cua receipt ghi codex_cli (run ID khai {x["run_id"]}). Day la hai loi khai khac nhau; checkout khong kem run.json cua chinh luot de phan xu be mat thuc te. CLI/launcher trong receipt la loi khai ghi so, KHONG phai phep do lai runtime tai day. Giu nguyen byte verdict; can bo sung bang chung dung run truoc khi chon be mat, khong suy model/effort hay nang assurance tu caveat nay.'
 caveat(stem,'SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC','P2',desc)
patch=[]
for path,s in sorted(mut.items()):
 if path.endswith('.yaml'):yaml.safe_load(s)
 patch.extend(difflib.unified_diff((R/path).read_text().splitlines(keepends=True),s.splitlines(keepends=True),fromfile=path,tofile=path))
(BASE/'HINT.patch').write_text(''.join(patch));print('HINT files=',len(mut),'lines=',len(''.join(patch).splitlines()))
