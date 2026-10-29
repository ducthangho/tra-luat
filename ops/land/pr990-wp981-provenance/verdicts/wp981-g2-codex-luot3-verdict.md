verdict: approve
reviewed_sha: afd3a861bdaed63ada0f24ee8dbf2af166e86178

**Approve merge commit trong phạm vi hẹp của lượt 3/3.** Không phát hiện finding P0/P1/P2/P3 mới do merge. Hai tệp write set giống từng byte với head đã approve ở lượt 2; cây merge đúng hợp nhất sạch của hai cha. Bộ kiểm trên dữ liệu thật đạt **23/23, rc 0**, bộ test đạt **11/11, rc 0**. Phần master mang vào không làm đổi kết quả bộ kiểm trên cả 78 hồ sơ được quét.

Phạm vi theo `runs/6018070a/prompt.snapshot`: packet wp981 r2, g1 theo gói, lớp `sensitive`; mở đúng một lượt xác minh merge sau lượt 2. Chỉ thị cung cấp authority #981 issuecomment-6443331447; không xác minh lại comment qua mạng. Ngưỡng áp dụng: approve chỉ khi không còn P0/P1/P2. Đây là review nội dung merge, không xác nhận đủ điều kiện push/land hoặc cấp quyền thực hiện các thao tác đó.

Reviewer độc lập Codex, provider `openai_codex`, họ GPT-6/OpenAI theo cấu hình phiên; thực thi qua phiên API có công cụ shell cục bộ, transport `machine`. Không có receipt độc lập để đo model ID/effort thực phục vụ hoặc phân loại launcher/CLI/Desktop; không tự nâng lời khai này thành assurance đã được máy chứng nhận. Executor họ Claude theo assignment. Sandbox thực tế `workspace-write`, mạng bị hạn chế; đã tuân thủ chỉ thị không mạng, không push và coi checkout `cay-kho/` là chỉ đọc. Mọi script, dữ liệu phản chứng, log, object Git mới và temp nằm ngoài checkout, trong `evidence/`.

Các mốc đã đo bằng Git cục bộ:

- HEAD detached: `afd3a861bdaed63ada0f24ee8dbf2af166e86178`.
- Tree: `9bbe9c085f6d5df585e7b0a29541d5d110d90649`.
- Cha 1: `2c70821245f777ede564c79e4e4abade0de53ae6` — head lượt 2.
- Cha 2: `20a2e2b3dd52a83442c739d17db1f1bd66181a6c` — master được giao.
- Merge-base: `74132ce20cb1f9f74e163717908eca384f672dd0`.
- SHA-256 `SPEC.md`: `3d026415193d3f3b1ceef005cdc99fcc73871b0c7539697f82b4b0198f578079`, đúng assignment.
- Remote được cấu hình: `https://github.com/ducthangho/tra-luat.git`; chỉ đọc cấu hình, không liên hệ remote.
- Git `2.43.0`, Python `3.13.17`, PyYAML `6.0.3`. Script đặt `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=evidence/tmp`, `GIT_OPTIONAL_LOCKS=0`; Git chạy với `core.abbrev=7` theo từng lệnh.

[Script tái chạy](evidence/review_merge.py) ghi argv, cwd, rc thật, stdout/stderr vào từng tệp `.json` và `.out`. Các lệnh `python -B evidence/review_merge.py ...` dưới đây chạy từ thư mục chứa verdict; lệnh `python ops/...` và Git chạy với cwd `cay-kho/`.

**Tính toàn vẹn write set và merge.** Lệnh `python -B evidence/review_merge.py integrity` trả rc 0 ([output](evidence/integrity-summary.out)). Với mỗi tệp, script lấy blob bằng `git cat-file blob`, so bytes trực tiếp, so blob OID bằng `git rev-parse SHA:path`, tính SHA-256 riêng trên hai phiên bản và đối chiếu cả bytes trong checkout.

| Tệp | Blob OID ở cả cha 1 và merge | SHA-256 ở cả cha 1 và merge | Kết quả |
|---|---|---|---|
| `ops/kiem_ho_so_land.py` | `846f3697dc453f349852a613ed9a2ec7ab369569` | `5ee2385db62ce529200ee936dda28481ed94182907e58acf7974c977025b4fe4` | Giống từng byte |
| `ops/kiem_ho_so_land_test.py` | `45874c6be6286406ea780ae9d9d489662da446bb` | `943fabb42682a62749c1b972bbd5fab76d830db3c967bd7dc5c72ecb5d67b68c` | Giống từng byte |

`git diff 74132ce20cb1f9f74e163717908eca384f672dd0 20a2e2b3dd52a83442c739d17db1f1bd66181a6c -- ops/kiem_ho_so_land.py ops/kiem_ho_so_land_test.py` trả rc 0, stdout rỗng ([log](evidence/master-write-set.json)). Master chỉ đổi 5 tệp: hai skill `cross-review`/`land-packets`, `ops/bien_nhan_v2.py`, `ops/bien_nhan_v2_test.py`, và `ops/land/pr963-wp943-land-evidence.yaml`. Không thêm/xóa hồ sơ `*-land-evidence.yaml` nào.

`git diff-tree --cc afd3a861bdaed63ada0f24ee8dbf2af166e86178` trả rc 0, stdout **chỉ có dòng OID commit, 41 byte**; không có hunk. Thêm `--no-commit-id` thì stdout rỗng. Không dùng riêng combined diff để suy merge sạch: đã chạy thêm `git merge-tree --write-tree 2c70821245f777ede564c79e4e4abade0de53ae6 20a2e2b3dd52a83442c739d17db1f1bd66181a6c`, trả rc 0 và đúng tree `9bbe9c085f6d5df585e7b0a29541d5d110d90649` ([log](evidence/merge-tree.json)). Object mới được ghi vào `evidence/merge-objects`, đọc object cũ qua alternate; không ghi object vào kho được review. Git in cảnh báo deprecation do script đặt `GIT_GRAFT_FILE=/dev/null`; đây không phải conflict, stderr gốc được giữ nguyên.

Phép so độc lập trên toàn bộ mục `git ls-tree -rz --full-tree` (gồm path, mode, type, OID) cho `TREE_UNION_EXACT=True p1_changed=2 master_changed=5 overlap=0 entries=7259`. Như vậy **nội dung cuối không có chỉnh sửa resolve ngoài kết quả merge sạch**; phép đo không suy đoán lịch sử thao tác bàn phím của người tạo commit. Diff/stat được sinh lại khớp từng byte với hai hiện vật cung cấp. Ngoài ra, `git diff BASE P1` bằng từng byte `git diff P2 HEAD`: diff của packet sau merge vẫn đúng 2 tệp, `47/11` và `137/3` dòng thêm/xóa, tổng 184 dòng thêm ([diff sau merge](evidence/packet-diff-after-merge.out), [numstat](evidence/packet-numstat-after-merge.out)).

**Ảnh hưởng lên dữ liệu thật.** `python -B evidence/review_merge.py data` trả rc 0 ([output](evidence/data-summary.out)). Hai lệnh được yêu cầu đã chạy trên checkout exact HEAD:

```text
python ops/kiem_ho_so_land.py --root .
TỔNG: 23/23 hồ sơ landed True đạt · 0 miễn trừ · rc=0
exit code: 0

python -B ops/kiem_ho_so_land_test.py
11/11
exit code: 0
```

Log đầy đủ: [dữ liệu thật](evidence/real-text.json), [bộ test](evidence/unit-tests.json). Đã trích tất cả 78 hồ sơ top-level từ cha 1 sang `evidence/p1-data/`, chạy **cùng mã bộ kiểm đã xác minh không đổi** trên tập đó và trên dữ liệu merge. Hai stdout `--json` bằng từng byte, gồm tên tệp, trạng thái, lý do, các tổng và rc: `DATA_AB_JSON_BYTES_EQUAL=True rows=78 n_dat=23 n_landed=23 n_mien_tru=0 rc=0` ([cha 1](evidence/p1-data-json.json), [merge](evidence/real-json.json)). Đây là phép đo delta dữ liệu, không phải tuyên bố đã chạy lại toàn bộ cổng trên checkout cha 1.

| Sáu hồ sơ kiểu b | Cha 1 | Merge | Nguồn landed trên merge |
|---|---|---|---|
| `pr870-claude-md-bai-hoc-c` | DAT | DAT | `landed_20261026.landed` |
| `pr889-claude-md-bai-hoc-c` | DAT | DAT | `landed_20261026.landed` |
| `pr896-claude-md-bai-hoc-c-tro-nguon` | DAT | DAT | `landed_20261027.landed` |
| `pr924-wp923` | DAT | DAT | `landed_20261027.landed` |
| `pr950-wp834` | DAT | DAT | `landed_20261027.landed` |
| `pr963-wp943` | DAT | DAT | `landed_20261027.landed` |

Riêng `ops/land/pr963-wp943-land-evidence.yaml:102`, 8 dòng mới chỉ thêm `assurance_81.thuc_thi` và `assurance_81.thuc_thi_ghi_chu`. Sau khi parse YAML và bỏ đúng hai khóa mới khỏi bản merge, toàn bộ tài liệu bằng bản cha 1; `authorized_head_sha`, URL gốc, `trang_thai_packet`, khối `landed_20261027` và comment duyệt đều không đổi. Phản chứng trên bản sao giữ metadata mới nhưng xóa comment hoặc làm SHA sai vẫn `TRUOT/1`; tắt khối landed vẫn `BO_QUA/0`. Bốn biến thể ở hai phía cho cùng toàn bộ JSON, tổng 8 lượt CLI ([output](evidence/metadata-summary.out)). Không sửa hồ sơ thật hoặc thêm miễn trừ.

**Bảng SĂN** ghi các giả thuyết đã thử, không dùng riêng tổng suite xanh làm bằng chứng cho kết luận tương tác.

| Hướng / giả thuyết | LỆNH | OUTPUT THẬT (trích) | Kết luận |
|---|---|---|---|
| Merge chèn thay đổi không thuộc hai cha hoặc làm mất bản vá đã duyệt | `python -B evidence/review_merge.py integrity` | `MERGE_TREE=9bbe9c085f6d5df585e7b0a29541d5d110d90649 rc=0 MATCH_HEAD=True`; `TREE_UNION_EXACT=True p1_changed=2 master_changed=5 overlap=0 entries=7259` | KHÔNG PHẢI LỖI — [log](evidence/integrity-summary.out) |
| Hồ sơ master mới/đổi làm đổi số landed, trạng thái hoặc lý do báo cáo | `python -B evidence/review_merge.py data` | `M ops/land/pr963-wp943-land-evidence.yaml`; `DATA_AB_JSON_BYTES_EQUAL=True rows=78 n_dat=23 n_landed=23 n_mien_tru=0 rc=0` | KHÔNG PHẢI LỖI — [log](evidence/data-summary.out) |
| Metadata assurance mới ở pr963 che lỗi thẩm quyền/SHA hoặc tự kích hoạt landed | `python -B evidence/review_merge.py metadata` | `merge missing-comment: TRUOT rc=1`; `merge invalid-sha: TRUOT rc=1`; `merge inactive-block: BO_QUA rc=0`; `PR963_METADATA_AB_EQUAL=True cases=4 cli_runs=8` | KHÔNG PHẢI LỖI — [log](evidence/metadata-summary.out) |
| Tệp master mang vào thêm caller/import phụ thuộc hành vi cũ | `rg -n kiem_ho_so_land .`; quét thêm tệp ẩn và so `git grep` hai commit bằng `python -B evidence/review_merge.py callers` | `RG_LINES=104 RG_HIDDEN_LINES=105`; `TRACKED_REFERENCES_IDENTICAL=True matches=105 MASTER_CHANGED_DIRECT_MATCHES=[]` | KHÔNG PHẢI LỖI trong các đường đã rà — [rg](evidence/rg-callers.out), [log đối chiếu](evidence/callers-summary.out) |
| Bộ gọi CI không còn nhận đúng marker N/N sau merge | `python -B evidence/review_merge.py harness` | `REGISTERED_PATTERN=^(\d+)/(\d+)$ ACTUAL_OUTPUT_MATCHES=[('11', '11')] test_rc=0`; `HARNESS_CONTRACT=True; full_registry_gate=not_run` | KHÔNG PHẢI LỖI ở hợp đồng marker — [log](evidence/harness-summary.out) |

Về caller: quét có tệp ẩn bổ sung đúng mục đăng ký `.claude/dev/ci_dang_ky_test.py:54`. Các tham chiếu executable còn lại nằm trong chính bộ kiểm/test của nó; 5 tệp master mang vào không chứa tên bộ kiểm. Đã đọc import bằng AST và phần diff liên quan: bộ kiểm chỉ import thư viện chuẩn và PyYAML; `bien_nhan_v2` không import/gọi bộ kiểm, và không nằm trong đường import của nó. Hai skill thêm hướng dẫn GraphQL, không thêm lời gọi L-6. `requirements.txt`, `ci.yml` và sổ đăng ký test giống từng byte cha 1. Quét chuỗi tự nó không chứng minh mọi lời gọi động đều vắng; kết luận ở đây dựa thêm vào tập path thay đổi đóng và đường import đã đọc.

**ĐỐI CHIẾU LƯỢT TRƯỚC.** `VERDICT_LUOT2.md` approve tại `2c70821245f777ede564c79e4e4abade0de53ae6`, không có finding còn mở. Theo chỉ thị lượt 3, không mở lại review ngữ nghĩa bản vá khi cả hai tệp không đổi. Bằng chứng blob/SHA-256 và diff giữ nguyên xác nhận merge bảo toàn bản đã duyệt; suite hiện tại chạy lại đạt 11/11. Không khai đã tái chạy riêng bộ probe/đột biến ngoài kho của reviewer lượt 2.

| Lớp/giới hạn được bàn giao từ lượt 2 | Trạng thái lượt trước | Đối chiếu lượt này |
|---|---|---|
| `mutant-crash-counted-as-kill` và ba mutant `skip-sha-pure-b`, `only-first-active-block`, `relax-a-if-active-b` | Đã đóng bằng phép đo lượt 2 | Bảo toàn nguyên bytes mã và test; không có bản sửa mới trong merge để phân loại lại |
| Bốn mutant riêng sống ở lượt 2 | Giới hạn độ phủ, không phải lỗi sản phẩm đã xác nhận | Giữ nguyên giới hạn; không tự tuyên bố đã đóng hoặc đã thử lại |
| N3/N4 ngoài bộ kiểm đang xét | Lượt 2 ghi cổng rộng chưa xanh/không đo được trong môi trường đó | Không suy kết quả cũ sang SHA mới; không chứng nhận các cổng này trong lượt hẹp |

Bảng lớp finding mới: **0 lớp, 0 biểu hiện, không có finding để yêu cầu sửa**. Không tạo HINT.patch và không sửa mã executor.

Các kiểm tra bổ sung đã chạy: `git diff --check P1 HEAD` và `git diff --check P2 HEAD` đều rc 0, stdout rỗng ([P1](evidence/diff-check-p1.json), [P2](evidence/diff-check-p2.json)); `python -B .claude/dev/packet_loop.py doctrine-scan --root .` trả `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`, rc 0 ([log](evidence/doctrine.json)).

**Giới hạn và bàn giao.** `passed`: các phép so tính toàn vẹn, tái dựng merge, A/B dữ liệu, phản chứng pr963, rà caller, hợp đồng marker, 23/23, 11/11, diff-check và doctrine-scan. `failed`: không có trong các phép chạy lượt này. `skipped`: không có ca nào bị bỏ trong suite 11/11. `not_run`: full registry gate, toàn bộ `tl.py --selftest`, bộ test riêng của `bien_nhan_v2`, bare Ruff và review lại toàn bộ nội dung master. `not_measured`: CI/check runs trên exact merge SHA, trạng thái ref từ xa và receipt model thực phục vụ; assignment cấm mạng. Không nâng các mục chưa chạy/chưa đo thành pass.

Cuối lượt, `python -B evidence/review_merge.py final` trả rc 0: `INITIAL_FINAL_IDENTICAL=True files=7259`, HEAD/tree giữ nguyên; working diff, index diff, untracked và ignored đều rỗng. SHA-256 cùng mode của tất cả 7.259 tệp khớp snapshot đầu ([output](evidence/final-summary.out), [snapshot đầu](evidence/integrity-initial.json), [snapshot cuối](evidence/integrity-final.json)). Hai snapshot chứng minh không có delta quan sát được giữa hai mốc, không tự chứng minh toàn bộ lịch sử thao tác. Checkout không cần hoàn nguyên.
