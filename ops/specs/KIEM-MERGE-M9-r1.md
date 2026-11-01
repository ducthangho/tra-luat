# Đặc tả packet `KIEM-MERGE-M9` r1: `kiem-merge` K7 đòi `full_mutant_audit` khi diff chạm vùng M9 (ADR-0060)

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587

| trường | giá trị |
|---|---|
| packet_id | `KIEM-MERGE-M9`, revision 1, generation 1 |
| packet_issue | #1120 |
| nguon_cap_viec | phần ngoài phạm vi của packet C (`ops/specs/DIEU-KIEN-MERGE-CONG-r1.md` §5 và A13). Chủ kho mở ngày 01-11-2026 trong phiên `session_015GtxrYPjZCTZeRiazdssgq` (*"mở một packet riêng, cấp lease và thực thi ở một phiên mới riêng"*). Ba quyết định chốt qua một vòng hỏi: bằng chứng là run đúng H kèm lối miễn · Windows chỉ chạy ca mới · 5 tệp/300 dòng, packet tự chạy audit |
| ưu tiên | chủ kho đặt gọn nhẹ, tốc độ chạy và hiệu năng quy trình **trên** độ chặt của vật chứng |
| review_class | `sensitive`, vì thêm điều kiện vào cổng `.claude/dev/packet_loop.py` (§20) |
| base | `origin/master` lúc cấp lease (đo khi soạn, 01-11: `f4b513d`) |
| executor / reviewer | `anthropic_claude` (một phiên Claude Code MỚI, riêng) / `openai_codex` qua `launcher.py run`, cùng connector `@codex review` trên PR draft |
| windows | `required` (M3 bước 2: diff chạm `.claude/dev/**`) |

## 1. Vì sao — số đo (01-11-2026)

| # | sự kiện | số đo |
|---|---|---|
| S1 | luật | ADR-0060 M9 đòi `full_mutant_audit` khi diff chạm `.claude/dev/**`, `ops/**/*.py` hoặc `.github/workflows/**` |
| S2 | cổng | `kiem-merge` (packet C, merge `aeecf9f`) kiểm K0–K6, **không** điều kiện nào đọc M9. Packet C miễn nó ở A13 và ghi ở §5 *"ngoài phạm vi"* |
| S3 | nguồn audit | `.github/workflows/ci-dot-bien-du.yml` chạy theo lịch hằng tuần hoặc `workflow_dispatch` trên một ref. Các lượt `success` gần đây mất 15–35 phút (run 41248410668, 40135027762, 39741395585) |
| S4 | khuôn dùng lại | `_dong_chu_kho` (dòng của chủ kho, K5/K6), `_doc_json`, `_trang_du`, bộ đọc `git diff --raw` của `_phan_loai_windows`, các fixture `_c1106*` trong test |

## 2. Thay đổi

### 2.1 K7 trong `kiem-merge`

Hai đối số mới, cả hai có thể vắng: `--dot-bien-du-runs <tệp>` và `--dot-bien-du-jobs <tệp>` (lặp được).
- `--dot-bien-du-runs` là readback REST `GET actions/workflows/ci-dot-bien-du.yml/runs?head_sha=H`, dạng trang
  `{total_count, workflow_runs}`.
- `--dot-bien-du-jobs` là `GET actions/runs/<id>/jobs`, dạng trang `{total_count, jobs}`.

| # | điều kiện | phép đo |
|---|---|---|
| K7 | M9 `full_mutant_audit` | **Phạm vi.** Một tệp trong `git diff --raw --no-renames B..H` khớp `.claude/dev/**`, hoặc nằm dưới `ops/` với đuôi `.py`, hoặc khớp `.github/workflows/**` ⇒ `bat_buoc`; không tệp nào khớp ⇒ đạt ngay. Lỗi git ⇒ KHÔNG ĐO ĐƯỢC, tức không đạt. **Khi `bat_buoc`**, đạt nếu một trong hai: (a) comment chủ kho (`--chu-kho-comment`, `user.login` = `CHU_KHO`) có dòng khớp `^full_mutant_audit: H mien$`; (b) có **ít nhất một** run trong `--dot-bien-du-runs` với `path` = `.github/workflows/ci-dot-bien-du.yml`, `head_sha` = H, `status` = `completed`, `conclusion` = `success`, và mọi job của **đúng run_id và run_attempt ấy** trong `--dot-bien-du-jobs` có `status` = `completed`, `conclusion` = `success`; tập job khác rỗng; trang đủ (`total_count` = số phần tử phân biệt id) |

Thông báo thiếu ghi `K7 full_mutant_audit` cùng lý do. K7 đi vào cùng danh sách M6 với K0–K6.

### 2.2 Tài liệu

- `docs/adr/0060-…md` mục *Cưỡng chế — M11*: câu về `packet_loop.py` ghi `K0–K7` thay `K0–K6`; mục *Nợ*: bỏ hoặc đổi
  ý *"`kiem-merge` không kiểm `full_mutant_audit`"* nếu có. Câu về chú thích `ci.yml` giữ nguyên, vì `ci.yml` thuộc
  write set của packet D.
- `.claude/skills/land-packets/SKILL.md`: dòng `kiem-merge` ghi `K0–K7` và hai cờ mới.

## 3. Write set

`.claude/dev/packet_loop.py` · `.claude/dev/packet_loop_test.py` · `docs/adr/0060-dieu-kien-merge-va-moc-ready.md` ·
`.claude/skills/land-packets/SKILL.md` · `ops/specs/KIEM-MERGE-M9-r1.md` (chép **nguyên byte** từ nhánh lease vào
commit đầu tiên của nhánh thực thi, để K1 đọc được blob tại H). Năm tệp, ≤ 300 dòng thêm, tính cả tệp đặc tả.

## 4. Nghiệm thu

Ca mới trong `.claude/dev/packet_loop_test.py` mang tiền tố `cong_m9_`, dùng lại fixture `_c1106`. Đột biến đích phải
bị giết **đúng lý do**, tức ở tín hiệu assertion của ca đích; traceback không tính.

| # | tiêu chí | phép đo làm ĐỎ |
|---|---|---|
| A1 | `packet_loop_test.py` N/N, hai số bằng nhau; mọi ca `cong_c_*` cũ vẫn xanh | bất kỳ ca đỏ |
| A2 | ca: diff chỉ `docs/x.md` ⇒ K7 đạt khi không có readback · diff `.claude/dev/x.py` mà không run, không miễn ⇒ rc `RC_GATE` kèm `K7` · có run `success` đúng H, job đủ `success` ⇒ rc 0 · miễn `full_mutant_audit: H mien` ⇒ rc 0 · `ops/a/b.py` ⇒ `bat_buoc` · `.github/workflows/x.yml` ⇒ `bat_buoc` · `ops/x.md` ⇒ không | — |
| A3 | ca đỏ K7: run `head_sha` ≠ H · `conclusion` ≠ `success` · một job `failure` · job của run_attempt khác · tập job rỗng · trang thiếu (`total_count` lớn hơn số phần tử) · miễn bởi người không phải `CHU_KHO` · dòng miễn mang SHA khác H · `git diff` lỗi | — |
| A4 | đột biến đích (mỗi cái giết ca tương ứng): bỏ so `head_sha` = H · bỏ kiểm job · nhận job của attempt khác · bỏ kiểm người miễn · bỏ `.github/workflows/**` khỏi phạm vi · bỏ `ops/**/*.py` khỏi phạm vi · coi lỗi git là "không chạm" | đột biến sống ⇒ đỏ |
| A5 | M6: K7 thiếu cùng một điều kiện K0–K6 khác ⇒ thông báo nêu cả hai | — |
| A6 | `git diff --numstat <base> <ứng viên>`: đúng năm tệp §3, ≤ 300 dòng thêm | tệp thứ sáu ⇒ đỏ |
| A7 | `doctrine-scan`, `adr-song`, `doc-claims-check` xanh; ADR-0060 và skill ghi `K0–K7` (vế dương) | — |
| A8 | Windows (M3 `required`): **một** lượt ca `cong_m9_*` và `cong_c_*` trên `tra-luat-win` tại ứng viên, > 0 ca, không ca `skipped`. Lượt nền Windows: **chủ kho miễn** | 0 ca ⇒ đỏ |
| A9 | M9 cho chính packet này: một lượt `ci-dot-bien-du.yml` (`workflow_dispatch` trên nhánh thực thi) `success` tại head cuối; `kiem-merge` trên PR, với readback của lượt ấy, ra rc 0 **trước khi bỏ draft**. Đây là canary dữ liệu thật của K7 | run đỏ ⇒ sửa hoặc hỏi chủ kho, không miễn tự động |

## 5. Ngoài phạm vi

- Sửa chú thích `full_mutant_audit` trong `.github/workflows/ci.yml` (`gate-nhanh-manh`): tệp thuộc packet D.
- Tự gọi workflow từ trong lệnh; `kiem-merge` chỉ đọc readback.
- Required check theo lease ngoài M9; `kiem-dong-wp` không đổi.
- Packet tài liệu sau C (biến ADR-0060 thành mặc định).

## 6. `chua_do_duoc`

- Readback REST do executor lấy: lệnh kiểm nội dung, không chứng minh nguồn (cùng giới hạn với K2 của packet C).
- Thời gian chạy `ci-dot-bien-du` trên nhánh mới: ước tính 15–35 phút từ lịch sử, chưa đo trên nhánh này.
