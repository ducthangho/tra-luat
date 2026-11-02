from pathlib import Path
import difflib,json,subprocess,yaml
from audit import BASE,ROOT,OUT,SHA,MASTER,record
copy=Path((OUT/'copy-path.txt').read_text());assert subprocess.check_output(['git','-C',str(copy),'rev-parse','HEAD']).decode().strip()==SHA
assert subprocess.check_output(['git','-C',str(copy),'status','--porcelain'])==b''
texts={};caveats={
'pr823-wp802':'''verdict_usage_caveats:
- id: SURFACE-TU-KHAI-KHAC-HO-SO-RUNTIME-CHUA-DO-DUOC
  muc: P2
  verdict_path: ops/land/pr823-wp802-provenance/verdict-luot5/wp802-g1-luot5-codex-verdict.md
  verdict_sha256: b6ee86d0c9e523dfbe87718d12b4d646464e7a8720e9789f071f4aa04d6e3f01
  mo_ta: >-
    Verdict luot 5 dong 6 tu khai codex_service; review.so_loi_goi_codex_cli cua
    ho so nay ghi 5, va review.luot_cuoi.reviewer thuat lai launcher run b3d8a108
    cho CHINH luot 5 tren 5c6c7a8ac0dc1b968cfda9d11065e5f3e8713456
    (readback-comment-6247520447.json). Tai 05bc12e2b9008071ca28edbd4574e58644d48220
    khong co run.json/transcript cua dung run de phan xu hai loi khai surface.
    So luot CLI va loi thuat lai khong thay bang chung runtime. Be mat thuc chay
    KHONG_DO_DUOC; khong tu chon codex_cli hay codex_service. Giu byte verdict,
    khong chung thuc model/effort hay nang assurance/quyen merge/land.
''',
'pr877-wp854':'''verdict_usage_caveats:
- id: SURFACE-TU-KHAI-KHAC-HO-SO-RUNTIME-CHUA-DO-DUOC
  muc: P2
  verdict_path: ops/land/pr877-wp854-provenance/verdicts/wp854-g1-luot2-codex-verdict.md
  verdict_sha256: 612e86d854f4a7aad84a5f8e8d5986f58677e1b789d6ad3f176fefd1435cf277
  mo_ta: >-
    Verdict luot 2 dong 11 tu khai codex_service; khong_do_duoc.0 cua ho so nay
    lai thuat lai cac luot review co header CLI gpt-6.1-sol xhigh. Tai
    05bc12e2b9008071ca28edbd4574e58644d48220 khong co run.json/transcript cua
    chinh luot 2 tren b952c106ba6bbf94699bda5fe5fb2f6d7f7256fb de phan xu
    hai loi khai surface; cau noi ve header CLI chi la nguon thu cap.
    Be mat thuc chay KHONG_DO_DUOC; khong tu chon codex_cli hay codex_service.
    Giu byte verdict, khong chung thuc model/effort hay nang assurance/quyen merge/land.
'''}
for stem,extra in caveats.items():
 path='ops/land/'+stem+'-land-evidence.yaml';s=(ROOT/path).read_text();assert 'verdict_usage_caveats:' not in s;texts[path]=s.rstrip()+'\n\n'+extra
path='ops/land/pr491-r358-ghi-so-land-evidence.yaml';s=(ROOT/path).read_text();old='    NỢ CŨ KHÔNG ĐỘNG TỚI: `_kiem_bia_mo`';assert s.count(old)==1
s=s.replace(old,'    Ảnh chụp lời khai lịch sử trong blob tại cdd0b1d19439e286fb7a86020ce2d258bafc2102:\n'+old)
ending='    `origin/master`; trạng thái Issue/PR chưa hỏi lại API trong đợt này.\n';assert s.count(ending)==1
s=s.replace(ending,ending+'''    Đính chính tại 05bc12e2b9008071ca28edbd4574e58644d48220: PR #490 ĐÃ merge bằng
    8cee9410e958a6b9d956e080c11878fbd80d9f5f, cha thứ hai là head
    01e7f77d707cb093b5ba6d9b9d8577f40d025488. `git merge-base --is-ancestor
    8cee9410e958a6b9d956e080c11878fbd80d9f5f 3e973a03b151e37cd402e0a723816eeaa8247193`
    và cùng lệnh với 05bc12e2b9008071ca28edbd4574e58644d48220 đều rc=0.
    Câu "#490 chưa merge" ở trên chỉ thuộc mốc lịch sử đã ghim; nhãn THUẬT LẠI
    không tự neo thời điểm. Chỉ đính chính quan hệ Git, không xác nhận lại trạng thái
    Issue #463–#467, PR #479 hoặc các nợ khác, không suy Packet đã landed.
''')
texts[path]=s
old_partial='VERDICT.partial.md chi co dong dang_lam + mot phep do t26; KHONG duoc tinh la verdict.'
new_partial='VERDICT.partial.md (28214 byte) van dang_lam, da ghi 14 muc phep do/doi chieu (gom t26, t27, t138, bon cong va cac huong Git/dot bien); KHONG duoc tinh la verdict hoan tat.'
for path in ['ops/reviews/pr896-review-6-codex-verdict.receipt.yaml','ops/reviews/README.md']:
 t=(ROOT/path).read_text();assert t.count(old_partial)==1;texts[path]=t.replace(old_partial,new_partial)
patch='# chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit\n'
for path,s in sorted(texts.items()):
 if path.endswith(('.yaml','.yml')):yaml.safe_load(s)
 before=(ROOT/path).read_text();patch+=''.join(difflib.unified_diff(before.splitlines(keepends=True),s.splitlines(keepends=True),fromfile=path,tofile=path))
(BASE/'HINT.patch').write_text(patch)
for mode in ['dry-run','apply']:
 cmd=['patch','--batch','--fuzz=0','-p0','-i',str(BASE/'HINT.patch')]
 if mode=='dry-run':cmd.insert(1,'--dry-run')
 p=subprocess.run(cmd,cwd=copy,capture_output=True,text=True);(OUT/('hint-'+mode+'.log')).write_text(p.stdout+p.stderr);print(mode,'rc='+str(p.returncode),p.stdout);assert p.returncode==0
for path,s in texts.items():assert (copy/path).read_text()==s
(OUT/'hint-paths.json').write_text(json.dumps(list(texts),indent=2))
record(13,'Gợi ý vá tài liệu trên clone exact SHA','PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/build_hint.py; patch --dry-run --batch --fuzz=0 -p0 -i <HINT.patch>; patch --batch --fuzz=0 -p0 -i <HINT.patch>','patch_paths=5 dry_run_rc=0 apply_rc=0\n'+(OUT/'hint-dry-run.log').read_text()+'YAML parsed; 5/5 applied files byte-match intended text. No receipt v1 or verdict modified.')
