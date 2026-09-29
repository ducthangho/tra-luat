from pathlib import Path
import hashlib,json,shutil,difflib,subprocess
R=Path(__file__).resolve().parents[1];T=R/'cay-kho';O=R/'do-review10';H=R/'goi-y';C=H/'cay'
sha=lambda b:hashlib.sha256(b).hexdigest()
LABEL='chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit'
slug1='bia-mo-mot-ref-khong-thu-hoi-moi-ban';slug2='manifest-luot8-liet-ke-hien-vat-khong-duoc-giao'
prov={'reviewed_sha':'c43347d1e2c2f76bb21dc2d9d28bd6bfa153d355','label':LABEL,
    'scope':'Gợi ý ngoài checkout. P1 chỉ bổ sung hồ sơ chặn/readback; không đóng trạng thái trước hạn, không cấp hay thu hồi lease. P2 phục dựng byte thiếu, giữ nguyên manifest lịch sử.',
    'files':[]}
def record(rel,source,slugs,operation):
    target=C/rel;b=target.read_bytes();base=T/rel
    entry={'path':rel,'operation':operation,'slugs':slugs,'target_existed_at_reviewed_sha':base.is_file(),
        'target_base_sha256':sha(base.read_bytes()) if base.is_file() else None,'source_path':str(source.relative_to(T)) if source else None,
        'source_sha256':sha(source.read_bytes()) if source else None,'hint_sha256':sha(b),'hunks':[]}
    before=base.read_text().splitlines() if base.is_file() else []
    after=target.read_text().splitlines()
    for tag,i,j,a,z in difflib.SequenceMatcher(a=before,b=after,autojunk=False).get_opcodes():
        if tag!='equal':entry['hunks'].append({'kind':tag,'base_start_line':i+1,'base_line_count':j-i,'hint_start_line':a+1,'hint_line_count':z-a,'slugs':slugs})
    prov['files'].append(entry)

rel='ops/issues/463-GATE-TACH-JOB-CAT-CHI-PHI.md';src=T/rel;target=C/rel;target.parent.mkdir(parents=True,exist_ok=True)
old=src.read_text()
block='''### ĐỐI CHIẾU LƯỢT 10 — trạng thái chặn trước hạn #456

Đo độc lập trên snapshot sandbox của `c43347d1e2c2f76bb21dc2d9d28bd6bfa153d355`,
07-09-2026 11:29:38Z: `ai-dang-giu` cho registry **2** (#456 + exec-1r4),
workflow **1** (exec-1r4). Đây là readback mirror được giao, không phải GitHub trực tiếp.
P1 `bia-mo-mot-ref-khong-thu-hoi-moi-ban` **còn mở**. `check` r4 rc=0 không chứng minh A9.

Tại snapshot này, blob #456 chưa bia mộ `8b2103c06687546379a17f6deafc97f1fe0173fd`
có trên **10 tên nhánh**: `master`, `ops/cap-lease-456`, `ops/cap-lease-461`,
`claude/agents-ngoai-goi`, `claude/cap-nhat-trang-thai-pr-taxzax`,
`claude/elegant-bun-cd554f`, `claude/priceless-volhard-329577`,
`claude/r356-bien-nhan-cross-review`, `claude/tra-luat-process-review-o4d7kb`,
`ops/lease-wp461-g2`. Mirror còn mục `HEAD` trùng master, không cộng thành nhánh máy chủ độc lập.
Danh sách 9 tên đo trước đó không đủ cho snapshot này; tip của nhánh bổ sung mang giờ commit
11:20:33Z, nên không suy rằng phép đo máy chủ 10:22Z đã bỏ sót nó lúc ấy.

R3 đã có ở base review lượt 9 (cấp 09:44:51Z, commit `3ef7d2a`); r4 mới thêm sau base
(cấp 10:17:12Z, commit `1a33030`). Đây là các sự kiện `executor_lease_granted` riêng.
Bia mộ hai chiều r3→r4 tắt bản r3 tương ứng, không làm blob #456 cũ trên ref khác hết giữ.
Không có miễn trừ loại trừ write set do “cấp liên tục”. Mỗi lần cấp lại vẫn phải xét giao
write set theo Protocol §1.2/§5. Hồ sơ đang chặn thi công; việc đã cấp lease không chứng minh
executor đã bắt tay sửa runtime, và cũng không chứng minh A9 đạt.

Theo chỉ thị giao review lượt 10, chủ kho chọn **chờ hết hạn tự nhiên 14:30:07Z 07-09-2026**.
Chưa có readback sau hạn trong hồ sơ này. Giữ trạng thái chặn, không coi revision mới hoặc
merge PR là cách đóng P1. Khi đến hạn, executor phải đọc lại đầy đủ ref và chạy
`ai-dang-giu` trên cả hai đường write set; phải có đúng tên lease hiện hành, mỗi đường
`NGƯỜI_GIỮ 1`, không còn bản #456 `CÒN_HẠN` thiếu bia mộ, và không có kết quả
`KHÔNG_XÁC_ĐỊNH`. Ghi thời điểm, exact head, tập ref đã đối chiếu và stdout thật.
Chỉ sau đó mới ghi **đóng trạng thái bằng hết hạn tự nhiên và readback**, không ghi “đã vá”.
Lịch sử cấp khi write set giao nhau vẫn được giữ. R4 khi ấy cũng phải còn hiệu lực;
thời gian trôi không thay thế phép kiểm các điều kiện khác của packet.

'''
marker='\n---\n\n**Đặc tả đóng băng (revision 4):**'
assert old.count(marker)==1
target.write_text(old.replace(marker,'\n'+block+marker))
record(rel,src,[slug1],'document_open_state_and_required_future_readback')

base='ops/reviews/pr468-hoso-4-packet-review-9-codex/artifact-repair';src=T/base;dst=C/base
shutil.copytree(src,dst,dirs_exist_ok=True)
for p in sorted(src.rglob('*')):
    if p.is_file():record(str(p.relative_to(T)),p,[],'unchanged_context_for_standalone_checksum')
missing=[]
for n,line in enumerate((src/'ARTIFACTS.sha256').read_text().splitlines(),1):
    expected,sub=line.split(maxsplit=1);sub=sub.lstrip('*');path=dst/sub
    if not path.is_file():
        source=T/'ops/reviews/pr468-hoso-4-packet-review-8-codex'/sub
        assert sha(source.read_bytes())==expected
        path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(source.read_bytes())
        record(str(path.relative_to(C)),source,[slug2],'restore_exact_bytes_from_complete_round8')
        prov['files'][-1]['manifest_path']=base+'/ARTIFACTS.sha256';prov['files'][-1]['manifest_line']=n
        missing.append(sub)
assert len(missing)==19
readme=dst/'README.md'
readme.write_text('''# Bản thử phục dựng gói lượt 8, thực hiện trong review lượt 9

Thư mục này là bản sao phục dựng gói lượt 8 dùng cho phép thử
`artifact_checks.py` của reviewer lượt 9. Nó không phải lần chạy test mới trên
head lượt 9 hay head lượt 10. Các timestamp, đường dẫn scratch và số đo bên trong
thuộc hiện vật lịch sử lượt 8; giữ nguyên để truy nguồn.

`../artifact-checks.json` ghi lượt 9: bản lượt 8 gốc khi ấy có 50/69 tệp,
bản thử phục dựng đạt 69/69. Khi chép bản thử vào kho tại c43347d, 19 tệp rig/
lại bị thiếu. Gợi ý lượt 10 điền chúng bằng byte có đúng băm từ gói lượt 8
đã hoàn chỉnh, không sửa manifest để bỏ cam kết. `sha256sum --check ARTIFACTS.sha256`
trong bản gợi ý đạt 69/69. Kết quả thử này không biến suite lịch sử thành suite mới chạy.

chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit
''')
record(str(readme.relative_to(C)),None,[slug2],'label_historical_repair_copy')
prov['manifest_source_sha256']=sha((src/'ARTIFACTS.sha256').read_bytes())
H.mkdir(exist_ok=True)
(H/'hint_provenance.json').write_text(json.dumps(prov,ensure_ascii=False,indent=2)+'\n')
(H/'README.md').write_text(f'''# Gói gợi ý review PR #468 lượt 10

**{LABEL}**

Nền: `c43347d1e2c2f76bb21dc2d9d28bd6bfa153d355`. Cây tệp nằm trong `cay/`;
`hint_provenance.json` ghi nguồn byte, băm nền, băm đầu ra và từng hunk → slug.
Tệp thêm mới có `target_base_sha256: null`; 19 hiện vật phục dựng có nguồn
`source_path`/`source_sha256` trong gói lượt 8. Không áp mù khi nền khác.

- `{slug1}`: Issue #463 được bổ sung số đo chặn và thủ tục readback sau hạn.
  Đây là sửa hồ sơ vận hành; **không đóng P1 trước 14:30:07Z**, không thay/cấp/thu hồi lease.
  Đường chủ kho chọn cần thời gian thực và readback mới; gói tệp không thay được việc đó.
- `{slug2}`: phục dựng đúng 19 tệp còn thiếu trong bản thử lượt 9,
  giữ nguyên manifest. Kèm 50 tệp và manifest nguyên trạng để tự kiểm checksum trong cây gợi ý;
  README phân biệt bản thử lịch sử với hiện vật đo mới.

Gói không chứa commit, push, lease mới, biên nhận mới hay kết quả CI mới.
''')
p=subprocess.run(['sha256sum','--check','ARTIFACTS.sha256'],cwd=dst,capture_output=True,text=True)
(O/'hint-manifest.stdout').write_text(p.stdout);(O/'hint-manifest.stderr').write_text(p.stderr)
validation={'rc':p.returncode,'ok':sum(s.endswith(': OK') for s in p.stdout.splitlines()),'restored':len(missing),'included_files':len(prov['files']),
    'all_output_hashes_match':all(sha((C/f['path']).read_bytes())==f['hint_sha256'] for f in prov['files']),
    'all_source_hashes_match':all(not f['source_path'] or sha((T/f['source_path']).read_bytes())==f['source_sha256'] for f in prov['files']),
    'all_base_hashes_match':all((sha((T/f['path']).read_bytes())==f['target_base_sha256']) if f['target_existed_at_reviewed_sha'] else not (T/f['path']).exists() for f in prov['files']),
    'changed_hunks_mapped':all(h['slugs'] for f in prov['files'] for h in f['hunks'])}
assert validation['rc']==0 and validation['ok']==69 and all(v for k,v in validation.items() if k.startswith('all_') or k=='changed_hunks_mapped')
(O/'hint-validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(validation,ensure_ascii=False,indent=2))
