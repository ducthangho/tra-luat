# Đặc tả packet LAND-EVIDENCE-KHAI-PHAI-CO-NGUON — r3 (đợt g2, siết mẫu)

Đặc tả đóng băng. Sửa tệp này là đổi băm; muốn đổi thì soạn r4, không sửa đè. Soạn bởi phiên Claude Code
`session_017khPoiSXW9Yvefabg6MWaH` ngày 18-10-2026. r3 **không thay** r1 (`063ccaa6…`) và chỉ sửa **một** điểm của r2
(`ops/specs/land-evidence-khai-phai-co-nguon-r2.md`, sha256 `c70c19b57ad1d9bf0304a04bbb259b0b74ebc366824c24597c7207b7beaf14a0`):
**mẫu của dòng `MOI`** (Q1-r2). Mọi điều khác của r2 giữ nguyên: một dòng, cùng tệp, cùng nhánh, cùng điều kiện xong packet,
cùng bảng nghiệm thu. Chủ kho chấp nhận bằng comment cấp/gia hạn lease neo băm tệp này.

## packet_id · packet_issue

- `packet_id`: `land-evidence-khai-phai-co-nguon`
- `packet_issue`: [#773](https://github.com/ducthangho/tra-luat/issues/773)
- `revision`: 3

## vi_sao_co_r3 (đo được, không suy)

Review Codex CLI trên head #778 `128b2e8` (F1/P2): mẫu r2 tự mâu thuẫn với chính dòng `mẫu` trong bảng nghiệm thu r2 ("đầu
ra hỏng KHÔNG khớp"). `bang_chung_xanh` (`re.search(mau, text, re.M)`) nhận mẫu r2 cho các đầu ra hỏng sau, đo bằng chính hàm ấy
trên đầu ra thật của `ops/land_evidence_nguon_test.py`:

| Đầu ra | Mẫu r2 | Mẫu r3 |
|---|---|---|
| thật (`CA: 14/14` … `TONG: DAT`) | qua | qua |
| `DOT BIEN: 36/37` (một đột biến sống) | **qua** | trượt |
| nối `TONG: DO` sau tổng kết | **qua** | trượt |
| `TONG: DO` trước tổng kết | **qua** | trượt |
| `TU KIEM PHAN HANG: DO` | **qua** | trượt |
| dòng log thừa sau `TONG: DAT` | **qua** | trượt |
| `CA: 13/14`, `CA: 0/0`, `DOT BIEN: 0/0`, `TONG: DO`, thiếu dòng `DOT BIEN`, đảo thứ tự | trượt | trượt |

Bộ chạy gộp stdout+stderr (`stderr=STDOUT`, `text=True`): đầu ra thật gộp vẫn qua mẫu r3.

## quyet_dinh

- **Q1-r3 — mẫu:** dòng `MOI` của `ops/land_evidence_nguon_test.py` dùng
  `r"(?ms)\A(?!.*^(?:TONG|TU KIEM PHAN HANG): DO\b).*^CA: ([1-9]\d*)/(\1) dat\nDOT BIEN: ([1-9]\d*)/\3 bi giet dung ly do\nTU KIEM PHAN HANG: DAT \(\d+ dot bien\)\nTONG: DAT\n?\Z"`.
  Mẫu có **ba** nhóm bắt, nên `bang_chung_xanh` bỏ qua phép so `N == N` của nó; thay vào đó chính mẫu ép `CA: N/N` và
  `DOT BIEN: M/M` bằng backreference (`(\1)`, `\3`), ép N, M > 0, ép bốn dòng tổng kết liền nhau ở CUỐI đầu ra, và cấm mọi dòng
  `TONG: DO`/`TU KIEM PHAN HANG: DO`. Vẫn đúng một dòng thêm vào `MOI`, 0 dòng xoá.
- **ngoai_pham_vi r3:** bộ kiểm sổ đăng ký (`ci_dang_ky_test.py` không `--chay`) không phát hiện một mẫu `MOI` sai/quá rộng —
  đúng cho MỌI mục `MOI`, không riêng mục này. Không sửa ở packet #773; chỉ ghi nợ.

## nghiem_thu (g2, thay hàng `mẫu` của r2)

| Mục | Tiêu chí | Phép đo làm ĐỎ |
|---|---|---|
| mẫu | Mẫu r3 khớp đầu ra thật (gộp stdout+stderr); MỌI hàng "trượt" ở bảng trên đều trượt khi đo bằng `bang_chung_xanh`. | Một đầu ra hỏng qua. |
