from pathlib import Path
import json,shutil
S=Path(__file__).resolve().parent;E=S/'evidence'
pre=json.loads((E/'preflight.json').read_text());byt=json.loads((E/'bytes.json').read_text());rec=json.loads((E/'receipt.json').read_text());ci=json.loads((E/'ci.json').read_text());integ=json.loads((E/'final-integrity.json').read_text());mut=json.loads((E/'mutation.json').read_text())
assert pre['outside_reviews']==[] and pre['patch_matches']
assert rec['mismatches']==[] and ci['local_kiem_re_rc']==0
assert all(x['rc']==1 and x['only_new_receipt_failed'] for x in mut)
assert not integ['added'] and not integ['removed'] and not integ['modified'] and not integ['status']
for label in ('counted','failed'):
 for k in ('mismatch','generated_or_unknown','undeclared_missing','omitted_mismatch','manifest_uncovered','manifest_extra','manifest_duplicates'):assert not byt[label][k],(label,k)
shutil.copyfile(S/'VERDICT.md',E/'VERDICT.progress.md')
report='''Verdict: approve
Reviewed commit: 1a87a863174ef104b2df8bc98b77724fb6796d9b

Hoàn tất cross-review PR #1136 lượt 1: **approve — 0 P0, 0 P1, 0 P2, 0 P3** trong phạm vi offline được giao. 87 tệp nguồn lưu khớp byte; 7 tệp bỏ khai đủ hash/bytes; biên nhận khớp các trường đo được; README thêm đúng 5 hàng. Các cổng yêu cầu đạt, và đột biến hash làm đỏ đúng biên nhận mới. Không cấp quyền merge/land.

| Finding còn mở | Vị trí | Lệnh/output | Hướng vá |
|---|---|---|---|
| Không có (0/0/0/0) | — | Các phép đo dương/âm dưới đây | Không yêu cầu vá |

Mọi lệnh dưới đây chạy từ sandbox này, trừ lệnh ghi rõ chạy tại bản sao. Dùng `PYTHONDONTWRITEBYTECODE=1`; `git config --file audit.gitconfig core.abbrev 7`, trỏ `GIT_CONFIG_GLOBAL` vào tệp ấy cho phép đo clone gốc; đặt `git config core.abbrev 7` trong từng bản sao. Lệnh và output đầy đủ nằm trong các script/log được dẫn. Không suy kết quả GitHub từ mô phỏng cục bộ.

**Phạm vi và neo.** `python3 setup_audit.py` → [evidence/preflight.json](evidence/preflight.json):

- `git rev-parse HEAD` = SHA dòng 2; tree `5888c2e34c8e35ae13dd5eb017370186e1b17d7a`; `git status --porcelain=v1` rỗng; `git config core.abbrev` = `7`.
- `git merge-base HEAD origin/master` = `62e629156fd0729b743f15eed2f32487786b9adc`; `git diff --name-only 62e6291 HEAD` = **93 đường dẫn**, `outside_reviews=[]`.
- `git diff 62e6291 HEAD` khớp nguyên byte `DIFF.patch`, SHA256 `2704197fbfa4c55216789f6a30e993d1af665a95ea4d7184386f2c8a8d925474`.
- `git log 62e6291..HEAD` có đúng hai commit `62a30b1d7a153cedc19ca711b0c60c77baf142e6` và `1a87a863174ef104b2df8bc98b77724fb6796d9b`.

**Cổng và delta.** `python3 measure_gates.py` chạy trên `work/base` ở `62e6291` và `work/head` ở SHA ứng viên. [evidence/gates.json](evidence/gates.json) ghi argv, rc, stdout/stderr nguyên văn; [direct_gates.py](direct_gates.py) gọi trực tiếp tất cả hàm tên `t26_*`/`t27_*`.

| Lệnh tại mỗi bản sao | Base | HEAD | Delta/output |
|---|---|---|---|
| `python3 ops/bien_nhan_v2.py --root .` | rc0, 295 ĐẠT v2, tổng 348 | rc0, 296 ĐẠT v2, tổng 349 | +1 biên nhận đạt; cùng 0 vi phạm, 0 KHÔNG ĐO ĐƯỢC; 11/11 miễn trừ, 42 nợ không đổi |
| `python3 ops/land_evidence_nguon.py --root .` | rc0 | rc0 | Cùng 79 ĐẠT, 25/28 miễn trừ, tổng 104; 0 vi phạm, 0 KHÔNG ĐO ĐƯỢC |
| `python3 ../../direct_gates.py .` | rc0, 3 PASS | rc0, 3 PASS | t26, t27 mục lục và t27 phản chứng đuôi HOA đều chạy; SyntaxWarning `\\d` nền giống nhau |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | rc0 | rc0 | Cùng “đã quét 10 tệp, 0 chỗ chép doctrine” |
| `git diff --check 62e6291 HEAD` | rc0, rỗng | rc2 | 16 thông báo trailing whitespace, chỉ hai log nêu dưới |
| `git -c core.whitespace=-blank-at-eol,-blank-at-eof,-space-before-tab diff --check 62e6291 HEAD` | rc0, rỗng | rc0, rỗng | Không có lỗi theo cấu hình CI |
| Chính `ci_duong_nhanh.kiem_diff_check()` | `[]` | `[]` | Lệnh thật thêm `--attr-source=62e6291…`, `--no-renames`, diff ba chấm; rc0, stdout/stderr rỗng |

`python3 mutate_receipt.py` đổi **riêng ký tự đầu `verdict_sha256` c601… → d601…** của biên nhận mới trong `work/mutant`, rồi hồi nguyên. [evidence/mutation.json](evidence/mutation.json), [stderr validator](evidence/mutant-bien-nhan.stderr) và [stdout direct](evidence/mutant-direct.stdout): validator rc1, **1 vi phạm** tại `pr1131-review-1-codex-verdict.receipt.yaml`, “blob tại evidence_url băm c601… nhưng biên nhận khai d601…”. t26 rc1/FAIL “LỆCH BĂM” đúng cùng tệp; hai t27 vẫn PASS. `git status --porcelain=v1` sau hồi nguyên rỗng. Phép thử này không chứng minh mọi trường của biên nhận đều được validator cưỡng chế.

**Khoảng trắng và cổng nghiêm hơn.** `python3 audit_bytes.py` → [evidence/bytes.json](evidence/bytes.json): `evidence/gates-progress.txt` khớp nguồn, **5.382 bytes**, SHA256 `5f3cdf640f3de69333ac6364b42cdf52a6bc5bad5873f8386b1ab85b56e667bb`. Khoảng trắng cuối dòng tại **2, 3, 4, 6, 28, 50, 58, 61, 62, 64, 71, 75, 76, 80**. [Output mặc định](evidence/head-diff-default.stdout) báo 14 dòng ấy và hai dòng **1, 16** của `evidence/mutations-progress.txt`. Cả hai log giữ nguyên byte nguồn; không cần sửa hiện vật để làm sạch check mặc định.

`python3 audit_ci.py` → [evidence/ci.json](evidence/ci.json): dựng commit merge **mô phỏng cục bộ chỉ trong bản sao**, tree trùng HEAD; classifier trả `duong_nhanh`; chính `lenh_kiem_re` rc0, **“kiem-re DAT (93 tep doi, 0 loi)”**. Ghi lại argv thật:

```text
git --attr-source=62e629156fd0729b743f15eed2f32487786b9adc -c core.whitespace=-blank-at-eol,-blank-at-eof,-space-before-tab diff --check --no-renames 62e629156fd0729b743f15eed2f32487786b9adc...1a87a863174ef104b2df8bc98b77724fb6796d9b
=> rc=0, stdout=b'', stderr=b''
```

Ca hiện hữu `t20d_kiem_re_khoang_trang_cuoi_dong_khong_do()` **PASS**, kiểm cả chiều check mặc định đỏ và CI xanh trên fixture.

`audit_ci.py` thực hiện `git grep -n -e --check` trên tập tệp tracked ngoài các thư mục hiện vật đã loại trong script → [evidence/all-check-calls.txt](evidence/all-check-calls.txt), rồi quét AST **154 tệp Python**, không lỗi parse. Các lời gọi mang đối số `diff`/`--check` nằm ở `ops/ci_duong_nhanh.py:621` và `ops/ci_duong_nhanh_test.py:898,903,969,989,1016,1093`. Những lời gọi trong selftest dùng `with kho_that(...)` — kho fixture tạm, không phải diff PR này; ngữ cảnh ghi tại [evidence/check-context.json](evidence/check-context.json). Workflow `.github/workflows/ci.yml:740–757` gọi `kiem-re` khi `duong_nhanh` và selftest trên Linux.

Có lệnh nghiêm trong hiện vật lịch sử `ops/evidence/wp685-r28-g5-attempt-2/chay_b1_b5.sh:17`, neo base `ab457c6…`; `git grep -n -F chay_b1_b5 -- .github/workflows .claude/dev ops/ci_duong_nhanh.py ops/cong_cu_test.py scripts` → **rc1, rỗng**. `.agents/skills/work-packet/SKILL.md:88` là ví dụ `git diff --check` không truyền range, kèm chỉ thị chọn theo Packet; các nhắc ở `scripts/tl_selftest.py:22705,22755` là comment lịch sử. **Không tìm thấy cổng khác chạy check whitespace nghiêm hơn lên diff PR này trong mã/workflow tại HEAD.** Trạng thái CI/GitHub thực tế: **KHÔNG ĐO ĐƯỢC**.

**Byte, manifest và tệp bỏ.** `python3 audit_bytes.py` duyệt đệ quy, kể cả tên ẩn; ánh xạ `launcher.out ← launcher.json`, `run/* ← runs/<id>/*`, script/config ở `evidence/` về tên tương ứng tại gốc nguồn. Kết quả từng tệp/hash/bytes ở [evidence/bytes.json](evidence/bytes.json):

| Nguồn → thư mục kho | Tệp nguồn | Lưu khớp byte | Bỏ có khai | Bỏ không khai / lệch |
|---|---:|---:|---:|---:|
| `nguon/review1131b` → `pr1131-review-1-codex` (trừ thư mục lượt hỏng) | 86 | 81 | 5 | 0 / 0 |
| `nguon/review1131a` → `luot-hong-xac-thuc` | 8 | 6 | 2 | 0 / 0 |

Không có tệp hiện vật không ánh xạ được; hai `OMITTED.txt` và `SHA256SUMS` là metadata tạo khi ghi sổ. `sha256sum -c SHA256SUMS` tại thư mục cha → **rc0, 89/89 OK** ([log](evidence/bytes-counted-sha256sum.txt)); tập manifest bằng đúng mọi tệp dưới thư mục trừ chính manifest, không thiếu/thừa/trùng. **7 mục** thuộc thư mục lượt hỏng được manifest cha phủ; tiền lệ `pr1119-review-1-codex/luot-hong-dia/` cũng dùng manifest cha.

Các tệp nguồn vắng đều có đúng SHA256 và bytes trong `OMITTED.txt` tương ứng: lượt tính gồm `DIFF.patch`, `launcher.err`, `evidence/history-attempt1.json`, `evidence/history.json`, `evidence/original-before.json`; lượt hỏng gồm `DIFF.patch`, `launcher.err`. `undeclared_missing=[]`, `omitted_mismatch=[]`, `declared_but_not_missing=[]`; không bỏ sót tệp trong thư mục con. Ba JSON lớn lần lượt **4.571.741 / 4.571.479 / 1.458.580 bytes**; launcher.err rỗng. Các thư mục clone/work/nguon không có trong đầu vào sao chép nên nội dung bên trong chúng **KHÔNG ĐO ĐƯỢC**.

`git diff 180039c 0e824fe` tái tạo **946.152 bytes**, SHA256 `b3cd603ebe29f46e0d614306e3d050f77fa3a653eadd31cf12c6dc3c1fe760d2`, khớp cả hai `DIFF.patch` nguồn và hai lời khai OMITTED. Bản phẳng `pr1131-review-1-codex-verdict.md`, bản lưu `VERDICT.md` và nguồn cùng **20.188 bytes**, SHA256 `c601112323513db31e0aefc40340672d69fba39567e3f8639b3ebdd53fd321e6`.

**Biên nhận.** `python3 audit_receipt.py` → [evidence/receipt.json](evidence/receipt.json): **85 đối chiếu, mismatches=[]**. Các giá trị chính:

| Trường / phép đo | Output và đối chiếu |
|---|---|
| Verdict/đếm finding | VERDICT dòng 1 `approve`, dòng 4 `0 P0, 0 P1, 0 P2, 0 P3`; `findings_ids=[]`; biên nhận khớp, không đếm bốn caveat sử dụng thành finding |
| SHA/tree | VERDICT dòng 2 và run.head = `0e824fe4c1ac674081c93c6f2098e5433c932890`; `git rev-parse 0e824fe^{tree}` = `e3d867387abbcee063ab7b72803655d826bb0964` |
| Merge | `git show -s --format=%P 2609cd8` = `c165a5d0d4048e10e7da875f2ba7524136fb5735 0e824fe4c1ac674081c93c6f2098e5433c932890`; cha thứ hai đúng reviewed_sha; subject nhắc PR #1131; `merge-base --is-ancestor 2609cd8 origin/master` rc0 |
| Base | `git merge-base 0e824fe c165a5d` = `180039c4b791fba4c89991623151cbb7378fce53`; không nhầm base review với cha thứ nhất khi master đã tiến |
| Ngày merge | Git ghi `2026-11-02T05:25:07+07:00`, tương ứng `2026-11-01T22:25:07Z`; lời ghi ngày 01-11 phù hợp UTC |
| Evidence URL | Commit `62a30b1d7a153cedc19ca711b0c60c77baf142e6`; `merge-base --is-ancestor <commit> HEAD` rc0; `git show <commit>:ops/reviews/pr1131-review-1-codex-verdict.md` trùng byte và hash verdict; kiểm blob local, không truy cập URL |
| Run tính | `260f271e8d1b445da0f03da5e69d8676`; rc0; `xong`; **555,436 s**, khớp chênh timestamp làm tròn 3 chữ số; `worktree_sach=true` |
| Model/effort | run có **25** phần tử model_phuc_vu, đều `gpt-6-astra`; trạng thái `DO_DUOC`; effort `[xhigh]`, `DO_DUOC`; model/model_da_chay/evidence_ref khớp |
| Prompt và sandbox | Hash prompt `542e7e873bbbb595ebbe9e60a92223e71e4c8872ed4e5601eae874d361cb0f22` khớp PROMPT của cả hai lượt; run tính `sandbox_trang_thai=DO_DUOC`, quan sát cho phép ghi tổ tiên workspace, phù hợp caveat checkout không cưỡng chế read-only |
| Run/checkpoint/log | Cả hai launcher.out parse bằng run.json; checkpoint id/head/hash khớp; stdout/stderr khớp SHA256/bytes run khai; thời lượng đều khớp timestamp |
| Lớp review | Gọi chính `_tinh_lop_tu_write_set` với `git diff --name-only 180039c 0e824fe`: **180 tệp**, đều ops/reviews, trả `sensitive`; review_class/effective_review_class khớp |
| Assurance | `cross_approved` phù hợp approve 0/0/0/0, provider/model ghi trong run và executor Claude theo đầu vào; không dùng tài khoản người đăng để suy model |
| Lượt hỏng | `ee42b27f1217481fa856bdcfc37b5f88`; cùng head; rc1; **20,859 s** → 20,9 s; không có VERDICT ở nguồn lẫn bản lưu; không có receipt/lượt review riêng được thêm |

`ket_luan` ghi 170 tệp / 9 tệp bỏ / hai biên nhận / README +10 / dòng trống cuối verdict lượt 2 và CI — **khớp tóm tắt VERDICT nguồn dòng 4**, nói về review PR #1131 đã được ghi sổ, không phải số tệp của PR #1136 này. Phép đối chiếu ở đây xác nhận chép đúng lời kết luận; không tái chạy toàn bộ review lịch sử.

So cấu trúc với `pr1119-review-2-codex-verdict.receipt.yaml` bằng `audit_receipt.py`: `keys_added=[]`, `keys_removed=[]`; 13 trường chính sách/schema/role/provider/class/assurance/axes khớp. Lượt hỏng đặt dưới thư mục của lượt tính như tiền lệ `luot-hong-dia`; khác biệt có giải thích ngay trong `OMITTED.txt`: lượt này không có VERDICT vì dừng trước khi ghi. Không thấy lệch tiền lệ cần sửa trong phạm vi đã đo.

**README.** `audit_receipt.py` lấy `git show 62e6291:ops/reviews/README.md` rồi so với HEAD bằng cả tập và multiset các dòng bắt đầu `| `: **1.262 → 1.267**, `added=5`, `removed=[]`, `set_added_count=5`. Một hàng mục lục khớp verdict/receipt, approve, cross_approved, lượt 1/PR #1131, 0/0/0/0, run 260f271e, model, head 0e824fe, merge 2609cd8, 20.188 bytes. Bốn hàng caveat khớp **nguyên văn** id và mo_ta của biên nhận, mỗi hàng đúng một lần. [evidence/receipt.json](evidence/receipt.json) lưu đủ năm hàng.

**Giới hạn không nâng thành phép đo.** Lượt hỏng có `failure_class=unknown`; stderr lưu chỉ **39 bytes**, nội dung `Reading additional input from stdin...`, không có lỗi HTTP. Nguyên nhân **401**, credential cũ và nạp lại **agent_creds rev 3** trong caveat là lời thuật lại; **KHÔNG ĐO ĐƯỢC** độc lập từ hiện vật đã lưu, dù đầu vào mô tả lượt hỏng là 401. Rc/thời lượng/no-VERDICT đã được đo riêng ở trên.

Phiên executor, chỉ thị chủ kho, credential push, GitHub submitter, exact CLI argv/version và model *được yêu cầu* không được run.json lưu đầy đủ để tái dựng; tính độc lập toàn bộ context và service identity phía ngoài run cũng **KHÔNG ĐO ĐƯỢC**. Phép đo chỉ xác nhận nội dung run/PROMPT/checkpoint và các trường phục vụ model/effort đã lưu. `sandbox_trang_thai=DO_DUOC` là quan sát lấy mẫu có giới hạn ngay trong run.json, không chứng minh mọi lệnh đều bị sandbox cưỡng chế. Trạng thái GitHub PR/check/branch protection/URL hiện tại và quyền merge/land: **KHÔNG ĐO ĐƯỢC** qua mạng trong review này.

**Toàn vẹn cuối.** `python3 finish_integrity.py` → [evidence/final-integrity.json](evidence/final-integrity.json): **10.905 tệp trước = 10.905 tệp sau**, `added=[]`, `removed=[]`, `modified=[]`; HEAD vẫn đúng SHA dòng 2; status rỗng. Chỉ đột biến trong bản sao tạm.

Nhật ký tăng dần trước khi chốt được giữ ở [evidence/VERDICT.progress.md](evidence/VERDICT.progress.md). Hai lỗi harness đã sửa, không tính thành finding: ban đầu audit byte giả định thư mục con có manifest riêng (thực tế manifest cha phủ đủ); đối chiếu base ban đầu nhầm với cha thứ nhất merge, sau sửa thành merge-base. Lần ghi JSON của audit CI ban đầu gặp `set` không serialize được; bản chạy hoàn tất và output cuối nằm ở evidence/ci.json. Các lỗi harness không được dùng làm bằng chứng PR thất bại.
'''
(S/'VERDICT.md').write_text(report,encoding='utf-8')
print('VERDICT written',len(report.encode()),'bytes')
print('\n'.join(report.splitlines()[:9]))
