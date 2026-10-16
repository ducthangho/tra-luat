---
kieu: dac_ta_packet
packet: CI-DOT-BIEN-CHIA-MANH
packet_id: CI-DOT-BIEN-CHIA-MANH
ban: r2
trang_thai: dong_bang_khi_dang_bam
nguon_cap_viec: >-
  Chỉ thị chủ kho cho phiên Claude Code 27-09-2026: "Hướng 1 — chia nhỏ vòng đột biến của
  `ops/nhanh_don_duoc_test.py` … chạy thành nhiều mảnh song song, để lượt đột biến đủ hằng tuần giảm từ khoảng 60 phút
  xuống còn cỡ 25 phút … mỗi mảnh vẫn phải giết đúng tập mutant của nó; tổng các mảnh phải bằng tập đầy đủ, không mất
  và không trùng mutant; bằng chứng dương dạng N/N". Quyết định trong phiên (AskUserQuestion, 27-09): "Matrix + job
  gom"; "4 mảnh"; "Nâng trần cho cả hai" (≤ 3 tệp, ~450 dòng thêm); lease cấp SAU khi hai lease cũ trên
  `ci_dang_ky_test.py` hết hạn ("Soạn spec + Issue ngay, cấp lease sau 15:19Z").
nguon_cap_viec_r2: >-
  Chủ kho 27-09-2026 (sau land #662): "Có đưa r543 vào #661". Đo trên PR #662 (job `108605757869`): lượt ĐỦ của
  `nhanh_don_duoc_test` ĐỎ vì đột biến `dau-phien-bo-vong-rut-lai` làm `r543` chết lây ~3,3 % lượt (tái hiện tại chỗ:
  10/300 dưới đột biến, 0/300 trên mã gốc); chạy lại cùng head ⇒ xanh (job `108616023380`, 200/200).
ghi_chu_hinh_dang: Chưa cổng nào đọc tệp này. Nó là DỮ LIỆU cho lease và cho reviewer.
---

# `CI-DOT-BIEN-CHIA-MANH` — chia vòng đột biến của `nhanh_don_duoc_test` thành 4 mảnh + job gom trong lượt tuần (bản **r2**)

- `packet_id`: **`CI-DOT-BIEN-CHIA-MANH`** · `revision`: 2 · `generation`: 1 (dự kiến; chưa cấp lease nào cho r1) — r1 `ae11b48f…` bị thay bởi bản này
- `review_class`: **`sensitive`** — đổi chính sách chọn test của CI (`ci_dang_ky_test.py`), bộ test có vòng đột
  biến tự kiểm, và workflow.
- `risk`: `sensitive` · `environment`: `cloud` · `depends_on`: `[]` (kế thừa #651 `68b552d`, đã land)
- executor: `anthropic_claude` · `claude_code` · `claude-opus-5-5`
- assurance: Codex CLI tại chỗ (`gpt-6-astra`, `xhigh`, tối đa **2** lượt theo §8) + Codex connector (advisory);
  **`human_audited`** là cổng land.
- base: `origin/master` **`518faca7c79b55f068bef8996d28cedad3d242aa`** (đo 2026-09-27T13:29Z; W1–W3 không đổi so `5c79fa2`). Nếu master trôi trước
  khi cấp lease thì lease neo master MỚI và ghi lại đo §1 nếu `ops/nhanh_don_duoc_test.py`/W2/W3 đổi.

## 1. Phép đo nền

- Run `36279193715` (`workflow_dispatch` của `ci-dot-bien-du.yml` trên `68b552d`, `CI_DANG_KY_WORKERS=2`), job
  `108507663436` **3628 s**; bước `test registry` 3605 s. Dòng `CI_DANG_KY_THOI_GIAN` (tải log job, đo 27-09 09:3xZ):
  `ops/nhanh_don_duoc_test.py` **3219,7 s** (bắt đầu 23:28:29Z — sau `subagent_ghi_detect_test` — tới 00:22:09Z) ·
  `pretooluse_guard_test` **1243,5 s** · `subagent_ghi_detect_test` 318,6 s · `mcp_gh_test` 59,1 s · còn lại < 3 s.
  `"so_lop_logic": 2`, `"so_lop_dung_duoc": 2` ⇒ runner **2 lõi**.
- Tại chỗ (container 4 lõi, head `5c79fa2`): T1..T8 (`NHANH_DON_DUOC_KHONG_DOT_BIEN=1`) **1,3 s**; một lượt
  `NHANH_DON_DUOC_CHI_TU_KIEM=1` (48 ca `TU_KIEM`) **10,9 s**. `DOT_BIEN` = **10** mutant (mỗi cái chạy T1..T8, ≤ 2 lần);
  `DOT_BIEN_TU_KIEM` = **185** mutant (mỗi cái chạy trọn 48 ca `TU_KIEM` trong tiến trình con) ⇒ ≈ 97 % thời gian bộ.
- Hệ quả thiết kế: tổng việc lượt tuần ≈ 4 840 giây-lõi; song song trong MỘT job 2 lõi tối đa xuống ≈ 40 phút ⇒ phải
  chia sang nhiều JOB (runner riêng). 4 mảnh ⇒ mỗi mảnh ≈ 3220 / 4 ≈ 805 s + thiết lập; đường găng còn lại là
  `pretooluse_guard_test` ≈ 1243 s ⇒ ước lượt tuần ≈ 22–25 phút (ước, không phải cam kết; A7 đo thật).

## 2. Lệch có duyệt

Trong lượt TUẦN (không phải lane PR), job registry chạy `nhanh_don_duoc_test` ở chế độ nhẹ (T1..T8) vì vòng đột biến
ĐỦ của nó do 4 job mảnh + job gom cùng workflow đảm nhận. Chỉ bật được bằng biến `CI_DANG_KY_DOT_BIEN_MANH` mà
`loi_env_registry` CẤM trong `ci.yml` (env bước registry phải BẰNG ĐÚNG `ENV_REGISTRY`), và `loi_workflow_dot_bien_du`
chỉ cho phép khi workflow tuần có đủ job mảnh + job gom đúng hình dạng (M5). Lane PR/master không đổi.
Nâng trần ADR-0044 (`sensitive` ≤ 300 dòng) lên **~450 dòng thêm, ≤ 3 tệp** — quyết định chủ kho 27-09.

## 3. Ngoài phạm vi

| thứ | lý do |
|---|---|
| chia mảnh `pretooluse_guard_test` / `subagent_ghi_detect_test` | ngoài chỉ thị; ghi thành hướng tiếp nếu A7 cho thấy đường găng vượt 25 phút |
| đổi `ops/nhanh_don_duoc.py` (công cụ) | không đổi hành vi công cụ |
| lane PR (`ci.yml`) | không đổi; `gate-registry` giữ nguyên, `BAM_GATE_REGISTRY` không đổi |
| song song TRONG một mảnh | runner 2 lõi; tăng rủi ro tranh chấp, không cần cho mục tiêu |
| Windows | lượt tuần chỉ ubuntu (như #651) |

## 4. Write set — 3 đường

| # | đường dẫn | vì sao |
|---|---|---|
| W1 | `ops/nhanh_don_duoc_test.py` | M1 chế độ mảnh · M2 chế độ gom · M3 ca tự kiểm + đột biến riêng · M7 `r543` tất định |
| W2 | `.claude/dev/ci_dang_ky_test.py` | M4 biến `CI_DANG_KY_DOT_BIEN_MANH` trong `ke_hoach` · M5 chốt hình dạng workflow tuần mới · phản chứng `p*` |
| W3 | `.github/workflows/ci-dot-bien-du.yml` | M6 job `dot-bien-manh` (matrix 4) + job `dot-bien-gop` |

## 5. Mục tiêu

| # | mục tiêu | đường |
|---|---|---|
| M1 | `NHANH_DON_DUOC_MANH="k/N"` (khớp đúng `^[0-9]/[2-8]$`, `k < N`; sai ⇒ rc≠0, không chạy gì) ⇒ chạy T1..T8 + trọn `TU_KIEM` + CHỈ mutant có chỉ số `i % N == k` trong `DOT_BIEN` và trong `DOT_BIEN_TU_KIEM`. Tên mutant trong mỗi bảng phải DUY NHẤT (trùng ⇒ rc≠0). Bắt buộc có `NHANH_DON_DUOC_MANH_RA=<tệp>`; chỉ khi mảnh ĐẠT trọn mới ghi JSON `{phien_ban, manh, so_manh, sha256_test, sha256_tool, giet, tk_giet}` (tên đã GIẾT theo thứ tự bảng). In `MANH k/N: MUTANT giet = a / a · TU DOT BIEN giet = b / b`. Chế độ mảnh **KHÔNG** in dòng `MUTANT: giet = … / tong …` (mẫu `MAU_DAY_DU`). Tiến trình con của vòng đột biến không thừa kế hai biến mảnh | W1 |
| M2 | `python ops/nhanh_don_duoc_test.py --gop <thư mục>`: đọc MỌI `*.json` trong thư mục; ĐẠT chỉ khi: đúng N tệp, cùng `so_manh = N`, tập `manh` = `{0..N-1}`, `sha256_test`/`sha256_tool` = băm của tệp đang chạy, `giet`/`tk_giet` của mảnh k BẰNG ĐÚNG phân hoạch k (tái tính từ bảng), hợp các mảnh = trọn bảng, đôi một rời nhau. ĐẠT ⇒ in `GOP MANH N/N` và dòng `MUTANT: giet = 10 · khong giet = 0 · khong do duoc = 0 / tong 10` (khớp `MAU_DAY_DU`) và `TU DOT BIEN: giet = 185 / 185`; mọi lệch ⇒ rc≠0 kèm lý do | W1 |
| M3 | Mỗi chốt của M1/M2 có ca `TU_KIEM` riêng (`r549`…), vào `NHOM_BAT_BUOC`/`SAN_NHOM`, và có đột biến riêng trong `DOT_BIEN_TU_KIEM` gỡ đúng chốt ấy làm ca ĐỎ | W1 |
| M4 | `ke_hoach`: biến `CI_DANG_KY_DOT_BIEN_MANH` = đúng `ops/nhanh_don_duoc_test.py` ⇒ bộ ấy `nhe` với lý do "vòng đột biến do job mảnh + gom"; giá trị khác (rỗng thì coi như vắng) ⇒ registry ĐỎ trước khi chạy bộ nào; hai bộ kia không đổi | W2 |
| M5 | `loi_workflow_dot_bien_du` (danh sách CHO PHÉP mọi tầng): job `dot-bien-du` như cũ trừ env bước registry = `{CI_DANG_KY_WORKERS: "2", CI_DANG_KY_DOT_BIEN_MANH: "ops/nhanh_don_duoc_test.py"}`; job `dot-bien-manh` và `dot-bien-gop` đúng hình dạng GHIM (matrix `manh: [0, 1, 2, 3]` khớp N=4 trong `NHANH_DON_DUOC_MANH`; tải lên/tải về artifact đúng tên/mẫu; `dot-bien-gop` `needs: dot-bien-manh`; không `if`/`continue-on-error`/`env` cấp workflow; `permissions: {contents: read}`) | W2 |
| M6 | W3 theo M5; `actionlint` rc=0 | W3 |
| M7 | `r543` TẤT ĐỊNH dưới đột biến `dau-phien-bo-vong-rut-lai`: ca không được chết vì hai lần rút đầu phiên trùng nhau (bộ sinh của ca vẫn giữ KHÔNG GIAN HẸP mà `r508`/`r528` cần, nhưng không lặp giá trị liên tiếp). Tập ca đỏ của đột biến ấy phải đúng `{r527, r528}` MỌI lượt. Không đổi `DOT_BIEN_TU_KIEM` đích của mục ấy, không nới phân hạng | W1 |

## 6. Nghiệm thu

| # | tiêu chí | phép đo làm ĐỎ |
|---|---|---|
| A1 | Tại chỗ: 4 lượt `NHANH_DON_DUOC_MANH=k/4` rồi `--gop` ⇒ `GOP MANH 4/4`, `MUTANT: giet = 10 · … / tong 10`, `TU DOT BIEN: giet = N / N` (N = số mục bảng lúc đo, hai số BẰNG NHAU), rc=0; tổng `a` các mảnh = 10, tổng `b` = N | bất kỳ lượt rc≠0 hoặc hai số lệch |
| A2 | `--gop` ĐỎ với: thiếu 1 tệp · thừa 1 tệp (mảnh trùng) · một tên bị chuyển sang mảnh khác · một tên bị xoá · `sha256_test` lệch · `so_manh` lệch · JSON hỏng | ca `r549+` tương ứng; đột biến gỡ từng chốt ⇒ ca ĐỎ |
| A3 | Chế độ mảnh: `k/N` sai hình dạng (`4/4`, `0/1`, `a/4`, `0/9`, ` 0/4`) ⇒ rc≠0 và KHÔNG chạy vòng đột biến; vắng `..._RA` ⇒ rc≠0; không in dòng `MAU_DAY_DU`; phân hoạch 4 mảnh phủ đúng bảng, rời nhau | ca `r5xx` + đột biến |
| A4 | Toàn bộ suite KHÔNG mảnh (hành vi cũ) vẫn ĐẠT tại chỗ: `MUTANT: giet = 10 · khong giet = 0 · khong do duoc = 0 / tong 10`, `TU KIEM co dot bien rieng: k/k`, `dot bien giet N/N` | rc≠0 hoặc số lệch |
| A5 | W2: `ke_hoach` nhận biến đúng ⇒ `nhe`; giá trị lạ ⇒ ĐỎ; `ci.yml` thêm biến vào env registry ⇒ `loi_env_registry` ĐỎ; `loi_workflow_dot_bien_du` ĐỎ với: thiếu job gom · gom không `needs` · matrix 3 phần tử · `NHANH_DON_DUOC_MANH` sai N · job mảnh có `if` · `continue-on-error` · env registry thiếu/thừa biến · trôi bước so `gate-registry`; workflow thật ĐẠT | ca `p*` |
| A6 | Delta = 0 trên bộ khác: `ci_dang_ky_test.py` phần chung, ruff F delta = 0 (`nhanh_don_duoc_test.py`, `ci_dang_ky_test.py`), `actionlint` W3 rc=0 | đo hai vế cùng một lệnh |
| A8 | `r543` dưới đột biến `dau-phien-bo-vong-rut-lai`: ≥ 300 lượt gọi trực tiếp ⇒ 0 lượt đỏ (nền đo 10/300); trên mã gốc 0/300; mọi mục `DOT_BIEN_TU_KIEM` đang nhắm `r543` vẫn GIẾT (đo trong A4); đột biến trả bộ sinh cũ của `r543` ⇒ phép đo 300 lượt lại thấy lượt đỏ | đo trực tiếp + A4 |
| A7 | Sau land (quan sát, không phải cổng land): một `workflow_dispatch` của W3 — mọi job xanh, `GOP MANH 4/4`, thời gian tường workflow so 3628 s nền | — |

## 7. Ngân sách CI

`0 / 1 / 2` lượt `pull_request`. PR chạm `ops/nhanh_don_duoc_test.py` ⇒ `gate-registry` chạy ĐỦ bộ ấy (~50 phút).
`workflow_dispatch` của W3: không cấp trước land (chỉ gọi được từ nhánh mặc định).

## 8. Điều kiện dừng

S1 chạm đường ngoài W1–W3 · S2 CI đỏ vì packet · S3 hết 2 lượt Codex ⇒ Review Rescue Checkpoint, hỏi chủ kho ·
S4 push chỉ sau review tại chỗ sạch · S5 > 450 dòng thêm · S6 hết hạn lease ⇒ handoff §7.

## 9. `hinh_dang_ke_thua`

`khong_ap_dung` — không phải packet khắc phục. Kế thừa hình dạng chốt workflow tuần của #651 (`loi_workflow_dot_bien_du`,
`loi_actionlint`) và bài học "tín dụng giả" (`CLAUDE.md`): mảnh chỉ tính GIẾT theo đúng bộ phân hạng hiện có
(`doc_kenh`, `TinHieuChotCa`), không thêm đường phân hạng mới.

## 10. `chua_do_duoc`

- Thời gian thật của lượt tuần sau chia (chỉ A7 đo được, sau land).
- Artifact giữa các job: phụ thuộc `actions/upload-artifact@v4` / `download-artifact@v4`; hành vi lỗi của action
  (tệp vắng) chỉ đo được trên runner thật.
- Danh tính người ký lease (#566); effort thực tế của phiên executor.
