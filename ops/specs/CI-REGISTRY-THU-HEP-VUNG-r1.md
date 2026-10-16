---
kieu: dac_ta_packet
packet: CI-REGISTRY-THU-HEP-VUNG
packet_id: CI-REGISTRY-THU-HEP-VUNG
ban: r1
trang_thai: dong_bang_khi_dang_bam
nguon_cap_viec: >-
  Chỉ thị chủ kho trong phiên Claude Code 26-09-2026: "Mở packet CI-REGISTRY-THU-HEP-VUNG: (1) sửa P2 #649
  r4111733460 — chế độ nhẹ từ chối dòng khớp MAU_DAY_DU cho bộ trong MAU_NHE; (2) thu hẹp VUNG_CHUNG/TIEN_TO_CHUNG
  trong .claude/dev/ci_dang_ky_test.py (bỏ ci_dang_ky_test.py khỏi vùng đột biến của bộ khác, .github/** → ci.yml);
  (3) chế độ nhẹ cho .claude/hooks/subagent_ghi_detect_test.py; (4) workflow riêng chạy đột biến đủ hằng tuần +
  workflow_dispatch."
ghi_chu_hinh_dang: Chưa cổng nào đọc tệp này. Nó là DỮ LIỆU cho lease và cho reviewer.
---

# `CI-REGISTRY-THU-HEP-VUNG` — thu hẹp vùng đột biến, chế độ nhẹ cho bộ thứ ba, lượt đủ hằng tuần (bản **r1**)

- `packet_id`: **`CI-REGISTRY-THU-HEP-VUNG`** · `revision`: 1 · `generation`: 1 (dự kiến)
- `review_class`: **`sensitive`** — đổi chính sách chọn test của CI, bộ test của hook bảo vệ, và thêm một workflow.
- `risk`: `sensitive` · `environment`: `cloud` · `depends_on`: `[]` (kế thừa #643 `6d9581c` và #647 `4257814`, đã land)
- executor: `anthropic_claude` · `claude_code` · `claude-opus-5-5`
- assurance: Codex CLI tại chỗ + Codex connector (`advisory_review`); **`human_audited`** là cổng land.
- base: `origin/master` **`24c48e28bacd2c835e6acf7df64c7ee60ae6d424`** (đo 2026-09-26T15:15Z)

## 1. Phép đo nền

- Biên nhận #643: `issues/643#issuecomment-5845867513`; biên nhận #647: `issues/647#issuecomment-5847271381`.
- Run `36246637438` (PR #648, head `1ff9519`), job `gate-registry` `108416948643`: **53m07s**. Kế hoạch in
  `ops/nhanh_don_duoc_test.py: day_du — diff chạm .claude/dev/ci_dang_ky_test.py` ⇒ bộ ấy chạy đủ **2804,52 s**
  chỉ vì PR sửa bộ chọn, không sửa `ops/nhanh_don_duoc*`. `pretooluse_guard_test` 1129,88 s ·
  `subagent_ghi_detect_test` **291,81 s** (`DOT BIEN 25/25 bi giet`, `CA 42/42`).
- Tại chỗ (container, head `24c48e2`): 42 ca nền của `subagent_ghi_detect_test` chạy **7,6 s** ⇒ vòng đột biến
  (25 + 6 nhắm bộ test + 1 nhắm `settings.json`) chiếm ≈ 97 %.
- A4 của #647 (run `36250327138`, master `24c48e2`): lúc đo vẫn `pending` (chờ run `36249954099`). KHÔNG dùng làm
  bằng chứng ở đây; ghi khi có.

## 2. Lệch protocol có duyệt

Mở rộng lệch của #643/#647 (`docs/PROTOCOL_DA_PHIEN.md:839-840`, selector không qua shadow) sang **bộ thứ ba**
`subagent_ghi_detect_test`. Căn cứ: chỉ thị chủ kho ở đầu tệp. Phạm vi y hệt: chỉ vòng đột biến bị bỏ khi diff
không chạm vùng; ca nền và mọi bộ khác vẫn chạy mọi lượt; fallback fail-closed của `ke_hoach` giữ nguyên.

**Thu hẹp vùng (M2) là nới chốt có chủ đích**, và phần mất đi được bù bằng M4:
- `.claude/dev/ci_dang_ky_test.py` ra khỏi vùng chung: bộ chọn tự canh bằng `phan_chung` (chạy mọi lượt, không
  có chế độ nhẹ). Rủi ro còn lại — một bản sửa bộ chọn lỡ đặt cờ nhẹ sai chỗ — chỉ lộ ở lượt đủ hằng tuần (M4).
- `.github/**` → chỉ `.github/workflows/ci.yml` (vẫn nằm trong `VUNG_CHUNG`). Workflow khác, `.github/checks/**`
  không còn ép đủ. `ops/cai_*`, `ops/cong_cu*`, `requirements.txt`, tệp gốc lạ giữ nguyên luật cũ.

## 3. Ngoài phạm vi

| thứ | lý do |
|---|---|
| sửa hook (`subagent_ghi_detect.py`, `pretooluse_guard.py`) | không đổi hành vi hook |
| sửa `ci.yml` | env con do `ci_dang_ky_test.py` đặt; lượt đủ đi workflow riêng |
| nhánh Windows cho `subagent_ghi_detect_test` | bộ không có nhánh Windows; hành vi Windows không đổi ngoài cờ nhẹ |
| `nhanh_don_duoc_test` từ chối dòng đủ khi nhẹ | không áp được: dòng nhẹ `8/8` là tập con của đầu ra đủ (#649 r4111735347) |

## 4. Write set — 3 đường

| # | đường dẫn | vì sao |
|---|---|---|
| W1 | `.claude/dev/ci_dang_ky_test.py` | M1 từ chối dòng đủ khi nhẹ; M2 thu hẹp vùng; M3 đăng ký bộ thứ ba; M4 chốt workflow mới; phản chứng |
| W2 | `.claude/hooks/subagent_ghi_detect_test.py` | cờ chế độ nhẹ + dòng bằng chứng riêng + ca tự kiểm + đột biến nhắm bộ test |
| W3 | `.github/workflows/ci-dot-bien-du.yml` | lượt đột biến đủ: `schedule` hằng tuần + `workflow_dispatch` |

Ngưỡng ADR-0044: ≤ 3 tệp, ≤ 300 dòng thêm.

## 5. Mục tiêu

| # | mục tiêu | đường |
|---|---|---|
| M1 | chế độ nhẹ + bộ có trong `MAU_NHE` ⇒ đầu ra có dòng khớp `MAU_DAY_DU[bộ]` (bất kể số) là **ĐỎ**, in lý do riêng; áp cả Windows. Bộ không trong `MAU_NHE` (`nhanh_don_duoc_test`) không đổi | W1 |
| M2 | `VUNG_CHUNG` = `(".github/workflows/ci.yml", "requirements.txt")`; `TIEN_TO_CHUNG` = `("ops/cai_", "ops/cong_cu")`; vùng riêng theo bộ có thể mở rộng (`VUNG_THEM`) | W1 |
| M3 | cờ `SUBAGENT_GHI_DETECT_KHONG_DOT_BIEN=1` ⇒ chạy đủ ca nền, **bỏ** mọi vòng đột biến, in `TONG: CA a/b dat · DOT BIEN n muc CHE DO NHE — do khi diff cham vung` (không chữ `bi giet`), `DAT` chỉ khi đủ ca nền và `n > 0`. Bộ vào `NHE`/`MAU_DAY_DU`/`MAU_NHE`; vùng = `{bộ, subagent_ghi_detect.py, .claude/settings.json}` ∪ chung | W1+W2 |
| M4 | W3 chạy `python .claude/dev/ci_dang_ky_test.py --chay` KHÔNG có biến diff ⇒ `ke_hoach` fail-closed ⇒ đủ cho mọi bộ. W1 chốt W3: `on` đúng `{schedule, workflow_dispatch}`, `permissions: {contents: read}`, không `env`/`defaults` cấp workflow, một job, bước = bước `gate-registry` của `ci.yml` trừ `env` của bước registry = `{CI_DANG_KY_WORKERS: "2"}` (trích từ CHÍNH hai tệp YAML, không chép) | W1+W3 |

## 6. Nghiệm thu

| # | tiêu chí | phép đo làm ĐỎ |
|---|---|---|
| A1 | qua CHÍNH `chay_moi`: nhẹ + dòng đủ ⇒ ĐỎ (Linux, Windows, cả dòng đủ có mutant sống); nhẹ + dòng nhẹ ⇒ ĐẠT; `nhanh_don_duoc` nhẹ + dòng `MUTANT` ⇒ vẫn ĐẠT | ca `p*` |
| A2 | `ke_hoach`: `ci_dang_ky_test.py`, `.github/workflows/khac.yml`, `.github/checks/x.py` ⇒ nhẹ; `ci.yml`, `requirements.txt`, `ops/cai_*`, tệp gốc lạ ⇒ đủ; `.claude/settings.json` ⇒ đủ cho bộ subagent, nhẹ cho hai bộ kia | ca `p*` |
| A3 | W2 tự kiểm: cờ đúng `"1"` mới nhẹ; dòng nhẹ không chứa `bi giet`; `n = 0` ⇒ `DO`; đột biến nhắm bộ test gỡ từng chốt ⇒ ca đích ĐỎ | ca `t*` + `DOT_BIEN_NHAM_TEST` |
| A4 | W3: workflow thật ĐẠT; thêm `push`/`pull_request`, bỏ `schedule`, `env` cấp workflow có cờ nhẹ, `env` bước registry thêm biến diff, trôi một bước so `gate-registry`, `permissions` ghi ⇒ ĐỎ; `actionlint` rc=0 | ca `p*` + actionlint |
| A5 | CI của PR xanh. Sau land: một lượt `workflow_dispatch` của W3 in `day_du` cho cả ba bộ (quan sát, không phải cổng land) | quan sát |

## 7. Ngân sách CI

`0 / 1 / 2` lượt `pull_request` (mỗi lượt = một workflow run; chạy lại job trong cùng run không tính thêm).
`workflow_dispatch` của W3 **không** được cấp trước land (W3 chỉ gọi được từ nhánh mặc định sau merge).

## 8. Điều kiện dừng

S1 chạm đường ngoài W1–W3 · S2 CI đỏ vì packet · S4 push chỉ sau review tại chỗ sạch · S5 > 300 dòng ·
S6 hết hạn lease ⇒ handoff §7.
