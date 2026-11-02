verdict: approve
reviewed_sha: 0eb66e513f2736f0bfc342ddbcbc70b84f773b3b

Approve trong phạm vi xác minh merge của lượt 4/4, packet wp981 r2, lớp `sensitive`. Không phát hiện finding P0/P1/P2/P3 mới. Hai tệp write set giữ nguyên từng byte; tree đúng kết quả hợp nhất hai cha. Bộ test đạt **11/11, rc 0**. Cổng L-6 trả **23/23 hồ sơ landed đạt, rc 0**, không `TRUOT`/`LOI`. Kết quả của cả **78 hồ sơ** giống từng byte với cha 1.

**Phạm vi, authority và danh tính.** Nguồn giao việc là `runs/8eb247e7/prompt.snapshot`: mở lượt thứ tư theo #981 issuecomment-6512475787 để bổ sung hồ sơ land PR #1027. Ngưỡng áp dụng: không còn P0/P1/P2 mới được approve. Đã đọc verdict lượt 3, đặc tả và các quy tắc reviewer liên quan trong AGENTS/CONTEXT/PROTOCOL/CLAUDE/kế hoạch đa provider. Không kiểm chứng comment, trạng thái PR hoặc việc merge vào master qua mạng vì assignment cấm mạng. Đây là verdict nội dung trên exact SHA, không cấp quyền land hoặc chứng nhận mọi gate phát hành.

Reviewer là Codex, provider `openai_codex`, họ model `openai` theo cấu hình phiên; session review này độc lập với executor, không nhận context executor. Thực thi qua phiên API có công cụ shell cục bộ, transport `machine`; sandbox `workspace-write`, checkout được giao nằm ngoài vùng cho phép ghi. Không có receipt runtime độc lập để đo model ID/effort thực phục vụ, subtype CLI/Desktop/service, hoặc danh tính runtime executor; phần đó là `khong_do_duoc`. Executor `claude` là thông tin assignment. Không tự nâng lời khai này thành assurance `cross_approved` đã được máy chứng nhận; phiên điều phối cần ghép receipt thực thi theo §8.1. Không đăng GitHub, không có GitHub submitter trong lượt này.

Môi trường đã đo: Linux x86_64, Python 3.13.17 (`/usr/bin/python`), Git 2.43.0, PyYAML 6.0.3 ([environment.json](evidence/environment.json)). Các phép chạy Python dùng `-B`, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPYCACHEPREFIX=$PWD/evidence/pycache`, `TMPDIR=$PWD/evidence/tmp`. Các phép Git sau snapshot đầu đặt `GIT_OPTIONAL_LOCKS=0`; driver ghim `core.abbrev=7` theo từng lệnh, không ghi Git config.

**Mốc Git và đặc tả đã tự đo.**

- Checkout: `/home/user/wp981-rv4/cay-kho`.
- HEAD: `0eb66e513f2736f0bfc342ddbcbc70b84f773b3b`; tree: `04702940110da99d13068b5857f04cedc8d2c3ae`.
- Cha 1: `afd3a861bdaed63ada0f24ee8dbf2af166e86178`; cha 2: `44884446f71c89e25f9a72ac58e4f597db63c1ba`.
- Merge-base hai cha: `20a2e2b3dd52a83442c739d17db1f1bd66181a6c`.
- SHA-256 bản `SPEC.md` đi kèm: `3d026415193d3f3b1ceef005cdc99fcc73871b0c7539697f82b4b0198f578079`, đúng assignment. Đường dẫn `ops/specs/wp981-r2.md` không hiện diện trong checkout; review dùng chính bản đi kèm đã xác minh hash, không giả định đã đọc tệp ấy từ HEAD.

[Driver tái chạy](evidence/review.py) đặt mọi output/fixture dưới `evidence/`; các lời gọi con lưu argv, cwd, rc, stdout và stderr tại `evidence/logs/*.json`, kèm `.out`/`.err`. Các lệnh driver dưới đây chạy từ thư mục chứa verdict. Lệnh Python sản phẩm dùng đường dẫn tuyệt đối, cwd ở thư mục verdict; dữ liệu thật được chỉ định bằng `--root`.

**Tính toàn vẹn write set và merge.** `python -B evidence/review.py integrity` rc 0 ([output](evidence/integrity-summary.out)). Lấy blob bằng `git cat-file blob`, OID bằng `git rev-parse SHA:path`, so bytes trực tiếp và tự băm SHA-256 tại HEAD, cha 1, head lượt 2 `2c70821245f777ede564c79e4e4abade0de53ae6`; đồng thời so với bytes trong checkout.

| Tệp | Blob OID chung ở cả ba commit | SHA-256 chung | Kết quả |
|---|---|---|---|
| `ops/kiem_ho_so_land.py` | `846f3697dc453f349852a613ed9a2ec7ab369569` | `5ee2385db62ce529200ee936dda28481ed94182907e58acf7974c977025b4fe4` | Giống từng byte |
| `ops/kiem_ho_so_land_test.py` | `45874c6be6286406ea780ae9d9d489662da446bb` | `943fabb42682a62749c1b972bbd5fab76d830db3c967bd7dc5c72ecb5d67b68c` | Giống từng byte |

`git -C /home/user/wp981-rv4/cay-kho diff-tree --cc 0eb66e513f2736f0bfc342ddbcbc70b84f773b3b` trả rc 0, chỉ in OID commit và xuống dòng (41 byte), không hunk. Thêm `--no-commit-id` cho stdout 0 byte. Không dựa riêng vào combined diff để kết luận: so các mục `git ls-tree -rz --full-tree` theo path/mode/type/OID cho merge-base, hai cha và HEAD chứng minh:

```text
MASTER_CHANGED 110 MATCHES_SUPPLIED_LIST=True WRITE_SET_OVERLAP=0
TREE_UNION_EXACT=True p1_changed=2 master_changed=110 overlap=0 entries=7358
```

Nội dung cuối không có sửa resolve bổ sung ngoài hợp nhất sạch của hai cha; phép đo không suy đoán thao tác bàn phím lịch sử. Diff cha 2→HEAD vẫn đúng hai tệp packet, lần lượt `47/11` và `137/3` dòng thêm/xóa, tổng **184 dòng thêm** ([numstat](evidence/logs/packet-numstat.out)).

**Chạy thật và so từng hồ sơ.** Ba lệnh yêu cầu đã chạy trên exact checkout, mỗi lệnh rc 0:

```text
python -B /home/user/wp981-rv4/cay-kho/ops/kiem_ho_so_land_test.py
11/11

python -B /home/user/wp981-rv4/cay-kho/ops/kiem_ho_so_land.py --root /home/user/wp981-rv4/cay-kho
TỔNG: 23/23 hồ sơ landed True đạt · 0 miễn trừ · rc=0

python -B /home/user/wp981-rv4/cay-kho/ops/kiem_ho_so_land.py --root /home/user/wp981-rv4/cay-kho --json
n_dat=23; n_landed=23; n_mien_tru=0; rc=0; len(tep)=78
```

Dòng cuối trên là trích các trường JSON, không phải nguyên văn toàn stdout. Log gốc: [suite](evidence/logs/unit-head.json), [text đầy đủ](evidence/logs/head-text.out), [JSON đầy đủ](evidence/logs/head-json.out). **Mọi dòng `TRUOT`/`LOI` trên cây thật: không có (0 dòng).** 55 hồ sơ còn lại là `BO_QUA`; không hồ sơ nào cần miễn trừ.

Dựng toàn cây cha 1 bằng `git archive --format=tar -o <evidence/parent.tar> afd3a861bdaed63ada0f24ee8dbf2af166e86178`, rồi giải nén vào `evidence/parent/`. Không dùng `git worktree` để tránh thay metadata của kho được review. SHA-256 archive: `f3fa5dbeb2f28c0b9ccc3411dc86aced1d681f5f974aac7334e690d724f61fdb`. Đã chạy **script của cây cha 1** với `--root <evidence/parent> --json`, không chỉ thay dữ liệu cho script HEAD ([argv/rc/output](evidence/logs/parent-json.json)).

`python -B evidence/review.py data` rc 0 ([output](evidence/data-summary.out)):

```text
DATA_AB_JSON_BYTES_EQUAL=True parent_rows=78 head_rows=78 changed_rows=0
LAND_FILES_BYTES_EQUAL=True count=78 added=0 removed=0 modified=0
```

Đối chiếu bao gồm tên tệp, trạng thái, toàn bộ lý do, thứ tự, các tổng và rc. Có bảng đủ **78/78 hồ sơ**, không chỉ sáu hồ sơ được nhấn mạnh: [TSV](evidence/per-record-comparison.tsv), [JSON có cả lý do trước/sau](evidence/per-record-comparison.json).

| Hồ sơ kiểu (b) | Cha 1 | HEAD | Nguồn landed |
|---|---|---|---|
| `pr870-claude-md-bai-hoc-c` | DAT | DAT | `landed_20261026.landed` |
| `pr889-claude-md-bai-hoc-c` | DAT | DAT | `landed_20261026.landed` |
| `pr896-claude-md-bai-hoc-c-tro-nguon` | DAT | DAT | `landed_20261027.landed` |
| `pr924-wp923` | DAT | DAT | `landed_20261027.landed` |
| `pr950-wp834` | DAT | DAT | `landed_20261027.landed` |
| `pr963-wp943` | DAT | DAT | `landed_20261027.landed` |

**Ảnh hưởng của 110 tệp master mang vào.** Tập path tự sinh khớp chính xác `tep_master_mang_vao.txt`; **không có tệp nào dưới `ops/land/`**, vì vậy không có `*-land-evidence.yaml` mới, sửa hoặc xóa. SHA-256 từng tệp trong 78 hồ sơ cũng được đối chiếu, không chỉ tên hoặc số lượng.

Đã chạy `rg -n kiem_ho_so_land /home/user/wp981-rv4/cay-kho` (104 dòng), rồi quét thêm `--hidden -g '!.git'` (105 dòng; bổ sung mục sổ test ở `.claude/dev/ci_dang_ky_test.py:54`). [Log rg](evidence/rg-callers.out), [log có tệp ẩn](evidence/rg-hidden-callers.out). `git grep -n` trên cả hai commit cho **105 tham chiếu giống nhau** sau khi bỏ tiền tố SHA.

Trong 110 tệp, chỉ `.claude/dev/ci_dang_ky_test.py` chứa tham chiếu này. Diff của nó chỉ sửa/thêm hai chú thích về timeout; toàn AST trước/sau giống nhau. Phép thử chạy hàm `bang_chung_xanh` được trích nguyên từ AST hai bản với chính marker đăng ký: nhận stdout thực `11/11`; từ chối `10/11`, `0/0` và thiếu marker ở cả hai bản. Đây là phép đo hợp đồng marker, không phải chạy toàn bộ registry gate. `requirements.txt` và `.github/workflows/ci.yml` giống bytes. Gate chỉ import `argparse,json,pathlib,re,sys,yaml`; các thay đổi `scripts/tl.py`, backup config trong `tl_core`, VERSION/manifest, tài liệu và hiện vật wp960 không nằm trong đường import này. Không phát hiện caller/import mới hoặc thay đổi hành vi L-6 do merge. Quét chuỗi không tự chứng minh mọi lời gọi động đều vắng; kết luận dựa thêm vào tập thay đổi đóng, AST, đường import và phép đo A/B.

**Bảng SĂN — các hướng độc lập có lệnh và output đã chạy.**

| Hướng / giả thuyết | LỆNH | OUTPUT THẬT (trích) | Kết luận |
|---|---|---|---|
| Merge làm mất bản vá hoặc chèn nội dung ngoài hai cha | `python -B evidence/review.py integrity` | `TREE_UNION_EXACT=True p1_changed=2 master_changed=110 overlap=0 entries=7358`; hai `BYTE_IDENTICAL` | KHÔNG PHẢI LỖI — [log](evidence/integrity-summary.out) |
| Dữ liệu master làm đổi số landed, trạng thái hoặc lý do từng hồ sơ | `python -B evidence/review.py data` | `DATA_AB_JSON_BYTES_EQUAL=True parent_rows=78 head_rows=78 changed_rows=0`; `added=0 removed=0 modified=0` | KHÔNG PHẢI LỖI — [log](evidence/data-summary.out) |
| Caller/import mới hoặc registry đổi cách nhận kết quả | `rg -n kiem_ho_so_land /home/user/wp981-rv4/cay-kho`; `python -B evidence/review.py callers` | `TRACKED_REFERENCES_IDENTICAL=True matches=105`; `REGISTRY_AST_IDENTICAL=True`; `HARNESS head empty-0/0 accepted=False expected=False` | KHÔNG PHẢI LỖI trong phạm vi đã rà — [log](evidence/callers-summary.out) |
| Sáu hồ sơ kiểu (b) bỏ lọt thiếu comment/duyệt/SHA, sai kiểu, hoặc nới kiểu (a) khi cùng có (b) | `python -B evidence/review.py probes` | `PROBE pr870-claude-md-bai-hoc-c-land-evidence.yaml missing-comment TRUOT rc=1`; `malformed-block LOI rc=3`; `PROBES_PASS records=6 cases_per_record=7 cli_runs=42` | KHÔNG PHẢI LỖI — [log](evidence/probes-summary.out), [kết quả từng ca](evidence/probe-results.json) |
| Whitespace trong phần master là lỗi packet hoặc làm hỏng code cổng | `python -B evidence/review.py callers`; `git diff --check` cho hai phía | `WHITESPACE_FAILURE_IDENTICAL_TO_MASTER=True rc=2`; `DIFF_CHECK p2 rc=0 output_lines=0` | KHÔNG PHẢI LỖI của packet — giải thích và phạm vi thất bại bên dưới |

42 phép thử dùng bản sao dữ liệu của từng hồ sơ dưới `evidence/probes/`, chạy CLI HEAD thật và giữ nguyên hằng miễn trừ. Mỗi hồ sơ có bảy ca: baseline `DAT/0`, thiếu comment `TRUOT/1`, chưa duyệt `TRUOT/1`, SHA sai `TRUOT/1`, `landed: "true"` là `BO_QUA/0`, khối không phải ánh xạ `LOI/3`, đồng thời bật kiểu (a) với URL gốc sai là `TRUOT/1`. Các dòng `TRUOT`/`LOI` này là **kỳ vọng của fixture âm**, không phải kết quả trên hồ sơ thật.

**Phép kiểm đỏ được giữ nguyên.** `git diff --check afd3a86… 0eb66e5…` rc **2**, 119 dòng stdout: 61 chẩn đoán trên bốn hiện vật `ops/reviews/wp960-review-1-codex/diff.patch`, `ops/reviews/wp960-review-2-codex/{HINT.patch,diff-tu-luot1.patch,diff.patch}`. Có 58 báo trailing whitespace và 3 báo dòng trống EOF; mọi dòng bị nêu đều là chính xác một dấu cách `' '`, tức dòng ngữ cảnh trống của unified diff ([phân tích từng dòng](evidence/whitespace-analysis.json)). Toàn stdout lỗi giống từng byte khi chạy diff-check trên **merge-base→cha 2**; không do packet/resolve merge. Diff-check **cha 2→HEAD** rc **0**, stdout rỗng. Vì đây là byte của hiện vật patch lưu trữ, không phải whitespace mới trong mã sản phẩm, không mở finding sản phẩm và không sửa hiện vật. Vẫn ghi phép kiểm rộng là `failed`, không gọi nó là pass. Lần chạy đầu của driver dừng do chưa cho phép rc 2 của phép đo này; đã giữ [stdout](evidence/integrity-first-attempt.out)/[stderr](evidence/integrity-first-attempt.err), rồi sửa riêng driver evidence để ghi nhận và tiếp tục, không sửa checkout.

**ĐỐI CHIẾU LƯỢT TRƯỚC.** `VERDICT_LUOT3.md` approve tại `afd3a861bdaed63ada0f24ee8dbf2af166e86178`, không có finding mở. Lượt này tự xác minh lại hai blob, suite và dữ liệu, không chỉ kế thừa tổng kết.

| Nội dung bàn giao | Đối chiếu lượt này |
|---|---|
| Write set giữ nguyên bản đã approve lượt 2; merge lượt 3 không thêm lỗi | ĐÃ XÁC MINH: bytes/OID/hash của cả ba head giống nhau; merge hiện tại cũng là hợp nhất sạch |
| 23 landed / 78 hồ sơ, sáu kiểu (b) đều DAT | ĐÃ XÁC MINH: CLI hai cây có toàn stdout JSON giống bytes; 42 fixture âm/dương kiểm lại chốt |
| `mutant-crash-counted-as-kill` và ba mutant `skip-sha-pure-b`, `only-first-active-block`, `relax-a-if-active-b` đã đóng ở lượt 2 | Bản mã/test được bảo toàn; suite 11/11 chạy lại, gồm ca đột biến và kiểm crash không được tính thành kill |
| Bốn mutant riêng còn sống trong ghi chú giới hạn lượt 2 | Chưa tái chạy bộ probe riêng đó; không tự tuyên bố đã đóng giới hạn độ phủ |
| N3/N4 rộng và identity runtime chưa chứng nhận trong lượt 3 | Không suy kết quả cũ sang HEAD mới; giới hạn lượt này ghi rõ bên dưới |

Bảng lớp finding mới: **0 lớp, 0 biểu hiện**; không có finding cần định dạng P0/P1/P2/P3 hoặc yêu cầu sửa. Không tạo HINT.patch, không sửa mã executor.

**Snapshot đầu/cuối và tính chỉ đọc.** Các lệnh bắt buộc đều đã thực hiện:

```text
git -C /home/user/wp981-rv4/cay-kho rev-parse HEAD 'HEAD^{tree}'
git -C /home/user/wp981-rv4/cay-kho status --porcelain --untracked-files=all --ignored=matching
git -C /home/user/wp981-rv4/cay-kho ls-files -s | sha256sum
```

| Phép đo | Đầu lượt | Cuối lượt |
|---|---|---|
| HEAD | `0eb66e513f2736f0bfc342ddbcbc70b84f773b3b` | `0eb66e513f2736f0bfc342ddbcbc70b84f773b3b` |
| Tree | `04702940110da99d13068b5857f04cedc8d2c3ae` | `04702940110da99d13068b5857f04cedc8d2c3ae` |
| Status gồm tracked/untracked/ignored | 0 dòng, rc 0 | 0 dòng, rc 0 |
| SHA-256 `git ls-files -s` | `9b8bfaf9a19b74a121940db6e3fea58bf369d7324e2287124c399bd5377575e6` | `9b8bfaf9a19b74a121940db6e3fea58bf369d7324e2287124c399bd5377575e6` |

Snapshot đầu khớp cả snapshot điều phối. Log [HEAD đầu](evidence/snapshot-before-head.txt), [status đầu](evidence/snapshot-before-status.txt), [index đầu](evidence/snapshot-before-index.txt); [HEAD cuối](evidence/snapshot-after-head.txt), [status cuối](evidence/snapshot-after-status.txt), [index cuối](evidence/snapshot-after-index.txt). `git diff --exit-code` và `git diff --cached --exit-code` cuối lượt đều rc 0, stdout 0 byte.

**Checkout không bị ghi trong lượt review này**: không checkout/stash, không sửa rồi hoàn nguyên, không tạo fixture/cache/bytecode/object Git trong cây. Mọi ghi do reviewer thực hiện nằm ở `VERDICT.md` và `evidence/` bên ngoài cây. Snapshot chứng minh không có delta quan sát được giữa hai mốc; tự nó không chứng minh toàn bộ lịch sử thao tác, nên lời khai chỉ đọc còn dựa trên các lệnh đã thực hiện và ranh giới sandbox thực tế.

**Trạng thái kiểm tra và giới hạn.** `passed`: xác minh spec/hash và write set, tree hợp nhất, suite 11/11, CLI text/JSON, A/B 78 hồ sơ, 42 fixture, caller/import/hợp đồng marker, diff-check packet so cha 2, snapshot đầu/cuối. `failed`: diff-check phần master mang vào (lỗi hình thức của patch lưu trữ đã phân tích). `skipped`: không ca nào bị bỏ trong suite 11/11. `not_run`: toàn bộ `ci_dang_ky_test.py` (cả có/không `--chay`), `tl.py --selftest`, doctrine-scan, bare Ruff, gate phát hành và review đầy đủ nội dung 110 tệp master ngoài tương tác với L-6. `not_measured`: CI/check runs exact HEAD, ref/trạng thái từ xa, receipt model/effort runtime. Các mục chưa chạy/chưa đo không được tính là xanh; verdict này hoàn tất phạm vi review merge được giao, không thay nghiệm thu land tổng thể.
