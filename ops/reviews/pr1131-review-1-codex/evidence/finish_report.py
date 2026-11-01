from pathlib import Path
import json
S=Path(__file__).resolve().parent;E=S/'evidence'
receipts=json.loads((E/'receipts.json').read_text());history=json.loads((E/'history.json').read_text());bs=json.loads((E/'bytes.json').read_text());ci=json.loads((E/'ci.json').read_text());integrity=json.loads((E/'final-integrity.json').read_text())
assert receipts['failures']==history['failures']==[]
assert all(not r['errors'] and r['manifest']['rc']==0 and not r['manifest']['missing'] and not r['manifest']['extra'] and not r['manifest']['duplicates'] for r in bs['runs'])
assert ci['kiem_re_rc']==0 and ci['parse_failures']==[]
assert all(not integrity[x] for x in ('changed','added','removed'))
journal=(S/'VERDICT.md').read_text().split('\n',2)[2]
journal=journal.replace('Trạng thái: đang đo; verdict tạm thời chưa phải kết luận review. Chỉ ghi trong sandbox; phép thử có đột biến chạy trên bản sao tạm.','Nhật ký dưới đây đã được ghi tăng dần. Các báo lệch do bộ đo tự viết được giữ kèm phần hiệu chỉnh; kết quả cuối dùng các lần chạy đã hiệu chỉnh.')
report='''Verdict: approve
Reviewed commit: 0e824fe4c1ac674081c93c6f2098e5433c932890

Hoàn tất cross-review PR #1131 lượt 1: **approve — 0 P0, 0 P1, 0 P2, 0 P3** theo phạm vi offline được giao. Hai biên nhận khớp nguồn đo được; 170 tệp lưu khớp nguyên byte, 9 tệp bỏ khai đủ; README tăng đúng 10 hàng. Dòng trống cuối verdict lượt 2 đúng nguyên bản và không làm đỏ cấu hình CI hiện hành. Căn cứ và giới hạn của từng kết luận ở dưới. Không cấp quyền merge/land.

| Finding còn mở | Vị trí | Lệnh/output | Hướng vá |
|---|---|---|---|
| Không có (0/0/0/0) | — | Các phép đo dương/âm dưới đây | Không yêu cầu vá |

Ngưỡng áp dụng: không còn P0/P1/P2/P3. Mọi lệnh Python đo dùng `PYTHONDONTWRITEBYTECODE=1`; `git config core.abbrev 7` đã đặt trong `work/head` và `work/base`, git đọc clone gốc dùng `GIT_CONFIG_GLOBAL=$PWD/audit.gitconfig` với cùng giá trị, `GIT_OPTIONAL_LOCKS=0`. Các phép thử chạy trên bản sao; không sửa `cay-kho/`.

**Phạm vi và tính toàn vẹn.** `python3 audit_bytes.py` → `evidence/preflight.json`: `git rev-parse HEAD` = SHA dòng 2; tree `e3d867387abbcee063ab7b72803655d826bb0964`; status rỗng; `git diff --name-only 180039c HEAD` = **180 đường dẫn**, `outside_scope=[]`; `git diff 180039c HEAD` khớp `DIFF.patch`. `git log 180039c..HEAD` có đúng `9105a1a6f82915c0382edb2d3198c227c6d56d7b` và `0e824fe4c1ac674081c93c6f2098e5433c932890`. `python3 audit_history.py` đo `git merge-base HEAD origin/master` = `180039c4b791fba4c89991623151cbb7378fce53`.

**Cổng và delta.** `python3 measure_gates.py` chạy cùng lệnh trên `work/base` ở `180039c` và `work/head` ở SHA ứng viên; command/stdout/stderr nguyên văn ở `evidence/gates.json` và `evidence/{base,head}-*.stdout/.stderr`.

| Lệnh thật trong từng bản sao | Base | HEAD | Delta/kết quả |
|---|---|---|---|
| `python3 ops/bien_nhan_v2.py --root .` | rc0, 291 ĐẠT v2, tổng 344 | rc0, 293 ĐẠT v2, tổng 346 | +2 biên nhận đạt; cả hai 0 vi phạm, 0 KHÔNG ĐO ĐƯỢC; nợ/miễn trừ giữ nguyên |
| `python3 ops/land_evidence_nguon.py --root .` | rc0 | rc0 | Cùng 75 ĐẠT, 25/28 miễn trừ, tổng 100; 0 vi phạm, 0 KHÔNG ĐO ĐƯỢC |
| `python3 ../../direct_tests.py .` | rc0, 3 PASS | rc0, 3 PASS | Gọi trực tiếp mọi hàm `t26_*`/`t27_*`, gồm cả ca đuôi HOA; cùng SyntaxWarning nền |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | rc0 | rc0 | Cùng “đã quét 10 tệp, 0 chỗ chép doctrine” |
| `git diff --check 180039c HEAD` | rc0, rỗng | rc2 | Chỉ 2 thông báo `new blank line at EOF`, dòng 105 của hai bản verdict lượt 2 |
| `git -c core.whitespace=-blank-at-eol,-blank-at-eof,-space-before-tab diff --check 180039c HEAD` | rc0, rỗng | rc0, rỗng | Không phát sinh lỗi dưới cấu hình CI |
| Chính `ci_duong_nhanh.kiem_diff_check()` với base/head | `[]` | `[]` | Gồm `--attr-source=180039c…`, `--no-renames` và diff ba chấm đúng mã CI |

`python3 mutate_receipts.py` → `evidence/mutations.json`: đổi riêng 1 ký tự `verdict_sha256` của **từng** biên nhận mới trên bản sao. Bốn lần chạy (2 biên nhận × `bien_nhan_v2` và direct t26/t27) đều rc1, `only_expected=true`. `bien_nhan_v2` mỗi lần báo đúng **1 vi phạm**, “blob tại evidence_url băm … nhưng biên nhận khai …”; t26 FAIL “LỆCH BĂM”, hai t27 vẫn PASS. `git status --porcelain` sau hồi nguyên rỗng. Không suy đã thử đột biến mọi trường khác.

**Dòng trống cuối tệp và cổng CI khác.** `python3 audit_bytes.py` đo bản nguồn, bản lưu và bản phẳng lượt 2 cùng **16.314 bytes**, SHA256 `7beb37162f9a02089fea003b5db4261ada7f3c92d2b42d012c4db85b09d68331`, đuôi hex `657267652f6c616e642e0a0a` (hai LF). Vì vậy không sửa dòng trống của verdict nguồn.

`python3 audit_ci.py` → `evidence/ci.json`: dựng merge **mô phỏng local** từ base/head, tree trùng HEAD; chính classifier trả `duong_nhanh`; chính `lenh_kiem_re` rc0, output `kiem-re DAT (180 tep doi, 0 loi)`. Ghi argv subprocess thật: `git --attr-source=180039c… -c core.whitespace=-blank-at-eol,-blank-at-eof,-space-before-tab diff --check --no-renames 180039c…...0e824fe…` → rc0, stdout/stderr rỗng. Ca hiện hữu `t20d_kiem_re_khoang_trang_cuoi_dong_khong_do()` PASS, kiểm cả chiều mặc định đỏ và CI xanh trên fixture.

Tìm bằng `git grep -n -e --check -- '*.py' '*.sh' '*.ps1' '*.yml' '*.yaml' ':!ops/reviews' ':!ops/land' ':!ops/specs' ':!docs'` → `evidence/all-check-calls.txt`, rồi AST trong `audit_ci.py` trên **131 tệp Python hoạt động** → không lỗi parse. Các call site chính xác mang `diff`/`--check` chỉ ở `ops/ci_duong_nhanh.py:466` và `ops/ci_duong_nhanh_test.py:865,870,936,956,983,1059`. Các call site trong selftest dùng kho fixture tạm; không áp check nghiêm lên diff PR này. `.github/workflows/ci.yml:688–702` gọi `kiem-re` khi `duong_nhanh`; dòng 705–707 gọi selftest đó. Các nhắc trong `scripts/tl_selftest.py:22705,22755` là comment lịch sử. **Không tìm thấy cổng khác chạy `--check` nghiêm hơn trên diff PR trong mã/workflow tại HEAD.** Đây không phải xác nhận trạng thái run GitHub thực tế.

**Byte và khai tệp bỏ.** `python3 audit_bytes.py` dùng duyệt đệ quy có tệp ẩn, ánh xạ theo chỉ thị; `evidence/bytes.json` ghi mỗi source/target/hash/bytes, lỗi và độ phủ manifest.

| Thư mục nguồn → thư mục kho | Tệp nguồn | Khớp byte | Bỏ, khai hash/bytes đúng | Thiếu khai/lệch byte |
|---|---:|---:|---:|---:|
| `review1119b` → `pr1119-review-1-codex` (không đếm lặp lượt hỏng) | 80 | 77 | 3 | 0 |
| `review1119a` → `pr1119-review-1-codex/luot-hong-dia` | 12 | 9 | 3 | 0 |
| `review1119c` → `pr1119-review-2-codex` | 87 | 84 | 3 | 0 |

`sha256sum -c SHA256SUMS` trong thư mục lượt 1 → rc0, **88/88** mục OK, phủ cả lượt hỏng; trong lượt 2 → rc0, **85/85** mục OK. Mỗi manifest phủ mọi tệp dưới cây trừ chính nó; missing/extra/duplicates đều `[]`. Lượt hỏng được manifest cha bao phủ, không cần manifest riêng. Tệp sinh thêm chỉ gồm `OMITTED.txt`/`SHA256SUMS`; không có đích không ánh xạ được. Hai bản phẳng khớp `VERDICT.md`: lượt 1 **15.330 bytes**, SHA256 `a28c2594116bff50653a6486fa07fd97cb2ad5e6b440c43277ad644f2f014d65`; lượt 2 như trên.

Chín tệp vắng gồm mỗi lượt một `DIFF.patch`, `launcher.err` rỗng và một ảnh chụp lớn: lượt 1 `evidence/repo-before.json` **1.455.011 bytes**; lượt hỏng `evidence/original-snapshot.json` **1.455.295 bytes**; lượt 2 `evidence/original-hashes.json` **1.819.869 bytes**. Từng sha256 trong `OMITTED.txt` khớp hash tự tính ở `evidence/bytes.json`. `python3 audit_receipts.py` tái lập `git diff f4b513d a8f7470` → **710.702 bytes**, SHA256 `29910d47cde0b30c4f0b3d6436a0c38d92dfa58d256a4f33aea8a5a19c934203`, bằng nguồn lượt 1 và lượt hỏng; `git diff c82047d 8715ac9` → **711.699 bytes**, SHA256 `dff14de1573c20bc2a256fb8823b19a366b3173e67f898482dddf6e6c9342034`, bằng nguồn lượt 2. Diff bổ sung giữa hai reviewed SHA dưới `ops/reviews/` và verdict lượt 1 lưu trong lượt 2 cũng khớp byte.

**Biên nhận.** `python3 audit_receipts.py` → **291 đối chiếu, failures=[]**, chi tiết expected/actual/lệnh git ở `evidence/receipts.json`.

| Trường đo từ verdict/run/git | Lượt 1 | Lượt 2 |
|---|---|---|
| verdict / assurance / P0,P1,P2,P3 | `changes_requested` / `cross_reviewed` / 0,0,0,2 | `approve` / `cross_approved` / 0,0,0,0 |
| findings_ids | `bo-sot-cache-khong-khai`, `caveat-loai-diff-sai`, đều P3 | `[]` |
| reviewed SHA | `a8f74709578f3c68833d366ed80b66fc10fbf0a3` | `8715ac9f591b27d9b176e9d656437ef4b71b54dc` |
| reviewed tree | `66458c331fca22ac5dd497e756f18a80179302f2` | `ad90d9046a4367e0649a2f812daccdb2b0622af7` |
| run_id | `feeb867a075142f8af1b0823c7e2be79` | `89d650769c354435a475508fc7992825` |
| ma_thoat / trạng thái / giây | 0 / xong / 619.803 | 0 / xong / 540.166 |
| sự kiện / model / effort | 22 / toàn bộ `gpt-6-astra` / `xhigh` | 20 / toàn bộ `gpt-6-astra` / `xhigh` |
| prompt_sha256 | `b5bc5f43c50cd01c21bc63dc81a4ef5167447b90e94caa6324e7702929fbf014` | `29929370805223ca84cb9e881fb713da7c0686887bcc977bc5199172a1c5a78d` |
| sandbox_trang_thai / worktree_sach khi phóng | DO_DUOC / true | DO_DUOC / true |
| `_tinh_lop_tu_write_set(diff base..reviewed_sha)` | 254 tệp, sensitive | 254 tệp, sensitive |

`git show -s --format=%P 180039c` → cha 1 `c82047da4d6f9546ce1d68282c37acf9567b74bc`, cha 2 `8715ac9f591b27d9b176e9d656437ef4b71b54dc`; message chứa `Merge pull request #1119`. `git merge-base --is-ancestor a8f7470 180039c` rc0. Hai `evidence_url` trỏ đúng blob tại `9105a1a6f82915c0382edb2d3198c227c6d56d7b`, commit này là tổ tiên HEAD (rc0), hash blob bằng hash verdict khai trong biên nhận. `launcher.out` decode bằng `run.json`; checkpoint/run/prompt và hash/bytes stdout/stderr khớp; thời lượng tính từ timestamp khớp tới 0,001 giây.

Đối chiếu tiền lệ `pr1058-review-{1,2}`, `pr1110-review-{1,2}`, `pr1114-review-{1,2}`: 21 trường cấu trúc/identity mỗi cặp không lệch; riêng `pr1058` giữ đúng mapping `changes_requested` → `cross_reviewed`, `approve` → `cross_approved`. Khác biệt findings/head/caveat tương ứng dữ liệu từng lượt, không thấy lệch tiền lệ không lý do (`evidence/receipts.json`, nhóm `precedent.*`).

**Xử lý finding lịch sử và lượt hỏng.** `python3 audit_history.py` → **56 đối chiếu, failures=[]** (`evidence/history.json`). `6379bc5d784eb9af103b79cc074e4766c0516ae5` nằm sau reviewed SHA lượt 1 và trước lượt 2 (hai ancestry rc0); đúng 5 tệp sửa, nội dung ở commit vá được giữ tới `8715ac9`. Ba khai báo cache mới có đường dẫn/hash/bytes khớp bằng chứng `closure.json` của lượt 2; hai caveat #1114 và hai hàng README chuyển sang khai `DIFF.patch CO trong kho`. Tự dựng lại hai DIFF #1114 từ git cho **1.913/4.160 bytes**, khớp hash và manifest. Các số 237 bản sao, 13 tệp bỏ, 4 biên nhận, +23 hàng trong `ket_luan` lượt 2 khớp verdict và JSON nguồn; đây là kiểm lời thuật lịch sử, không tự khai chạy lại review #1119.

Run hỏng `e9bd849279954310b67722bef764b7f4` có head `a8f7470`, `ma_thoat=0`, `trang_thai=xong`, **221.882 giây**, nhưng stdout nói “Chưa hoàn tất review… No space left on device”; VERDICT ghi rõ “Trạng thái tạm thời”. Vì vậy rc0 launcher không biến nó thành lượt review hoàn chỉnh; caveat loại khỏi hai lượt chính phù hợp hiện vật. VERDICT tạm có preflight HEAD/tree/status, chưa có kết luận review hoàn tất; cụm “chua do gi” được đọc trong ngữ cảnh chưa hoàn tất phép đo nội dung, không phủ nhận preflight đã ghi.

**README.** `python3 audit_receipts.py` dùng multiset mọi hàng bắt đầu `| `: **1240 → 1250**, added=10, removed=0, chỉ đúng tập mong đợi. Hai hàng mục lục khớp verdict/receipt, số lượt, assurance, P*, head, bytes, model/run; tám hàng caveat (5+3) khớp nguyên văn `id` và `mo_ta` trong biên nhận. Từng hàng ở `evidence/receipts.json.readme` và từng phép kiểm `README.*`.

**Giới hạn đo.** Trạng thái PR/check/run/submitter/quyền trên GitHub thực, merge ref GitHub hiện tại, CLI version `0.164.0`, argv đầy đủ (`--expected-head`, `--require-clean`), danh tính/độc lập context phía máy chủ, model executor thực tế: **KHÔNG ĐO ĐƯỢC độc lập** từ bộ tệp offline này. `run.json` chỉ lưu chương trình/số đối số/vân tay của argv; stderr đã lọc. Đo telemetry chỉ xác nhận hiện vật cung cấp, không chứng thực nhà cung cấp phía máy chủ. Raw cache của sandbox #1114 và trạng thái đĩa/inode lúc run hỏng không được cấp: **KHÔNG ĐO ĐƯỢC** lại; chỉ đối chiếu git và bằng chứng lưu của lượt đó. Không chạy toàn bộ CI/selftest hay suite lịch sử; chỉ chạy các cổng/ca nêu trên và phép bổ sung `t20d`/đường nhanh local.

`python3 final_integrity.py` → rc0 (`evidence/final-integrity.json`): **10.638 → 10.638 tệp** trong checkout gốc, gồm tracked/untracked/ignored ngoài nội bộ `.git`, changed/added/removed đều `[]`; status rỗng; HEAD/tree giữ nguyên. Hai biên nhận trên bản sao đã hồi nguyên byte. Ảnh chụp trước/sau chứng minh không có delta quan sát ở hai mốc, không chứng minh mọi thời điểm giữa hai mốc.

**Nhật ký tăng dần** (giữ kết quả trung gian và hiệu chỉnh bộ đo):
'''
report+='\n'+journal+'\nHiệu chỉnh kiểm caveat SCRIPT-DO-DOC-DUONG-DAN-SANDBOX: lần đầu audit_history.py chỉ tìm đường dẫn tuyệt đối trong *.py, bỏ phần “bằng chứng” của câu gốc; đã mở đúng phạm vi script hoặc evidence, đo lại 56 đối chiếu đều khớp. Bản đầu lưu `evidence/history-attempt1.*`. Không phải finding của candidate.\n'
(S/'VERDICT.md').write_text(report)
print('final verdict written',len(report.encode()),'bytes')
print('\n'.join(report.splitlines()[:10]))
