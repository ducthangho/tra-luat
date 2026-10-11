# wp727 — `tl_gws.py`: bước làm tươi `nlm auth refresh` và chuỗi gợi ý theo quy trình WP710 (kế nhiệm WP710, slice B2, #727) — Spec r2

> Nguồn quyết định: chủ kho đồng ý MỌI khuyến nghị Q1–Q10 của bản nháp
> `ops/specs/wp710-ke-nhiem-nhap.md` (commit `24254793c369f836297e9776fa3b6e721a25eefb`, PR #724), 2026-10-09.
> Spec này là slice B2 (#727) của Q1 (Q4). KHÔNG cấp việc: cần Issue `wp727`, lease còn hiệu lực và comment cấp quyền.

## Định danh và thẩm quyền

- `packet_id`: `wp727` · `packet_issue`: 727 · `mission_issue`: 727 · `revision`: 2 · `generation` đề xuất: 1.
- `nguon_cap_viec`: packet khắc phục; cha WP710 (#710, Spec r4 sha256
  `a51164cf4bb0b3f41d4c01ef56a522c339caac008f2d855b3819a3ebb642bc0b`, land `8b59185975a938504de5963d2310e574dd4858b2`);
  lớp `huong-dan-cu-con-lech-sau-va-ngoai-write-set` [P3]. `tl_gws.py` KHÔNG có trong danh sách của verdict; tìm ra
  khi quét toàn kho 16:55Z.
- Base đo: `origin/master` `353da6b30f7e2f54a7bed92db97c0fe9ea70a21d`, tree `786902b6da7740c47654cc781faa244312736498`.
- `executor`: `claude` · `environment`: `cloud` (Linux) · reviewer: `codex` (`cross_approved`); dự phòng human audit.
- `risk`: **sensitive** · `review_class`: **sensitive** · ADR-0044: xếp **chạm authority** vì `tl_gws.py` chứa cổng
  canary quyết định upload credential (`_nlm_files_after_live_canary`, ~857) ⇒ trần **≤3 tệp, ≤300 dòng thêm**.
  Write set = 3 tệp.
- Change-impact policy vắng ⇒ ngoại lệ thủ công có giới hạn cho đúng ba đường dẫn.
- Land: PR vào `master` (tiền lệ WP710).

## write_set (exact)

| đường dẫn | thay đổi được phép |
|---|---|
| `scripts/tl_gws.py` | CHỈ: thân `_refresh_nlm_auth` (~756–766) và docstring của nó; các chuỗi thông báo/gợi ý ở ~839, ~1405, ~1672, ~1695, ~1718, ~1727 (docstring), ~1769, ~1787. KHÔNG đổi `_nlm_auth_alive`, `_nlm_canary_*`, `_nlm_files_after_live_canary`, thứ tự gọi, mã thoát, hay bất kỳ hàm nào khác. |
| `changelog.d/wp-727.md` | mảnh changelog. |
| `scripts/test_fragments/wp727_tl_gws_refresh.py` | ca khoá. |

KHÔNG sửa `scripts/tl_selftest.py` (các ca hiện có ở ~4690–4850 vá `_refresh_nlm_auth` bằng lambda — phải tiếp tục
xanh nguyên trạng). Land-only: `RELEASE_MANIFEST.json`.

## ngoai_pham_vi

- Cổng canary, danh sách cho phép thân canary, payload guard — đã land ở WP710.
- `scripts/tl_core/cli.py` (help `--refresh`, slice A (#725) viết trung tính để không phụ thuộc slice này).
- Hit đã nhất quán hoặc lưu trữ trong `tl_gws.py` (~108–110, 310–359, 712, 739, 803–807, 858–888, 959–1071,
  1116–1349, 1481, 1743–1781 trừ các dòng liệt kê ở write set) — giữ nguyên.

## muc_tieu

1. `_refresh_nlm_auth`: đổi lệnh từ `nlm login --check` sang `nlm auth refresh` (argv `[nlm, "auth", "refresh"]`,
   cùng lệnh wrapper WP710 gọi ở `scripts/nlm-credential-refresh.ps1:1019`), giữ best-effort, giữ timeout có giới
   hạn, không in đầu ra con. Docstring nói rõ: giá trị trả về KHÔNG phải bằng chứng sống; cổng canary chạy sau mới là
   chốt. Ba điểm gọi (~954, ~1021, ~1746) không đổi.
2. Chuỗi gợi ý ~1405 và ~1787: bỏ "Kiểm: nlm login --check"; trỏ phép kiểm canary (`tl nlm-auth-status` hoặc câu tương
   đương đã có trong kho).
3. Chuỗi ~839, ~1672, ~1695, ~1718, docstring ~1727, ~1769: thứ tự phục hồi theo WP710 — đăng nhập lại trên máy gốc
   khi cần → wrapper `nlm-credential-refresh.ps1` (refresh → canary → stage), hoặc nói lệnh stage tự chạy canary;
   ~1769 bỏ gợi ý "`--refresh`" như cách cứu cookie chết.
4. changelog; 5. fragment test.

## nghiem_thu (L3)

- **N1.** Fragment chặn `subprocess.run` trong `tl_gws`, gọi `_refresh_nlm_auth()`, đòi argv kết thúc bằng
  `["auth", "refresh"]`, có `timeout` hữu hạn, và **0** lời gọi chứa `"--check"`. ĐỎ: đột biến trả argv cũ.
- **N2 (không vòng qua cổng).** Với `_refresh_nlm_auth` trả `True` và canary trả `False`/`None`: `nlm-auth-stage`
  (kể cả `--refresh`, `--force`) upload **0** lần, rc 4. ĐỎ: đột biến cho `_nlm_files_after_live_canary` tin giá trị
  của `_refresh_nlm_auth` ⇒ upload 1 ⇒ đỏ. (Ca `tl_selftest.py` ~4643–4680/~4790–4830 đã đo cổng; ca này đo riêng
  đường `--refresh`.)
- **N3 (lỗi refresh không chặn ngược).** `subprocess` ném `TimeoutExpired`/`OSError` ⇒ `_refresh_nlm_auth` trả
  `False`, lệnh stage vẫn đi tới canary (thứ tự nhật ký: refresh → canary). ĐỎ: đột biến để ngoại lệ lan.
- **N4.** Mọi chuỗi thuộc write set chứa `login --check` phải nằm trong danh sách CHO PHÉP ghi cứng (câu phủ định);
  ĐỎ: thêm lại "Kiểm: nlm login --check" ⇒ đỏ; nới danh sách cho phép ⇒ xanh lại.
- **N5.** `git diff <base> -- scripts/tl_gws.py` chỉ chạm các vùng ở write set (đếm hunk bằng máy, liệt kê trong
  handoff). ĐỎ: hunk ngoài vùng.
- **N6 — nghĩa vụ LAND.** `scripts/tl_gws.py` có trong `RELEASE_MANIFEST.json`: hồ sơ land tái sinh manifest và
  chạy TẠI CHỖ `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` ⇒ `ok=true`,
  `expected == checked`, trước merge.
- **N7.** Ruff F delta 0 (nền `tl.py` 12 F821 + 0 F401 theo CLAUDE.md; đo lại); selftest N/N; `golden-test` và
  determinism xanh (chuỗi thông báo có thể xuất hiện trong snapshot — đo, đừng đoán); worker gate xanh.

## hinh_dang_ke_thua (L4)

- Lớp `huong-dan-cu-con-lech-sau-va-ngoai-write-set`: 7 lượt (3→9), chưa vá do ngoài write set.
- Hình dạng: phạm vi lời khai hẹp hơn lỗi thật — `tl_gws.py` không có trong verdict. Executor tự quét lại toàn tệp.

## chua_do_duoc

- `nlm auth refresh` có thật sự làm tươi cookie từ browser profile trong ngữ cảnh lệnh `tl` (không tương tác) hay không
  — chỉ đo được LIVE trên máy gốc; ngoài lease. Thứ được bảo đảm offline: lệnh mới không mở được upload khi canary âm.
- `nlm-auth-status` có đòi thân đúng notebook không — xem slice B1 (#726) mục 2.

## Đính chính r2 sau review PR #724

- Review P2 [4242170329](https://github.com/ducthangho/tra-luat/pull/724#discussion_r4242170329): dòng "Land: PR vào master" phía trên là route lịch sử r1. Lease chủ kho [6091615222](https://github.com/ducthangho/tra-luat/issues/727#issuecomment-6091615222) ghi `target_branch_neu_land: master`; PR #731 đã merge. Điều đó không chứng minh đã có mission integration hay draft land PR.
- Đối với packet mới, dùng `mission/<issue>/integration` rồi draft land PR theo Protocol §5. Bất kỳ ngoại lệ direct-to-master phải được chủ kho quyết định bền cho đúng packet/head trước transition. Manifest, gate và approval gắn exact SHA của transition thực tế.
- Đây là đính chính hồ sơ, không cấp lại lease của wp727 và không tự tuyên bố finding đã đóng. Review P2 chỉ được adjudicate sau khi quyết định ngoại lệ lịch sử được ghi và reviewer đọc nó.
