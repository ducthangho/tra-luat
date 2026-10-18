# Cross-review độc lập — Packet #773, PR #778, đợt g2 (nối CI) + toàn PR, lượt 1

Bạn là reviewer Codex, khác họ với executor (Claude). Vai READ-ONLY với kho: KHÔNG sửa tệp nào trong `KHO`. Chỉ ghi vào
thư mục ra (thư mục làm việc hiện tại) hoặc /tmp. Kết quả bắt buộc: tệp `VERDICT.md` trong thư mục ra.

## Định danh (băm là định danh, không phải tên nhánh)

- Kho `ducthangho/tra-luat`, bản sao tại `KHO=/home/user/rv773`, detached ở exact head.
- Exact head: `128b2e892f91dd353367c082bfc9cf2c300ecfb7` (nhánh `agent/wp773-g1-claude`, PR #778).
- Master hiện `fb490a7` (đã merge vào head). Diff toàn PR so master: `git -C KHO diff fb490a7 128b2e8` — 3 tệp:
  `ops/land_evidence_nguon.py`, `ops/land_evidence_nguon_test.py` (g1, đã review 9 lượt, lượt 9 approve 0/0/0 ở `8b496f9`),
  `.claude/dev/ci_dang_ky_test.py` (g2, đúng 1 dòng). Thay đổi mã g1 kể từ `8b496f9`: `git -C KHO diff 8b496f9 128b2e8 --
  ops/land_evidence_nguon.py ops/land_evidence_nguon_test.py` (kỳ vọng rỗng — kiểm).
- Spec g2: `ops/specs/land-evidence-khai-phai-co-nguon-r2.md` trên ref `origin/ops/wp773-r2-g2-lease`, sha256
  `c70c19b57ad1d9bf0304a04bbb259b0b74ebc366824c24597c7207b7beaf14a0` (kiểm băm: `git -C KHO show
  origin/ops/wp773-r2-g2-lease:ops/specs/land-evidence-khai-phai-co-nguon-r2.md | sha256sum`). Spec r1 g1 ở
  `origin/ops/wp773-r1-g1-lease`. Các VERDICT g1 lượt 1–9 ở `origin/ops/wp773-r1-g1-reviews:ops/reviews/`.
- Issue: https://github.com/ducthangho/tra-luat/issues/773.

## Bối cảnh

g2 thêm một dòng `MOI` để `gate-registry` chạy `ops/land_evidence_nguon_test.py` và khớp dòng tổng kết bằng mẫu. Trước
đó CI #778 đỏ vì hai hồ sơ land trên master thiếu token nguồn; PR #787 và #821 (đã merge) gắn nguồn. Nay cục bộ:
`CA: 14/14`, `DOT BIEN: 37/37 bi giet dung ly do`, `TONG: DAT`; `ci_dang_ky_test.py` rc=0; cây thật
`2 ĐẠT · 28/28 miễn trừ · 0 vi phạm`. CI trên head này đang chạy.

## Nhiệm vụ — ĐO, đừng chỉ đọc

1. Đọc spec r2 (bảng `nghiem_thu`) rồi diff. Kiểm từng tiêu chí: diff g2 đúng 1 dòng thêm/0 xoá; không tệp ngoài write set
   g1+g2; `python3.13 -B .claude/dev/ci_dang_ky_test.py` rc=0 (chạy trong bản sao tạm nếu nó ghi gì — KHO read-only).
2. Mẫu `MOI`: có đúng 2 nhóm bắt? Đọc `bang_chung_xanh` và cách `gate-registry`/`--chay` dùng mẫu (`re.M`?). Tự dựng đầu ra
   hỏng: `TONG: DO`, `CA: 13/14`, `DOT BIEN: 0/0 …`, thiếu dòng `DOT BIEN`, dòng thừa/khác thứ tự, `CA: 0/0` — mỗi cái phải
   KHÔNG qua. Có đầu ra hỏng nào lọt (vd chế độ NHE, CRLF, tiền tố log CI, `TONG: DAT` xuất hiện ở dòng khác)? Có đột biến
   nào trên dòng đăng ký (bỏ dòng, sai đường dẫn, sai mẫu) mà `ci_dang_ky_test.py` không bắt?
3. Đăng ký `MOI` có làm test chạy ở chế độ ĐẦY ĐỦ trên CI (đột biến chạy thật) hay bị cắt? Thời gian ~45 s có vấn đề không?
4. Chạy lại `python3.13 -B ops/land_evidence_nguon_test.py` (~50 s, trong bản sao tạm) và bộ kiểm trên cây thật. Có ca nào
   phụ thuộc trạng thái master (hồ sơ land mới thêm sau cutover) khiến test DỄ VỠ khi hồ sơ tương lai vào master? Đây là
   rủi ro vận hành thật (đã xảy ra hai lần) — đánh giá và phân hạng, đừng bỏ qua.
5. Soi lại toàn bộ g1 nếu có thay đổi kể từ `8b496f9` (kỳ vọng không).

**NGƯỠNG: chủ kho đòi hết P1, P2 VÀ P3.** Approve chỉ khi P1=0, P2=0, P3=0. Thứ ngoài phạm vi spec ghi mục riêng.
Hướng thử cần SOẠN nội dung nhạy cảm thì mô tả bằng lời, đừng soạn.

## Định dạng VERDICT.md

- Dòng đầu: `Reviewed commit: 128b2e892f91dd353367c082bfc9cf2c300ecfb7`
- Dòng hai: `Verdict: approve` hoặc `Verdict: request_changes`, kèm `P1=a P2=b P3=c`.
- Mỗi finding: mức, tệp:dòng, mô tả, lệnh tái hiện + đầu ra đo được, đề xuất sửa.
- Mục "Đã đo" và "Ngoài phạm vi".
