# wp725 — Hướng dẫn NLM cũ: tài liệu và chuỗi trợ giúp (kế nhiệm WP710, slice A, #725) — Spec r2

> Nguồn quyết định: chủ kho đồng ý MỌI khuyến nghị Q1–Q10 của bản nháp
> `ops/specs/wp710-ke-nhiem-nhap.md` (commit `24254793c369f836297e9776fa3b6e721a25eefb`, PR #724), phiên
> https://claude.ai/code/session_01EENkYtuRtrNS79zt6PTN7h, 2026-10-09. Spec này là slice A (#725) của Q1.
> Đặc tả này KHÔNG cấp việc: cần Issue `wp725`, lease còn hiệu lực và comment cấp quyền của chủ kho.

## Định danh và thẩm quyền

- `packet_id`: `wp725` · `packet_issue`: 725 · `mission_issue`: 725 · `revision`: 2 · `generation` đề xuất: 1.
- `nguon_cap_viec`: packet khắc phục; cha WP710 (#710, Spec r4 sha256
  `a51164cf4bb0b3f41d4c01ef56a522c339caac008f2d855b3819a3ebb642bc0b`, land `8b59185975a938504de5963d2310e574dd4858b2`).
  Finding gốc: lớp `huong-dan-cu-con-lech-sau-va-ngoai-write-set` [P3], `ops/reviews/wp710-g5-luot-9/VERDICT.md`
  dòng 20 và mục "FINDING THEO LỚP", trong commit `2e53b19a9c86a06f8f67247f9d68d8933d780de0` (định danh là BĂM; tìm
  ở `master` trước, chưa thấy thì fetch nhánh `ops/wp710-g5-hien-vat-review`).
- Base đo: `origin/master` `353da6b30f7e2f54a7bed92db97c0fe9ea70a21d`, tree `786902b6da7740c47654cc781faa244312736498`
  (đo 2026-10-09T16:58Z). Đo lại base trước khi cấp lease.
- `executor`: `claude` · `environment`: `cloud` (Linux) · reviewer: `codex` (khác provider, `cross_approved`); dự
  phòng human audit.
- `risk`: normal · `review_class`: **systemic** — chạm 3 tệp nằm trong `RELEASE_MANIFEST.json` và một golden; không
  đổi hành vi thực thi nào (chỉ chuỗi help và văn bản).
- Change-impact policy `.github/coordination/change-impact.v1.json` VẮNG (đo 16:52Z) ⇒ không có closure máy tính;
  chủ kho cấp **ngoại lệ thủ công có giới hạn** cho đúng sáu đường dẫn dưới đây (cùng hình thức nợ #473 của WP710).
- Land: PR vào `master` (tiền lệ WP710, `target_branch_neu_land: master`); KHÔNG có integration branch.

## write_set (exact, không prefix, không glob)

| đường dẫn | thay đổi được phép |
|---|---|
| `scripts/tl_core/cli.py` | CHỈ chuỗi `help=` của parser `nlm-auth-stage` (dòng ~145) và hai cờ `--refresh` (~147), `--force` (~150). Không đổi tên lệnh/cờ, không đổi `set_defaults`, không đổi parser nào khác. |
| `references/golden/parser_surface.json` | CHỈ giá trị băm của khoá `nlm-auth-stage`, sinh bằng `TL_WRITE_PARSER_SURFACE=1 python scripts/tl.py --selftest`; mọi dòng khác giữ nguyên byte. |
| `references/COWORK_PROJECT.md` | "Bước 3 — Đồng bộ cookie nlm": thay hướng dẫn cũ bằng con trỏ tới quy trình WP710; bỏ khối Task Scheduler. |
| `references/RUNBOOK.md` | CHỈ câu ở dòng ~195 lấy "`nlm login --check` xanh" làm tín hiệu thành công. Mục "WP710 — làm tươi credential NLM" KHÔNG đổi. |
| `changelog.d/wp-725.md` | mảnh changelog, không bump version. |
| `scripts/test_fragments/wp725_huong_dan_nlm.py` | ca khoá (protocol §5: test mới vào fragment, KHÔNG vào `tl_selftest.py`). |

Sáu tệp = trần packet thường của ADR-0044. Land-only, NGOÀI write set Executor: `RELEASE_MANIFEST.json`, `VERSION`,
mọi golden khác.

## ngoai_pham_vi

- `docs/WORKFLOW_RASOAT_TU_DONG.md` — Q2: tài liệu lưu trữ (dòng 3 "⛔ TÀI LIỆU LƯU TRỮ … KHÔNG PHẢI CHỈ DẪN VẬN
  HÀNH", thuộc `_DOC_CLAIMS_HISTORICAL` tại `scripts/tl_core/workflow.py:841`); dòng 274 đã nói "KHÔNG tin
  `nlm login --check`". Verdict lượt 3–9 nêu tệp này; spec này đóng phần ấy bằng lý do, không bằng sửa.
- `scripts/tl.py:122–123` (chú thích thứ tự cũ) — nợ có tên `tl-py-chu-thich-thu-tu-stage-cu`; `tl.py` là tệp nóng.
- Ba script shell → slice B1 (#726); `scripts/tl_gws.py` → slice B2 (#727). Đồng hồ WSL (Q8) → không làm.
- Mọi hit lưu trữ/đã nhất quán của bảng phân loại trong bản nháp (≈60 dòng dùng `nlm login` làm bước PHỤC HỒI hoặc
  cài đặt lần đầu — RUNBOOK cho phép).
- LIVE, credential thật, Drive, deploy, merge/land.

## muc_tieu (mỗi dòng chiếu MỘT đường dẫn — L2)

1. `scripts/tl_core/cli.py` — help `nlm-auth-stage`: bỏ "[CODE, sau `nlm login`]", nói lệnh chỉ upload sau canary
   LIVE dương. Help `--refresh`: trung tính, không mô tả cơ chế (để không phụ thuộc slice B2 (#727)) — "làm tươi
   best-effort trước khi gói; KHÔNG thay cổng canary". Help `--force`: bỏ câu "bỏ qua cổng verify-LIVE — ép stage
   DÙ cookie đang chết"; nói đúng: `--force` KHÔNG qua được cổng canary (RUNBOOK:176, lớp WP710 đã land).
2. `references/golden/parser_surface.json` — một dòng băm `nlm-auth-stage` mới.
3. `references/COWORK_PROJECT.md` — dòng ~83 bỏ "tự `nlm login --check` refresh"; dòng ~84–88 bỏ hướng dẫn
   `schtasks /Create … TL_MASTER_KEY=…` (Q7: trái giới hạn "không Scheduled Task" của WP710, và đặt master key
   vào dòng lệnh task); thay bằng con trỏ tới RUNBOOK mục "WP710 — làm tươi credential NLM" và lệnh wrapper
   (`-EnableKeepalive` có giới hạn). Dòng ~94: khi profile chết — đăng nhập lại trên máy gốc rồi chạy wrapper
   (refresh → canary → stage), không "`nlm login` → `secrets-set --nlm`" trần. Giữ con trỏ RUNBOOK→COWORK_PROJECT
   mà ca r228 cần (`tl_selftest.py:26401`).
4. `references/RUNBOOK.md` — dòng ~195: thay "`nlm login --check` xanh" bằng phép kiểm canary dương.
5. `changelog.d/wp-725.md` — mô tả ngắn, có câu nêu rõ phần nào cố ý không làm.
6. `scripts/test_fragments/wp725_huong_dan_nlm.py` — các ca của N1–N2.

## nghiem_thu (mỗi tiêu chí nêu phép đo làm nó ĐỎ — L3)

- **N1.** Trong `COWORK_PROJECT.md`, `RUNBOOK.md` và các chuỗi help của ba parser/cờ trên, mọi dòng chứa
  `login --check` phải thuộc một **danh sách CHO PHÉP** ghi cứng trong fragment (câu phủ định có chủ đích, mỗi mục
  neo bằng chuỗi con duy nhất). ĐỎ: thêm lại một dòng khẳng định chứa `nlm login --check` vào một trong các tệp ấy
  ⇒ ca đỏ; đột biến nới danh sách cho phép để chứa dòng ấy ⇒ ca xanh lại (chứng minh ca đo danh sách).
- **N2.** Fragment dựng parser thật (`build_parser()` hoặc đường tương đương của `tl`) và đòi help `--force` không
  chứa "bỏ qua cổng" / "DÙ cookie đang chết", và chứa khẳng định cổng canary vẫn áp. ĐỎ: đột biến trả help cũ.
- **N3.** `r77a_parser_surface_matches_snapshot` xanh; `git diff <base> -- references/golden/` = đúng 1 dòng
  thêm + 1 dòng xoá, cùng khoá `nlm-auth-stage`. ĐỎ: sửa help mà không sinh lại golden ⇒ r77a đỏ (ca có sẵn).
- **N4.** Ca r228 (`tl_selftest.py:26401`) vẫn xanh. ĐỎ: xoá con trỏ RUNBOOK→COWORK_PROJECT ⇒ r228 đỏ (có sẵn).
- **N5.** `cli.py`: `git diff <base> -- scripts/tl_core/cli.py` chỉ chạm ba chuỗi `help=` (đếm hunk bằng máy trong
  handoff). ĐỎ: bất kỳ thay đổi nào ngoài ba chuỗi ấy.
- **N6 — nghĩa vụ LAND.** Ba tệp `scripts/tl_core/cli.py`, `references/COWORK_PROJECT.md`, `references/RUNBOOK.md`
  và `references/golden/parser_surface.json` có trong `RELEASE_MANIFEST.json` (đo 16:58Z: manifest 183 tệp). Sửa
  NỘI DUNG làm sha lệch dù `file_count` không đổi; lane PR (manifest tạm) KHÔNG bắt được, lane LAND trên `master`
  mới bắt. Hồ sơ land phải: tái sinh `RELEASE_MANIFEST.json` (`python scripts/tl.py release-manifest --out
  RELEASE_MANIFEST.json --json`) và chạy TẠI CHỖ `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict
  --json` ⇒ `ok=true`, `expected == checked`, TRƯỚC khi merge. ĐỎ: bỏ tái sinh ⇒ `ok=false`.
- **N7.** Gate theo CLAUDE.md: ruff F delta = 0 so master; `python scripts/tl.py --selftest` N/N (hai số bằng nhau);
  worker gate xanh trên exact head. Đo lại "nền" trên `origin/master` nếu đỏ.

## hinh_dang_ke_thua (L4)

- Lớp `huong-dan-cu-con-lech-sau-va-ngoai-write-set`: nêu ở các lượt 3→9 của WP710 (7 lượt theo chỉ thị chủ kho;
  lượt 4–9 đối chiếu được trong hồ sơ g5), CHƯA VÁ vì ngoài write set — lặp không do vá hờ.
- Hình dạng phải chép sang: **phạm vi lời khai của reviewer hẹp hơn lỗi thật** (verdict nêu 4 tệp; quét toàn kho ra
  thêm 4 tệp lệch, 1 tệp nêu mà không lệch). Executor TỰ quét lại
  `rg -n 'nlm login|login --check|nlm-auth-stage'` trên head của mình và khai trong handoff mọi hit thuộc sáu tệp,
  không vá theo danh sách của spec.
- Bộ đếm hình dạng của packet này bắt đầu ở 0; lặp cùng hình dạng ≥3 lần ⇒ dừng và hỏi.

## chua_do_duoc

- Hành vi Cowork thật sau khi đổi văn bản — không áp dụng (chỉ tài liệu).
- Số dòng `~145/147/150`, `~83–94`, `~195` đo 16:55Z; Executor đo lại trên base được lease.

## Đính chính r2 sau review PR #724

- Review P2 [4242170329](https://github.com/ducthangho/tra-luat/pull/724#discussion_r4242170329) chỉ ra route trực tiếp vào `master` không đúng route mặc định ở Protocol §5. Dòng "Land: PR vào master" phía trên là ghi nhận **lịch sử r1**, không phải quy tắc cho packet mới.
- Lease do chủ kho đăng cho #725 tại [comment 6091609833](https://github.com/ducthangho/tra-luat/issues/725#issuecomment-6091609833) đã ghi rõ `target_branch_neu_land: master`; PR #729 đã merge. Biên bản này không tuyên bố đã có `mission/725/integration` hoặc draft land PR. Nếu cần coi route lịch sử là ngoại lệ hợp lệ, phải có quyết định chủ kho nêu rõ phạm vi #725–#727 và lý do; không suy từ tiền lệ WP710.
- Packet kế nhiệm dùng route `mission/<issue>/integration` → draft land PR → canonical theo Protocol §5, trừ khi có ngoại lệ mới được ghi bền trước khi cấp lease. Các nghĩa vụ manifest/gate áp vào transition thực tế, gắn exact SHA.

Spec r2 là hồ sơ đính chính cho công việc đã merge, không cấp lại quyền Executor hay làm stale review sản phẩm trên r1. Không sửa lịch sử. Hash/spec/lease mới chỉ dùng nếu phát sinh công việc mới.
