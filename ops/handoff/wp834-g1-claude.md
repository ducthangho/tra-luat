# Handoff wp834 g1 — executor `claude` (phiên cloud), 26-10-2026

- Packet #834 `MAY-ADR-0054-a2` r1 g1 · lease `ops/leases/wp834-r1-g1-claude.yaml` @ `02235f9` (nhánh `ops/wp834-r1-g1-lease`).
- Đặc tả `ops/specs/wp834.md` sha256 `c57ef4d86592218729b811efede7909803d75b6d18ca0d0c3e5059848b44a9d2` và phần chung
  `ops/specs/may-adr-0054-chung.md` sha256 `4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0` — băm lại trên master: khớp.
- **TRẠNG THÁI (cập nhật): APPROVE lượt 7, đã đẩy, PR #950** — xem mục CẬP NHẬT ngay dưới. Lịch sử dừng same-failure giữ nguyên bên dưới. Nhánh code
  `agent/wp834-g1-claude` **CHƯA ĐẨY** (chưa có approve; `push_policy` chỉ cho một lần đẩy sau approve). Chưa có PR.
- Packet này **KHÔNG kích hoạt ADR-0054** và không chạm `_che_do_0054`.
- Không merge/land/deploy. Không force-push, rebase, xoá ref.

## CẬP NHẬT 26-10-2026 ~07:00Z — APPROVE, đã đẩy một lần, PR #950

- Chủ kho chọn (a) (#834 issuecomment-6408783497): `same_failure_limit` của `required-mutation-coverage-missing` 2 → 3, chỉ lease
  này; lượt 7 có luật phân hạng (đột biến độ phủ MỚI do reviewer tự dựng mà sản phẩm từ chối đúng ⇒ P3).
- `742ba39`: ba ca + ba đột biến cho mutant sống lượt 6 (`ignore_job_run_id`, `ignore_invalid_ref_entries`,
  `ignore_p3_value_types`), ghép vào dòng sẵn có ⇒ diff giữ **447/450**. `8ac10ce`: merge `origin/master` `356eb26`
  (55 commit, không chạm write set) TRƯỚC lượt 7 để head được duyệt = head đẩy.
- **Codex lượt 7 (7/8)** — run `945ef0f9`, `8ac10ce`, prompt sha256 `1982e8d4…`, 732 s rc0, `model_phuc_vu: gpt-6-astra`:
  **approve — 0 P0 · 0 P1 · 0 P2 · 1 P3**. Hiện vật `ops/reviews/wp834-g1-codex-luot7/`, VERDICT sha256 `37f009b8…`.
  Nợ P3 có tên `required-mutation-coverage-missing`: thiếu ca bảo vệ neo head của finding issue comment (`if n is None and hang`)
  và kiểu id trang (`type(x.get("id")) is int`); sản phẩm từ chối đúng ở A/B. Owner gợi ý: executor #834, chủ kho theo dõi.
- Suite đầy đủ trên `8ac10ce` (clone ghim): `nền: 938/938 đạt · BỎ QUA: 1` · ca 939 · đột biến 1306 · `TỔNG: ĐẠT` · rc0 · 51m31s.
  63/63 ca `r834_*`; 59/59 đột biến `r834_*` + `r812_bo_generation` giết đúng ca. `ci_dang_ky_test.py` `1070/1070 · TỔNG: ĐẠT`.
- **Đẩy MỘT lần** `agent/wp834-g1-claude` = `8ac10ce47d2587c91637d74d299e3c781025be1e` (ls-remote xác nhận). **PR draft #950.**
  Master sau đó tiến tới `9372ecd` (chỉ `ops/land`, merge sạch) — không merge thêm (hết lượt Codex để xác minh lại).
- Việc còn lại: CI PR #950 xanh trên head cuối (executor theo dõi); merge/land: chủ kho.

## Nhánh code cục bộ (rẽ từ `ab344da`), head `394d24787aaa5b4e4638b0820b42fe25b6f0432c`

| commit | nội dung |
|---|---|
| `17a3714` | M1–M5: lệnh `accept`; I7 CI (app, workflow, job; attempt mới nhất của run mới nhất; job ↔ check-run cùng kho/app/suite; luật `kiem-gate`); I7 connector (một kho + PR + head; đủ trang theo id từng endpoint; id trùng mâu thuẫn bị từ chối; PENDING không là xong; finding ở ba endpoint, hạng miền đóng); I11 slug P3 connector từ `bang_lop[].connector_refs` của biên nhận H; protocol §4 |
| `0b8d48c` | vá 7 lớp Codex lượt 1 + 2 lớp suite nền (mã mới trùng mốc đột biến cũ `kg_*`; ma trận codepage chưa phủ `accept`) |
| `19743fa` | vá 3 lớp lượt 2 + định dạng THẬT của connector `**Reviewed commit:** \`sha10\`` (bản trước từ chối nhầm; mẫu ở `ops/land/pr889-claude-md-bai-hoc-c-provenance/readback-comments-889-sau-review-lai.json`) |
| `7436fe3` | sửa thứ tự cặp thay thế của đột biến `r834_xet_dung_truoc_dau_vao` (bản cũ tự xoá dòng vừa chèn ⇒ SỐNG giả) |
| `dcb77e7` | vá 3 lớp P2 lượt 3: state dự kiến mã hoá được TRƯỚC `_xet_dung`; `_r834_ca` phân loại CLI sập là tín dụng giả (`CliSapDo`); ca/đột biến dừng trước H/P3, job chưa xanh, P1 ở review comment |
| `19a862b` | độ phủ lượt 4: check lease ngoài hằng, id riêng từng endpoint, review hoàn tất đơn độc (chỉ test) |
| `394d247` | lượt 5: P1 jobs có attempt mới hơn `run_attempt` của readback run ⇒ không đạt; ca/đột biến `connector_refs` lặp, quyết định P3 thiếu trường |

Write set: diff `ab344da..394d247` đúng 3 tệp — `packet_loop.py` +181/−1 · `packet_loop_test.py` +262/−3 · `PROTOCOL_DA_PHIEN.md` +4/−1
⇒ **447/450** dòng thêm (ADR-0053).

## Nghiệm thu đo trên `394d247` (clone thường, `.git` là thư mục, `core.abbrev 7`, không nông)
- 60 ca `r834_*`: **60/60**. Phủ đủ 18 mục bắt buộc của `nghiem_thu` (bảng đối chiếu từng mục ở verdict lượt 2–6).
- Đột biến `r834_*` + `r812_bo_generation` (nay cũng nhắm `r834_bnc_lech_generation`): **56/56 GIẾT đúng ca**, 0 sống, 0 tín dụng giả
  (đọc tên ca + lớp ngoại lệ + thông điệp; ca đích nhận rc=0/accepted, rc=3 của cọc `_xet_dung`, hoặc state đổi byte).
- `moc_dot_bien_phai_khop_DUNG_MOT_CHO`, `stdout_cp1252`, `stdout_cp1258` xanh. `doctrine-scan` rc0 · `adr-song` rc0 (55/55) ·
  `git diff --check` rc0 · ruff `--select F`: 3 (2 F541 + 1 F841) = nền 3 ⇒ delta 0.
- Suite đầy đủ `python .claude/dev/packet_loop_test.py`: **935/935 · BỎ QUA 1 · 1303 đột biến · TỔNG: ĐẠT** (mục cuối tệp).

## Cross-review Codex — 6/8 lời gọi (ADR-0052), mỗi lượt qua `.claude/dev/launcher.py run`
`codex exec -m gpt-6-astra -c model_reasoning_effort=xhigh -s workspace-write`, sandbox = clone detached tại head + `tham-chieu/`
(lease chép, verdict thiết kế #812 g2, verdict các lượt trước), không mạng. `run.json` mỗi lượt ghi `model_phuc_vu: gpt-6-astra`.
Hiện vật: `ops/reviews/wp834-g1-codex-luotN/{PROMPT.md,VERDICT.md,run.json}`.

| lượt | run_id (short) | head | prompt sha256 | thời lượng | verdict | VERDICT sha256 |
|---|---|---|---|---|---|---|
| 1 | `feb68265` | `17a3714` | `a59ecbbe…` | 802 s rc0 | request_changes 0/4/3 (P0/P1/P2) | `cc562118…` |
| 2 | `3a03124d` | `0b8d48c` | `bf357eb4…` | 1300 s rc0 | request_changes 0/1/2 — 5/7 lớp lượt 1 đóng | `cb53cee1…` |
| 3 | `bb760ea9` | `7436fe3` | `f2c30924…` | 802 s rc0 | request_changes 0/0/3 | `d452fd8b…` |
| 4 | `89a9c925` | `dcb77e7` | `0fb359b7…` | 879 s rc0 | request_changes 0/0/1 | `7b44edac…` |
| 5 | `2f03ac52` | `19a862b` | `e6149b15…` | 846 s rc0 | request_changes 0/1/1 | `98237983…` |
| 6 | `f77b274e` | `394d247` | `3a2a7dc7…` | 698 s rc0 | request_changes 0/0/1 | `61c33076…` |

Lý do mỗi lượt sau lượt 1: lượt trước `request_changes` và đã vá. Lớp sản phẩm đã đóng theo Codex: `ci-attempt-provenance-missing`
(cả biểu hiện tái lộ lượt 5), `conflicting-evidence-overwrite`, `connector-verdict-incomplete`, `connector-head-binding-incomplete`,
`workflow-jobs-pagination-cross-run`, `accept-state-schema-incomplete`, `ci-job-input-schema-incomplete`, `stop-validation-order`,
`connector-parser-mutant-false-credit`. Phần connector của lớp thiết kế #812 `findings-not-receipt-bound`: đóng (lượt 1).

## VÌ SAO DỪNG — điều kiện same-failure

Lớp **`required-mutation-coverage-missing` (P2)** có mặt ở **cả sáu** lượt. Mỗi lượt executor thêm ca giết đúng các đột biến sống
reviewer nêu, và mỗi lượt reviewer tự dựng 3 đột biến mới (gỡ một chốt khác) vẫn sống trọn bộ ca `r834_*`. Theo chính Codex,
đây là **thiếu nghiệm thu, không phải lỗi hành vi**: ở mọi probe A/B, mã sản phẩm từ chối đúng; chỉ suite chưa có ca bảo vệ chốt.

Protocol đặt `same_failure_limit: 2` (`docs/PROTOCOL_DA_PHIEN.md` mục schema, `MAC_DINH_TRAN_SAME_FAILURE = 2`). **Executor đã
không đối chiếu trần này từ lượt 2 — lẽ ra phải dừng lúc ấy.** Đây là lỗi kỷ luật của phiên executor, ghi thẳng ở đây.

Lượt 6 còn mở đúng ba đột biến (verdict lượt 6, mục F2):
1. `ignore_job_run_id` — job đổi `run_id` 100→90, giữ attempt/head/name/URL ⇒ sản phẩm 12/VẮNG, mutant bỏ cặp `run_id` khỏi phép nối ⇒ accepted.
2. `ignore_invalid_ref_entries` — thêm `['invalid_endpoint', 11]` cạnh ref đúng ⇒ sản phẩm 11, mutant gỡ `len(refs) != sum(...)` ⇒ accepted.
3. `ignore_p3_value_types` — `owner` = 123 ⇒ sản phẩm 2, mutant gỡ kiểm giá trị chuỗi không trắng ⇒ accepted.

Ba ca vá đã được reviewer chạy (CONFIRM) và giết đúng; thêm vào cần ~3–4 dòng ⇒ chạm/vượt trần 450 nếu không gộp dòng test hiện có.

## Quyết định cần chủ kho (chọn một)
- **(a) Nâng trần same-failure cho lớp này thêm 1 + dùng lời gọi Codex 7/8**: executor thêm 3 ca/đột biến trên (gộp dòng test để
  giữ ≤ 450), chạy lại suite đầy đủ, gọi Codex lượt 7 kèm chỉ thị phân hạng đột biến độ phủ mới tự dựng (sản phẩm đã từ chối đúng).
  Đề xuất của executor: (a) — mọi lớp hành vi đã đóng; phần còn lại là độ phủ, mà vòng "reviewer tự dựng đột biến mới" không tự hội tụ.
- **(b) Chấp nhận F2 làm nợ có tên** (owner, hướng xử lý) và cho phép đẩy head hiện tại — cần chủ kho xác định vì Codex chưa approve.
- **(c) Revision/tách stable slice** theo protocol §12.

## Lỗi/quan sát khác (ghi, KHÔNG vá)
- Container mở ra **nông**; phải `fetch --unshallow` trước khi đo (`_che_do_0054` trả False trên kho nông).
- Executor đã hai lần sửa cây làm việc trong lúc suite đầy đủ đang chạy trên chính cây ấy (lượt trên `0b8d48c`, `7436fe3` bị huỷ,
  không dùng số). Từ `dcb77e7` suite chạy trong clone riêng ghim đúng commit.
- Suite nền trên `17a3714` (lượt sạch duy nhất của head ấy): `891/894 · BỎ QUA 1` — ba ca đỏ do bản vá (đã vá ở `0b8d48c`).
- Suite nền `dcb77e7`: `929/929 · BỎ QUA 1`; `19a862b`: `932/932 · BỎ QUA 1` (phần đột biến của hai lượt ấy bị dừng khi head đổi).
- `launcher.py` header `stderr.log` của codex-cli 0.164.0 chỉ có `Reading additional input from stdin...` — model/effort lấy từ
  `run.json` (`model_phuc_vu`), không từ header.
- Nợ P3 của #929 (ca `ls[0] == 0` của `_che_do_0054`) không thuộc đặc tả wp834; chưa làm.

## Suite đầy đủ trên `394d247`
Clone thường ghim đúng `394d247` (`.git` thư mục, `core.abbrev 7`, `autocrlf false`, `eol lf`, không nông), `python .claude/dev/packet_loop_test.py`: `nền: 935/935 đạt · BỎ QUA: 1` (`luong_canonical_chay_that`, chỉ Windows — đột biến `luong_canonical_chay_that_dao_os_name` theo đó không tính là giết) · SỐ LIỆU máy đếm: ca **936**, đột biến **1303**, lớp lách 78, ca bắt-oan 35, ngoại lệ AC 18 = 0 · `TỔNG: ĐẠT` · rc=0 · 49m03s.
