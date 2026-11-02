---
kieu: dac_ta_packet
packet: CI-G5-CONG-CU-CHIA-MANH
packet_id: CI-G5-CONG-CU-CHIA-MANH
packet_issue: 668
ban: r1
trang_thai: dong_bang_khi_dang_bam
nguon_cap_viec: >-
  Phiếu mở packet chủ kho dán vào phiên Claude Code 28-09-2026 ("CI-G5-CONG-CU-CHIA-MANH: kéo bước G5 của job gate
  từ ~46 phút về lại ~5–10 phút"), rồi chỉ thị "Không Ci, full CI, CI  do lỗi đã biết. Lặp vá lỗi, cross review theo
  phân lớp, đăng verdict, tới khi hết P1, P2, P3." Quyết định trong phiên (AskUserQuestion, 28-09): "Chia mảnh mọi
  PR"; "8 mảnh"; "Chủ kho thêm sau land" (ruleset); "≤ 5 tệp, ~600 dòng" (trần ADR-0044). Neo:
  issues/668#issuecomment-5865431816.
ghi_chu_hinh_dang: Chưa cổng nào đọc tệp này. Nó là DỮ LIỆU cho lease và cho reviewer.
---

# `CI-G5-CONG-CU-CHIA-MANH` — chia bán kính đột biến của `cong_cu_test` thành 8 mảnh + job gom (bản **r1**)

- `packet_id`: **`CI-G5-CONG-CU-CHIA-MANH`** · Issue **#668** · `revision`: 1 · `generation`: 1
- `review_class`: **`sensitive`** — đổi workflow `ci.yml`, đổi chính sách G5 (`loi_g5_workflow`), và bộ test có
  vòng đột biến tự kiểm.
- `risk`: `sensitive` · `environment`: `cloud` · `depends_on`: `[]`
- executor: `anthropic_claude` · `claude_code` · `claude-opus-5-5`
- assurance: Codex CLI tại chỗ (`gpt-6-astra`, effort ≥ medium), lặp theo chỉ thị chủ kho tới 0 P1/P2/P3;
  **`human_audited`** là cổng land.
- base: `origin/master` **`f8a7829cc44f296c25faf1a6439b603ba840f70b`** (đo 2026-09-28T07:20Z).

## 1. Phép đo nền

CI (log job, bước G5 `python ops/cong_cu.py kiem-tra --json` + `python ops/cong_cu_test.py`):

| master | job gate | bước G5 | run |
|---|---|---|---|
| `10e859d` (trước #581) | 9m48s | 5m12s | 36336611059 |
| `2c1a4a8` (merge #581) | 52m54s | 48m21s | 36337649143 |
| `79efb0e` | 34m41s | 31m38s | 36358844601 |
| `ceb1a3f` | 50m21s | 45m56s | 36362558889 |

Log `ceb1a3f` in `2 tiến trình` trong khi ci.yml không đặt `CONG_CU_TEST_TIEN_TRINH` ⇒ `min(4, os.cpu_count())` = 2 ⇒
runner **2 lõi**. Tăng số tiến trình trong một job không mua được gì.

Tại chỗ (container 4 lõi, `f8a7829`, `CONG_CU_TEST_TIEN_TRINH=2`, `PYTHONDONTWRITEBYTECODE=1`, dấu thời gian theo dòng):

| đoạn của `main()` | mốc (s) | thời lượng |
|---|---|---|
| 53 ca (`CA`) | 0 → 24,0 | 24,0 s |
| cổng trên cây thật | → 42,6 | 18,6 s |
| tự kiểm phân hạng + giàn giáo + song song (N126) | → 159,7 | 117,1 s |
| vòng bán kính 212 đột biến (2 tiến trình) | 159,7 → … | **đang đo lúc đóng băng** — số thật ghi vào evidence trên #668, không sửa spec |

Đo từng ca tuần tự trong một tiến trình: tổng 22,3 s; ba ca `t39` 3,38 s · `t28` 3,17 s · `t51` 2,76 s chiếm 42 %.
`_do_ban_kinh` chạy lại TRỌN `CA` cho mỗi đột biến ⇒ vòng bán kính ≈ 212 × (một lượt `CA`) / số tiến trình.

Hệ quả thiết kế (ƯỚC, từ CI): G5 45m56s trừ ~3 phút phần trước bán kính ⇒ vòng bán kính ≈ 43 phút ≈ 93 % bước G5, tức
≈ 212 × ~24 s / 2 tiến trình. Chỉ nhanh lên được bằng nhiều RUNNER. 8 mảnh ⇒ mỗi mảnh ≈ 43/8 ≈ 5,4 phút đo + một lượt
`CA` (~0,5 phút) + thiết lập (~1,5–2 phút) ≈ 7,5–8 phút — ước, không phải cam kết; A9 đo thật sau land.

## 2. Lệch có duyệt

- Trần ADR-0044 (`sensitive` ≤ 3 tệp, ≤ 300 dòng thêm) nâng lên **≤ 5 tệp, ~600 dòng thêm** — chủ kho 28-09.
  Vượt 600 dòng thêm ⇒ DỪNG, hỏi chủ kho.
- Số lượt Codex vượt trần 2 lượt §8 — chủ kho: "Lặp vá lỗi, cross review theo phân lớp, đăng verdict, tới khi hết
  P1, P2, P3."
- Không chạy CI trước land (không mở PR tới khi chủ kho báo) — chủ kho: "Không Ci, full CI, CI do lỗi đã biết".

## 3. Ngoài phạm vi

| thứ | lý do |
|---|---|
| tăng tốc từng ca (`t39`/`t28`/`t51`) | đổi hành vi ca; không cần cho mục tiêu |
| bán kính theo diff (mẫu #643) | chủ kho chọn "Chia mảnh mọi PR" — PR nào cũng đo ĐỦ |
| sửa `ops/bash_nen.py` (SyntaxWarning) | không được cấp |
| thêm context `gate-cong-cu-gop` vào ruleset | thao tác trên GitHub, chủ kho làm sau land (§7) |
| đổi `ci-dot-bien-du.yml` | bán kính ĐỦ đã chạy trên mọi PR và mọi push master; không cần lượt tuần riêng |

## 4. Write set — 5 đường

| # | đường dẫn | vì sao |
|---|---|---|
| W1 | `ops/cong_cu_test.py` | M1 chế độ gate · M2 chế độ mảnh · M3 chế độ gom · M4 ca tự kiểm + đột biến riêng |
| W2 | `.github/workflows/ci.yml` | M5 job `gate-cong-cu` + `gate-cong-cu-gop`; env bước G5 của `gate` |
| W3 | `.claude/dev/ci_dang_ky_test.py` | M6 `loi_g5_workflow` nhận hình dạng hai job mới (danh sách CHO PHÉP) + phản chứng `p*` |
| W4 | `.claude/dev/launcher_test.py` | M7 `t152` đếm `AL_VER:` trong ci.yml: 4 → 5 |
| W5 | `.claude/hooks/session-start.sh` | M7 chỉ chú thích "4 chỗ" → "5 chỗ"; không đổi lệnh nào |

## 5. Mục tiêu

| # | mục tiêu | đường |
|---|---|---|
| M1 | **Chế độ gate.** Vắng `CONG_CU_TEST_BAN_KINH` ⇒ hành vi cũ, không đổi (đo trọn bán kính tại chỗ). `CONG_CU_TEST_BAN_KINH=manh` ⇒ chạy `CA` + cổng cây thật + tự kiểm như cũ, KHÔNG chạy vòng bán kính, in một dòng nói rõ bán kính giao cho job mảnh + gom. Mọi giá trị khác (kể cả rỗng) ⇒ rc≠0 TRƯỚC khi chạy ca nào | W1 |
| M2 | **Chế độ mảnh.** `CONG_CU_TEST_MANH="k/N"` (khớp ĐÚNG `^(0\|[1-9][0-9]?)/([1-9][0-9]?)$`, `2 ≤ N ≤ 16`, `0 ≤ k < N`) + bắt buộc `CONG_CU_TEST_MANH_RA=<tệp>`; sai hình dạng, thiếu tệp ra, hay có cả `CONG_CU_TEST_BAN_KINH` ⇒ rc≠0 TRƯỚC khi chạy ca nào. Chạy `CA`; có ca ĐỎ ở nền hay tiền kiểm bị bỏ qua ⇒ rc≠0, không ghi tệp. Đo bán kính CHỈ các đột biến có chỉ số `i % N == k` trong `DOT_BIEN`, qua ĐÚNG đường tiến trình con hiện có (`--ban-kinh-con`) và ĐÚNG bộ nhận `_nhan_ket_qua_con`. Mảnh ĐẠT trọn (mọi bản ghi hợp lệ, 0 lỗi theo `_ket_luan_ban_ghi`) mới ghi tệp: dòng đầu `MANH <json>` (`phien_ban`, `manh`, `so_manh`, `sha256_test`, `head`), rồi đúng một dòng `BKCON <bản ghi>` cho mỗi đột biến của mảnh | W1 |
| M3 | **Chế độ gom.** `python ops/cong_cu_test.py --gop <thư mục>`: đọc MỌI mục trong thư mục; ĐẠT chỉ khi: mọi mục là tệp; đầu tệp đúng khoá và kiểu; cùng `so_manh = N`; đúng N tệp; tập `manh` = `{0..N-1}`; `sha256_test` và `head` BẰNG của chính tiến trình gom; bản ghi của mảnh k qua `_nhan_ket_qua_con` với nhóm = ĐÚNG phân hoạch k (tái tính từ `DOT_BIEN` của tiến trình gom); tổng bản ghi = `len(DOT_BIEN)`. Kết luận từng đột biến bằng CÙNG `_ket_luan_ban_ghi` mà đường song song dùng. ĐẠT ⇒ in `GOM MẢNH N/N`, bảng bán kính theo thứ tự `DOT_BIEN`, và dòng `SỐ LIỆU GOM: … đột biến=<len(DOT_BIEN)> · lỗi đột biến=0`; mọi lệch ⇒ rc≠0 kèm lý do | W1 |
| M4 | Mỗi chốt của M1/M2/M3 có ca tự kiểm (đi qua cửa tiến trình con đọc `TEP_TEST` để đột biến cắn được), và có đột biến RIÊNG trong `DOT_BIEN` gỡ đúng chốt ấy làm ca đích ĐỎ với bán kính 1. Không thêm đường phân hạng mới | W1 |
| M5 | `ci.yml`: bước G5 của `gate` thêm `env: CONG_CU_TEST_BAN_KINH: manh`. Job `gate-cong-cu` (`needs: chuan-bi`, matrix `os` từ `chuan-bi` × `manh: [0..7]`, `fail-fast: false`) chạy ĐÚNG phần thiết lập G5 của `gate`, rồi bước G5 mảnh (probe + selftest; `CONG_CU_TEST_MANH`/`_RA` qua `env`, không `${{ }}` trong `run`), rồi `actions/upload-artifact@v4` (`if-no-files-found: error`). Job `gate-cong-cu-gop` (`needs: gate-cong-cu`, `if: ${{ !cancelled() }}`, matrix `os`) tải về theo mẫu tên của CÙNG `os` rồi chạy `--gop` | W2 |
| M6 | `loi_g5_workflow` (danh sách CHO PHÉP): `gate` = [probe, selftest] + env ĐÚNG `{CONG_CU_TEST_BAN_KINH: manh}`; `gate-cong-cu` = [probe, selftest] + env ĐÚNG hai biến mảnh, matrix `manh` = đúng `0..N-1` khớp N trong `CONG_CU_TEST_MANH`; `gate-cong-cu-gop` = đúng một lệnh `--gop`, `needs` chứa `gate-cong-cu`, `if` ĐÚNG `${{ !cancelled() }}`, trước bước gom chỉ thiết lập + `download-artifact`; `gate` có env bán kính mà thiếu một trong hai job ⇒ ĐỎ | W3 |
| M7 | `t152` đòi 5 chỗ `AL_VER:` khớp hook; chú thích hook nói 5 chỗ | W4, W5 |

## 6. Nghiệm thu

| # | tiêu chí | phép đo làm ĐỎ |
|---|---|---|
| A1 | Tại chỗ: 8 lượt `CONG_CU_TEST_MANH=k/8` rồi `--gop` ⇒ `GOM MẢNH 8/8`, bảng bán kính đủ `len(DOT_BIEN)` dòng `ok`, `lỗi đột biến=0`, rc=0; tổng đột biến các mảnh = `len(DOT_BIEN)` | lượt nào rc≠0 hoặc số lệch |
| A2 | `--gop` ĐỎ với: thiếu một tệp · nhân đôi một mảnh · một tên chuyển sang mảnh khác · một tên bị xoá · `sha256_test` lệch · `head` lệch · `so_manh` lệch · đầu tệp hỏng · bản ghi hỏng · thư mục rỗng/không có | ca tự kiểm; đột biến gỡ từng chốt ⇒ ca ĐỎ |
| A3 | Chế độ mảnh: `8/8`, `0/1`, `a/8`, `01/8`, ` 0/8`, `0/17` ⇒ rc≠0 và không chạy ca nào; vắng `_RA` ⇒ rc≠0; có cả `CONG_CU_TEST_BAN_KINH` ⇒ rc≠0; phân hoạch N mảnh phủ đúng `DOT_BIEN`, rời nhau | ca tự kiểm + đột biến |
| A4 | Chế độ gate: `CONG_CU_TEST_BAN_KINH=manh` ⇒ không phóng tiến trình con bán kính nào, rc=0 trên nền xanh; giá trị lạ/rỗng ⇒ rc≠0 | ca tự kiểm + đột biến |
| A5 | Hành vi cũ (vắng mọi biến mới) vẫn ĐẠT: `cong_cu_test: N/N`, bán kính đủ, `lỗi đột biến=0` | rc≠0 |
| A6 | W3: `loi_g5_workflow` trên ci.yml thật = ĐẠT; ĐỎ với: gate có env bán kính mà thiếu job mảnh · thiếu job gom · gom không `needs` · gom không `if` hoặc `if` khác · matrix `manh` thiếu/thừa phần tử · `CONG_CU_TEST_MANH` sai N · env thừa/thiếu · lệnh G5 sai hình dạng | ca `p*` |
| A7 | Delta = 0 trên các bộ khác: `ci_dang_ky_test.py` (phần chung), `launcher_test.py` (`t152`), `lease_publish_test.py` (t24/t31/t35/t161/t162), `actionlint` trên ci.yml rc=0, ruff F delta = 0 cho W1/W3/W4 | đo hai vế cùng một lệnh |
| A8 | Cross-review Codex theo phân lớp, lặp tới 0 P1/P2/P3; verdict đăng lên #668 | — |
| A9 | Sau land (quan sát, không phải cổng land): trên PR đầu tiên sau land, `gate-cong-cu` ≤ 10 phút tường/mảnh, lượt CI tổng ≤ 15 phút; `gate-cong-cu-gop` in `GOM MẢNH 8/8` | — |

## 7. Nghĩa vụ sau land

- Chủ kho thêm context `gate-cong-cu-gop (ubuntu-latest)` vào ruleset `bao-ve-cong-dang-lease`. Trước lúc đó job gom
  ĐỎ làm workflow đỏ nhưng KHÔNG chặn merge.
- Bookkeeping theo tiền lệ #665: spec + lease vào master, thu hồi lease bằng rút hạn.

## 8. Ngân sách CI

`0 / 0 / 0` lượt trước land — chủ kho: "Không Ci, full CI, CI do lỗi đã biết". Mọi phép đo ở A1–A7 chạy tại chỗ.
Chi phí phút sau land (ước): +7 job setup mỗi lượt ubuntu so với nay; tổng phút tính tiền của G5 tăng ~15–20 phút
mỗi lượt đổi lấy thời gian tường. Trên master, matrix `os` nhân đôi số mảnh (ubuntu + windows).

## 9. Điều kiện dừng

S1 chạm đường ngoài W1–W5 · S2 CI đỏ vì packet (hiện không chạy CI) · S3 lặp Codex tới hết P1/P2/P3, dấu hiệu không
hội tụ (cùng hình dạng finding ≥ 3 lần) ⇒ hỏi chủ kho · S4 push chỉ sau review tại chỗ · S5 > 600 dòng thêm ·
S6 hết hạn lease ⇒ handoff §7.

## 10. `hinh_dang_ke_thua`

`khong_ap_dung` — không phải packet khắc phục. Kế thừa hình dạng mảnh + gom của #661 (`CI-DOT-BIEN-CHIA-MANH`) và
hợp đồng N129 của `cong_cu_test` (con chỉ gửi DỮ LIỆU ĐO, cha tự kết luận): tệp mảnh chứa đúng các bản ghi `BKCON`,
job gom kiểm bằng CÙNG bộ nhận của đường song song.

## 11. `chua_do_duoc`

- Thời gian thật của `gate-cong-cu`/`gate-cong-cu-gop` trên runner (chỉ A9, sau land).
- Hành vi `upload-artifact@v4`/`download-artifact@v4` khi thiếu tệp — chỉ đo được trên runner thật; job gom không
  dựa vào nó (thiếu mảnh ⇒ gom ĐỎ theo M3).
- Đường Windows của chế độ mảnh/gom: chỉ chạy trên master sau land (matrix `os`).
- Danh tính người ký lease (#566); effort thực tế của phiên executor.
