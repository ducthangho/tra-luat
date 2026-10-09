---
kieu: dac_ta_packet
packet: CI-REGISTRY-NANG-TRAN-BO-DAY-DU
packet_id: CI-REGISTRY-NANG-TRAN-BO-DAY-DU
packet_issue: 705
ban: r3
trang_thai: dong_bang_khi_dang_bam
nguon_cap_viec: >-
  Chủ kho trong phiên Claude Code session_01WktdUCQr2FQQ5j76LjrxgF, 2026-10-01: "Đồng ý các khuyến nghị" — Q1 (c) nâng
  trần ngay, chia mảnh để packet sau; Q3 executor phiên này + reviewer review-opus-max (same_provider), land human_audited;
  Q4 5400 s / 105 phút. Neo: issues/705. r2: review lượt 1 (issuecomment-5930405321) ra F1 P2 ngoài write set; chủ
  kho chọn "Spec r2 nới write set (Recommended)" — thêm W4, vá F1 cùng ba P3 F2–F4 theo hint. r3: Codex cross-review
  PR #707 lượt 1 khác họ (verdict sha256 045279e9…628e06d, head f9c8dbd) ra 0 P1 / 1 P2 / 1 P3; chủ kho chọn "Spec r3
  + lease g3 (Recommended)" (AskUserQuestion, 2026-10-07) — r3 = r2 + erratum ba con số §1 + M10/A2(e) cho lớp P2.
ghi_chu_hinh_dang: Chưa cổng nào đọc tệp này. Nó là DỮ LIỆU cho lease và cho reviewer.
---

# `CI-REGISTRY-NANG-TRAN-BO-DAY-DU` — nâng trần một bộ của registry và trần job `gate-registry` (bản **r3**)

- `packet_id`: **`CI-REGISTRY-NANG-TRAN-BO-DAY-DU`** · Issue **#705** · `revision`: 3 · `generation`: 3
- `review_class`: **`sensitive`** — đổi `.github/workflows/ci.yml` và một hằng số của cổng registry.
- `risk`: `sensitive` · `environment`: `cloud` · `depends_on`: `[]`
- executor: `anthropic_claude` · `claude_code` · `claude-opus-5-5`
- reviewer: `review-opus-max` (`claude-opus-5-5`, effort max) — **`advisory_review` / `same_provider`** vì cùng họ với
  executor; Codex hết hạn mức tới 2026-10-03 18:31. Cổng land: **`human_audited`**.
- reviewer từ r3: Codex CLI (`openai_codex`, khác họ executor) — review chéo trên head thật của nhánh thi công. Cổng land
  giữ nguyên **`human_audited`** theo Q3; r3 KHÔNG đổi cổng land.
- base: `origin/master` **`7e5958e`** (đo 2026-10-01T10:31Z).

## 1. Phép đo nền

`GIAY_TOI_DA_MOT_BO = 4500` (`.claude/dev/ci_dang_ky_test.py:696`); `gate-registry.timeout-minutes: 90`
(`.github/workflows/ci.yml:843`); `dot-bien-du.timeout-minutes: 90` (`.github/workflows/ci-dot-bien-du.yml:21`) — đo
2026-10-01T10:3xZ trên `7e5958e`.

Thời gian `ops/nhanh_don_duoc_test.py` chế độ ĐỦ (đơn vị: giây tường của một bộ, theo `CI_DANG_KY_THOI_GIAN`):

| lượt | commit | giây | kết quả bộ | job `gate-registry` |
|---|---|---|---|---|
| master #681 (run 36642392330) | `7b308bc` | 3645 | rc=0 | xanh, 67 phút |
| master #668 lượt 1 (run 36696528580) | `423b4ba` | > 4500 | rc=-9 hết giờ | ĐỎ, 83 phút |
| master #668 lượt 2 (cùng run, chạy lại) | `423b4ba` | > 4500 | rc=-9 hết giờ | ĐỎ, 83,1 phút |
| PR #703 (run 36839918701) | `46bc11d` | > 4500 | rc=-9 hết giờ | ĐỎ, 83,2 phút |

Delta tại chỗ (container 4 lõi, hai clone dựng một lệnh, chạy tuần tự, 2026-10-01): `7b308bc` **4604 s** · `423b4ba`
**4586 s** (−0,4 %; output khớp từng dòng; tệp test trùng byte). Hai bộ vô can trong cùng các lượt ĐỎ cũng chậm 22–42 %
(`pretooluse_guard_test` 914 → 1213–1300 s; `subagent_ghi_detect_test` 316 → 386–400 s) ⇒ runner chậm, biên 19 % không đủ.

Chọn số (chủ kho Q4): 3645 s × 1,42 (mức chậm nhất đo được, làm tròn) ≈ 5180 s, cộng ~4 % ⇒ **5400 s**. Job: 5400 s (90 phút) +
~8 phút thiết lập + ~2 phút chờ worker ≈ 100 ⇒ **105 phút**. KHÔNG bảo đảm mọi runner — chỉ nới biên tới ~48 % trên
3645 s; giải pháp bền là chia mảnh (ngoài phạm vi, §3).

> **Erratum r3** (lớp `ty-le-cham-khong-khop-so-do`, P3). r1/r2 ghi "25–40 %", "1,40" và "~6 %". Tính lại từ chính các
> số đo trên: 1213/914 = 1,327 · 1300/914 = 1,422 · 386/316 = 1,222 · 400/316 = 1,266 ⇒ dải **22–42 %**, mức chậm nhất
> **1,42**; 3645 × 1,42 = 5176 s; 5400/5176 − 1 = **4,3 %**; 5400/3645 − 1 = 48,1 %. Số đo thô và lựa chọn 5400 s / 105
> phút KHÔNG đổi. Chú thích hằng ở W1 (M8) đã ghi đúng 22–42 % / ~4 % từ r2.

## 2. Lệch có duyệt

- Reviewer cùng họ executor (`same_provider`) — Codex hết hạn mức; chủ kho Q3.
- Không lệch trần ADR-0044: ≤ 3 tệp, ≤ 300 dòng thêm (ước ~15). r2: 4 tệp — vượt trần số tệp ADR-0044 cho `sensitive` một tệp; chủ kho duyệt (chọn spec r2 nới write set); ≤ 30 dòng thêm.

## 3. Ngoài phạm vi

| thứ | lý do |
|---|---|
| chia mảnh `nhanh_don_duoc_test` trên PR (`ci.yml`) | packet sau (chủ kho Q1 c); cần thiết kế lại `loi_env_registry` vốn cấm mảnh trong `ci.yml` |
| thu hẹp `VUNG_CHUNG` | đổi ngữ nghĩa vùng của #651; không được giao |
| trần của `pretooluse_guard_test` / `subagent_ghi_detect_test` riêng | cùng hằng số `GIAY_TOI_DA_MOT_BO` — nới chung, không tách |
| A9 của #668 (mảnh `gate-cong-cu` 13–19 phút) | packet riêng |
| sửa `ops/nhanh_don_duoc_test.py` | không cần; bộ không đổi |

## 4. Write set — 4 đường (r2 thêm W4)

| # | đường dẫn | vì sao |
|---|---|---|
| W1 | `.claude/dev/ci_dang_ky_test.py` | M1 hằng số + chú thích · M2 băm job · M3 các ca neo số cũ |
| W2 | `.github/workflows/ci.yml` | M4 `gate-registry.timeout-minutes` |
| W3 | `.github/workflows/ci-dot-bien-du.yml` | M5 `dot-bien-du.timeout-minutes` |
| W4 | `ops/ci_duong_nhanh_test.py` | M6 `KHUNG_JOB['gate-registry']['timeout-minutes']` (ca `y13` khoá topology ci.yml) |

## 5. Mục tiêu

| # | mục tiêu | đường |
|---|---|---|
| M1 | `GIAY_TOI_DA_MOT_BO` 4500 → **5400**; chú thích ghi số đo §1 và lý do chọn số, theo idiom `#643` sẵn có | W1 |
| M2 | `BAM_GATE_REGISTRY` cập nhật thành băm thật của job `gate-registry` SAU M4 (tính bằng chính `bam_gate_registry` trên ci.yml mới), không đổi gì khác của job | W1 |
| M3 | Ca `p643-tran-bo-nho-hon-timeout-job` đòi `GIAY_TOI_DA_MOT_BO == 5400` và `< 60 * timeout-minutes`; hai ca neo số 90 (`p661-M5-du-timeout-float-do`, `p651-M4-yaml-tho-timeout-trung`) đổi sang 105 / 105.0 mà VẪN đỏ đúng lý do | W1 |
| M4 | `gate-registry.timeout-minutes: 105` (số nguyên) | W2 |
| M5 | `dot-bien-du.timeout-minutes: 105` (số nguyên) — `loi_workflow_dot_bien_du` buộc bằng `gate-registry` | W3 |
| M6 | (r2, F1) `KHUNG_JOB['gate-registry']['timeout-minutes']` 90 → **105** ở `ops/ci_duong_nhanh_test.py`; không đổi mục nào khác của bảng | W4 |
| M7 | (r2, F2) khối chú thích job `gate-registry` trong ci.yml nêu #705 và con số 105; không đổi khoá YAML nào (băm giữ nguyên) | W2 |
| M8 | (r2, F3) chú thích hằng ở W1 khai đúng dải chậm đo được từ §1 (22–42 %) và biên thật (~4 % trên tỉ lệ 1,42) | W1 |
| M9 | (r2, F4) ca `p661-M5-du-timeout-float-do` suy số float từ `timeout-minutes` của `gate-registry` trong ci.yml thật (không hằng tay) | W1 |
| M10 | (r3, lớp `tran-runtime-khong-duoc-ca-kiem-khoa` P2) ca `p643-tran-bo-nho-hon-timeout-job` đo thêm trần **thật sự truyền tới** `communicate` qua đường runtime `_chay_that` (tiến trình con giả, không chờ thật), đòi bằng `GIAY_TOI_DA_MOT_BO`; không thêm ca mới (N giữ nguyên) | W1 |

## 6. Nghiệm thu

| # | tiêu chí | phép đo làm ĐỎ |
|---|---|---|
| A1 | `python .claude/dev/ci_dang_ky_test.py` tại chỗ: `PHẢN CHỨNG: N/N đỏ đúng`, `TỔNG: ĐẠT`, N = N(base) (không mất ca) | rc≠0 hoặc N giảm |
| A2 | Đột biến: (a) `GIAY_TOI_DA_MOT_BO` trở lại 4500 ⇒ `p643-tran-bo-nho-hon-timeout-job` ĐỎ; (b) `timeout-minutes` ci.yml trở lại 90 ⇒ băm lệch ⇒ ĐỎ; (c) ci-dot-bien-du `dot-bien-du` 90 trong khi ci.yml 105 ⇒ `loi_workflow_dot_bien_du` ĐỎ; (d) đột biến đặt trần bộ 6300 (= 60 × 105, không còn nhỏ hơn trần job) ⇒ `p643` ĐỎ; (e) (r3) giá trị mặc định `gioi_han` của hàm chạy một bộ, hoặc đối số `gioi_han` truyền ở `_chay_that`, đổi về 4500 trong khi hằng giữ 5400 ⇒ `p643` ĐỎ (trước r3 hai đột biến này LỌT 1025/1025) | mỗi đột biến chạy trên bản sao, ghi ca đỏ |
| A3 | `actionlint` rc=0 trên cả hai workflow; ruff F delta 0 trên W1 so `7e5958e` | rc≠0 / delta≠0 |
| A4 | Delta = 0 trên `launcher_test.py` (`t152` đếm AL_VER, không đụng), `lease_publish_test.py`, và (r2) `ops/ci_duong_nhanh_test.py` (`CA 104/104 · DOT BIEN 383/383` như nền) — đo hai vế cùng một lệnh | lệch ca |
| A6 | (r2) Răng của M6: ci.yml về 90 trên bản sao ⇒ `ci_duong_nhanh_test --mot-ca y13…` ĐỎ `khac ['timeout-minutes']`; của M9: nới điểm so có kiểu ở `loi_workflow_dot_bien_du` ⇒ `p661-M5-du-timeout-float-do` LỌT, kể cả sau một lần nâng trần giả định | đột biến trên bản sao |
| A5 | CI của PR (MỘT lượt): `gate-registry` chạy chế độ ĐỦ (diff chạm ci.yml) và **xanh** dưới trần mới; ghi giây của `nhanh_don_duoc_test` | rc≠0 / hết giờ |

## 7. Nghĩa vụ sau land

- Packet kế nhiệm: chia mảnh `nhanh_don_duoc_test` trên PR (giải pháp bền); A9 của #668.
- Bookkeeping theo tiền lệ #665/#693: spec + lease vào master, thu hồi lease bằng rút hạn.

## 8. Ngân sách CI

Một lượt CI duy nhất khi đã sạch (chỉ thị chủ kho cho vòng lặp Opus). Không Windows, không chạy tay.

## 9. Điều kiện dừng

S1 chạm đường ngoài W1–W4 · S2 CI đỏ vì packet · S3 cùng lớp finding ≥ 3 lần ⇒ hỏi chủ kho · S4 push một lần sau review
sạch · S5 > 60 dòng thêm ⇒ hỏi · S6 hết hạn lease ⇒ handoff §7.

## 10. `hinh_dang_ke_thua`

`khong_ap_dung` — không phải packet khắc phục của một packet có biên nhận. Tiền lệ cùng hình: #643 (3600 → 4500, PR #644).

## 11. `chua_do_duoc`

- 5400 s có đủ trên runner chậm nhất: chỉ ước từ ba lượt đỏ (đều bị giết ở 4500, không biết số thật); A5 cho MỘT số đo.
- Danh tính người ký lease (#566); effort thực tế của phiên executor.
