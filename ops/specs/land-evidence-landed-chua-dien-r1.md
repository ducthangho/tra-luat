# Đặc tả packet LAND-EVIDENCE-LANDED-CHUA-DIEN — r1

Đặc tả đóng băng. Sửa tệp này là đổi băm; muốn đổi thì soạn r2, không sửa đè. Soạn bởi phiên Claude Code
`session_01FBUBzbedsJaUtQvX4vEYDE` ngày 19-10-2026, theo chỉ thị chủ kho trong phiên ("Đồng ý làm 1, 2 …", mục 2).

## packet_id · packet_issue

- `packet_id`: `land-evidence-landed-chua-dien`
- `packet_issue`: [#845](https://github.com/ducthangho/tra-luat/issues/845)
- `revision`: 1

## vi_sao_co (đo được, không suy)

- PR #840 (hồ sơ land của #831) có một head `473d56a` mang `trang_thai_packet.landed: true` trong khi `post_merge_checks`,
  `bookkeeping`, `lease.thu_hoi_cuoi`, `trang_thai_packet.landed_dieu_kien`, `ho_qua_cho_802` là CHUỖI `'CHO_DIEN — …'`.
  Codex connector bắt được (review comment 4309577154, P1). Không cổng nào bắt: `ops/land_evidence_nguon.py` đo token nguồn
  của lời khai `measured`, không đo phần hoàn tất có tồn tại hay không.
- PR #840 merge ở `ef81b98` (khi ấy `landed: false`, vẫn còn 8 chuỗi `CHO_DIEN`). Bản đầy đủ phải đi qua PR #842.
- Đo 19-10-2026 trên `9f4a539` (cây thật): 12 hồ sơ KHÔNG thuộc miễn trừ cutover. Mọi hồ sơ trong số đó có
  `trang_thai_packet.landed` kiểu `bool`; mọi hồ sơ `landed: true` có `post_merge_checks` và `bookkeeping` là danh sách
  mapping khác rỗng; 0 chuỗi chứa `CHO_DIEN`. **5/9 hồ sơ `landed: true` KHÔNG có `lease.thu_hoi_cuoi`** (pr778, pr791, pr793,
  pr800, pr801) ⇒ trường ấy KHÔNG được đòi (đòi là đỏ ngay cây thật).

## quyet_dinh

- **Q1 — luật L6 (một luật mới, cùng tệp):** chỉ áp khi `trang_thai_packet` là mapping CÓ khoá `landed`.
  1. `landed` không phải `bool` ⇒ ĐỎ (`'true'`, `1`, `null` đều ĐỎ — không đoán ý).
  2. `landed: true` ⇒ `post_merge_checks` VÀ `bookkeeping` mỗi cái phải là `list` khác rỗng mà MỌI phần tử là mapping.
     Đây là phần DANH SÁCH CHO PHÉP: kiểm KIỂU, không đoán chuỗi giữ chỗ — ca #840 (chuỗi đứng chỗ danh sách) bị bắt dù
     chuỗi ấy viết thế nào.
  3. `landed: true` ⇒ không chuỗi nào (khoá hoặc giá trị, mọi độ sâu, qua `duyet`) chứa `CHO_DIEN`. Đây là quy ước dấu của
     kho (bổ sung, không thay cho điểm 2): bắt ô giữ chỗ nằm trong trường kiểu chuỗi mà điểm 2 không phủ.
  4. `landed: false` ⇒ L6 không đòi gì: bản nháp được phép có ô giữ chỗ.
- **Q2 — miễn trừ:** hồ sơ băm khớp `MIEN_TRU_CUTOVER` vẫn bỏ qua như cũ (L5 không đổi, danh sách không đổi).
- **Q3 — kích thước:** ≤ 2 tệp, ≤ 150 dòng thêm.
- **Q4 — review:** Codex CLI qua `.claude/dev/launcher.py run`, tối đa 3 lời gọi.

## write_set

- `ops/land_evidence_nguon.py`
- `ops/land_evidence_nguon_test.py`

## ngoai_pham_vi

- Không đòi `lease.thu_hoi_cuoi`, `landed_dieu_kien`, `landed_ly_do` (cây thật không đồng nhất; muốn đòi thì r2 kèm sửa hồ sơ).
- Không kiểm dấu giữ chỗ trong CHÚ THÍCH YAML (parser bỏ chú thích).
- Không phủ hồ sơ để `trang_thai_packet` ở dạng không-mapping hoặc đặt `landed` ở chỗ khác.
- Không sửa hồ sơ nào; không đổi CI (bộ test đã đăng ký trong `ci_dang_ky_test.py`, định dạng dòng tổng kết giữ nguyên).

## nghiem_thu

| Mục | Tiêu chí | Phép đo làm ĐỎ |
|---|---|---|
| ca #840 | Hồ sơ `landed: true` + `post_merge_checks`/`bookkeeping` là chuỗi ⇒ rc=1, dòng `L6`. | rc=0. |
| bản nháp | `landed: false` + chuỗi `CHO_DIEN` ở các trường ấy ⇒ không có vi phạm `L6`. | Có `L6`. |
| kiểu | `landed: 'true'` ⇒ ĐỎ `L6`. Danh sách rỗng, phần tử không-mapping, thiếu `bookkeeping` ⇒ ĐỎ `L6`. | Một ca qua. |
| dấu | `landed: true`, danh sách hợp lệ, một chuỗi chứa `CHO_DIEN` ⇒ ĐỎ `L6`. | rc=0. |
| cây thật | `python ops/land_evidence_nguon.py --root .` vẫn rc=0. | rc≠0. |
| răng | Mỗi điểm 1–4 của Q1 có ít nhất một đột biến riêng, giết bằng `TinHieuChotCa`. Bộ test: `CA: N/N`, `DOT BIEN: M/M`, `TONG: DAT`. | Một đột biến sống / tín dụng giả. |
