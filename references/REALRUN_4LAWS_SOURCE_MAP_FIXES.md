# v1.17.12 — fix sau lần chạy thật nhóm 4 luật

Lần chạy thật với webapp `2.21.2b` cho thấy tầng `ping/boot` đã ổn: manifest 728 nguồn / 673 corpus, index offline không rỗng. Lỗi mới không nằm ở boot mà ở **chọn nguồn rà soát** và vệ sinh registry. Bản v1.17.12 hợp nhất source-map hotfix, lớp `WARN/title_mismatch`, và guard tái sử dụng số VBHN theo năm.

## Fix trong skill

1. **Thêm `tl source-map`** để lập bản đồ nguồn rà soát theo VBHN-first. Lệnh này đọc manifest offline và:
   - nếu luật gốc/sửa đổi có VBHN liên quan trong trường `goc`, chọn VBHN;
   - nếu truy vấn theo tên có nhiều hit, cảnh báo không lấy hit đầu;
   - nếu luật cũ không thấy VBHN đã xác minh trong corpus, cảnh báo `NO_VERIFIED_VBHN_IN_CORPUS` + `QT5_WEB_REQUIRED`, không kết luận là không tồn tại;
   - nếu nhóm có root/orphan/metadata rỗng hoặc tên file/metadata lệch, cảnh báo chạy `hygiene plan`.

2. **Client-side canonical score đồng bộ tinh thần 2.21.2b**: VBHN là tiebreaker, bản hết hiệu lực/thay thế bị trừ điểm. Cờ `OMNIBUS_NARROW_TITLE_CHECK` không áp cho chính VBHN vì VBHN hợp lệ thường có nhiều văn bản gốc trong `goc`.

3. **Guard tái sử dụng số VBHN theo năm**: số như `14/VBHN-VPQH` không đủ định danh; phải verify ngày ban hành, tiêu đề và dòng hợp nhất. Tên trơ như `VBHN_14-VBHN-VPQH` bị flag `VBHN_BARE_NUMBER`; thiếu ngày/năm bị flag `VBHN_MISSING_YEAR_OR_DATE`.

3. **Giữ fix Unicode/NFC**: `tl extract --find` tìm chuỗi bằng NFC + casefold, tránh âm tính giả khi kiểm các cụm tiếng Việt.

4. **Giữ fix hygiene an toàn**: không parse số đầu của `Mẫu_/PL_/Phụ_lục` thành số hiệu, tránh quarantine nhầm biểu mẫu/phụ lục hợp lệ.

## Lệnh khuyến nghị

```bash
python scripts/tl.py --config config.json boot --json
python scripts/tl.py --config config.json source-map "74/2025/QH15" "41/2024/QH15" "84/2015/QH13" "Bảo hiểm y tế"
python scripts/tl.py --config config.json hygiene scan --json
```

## Không tự ghi

Gói này không tự move Drive/NLM. Các việc như gỡ bản gốc khỏi notebook hoặc move bản trùng vào QUARANTINE vẫn phải duyệt từng dòng rồi mới chạy `hygiene plan ... --apply --confirm yes`.

## Fixture kỳ vọng

- `74/2025/QH15` → chọn Luật Việc làm 74/2025, không cảnh báo thiếu VBHN ồn ào.
- `41/2024/QH15` → chọn VBHN 19-VPQH.
- `84/2015/QH13` → chọn luật 84/2015 và cảnh báo `NO_VERIFIED_VBHN_IN_CORPUS` + `QT5_WEB_REQUIRED`.
- `Bảo hiểm y tế` → chọn VBHN 40-VPQH; dòng `Luat_57-2024-QH15_Bao_hiem_y_te` nằm trong `risky_candidates` với `OMNIBUS_NARROW_TITLE_CHECK,TITLE_METADATA_MISMATCH`.
- `14/VBHN-VPQH` → cảnh báo `VBHN_NUMBER_REUSE_RISK`; không tin hit theo số hiệu trần nếu chưa verify đúng năm/chủ đề.
