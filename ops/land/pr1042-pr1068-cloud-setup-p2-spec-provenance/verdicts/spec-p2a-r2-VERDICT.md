verdict: approve
reviewed_sha: 019d044739068d393e7067d3b88250e90c492713
reviewed_tree: 7cc8e189115f72d1befc749348f676f67a822d1f

Reviewer: `openai_codex`, phiên độc lập có công cụ shell trực tiếp, transport `machine`; không đăng GitHub. Không có receipt launcher trong lượt này để tự đo model/effort đã phục vụ, nên không tự cấp assurance `do_may`. Phạm vi: review đặc tả S-A2/errata r2; chỉ đối chiếu mã #1063 để kiểm lời khai đặc tả, không review lại code đã land. Ngưỡng áp dụng theo prompt: không còn bất kỳ P0–P3 nào mới approve.

## (i) DANH TÍNH VÀ PHẠM VI SỬA

Neo HEAD/tree khớp. Lệnh đầu tiên trên cây:

```text
$ git -C cay-kho rev-parse HEAD 'HEAD^{tree}'
019d044739068d393e7067d3b88250e90c492713
7cc8e189115f72d1befc749348f676f67a822d1f
```

Các phép đo danh tính tiếp theo (rc 0; `diff` khác nhau có rc 1 theo quy ước):

```text
$ git -C cay-kho status --porcelain=v1 --untracked-files=all
(không có output)
$ git -C cay-kho diff --name-status 97120d3c76ebb7c3eda4b585ff46f1c51e30c91b HEAD
A\tops/specs/cloud-setup-p2a-exec-r2.md
$ git -C cay-kho rev-parse HEAD:ops/specs/cloud-setup-p2a-exec-r2.md
6dc7ff17032ab9e8313d939ca0ef3af9a973f82b
$ git -C cay-kho hash-object ../SPEC.md
6dc7ff17032ab9e8313d939ca0ef3af9a973f82b
$ git -C cay-kho rev-parse HEAD:ops/specs/cloud-setup-p2a-exec-r1.md
d7d4e240a181c7b68dea72b0be0393e334544b75
$ sha256sum SPEC.md SPEC_R1.md cay-kho/ops/specs/cloud-setup-p2a-exec-r2.md cay-kho/ops/specs/cloud-setup-p2a-exec-r1.md
3de590bea4d26de3cf931df0757140a27fd36a2206f2ef381b95247f22563fed  SPEC.md
1071797a1cf2016a9266a98ccece02ed6edd4e80ca33d3b91b2547f7ca0c13e1  SPEC_R1.md
3de590bea4d26de3cf931df0757140a27fd36a2206f2ef381b95247f22563fed  cay-kho/ops/specs/cloud-setup-p2a-exec-r2.md
1071797a1cf2016a9266a98ccece02ed6edd4e80ca33d3b91b2547f7ca0c13e1  cay-kho/ops/specs/cloud-setup-p2a-exec-r1.md
$ cmp SPEC.md cay-kho/ops/specs/cloud-setup-p2a-exec-r2.md
(không có output)
$ cmp SPEC_R1.md cay-kho/ops/specs/cloud-setup-p2a-exec-r1.md
(không có output)
$ diff -u SPEC_R1.md SPEC.md > diff_r1_r2.patch
rc=1; đã tự tạo lại tệp diff.
```

Tất cả neo khớp; diff base→HEAD chỉ thêm đúng tệp r2. Đã tự chạy lại diff hai lần, rc=1 đúng quy ước; hai artifact diff giống nhau.

| Hunk của `diff -u` | Dòng thật thay đổi (r1 → r2) | Phân loại |
|---|---|---|
| `@@ -1,9 +1,11 @@` | 1 → 1; 3–6 → 3–8 | Tiêu đề, revision và metadata, ghi rõ r2 là errata, packet đã land với ba ngoại lệ |
| `@@ -40,7 +42,8 @@` | 43 → 45–46 | F1: cho thêm fixture deny theo mục tiêu 10 |
| `@@ -139,7 +142,7 @@` | 142 → 145 | F2: đúng hai trường JSON, bắt buộc cả hai hiện diện |
| `@@ -194,10 +197,24 @@` | bỏ r1:197; thêm r2:206–220 | F3: bỏ fileId khỏi chưa đo; thêm mục `errata_r2` |

Lệnh `python -B review_evidence/measure_static.py` rc=0. Script dùng `SequenceMatcher` trên **bytes có giữ newline**, kiểm đúng 8 dòng r1 được thay/bỏ: `[1,3,4,5,6,43,142,197]`; chèn cuối tệp là `errata_r2`. Phần còn lại bằng từng byte: **23119 byte**, SHA-256 `3e6a81c5e29614a51f568bd8f554de7dac041ad930c2dbb57e68f879f24c71ce`. Không có hunk ngoài các loại cho phép. Bằng chứng: `review_evidence/static.json`, `review_evidence/diff-recomputed.patch`.

## (ii) ĐÓNG F1/F2/F3

ĐỐI CHIẾU LƯỢT TRƯỚC: nguồn `VERDICT_SA_r1.md`, reviewed SHA `eb7242561f5dd99071991cbc38528bdb3cb1cf52`, tree `726ad3571166cf11709882e3c0e974bfe6acf328`. Cả ba finding được tự đo lại dưới đây, không nhận lời khai đã sửa làm bằng chứng.

### F2 — J1: ĐÃ VÁ THẬT

Đã chạy CLI thật của cây hiện tại bằng runner offline, sau `unset` bắt buộc:

```sh
unset TL_MASTER_KEY TL_AGENT_CREDS_FILEID CLAUDE_CODE_OAUTH_TOKEN GEMINI_API_KEY
python -B review_evidence/run_offline.py release_verify
```

Runner đặt `argv` đúng `scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json`, chạy entrypoint bằng `runpy`, giữ cây chỉ đọc, HOME/TMP/cache dưới `review_evidence/`, môi trường tối thiểu, chặn network và mở credential thật.

Output trích từ JSON thật, rc=0:

```json
{"ok": true, "strict": true, "expected_file_count": 195, "checked_file_count": 195, "failed": [], "errors": [], "package_hash_match": true}
```

Log đầy đủ: `review_evidence/release_verify.stdout`; stderr rỗng; audit `{"denied_events": []}`. J1 r2 dùng đúng hai tên trường và đòi có mặt trước so; không có nhu cầu alias `expected`/`checked`.

Đã parse JSON để kiểm trực tiếp: `release_keys_exist=true`, `old_aliases_absent=true`, `counts_equal=true` (hai alias cũ `expected`, `checked` đều vắng). Độ tin: cao.

### F1 — write set / mục tiêu 10: ĐÃ VÁ THẬT

r2:45–46 cho phép thêm fixture deny, khớp yêu cầu r2:109–110. AST của t50 trong cha thứ nhất của merge #1063 có 2 agent × 4 dạng đường dẫn × 3 lệnh = 24 ca; bản đã land và HEAD cùng có thêm đúng `agent-creds-exec --claude -- x` với kỳ vọng deny, nên thành 2×4×4=32. Nội dung t50 land/HEAD giống nhau; không đổi thuật toán vòng lặp, chỉ thêm fixture và cập nhật mô tả/tổng 24→32.

```sh
python -B review_evidence/measure_static.py
unset TL_MASTER_KEY TL_AGENT_CREDS_FILEID CLAUDE_CODE_OAUTH_TOKEN GEMINI_API_KEY
python -B review_evidence/run_offline.py t50
```

Hai lệnh rc=0; output t50 thật:

```json
{"ok": true, "detail": "2 agent x 4 cach viet x 4 lenh -> dung 32/32"}
```

Chỉ gọi fixture t50 có sẵn, không soạn chuỗi vượt guard. stderr rỗng, audit không có denied event. Nguồn trích riêng: `review_evidence/t50-base.txt`, `t50-land.txt`, `t50-head.txt`; số đo AST: `static.json`.

`git -C cay-kho diff 69dcfee9 HEAD -- .claude/hooks/pretooluse_guard_test.py` rc=0, output rỗng (`review_evidence/t50-land-head.diff`): toàn tệp test ở HEAD khớp bản đã land. Độ tin: cao.

### F3 — trạng thái fileId: ĐÃ VÁ THẬT

Lệnh static ở trên rc=0: AST `scripts/tl_gws.py` có `AGENT_CREDS_FILEID = 1I0-p-FKSy3255OUNv7xkhRACy3k1zqWQ`. r2 chứa ID ấy đúng 4 lần: mục tiêu 3, B1, kết quả LIVE 5, errata F3. Mục `chua_do_duoc` không còn fileId. Không đọc bản mã/credential, không gọi LIVE để đo lại nội dung bundle. F3 là lỗi trạng thái văn bản, đã đóng đúng.

```text
$ python -B review_evidence/measure_static.py
rc=0
fileid_source: 1I0-p-FKSy3255OUNv7xkhRACy3k1zqWQ
fileid_occurrences_r2: 4
fileid_in_chua_do_duoc: false
```

Độ tin: cao về trạng thái văn bản và hằng trong code; không khẳng định đã kiểm credential/bundle thật.

Lượt harness đầu: script static lỗi ghép list/bytes; runner t50 chặn cả `os.posix_spawn` hợp lệ của Python gọi guard. Đã sửa riêng harness ngoài kho và chạy lại thành công, giữ hai lượt lỗi trong `review_evidence/*first*`; không nhận lượt lỗi là pass.

## (ii) FINDING MỚI CỦA r2

**Không có finding P0–P3 trong phạm vi đã review.** Đã đối chiếu cả nội dung mới với văn bản r1 còn giữ và mã đã land:

| Khẳng định/khả năng mâu thuẫn | Phép đo và kết quả | Đánh giá |
|---|---|---|
| Packet đã land ở #1063 | `git -C cay-kho merge-base --is-ancestor 69dcfee9 HEAD`: rc=0, không output | Merge #1063 là tổ tiên HEAD; phù hợp metadata mới |
| Errata F1 mô tả t50 | AST trước/sau, diff và ca t50 thật ở trên: 24→32; chỉ thêm fixture deny của lệnh mới, tổng/mô tả khớp | Đúng với phần đã land; không có mâu thuẫn write set / mục tiêu 10 còn mở |
| Ba ngoại lệ được viện dẫn tại đầu r2 | Đọc bản chụp comment ID `6539003369` trong `ops/land/pr1063-wp1038-r1-provenance/readback-comments-1038.json`; trích nguyên nội dung sang `review_evidence/approved-exceptions.txt` | Đúng ba mục (a) parser, (b) S5 guard, (c) trần 550 dòng; bản chụp tự khai caveat agent chép lời chủ kho (#566), không coi là lần xác nhận online mới |
| (a) `allow_abbrev=False` cho parser gốc và hai cha LONG | `git -C cay-kho diff --unified=2 69dcfee9^1 69dcfee9 -- scripts/tl_core/cli.py`: rc=0; diff có `allow_abbrev=False` ở parser gốc và các parser chứa subparser | Khớp ngoại lệ parser; không coi đây là phần tự mở quyền mới của r2 |
| (b) S5 guard và test bảo vệ | Đọc diff/source guard, AST test: ngoài t33 (105→106) và t50, chỉ thêm t51/t52; guard có danh sách đọc, nối dòng, `commenters=""`, xử lý cờ giá trị và regex `\w` Unicode như ngoại lệ đã khai | Các ca mới thuộc phần S5 được viện dẫn; không có ca cũ khác bị đổi thuật toán để hợp thức hoá fixture F1 |
| Số đếm guard | `python -B review_evidence/measure_static.py`: rc=0, `_TL_LENH_GHI=99`, `_TL_LENH_GHI_LONG=7`, tổng writer=106, `_TL_LENH_DOC=93`; `agent-creds-exec` nằm trong bảng ghi | Khớp số 106 ở t33/mục tiêu 10 và 93 của ngoại lệ S5 |
| (c) Trần dòng cũ 450 so với code đã land | `git -C cay-kho diff --numstat 69dcfee9^1 69dcfee9`: rc=0; cộng 13 hàng = **13 tệp, +524/−58** (`review_evidence/land-numstat.txt`) | 524≤550 theo ngoại lệ (c). Các dòng 450 giữ nguyên là hợp đồng r1 được metadata r2 dẫn kèm ngoại lệ; không diễn giải chúng thành lời khai code land chỉ có ≤450 dòng |
| J1 và số tệp manifest | CLI thật rc=0, `ok=true`, hai key đúng cùng bằng 195 | 193 trong thân spec là số đo lịch sử có mốc/base, không phải đòi count của HEAD phải là 193 |
| Giới hạn chưa đo | Phần còn lại của `chua_do_duoc` giữ nguyên từng byte; r2 không biến agy/Claude thật, Windows Ctrl-C, lease/nền/số dòng thành bằng chứng đã pass | Giữ đúng giới hạn đã khai, không tính thành finding theo prompt |

Không phát hiện tiêu chí mới không đo được hoặc lời khai sai mới. Đây là đánh giá đặc tả trên dữ liệu offline, không xác nhận lại mọi gate hay thao tác LIVE của packet đã land.

## (iii) KẾT LUẬN

**approve**, neo `019d044739068d393e7067d3b88250e90c492713` / tree `7cc8e189115f72d1befc749348f676f67a822d1f`. Danh tính và phạm vi sửa đúng; F1/F2/F3 đều **ĐÃ VÁ THẬT**. Finding còn mở: **P0=0, P1=0, P2=0, P3=0** (0 lớp, 0 biểu hiện).

Kiểm cuối (`review_evidence/final_git.json`), mọi lệnh rc=0:

```text
$ git -C cay-kho rev-parse HEAD 'HEAD^{tree}'
019d044739068d393e7067d3b88250e90c492713
7cc8e189115f72d1befc749348f676f67a822d1f
$ git -C cay-kho status --porcelain=v1 --untracked-files=all --ignored=matching
(không output)
$ git -C cay-kho diff --exit-code
(không output)
$ git -C cay-kho diff --cached --exit-code
(không output)
$ git -C cay-kho diff --name-status 97120d3c76ebb7c3eda4b585ff46f1c51e30c91b HEAD
A    ops/specs/cloud-setup-p2a-exec-r2.md
```

SHA-256 cuối của SPEC/SPEC_R1 giữ đúng các giá trị ở (i). Không sửa cây `cay-kho/`; mọi harness/cache/output ở ngoài cây. Sandbox thực tế là workspace-write, cây được đối xử read-only; snapshot sạch chỉ chứng minh không có delta quan sát được ở các mốc, không chứng minh lịch sử không từng ghi/hoàn nguyên.

`passed`: identity/hash/phạm vi byte-diff, đối chiếu F1–F3, t50 32/32, release-verify strict 195/195 và snapshot cuối. Hai lỗi harness ban đầu là `failed` của harness, đã ghi và sửa ở scratch rồi chạy lại. `not_run`: full guard suite, full selftest hai nền, bare Ruff lint, CI online, LIVE, agy, Claude thật, Windows thật; không coi chúng là pass và không dùng việc chưa chạy làm finding của errata này. Không gọi mạng/Drive/NLM/webapp, không tải/chạy agy, không đọc/ghi credential thật.
