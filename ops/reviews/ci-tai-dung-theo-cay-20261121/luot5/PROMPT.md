# Review đặc tả lượt 5 — `CI-TAI-DUNG-THEO-CAY-A` r4, `-B1` r4, `-B2` r4

Bạn là reviewer độc lập (họ model OpenAI; người soạn đặc tả là Claude). Bạn chỉ đọc, chạy lệnh kiểm, và ghi kết luận. Đây
là review **đặc tả**, chưa có mã. Lượt 1–4 đều `changes_requested`; lượt 3 và 4 cho A r4 đạt riêng, A r4 không đổi ở lượt này.
Verdict ở `VERDICT-luot1.md` … `VERDICT-luot4.md`, hiện vật ở `luot1/out/` … `luot4/out/` (harness `luot4/out/review_r4.py`,
`luot4/out/review_tools.py`, bản YAML chứng kiến `luot4/out/thu/b1-r3-witness.yml`, `b2-r3-witness.yml` dùng lại được).

## Phạm vi và quyền

- Thư mục làm việc: thư mục chứa tệp này (gọi là `RV`). Chỉ được GHI trong `RV/out/`. Không sửa gì khác trong `RV`
  (cần thử thì chép sang `RV/out/thu/`).
- Không đọc ngoài `RV`. Không dùng mạng. Không đọc thư mục `.codex` hay memory nào.
- `RV/cay-kho/` là clone thưa của kho tại `origin/master` `45bae8d07a8cdf06a1ca9a7a2e015a6258169379` (bỏ `ops/reviews/` và
  `ops/land/` trừ `ops/land/pr997-wp978-land-evidence.yaml`). Lịch sử git đầy đủ, dùng được.
- Python trong sandbox không đọc được site-packages của người dùng. Đặt `PYTHONPATH=<RV>/py-lib` để có PyYAML 6.0.3 (hay chạy
  `python -S` như lượt 4).
- `RV/tacgia/` là vật liệu người soạn đã dùng để chạy thử tiêu chí của A. Chỉ đọc; cần chạy thì chép sang `RV/out/thu/`.
- `RV/luot4/out-goc/` là bản gốc thư mục `out/` của lượt 4 (vài thư mục con không đọc được); dùng `RV/luot4/out/`.

## Tài liệu

| tệp | nội dung |
|---|---|
| `SPEC-A-r4.md`, `SPEC-B1-r4.md`, `SPEC-B2-r4.md` | ba đặc tả cần review (A r4 không đổi từ lượt 3) |
| `SPEC-B1-r3.md`, `SPEC-B2-r3.md`, `DIFF-B1-r3-r4.patch`, `DIFF-B2-r3-r4.patch` | bản lượt 4 và phần đổi |
| `VERDICT-luot1.md` … `VERDICT-luot4.md`, `luot1/out/` … `luot4/out/` | verdict, script và bằng chứng của bốn lượt trước |
| `DE-XUAT-20261116.md`, `bang-chung/` | số đo lần 1 và lần 2 mà đặc tả dẫn |
| `cay-kho/.claude/skills/soan-spec/SKILL.md` | luật soạn đặc tả (L1–L7) |
| `cay-kho/docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md` | bảng E1–E5 và thứ phải mang theo mỗi mã |

## Bối cảnh thay đổi lớn ở r4

Lớp "hợp đồng kiểm lại chưa kín" đã có finding ở cả bốn lượt (F8, N3, R2–R5, S3–S5). r4 không vá thêm mà đổi thiết kế gốc:
bộ xét của B1 tách thành tầng thu (lưu nguyên văn mọi đầu vào thô vào `dau-vao/`) và hàm quyết định thuần có phiên bản ghim;
dòng `TAI_DUNG_AP_DUNG` do biểu thức Actions in ra cho tập hiệu lực; lệnh kiểm lại của B2 xác thực từng đầu vào với nguồn,
phát lại hàm thuần, kiểm bảy bất biến I1–I7 đọc thẳng từ `ADR-0068`, và tính lịch sử Q8 không có cửa sổ trượt. Hãy đánh giá
thiết kế mới này như một thiết kế, không chỉ như bản vá cho S1–S7.

## Việc cần làm

1. Với từng phát hiện S1–S7 của lượt 4 (và F, N, R còn mở): đã đóng thật chưa, đo bằng chính phép đo đã dựng nó (dùng lại
   `luot4/out/review_r4.py`). S1: chạy lại `windows` và `pins` trên bản YAML làm đúng mục tiêu B1 r4, B2 r4 (thêm bước
   `ghi-ap-dung` và đúng các thay đổi r4 vào bản chứng kiến). S2: các phản chứng `provenance` (đuôi SHA giả, commit một cha cùng
   tiêu đề) trên thiết kế bundle. S3: các lịch sử `history`, gồm "lượt đỏ mất artefact rồi 20 lượt tốt". S4, S5: các mô hình
   `contract`, gồm "ghi trung thực hai kế hoạch khác nhau mà đánh dấu `nhanh`" và "xét lỗi sau khi ghi, tải thành công".
2. **Consumer của `ci.yml`.** Bảng consumer ở mục 0 của B1 r4 liệt kê 21 tệp mã và 4 workflow tìm bằng `git grep`. Kiểm bảng ấy
   có đủ không (chạy lại phép tìm của bạn), rồi chạy cột "phép đo" của từng dòng trên bản YAML chứng kiến r4. Một consumer bị
   bỏ sót hay đỏ là finding.
3. Đo lại mọi trích dẫn `tệp:dòng` và lời khai về mã trong ba đặc tả trên `cay-kho`.
4. Tìm lỗi thiết kế mới, ưu tiên: hàm quyết định có thật sự thuần được không với các phép đang liệt kê (4a–4g); phép xác thực
   từng đầu vào ở B2 1e có đường lọt không (nhất là danh sách lượt PR lưu lúc t0, khối `env:` trong log, dòng `Runner Image`);
   bảy bất biến I1–I7 có khớp `ADR-0068` Q1–Q7 không; dòng `TAI_DUNG_AP_DUNG` có thể sai lệch với tập thật sự dùng không; lịch
   sử Q8 (a–f) có thể bị lừa hay rơi vào đường cụt không đáng có; fail-open của bộ xét B1 hay của việc bật ở B2; khối
   `nang_tran` của B1 (ước 600, xin 650) và của B2 (ước 485, xin 550).
5. Kiểm L1–L7 cho ba đặc tả, gồm việc mỗi câu nói tới hỏi chủ kho mang mã E và đủ thứ phải mang theo của mã ấy theo bảng
   `ADR-0067`.
6. Mỗi phát hiện ghi: mức P0–P3, tệp:dòng, hiện tượng, bằng chứng chạy được (lệnh + kết quả), gợi ý hướng sửa. Phản chứng cần
   dựng thì dựng bằng fixture git, YAML và mô hình như các lượt trước; điều gì cần mô tả thay vì dựng thì mô tả bằng lời.

## Đầu ra

Ghi `RV/out/VERDICT.md` gồm: neo đã kiểm (băm ba đặc tả, HEAD của `cay-kho`), trạng thái từng phát hiện lượt 4, bảng lệnh đã
chạy (lệnh, cwd, rc, kết luận), phát hiện mới, kết luận. Dòng CUỐI CÙNG của câu trả lời cuối của bạn phải đúng một trong hai
dạng:

```
KET_LUAN: approve
KET_LUAN: changes_requested
```

`approve` chỉ khi không còn P0, P1, P2 mở.
