from common import *
def load(name):return json.loads((E/name).read_text())
for name in ['bytes.json','receipts.json','readme.json','claims.json']:
    assert load(name)['failures']==[],name
for side in ['head','base']:assert all(x['rc']==0 for x in load(side+'-gates.json'))
final=load('final-integrity.json');assert not any(final[k] for k in ['changed','added','removed','original_status','mutant_status'])
assert len(final['mutations_verified'])==4
summary='''Hoàn tất cross-review PR #1119 lượt 2: **approve — 0 P0, 0 P1, 0 P2, 0 P3** theo phạm vi kiểm offline được giao. Hai finding lượt 1 ĐÃ VÁ THẬT; không phát hiện finding mới. Cổng HEAD/base xanh, 237 bản sao khớp byte, 13 tệp bỏ được khai đúng, bốn biên nhận khớp trường đo được, README tăng đúng 23 hàng. Căn cứ từng kết luận là lệnh/output trong nhật ký và các bảng dưới đây. Không cấp quyền merge/land.

| Finding còn mở | Vị trí | Lệnh/output | Hướng vá |
|---|---|---|---|
| Không có (0/0/0/0) | — | Các phép đo dương/âm dưới đây | Không yêu cầu vá |

Ngưỡng áp dụng: không còn P0/P1/P2/P3. Nhật ký đã ghi tăng dần; trạng thái ban đầu chưa duyệt được thay bằng kết luận sau khi hoàn tất phép đo. Chỉ dùng git và tệp tại chỗ; không chạy mạng, không sửa clone `cay-kho/`.
'''
p=S/'VERDICT.md';text=p.read_text();parts=text.split('\n',4)
assert parts[0]=='Verdict: request_changes' and parts[1]=='Reviewed commit: '+HEAD
p.write_text('Verdict: approve\nReviewed commit: '+HEAD+'\n\n'+summary+'\n'+parts[4])
note('''Bảng cổng — lệnh bao `PYTHONDONTWRITEBYTECODE=1 python3 gates.py base` và `... gates.py head`, output `evidence/{base,head}-gates.json` cùng stdout/stderr. Các lệnh dưới chạy tại `work/base` và `work/head`; mỗi bản sao đã chạy `git config core.abbrev 7`. Các phép git đọc clone gốc dùng override cùng giá trị để giữ nguyên cấu hình gốc.

| Lệnh | Base c82047d | HEAD 8715ac9 | Delta |
|---|---|---|---|
| `python3 ops/bien_nhan_v2.py --root .` | rc0; 287 ĐẠT v2, tổng 340 | rc0; 291 ĐẠT v2, tổng 344 | +4 v2; vi phạm 0→0; KHÔNG ĐO ĐƯỢC 0→0 |
| `python3 ops/land_evidence_nguon.py --root .` | rc0; 75 ĐẠT, 25/28 miễn trừ, tổng 100 | rc0; output giống base | 0 |
| `python3 ../../direct.py .` | rc0; 3/3 PASS | rc0; 3/3 PASS | 0 |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | rc0; 10 tệp, 0 chỗ chép doctrine | rc0; giống base | 0 |
| `git diff --check c82047d HEAD` | rc0; rỗng | rc0; rỗng | 0 |

`direct.py` gọi trực tiếp cả ba hàm `t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi`, `t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc`, `t27_phan_chung_verdict_duoi_HOA_thieu_muc_luc_phai_DO_tren_moi_nen`. `final_integrity.py` đối chiếu output: hai SyntaxWarning của lease_publish_test.py giống nhau giữa base/HEAD sau bỏ phần đường dẫn; không có lỗi mới. Nợ biên nhận giữ nguyên: legacy 11/11, nợ đóng băng 42, L-REVIEW=1, L-ANCESTRY=60, L-SURFACE=0.

ĐỐI CHIẾU LƯỢT TRƯỚC — output `python3 closure.py`, `evidence/closure.json`:

| Finding lượt 1 | Phân loại | Phép đo trên HEAD |
|---|---|---|
| bo-sot-cache-khong-khai | ĐÃ VÁ THẬT | Ba tệp .gitignore/0.17.3/12591984194595340168/CACHEDIR.TAG trước thiếu khai, nay đủ hash/bytes 35/252/43; manifest chứa hash OMITTED mới và sha256sum rc0 |
| caveat-loai-diff-sai | ĐÃ VÁ THẬT | Hai DIFF.patch #1114 tồn tại, 1913/4160 bytes, khớp nguồn/git diff/manifest; hai caveat và hai hàng README đều ghi “DIFF.patch CO trong kho.” |

`prepare.py` đo diff a8f7470..HEAD trong ops/reviews chỉ đổi 5 tệp: README, hai receipt #1114, OMITTED và SHA256SUMS của #1114 lượt 1. Không đổi verdict/hiện vật nguồn. Byte toàn tập, manifest, cổng và delta đều đạt; không phát hiện lỗi mới từ bản vá.
''')
rows=['| Thư mục | Tệp nguồn cấp | Khớp byte | Vắng khai đúng | Manifest entries / rc |','|---|---:|---:|---:|---|']
for d in load('bytes.json')['results']:rows.append(f'| {d["stem"]} | {d["source_files"]} | {d["copied"]} | {d["declared_correct"]} | {d["manifest_entries"]} / {d["manifest_rc"]} |')
note('Byte — `python3 bytes_audit.py`, output `evidence/bytes.json`, `failures=[]`:\n\n'+'\n'.join(rows)+'''

Tổng 250 tệp nguồn, 237 bản sao bằng byte, 13 tệp vắng khai đúng; thiếu khai=0. Bốn bản phẳng bằng VERDICT nguồn. `sha256sum -c SHA256SUMS` cho 59/45/45/92 dòng OK; tập manifest phủ mọi tệp lưu trừ chính SHA256SUMS, không thiếu/thừa/trùng. Phép duyệt dùng rglob, có cả tệp ẩn và cache bị .gitignore che khỏi rg mặc định.

Hai DIFF.patch #1110 bỏ có chủ ý: `git diff c6dd7b3 e137f8c` và `git diff fb74c6e 3a3aac5` mỗi lệnh tái sinh đúng 261239 bytes, SHA256 `79c3d941cbfbc0cb32301c73d00237885aaf275bfef3aef347c1a5ded42968b6`. Cả bốn DIFF nguồn đều bằng git diff base_sha..reviewed_sha của receipt (`git_diff_equal=true`). Bốn launcher.err rỗng, cùng hash `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Bốn tệp >500 KB bị bỏ: 2043534, 822015, 838749, 1415498 bytes; hash/bytes khớp khai. Mọi chi tiết ở `evidence/pr*-mapping.json`.
''')
rows=['| PR/lượt | reviewed_sha | run_id | Giây / sự kiện model | sandbox_trang_thai |','|---|---|---|---|---|']
for d in load('receipts.json')['summary']:rows.append(f'| {d["stem"]} | `{d["sha"]}` | `{d["run_id"]}` | {d["duration"]} / {d["events"]} | {d["sandbox"]} |')
note('Biên nhận — `python3 receipts_audit.py`: 326 đối chiếu, `failures=[]`; expected/actual trong `evidence/receipt-checks.json`.\n\n'+'\n'.join(rows)+'''

Mọi run nguồn ma_thoat=0, trạng thái xong, model gpt-6-astra, effort xhigh; thời lượng khớp timestamp làm tròn 3 chữ số. Prompt SHA256, checkpoint, launcher và hash/bytes stdout/stderr đều khớp. SANDBOX-KHONG-DO-DUOC xuất hiện đúng ở #1110 lượt 1, #1114 lượt 1/2; vắng đúng ở #1110 lượt 2. Các trường này được đối chiếu với hiện vật, không chứng minh đầy đủ danh tính phiên phía máy chủ.

Các phép git trong `receipts_audit.py`: `git rev-parse f4b513d^2` = `3a3aac561ba359c08dfe92d95584b56494fc12d4`, `git rev-parse fb74c6e^2` = `51435a44659c4026539497a47ace971a71a64f40`; hai lượt 1 là tổ tiên merge (merge-base --is-ancestor rc0), khác head cuối. Cả hai merge là tổ tiên origin/master tại chỗ, message mang đúng PR. `git merge-base --is-ancestor cf5acfa HEAD` rc0; cả bốn evidence_url neo commit đầy đủ `cf5acfa7282ec42ef282015fa27fc642a4515588`, đúng path, blob bằng byte verdict và hash receipt. Reviewed tree bằng `git rev-parse <reviewed_sha>^{tree}` ở cả bốn. `_tinh_lop_tu_write_set` trên diff base..reviewed_sha trả sensitive cho 46/46/1/1 đường dẫn; classifier cùng blob tại bốn SHA và HEAD.

`python3 claims_audit.py`: 114 đối chiếu, failures=[]; ket_luan khớp verdict/log nguồn. #1110 lượt 1 có 41 bản sao/2 khai bỏ/116 đối chiếu lịch sử; cả hai lượt #1110 thêm đúng 4 hàng README lịch sử, mất0; diff ops/reviews giữa e137f8c..3a3aac5 rỗng. #1114 log nguồn ghi 52/52 và 80/80, wrapper base đỏ đúng p3b4/head xanh, hai đảo bản vá đỏ; lượt 2 cộng các worker được 26/1800→0/1800, 20/1200 R→Z, hai mutant bỏ giết làm a4/a11/b10 đỏ, thời gian suite tăng 15.017s (4.92%). Đây là đối chiếu nội dung lưu trữ của lượt cũ, không phải chạy lại các suite lịch sử. 23 trường cố định × 3 tiền lệ × 4 biên nhận đều khớp; khác assurance/ket_luan của pr1058 lượt 1 có căn cứ verdict changes_requested. Các caveat bổ sung có căn cứ run và quan hệ head/merge.
''')
rows=['| Biên nhận bị đổi verdict_sha256 | bien_nhan_v2 | t26 | Hai t27 | Chẩn đoán |','|---|---:|---:|---|---|']
for d in final['mutations_verified']:rows.append(f'| {d["receipt"]} | rc1 | FAIL | PASS | Chỉ đúng tệp này |')
note('Đột biến — `python3 mutations.py` và đọc lại output bằng `python3 final_integrity.py`; `evidence/mutations.json`, `evidence/final-integrity.json`:\n\n'+'\n'.join(rows)+'''

Mỗi lần chỉ đổi ký tự đầu hash, hồi nguyên trong finally; cổng bien_nhan_v2 báo blob evidence_url băm khác verdict_sha256, đúng 1 vi phạm; t26 báo LỆCH BĂM. Tổng 4/4 đột biến và 8/8 lần cổng đỏ đúng tệp. Chỉ thử trường hash, không suy đã thử riêng reviewed_sha/evidence_url.

README — `python3 readme_audit.py`: multiset hàng bắt đầu `| ` tăng 1217→1240; added=23, removed=0, extra=[], missing=[], failures=[]. Chính xác 4 hàng mục lục và 19 hàng caveat, đối chiếu cả mô tả; không mất hàng cũ và không có hàng mới ngoài bốn lượt.

Giới hạn: GitHub hiện tại, job CI/Windows thật, giá trị expectedHeadSha thực gửi qua API, credential/actor đăng, chỉ thị trong phiên executor và URL còn được GitHub phục vụ: **KHÔNG ĐO ĐƯỢC**. Câu caveat “Windows that do o CI ngoai luot review” chỉ là lời khai ngoài lượt, không phải kết quả đã xác minh ở đây. Phiên/nhà cung cấp phía máy chủ, toàn bộ argv chạy lịch sử, phiên bản CLI ngoài hiện vật nguồn và mức bao phủ cơ chế sandbox lịch sử: **KHÔNG ĐO ĐƯỢC**. Không suy KHONG_DO_DUOC thành “không có sandbox”. Các cây cay-kho/work/copies và thư mục con nguon bị loại khỏi đầu vào: **KHÔNG ĐO ĐƯỢC byte**, chỉ kiểm phạm vi khai loại cây. Không dựng nội dung nhạy cảm.

Kiểm cuối `python3 final_integrity.py`: 13334 tệp clone gốc trước/sau giữ nguyên hash, changed/added/removed=[], status rỗng, HEAD đúng ứng viên, tree `ad90d9046a4367e0649a2f812daccdb2b0622af7`; bản đột biến đã hồi nguyên. Verdict này không cấp quyền merge/land.
''')
print('VERDICT.md finalized: approve; P0/P1/P2/P3=0/0/0/0; bytes='+str(p.stat().st_size))
