tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# N2-1342-GHIM-MERGE r1 — phép so byte N2 của #1342 r1 ghim đầu head vào merge commit, không đọc cây làm việc

- packet_id: N2-1342-GHIM-MERGE; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | #1365 |
| `nguon_cap_viec` | Chủ kho 17-11-2026 trong phiên điều phối #1206: "Đồng ý, mở micro-packet ghim lại N2 đi". Nợ của #1342 r1 (PR #1363, merge `ded5d41b1754ef05d87815f20c48203e6b00e58d`), executor báo khi bàn giao. |
| `review_class` | `sensitive` (bộ test của runtime WP1174) |
| `base` | nhánh mặc định lúc cấp lease |

## 0. Hiện trạng (đo 2026-11-17T08:17Z trên master `ded5d41`)

`.claude/dev/packet_loop_test.py`: `_BASE1342 = "14f7dd3a…"` (dòng 16567); `_additive_case1342` (16620) lấy `base = git show _BASE1342:.claude/dev/packet_loop.py`, `head = c.script.read_bytes()` — tức CÂY LÀM VIỆC; rồi `_additive1342(base, head) == []` (N2: chỉ thêm) và `_wired1342(head) == []` (N3: không nối dây), cùng mười phản chứng N2 dựng từ `head` và ba phản chứng N3. Blob `ded5d41:.claude/dev/packet_loop.py` = blob `675c38d:` (head đã audit của PR #1363), sha256 `e9012dbe2569953d4d0ae5472e4b13a8893cbedc6664e93f35e975c4ae15c40b`; cha thứ nhất của `ded5d41` là `14f7dd3`.

Hệ quả: sau land, bất kỳ thay đổi nào ở một định nghĩa có sẵn của `packet_loop.py` làm vế N2 ĐỎ dù mã đúng.

## 1. `write_set`

```
.claude/dev/packet_loop_test.py
```

## 2. `ngoai_pham_vi`

Không sửa `.claude/dev/packet_loop.py`. Không đổi `_additive1342`, `_wired1342`, `_new1342`, danh sách phản chứng, hay vế N3 (vẫn đo cây làm việc — r2 nối dây sẽ tự sửa vế ấy trong write set của nó). Không đổi ca khác.

## 3. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | Thêm hằng `_HEAD1342 = "ded5d41b1754ef05d87815f20c48203e6b00e58d"` (merge commit của PR #1363, chú thích nói vì sao). Trong `_additive_case1342`, `head` cho vế N2, cho tập `moi` và cho mười phản chứng N2 lấy từ `git show _HEAD1342:.claude/dev/packet_loop.py`, cùng chốt "thiếu object ⇒ ĐỎ, không thay bằng HEAD/merge-base" như `_BASE1342`. Vế N3 (`_wired1342`) đo trên cả blob ghim lẫn cây làm việc. | `.claude/dev/packet_loop_test.py` |

## 4. `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | Trên head: `wp1342_additive_byte_preserved` đạt; `wp1342_pure_platform_path` và 84 ca `wp1174_*` đạt (CI Ubuntu, gom `GOM: ĐẠT`). | Ca đỏ. |
| N2 | Bẫy đã gỡ: trong bản sao tạm của head, sửa một ký tự trong thân `_1174_read` của `packet_loop.py` (cây làm việc) ⇒ ca `wp1342_additive_byte_preserved` vẫn ĐẠT. Trên base (`ded5d41`) cùng thao tác ⇒ ca ĐỎ (tái lập bẫy). Ghi cả hai vào thân PR. | Head ĐỎ sau thao tác. |
| N3 | Răng còn nguyên: đổi `_HEAD1342` sang một OID khác (ví dụ `14f7dd3…`) ⇒ ca ĐỎ; đổi sang OID không tồn tại ⇒ ĐỎ với chẩn đoán "KHÔNG ĐO ĐƯỢC". Chèn `_1174_win_read(path)` vào thân `_1174_read` của cây làm việc ⇒ ca ĐỎ (N3 vẫn đo cây làm việc). | Một trong ba thao tác mà ca vẫn ĐẠT. |
| N4 | Ruff `--select F` delta 0; `adr-song`, `doctrine-scan` rc 0; `git diff --check` sạch; `git diff --numstat base..H` 1 tệp, ≤ 40 dòng thêm. | Gate thất bại. |

Chỉ chạy test nhắm đích; không chạy trọn `packet_loop_test.py`. Không cần đo Windows (ca chỉ đọc blob git, không có nhánh nền).

## 5. `pham_vi_e`

Không chạm E4, E5; không đảo quyết định của chủ kho.

## 6. `luat_dung`

Trần lời gọi Codex theo dòng khai `ADR-0055`, trần vòng theo `ADR-0048`; chạm trần ⇒ Review Rescue Checkpoint, xin tăng mang **E2**. Cần sửa ngoài write set ⇒ dừng, **E1**.

## 7. `hinh_dang_ke_thua`

Packet khắc phục của #1342 r1. Hình dạng lỗi: "tiêu chí PR-time viết thành ca test thường trực đo cây làm việc" — lần 1 (#1342 r1, ca N2). Chưa lặp.

## 8. `chua_do_duoc`

Không có.
