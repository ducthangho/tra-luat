Verdict: request_changes
Reviewed commit: 5dd347c67da680099e292acf02da7e363a0559bd

Hoàn tất cross-review PR #1058 lượt 1: **request_changes — 0 P0, 0 P1, 1 P2, 1 P3**. Các cổng đều qua, không có delta lỗi so base; byte/hashes, trường định lượng của ba biên nhận và hàng README khớp nguồn. Hai finding nằm ở lời khai của hồ sơ land. Lệnh và output ở các mục đo bên dưới và `evidence/`; script tái hiện đều nằm ngoài `cay-kho/`. Không cấp quyền merge/land.

Finding (hai lớp, hai biểu hiện):

- [P2] uy-quyen-land-suy-tu-merge: `ops/land/pr1047-wp1045-land-evidence.yaml:34` — `PYTHONDONTWRITEBYTECODE=1 python3 finding_checks.py authorization` — output `authorization_claim="uy quyen land la hanh dong merge cua chu kho."`, trong khi chính điều kiện (5) của tệp là `uy quyen land neo SHA: CHUA DAT` và yêu cầu mở lại là `chu kho ghi duyet ben neo 2014602`. Readback PR chỉ có `merged=true`, `merged_by=ducthangho`, head `2014602…`; comment 6529094452 ghi hộ nâng trần và điều kiện merge. Danh tính người bấm/duyệt land exact-SHA: **KHÔNG ĐO ĐƯỢC** từ hai nguồn này (dòng 35 cũng tự giới hạn như vậy). Câu cuối dòng 34 biến bằng chứng thao tác thành bằng chứng ủy quyền ngay trong trường authorization, trái mục đích tách hai vai của protocol §7 và điều kiện cuối hồ sơ. — Hướng vá: bỏ hoặc đính chính câu này thành “readback chỉ chứng minh thao tác merge; chưa có nguồn duyệt land bền neo exact SHA”, đồng bộ với điều kiện (5); giữ `landed: false`, không sửa readback. Kiểm đóng bằng cùng lệnh: lời giải thích authorization và điều kiện mở lại phải cùng ghi thiếu bằng chứng duyệt; việc sửa văn xuôi không được đổi kết luận merged hay tạo quyền land.

- [P3] nhan-windows-ke-ca-job-skipped: `ops/land/pr1047-wp1045-land-evidence.yaml:42` — `PYTHONDONTWRITEBYTECODE=1 python3 finding_checks.py labels` — output phản ví dụ duy nhất: `id=124215501550`, `name=gate-cong-cu-gop`, `conclusion=skipped`, `labels=[]`, `runner_id=null`; `executed_gate_jobs=14`, tổng `15 success / 1 skipped`. Vì vậy câu **measured** “moi job gate* nhan windows-latest” rộng hơn nguồn, dù số skipped ở cùng dòng đã được ghi đúng. — Hướng vá: ghi “14 job gate* đã chạy có nhãn windows-latest; gate-cong-cu-gop skipped, không có runner/nhãn”; giữ `chuan-bi` Ubuntu và tổng 15/1. Kiểm đóng: đối chiếu tất cả gate* đã chạy với nhãn, tách job skipped; không sửa JSON hay nâng skipped thành Windows execution/pass (protocol §10.2.3).


- Tiền kiểm: `git config core.abbrev 7; git rev-parse HEAD; git merge-base HEAD origin/master; git status --porcelain=v1` → head `5dd347c67da680099e292acf02da7e363a0559bd`; base `afc82f6d7447eb76fc8adbe46c1be90be88d331f`; status rỗng (rc 0).
- Phép đo tiếp theo dùng `PYTHONDONTWRITEBYTECODE=1`. Không truy cập mạng. Sự thật trực tiếp trên GitHub: KHÔNG ĐO ĐƯỢC; chỉ đối chiếu lời khai với readback được cung cấp.

Cập nhật 1 — kết quả cổng:

Lệnh tái hiện cả hai mốc: `PYTHONDONTWRITEBYTECODE=1 python3 gates.py` (bản base là clone riêng trong sandbox). Log: `evidence/gates.json`, `evidence/{head,base}-*.log`.

| Phép đo | Base afc82f6 | Head 5dd347c | Delta |
|---|---|---|---|
| `python3 ops/bien_nhan_v2.py --root .` | rc0; 257 ĐẠT v2, 11/11 legacy, 42 NỢ, 0 vi phạm, tổng 310 | rc0; 260 ĐẠT v2, 11/11 legacy, 42 NỢ, 0 vi phạm, tổng 313 | +3 v2; 0 vi phạm mới |
| `python3 ops/land_evidence_nguon.py --root .` | rc0; 66 ĐẠT, 25/28 miễn trừ, 0 vi phạm, tổng 91 | rc0; 67 ĐẠT, 25/28 miễn trừ, 0 vi phạm, tổng 92 | +1 ĐẠT; 0 vi phạm mới |
| `python3 ../direct_cases.py .` | rc0, PASS 3/3 direct functions | rc0, PASS 3/3 direct functions | 0; hai SyntaxWarning giống nhau |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | rc0, quét 10 tệp, 0 chỗ chép doctrine | rc0, quét 10 tệp, 0 chỗ chép doctrine | 0 |
| `git diff --check` | rc0, output rỗng | rc0, output rỗng | 0 |

`git diff --check afc82f6 HEAD` → rc0, output rỗng (`evidence/diff-range-check.log`). Cổng xanh chưa chứng minh mọi lời khai trong hồ sơ đúng nghĩa.

Cập nhật 2 — byte, biên nhận và Git đã đo:

`PYTHONDONTWRITEBYTECODE=1 python3 audit.py bytes receipts git` → rc0, `bytes PASS`, `receipts PASS`, `git PASS`; chi tiết `evidence/audit.log` và `evidence/checksums.log`.

- Mỗi lượt có 6/6 tệp gốc trùng byte với cả lease ref `a430543` và commit handoff `4b4f37f`; bản phẳng trùng `VERDICT.md`. Thư mục ghi sổ bổ sung `SHA256SUMS` (không có trong handoff gốc). Các manifest mới: 6 + 6 + 6 + 21 mục đều `OK`, rc0, phủ đủ tệp.
- Ba verdict: `request_changes`, `request_changes`, `approve`; đếm P0/P1/P2/P3 lần lượt `0/0/1/2`, `0/0/0/1`, `0/0/0/0`; IDs, SHA và kích thước khớp receipt. Tất cả reviewed SHA là tổ tiên của `b2d5f06` (rc0). Cả ba evidence URL neo `01171edfc6a8f6f9cd196e053118ba9e633a3227`, tổ tiên HEAD (rc0), blob đúng byte.
- Run IDs đúng lượt, rc0/xong; thời lượng 825.648 / 910.839 / 836.55 giây, sai số <0.001 giây so timestamp; sự kiện model 25 / 42 / 43 đều `gpt-6-astra`, effort `[xhigh]`, trạng thái model/effort `DO_DUOC`. Hash prompt/stdout/stderr/checkpoint khớp. Cả ba sandbox `KHONG_DO_DUOC` với lý do `DanhTinhDoi`.
- `bat_dau_utc` lượt 1/2 nằm trong cửa sổ g1 `[15:10,17:29)` ngày 30-10; lượt 3 bắt đầu 17:30:56 trong g2. Snapshot lease khớp byte Git; spec/write_set hash khớp; hạn mới `00:20Z` bằng thời điểm sửa +1200 giây; g1 không đổi ở `a430543`.
- `merge-va-diff.txt` khớp mọi output Git đã ghi: head tree `332aed0…`, merge tree `4687675…`, hai parents `6db9341…` / `2014602…`; hai diff cùng SHA-256 `65b4fa2e33f4c39fec5d4a287d3b1c94decdcde532141d25ab0bd82b046a69d7`, 2 tệp, +276/-10.

Phản ví dụ nhãn job đã được ghi tăng dần ở bước này; kết luận và hướng vá nằm trong finding `nhan-windows-ke-ca-job-skipped` ở đầu tệp.

Cập nhật 3 — readback và README đã đối chiếu:

`PYTHONDONTWRITEBYTECODE=1 python3 provenance_audit.py` → rc0; log `evidence/provenance.log`. Script giữ nguyên phản ví dụ nhãn Windows, không biến nó thành PASS.

| Run | SHA trong readback | Event / attempt | Trạng thái / số job đọc được |
|---|---|---|---|
| 41099144196 | 2014602 | pull_request / 1 | completed success; 23 success; 23 ubuntu-latest |
| 41099486628 | 2014602 | workflow_dispatch / 1 | completed success; 15 success + 1 skipped; 1 Ubuntu, 14 Windows, 1 không nhãn |
| 41110458965 | 2014602 | workflow_dispatch / 1 | completed success; 2 success; 1 Windows, 1 Ubuntu |
| 41145468254 | b2d5f06 | push / 1 | snapshot đầu in_progress/null; sau completed success, 23 success Ubuntu; updated_at 2026-10-31T00:31:59Z |
| 41145468496 | b2d5f06 | push / 1 | snapshot đầu in_progress/null; sau completed success, 2 success (Windows/Ubuntu); updated_at 2026-10-30T23:44:12Z |
| 41147719416 | a430543 | push / 1 | completed success; updated_at 2026-10-31T00:03:46Z; không có jobs/log để xác minh rc9 |

`total_count` bằng số job thực có, IDs không trùng; run_id/attempt/head_sha của mọi job khớp run. Hai job Windows được hồ sơ nêu đều có đúng bước cài shellcheck và G5 `completed/success` trong readback. Đây là đo nội dung readback, không phải đo lại CI.

Cùng lệnh cho các output sau:

- PR readback: `merged=true`, `merged_by=ducthangho`, `merged_at=2026-10-30T23:36:15Z`, head `2014602…`, base `5e458f4…`, merge `b2d5f06…`; các run tiền merge đã kết thúc trước merged_at.
- Comment 6529094452: `user=ducthangho`, app `claude`, `created_at=2026-10-30T17:29:22Z`; body là ghi hộ nâng trần 2→4 và nhắc điều kiện merge. Không phải approval exact SHA. Comment 6531582115: `chatgpt-codex-connector[bot]`, updated_at `19:24:25Z`, **code_review** completed trên `2014602…`, hai cờ findings false, trigger `Draft marked ready`; **security_review** là null.
- Tệp `ai-dang-giu-sau-rut-han/luc-do.txt`: ba đường dẫn đều ghi `NGƯỜI_GIỮ 0`, rc0, g1 `CÒN_HẠN · ĐÃ_BỊ_THAY_THẾ`, g2 `HẾT_HẠN`; mốc 00:23:19 sau hạn 00:20. Con số 713/713 và thiếu/thừa 0 có trong snapshot; không đo lại được tính đầy đủ của remote tại thời điểm lịch sử.
- README: mọi dòng base còn nguyên, đúng thứ tự trong merge `33118e0` và HEAD; 8 hàng PR #1050 giữ nguyên byte. Mỗi lượt wp1045 có 1 hàng mục lục + 3 caveat; lease, generation, verdict, assurance ghi trong receipt, run ID, reviewed SHA, số finding, số byte khớp.

`PYTHONDONTWRITEBYTECODE=1 python3 finding_checks.py` → rc0; `evidence/findings.log` chứa hai phản ví dụ để tái hiện độc lập.

Cập nhật cuối — trạng thái, giới hạn và toàn vẹn:

- `PYTHONDONTWRITEBYTECODE=1 python3 provenance_audit.py` → `land_status` có `landed=false`, `assurance_81=CHUA_DAT`; `python3 audit.py receipts` → cả ba `sandbox_state=KHONG_DO_DUOC`. Giữ hai trạng thái này phù hợp bằng chứng thiếu sandbox và thiếu Checkout / Workflow definition / Gate output. Hai snapshot in_progress rồi success mô tả hai thời điểm, không mâu thuẫn. Review `approve`/`cross_approved` ở receipt và README không được dùng để suy §8.1 đã ĐẠT; cả receipt lượt 3 và hồ sơ đều ghi rõ giới hạn ấy. Câu suy ủy quyền từ merge vẫn phải sửa như finding P2.
- `git diff --name-only afc82f6 HEAD` → 51 tệp, ngoài `ops/reviews/**`/`ops/land/**` = `[]`; đối chiếu byte `git diff afc82f6 HEAD` với `DIFF.patch` → `True`, SHA-256 `a8e3d2e479804d07751849d0dc4f74a2ae4c7d5613473833a8a3a9470a1ed8da` (`evidence/final-state.json`).
- Kiểm cuối `git rev-parse HEAD HEAD^{tree}` → head `5dd347c67da680099e292acf02da7e363a0559bd`, tree `7176a9306859b0b772d49d6ddf9d5ddca0cf8167`. `git status --porcelain=v1 --untracked-files=all --ignored`, `git diff --exit-code`, `git diff --cached --exit-code` → cả ba rc0, stdout/stderr rỗng. Không có thay đổi nội dung checkout quan sát được ở mốc cuối; chỉ cấu hình `core.abbrev=7` theo yêu cầu.

**KHÔNG ĐO ĐƯỢC** trong review này:

| Phần | Lệnh/nguồn đã đối chiếu và giới hạn |
|---|---|
| Trạng thái GitHub thật, tính xác thực/đầy đủ của REST readback, giờ thực hiện GET 23:40/04:05 và lỗi GraphQL 403 | `python3 provenance_audit.py` chỉ đọc tệp được cung cấp; các `created_at`/`updated_at` là trường trong JSON, không chứng minh thời điểm tải. Không có phép gọi mạng. |
| Người thật bấm merge, phiên dùng credential, approval exact SHA | `python3 finding_checks.py authorization` chỉ thu được actor tài khoản và comment ghi hộ; không suy thêm danh tính/quyền. |
| Checkout CI, exact workflow-definition OID/blob/hash của run và output/rc/marker từng gate | `python3 provenance_audit.py` đo run/jobs/steps JSON; không có bộ provenance đủ bốn mốc §10.2.2. `head_sha` và nhãn runner không thay ba mốc còn thiếu. |
| Số ca CI 312/312, 255/255, đột biến 502/502, 410/410; log publish lease rc9 | `rg -n 'Thuat_lai|thuat_lai|khong luu' cay-kho/ops/land/pr1047-wp1045-land-evidence.yaml` → các dòng 43, 84–85 đã đánh dấu thuật lại/không lưu log. Không tái chứng nhận các số này từ jobs JSON. |
| Đầy đủ ref và người giữ lease tại 00:23 lịch sử | `python3 provenance_audit.py` đối chiếu snapshot 713/713, NGƯỜI_GIỮ 0 ×3; `git for-each-ref --format='%(refname)' refs/remotes/origin` hiện có 717 nhánh khi loại `/HEAD` (`evidence/final-state.json`). Không dùng tập ref hiện tại để xác nhận tập remote lịch sử hoặc tuyên bố ai đang giữ ở hiện tại. |
| Thực thi lại phép đo trong các VERDICT gốc, toàn bộ lịch sử sandbox/context độc lập và argv CLI nguyên văn | `python3 audit.py bytes receipts` xác minh bản sao, run JSON, hash và những trường có thể đo. `git ls-tree -r` của ba thư mục handoff chỉ có 6 tệp/lượt; không có `evidence/`. Receipt/README đã nêu thiếu script, checkout không cưỡng chế read-only và sandbox `KHONG_DO_DUOC`. Các kết quả bên trong verdict gốc chỉ được đối chiếu là lời của nguồn, không tự nhận đã tái chạy. |

Ngưỡng yêu cầu là không còn P0/P1/P2/P3; hai finding trên khiến PR chưa đạt ngưỡng. Kết luận chỉ áp dụng commit đã ghi ở dòng 2.
