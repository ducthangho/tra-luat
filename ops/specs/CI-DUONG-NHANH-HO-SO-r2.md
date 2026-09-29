# CI-DUONG-NHANH-HO-SO — đặc tả đóng băng (revision 2)

Thay revision 1 (`ops/specs/CI-DUONG-NHANH-HO-SO.md`, sha256 `e694984148882d5e8d64542577321610ed7b8fe242ba100d154adb0e1ed8c64c`). Lý do revision: phiên thi công đo được đặc tả r1 tự mâu thuẫn (mục "Vì sao r2"); chủ kho chọn hướng A trong phiên Claude Code 2026-09-29. Mọi mục không nêu ở mục "Khác biệt so với r1" giữ nguyên r1.

Nguồn quyết định: chủ kho `ducthangho`, phiên Claude Code 2026-09-29. Hướng "cách 1" (Issue #674, ~02:50Z);
Q1–Q6 chốt "theo khuyến nghị" (~05:30Z, xem comment Issue #674 do phiên ghi hộ). Đặc tả này thay bản nháp
đăng ở Issue #674 (comment 5882832190, 5882874442). Số đo trong tệp này lấy ngày 2026-09-29; đo lại trước
mỗi bước công bố (lease, merge).

## packet_id · packet_issue
`CI-DUONG-NHANH-HO-SO` · #674

## nguon_cap_viec
Issue #674, tự thân là phiếu mở packet của chủ kho. Không có dòng kế hoạch `tệp:dòng` nào khác.

## review_class
`sensitive` — `docs/PROTOCOL_DA_PHIEN.md` mục Review Class liệt "workflow/CI authority" vào `sensitive`
(đo 2026-09-29: dòng 680). Đòi Codex `cross_approved` hoặc `human_audited`.

## write_set
1. `.github/workflows/ci.yml`
2. `ops/ci_duong_nhanh.py` (mới)
3. `ops/ci_duong_nhanh_test.py` (mới)
4. `.claude/dev/ci_dang_ky_test.py` (r2; chỉ đúng một dòng: thêm `"ops/ci_duong_nhanh_test.py"` vào `DA_NOI`)

Ngoài write set, cố ý: `ops/cong_cu_test.py`, job `gate-registry`,
`RELEASE_MANIFEST.json` (xem `chua_do_duoc` mục 4 về manifest).

## ngoai_pham_vi
- Không đổi job `gate-registry`, `gate-packet-loop` về cấu trúc; không đổi ruleset 20856202; không đổi required checks.
- Không dùng `paths:` / `paths-ignore:`. Không áp cho `push` và `workflow_dispatch` (luôn đầy đủ).
- Không mở rộng `JOB_G5` / `cong_cu_test.t6` (Q6 chọn phương án i: chấp nhận lỗ, ghi thành nợ có tên
  `ci-if-cap-job-gate-ops-va-buoc-sau-g5-khong-co-cong-canh`).
- Không chạy Windows CI (chủ kho, 2026-09-29).
- Không đổi số dòng `AL_VER:` trong `ci.yml` (không thêm bước cài actionlint).

## Quyết định đã chốt (Q1–Q6)
- Q1: bước phân loại nằm ở job `chuan-bi`, xuất `outputs.che_do`; `chuan-bi` thêm `actions/checkout` `fetch-depth: 0`.
- Q2: allowlist đúng bốn tiền tố `ops/land/`, `ops/leases/`, `ops/reviews/`, `ops/specs/`.
- Q3: diff rỗng ⇒ `duong_nhanh`, kèm dòng log riêng phân biệt.
- Q4 (SỬA ở r2): KHÔNG đụng job `gate-registry` và KHÔNG đụng `BAM_GATE_REGISTRY`/`JOB_G5`/logic của `ci_dang_ky_test.py`; chỉ được thêm ĐÚNG MỘT mục `"ops/ci_duong_nhanh_test.py"` vào `DA_NOI` (r1 cấm hẳn; cấm ấy không đứng cùng nghiệm thu 9, xem dưới).
- Q5: lease #674 chỉ cấp khi lease `ci.yml` của #668 đã nhả; thi công trên master đã có #668 (đo lại baseline `AL_VER` và `JOB_G5` lúc đó).
- Q6: phương án i (nợ có tên), write set giữ hẹp.

## muc_tieu
- **M1** — `chuan-bi` có bước phân loại: sự kiện `pull_request`, diff `base...head` (ba chấm), trả `che_do` ∈ {`duong_nhanh`, `day_du`}. → `.github/workflows/ci.yml`
- **M2** — Trong `gate`, `gate-ops`, `gate-packet-loop`, các bước nặng có `if:` mức bước theo `needs.chuan-bi.outputs.che_do`; job vẫn khởi động, ba required check vẫn báo. Bước bị bỏ in `DUONG_NHANH: bo qua <buoc> vi diff chi gom …`. Bước kiểm rẻ giữ lại. → `.github/workflows/ci.yml`
- **M3** — Logic phân loại, allowlist, ba trạng thái và dòng log nằm trong script Python có phản chứng. → `ops/ci_duong_nhanh.py`, `ops/ci_duong_nhanh_test.py`
- **M4** — Ba trạng thái fail-close: đo được và toàn allowlist ⇒ nhanh; đo được và có tệp ngoài ⇒ đầy đủ; KHÔNG ĐO ĐƯỢC (thiếu SHA, SHA không phải 40 hex thường hoặc toàn số 0, git lỗi hoặc ném) ⇒ đầy đủ. → `ops/ci_duong_nhanh.py`

Danh sách bước nặng bị bỏ và bước kiểm rẻ giữ lại do phiên thi công đề xuất trong PR, đóng băng qua review; phải
gồm ở `gate`: `tl selftest`, `release-check full`, `release-bundle x2`, `golden-test`, `determinism-audit`; ở
`gate-ops`: cgroup + `gate_lifecycle`, `lease-publish selftest`; ở `gate-packet-loop`: `packet-loop selftest`.
Bước giữ lại tối thiểu: `doctrine-scan`, kiểm YAML parse, `git diff --check`, và `lease_publish.py check` cho tệp lease đổi.

## nghiem_thu
Mỗi tiêu chí kèm phép đo làm nó ĐỎ.
1. PR chỉ đổi `ops/land/x.yaml` ⇒ `duong_nhanh`. ĐỎ khi: đột biến làm `phan_loai` trả `day_du` cho tập toàn allowlist (ca `t1`).
2. PR đổi `ops/leases/y.yaml` + `scripts/tl.py` ⇒ `day_du`. ĐỎ khi: đột biến **nới allowlist** thêm `scripts/` (ca `t9` phải làm `t2` đỏ).
3. KHÔNG ĐO ĐƯỢC ⇒ `day_du`. ĐỎ khi: đột biến **fail-open** (không đo được ⇒ nhanh) làm ca `t5`/`t6` đỏ (ca `t10`).
4. `push` và `workflow_dispatch` ⇒ `day_du`, không gọi `git diff`. ĐỎ khi: đột biến gọi git cho `push` (ca `t3`).
5. Tệp `.github/workflows/ci.yml` trong diff ⇒ `day_du`. ĐỎ khi: đột biến thêm `.github/` vào allowlist (ca `t8`).
6. Đột biến ở tầng YAML: gỡ điều kiện `github.event_name == 'pull_request'` khỏi bước phân loại, hoặc đổi `if:` của một bước nặng thành luôn-bỏ ⇒ ca kiểm cấu trúc `ci.yml` trong `ci_duong_nhanh_test.py` phải ĐỎ (ca này bù cho lỗ mà `ci_dang_ky_test` và `cong_cu_test.t6` không canh, Q6-i).
7. Không dùng `paths:` / `paths-ignore:`: ca `ci_duong_nhanh_test.py` quét `ci.yml` và ĐỎ nếu gặp khoá đó.
8. `actionlint .github/workflows/ci.yml` rc=0 (kèm `shellcheck` có mặt); chèn `${{ }}` rỗng vào comment của `run:` ⇒ rc≠0.
9. `python .claude/dev/ci_dang_ky_test.py` N/N (hai số bằng nhau, không tin `rc`), N = N baseline lúc thi công cộng số ca do đúng một mục `DA_NOI` mới thêm (đo baseline trước và sau, ghi cả hai). ĐỎ khi: đột biến gỡ mục mới khỏi `DA_NOI` ⇒ `test sống chưa đăng ký: ops/ci_duong_nhanh_test.py`; đột biến gỡ bước gọi `python ops/ci_duong_nhanh_test.py` khỏi mọi `run:` của `ci.yml` ⇒ sổ báo mục `DA_NOI` không có lời gọi thật. Diff của `.claude/dev/ci_dang_ky_test.py` phải đúng một dòng thêm (`git diff --numstat`); hơn thì dừng hỏi chủ kho.
10. `python scripts/tl.py --selftest` N/N (hai số bằng nhau); delta ruff F so `origin/master` = 0.
11. PR thật chỉ đổi `ops/land/*.yaml`: ba required check `success`, log có dòng `DUONG_NHANH`, `gate (ubuntu-latest)` ngắn hơn rõ rệt so 52 phút đo ngày 2026-09-29 (run 36518707072). CHỈ đo được sau khi có PR thật — ghi `chua_do_duoc`, không tính là đã đạt trước land.

## hinh_dang_ke_thua
`khong_ap_dung` — không phải packet khắc phục.

## chua_do_duoc
1. Thời gian tiết kiệm thật: cần PR thật.
2. `git diff base...head` trên PR có lịch sử phức tạp (rebase giữa chừng, fork): chỉ đo được trên GitHub.
3. `pull_request.base.sha` / `head.sha` luôn là 40 hex ở mọi loại sự kiện con: giả định theo tài liệu GitHub, chưa tự đo.
4. `RELEASE_MANIFEST.json`: `ops/**` không nằm trong manifest theo CLAUDE.md, còn `ci.yml`/`.github/**` thì phiên thi công phải đo bằng `release-verify --strict` trước khi tin.
5. Hành vi khi #668 land trước: số `AL_VER:` (hiện 4, #668 dự kiến 5) và `JOB_G5` phải đo lại lúc thi công.

## Vì sao r2 (đo được, phiên thi công session_01Fd7YEcw3odAk7QKkydKycE, Issue #674 comment 5885368941)
`tim()` trong `.claude/dev/ci_dang_ky_test.py` coi mọi `ops/*_test.py` ở mức đỉnh là "test sống"; `kiem()` đòi mỗi test sống nằm trong `DANG_KY = MOI | DA_NOI`, và mỗi mục `DA_NOI` phải có lời gọi thật trong một `run:` của workflow. Đo trên clone tạm tại `1741e0a`: nền `ĐĂNG KÝ: 22/22`, rc=0; nền cộng đúng một tệp `ops/ci_duong_nhanh_test.py` ⇒ `ĐĂNG KÝ: 23/22`, `TỔNG: ĐỎ`, rc=1. Tức r1 (test mới đúng tên, nghiệm thu 9, Q4 cấm sửa) không thoả cùng lúc. Ba hướng đã cân: (A) thêm tệp vào write set [chọn]; (B) đổi tên tránh `*_test.py`; (C) gộp test vào `--selftest`. (B) và (C) né đúng sổ sinh ra để bắt test chưa nối nên bị loại.

## Khác biệt so với r1
- write set thêm `.claude/dev/ci_dang_ky_test.py` (một dòng); Q4 sửa; nghiệm thu 9 viết lại; M3 thêm: `ci.yml` có bước gọi `python ops/ci_duong_nhanh_test.py` ở một job bắt buộc, ngoài đường bị bỏ (phiên thi công chọn `gate` hay `gate-ops` theo đo và ghi lý do).
- Giao với lease #668: `.claude/dev/ci_dang_ky_test.py` và `.github/workflows/ci.yml` cùng nằm trong write set lease #668 g2 (`ci-g5-cong-cu-chia-manh-r1-g2-claude`, hạn 2026-09-30T07:41Z). Chủ kho duyệt lệch (chọn A, 2026-09-29); #674 KHÔNG land trước #668. #668 cũng sửa `ci_dang_ky_test.py` (`loi_g5_workflow`/`JOB_G5`), nên hai thay đổi trên tệp ấy hợp nhất sau khi #668 land; xung đột không giải được mà không đổi hành vi ⇒ dừng hỏi chủ kho.

## Quan hệ với packet khác
- #668 giữ `ci.yml` và `.claude/dev/ci_dang_ky_test.py` (lease `ci-g5-cong-cu-chia-manh-r1-g2-claude`, hạn 2026-09-30T07:41Z lúc soạn r2). Chủ kho duyệt #674 thi công song song trên hai tệp này (lệch có ghi trong lease); #674 chỉ land sau #668, trên master đã chứa #668.
- Bản nháp script + 13 ca test do phiên chuẩn bị soạn ở scratchpad (không nằm trong kho); phiên thi công dựng lại trong write set, không chép mù.
