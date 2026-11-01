Verdict: approve
Reviewed commit: e137f8ce1215e0e6a6c8fbc1aa949b31fa2e4e7d

Hoàn tất cross-review PR #1110 lượt 1: **approve — 0 P0, 0 P1, 0 P2, 0 P3** trong phạm vi đo offline được giao. HEAD/base cùng xanh, delta vi phạm bằng 0; 41 tệp sao chép khớp nguồn, hai tệp loại khai đúng; 116 đối chiếu biên nhận khớp; README giữ đủ hàng cũ và thêm đúng bốn hàng. Đột biến băm bị cổng chặn đúng biên nhận mới. Kho gốc giữ nguyên byte. Lệnh, output và giới hạn đo được ghi dưới đây.

Finding: không có mục `- [P0..P3] <slug>` được xác minh; không có yêu cầu vá.

| Mức | Số finding |
|---|---:|
| P0 | 0 |
| P1 | 0 |
| P2 | 0 |
| P3 | 0 |

Phạm vi: cross-review PR #1110, ghi sổ lượt 1 của PR #1075. Chỉ dùng git/tệp cục bộ; kết quả GitHub ngoài dữ liệu này là KHÔNG ĐO ĐƯỢC. Không cấp quyền merge/land.

Đợt 1 — `PYTHONDONTWRITEBYTECODE=1 python3 prepare_audit.py` → rc0. HEAD `e137f8ce1215e0e6a6c8fbc1aa949b31fa2e4e7d`, tree `49821da8bbf5787a4e10ffcc854354e6c72f9cf8`; merge-base `c6dd7b33b4f215809bf281ee1533bc1e8fa6920c`; 46 tệp đổi, `outside_reviews=[]`, `patch_equal=true`, `status=""`, detached HEAD. `core.abbrev=7`; ba bản sao riêng đã dựng và đặt `git config core.abbrev 7`. Bằng chứng: `evidence/preflight.json`, `evidence/original-snapshot.json`.

Đợt 2 — `PYTHONDONTWRITEBYTECODE=1 python3 audit_archive.py` → rc0; 43 tệp nguồn, 41 tệp sao chép bằng byte, 43 tệp lưu trữ gồm thêm OMITTED.txt/SHA256SUMS. `sha256sum -c SHA256SUMS` → rc0, 42 dòng OK, phủ đủ mọi tệp trừ chính manifest; không mục trùng. Verdict phẳng bằng nguồn: 13376 bytes, SHA256 `b823f2bc10297143977095eca1474d1fc73e2e98be0305173b2c486e9f8c38f6`. Hai tệp loại khai đúng; `unaccounted_source_files=[]`, `errors=[]`. Bằng chứng: `evidence/archive.json`, `evidence/archive-mapping.json`, `evidence/sha256sum.stdout`.

Đợt 3 — `PYTHONDONTWRITEBYTECODE=1 python3 audit_receipt.py` → rc0; 116 đối chiếu, `errors=[]`. SHA/tree, verdict/đếm P*, merge/cha thứ hai, blob neo tổ tiên, telemetry nguồn, prompt/checkpoint/stdout/stderr, class và câu `ket_luan` khớp. 22 trường cố định so tiền lệ pr1071 không lệch. Từng phép so actual/expected ở `evidence/receipt-checks.json`; số đo và phần KHÔNG ĐO ĐƯỢC ở `evidence/receipt.json`.

Đợt 4 — `PYTHONDONTWRITEBYTECODE=1 python3 audit_gates.py` → rc0. Cả năm lệnh cổng trên cả HEAD/base đều rc0. `bien_nhan_v2`: 286→287 ĐẠT v2, tổng 339→340, vi phạm 0→0; `land_evidence_nguon`: 75 ĐẠT, tổng 100, 0 vi phạm ở cả hai. Gọi trực tiếp ba hàm t26/t27 đều PASS; doctrine-scan sạch 10 tệp; diff-check rỗng. Bằng chứng: `evidence/{head,base}-gates.json` và từng tệp `.stdout`/`.stderr`.

Đợt 5 — `PYTHONDONTWRITEBYTECODE=1 python3 audit_readme.py` → rc0; `base_rows=1213`, `head_rows=1217`, `removed=[]`, đúng một mục lục + ba caveat. Bỏ bốn hàng mới khỏi README tại HEAD → bằng base nguyên byte. Merge `e137f8c` giữ mọi hàng của cả hai cha; hiện vật/biên nhận không đổi qua merge. Bằng chứng: `evidence/readme.json`.

Đối chiếu cổng. Lệnh tái hiện từ sandbox: `PYTHONDONTWRITEBYTECODE=1 python3 audit_gates.py`. Lệnh con bên dưới chạy tại `work/base` hoặc `work/head`; runner đặt `PYTHONDONTWRITEBYTECODE=1`, `core.abbrev=7`, lưu cwd/lệnh/rc và hai luồng output riêng.

| Lệnh | Base `c6dd7b3` | Head `e137f8c` | Delta |
|---|---|---|---|
| `python3 ops/bien_nhan_v2.py --root .` | rc0; 286 ĐẠT v2; tổng 339; 0 vi phạm; 0 KHÔNG ĐO ĐƯỢC | rc0; 287 ĐẠT v2; tổng 340; 0 vi phạm; 0 KHÔNG ĐO ĐƯỢC | +1 biên nhận v2; 0 vi phạm mới |
| `python3 ops/land_evidence_nguon.py --root .` | rc0; 75 ĐẠT; 25/28 miễn trừ; tổng 100; 0 vi phạm; 0 KHÔNG ĐO ĐƯỢC | cùng kết quả | 0 |
| `python3 ../../direct_gates.py .` | rc0; ba hàm t26/t27 PASS | rc0; ba hàm t26/t27 PASS | 0 |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | rc0; sạch, quét 10 tệp, 0 chỗ chép doctrine | cùng kết quả | 0 |
| `git diff --check c6dd7b3 HEAD` | rc0; output rỗng | rc0; output rỗng | 0 |

`evidence/{head,base}-bien-nhan.stdout` cùng ghi 11/11 miễn trừ legacy và 42 NỢ đóng băng; không đọc miễn trừ thành đã kiểm lại nội dung. `direct_gates.py` import module của chính checkout, gọi trực tiếp `t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi`, `t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc`, `t27_phan_chung_verdict_duoi_HOA_thieu_muc_luc_phai_DO_tren_moi_nen`; cả ba có kết quả PASS. Hai SyntaxWarning tại dòng 3062/5205 nằm trong stderr của cả HEAD và base, không phải lỗi mới.

Kiểm kê byte. `PYTHONDONTWRITEBYTECODE=1 python3 audit_archive.py` → 41/41 bản sao khớp nguồn, không tệp nguồn đầu vào bị bỏ sót mà không khai. Ánh xạ bao gồm `launcher.out ↔ launcher.json`, `run/* ↔ runs/71490d5a/*`, `evidence/*.py ↔ *.py` gốc. `evidence/archive-mapping.json` ghi từng đường dẫn, bytes, SHA256 và kết quả so byte. `sha256sum -c SHA256SUMS` tại `cay-kho/ops/reviews/pr1075-review-1-codex` → rc0; 42 dòng OK, tập manifest bằng toàn bộ tệp trừ chính nó. Hai tệp do ghi sổ thêm là OMITTED.txt và SHA256SUMS.

| Tệp nguồn không đưa vào kho | Bytes đo | SHA256 đo | OMITTED.txt |
|---|---:|---|---|
| `DIFF.patch` | 301308 | `de449cef2a3e30daa823b384a63ae390b972a4ca33240fddffb26761e64cbae1` | khớp |
| `launcher.err` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | khớp |

`audit_receipt.py` chạy `git diff 3574cb0 907c474` → bằng byte DIFF.patch nguồn. Các thư mục gốc `cay-kho/`, `work/`, `nguon/` không nằm trong đầu vào được cấp: nội dung/từng tệp bên trong **KHÔNG ĐO ĐƯỢC**; không coi một dòng loại thư mục là chứng cứ đã băm từng tệp của nó.

Biên nhận. Lệnh tái hiện: `PYTHONDONTWRITEBYTECODE=1 python3 audit_receipt.py` → rc0, 116 đối chiếu, `errors=[]`. Mỗi đối chiếu có actual/expected/ok trong `evidence/receipt-checks.json`.

| Trường | Output đo từ git/tệp nguồn |
|---|---|
| Verdict/đếm finding | `approve`; P0/P1/P2/P3 = 0/0/0/0; IDs rỗng; khớp dòng 1 và dòng 4 verdict |
| `reviewed_sha` | `907c474e5dd22b2f389e8c342e7c79c6fbcb760e`; khớp dòng 2 verdict và run.json |
| `reviewed_tree` | `d01f444ce113e812178093aab25ce3ea9d14aeed` |
| Verdict bytes/SHA256 | 13376; `b823f2bc10297143977095eca1474d1fc73e2e98be0305173b2c486e9f8c38f6` |
| `land_merge_commit` | `53d670cf5bdeee1c5a5dcb5cefa6a0e7ff9a8b54` |
| Hai cha merge | `a284f8a5d5f980cc155dfb939253fc84c7901ea3`, `907c474e5dd22b2f389e8c342e7c79c6fbcb760e` |
| `evidence_url` commit | `f0c4ed69e5901bd2122f51cf96c7c7d6a7af8606`; blob bằng byte/băm verdict nguồn |
| `run_id` | `71490d5a710944e395c81836182f3c99` |
| `ma_thoat`, trạng thái, thời lượng | 0; `xong`; 412.567 giây; chênh timestamp 412.566729 giây |
| Model/effort lịch sử | 19 sự kiện, 19 response_id khác nhau, chỉ `gpt-6-astra`; effort `xhigh`; trạng thái telemetry `DO_DUOC` |
| `prompt_sha256` | `766febde02127566e8ab3b4b0248c5ecc95bc6794fee912fcee60e9dd9854550` |
| `sandbox_trang_thai` | run.json lịch sử ghi `DO_DUOC`; có quan sát và giới hạn lấy mẫu |
| `_tinh_lop_tu_write_set` trên diff `3574cb0..907c474` | 58 tệp, toàn bộ `ops/reviews/**`; trả `sensitive`, khớp cả hai trường class |

Cùng script chạy `git merge-base --is-ancestor f0c4ed6 HEAD` và `git merge-base --is-ancestor f0c4ed6 6af4c9a` → rc0; `git show f0c4ed6:ops/reviews/pr1075-review-1-codex-verdict.md` → băm và byte như bảng. `git merge-base --is-ancestor 53d670c origin/master` → rc0. `git merge-base 907c474 53d670c^1` → `3574cb07dba8a8f7f32384ee3d1d3dfbf3a4f70e`. Commit date `53d670c` là `2026-11-01T12:53:47+07:00`; đây là metadata git, không thay cho thời điểm `merged_at` qua API.

`launcher.json` parse bằng run.json; checkpoint khớp hash/run_id/head/prompt; stdout/stderr khớp hash/bytes trong run.json. Các con số model/effort ở trên là đối chiếu telemetry lưu lại, không suy từ cờ yêu cầu CLI. Source prompt.snapshot được run.json khai đã xóa; không có trong tập tệp nguồn đầu vào, nên không phải tệp nguồn bị bỏ sót khi ghi sổ.

`ket_luan` khớp dòng 4 verdict và các kết quả lưu trong nguồn: 53 tệp chép, hai tệp loại, 75 đối chiếu biên nhận, bốn hàng README mới, không mất hàng cũ, đột biến băm đỏ đúng pr1071. Output `evidence/receipt.json.ket_luan_saved_source_counts` ghi các số này. Đây là kiểm câu tóm tắt **review #1075 về việc ghi sổ #1071**; con số 53 không phải số tệp ghi sổ mới của PR #1110 (đo được là 41). Không tuyên bố đã chạy lại toàn bộ review lịch sử thiếu nguồn con.

README/lịch sử. `PYTHONDONTWRITEBYTECODE=1 python3 audit_readme.py` → rc0, `errors=[]`. So tập đa hàng bắt đầu `| `, giữ cả số lần lặp: base 1213, HEAD 1217, `removed=[]`. Ba ID/nội dung caveat bằng biên nhận; mục lục khớp verdict, assurance, lượt, PR, đếm P*, model/run, head, merge, bytes và liên kết. Bỏ đúng bốn hàng mới khỏi toàn văn → bằng base nguyên byte.

| Commit | Output đo |
|---|---|
| `f0c4ed6` | 44 tệp hiện vật mới; đúng tập hiện vật trong diff của PR |
| `6af4c9a` | chỉ README và biên nhận, hai tệp |
| `e137f8c` | hai cha `6af4c9a`, `c6dd7b3`; giữ 1217/1213 hàng của từng cha; thiếu 0/0 |

`git diff 6af4c9a HEAD -- ops/reviews/pr1075-review-1-codex ops/reviews/pr1075-review-1-codex-verdict.md ops/reviews/pr1075-review-1-codex-verdict.receipt.yaml` → rỗng. Merge không đổi hiện vật/biên nhận. Toàn bộ danh sách đường dẫn/lịch sử được lưu ở `evidence/readme.json.history`.

Tiền lệ. `audit_receipt.py` → `precedent_fixed_fields=22`, `precedent_fixed_differences={}` khi so với pr1071 lượt 1; loại/cường độ neo, ba ID/mức caveat, các trường identity cấu trúc cũng khớp. Các trường thay đổi được liệt kê tại `precedent_changed_fields`: PR/SHA/tree/băm/run/thời lượng/số tệp/tóm tắt đổi theo nguồn mới. Caveat tệp loại chuyển từ `evidence/readme.diff` sang `launcher.err` phù hợp tập nguồn đã đo; `evidence/readme.diff` lần này đã có trong manifest và khớp byte. Không thấy khác biệt thiếu lý do trong các trường đã đối chiếu.

Giới hạn và lời khai rộng hơn phép đo. `PYTHONDONTWRITEBYTECODE=1 python3 audit_receipt.py` lưu `unmeasured` trong `evidence/receipt.json`; các mục dưới không được suy thành đã xác thực từ cổng xanh:

- `land_merge_commit_ghi_chu` ghi `(a)` cho cả `merge_method merge` và `expectedHeadSha`: git đo được đồ thị hai cha/cha thứ hai; tham số request GitHub **KHÔNG ĐO ĐƯỢC**. Trạng thái PR/CI hiện tại, quyền/actor tài khoản và việc URL được phục vụ công khai cũng **KHÔNG ĐO ĐƯỢC**.
- `model_reviewer_identity.cli` khai phiên bản `codex-cli 0.164.0`, launcher argv/cờ, model/effort yêu cầu: **KHÔNG ĐO ĐƯỢC** từ run.json chỉ giữ chương trình/số đối số/vân tay. Phần model/effort được phục vụ đã đối chiếu telemetry lưu lại như bảng, không chứng thực ngoài nguồn đó.
- Họ/danh tính executor, chỉ thị chủ kho, việc không fork hoặc tái sử dụng context ngoài prompt/run/checkpoint được cấp: **KHÔNG ĐO ĐƯỢC** độc lập. Việc `cross_approved` khớp tiền lệ không thay thế kiểm chứng các danh tính này.
- `sandbox_gioi_han` ghi lấy mẫu mỗi 0.2 giây, có thể lọt lệnh ngắn; `DO_DUOC` chỉ nói đã quan sát cơ chế. Cưỡng chế mọi lệnh lịch sử: **KHÔNG ĐO ĐƯỢC**. Ba caveat liên quan đã hiện đủ trên README.

Những giới hạn này cùng dạng với pr1071, không phải bằng chứng mâu thuẫn mới của PR #1110. Kết luận review chỉ áp dụng tính toàn vẹn và trung thực ghi sổ trong phạm vi git/tệp được cấp.

Phản chứng. `PYTHONDONTWRITEBYTECODE=1 python3 audit_mutation.py` → rc0 của phép thử. Chỉ sửa `verdict_sha256` thành 64 ký tự `f` trên `work/mutant`; `git diff --numstat` → `1 1 ops/reviews/pr1075-review-1-codex-verdict.receipt.yaml`. Giữ hình dạng băm hợp lệ để kiểm nội dung, không chỉ schema.

- `python3 ops/bien_nhan_v2.py --root .` → rc1; 1 vi phạm, `red_receipts=["pr1075-review-1-codex-verdict.receipt.yaml"]`. Stderr: `ĐỎ pr1075-review-1-codex-verdict.receipt.yaml: ... blob tại evidence_url băm b823f2bc1029… nhưng biên nhận khai verdict_sha256 ffffffffffff… — mỏ neo KHÔNG trỏ đúng thứ nó khai`.
- `python3 ../../direct_gates.py .` → rc1; t26 FAIL với `pr1075-review-1-codex-verdict.receipt.yaml: LỆCH BĂM`; cả hai t27 PASS.
- Khôi phục byte gốc → `restored_bytewise=true`, `status_after=""`. Bằng chứng đầy đủ: `evidence/mutation.json`, `evidence/mutant-{bien-nhan,direct}.{stdout,stderr}`.

Bộ đọc log lần đầu của phép thử chỉ tìm thông báo đỏ trên stdout nên assertion của **script đo** thất bại; cổng đã báo đúng trên stderr. Đã sửa script đo đọc cả hai luồng và chạy lại thành công như trên; lần đầu giữ tại `evidence/attempt1-*`. Đây không phải finding của kho được review.

Toàn vẹn cuối. `PYTHONDONTWRITEBYTECODE=1 python3 final_audit.py` → rc0, `errors=[]`; đối chiếu 12730 tệp của kho gốc, gồm `.git`, cho `original_snapshot_equal=true`. `git status --porcelain=v1 --untracked-files=all --ignored` → rỗng tại `cay-kho`, `work/head`, `work/base`, `work/mutant`. HEAD/tree gốc giữ nguyên như dòng 2 và preflight. Output land/direct/doctrine/diff-check HEAD/base bằng byte; SyntaxWarning sau chuẩn hóa đường dẫn bằng nhau; đột biến đã khôi phục. Bằng chứng: `evidence/final-integrity.json`.
