---
kieu: dac_ta_packet
packet: CI-REGISTRY-NANG-TRAN-BO-DAY-DU
packet_id: CI-REGISTRY-NANG-TRAN-BO-DAY-DU
packet_issue: 705
ban: r1
trang_thai: dong_bang_khi_dang_bam
nguon_cap_viec: >-
  Chủ kho trong phiên Claude Code session_01WktdUCQr2FQQ5j76LjrxgF, 2026-10-01: "Đồng ý các khuyến nghị" — Q1 (c) nâng
  trần ngay, chia mảnh để packet sau; Q3 executor phiên này + reviewer review-opus-max (same_provider), land human_audited;
  Q4 5400 s / 105 phút. Neo: issues/705.
ghi_chu_hinh_dang: Chưa cổng nào đọc tệp này. Nó là DỮ LIỆU cho lease và cho reviewer.
---

# `CI-REGISTRY-NANG-TRAN-BO-DAY-DU` — nâng trần một bộ của registry và trần job `gate-registry` (bản **r1**)

- `packet_id`: **`CI-REGISTRY-NANG-TRAN-BO-DAY-DU`** · Issue **#705** · `revision`: 1 · `generation`: 1
- `review_class`: **`sensitive`** — đổi `.github/workflows/ci.yml` và một hằng số của cổng registry.
- `risk`: `sensitive` · `environment`: `cloud` · `depends_on`: `[]`
- executor: `anthropic_claude` · `claude_code` · `claude-opus-5-5`
- reviewer: `review-opus-max` (`claude-opus-5-5`, effort max) — **`advisory_review` / `same_provider`** vì cùng họ với
  executor; Codex hết hạn mức tới 2026-10-03 18:31. Cổng land: **`human_audited`**.
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
**4586 s** (−0,4 %; output khớp từng dòng; tệp test trùng byte). Hai bộ vô can trong cùng các lượt ĐỎ cũng chậm 25–40 %
(`pretooluse_guard_test` 914 → 1213–1300 s; `subagent_ghi_detect_test` 316 → 386–400 s) ⇒ runner chậm, biên 19 % không đủ.

Chọn số (chủ kho Q4): 3645 s × 1,40 (mức chậm nhất đo được) ≈ 5100 s, cộng ~6 % ⇒ **5400 s**. Job: 5400 s (90 phút) +
~8 phút thiết lập + ~2 phút chờ worker ≈ 100 ⇒ **105 phút**. KHÔNG bảo đảm mọi runner — chỉ nới biên tới ~48 % trên
3645 s; giải pháp bền là chia mảnh (ngoài phạm vi, §3).

## 2. Lệch có duyệt

- Reviewer cùng họ executor (`same_provider`) — Codex hết hạn mức; chủ kho Q3.
- Không lệch trần ADR-0044: ≤ 3 tệp, ≤ 300 dòng thêm (ước ~15).

## 3. Ngoài phạm vi

| thứ | lý do |
|---|---|
| chia mảnh `nhanh_don_duoc_test` trên PR (`ci.yml`) | packet sau (chủ kho Q1 c); cần thiết kế lại `loi_env_registry` vốn cấm mảnh trong `ci.yml` |
| thu hẹp `VUNG_CHUNG` | đổi ngữ nghĩa vùng của #651; không được giao |
| trần của `pretooluse_guard_test` / `subagent_ghi_detect_test` riêng | cùng hằng số `GIAY_TOI_DA_MOT_BO` — nới chung, không tách |
| A9 của #668 (mảnh `gate-cong-cu` 13–19 phút) | packet riêng |
| sửa `ops/nhanh_don_duoc_test.py` | không cần; bộ không đổi |

## 4. Write set — 3 đường

| # | đường dẫn | vì sao |
|---|---|---|
| W1 | `.claude/dev/ci_dang_ky_test.py` | M1 hằng số + chú thích · M2 băm job · M3 các ca neo số cũ |
| W2 | `.github/workflows/ci.yml` | M4 `gate-registry.timeout-minutes` |
| W3 | `.github/workflows/ci-dot-bien-du.yml` | M5 `dot-bien-du.timeout-minutes` |

## 5. Mục tiêu

| # | mục tiêu | đường |
|---|---|---|
| M1 | `GIAY_TOI_DA_MOT_BO` 4500 → **5400**; chú thích ghi số đo §1 và lý do chọn số, theo idiom `#643` sẵn có | W1 |
| M2 | `BAM_GATE_REGISTRY` cập nhật thành băm thật của job `gate-registry` SAU M4 (tính bằng chính `bam_gate_registry` trên ci.yml mới), không đổi gì khác của job | W1 |
| M3 | Ca `p643-tran-bo-nho-hon-timeout-job` đòi `GIAY_TOI_DA_MOT_BO == 5400` và `< 60 * timeout-minutes`; hai ca neo số 90 (`p661-M5-du-timeout-float-do`, `p651-M4-yaml-tho-timeout-trung`) đổi sang 105 / 105.0 mà VẪN đỏ đúng lý do | W1 |
| M4 | `gate-registry.timeout-minutes: 105` (số nguyên) | W2 |
| M5 | `dot-bien-du.timeout-minutes: 105` (số nguyên) — `loi_workflow_dot_bien_du` buộc bằng `gate-registry` | W3 |

## 6. Nghiệm thu

| # | tiêu chí | phép đo làm ĐỎ |
|---|---|---|
| A1 | `python .claude/dev/ci_dang_ky_test.py` tại chỗ: `PHẢN CHỨNG: N/N đỏ đúng`, `TỔNG: ĐẠT`, N = N(base) (không mất ca) | rc≠0 hoặc N giảm |
| A2 | Đột biến: (a) `GIAY_TOI_DA_MOT_BO` trở lại 4500 ⇒ `p643-tran-bo-nho-hon-timeout-job` ĐỎ; (b) `timeout-minutes` ci.yml trở lại 90 ⇒ băm lệch ⇒ ĐỎ; (c) ci-dot-bien-du `dot-bien-du` 90 trong khi ci.yml 105 ⇒ `loi_workflow_dot_bien_du` ĐỎ; (d) đột biến đặt trần bộ 6300 (= 60 × 105, không còn nhỏ hơn trần job) ⇒ `p643` ĐỎ | mỗi đột biến chạy trên bản sao, ghi ca đỏ |
| A3 | `actionlint` rc=0 trên cả hai workflow; ruff F delta 0 trên W1 so `7e5958e` | rc≠0 / delta≠0 |
| A4 | Delta = 0 trên `launcher_test.py` (`t152` đếm AL_VER, không đụng), `lease_publish_test.py` — đo hai vế cùng một lệnh | lệch ca |
| A5 | CI của PR (MỘT lượt): `gate-registry` chạy chế độ ĐỦ (diff chạm ci.yml) và **xanh** dưới trần mới; ghi giây của `nhanh_don_duoc_test` | rc≠0 / hết giờ |

## 7. Nghĩa vụ sau land

- Packet kế nhiệm: chia mảnh `nhanh_don_duoc_test` trên PR (giải pháp bền); A9 của #668.
- Bookkeeping theo tiền lệ #665/#693: spec + lease vào master, thu hồi lease bằng rút hạn.

## 8. Ngân sách CI

Một lượt CI duy nhất khi đã sạch (chỉ thị chủ kho cho vòng lặp Opus). Không Windows, không chạy tay.

## 9. Điều kiện dừng

S1 chạm đường ngoài W1–W3 · S2 CI đỏ vì packet · S3 cùng lớp finding ≥ 3 lần ⇒ hỏi chủ kho · S4 push một lần sau review
sạch · S5 > 60 dòng thêm ⇒ hỏi · S6 hết hạn lease ⇒ handoff §7.

## 10. `hinh_dang_ke_thua`

`khong_ap_dung` — không phải packet khắc phục của một packet có biên nhận. Tiền lệ cùng hình: #643 (3600 → 4500, PR #644).

## 11. `chua_do_duoc`

- 5400 s có đủ trên runner chậm nhất: chỉ ước từ ba lượt đỏ (đều bị giết ở 4500, không biết số thật); A5 cho MỘT số đo.
- Danh tính người ký lease (#566); effort thực tế của phiên executor.
