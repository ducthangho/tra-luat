# Rà soát Bộ luật Lao động + Nhật ký sự cố skill

*Phiên chạy: 27/06/2026 · skill tra-luat v1.22.14 · webapp 2.21.2i (LIVE).*
*Chế độ: fallback webapp GAS (TL_WEBAPP/TL_TOKEN) — KHÔNG có `tl_secrets.enc` nên gws/direct-media không khởi tạo; lệnh lõi vẫn chạy qua GAS.*

---

## PHẦN A — Kết quả rà soát chồng chéo

**Nguồn canonical (VBHN-first):** `VBHN_18-VBHN-VPQH_2026_Bo_luat_Lao_dong` — sohieu `18-VBHN-VPQH`, cat `20_Lao_dong`, còn hiệu lực, đã nạp NLM. GDoc `1gJn-6pjj2IMUU0F4K2HNV6L9f73YfSHHjUH2ZICPxos`.
**Công cụ:** `tl rasoat-chongcheo` (E1) · `tl footnote-map` (B3). Điều khoản verify từ cache; E1 chỉ dựng tập liên quan + kiểm hiện diện.

### 1. Cụm `lao_dong_xa_hoi` — 8 luật liên quan, đủ trong corpus (thiếu=0, pending=0)

| Lĩnh vực giao thoa | Canonical | Hiện diện |
|---|---|---|
| Bảo hiểm xã hội | 19/VBHN-VPQH (2026) | ✓ |
| Bảo hiểm y tế | 40/VBHN-VPQH (2026) | ✓ |
| An toàn, vệ sinh lao động | 14/VBHN-VPQH (2024) | ✓ ⚠ trùng số hiệu |
| Việc làm | 74/2025/QH15 | ✓ |
| Công đoàn | 90/VBHN-VPQH (2025) | ✓ |
| Giáo dục nghề nghiệp | 124/2025/QH15 | ✓ |
| NLĐ Việt Nam đi làm việc ở nước ngoài | 8/VBHN-BNV (2026) | ✓ |
| Dân số | 113/2025/QH15 | ✓ |

### 2. Điểm sửa đổi cấp Điều (footnote-map B3) — 5 điểm, 1 PENDING

| Điều/Khoản BLLĐ | Luật sửa | Hiệu lực | Loại |
|---|---|---|---|
| Điều 59 K2 | 124/2025/QH15 (GDNN) — điểm a K1 Đ43 | 01/01/2026 | sửa đổi |
| Điều 61 K3 | 124/2025/QH15 (GDNN) — điểm b K1 Đ43 | 01/01/2026 | sửa đổi |
| Điều 139 K1 | 113/2025/QH15 (Dân số) — K1 Đ29 | **01/07/2026 ⏳ PENDING** | sửa đổi |
| Điều 154 K8a | 71/2025/QH15 (CN công nghệ số) — K4 Đ49 | 01/01/2026 | bổ sung |
| Điều 217 K3 | 71/2025/QH15 — K1 Đ44 | 01/01/2026 | sửa đổi |

### 3. Đánh giá

Các giao thoa là **dẫn chiếu liên thông + phân định phạm vi, KHÔNG xung đột quy phạm**:
Điều 59/61 đồng bộ thuật ngữ với Luật GDNN; Điều 154 mở rộng diện miễn GPLĐ (không mâu thuẫn); Điều 217 điều chỉnh kỹ thuật. **Rủi ro thực chất duy nhất** là độ trễ hiệu lực **Điều 139 K1** (nghỉ thai sản con thứ hai lên 7 tháng) — **hiệu lực 01/07/2026, hôm nay 27/06/2026 chưa áp dụng** (còn 4 ngày); bản VBHN đã chèn nội dung mới nhưng tới ngày đó bản 6 tháng cũ mới hết hiệu lực.

### 4. Cảnh báo vệ sinh registry (do skill phát hiện)

- `Luat_45-2019-QH14` (bản gốc) còn cờ `NLM_STATUS_MISMATCH` + `OMNIBUS_NARROW_TITLE_CHECK` → ứng viên giải phóng slot vì đã có VBHN 18 thay thế.
- `14/VBHN-VPQH` (ATVSLĐ) ⚠ TRÙNG-SỐ-HIỆU (số hiệu VBHN tái dùng theo năm).
- `VBHN_18-VPQH` (thiếu năm, cờ `VBHN_MISSING_YEAR_OR_DATE`) đã được cách ly đúng.
- `relation-check` trả ứng viên nhiễu (vd `108/2026/NĐ-CP` về giáo dưỡng) — KHÔNG thực sự sửa BLLĐ, bỏ qua.

---

## PHẦN B — Các vấn đề với skill trong quá trình chạy

Xếp theo mức nghiêm trọng. Phần lớn là **hỏng file do mount** (NUL-pad / cắt cụt), không phải lỗi logic skill.

### B1. Thiếu `tl_secrets.enc` → bootstrap crash
`python scripts/tl.py bootstrap --env cowork --secrets-file ./tl_secrets.enc` ném `FileNotFoundError: './tl_secrets.enc'`. File này KHÔNG có trong thư mục Context (dù bootstrap doc yêu cầu). Hệ quả: không khởi tạo được gws binary/cred, NLM cookie, direct-media. **Workaround:** chạy fallback webapp GAS — lấy `TL_WEBAPP` + `TL_TOKEN` từ `tra_luat_config.v2.json`, export env. Lệnh lõi (source-map/cluster/footnote-map/rasoat-chongcheo/relation-check) chạy đầy đủ qua GAS.

### B2. `tl.py` bản Context bị CẮT CỤT THẬT (nghiêm trọng)
Bản trong Context: 337,287 B / 5630 dòng — **mất ~15 dòng cuối** (đứt giữa định nghĩa `_CREDS_LAZY_CMDS`, cụt ở "# tự lo cre", thiếu cả khối `main()` dispatch). Biên dịch → `SyntaxError: '{' was never closed`. Cơ chế **self-heal NUL của skill KHÔNG cứu được** vì đây là **mất byte thật**, không phải NUL-pad (đúng như comment trong `_selfheal_module`).

### B3. Mount trả nội dung KHÔNG NHẤT QUÁN
`bootstrap`/`ping`/`boot` chạy được ở 1–2 lần gọi đầu (traceback tham chiếu **dòng 5645** = bản ĐỦ), nhưng các lần đọc sau lại ra bản **5630 dòng** (cụt) → `source-map` fail. Cùng một file, cùng mtime, đọc ra độ dài khác nhau → mount không ổn định (đúng lớp lỗi mà self-heal được sinh ra để chống, nhưng chỉ chống được NUL).

### B4. Bản skills-plugin (read-only) nhiễm NUL
`tl.py` ở mount skills đủ dài (342,960 B) nhưng chứa **5,692 NUL byte** → `ValueError: source code string cannot contain null bytes`. Sau khi strip NUL thì compile OK (337,268 B). Đây là bản ĐỦ DÀI duy nhất dùng được cho `tl.py`.

### B5. Hỏng CHÉO giữa hai bản — phải ghép từng file
Không bản nào nguyên vẹn toàn bộ:
- skills copy: `tl.py` đủ (sau strip NUL) nhưng `tl_gws.py`, `nlm_cli.py`, `secret_guard.py` cắt cụt thật (unterminated string / thiếu indented block).
- Context copy: các file đó nguyên, nhưng `tl.py` cụt.
**Workaround:** dựng thư mục mirror ghi được, với mỗi `.py` chọn bản (Context hoặc skills, đã strip NUL) **compile được** → toàn bộ tree compile sạch. Đây chính là phương án skill tự khuyến nghị ("mirror scripts/ sang thư mục ghi được + strip NUL rồi chạy lại").

### B6. `references/subject_clusters.json` cắt cụt → `tl cluster` hỏng âm thầm
Bản skills: 814 B (JSON hỏng, đứt giữa chuỗi note). Bản Context: 1058 B (đủ). JSON hỏng khiến `tl cluster` trả `{"clusters": {}}` **không báo lỗi** — dễ kết luận nhầm "không có cụm". Sau khi thay bằng bản Context, cụm `lao_dong_xa_hoi` xuất hiện và `rasoat-chongcheo` chạy đủ.

### B7. `tl cluster "<text>"` không khớp free-text
Dù cụm `lao_dong_xa_hoi` đã có, `tl cluster "lao động xã hội"` / `"pháp luật về lao động"` vẫn trả "không có ánh xạ cụm". Lệnh đòi đúng key, trong khi `rasoat-chongcheo` resolve đúng cụm. Gây hiểu nhầm — nên dùng `rasoat-chongcheo` trực tiếp.

### B8. `tl bootstrap` nuốt exit code
Lệnh traceback nhưng vẫn trả `EXIT 0` → script gọi tự động dễ tưởng thành công.

### B9. `.pyc` cache lệch phiên bản Python
`scripts/__pycache__/*.pyc` biên cho **cpython-313** trong khi sandbox chạy **Python 3.10.12** → Python bỏ qua, biên dịch lại từ source mỗi lần (nên lỗi cắt cụt mới lộ ra). Không gây hại nhưng vô dụng.

### B10. gws không khả dụng (đúng thiết kế)
`footnote-map` in `[FALLBACK→GAS] op=read backend=gws lỗi: gws not available (PATH/version/auth)` rồi tự lùi về GAS và cho kết quả đúng. Đây là fallback có chủ đích do thiếu secrets (B1), không phải lỗi.

---

### Khuyến nghị
1. **Cấp lại `tl_secrets.enc`** vào thư mục Context (hoặc nạp master key) để dùng gws/direct-media thay vì chỉ GAS.
2. **Re-sync skill** để vá file cắt cụt/NUL — hiện cả hai mount đều hỏng từng phần; phải ghép mirror thủ công mới chạy được.
3. Thêm guard cho `tl cluster`: báo lỗi rõ khi `subject_clusters.json` không parse được, thay vì trả cụm rỗng im lặng.
4. Sửa exit code của `bootstrap` để phản ánh đúng traceback.
