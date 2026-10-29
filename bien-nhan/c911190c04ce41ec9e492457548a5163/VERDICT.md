verdict: approved
reviewed_sha: f4d15edcb5d0a9742182273e5950f76165060667
Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.

Đã review lại TOÀN BỘ diff trên hai trục **Spec** và **Standards/Security**, từ baseline `96667715996d41bc45e70a64fbaa8996de20f6a0` tới SHA ở dòng 2. Áp ngưỡng **0 P0–P3** của đặc tả §3, với effective review class `sensitive` theo lease; không có finding mới.

Reviewer: `openai_codex`, `model_family: openai`, phiên độc lập với Executor Claude. Metadata `run/c911190c/run.json` ghi `execution_surface: codex_cli`, `transport: machine`, run ID `c911190c04ce41ec9e492457548a5163`. Metadata chưa có bằng chứng model/effort phục vụ từng response; không suy các giá trị đó từ tên công cụ. Báo cáo này kết luận nội dung review, không tự chuyển state/assurance, xác nhận required CI hay cấp quyền merge/land.

Candidate tree: `dbef3516db6055cd1d5b5d88736a6c9b69dbfe10`. Đặc tả authoritative tại `96667715996d41bc45e70a64fbaa8996de20f6a0:ops/specs/WINDOWS-LOCAL-MAY-CHU-KHO-r1.md` và bản trong checkout có cùng SHA-256 `377ecea689043fcab4d007d65d9592bd28819fa37983796e0c1b75b2c154e715`. Lease khớp packet/revision 1/generation 1, baseline và hai đường dẫn được phép; `write_set_hash` được tính lại và khớp. Checkout đang detached tại candidate; branch packet trong clone cũng trỏ candidate.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn: `VERDICT-luot-1.md`, reviewed SHA `fff91390dafb3b8a16e6d11a7243dce036618260`; một lớp, một biểu hiện P1.

| Lớp / finding | Kết quả tự kiểm trên SHA hiện tại | Bằng chứng và phạm vi đóng |
|---|---|---|
| `con-tro-tao-them-nghia-vu` [P1 ở lượt 1] | **ĐÃ VÁ THẬT** | `docs/PROTOCOL_DA_PHIEN.md:1015` hiện là ``Quy ước sử dụng máy Windows local của chủ kho nằm tại `ADR-0057`.`` Câu chỉ định vị quy ước, không còn mệnh lệnh chạy test khi máy online. Diff Git từ SHA lượt 1 tới candidate khớp byte với `diff-tu-luot-1.patch` và chỉ thay câu này. Đọc lại toàn ADR và cả hai dòng thêm vào protocol: quyền dùng local vẫn là tùy chọn (ADR:8), điều kiện Online và nghĩa vụ khi đã chạy nằm ở ADR:31–35, không có nghĩa vụ cùng lớp do bản vá sinh ra. |

Quét lớp **nghĩa vụ vượt đặc tả** trên toàn bộ 75 dòng thêm: phần mở đầu, 10 quyết định, “Những gì KHÔNG đổi”, mục cổng, phương án bị loại, hàng §20 và câu §10.2. Mỗi nghĩa vụ truy được về đặc tả §2/§5 hoặc ranh giới đã có trong protocol; không còn biểu hiện mở. Lớp cũ đóng 1/1 (100%); lớp mới 0, lớp tái mở 0. Không dùng scanner xanh thay kết luận đọc nghĩa.

## Đối chiếu đặc tả và tính đúng của lời khai

Mười gạch đầu dòng của đặc tả §2.1 đều có trong ADR:

| Yêu cầu | Vị trí ADR-0057 | Đối chiếu |
|---|---|---|
| Phạm vi | 31–32 | Đúng máy chủ kho, Desktop Commander, `list_devices` = `Online`; không bắt mọi packet dùng local. |
| Merge cộng thêm | 33–35 | Giữ điều kiện đã chạy test; sửa lỗi do diff, nêu lỗi base kèm SHA, khai “không đo local” khi offline; không thay required CI. |
| Khoá | 36–37 | Đúng đường dẫn, mẫu nội dung, xoá nội dung khi xong và không chạy test nặng khi phiên khác giữ. |
| Kiểm tải | 38–39 | Lệnh `Get-CimInstance` khớp; ghi nhận process ngoài phiên, không tự dừng chúng. |
| Cô lập | 40–41 | Đúng thư mục riêng theo session, clone GitHub, `core.abbrev 7`, không đụng kho làm việc chủ kho. |
| Môi trường | 42–43 | Đủ ba biến UTF-8/bytecode, gọi `python`, dùng `git -C` khi đường dẫn có dấu. |
| Tiến độ | 44 | Đúng ngưỡng quá 5 phút và hai cách in tiến độ. |
| Đo lường | 45–46 | Đúng `do-luong.csv`, một dòng mỗi lượt, đủ 13 cột đúng thứ tự. |
| Bằng chứng | 47 | Đủ SHA, lệnh, N/N, nhãn “local”. |
| Xem xét lại | 48–49 | Đúng 10 packet có dùng local HOẶC 30 ngày, chủ kho xét bằng CSV. |

- **D1–D6, ADR:19–24 so với đặc tả:22–27:** đủ sáu hàng, SHA, PID, thời điểm, thời lượng, mã lỗi, số ca và sự kiện/bài học khớp. Script bổ sung đối chiếu token số của từng ô số đo; phần chữ và ý nghĩa đã đọc riêng. “Selftest của `tl.py`” diễn đạt lại `tl selftest`, không đổi số đo. ADR:26–27 tự giới hạn kết luận vào một ngày/một máy.
- **§20, protocol:1537:** đúng một hàng ADR-0057 trong bảng A, trạng thái Accepted, cột cổng đúng nguyên văn `không cổng — kỷ luật executor`. Chỉ có một câu thêm tại worker gate §10.2.4, dòng 1015, trước phần định nghĩa trạng thái; câu ấy chỉ trỏ tới ADR, không chép điều kiện/ngưỡng/doctrine.
- **Lời khai không cổng, ADR:59–65:** có mục tường minh, nêu khoá không nguyên tử và tooling nằm ngoài packet. Quét sáu tệp cổng của protocol §20 và quét rộng các tệp Python/workflow/shell ngoài `ops/reviews/` không thấy `KHOA.txt`, `do-luong.csv`, `list_devices`, “không đo local”. Đọc `.claude/dev/packet_loop.py:1916` xác nhận `adr-song` kiểm đăng ký, trạng thái và cấu trúc Markdown, không phân xử nghĩa vụ Windows local. “Không đọc nội dung” ở ADR:62 được đọc trong ngữ cảnh này là không đánh giá doctrine, không phải không mở bytes tệp. `doctrine-scan` tại dòng 1625 dùng protocol làm nguồn so với adapter, không chứng minh câu mới trong protocol đúng nghĩa.
- **Tham chiếu:** đường dẫn đặc tả, protocol và các bộ test được nhắc tồn tại. Hai SHA rút gọn giải ra commit thật: `1cc847defbe646c68f4126144dbc80e02eafd61b`, `e9967f07b95c6458afc63dabf4a5c0494e90eca7`. Baseline là merge PR #1020. Merge PR #1010 (`d8d5571e7c1669360eba672f2547d14081039b9b`) có đúng bản vá r929 mở quyền ghi trước khi xoá Git object; diff parent thứ nhất và comment tại `.claude/dev/packet_loop_test.py:8470` hỗ trợ lời khai WinError 5. `t192_S8` và c91/c93/c96 có trong `ops/lease_publish_test.py:10767` và `ops/bien_nhan_v2_test.py:3093`, `3282`, `3408`. Tên `t27` có nhiều consumer nên chỉ xác nhận tên tồn tại; không dùng nó làm bằng chứng đã tái hiện lỗi Windows của #1006.
- **“Những gì KHÔNG đổi”, ADR:51–57:** đối chiếu protocol §8, §5, §10.2.2–§10.2.4 và §11: không mâu thuẫn review class, write set, provenance/required CI hay credential boundary. Local xanh không bị nâng thành check run/receipt Windows CI, không có quyền merge/land mới, không có lệnh dừng process phiên khác. Mọi đường dẫn thay đổi đều thuộc lease; không sửa CI/check bắt buộc, thêm công cụ khoá hay sổ đo.

**Giới hạn bằng chứng:** không có CSV/log Windows gốc trong bundle, nên D1–D6 được kiểm về việc chép đúng đặc tả, không tái đo Windows hay xác minh nhân quả. Nội dung comment cấp quyền `6493571372`, trạng thái PR #1014 và lịch sử packet #1006/#1017/mission #748 không có readback GitHub độc lập ở lượt này; các neo đó được dẫn từ spec/lease, không khai thành sự kiện API đã xác minh. `origin` là mirror cục bộ `/home/user/tra-luat`; không đọc repo nguồn ngoài sandbox và không khai đã kiểm remote GitHub hiện hành. Không thấy bằng chứng đối nghịch để lập finding về các neo này.

Checkout được xử lý read-only. Snapshot trước/sau băm nội dung 8058 tệp, gồm tracked và mọi untracked/ignored được liệt kê, đồng thời kiểm HEAD/tree, index, diff và status: hoàn toàn khớp, không có untracked/ignored. Sandbox thực tế là `workspace-write`, không phải filesystem chặn ghi checkout; hai snapshot chỉ chứng minh không có delta tại hai mốc quan sát, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên.

## Đã chạy

- `git -C cay-kho rev-parse HEAD` — rc 0; `f4d15edcb5d0a9742182273e5950f76165060667`.
- `sha256sum cay-kho/ops/specs/WINDOWS-LOCAL-MAY-CHU-KHO-r1.md` — rc 0; `377ecea689043fcab4d007d65d9592bd28819fa37983796e0c1b75b2c154e715`.
- `git show 96667715996d41bc45e70a64fbaa8996de20f6a0:ops/specs/WINDOWS-LOCAL-MAY-CHU-KHO-r1.md | sha256sum` (cwd `cay-kho/`) — rc 0; cùng hash; script audit cũng kiểm rc Git trực tiếp trước khi băm.
- `git -C cay-kho status --short` — rc 0; stdout rỗng.
- Trong `cay-kho/`, với bytecode tắt và cache/output ngoài checkout:
  - `python3 .claude/dev/packet_loop.py adr-song --root .` — rc 0; `adr-song: sạch — 56 ADR trên đĩa, 56 dòng trong §20, khớp 1–1 (tha thiếu trạng thái: ['0016'])`.
  - `python3 .claude/dev/packet_loop.py doctrine-scan --root .` — rc 0; `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`.
  - `python3 scripts/tl.py doc-claims-check --json` — rc 0; `"ok": true`, `"files_scanned": 116`, `"flags": []`, `"advisory_count": 381`, `"layers_skipped": {}`.
- `git diff --numstat 96667715996d41bc45e70a64fbaa8996de20f6a0 HEAD` (cwd `cay-kho/`) — rc 0; `2 0 docs/PROTOCOL_DA_PHIEN.md`, `73 0 docs/adr/0057-windows-local-may-chu-kho.md`: 2 tệp, 75 dòng thêm, 0 dòng xoá; dưới trần 2 tệp / 140 dòng thêm.
- `git diff --check 96667715996d41bc45e70a64fbaa8996de20f6a0 HEAD` (cwd `cay-kho/`) — rc 0; stdout rỗng.
- `PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0 python3 review_checks.py audit` — rc 0; `files=2`, `added_lines=75`, `deleted_lines=0`, `write_set_match=true`, `write_set_hash_match=true`, `section20_row_count=1`, `pointer_line=1015`, `decision_count=10`, `D1_D6_numeric_cells_equal=true`, cả hai diff cung cấp khớp diff Git.
- `PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0 python3 reference_audit.py` — rc 0; 13 command/rc/stdout/stderr lưu tại `evidence/reference-audit.json`; hai commit tham chiếu giải đúng; quét sáu cổng và mã rộng đều `rg` rc 1, stdout rỗng (nghĩa là không có match, không phải lỗi lệnh).
- Lệnh quét sáu cổng là `rg -n 'KHOA\.txt|do-luong\.csv|list_devices|không đo local|0057|WINDOWS-LOCAL-MAY-CHU-KHO' ops/lease_publish.py .claude/dev/packet_loop.py .claude/dev/launcher.py .claude/dev/gate_lifecycle.py .github/workflows/ci.yml .github/workflows/ops-publish-lease.yml` — rc 1; stdout/stderr rỗng. Cú pháp đầy đủ của quét rộng nằm trong script và JSON evidence.
- `git rev-parse --is-shallow-repository`, `git config --get core.abbrev` (cwd `cay-kho/`) — từng rc 0; lần lượt `false`, `7`.
- `python3 --version`, `git --version`, `uname -sr` — từng rc 0; `Python 3.13.17`, `git version 2.43.0`, `Linux 6.18.44-fc-v185`.
- `PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0 python3 review_checks.py snapshot before` — rc 0; HEAD đúng, tree `dbef3516db6055cd1d5b5d88736a6c9b69dbfe10`, đã băm nội dung 8058 tệp, worktree sạch, 0 untracked, 0 ignored.
- `PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0 python3 review_checks.py snapshot final` — rc 0; cùng HEAD/tree, 8058 tệp, `snapshot_unchanged=true`, sạch tracked/untracked/ignored.
- `PYTHONDONTWRITEBYTECODE=1 python3` heredoc kiểm lại ba cặp log với metadata đã lưu — rc 0; `{"gate_logs_verified": 3, "rc_zero": 3, "stdout_stderr_hashes_match": true}`.

Ba gate đều **passed** theo lệnh/rc và bằng chứng dương của lượt này. Full selftest, Ruff, Windows local và CI **not_run**: không thuộc ba phép nghiệm thu của packet tài liệu này; không khai chúng là passed. Raw log, environment overrides, stdout/stderr hash, diff, audit và snapshot nằm trong `evidence/`; script tái lập nằm ở thư mục sandbox, ngoài `cay-kho/`.
