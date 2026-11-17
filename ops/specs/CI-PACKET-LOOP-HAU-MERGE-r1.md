tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# CI-PACKET-LOOP-HAU-MERGE r1 — push nhánh mặc định chạy lại bộ ca packet-loop

- packet_id: CI-PACKET-LOOP-HAU-MERGE; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | #1353 |
| `nguon_cap_viec` | Chủ kho chọn "Đăng waiver + sửa M2" (AskUserQuestion phiên điều phối #1206, 17-11-2026 ~00:47Z) sau connector P1 PR #1351 r4593745939. |
| `review_class` | `sensitive` (cổng bắt buộc `gate-packet-loop`) |
| `base` | nhánh mặc định lúc cấp lease |

## 0. Vấn đề (đo 16/17-11-2026)

`ops/ci_duong_nhanh.py::phan_loai_packet_loop` (M2 của #1343) trả `bo_qua` cho MỌI `push` lên nhánh mặc định. Trên push `b8bc64f` (run 43969906464) và `e4cce23` (run 43975814762), job gom `gate-packet-loop (ubuntu-latest)` in `GOM: KHÔNG ĐO - packet_loop=bo_qua`, `gate-packet-loop-manh` `skipped`. Mốc §10.2.2 gate_output của mọi merge commit vì vậy thiếu dấu hiệu dương; ghi `owner_waived` thì cần waiver bền của chủ kho cho TỪNG SHA (§10.2.3). Từ #1343 mỗi mảnh ≤ 5 phút, 16 mảnh song song (CI PR 43929227587: mảnh chậm nhất 234 s).

## 1. `write_set`

```
ops/ci_duong_nhanh.py
ops/ci_duong_nhanh_test.py
```

## 2. `ngoai_pham_vi`

Không đổi logic `pull_request` (chỉ chạy khi diff chạm `PHU_THUOC_PACKET_LOOP`, fail-closed). Không sửa `.github/workflows/ci.yml`, `.claude/dev/packet_loop_test_manh.py`, `packet-loop-dot-bien.yml` (CA_DAI và bảng đột biến vẫn ở workflow đêm). Không xử lý nợ ghim dấu vân Windows (`chay-cong-windows_test.ps1`) hay `danh_gia_gate.py` của hồ sơ land.

## 3. `muc_tieu`

| # | mục tiêu |
|---|---|
| M1 | `push` (nhánh mặc định) ⇒ `packet_loop=chay`, lý do in rõ "push nhanh mac dinh: chay bo ca packet-loop hau merge". Mọi sự kiện khác `pull_request` vẫn `chay` (fail-closed) như cũ. |
| M2 | Cập nhật docstring/chú thích của `phan_loai_packet_loop` cho đúng hành vi mới, ghi nguồn quyết định (#1353). |
| M3 | Ca `t100` khẳng định push ⇒ `chay` (kể cả khi diff không chạm tập phụ thuộc, và khi diff rỗng). Đột biến `pl_push_van_chay` của #1343 không còn văn bản đích: thay bằng đột biến mới khôi phục nhánh `push ⇒ bo_qua`, phải làm `t100` ĐỎ. |

## 4. `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | `ops/ci_duong_nhanh_test.py` toàn bộ đạt (`TONG: DAT`), gồm `t100`–`t103`. | Khôi phục `if su_kien == "push": return PL_BO_QUA` ⇒ `t100` đỏ. |
| N2 | Bảng đột biến của `ci_duong_nhanh_test.py` (họ `pl_*` và mọi đột biến có đích `t100`) giết đúng ca; không còn đột biến mang văn bản đích đã mất. | Đột biến nào `khong khop` / sống ⇒ đỏ. |
| N3 | Ruff `--select F` delta 0 trên hai tệp; `adr-song`, `doctrine-scan` rc 0. | — |
| N4 | Hậu merge (đo trên chính merge commit): run `ci.yml` push có `gate-packet-loop-manh` chạy 16/16 mảnh và job gom in `GOM: ĐẠT`. | Gom in `KHÔNG ĐO` hoặc mảnh `skipped`. |

Chỉ chạy test nhắm đích; không chạy trọn `packet_loop_test.py` trên máy executor; không chạy Windows (chỉ đạo chủ kho).

## 5. Kích thước và trần

2 tệp, dự kiến ≤ 40 dòng thêm. Trần `ADR-0053`: ≤ 450.

## 6. `luat_dung`

Cần sửa tệp ngoài write set (vd. `ci.yml` vì job `gate-packet-loop-manh` không chạy trên push) thì DỪNG và báo kèm bằng chứng.

## 7. `chua_do_duoc`

N4 chỉ đo được sau merge.
