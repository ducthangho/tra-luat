# wp726 — Ba script shell NLM: phán sống/chết bằng canary, không nuốt mã thoát (kế nhiệm WP710, slice B1, #726) — Spec r2

> Nguồn quyết định: chủ kho đồng ý MỌI khuyến nghị Q1–Q10 của bản nháp
> `ops/specs/wp710-ke-nhiem-nhap.md` (commit `24254793c369f836297e9776fa3b6e721a25eefb`, PR #724), 2026-10-09.
> Spec này là slice B1 (#726) của Q1 (Q3 cho `nlm-auto-refresh.sh`). KHÔNG cấp việc: cần Issue `wp726`, lease còn hiệu lực
> và comment cấp quyền của chủ kho.

## Định danh và thẩm quyền

- `packet_id`: `wp726` · `packet_issue`: 726 · `mission_issue`: 726 · `revision`: 2 · `generation` đề xuất: 1.
- `nguon_cap_viec`: packet khắc phục; cha WP710 (#710, Spec r4 sha256
  `a51164cf4bb0b3f41d4c01ef56a522c339caac008f2d855b3819a3ebb642bc0b`, land `8b59185975a938504de5963d2310e574dd4858b2`);
  finding gốc lớp `huong-dan-cu-con-lech-sau-va-ngoai-write-set` [P3] cộng hai tệp lệch mà verdict KHÔNG nêu
  (`env-reimport.sh`, `nlm-auth-import.sh`), tìm ra lúc quét toàn kho 16:55Z.
- Base đo: `origin/master` `353da6b30f7e2f54a7bed92db97c0fe9ea70a21d`, tree `786902b6da7740c47654cc781faa244312736498`.
- `executor`: `claude` · `environment`: `cloud` (Linux, có `bash`) · reviewer: `codex` (`cross_approved`); dự phòng
  human audit.
- `risk`: **sensitive** · `review_class`: **sensitive** — đổi mã thoát và phán quyết sống/chết của
  `nlm-auto-refresh.sh`, script mà Routine bảo trì gọi (CHANGELOG v1.35.87: Routine `trig_01ReWux8`).
- Kích thước (ADR-0044): spec xếp B1 là `sensitive` **KHÔNG chạm authority** — ba script là NGƯỜI GỌI; cổng canary
  quyết định upload nằm ở `scripts/tl_gws.py` (`_nlm_files_after_live_canary`) và KHÔNG đổi trong slice này. Vì vậy
  áp trần packet thường (≤6 tệp, ≤1.000 dòng): 5 tệp. Chủ kho bác cách xếp này thì tách tiếp, không gộp.
- Change-impact policy vắng ⇒ ngoại lệ thủ công có giới hạn cho đúng năm đường dẫn dưới đây.
- Land: PR vào `master` (tiền lệ WP710).

## write_set (exact)

| đường dẫn | thay đổi được phép |
|---|---|
| `scripts/nlm-auto-refresh.sh` | bước 3 "probe LIVE" (dòng ~74–86). |
| `scripts/env-reimport.sh` | khối probe LIVE (dòng ~127–140) và dòng gợi ý phục hồi. |
| `scripts/nlm-auth-import.sh` | bước 4 "PHÁN QUYẾT" (dòng ~193–201) và bước 5 báo lỗi stage (dòng ~204–212). |
| `changelog.d/wp-726.md` | mảnh changelog. |
| `scripts/test_fragments/wp726_script_nlm_canary.py` | ca khoá với `nlm`/`tl` giả. |

Land-only, ngoài write set: `RELEASE_MANIFEST.json`.

## ngoai_pham_vi

- `scripts/tl_gws.py` (slice B2 (#727)), tài liệu/help (slice A), `tl.py`, wrapper PowerShell của WP710.
- Đổi cổng canary hay danh sách cho phép thân canary — đã land ở WP710, không mở lại.
- Đổi lịch hay cấu hình Routine `trig_01ReWux8` — không đụng; chỉ ghi trong handoff mã thoát mới để chủ kho đối chiếu.
- LIVE, Drive, credential thật.

## muc_tieu

1. `scripts/nlm-auto-refresh.sh` (Q3): bỏ `nlm login --check` làm phán quyết. Phán quyết = mã thoát của
   `$PY scripts/tl.py nlm-auth-stage` — lệnh này tự chạy canary LIVE trước khi đọc jar (WP710) và tự lùi về
   `NLM_BASE_NOTEBOOK` khi không có ID ghim (`tl_gws.py:840–855`). Ánh xạ: rc 0 ⇒ SỐNG + bundle đã tươi, thoát 0;
   rc 4 ⇒ canary không dương ⇒ CHẾT, thoát 3 (giữ nghĩa mã 3 "cần re-harvest" ở đầu tệp); rc khác ⇒ hạ tầng/không
   kết luận, thoát 2. Bỏ `>/dev/null 2>&1 || true`; chỉ in mã và dòng tóm tắt, KHÔNG in đầu ra thô có thể chứa cookie
   (giữ nguyên chuẩn mực WP710). Gợi ý phục hồi dòng ~85: đăng nhập lại trên máy gốc rồi chạy wrapper
   `scripts/nlm-credential-refresh.ps1` (refresh → canary → stage), không "`nlm login && nlm-auth-stage`".
2. `scripts/env-reimport.sh`: probe sống/chết bằng canary notebook thật thay `login --check`. Phép dương PHẢI có
   cùng ngữ nghĩa cổng stage của WP710: thân trả về là đúng notebook (`_nlm_auth_alive(nb,
   require_notebook_body=True)`, `scripts/tl_gws.py:309–342`); rc 0 hay số notebook KHÔNG đủ. `tl nlm-auth-status`
   (`scripts/tl_core/nlm_ops.py:1679`, đi qua `_nlm_preflight_report`) CHƯA được đo là có đòi thân đúng notebook —
   Executor đo điều đó trước (đọc mã, file:line trong handoff); không đòi thì gọi `_nlm_auth_alive(...,
   require_notebook_body=True)` trực tiếp qua `$PY` từ script (không thêm lệnh `tl` mới — `tl.py`/`cli.py` ngoài write
   set). `True` ⇒ sống; `False` ⇒ chết; `None` ⇒ không kết luận (mã riêng, không gộp vào sống). Script này KHÔNG stage.
   Sửa gợi ý phục hồi như mục 1.
3. `scripts/nlm-auth-import.sh`: bước 4 phán sống bằng canary (như mục 2); bước 5 tách ba trường hợp theo rc của
   stage: 0 đã tươi · 4 "canary của lệnh stage không dương — KHÔNG upload" · khác "lỗi stage, có thể đã ghi một
   phần — kiểm Drive". Không còn in "cookie ở ĐÂY vẫn dùng được" khi rc 4.
4. `changelog.d/wp-726.md`; 5. fragment test.

## nghiem_thu (L3)

Đồ giả phải **GIỮ TRẠNG THÁI**, không diễn kịch bản (CLAUDE.md, bài học `ops-don-ref`): `nlm` giả và `tl` giả
(hoặc `PY` trỏ một python giả) ghi nhật ký argv mỗi lời gọi; trạng thái "cookie sống/chết" và "canary dương/âm" là
hai biến độc lập.

- **N1 (false-green).** Trạng thái: `nlm login --check` in "valid" nhưng canary ÂM. Cả ba script phải báo CHẾT
  (`nlm-auto-refresh.sh` thoát 3; `nlm-auth-import.sh` bước 4 thoát 4; `env-reimport.sh` đặt `NLM_RC=3`). Nhật ký:
  **0** lời gọi `login --check`. ĐỎ: đột biến khôi phục phán quyết `login --check` trong TỪNG script (ba đột biến
  riêng, mỗi cái làm ca của script ấy đỏ).
- **N2 (dương).** Canary dương ⇒ `nlm-auto-refresh.sh` thoát 0 và stage được gọi đúng 1 lần. ĐỎ: đột biến không
  gọi stage ⇒ đỏ.
- **N3 (không nuốt rc).** Stage trả 5 ⇒ `nlm-auto-refresh.sh` thoát 2, không 0. ĐỎ: đột biến thêm lại `|| true`.
- **N4 (rc 4 ≠ lỗi khác).** `nlm-auth-import.sh` với stage rc 4 in thông điệp "canary … không dương", với rc 5 in
  thông điệp lỗi stage; hai thông điệp khác nhau. ĐỎ: đột biến gộp hai nhánh.
- **N5 (không lộ bí mật).** `nlm`/`tl` giả in một chuỗi canh (`SENTINEL-COOKIE-…`) ra stdout/stderr; đầu ra của script
  không chứa chuỗi ấy. ĐỎ: đột biến bỏ chuyển hướng ⇒ chuỗi lộ.
- **N6 (nền).** Ca chạy bằng `bash` thật. Thiếu `bash` (vd Windows runner) ⇒ ca báo `skipped` có lý do và KHÔNG
  được đếm là đạt; trên Linux thiếu `bash` ⇒ ĐỎ (không được tha). Handoff khai riêng số ca `passed`/`skipped`.
- **N7 — nghĩa vụ LAND.** Ba script có trong `RELEASE_MANIFEST.json`: hồ sơ land tái sinh manifest và chạy TẠI CHỖ
  `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` ⇒ `ok=true`, `expected == checked`,
  trước merge. ĐỎ: bỏ tái sinh ⇒ `ok=false`.
- **N8.** Ruff F delta 0; selftest N/N; worker gate xanh; `shellcheck` nếu có mặt (ghi rõ có/vắng — CLAUDE.md: vắng
  `shellcheck` thì `actionlint` im lặng bỏ luật nền).

## hinh_dang_ke_thua (L4)

- Lớp `huong-dan-cu-con-lech-sau-va-ngoai-write-set`: 7 lượt (3→9) chưa vá do ngoài write set.
- Hình dạng: "VÁ ĐÚNG CHỖ ĐƯỢC CHỈ RỒI BỎ SÓT ĐƯỜNG THỨ BA" — cùng một lỗi (`login --check` làm phán quyết) có BA
  đường vào (ba script). Mỗi đường một đột biến riêng (N1); ba đột biến không phân biệt được bằng đầu vào ⇒ bộ ca
  chỉ đang đo một đường.

## chua_do_duoc

- Routine `trig_01ReWux8` đọc mã thoát thế nào, và nó còn bật không — chưa đo (không đọc cấu hình Routine trong phiên
  soạn spec). Đổi rc 3/2 có thể đổi màu báo cáo của Routine.
- `nlm` CLI và Drive thật — chỉ đồ giả.

## Đính chính r2 sau review PR #724

- Review P2 [4242170323](https://github.com/ducthangho/tra-luat/pull/724#discussion_r4242170323): rc 4 của `nlm-auth-stage` chỉ nói canary **không dương**; nó không phân biệt `False` (chết) với `None` (không kết luận). Dòng ánh xạ rc 4 → chết phía trên là yêu cầu r1 đã lỗi. Quy tắc r2: sau rc 4, probe lại bằng `_nlm_auth_alive(..., require_notebook_body=True)` với đầu ra bị chặn; chỉ `False` cho wrapper rc 3. `None` hoặc `True` mâu thuẫn với stage cho rc 2. Không parse stdout/stderr của probe.
- Review P2 [4242170327](https://github.com/ducthangho/tra-luat/pull/724#discussion_r4242170327): "đúng 1 lần stage" của N2 áp cho **toàn một lần chạy**. Export mới: `nlm-auth-import.sh` stage một lần, wrapper không stage lại khi import thành công; import/stage lỗi thì wrapper dừng rc 2, không retry stage, không xóa plaintext. Không có export: keep-warm stage đúng một lần. Ca stateful phải đo cả hai đường và mutant gọi stage lần hai.
- Mã đã merge ở PR #730 chứa phân nhánh tương ứng tại `scripts/nlm-auto-refresh.sh` blob `03f726fb2d64585fa4c4aa145658f9dd3c6d72a0` trên master `8aebf14af7d3918e4e45fc42569c2c156f9b3ca9`; fragment `wp726_script_nlm_canary.py` blob `19ace16d8e1a1bbec3bd3c676eb0fcdeff183199`. Đây là đối chiếu tĩnh; r2 không tự tạo biên nhận test mới.
- Review P2 [4242170329](https://github.com/ducthangho/tra-luat/pull/724#discussion_r4242170329): route trực tiếp vào master ở r1 là lịch sử, không phải quy tắc mới. Lease chủ kho [6091612697](https://github.com/ducthangho/tra-luat/issues/726#issuecomment-6091612697) ghi `target_branch_neu_land: master`. Muốn coi đó là ngoại lệ hợp lệ cần quyết định bền nêu rõ phạm vi. Packet mới theo Protocol §5 route integration và land PR.

Spec r2 là đính chính lịch sử; không cấp lại quyền r1. Nếu mã thay đổi sau blob trên, cần đánh giá lại và lease mới.
