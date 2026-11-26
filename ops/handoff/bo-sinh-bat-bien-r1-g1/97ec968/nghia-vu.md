# Bảng nghĩa vụ §2–3 → mệnh đề → phản chứng — bo-sinh-bat-bien r1 g1, ứng viên 97ec968 (lượt 4)

Rà theo NGHĨA VỤ của đặc tả (mỗi giá trị miền bắt buộc), không chỉ theo mệnh đề trong mã. Cột "hàng bảng" trỏ `bang-toan-tu/bang.md`;
cột "phản chứng" là biến thể trong ca (tên đúng như trong mã). Mỗi hàng có ít nhất một phản chứng đỏ rc 3 đúng ca và một đối chứng xanh cùng đường.

| § | Nghĩa vụ (giá trị miền) | Mệnh đề chốt | Hàng bảng | Phản chứng (ca → biến thể) | Đối chứng xanh cùng đường |
|---|---|---|---|---|---|
| 2.1.1 | 128 ký tự ASCII trong vũ trụ c37 | `len(vu_tru) == 158`, `len(set(vu_tru)) == 158` | `mien.ascii_c37` (cong1, tru1, cat), `c37.tong`, `c37.khac_nhau` | c39 → bản nguyên vẹn đòi đúng 648 ô (mọi sai lệch ASCII làm nó đỏ) · `Lu thành ASCII 'A'` | c39 `nguyên vẹn` (648 ô) |
| 2.1.1 | mỗi category trừ Cs ĐÚNG MỘT đại diện (29) | `not lech`, `lech = [... bmp.count(loai) != (loai != "Cs")]` | `c37.category`, `c37.lech`, `mien.LOAI` | c39 → `bỏ <loai>` × 29 · `lặp category Ll` · `Mn thành bản sao Mc` · `Mn thành ký tự Mc KHÁC` | c39 `nguyên vẹn` |
| 2.1.1 | đúng một ký tự ngoài BMP | `len(vu_tru) == 158` + `lech` (đếm phần BMP) | `c37.bien_bmp`, `c37.phan_bo_sinh` | c39 → `bỏ ký tự ngoài BMP` · `thừa một ký tự ngoài BMP` · `lặp CHÍNH ký tự ngoài BMP cuối` · `ngoài BMP thành U+FFFF` | c39 `ngoài BMP thành U+10000` (648 ô) |
| 2.1.1 | không ký tự nào thuộc CR/LF ở phần ngoài ASCII | `len(set(vu_tru)) == 158` (CR, LF đã có trong 128 ASCII) | `c37.khac_nhau` | c39 → `Lu thành ASCII 'A'` (cùng cơ chế: ký tự ASCII lọt vào phần bộ sinh) | c39 `nguyên vẹn` |
| 2.1.2 | số ô là hằng 648, cả hai chiều | `len(o) == 648` | `c37.so_o` | c39 → `c37 mất một ô rời` (647) · `c37 thừa một ô rời` (649) | c39 `bản sao nguyên vẹn` (648 ô) |
| 2.1.3 | hai chốt chạy TRƯỚC vòng ô | thứ tự trong c37 | — (thứ tự, không phải toán tử) | c39 đòi MỌI phản chứng 0 ô | c39 bản nguyên vẹn 648 ô |
| 2.2.1 | số phần tử qua L8 BẰNG ĐÚNG kỳ vọng, cả hai chiều, tám ca | `dem[0] - truoc == mong` | `c36.so_phan_tu`, `c36.cong_thuc` | c40 → `bỏ Mn` (a129, thiếu) · `mất một ô cấu trúc` (a129, thiếu) · `thêm một bản sao ô đầu` (a126, thừa) | c40 `nguyên vẹn` a126 · a129 · a131 |
| 2.2.1 | sàn `A_CA` bị thay, không giữ song song | (không còn sàn) | — | (đã kiểm ở lượt 1; không còn mã) | — |
| 2.2.1 (R1-02) | một ô cấu trúc bị thay bằng BẢN SAO ô khác | `len(van_tay) == mong - lap` | `c36.khac_nhau` | c40 → `ô khong khop thành bản sao ô đầu` (a129) · `một ô rời thành bản sao ô đầu` (a126) · `Mn thành bản sao Mc` (a126) · `nguyên vẹn, kỳ vọng gặp lại +1` (chiều thừa) | c40 `nguyên vẹn` a126 · a129 |
| 2.2.2 | tập category của phần tử đã qua L8 chứa tập bắt buộc | `not thieu` | `c36.category` | c40 → `Mn thành ký tự Mc KHÁC` (a126) | c40 `nguyên vẹn` a126 |
| 2.2.2 | có ít nhất một ký tự ngoài BMP | `any(ord(c) > 0xFFFF ...)` | `c36.ngoai_bmp` | c40 → `ngoài BMP thành U+FFFF` (a126) | c40 `ngoài BMP thành U+10000` (a126) |
| 2.2.2 | chỉ ca CÓ dùng bộ sinh mới chịu hai chốt trên | `if tru is not None` | `c36.nhanh_mien` (bo, dao, yeu) | c40 → `Mn thành ký tự Mc KHÁC` (nhánh bị tắt) · a131 nguyên vẹn (nhánh bị ép mở ⇒ c36 rc 4 ⇒ c40 đỏ rc 3) | c40 `nguyên vẹn` a131 |
| 2.2.3 | c38 giữ 24/24 | (ca cũ, không đổi) | — | c38 | c38 sổ nguyên vẹn |
| 2.3.1 | đúng năm bộ đối số của bảng mục 1 (danh tính, không chỉ số đếm) | `sorted(goi) == mien`, `len(mien) == 5`; `_mien_doi_so` đọc AST độc lập | `a135.mien_doi_so` ×2, `a135.ghi_loi_goi`, `a135.doc_mien`, `a135.vong`, `mien.BO_SINH_MONG` | a136 → BO_SINH_MONG `bo bo 4` · `bo bo 5` · `bo 5 thanh ban sao bo 2` · `thua ban sao bo 1` · `ca dung sau bo` | a136 `ban sao nguyen ven` |
| 2.3.1 | MỖI bộ đối số thực sự được kiểm (không bị vòng lặp bỏ qua) | vòng `for … in BO_SINH_MONG` + sáu mệnh đề từng bộ | `a135.vong` (cat, tru1, dao), `a135.chot_cuoi` | a136 → `chi sai o bo 0` … `chi sai o bo 4` (mỗi bộ một bộ sinh giả chỉ sai tại đúng bộ ấy) | a136 `that` |
| 2.3.1 | số phần tử từng bộ | `len(ra) == so` | `a135.so_phan_tu` | a136 → `bo Mn` · `thua mot ngoai BMP` · `rong` | a136 `that` |
| 2.3.1 | tập category vắng từng bộ (30 category) | `sorted(set(LOAI_UNICODE) - set(bmp)) == sorted(vang)` | `a135.category_vang`, `mien.LOAI_UNICODE` | a136 → `bo Mn` · `bo loc bo_loai` · `Mn thanh ban sao Mc` | a136 `that` |
| 2.3.1 | không lặp category | `len(bmp) == len(set(bmp))` | `a135.lap_category` | a136 → `Mn thanh ban sao Mc` · `Lu thanh U+007F` | a136 `that` |
| 2.3.1 | không phần tử nào thuộc `cam` | `not any(c in cam ...)` | `a135.thuoc_cam` | a136 → `bo loc cam` | a136 `that` |
| 2.3.1 | mọi đại diện từ U+0080, hai phía biên | `all(ord(c) >= 0x80 ...)` | `a135.tu_0080` | a136 → `Lu thanh ASCII` · `Lu thanh U+007F` | a136 `that` |
| 2.3.1 | phần tử cuối ngoài BMP và là ngoài BMP duy nhất, hai phía biên | `bool(ra) and ord(ra[-1]) > 0xFFFF and len(ra) - len(bmp) == 1` | `a135.cuoi.*`, `a135.bien_bmp` | a136 → `bo ngoai BMP` · `thua mot ngoai BMP` · `ngoai BMP len dau, cuoi la U+FFFF` · `rong` | a136 `cuoi la U+10000` |
| 2.3.1 | gom lý do lệch đúng | `if not dat`, `bang(not lech, …)` | `a135.gom`, `a135.chot_cuoi` | a136 → mọi biến thể đòi ĐÚNG danh sách mệnh đề lệch | a136 `that` |
| 2.3.2 | phép kiểm nhận bộ sinh làm tham số | `kiem_bo_sinh(bo_sinh)` | `a135.nho_dem` (khoá theo hàm) | a136 → mọi bộ sinh giả (nếu nhớ đệm che bộ sinh giả thì `chi sai o bo 0` xanh ⇒ a136 đỏ) | a136 `that` |
| 3 P1–P7 | bảy phản chứng là ca | — | — | c39 · c40 · a136 (bảng phản chứng `phan-chung/bang.md`) | — |

## Ngoài bảng, khai rõ

- Toán tử ngoài tập cố định và ngoài dữ liệu miền đã liệt kê (vd. đổi tên biến, đổi thứ tự hai chốt, hằng +2): không phủ.
- Một ô cấu trúc bị thay bằng một ô KHÁC không trùng ô nào: ngoài miền đặc tả (§8; reviewer lượt 2 và lượt 3 xếp như vậy).
- Phép so bên trong chính ca phản chứng (c39/c40/a136): thứ canh chúng là công cụ bảng (bỏ phép so của c40 ⇒ mọi ô `c36.*` thành SỐNG); reviewer lượt 3 đồng ý không đòi đệ quy.
- `a135.cuoi.khong_rong` / `bo`: bộ sinh rỗng làm a135 vỡ IndexError (rc 4) và a136 bắt sai hợp đồng rc 3 — đó là a136 giết, KHÔNG phải a135 đỏ đúng chốt (reviewer lượt 3 đã ghi).
