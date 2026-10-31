verdict: changes_requested
reviewed_sha: c24875d00e93e6a98e0a0abd0837e0cbcad65d4d
Kết quả: 0 P0, 1 P1, 1 P2, 0 P3.

## BẢNG ĐO

| khẳng định | bên giao khai | đo được (lệnh) | khớp? |
|---|---|---|---|
| Khóa review và phạm vi | c24875d, base b29da0b; 32 tệp, +11630/−0, ops/reviews + ops/land | `git rev-parse`, `git diff --numstat`; `evidence/final-integrity.log`: đúng OID, tree `9382f751…`, đúng 32/11630/0 | Có |
| Hai commit ghi sổ | e788a5d hiện vật; c24875d biên nhận/land | `git log b29da0b..c24875d`, đúng hai commit; artifact commit là tổ tiên c24875d rc 0 | Có |
| Chưa merge PR ghi sổ | Mỏ neo thấp trên nhánh PR | `git rev-parse origin/master` = b29da0b; `git merge-base --is-ancestor c24875d b29da0b` rc 1, không suy trạng thái PR trực tuyến | Khớp ancestry snapshot; không gọi mạng |
| Nguồn lease | origin/ops/wp1037-r1-g1-lease | Đóng băng thành OID `a34b9a38cda2669f9a90958c69bb6f2faa0f4353`; mọi `git show` nguồn dùng OID này | Có |
| Bản phẳng và VERDICT lượt 1 | Nguyên byte; 14251 byte, e33a3c3e…d2a95b | `python3 evidence/measure_artifacts.py`: flat = directory = source blob; cùng hash | Có |
| Bản phẳng và VERDICT lượt 2 | Nguyên byte; 10679 byte, 2f482565…49feaf | Cùng script: cả ba bản khớp byte/hash | Có |
| PROMPT lượt 1 và 2 | Bản gốc; hash ca20a3a0… / d1d75feb… | Cùng script: 3977 / 3907 byte; source_equal và HEAD_equal True | Có |
| run.json lượt 1 và 2 | Bản gốc | Cùng script: 10930 / 10492 byte, hash 58050918… / 21dfe28a…; source_equal True | Có |
| Manifest các thư mục | SHA256SUMS đầy đủ | Cùng script: 6/6 + 6/6 + 11/11 OK; không thiếu/thừa; `measure_receipts.py` kiểm thêm 6/6 mục manifest nguồn | Có |
| Checkpoint và stdout/stderr | Cùng run đúng hash | `measure_artifacts.py`: cả hai lượt sha256_match=True, bytes_match=True; checkpoint head/prompt/run ID khớp | Có về nội bộ; không có bản handoff riêng cho 3 tệp phụ |
| schema_version, kind, receipt_id | 2 / review_delivery_receipt / hậu tố hash verdict | `python3 evidence/measure_receipts.py`: đúng schema/kind, receipt_id_hash_suffix=True cả hai | Có |
| packet_id, packet_issue, revision, generation, lease_id | #1037; r1/g1; wp1037-r1-g1-claude | Cùng script: từng khóa receipt bằng lease; cả hai = True | Có |
| Review class và vai | reviewer codex; executor claude; sensitive | Lease `risk: sensitive`, code trong ops; receipt hai class sensitive; protocol ops-sensitive | Có |
| verdict và số P0..P3 lượt 1 | changes_requested; 0/0/1/2 theo finding | Script đếm `^- [P*]`: 0/0/1/2; verdict gốc `request_changes` được chuẩn hóa đúng | Có |
| verdict và số P0..P3 lượt 2 | approve; 0/0/0/0 | Script đếm đúng; bảng gốc không finding | Có |
| findings_ids và xử lý lượt trước | Ba slug P2/P3 lượt 1; lượt 2 đã đóng | Slug/hạng khớp các dòng finding gốc; lượt 2 có bảng ĐÃ VÁ THẬT cho cả ba; nội dung là bản gốc byte-identical | Có về ghi sổ; không tái chạy mutant code của packet |
| reviewed_sha / reviewed_tree lượt 1 | 016852ae7acc22a75bae9505febd1697a1ab79ba | Receipt = run = dòng 2 verdict; Git tree `6907a286e95a2c6e86c7c08c0ec700dc2a75ef58` = verdict | Có |
| reviewed_sha / reviewed_tree lượt 2 | 91466322f705658ed51b80c7c152f6b77f4f90c6 | Receipt = run = dòng 2 verdict; Git tree `c20eace3f4aacea3f33afc5861688cb94d64cf3d` = verdict/land | Có |
| base SHA | Base packet 757bde5; base PR ghi sổ b29da0b | Lease base `757bde561d09738858506aecf5de2f050a5f0d5e`; Git diff và PR readback khớp; không nhầm hai loại base | Có |
| Khóa tree/base/mức model | Receipt dùng model_evidence; không có khóa tree/base trực tiếp | Script xác nhận absent_optional_fields; §7 không bắt các khóa tùy chọn này; tree/base được kiểm từ nguồn khác | Không tính vắng khóa là lỗi |
| verdict_path/hash/bytes | Trỏ đúng bản phẳng, đúng hash và byte | `measure_receipts.py`: hash_equal=True, bytes_equal=True cho cả hai; đường dẫn đúng basename chuẩn | Có |
| evidence_url và anchor | Blob ghim e788a5d, cùng nhánh, strength thấp | `git show <OID>:<path>` bằng byte verdict; e788a5d → c24875d rc 0; không khai đã có canonical anchor mạnh | Có |
| reviewed_sha_to_tien và land_merge_commit | Hai reviewed SHA là tổ tiên b29da0b; head cuối là cha 2 | `git merge-base --is-ancestor` cả hai rc 0; `b29da0b^2` = 9146632 | Có |
| Run ID/head/prompt/state/rc/duration | 4d0668e2… / e400a320…; xong; rc 0; 934.249 / 567.318 s | `measure_receipts.py` + `artifacts.log`: đúng từng giá trị, prompt hash khớp; checkpoint cùng run | Có |
| Thời gian chạy thuộc lease | 09:08:51Z và 09:34:41Z trong cửa sổ 08:57Z–17:53Z | Script RUN_START_IN_LEASE=True cả hai | Có |
| model_* reviewer và mức bằng chứng | gpt-6-astra served; do_may; 27 / 19 sự kiện; xhigh | `receipts.log`: model_phuc_vu_trang_thai=DO_DUOC; mọi event cùng model; effort trạng thái DO_DUOC, [xhigh] | Có cho served model/effort |
| model_yeu_cau / CLI flags / version | gpt-6-astra; codex-cli 0.164.0 và command khai trong receipt | run chỉ giữ program/arg count/fingerprint; CLI_VERSION_METADATA_FIELDS=[]; raw stdout/stderr không có version | KHÔNG ĐO ĐƯỢC độc lập cấu hình yêu cầu/phiên bản |
| Provider/surface/transport/run identity | openai_codex/codex_cli/machine và session_run_id | `measure_receipts.py`: cả bốn trường bằng run metadata ở hai lượt | Có theo nguồn được giữ |
| Độc lập và assurance | Lượt 1 cross_reviewed; lượt 2 cross_approved | Hai run ID riêng, prompt riêng; model reviewer khác họ executor trong lease; lượt 1 không approve, lượt 2 approve 0/0/0/0 | Có trong phạm vi evidence; không nâng thành authority merge |
| Executor model / người vận chuyển | Claude theo lease; submitter ducthangho, chưa đăng bản chiếu | Lease khai claude-opus-5-5/claude; `actor_nguon` gắn (b); không có runtime executor hoặc readback push/comment PR #1050 | Lời khai đã tách; không xác nhận độc lập |
| Caveat read-only và scripts | Workspace có write; clean lúc phóng; scripts evidence ngoài repo | Run worktree_sach=True; permission observations có workspace write; các evidence/* không trong gói; run1 sampling KHONG_DO_DUOC, run2 DO_DUOC | Đúng giới hạn caveat; không bảo đảm RO toàn lịch sử |
| README hai hàng mục lục | Đúng file/receipt/verdict/SHA/bytes, không trùng | `evidence/readme.log`: TOC_COUNT=1 mỗi lượt; cả 6 link đích tồn tại; nội dung khớp receipt | Có |
| README bốn hàng caveat | Mỗi caveat của mỗi verdict có hàng riêng | readme.log: COUNT=1 mỗi cặp; t27 baseline 2/2 | Có |
| Land schema/identity/recorded_by | Schema 1, land_operator, cùng phiên executor chỉ ghi sổ; owner merge | Khóa chuẩn §7 có; PR API merged_by=ducthangho. Nhận dạng phiên/operator thực là lời khai; hồ sơ không tự gọi đó là người đã chứng minh | Đúng schema; phần phiên không đo độc lập |
| Authorization | Comment owner nêu điều kiện; không exact SHA | `measure_ci.py`: author OWNER ducthangho, 17:25:09Z, contains_authorized_head=False; PR API xác nhận merge, không thay exact-SHA approval | Có |
| Merged/head/base/parents/tree | Merge b29da0b, head 9146632, parents 8cdb15a + 9146632, tree 24a37be… | `measure_ci.py`: API và Git object khớp từng giá trị; diff hai cặp cùng hash 40b6d80f… và +120/−4 chỉ tệp test | Có |
| Spec và lease provenance | Spec hash 253f12ae…; lease snapshot a34b9a3; write set và hash | `measure_artifacts.py`, `measure_receipts.py`: spec hash đúng, lease byte-identical b1738f6f…, write_set_hash d7872905… đúng | Có |
| Lease đã nhả | `measured … DA NHA`, điều kiện (2) xong | `evidence/lease-timeline.log`: CÒN_HẠN lúc snapshot và commit; còn 718 giây; không bia mộ | **Không — P1 nha-lease-truoc-khi-het-han** |
| PR Ubuntu run | 41033737059, attempt1, pull_request, head9146632, success, 23/23 Ubuntu | `python3 evidence/measure_ci.py`: tổng=độ dài array=23, success=23, đúng head/attempt/labels | Có cho Run và job metadata |
| Windows attempts | 41069257658; attempt1 13success/2failure/1skipped; attempt2 15success/1skipped | ci.log: đúng counts, run failure→success; 14 nhãn Windows + 1 Ubuntu + 1 không runner mỗi array | Có |
| Windows runner và N/N | gate-ops job 124108765783; 95/95,137/137,2/2; lease255/255 | Jobs ghi runner1000026073/windows-latest/success; không có output N/N; hồ sơ nói rõ thuat_lai, log không lưu | Khớp metadata; N/N KHÔNG ĐO ĐƯỢC độc lập |
| Root cause Windows và runner_set input | Câu measured nói thiếu shellcheck, lỗi cai_cong_cu.sh/#1045; tên check windows-only | ci.log chỉ có hai step G5 fail, step cài shellcheck success; không có log chẩn đoán hay input dispatch | **Khai rộng — P2 nguyen-nhan-windows-khai-do-thieu-log** |
| Codex connector | not_measured/thuat_lai, ready17:28:26Z rồi merge17:28:50Z | Không lưu readback comment6529077259; không nhận running hoặc kết luận connector là đo độc lập | Đã hạ nhãn đúng; KHÔNG ĐO ĐƯỢC |
| Gate push master pending | Run41099184556 trên b29da0b pending lúc17:37Z | Snapshot runs: eventpush, attempt1, pending/null, head đúng; lời văn có mốc snapshot | Có ở snapshot; không suy trạng thái về sau |
| Bốn mốc CI §10.2.2 | Run measured; Checkout/definition/output chưa đo | REST files có Run identity; không có checkout log, exact definition blob/hash hoặc command/rc/marker CI; hồ sơ không nhận chúng là ĐẠT | Đúng trạng thái thiếu nguồn; HTTP403 thuật lại |
| assurance_81.thuc_thi | Reviewer lượt2 DAT; model/effort/sandbox đo được | Run2: 19 gpt-6-astra, xhigh, sandbox_trang_thai DO_DUOC và permission observations đúng mô tả; ghi giới hạn lấy mẫu | Có; không thay CI provenance |
| landed:false và việc còn thiếu | Chưa đủ post-merge evidence và approval exact SHA | Nguồn thiếu các mốc CI, owner comment không SHA; source code đã vào master qua diff giống byte | Đúng; điều kiện nhả lease phải sửa theo P1 |
| Sáu cổng | Yêu cầu rc0, marker dương/N=N | `evidence/baseline-*.log/.rc`: cả sáu rc0, TỔNG ĐẠT hoặc sạch; t26 1/1, t27 2/2, t138 1/1 | Có |
| Răng cổng trên dữ liệu | Byte verdict / hàng README / số P1 | `python3 evidence/measure_mutations.py`: byte→t26 đỏ; xóa mục lục/caveat→t27 đỏ; so_p1 đổi→sáu cổng vẫn xanh | Có răng hash/mục lục; **không có răng số đếm** |
| Gợi ý và nguyên trạng cây | HINT chỉ sửa dữ liệu, reviewer không sửa checkout gốc | `patch --dry-run --fuzz=0 -p0` rc0; thử áp/gate trên clone rồi phục hồi; final-integrity: cả hai cây sạch, 32/32 tệp gốc khớp HEAD | Có |

## BẢNG SĂN

Bắt đầu: đã đọc `run/1b0ff763/prompt.snapshot`. Chỉ đọc `cay-kho/`; chạy đột biến trên clone từ `mirror.git` ngoài `cay-kho/`. Không gọi mạng, không push. Nhật ký sẽ nối thêm sau mỗi hướng thử.

### Hướng 1 — Định danh và phạm vi (KHÔNG PHẢI LỖI)

Lệnh: `git -C cay-kho rev-parse HEAD HEAD^{tree} refs/remotes/origin/ops/wp1037-r1-g1-lease`; `git -C cay-kho rev-parse --is-shallow-repository`; `git -C cay-kho diff --name-status b29da0b HEAD`; `git -C cay-kho status --short`.
Output thật:
```text
HEAD c24875d00e93e6a98e0a0abd0837e0cbcad65d4d
TREE 9382f7512f3adf569f1f82c4d597c66fa1b463d7
LEASE_REF a34b9a38cda2669f9a90958c69bb6f2faa0f4353
is-shallow-repository false
status --short: (rỗng)
diff: 32 tệp, chỉ ops/reviews/** và ops/land/**
```
Đã tạo clone tách biệt `review-copy/` từ `mirror.git`, checkout exact SHA để chạy cổng/đột biến mà không ghi `cay-kho/`.

### Hướng 2 — Bản sao, manifest và hiện vật phụ (KHÔNG PHẢI LỖI)

Lệnh đã chạy: `python3 evidence/measure_artifacts.py` (đọc blob tại lease OID cố định `a34b9a38cda2669f9a90958c69bb6f2faa0f4353`, so byte với checkout exact reviewed SHA).
Output thật (đầy đủ: `evidence/artifacts.log`):
```text
ROUND 1 PROMPT.md: bytes=3977 sha256=ca20a3a06a82643b7d48fe3185600a35d00d4dc7d7e45c4dd7409c5b142d88dc original_equal=True HEAD_equal=True
ROUND 1 VERDICT.md: bytes=14251 sha256=e33a3c3efdeb3d55c7dd2c45ae831d814861690c360071b706026f4c9ed2a95b original_equal=True HEAD_equal=True
ROUND 2 VERDICT.md: bytes=10679 sha256=2f482565c235380145253d76ae51ab9606e8d7cfc8044d6efd113ff80049feaf original_equal=True HEAD_equal=True
```
Bản phẳng, PROMPT và run.json cả hai lượt đều khớp nguồn; mọi mục SHA256SUMS được kiểm, inventory không thiếu/thừa. Checkpoint/stdout/stderr khớp hash trong run.json; các tệp phụ này không có bản gốc tương ứng trong thư mục handoff của ref được cấp, nên chỉ xác nhận nội bộ và manifest, không suy có nguồn thứ hai độc lập. Lease snapshot khớp byte nguồn; spec hash khớp lease. Xem log cho toàn bộ hash và byte count.

### Hướng 3 — Sáu cổng baseline trên clone exact SHA (KHÔNG PHẢI LỖI)

Cwd: `review-copy/` (clone từ mirror, HEAD `c24875d…`); tất cả đặt `PYTHONDONTWRITEBYTECODE=1`. Lệnh và output thật:

| Lệnh | rc | Dòng kết luận |
|---|---:|---|
| `python3 ops/bien_nhan_v2.py --root .` | 0 | `255 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 308`; `TỔNG: ĐẠT` |
| `python3 ops/land_evidence_nguon.py --root .` | 0 | `65 ĐẠT · 25/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 90`; `TỔNG: ĐẠT` |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine` |
| `python3 ops/lease_publish_test.py --chi-ca=t26_` | 0 | `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` |
| `python3 ops/lease_publish_test.py --chi-ca=t27_` | 0 | `lease_publish: 2/2 đạt; đã chạy=2, bỏ qua=0` |
| `python3 ops/lease_publish_test.py --chi-ca=t138_` | 0 | `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` |

Log thật và rc: `evidence/baseline-*.log`, `evidence/baseline-*.rc`. Không có lỗi `Codex home is inside a repository` trong sáu lượt này. Các test báo N/N với tử bằng mẫu; không suy cổng kiểm đầy đủ nội dung mọi lời khai.

### Hướng 4 — Nội dung biên nhận, tree/base và model (KHÔNG PHẢI LỖI ở các trường đã đối chiếu)

Lệnh đã chạy, tái lập bằng `PYTHONDONTWRITEBYTECODE=1 python3 evidence/measure_receipts.py`: đọc YAML receipt, JSON run, đếm `^- \[P[0-3]\]` trong verdict, `git rev-parse <reviewed_sha>^{tree}`, `git show <evidence_commit>:<verdict_path>`, `git merge-base --is-ancestor <reviewed_sha> b29da0b`.
Output thật:
```text
ROUND 1 HEADS 016852ae7acc22a75bae9505febd1697a1ab79ba 016852ae7acc22a75bae9505febd1697a1ab79ba Reviewed commit: 016852ae7acc22a75bae9505febd1697a1ab79ba TREE 6907a286e95a2c6e86c7c08c0ec700dc2a75ef58 BASE 757bde561d09738858506aecf5de2f050a5f0d5e
ROUND 1 VERDICT changes_requested Verdict: request_changes counts_claim [0, 0, 1, 2] counts_measured [0, 0, 1, 2] count_basis finding finding_ids [{'id': 'c98-khong-khoa-noi-in-that', 'hang': 'P2'}, {'id': 'c98-bo-sot-tran-mac-dinh', 'hang': 'P3'}, {'id': 'c98-bo-sot-so-dong-nem', 'hang': 'P3'}]
ROUND 1 HASH e33a3c3efdeb3d55c7dd2c45ae831d814861690c360071b706026f4c9ed2a95b hash_equal True bytes 14251 bytes_equal True
ROUND 1 EVIDENCE e788a5d0d518f8a08ac13473a85197287fad4fcb ops/reviews/wp1037-g1-codex-luot1-verdict.md blob_equal True ancestor_of_review_head_rc 0 reviewed_ancestor_of_merge_rc 0
ROUND 1 MODEL DO_DUOC events 27 served ['gpt-6-astra'] requested_claim gpt-6-astra declared gpt-6-astra declared_served gpt-6-astra evidence do_may ref_exists True
ROUND 2 HEADS 91466322f705658ed51b80c7c152f6b77f4f90c6 91466322f705658ed51b80c7c152f6b77f4f90c6 Reviewed commit: 91466322f705658ed51b80c7c152f6b77f4f90c6 TREE c20eace3f4aacea3f33afc5861688cb94d64cf3d BASE 757bde561d09738858506aecf5de2f050a5f0d5e
ROUND 2 VERDICT approve Verdict: approve counts_claim [0, 0, 0, 0] counts_measured [0, 0, 0, 0] count_basis finding finding_ids []
ROUND 2 HASH 2f482565c235380145253d76ae51ab9606e8d7cfc8044d6efd113ff80049feaf hash_equal True bytes 10679 bytes_equal True
ROUND 2 EVIDENCE e788a5d0d518f8a08ac13473a85197287fad4fcb ops/reviews/wp1037-g1-codex-luot2-verdict.md blob_equal True ancestor_of_review_head_rc 0 reviewed_ancestor_of_merge_rc 0
ROUND 2 MODEL DO_DUOC events 19 served ['gpt-6-astra'] requested_claim gpt-6-astra declared gpt-6-astra declared_served gpt-6-astra evidence do_may ref_exists True
```
Cả hai run khai provider/surface/transport `openai_codex/codex_cli/machine`, trạng thái `xong`, rc 0, thời lượng `934.249` và `567.318`; prompt hash khớp. Lease khai executor `claude`, model `claude-opus-5-5`, model_family `claude`; không tự biến lời khai này thành phép đo runtime executor. Khác họ, independent process có run ID riêng, verdict lượt 2 approve; không thấy căn cứ bác `cross_approved` ở dữ liệu đã cấp.

`reviewed_tree`, `base_sha`, `muc_bang_chung_model` không có thành khóa trực tiếp trong receipt; tree có trong verdict gốc và xác minh Git ở trên, base lấy từ lease = `757bde561d09738858506aecf5de2f050a5f0d5e`; mức bằng chứng dùng khóa thực `model_reviewer_identity.model_evidence: do_may`. Schema tối thiểu §7 không bắt các khóa tùy chọn ấy; không tính vắng khóa là finding.

Lượt 1 có `sandbox_trang_thai: KHONG_DO_DUOC` (`luong lay mau sandbox hong (DanhTinhDoi)`); lượt 2 `DO_DUOC`. Không nhầm trạng thái đo sandbox với trạng thái đo model. Đang đối chiếu tiếp cách caveat phản ánh giới hạn này.

### Hướng 5 — Thời điểm rút hạn so với khẳng định đã nhả lease (LỖI)

Lệnh tái lập: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/measure_lease.py` đọc lease snapshot/YAML và `git show -s --format=%cI c24875d`; so thời điểm commit với hạn mới. Output thật (`evidence/lease-timeline.log`):
```text
reviewed_commit_time 2026-10-30T17:41:02+00:00
recording_snapshot_time 2026-10-30T17:37:30Z
lease_sua_lan_cuoi 2026-10-30T17:33:00Z
lease_until 2026-10-30T17:53:00Z lease_expires_at_utc 2026-10-30T17:53:00Z
at_reviewed_commit_lease_expired False seconds_until_expiration 718
da_bi_thay_the None bia_mo None
```
Nguồn còn ghi rõ chỉ nghiệm thu `ai-dang-giu` **sau hạn mới**. Hồ sơ land lại gắn `measured — … DA NHA` và điều kiện `(2) lease da nha` tại snapshot/commit trước hạn. Đây là trạng thái hoàn tất sớm hơn dữ liệu đo, không phải vấn đề gate master hoàn tất sau ghi sổ. Finding đang được xác minh với bộ phân loại lease sẵn có.

### Hướng 6 — Đột biến verdict một byte (KHÔNG PHẢI LỖI; t26 có răng)

Lệnh: `python3 evidence/measure_mutations.py`; biến thể `verdict-one-byte` đổi đúng byte đầu `V`→`v` của bản phẳng lượt 2 trên clone, giữ receipt/bản thư mục; chạy đủ sáu lệnh baseline rồi phục hồi.
Output thật: `t26 rc=1`, `lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0`; thông báo `LỆCH BĂM`, hash thật `42efd80dbb7db15a3c97fd36c9d7423df1dbe640e91fe98b14d8c274457676f9` khác receipt `2f482565…49feaf`.
`bien_nhan_v2 rc=0 TỔNG: ĐẠT`; `land_evidence_nguon rc=0 TỔNG: ĐẠT`; `doctrine_scan rc=0 sạch`; `t27 rc=0 2/2`; `t138 rc=0 1/1`. Các cổng còn xanh không có răng cho byte verdict trong worktree; riêng t26 bắt đúng sai lệch. Log: `evidence/mutant-verdict-one-byte-*.log`.

### Hướng 7 — Đột biến xóa hàng mục lục mới (KHÔNG PHẢI LỖI; t27 có răng)

Cùng script/lệnh, biến thể `readme-delete-toc` chỉ xóa hàng mục lục của verdict lượt 2, giữ nguyên bốn caveat. Output thật:
```text
t27 rc=1
README.md: verdict 'wp1037-g1-codex-luot2-verdict.md' KHÔNG có trong CỘT 'tệp verdict' của bảng 'Mục lục'.
lease_publish: 1/2 đạt; đã chạy=2, bỏ qua=0
```
Năm cổng còn lại rc=0: bien_nhan_v2/land_evidence_nguon `TỔNG: ĐẠT`, doctrine sạch, t26 `1/1`, t138 `1/1`. Chốt kiểm mục lục thực tế là t27. Log: `evidence/mutant-readme-delete-toc-*.log`.

### Hướng 8 — Đột biến số đếm P1 trong receipt (KHÔNG PHẢI LỖI ở baseline; chốt số đếm KHÔNG CÓ RĂNG trong bộ cổng đã giao)

Cùng script, biến thể `receipt-so-p1` đổi duy nhất `so_p1: 0`→`so_p1: 1` của receipt lượt 2, không đổi verdict/README/model/assurance. Output thật:
```text
bien_nhan_v2 rc=0 TỔNG: ĐẠT
land_evidence_nguon rc=0 TỔNG: ĐẠT
doctrine_scan rc=0 doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine
t26 rc=0 lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
t27 rc=0 lease_publish: 2/2 đạt; đã chạy=2, bỏ qua=0
t138 rc=0 lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
```
Sửa số đếm sai vẫn xanh mọi cổng; do đó baseline xanh không chứng minh `so_p1` khớp verdict. Baseline được tự đếm độc lập ở Hướng 4 và đúng; không biến giới hạn cổng vốn có thành cáo buộc số baseline sai. Log: `evidence/mutant-receipt-so-p1-*.log`.

Xác nhận tiếp Hướng 5 bằng hàm có sẵn, không sửa code: import `ops/lease_publish.py`, gọi `_phan_loai_lease(snapshot, bay_gio=<thời điểm>)`:
```text
EXISTING_CLASSIFIER 2026-10-30T17:37:30+00:00 CÒN_HẠN
EXISTING_CLASSIFIER 2026-10-30T17:41:02+00:00 CÒN_HẠN
EXISTING_CLASSIFIER 2026-10-30T17:53:00+00:00 HẾT_HẠN
```
Không chạy `ai-dang-giu` theo đồng hồ hiện tại rồi gán kết quả ngược cho SHA cũ.

### Hướng 9 — README: liên kết, hàng trùng và caveat (KHÔNG PHẢI LỖI về cấu trúc)

Lệnh thật: `python3 -` tách phần `## Mục lục`, đếm hàng theo tên tệp chính xác, đối chiếu caveat receipt và kiểm từng link bằng `Path.exists()`; log `evidence/readme.log`.
Output thật:
```text
ROUND 1 TOC_COUNT 1; CAVEAT CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY COUNT 1 LINES [809]
ROUND 1 CAVEAT SCRIPT-DO-DOC-DUONG-DAN-SANDBOX COUNT 1 LINES [810]
ROUND 2 TOC_COUNT 1; CAVEAT CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY COUNT 1 LINES [811]
ROUND 2 CAVEAT SCRIPT-DO-DOC-DUONG-DAN-SANDBOX COUNT 1 LINES [812]
LINKS round 1: verdict True; receipt True; artifact directory True
LINKS round 2: verdict True; receipt True; artifact directory True
```
Hai hàng mục lục ở 1115/1116 có đúng verdict, số đếm, byte count và SHA ở cột SHA; không trùng hàng. Cụm `luc merge (b29da0b)` lượt 2 đọc như định danh sự kiện merge; cột SHA và receipt đều xác nhận head là `9146632`. Không diễn giải riêng cụm ngoặc thành khẳng định đã review merge commit.

Caveat workspace-write chỉ cảnh báo checkout không được cưỡng chế read-only và snapshot sạch là lúc phóng; nó không khai toàn run sandbox được đo thành công. Run lượt 1 có lỗi luồng lấy mẫu; các observation vẫn cho thấy vùng workspace được cấp write. Không nâng caveat này thành bảo đảm sandbox; không tính lỗi đo sampling đã ghi trong nguồn là finding mới về model.

### Hướng 10 — Run/job/runner và nguyên nhân lỗi Windows (LỖI ở nhãn đo nguyên nhân; các số job khớp)

Lệnh đã chạy: `python3 evidence/measure_ci.py`; output đầy đủ `evidence/ci.log`. Trích output thật:
```text
RUN 41033737059 id 41033737059 attempt 1 event pull_request path .github/workflows/ci.yml head_sha 91466322f705658ed51b80c7c152f6b77f4f90c6 status completed conclusion success updated_at 2026-10-30T10:16:52Z
JOBS 41033737059 total_count 23 array_size 23 conclusions {'success': 23} head_sha_all_match True run_attempts [1]
RUNNER_LABELS 41033737059 {('ubuntu-latest',): 23}
JOB 123990054963 gate-ops (ubuntu-latest) conclusion success labels ['ubuntu-latest'] runner_id 1000025788 started_at 2026-10-30T09:30:35Z completed_at 2026-10-30T09:41:30Z
RUN 41069257658-a1 id 41069257658 attempt 1 event workflow_dispatch path .github/workflows/ci.yml head_sha 91466322f705658ed51b80c7c152f6b77f4f90c6 status completed conclusion failure updated_at 2026-10-30T15:07:53Z
JOBS 41069257658-a1 total_count 16 array_size 16 conclusions {'success': 13, 'failure': 2, 'skipped': 1} head_sha_all_match True run_attempts [1]
RUNNER_LABELS 41069257658-a1 {('ubuntu-latest',): 1, ('windows-latest',): 14, (): 1}
JOB 124108765783 gate-ops (windows-latest) conclusion success labels ['windows-latest'] runner_id 1000026073 started_at 2026-10-30T14:08:53Z completed_at 2026-10-30T14:41:04Z
JOB 124108765805 gate-cong-cu (windows-latest, 0) conclusion failure labels ['windows-latest'] runner_id 1000026071 started_at 2026-10-30T14:08:52Z completed_at 2026-10-30T14:09:56Z
FAILED_STEPS [(9, 'G5 manh ban kinh dot bien (#668)', 'failure')]
SHELLCHECK_STEPS [(7, 'cài shellcheck cho G5 (cài xong đo lại)', 'success')]
JOB 124108766201 gate-packet-loop (windows-latest) conclusion failure labels ['windows-latest'] runner_id 1000026080 started_at 2026-10-30T14:08:53Z completed_at 2026-10-30T14:09:57Z
FAILED_STEPS [(9, 'G5 probe ban ke cong cu (#290; selftest T1..T8 chi o job gate, chot M6', 'failure')]
SHELLCHECK_STEPS [(7, 'cài shellcheck cho G5 (cài xong đo lại)', 'success')]
JOB 124109330149 gate-cong-cu-gop conclusion skipped labels [] runner_id None started_at 2026-10-30T14:09:56Z completed_at 2026-10-30T14:09:56Z
RUN 41069257658-a2 id 41069257658 attempt 2 event workflow_dispatch path .github/workflows/ci.yml head_sha 91466322f705658ed51b80c7c152f6b77f4f90c6 status completed conclusion success updated_at 2026-10-30T17:17:33Z
JOBS 41069257658-a2 total_count 16 array_size 16 conclusions {'success': 15, 'skipped': 1} head_sha_all_match True run_attempts [2]
RUNNER_LABELS 41069257658-a2 {('windows-latest',): 14, ('ubuntu-latest',): 1, (): 1}
JOB 124149392588 gate-ops (windows-latest) conclusion success labels ['windows-latest'] runner_id 1000026073 started_at 2026-10-30T14:08:53Z completed_at 2026-10-30T14:41:04Z
JOB 124150752994 gate-cong-cu-gop conclusion skipped labels [] runner_id None started_at 2026-10-30T15:30:05Z completed_at 2026-10-30T15:30:05Z
SOURCE_TOKEN 'runner thieu shellcheck' FILES []
SOURCE_TOKEN 'cai_cong_cu.sh' FILES []
SOURCE_TOKEN '1045' FILES []
SOURCE_TOKEN '255/255' FILES []
SOURCE_TOKEN 'runner_set' FILES []
SOURCE_TOKEN 'windows-only' FILES []
```
Cả attempt có 14 job nhãn Windows, 1 job chuẩn bị Ubuntu, 1 skipped không nhãn/runner; không nhận skipped là đã chạy Windows. Job gate-ops attempt 1 = `124108765783`, runner `1000026073`, Windows, success; attempt 2 có job ID `124149392588` nhưng cùng thời gian/runner của lượt thành công cũ, không suy nó chạy lại. Số `95/95 · 137/137 · 2/2`, `255/255` được hồ sơ gắn rõ `thuat_lai … log khong luu trong kho`; KHÔNG coi là số tự đo bằng jobs JSON.

Ngược lại, nguyên nhân `runner thieu shellcheck — goc loi ops/cai_cong_cu.sh, tach packet #1045` nằm ngay trong câu `measured`, không có log/nguồn chứng minh; JSON chỉ chứng minh hai bước G5 thất bại. Hai step cài shellcheck báo success, nên càng không thể từ metadata suy kết luận thiếu công cụ ở bước sau. Không kết luận nguyên nhân đó sai; kết luận nhãn **measured** mạnh hơn evidence. `runner_set=windows-only` cũng không xuất hiện trong run/jobs JSON (chỉ đo được nhãn runner thật). Finding P2 bên dưới yêu cầu tách lời thuật lại hoặc giữ log đúng run/attempt.

### Hướng 11 — Merge, provenance CI, pending có mốc và lý do landed:false (KHÔNG PHẢI LỖI, trừ nhả lease ở Hướng 5)

Cùng lệnh `python3 evidence/measure_ci.py`, output thật:
```text
POST_MERGE {'id': 41099184556, 'run_attempt': 1, 'event': 'push', 'head_sha': 'b29da0bfe3bfb7a7be69136a1c5c40f82c088a93', 'status': 'pending', 'conclusion': None, 'updated_at': '2026-10-30T17:28:54Z'}
PR 1041 True 2026-10-30T17:28:50Z ducthangho head 91466322f705658ed51b80c7c152f6b77f4f90c6 base 757bde561d09738858506aecf5de2f050a5f0d5e merge b29da0bfe3bfb7a7be69136a1c5c40f82c088a93
MERGE_OBJECT b29da0bfe3bfb7a7be69136a1c5c40f82c088a93 24a37bebf90e5f8e2dd3d4a34e842f2e2f9c6a39 8cdb15a786304bab084b43c8b30c127ae87e2594 91466322f705658ed51b80c7c152f6b77f4f90c6
DIFF 757bde561d09738858506aecf5de2f050a5f0d5e 91466322f705658ed51b80c7c152f6b77f4f90c6 sha256 40b6d80f2c0140953cc8712362138de059503982cce0e736b9a196b892ad2198 numstat 120	4	ops/bien_nhan_v2_test.py
DIFF b29da0bfe3bfb7a7be69136a1c5c40f82c088a93^1 b29da0bfe3bfb7a7be69136a1c5c40f82c088a93 sha256 40b6d80f2c0140953cc8712362138de059503982cce0e736b9a196b892ad2198 numstat 120	4	ops/bien_nhan_v2_test.py
OWNER_COMMENT 6529010520 ducthangho OWNER 2026-10-30T17:25:09Z contains_authorized_head False
PARENTS2_EQUALS_REVIEWED True
LANDED False REVIEWER_ASSURANCE_81 DAT
```
Các câu pending đều gắn `luc ghi so`, `17:37Z`, hoặc nằm trong đoạn snapshot được header định thời. Không suy pending là hiện trạng sau snapshot; không gọi mạng để lấy kết quả tương lai. Nguồn Run có đủ ID/attempt/event/head_sha. Checkout parents/tree/log của job, definition commit/blob/hash và command/rc/positive marker CI không được giữ trong provenance; hồ sơ đã khai `KHONG DO DUOC`, không tự lấy REST head_sha lấp các mốc đó. 403 GraphQL là lời giải thích của executor, không có raw lỗi riêng trong provenance để tôi xác minh HTTP status; phép đo offline chỉ xác nhận thiếu nguồn, không chứng nhận nguyên nhân 403.

Comment owner nêu điều kiện và thứ tự merge nhưng không exact SHA; PR API xác nhận merged_by, không chứng minh người/phien bấm credential (hồ sơ có caveat đúng). Vì thiếu post-merge provenance và durable exact-SHA authorization, `landed: false` vẫn hợp lý. Không nâng merge thành landed. Assurances model/effort/sandbox của reviewer lượt 2 được run.json hỗ trợ; không dùng DAT đó thay CI provenance.

### Hướng 12 — Xóa một caveat mới (KHÔNG PHẢI LỖI; t27 có răng)

`python3 evidence/measure_mutations.py`, biến thể `readme-delete-caveat`: chỉ xóa hàng `CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY` của lượt 2 khỏi README, giữ mục lục và receipt.
Output thật:
```text
t27 rc=1
README.md: caveat 'CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY' của wp1037-g1-codex-luot2-verdict.receipt.yaml KHÔNG nằm ở CỘT 'id' trên cùng hàng với 'wp1037-g1-codex-luot2-verdict.md' ở CỘT 'tệp verdict', trong bảng 'Cảnh báo đang có hiệu lực'.
lease_publish: 1/2 đạt; đã chạy=2, bỏ qua=0
```
Năm cổng còn lại rc=0 với cùng marker dương baseline. Full logs: `evidence/mutant-readme-delete-caveat-*.log`; toàn bộ bốn biến thể/mã thoát ở `evidence/mutations.json`. Tất cả đột biến được phục hồi trong `finally`, không thay code cổng.

### Hướng 13 — Giới hạn danh tính CLI và manifest nguồn (KHÔNG ĐO ĐƯỢC phần không được lưu; phần hash KHÔNG PHẢI LỖI)

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/measure_receipts.py`; output đầy đủ `evidence/receipts.log` giữ mọi trường receipt và các phép đối chiếu. Output thật:
```text
ROUND 1 RUN_START_IN_LEASE True assurance cross_reviewed executor_provider claude executor_lease_model claude-opus-5-5 executor_lease_family claude
ROUND 2 RUN_START_IN_LEASE True assurance cross_approved executor_provider claude executor_lease_model claude-opus-5-5 executor_lease_family claude
ROUND 1 CLI_VERSION_METADATA_FIELDS [] CLI_version_in_archived_stdout_stderr False
ROUND 2 CLI_VERSION_METADATA_FIELDS [] CLI_version_in_archived_stdout_stderr False
luot1-PROMPT.md OK
luot1-VERDICT-codex.md OK
luot1-run.json OK
luot2-PROMPT.md OK
luot2-VERDICT-codex.md OK
luot2-run.json OK
WRITE_SET_HASH d7872905e38bb8e57304520785c71c0562f88d84f60946af2cfb41e4f2cd792a d7872905e38bb8e57304520785c71c0562f88d84f60946af2cfb41e4f2cd792a
```
`run.json.lenh` chỉ giữ chương trình, số đối số và fingerprint; không giữ raw argv/CLI version. Vì vậy chuỗi `codex-cli 0.164.0` và toàn bộ cờ trong trường `cli` là lời khai cấu hình mà tôi **không đo độc lập được** từ bộ hiện vật này; không lấy model thực phục vụ làm bằng chứng cờ yêu cầu/CLI version. Hai run khai nguồn đo model riêng `DO_DUOC`, nên hạn chế này không bác dữ liệu served model đã đo. `actor_nguon` tự gắn `(b)`, chưa có readback bản chiếu/push credential của PR ghi sổ; không chứng nhận actor đăng bằng suy đoán từ commit author. Không có bằng chứng trái ngược để kết tội các lời khai này là sai.

### Hướng 14 — Kiểm HINT.patch trên bản sao (KHÔNG PHẢI LỖI của bản gợi ý)

Lệnh: `python3 evidence/make_hint.py`; `patch --dry-run --fuzz=0 -p0 -d review-copy < HINT.patch`, khi clone sạch tại `c24875d`.
Output thật (`evidence/hint-dry-run.log`, `.rc`):
```text
checking file ops/land/pr1041-wp1037-land-evidence.yaml
rc=0
```
Đã thử áp thật trên clone (`patch --fuzz=0 -p0`) rồi chạy `python3 ops/land_evidence_nguon.py --root . --tep ops/land/pr1041-wp1037-land-evidence.yaml`:
```text
apply rc 0 patching file ops/land/pr1041-wp1037-land-evidence.yaml
ĐẠT ops/land/pr1041-wp1037-land-evidence.yaml
land_evidence_nguon: 1 ĐẠT · 0/0 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 1
TỔNG: ĐẠT
hint land gate rc 0
```
Sau phép đo đã phục hồi byte gốc trong clone. `HINT.patch` định dạng `patch -p0` từ gốc kho, chỉ sửa dữ liệu hồ sơ land; không sửa bản verdict/nguồn nguyên byte và không áp vào `cay-kho/`. Cổng nguồn xanh chỉ kiểm tính hợp lệ cấu trúc/nguồn, không thay các phép đo ngữ nghĩa trong findings.

## FINDINGS

### nha-lease-truoc-khi-het-han  [P1]  Khai đã nhả lease khi lease vẫn còn hạn tại SHA ghi sổ

TỆP/DÒNG: `ops/land/pr1041-wp1037-land-evidence.yaml:70` (đoạn 69–72), `:83` (điều kiện 2); nguồn `ops/land/pr1041-wp1037-provenance/lease-wp1037-r1-g1.yaml.txt:80`, `:117`.

VẤN ĐỀ: Hồ sơ gắn nhãn `measured — ... DA NHA` và coi `(2) lease da nha` là việc xong. Tại snapshot ~17:37Z và commit `c24875d` 17:41:02Z, hạn mới còn ở tương lai 17:53Z. Nguồn không có bia mộ/thay thế và chính nó chỉ nhận nghiệm thu **sau hạn mới**. Bộ phân loại hiện hành vẫn trả `CÒN_HẠN`; rút ngắn thời gian giữ chưa giải phóng write set. Câu “đã nhả” có thể khiến packet #1021 tưởng đường ghi đã trống; phần `Mo lai — TAT CA` cũng bỏ mất bước xác minh nhả sau hạn. Dòng ngoặc `lease con han` ngay trong câu không làm khẳng định `DA NHA` thành đúng.

ĐÃ THỬ NGHIỆM: `git -C cay-kho show -s --format=%cI c24875d` → `2026-10-30T17:41:02+00:00`; đọc hai trường hạn đều `2026-10-30T17:53:00Z`; gọi hàm có sẵn `_phan_loai_lease(lease, bay_gio=...)` → `CÒN_HẠN` lúc 17:37:30Z và 17:41:02Z, `HẾT_HẠN` lúc 17:53Z. Log `evidence/lease-timeline.log`; tại commit còn 718 giây. Không gán kết quả quét ở thời điểm review hôm nay cho thời điểm ghi sổ.

ĐỘ TIN: cao

GỢI Ý VÁ: Sửa `lease.thu_hoi_cuoi`, điều kiện (2) và danh sách mở lại trong chính hồ sơ land, vì đây là nơi chuyển số hạn sang trạng thái hoàn tất. Ghi “đã rút hạn; chưa nhả tại snapshot; cần quét đủ ref sau 17:53Z”, giữ nguyên lease snapshot có băm. Ca khóa: hàm có sẵn phải trả `CÒN_HẠN` ở 17:41:02 và `HẾT_HẠN` đúng 17:53; kiểm hồ sơ không khai bước (2) xong trước đó. Nguy cơ vá: đừng đổi lịch sử thành “đã nhả” dựa trên đồng hồ hiện tại hoặc suy expiry của một blob chứng minh toàn bộ ref đã sạch; cần readback riêng cho lần nghiệm thu sau hạn. Gợi ý dữ liệu ở `HINT.patch`.

### nguyen-nhan-windows-khai-do-thieu-log  [P2]  Gắn nhãn measured cho nguyên nhân thất bại và cấu hình dispatch không có nguồn tương ứng

TỆP/DÒNG: `ops/land/pr1041-wp1037-land-evidence.yaml:39` (`pre_merge_checks[1].name` và `.ghi_chu`).

VẤN ĐỀ: Câu `measured` không chỉ đếm run/job mà còn khẳng định hai lỗi G5 do `runner thieu shellcheck — goc loi ops/cai_cong_cu.sh, tach packet #1045`. Bốn tệp nguồn chỉ là REST metadata; chúng cho thấy step fail và step cài shellcheck success, không có stdout/stderr chẩn đoán hay chứng cứ quy lỗi. Tên check còn ghi `runner_set=windows-only` dù nguồn không giữ inputs dispatch; nhãn job Windows chỉ chứng minh runner đã được cấp. Khác với N/N ở câu cuối đã gắn `thuat_lai ... log khong luu trong kho`, nguyên nhân và input này không được tách giới hạn. Đây là khai rộng hơn phép đo, không phải bằng chứng nguyên nhân thật nhất định sai.

ĐÃ THỬ NGHIỆM: `python3 evidence/measure_ci.py` → hai failed step lần lượt `G5 manh ban kinh dot bien (#668)` và `G5 probe ban ke cong cu (...)`; step 7 `cài shellcheck cho G5 (cài xong đo lại)` đều `success`. Quét toàn bộ provenance: `SOURCE_TOKEN 'runner thieu shellcheck' FILES []`, `'cai_cong_cu.sh' []`, `'1045' []`, `'runner_set' []`, `'windows-only' []`; có nhãn `windows-latest`, runner IDs và run conclusion đúng. `python3 ops/land_evidence_nguon.py --root .` baseline vẫn `TỔNG: ĐẠT`, rc 0: L1 chỉ đo tệp nguồn tồn tại, không kiểm nó chứng minh lời văn. Log `evidence/ci.log` và `evidence/baseline-land_evidence_nguon.log`.

ĐỘ TIN: cao

GỢI Ý VÁ: Tại đúng check Windows này, giữ `measured` cho API status/count/name/labels, tách nguyên nhân và input không có readback thành `thuat_lai`/`not_measured`; hoặc kèm log lỗi của đúng job/run/attempt và nguồn inputs rồi mới khai đo. Sửa tên check theo nhãn runner thực đã đo. Ca khóa: dùng bốn readback hiện có phải chỉ suy ra count, step failure và runner; gỡ log mà vẫn để nguyên nhân `measured` phải bị phát hiện bằng kiểm nội dung riêng (các cổng hiện có không đo điều này). Nguy cơ vá: đừng diễn giải step cài shellcheck success thành bằng chứng công cụ dùng được ở bước G5 sau đó, cũng đừng xóa trạng thái failure/skipped lịch sử khi hạ nhãn nguồn. Gợi ý dữ liệu ở `HINT.patch`.

## KIỂM CUỐI

Đọc lại HEAD/tree, status có cả untracked/ignored, diff worktree/index và từng byte 32 tệp thuộc PR; log `evidence/final-integrity.log`:
```text
cay-kho git rev-parse HEAD HEAD^{tree} rc 0 output c24875d00e93e6a98e0a0abd0837e0cbcad65d4d
9382f7512f3adf569f1f82c4d597c66fa1b463d7
cay-kho git status --short --untracked-files=all --ignored=matching rc 0 output (empty)
cay-kho git diff --exit-code rc 0 output (empty)
cay-kho git diff --cached --exit-code rc 0 output (empty)
cay-kho git diff --check rc 0 output (empty)
review-copy git status --short --untracked-files=all --ignored=matching rc 0 output (empty)
ALL_CHANGED_PATHS_EQUAL_HEAD_BLOB 32 / 32
NUMSTAT 32 files 11630 insertions 0 deletions
core.abbrev 7
origin/master b29da0bfe3bfb7a7be69136a1c5c40f82c088a93
```

Hai finding thuộc hai lớp độc lập: trạng thái lease trước hạn (P1) và lời khai CI rộng hơn nguồn (P2). Không có finding P0/P3. Sáu cổng baseline đều đạt; số đếm P1 không được sáu cổng cưỡng chế, đã ghi phản chứng riêng. Bản gợi ý áp/dry-run được trên clone và đã phục hồi clone; không sửa `cay-kho/`, không push, không gọi mạng. Mọi trạng thái động được đọc theo snapshot nguồn hoặc mốc commit `c24875d`, không dùng trạng thái hiện tại để viết lại lịch sử.
