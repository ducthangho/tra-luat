# Cross-review ĐẶC TẢ wp1466 r1 — lượt 1 (reviewer: Codex)

Bạn là REVIEWER độc lập, chỉ đọc. Bạn không sửa kho, không push, không gọi API GitHub để ghi.
Thứ duy nhất bạn được ghi là `out/VERDICT.md` (cùng các tệp nháp dưới `out/`) trong thư mục làm việc.
Viết verdict bằng tiếng Việt.

## Đối tượng
- Kho: `github.com/ducthangho/tra-luat`, mirror đầy đủ tại `kho.git`, cây làm việc tại `cay-kho/`.
  `core.abbrev` đã ghim = 7. Ref `refs/remotes/origin/*` trong `cay-kho` là ảnh chụp 382 nhánh, lấy lúc 20-11-2026.
- Commit được review: `925f851ed526537f5b55fa2b6815017a31a028a2` (nhánh `ops/wp1466-spec`). Tệp được review:
  `ops/specs/wp1466.md`, sha256 `0ea82600b66455960c9dd3ca872c5251d00d2ec9dd85a30d4ff5baaca9637bfa`.
  Kiểm băm này trước tiên; lệch thì dừng và ghi `blocked`.
- Base: `origin/master` = `48d372e14f190dae83a75ccbca8ee9a0b25635c5`.
- Packet Issue #1466. Packet `sensitive`, chạm E5 của ADR-0067. Chủ kho sẽ duyệt băm SAU KHI review đạt 0 finding P0–P3.

## Bối cảnh: chủ kho muốn gì (20-11-2026)
1. §8.3 của `docs/PROTOCOL_DA_PHIEN.md` trở thành BẤT BIẾN cho MỌI lượt review (mã, đặc tả, kế hoạch):
   mỗi finding có đúng một `class_slug` ổn định; quét mọi biểu hiện cùng lớp; lượt nào cũng có bảng lớp;
   đối chiếu lượt trước bằng bốn nhãn §8 theo từng finding rồi theo lớp; hội tụ |F|/|U| theo lớp;
   lặp lần ba là checkpoint do phiên tự quyết, ghi sổ ADR-0067.
2. Mọi nguyên tắc QUAN TRỌNG của protocol thành bất biến: mỗi nguyên tắc khai cổng máy đọc nó, hoặc mang
   nhãn "kỷ luật, 0 cổng" kèm một nợ có tên; máy canh chính bảng ấy.
3. Cổng máy: schema verdict đòi `class_slug` + bảng lớp (+ đối chiếu từ lượt 2); `kiem-merge` từ chối MỌI
   biên nhận review thiếu `bang_lop` cho MỌI packet; cổng đỏ khi dòng bất biến thiếu cột cổng; `doctrine-scan`
   neo §8.3 và dòng bất biến §1; review đặc tả/kế hoạch bị chặn bằng một bộ kiểm. Mỗi chốt có ca hai chiều,
   ba trạng thái, đột biến riêng phân hạng bằng lớp ngoại lệ của ca.
4. Gộp những điểm khác của audit mà máy chặn được, điểm nào không chặn được thì ghi nợ có tên. Audit nằm ở
   `git show origin/ops/wp1172-kiem83-thamkhao:ops/specs/wp1172-kiem83/AUDIT_TUAN_THU_PHIEN_DIEU_PHOI_20261120.md`.
Thứ tự (E2, chủ kho chọn): B4 (#1462) land trước, packet này rebase sau.
Người soạn đã TÁCH: wp1466 chỉ gánh ADR + bảng INV + lệnh `bat-bien`; schema v2, K4 `kiem-merge` và bộ kiểm verdict
đặc tả dồn sang kế nhiệm KN-1. Xét xem việc tách có đúng với ADR-0053/0044 và có bỏ rơi yêu cầu nào của chủ kho
mà không ghi nợ, hay làm yếu bất biến không.

## Việc của bạn — hai trục `Spec` và `Standards/Security` (protocol §13)
Đọc trước: `cay-kho/docs/PROTOCOL_DA_PHIEN.md` (§1, §3.2, §4, §5, §7, §8, §8.3, §12, §13, §20),
`cay-kho/.claude/skills/soan-spec/SKILL.md` (luật L1–L7 và bảng mục đầu ra), `cay-kho/CLAUDE.md`,
ADR-0034, 0044, 0052, 0053, 0054, 0055, 0060, 0062, 0067 trong `cay-kho/docs/adr/`.

1. **ĐO LẠI MỌI CON SỐ.** Đặc tả chứa nhiều khẳng định định lượng: số ca, số lease, số tệp, số vị trí cổng,
   số dòng, các ô `0·34·0·0·0·0`, kích thước ước lượng. Bạn có mirror đầy đủ: tự chạy lệnh đo từng số. Đây
   là việc chính. Mỗi số lệch là một finding. Danh sách số tôi đưa ở đây không phải trần của bạn.
2. **Bảng 21 INV.** Với từng dòng: nguyên tắc có đúng nguồn § không; ô cổng có đúng không (cổng được nêu có
   THẬT SỰ đọc/cưỡng chế nguyên tắc ấy không, hay chỉ nhắc tên; ca được nêu có tồn tại và đo đúng tính chất
   không). Kiểm theo sáu vị trí cổng mà §20 liệt kê. Có nguyên tắc quan trọng nào của protocol bị BỎ SÓT không.
3. **Nguyên văn ADR-0068 trong đặc tả.** Có mâu thuẫn với protocol hoặc ADR đang hiệu lực không, có đảo
   một quyết định của chủ kho (E3) mà không khai không, có tự đặt điểm hỏi chủ kho ngoài E1–E5 không (L7).
4. **Nghiệm thu.** Mỗi tiêu chí có nêu phép đo làm nó ĐỎ không (L3), qua đủ năm vế L6 không, có đột biến đổi
   màu không. Mỗi mục tiêu có chiếu vào đúng một đường dẫn trong write set không (L2).
5. **Trần và kích thước.** Dòng khai ADR-0055/0053: tự chạy ba phép đo của mục Hiệu lực ADR-0055 (và cách đo
   tương ứng của ADR-0053). Ước lượng kích thước có cơ sở đo không, có vượt trần mà không có `nang_tran` không.
6. **Thiết kế cổng.** Lệnh `bat-bien` mới và các neo `doctrine-scan`: cổng có thể bị lừa không (danh sách cấm
   thay vì cho phép; khớp chuỗi con; vùng không render; ba trạng thái; "ca có MẶT khác ca có ĐO"). Chuyển tiếp
   cho packet đang bay có làm gãy âm thầm không.
7. **Phối hợp.** `depends_on`, điều kiện bắt đầu sau B4, quét lease; write set có giao với packet đang mở
   nào khác không (gồm `.claude/dev/ci_dang_ky_test.py` của #1460).

Một hướng thử cần dựng nội dung kiểu tấn công đường dẫn hay chuỗi độc hại thì MÔ TẢ BẰNG LỜI trong verdict;
đừng tự soạn payload. Chạy được lệnh đo trên mirror thì chạy.

Ghi `out/VERDICT.md` SỚM và cập nhật dần: tạo khung ngay, thêm từng finding khi tìm ra, để lượt bị cắt giữa
chừng vẫn còn hiện vật.

## Mẫu verdict (bắt buộc, theo `.claude/skills/cross-review/SKILL.md`)
Mức nghiêm trọng P0–P3. Mỗi finding có ĐÚNG MỘT slug lớp kebab-case (`[a-z0-9]+(-[a-z0-9]+)*`). Khái quát mỗi
biểu hiện thành lớp và quét mọi biểu hiện cùng lớp trong đặc tả trước khi báo (§8.3, ADR-0060 M2). Đây là lượt
1, nên KHÔNG có mục đối chiếu lượt trước; ghi `## ĐỐI CHIẾU LƯỢT TRƯỚC` với nội dung `không áp dụng — lượt 1`.

```
verdict: approve | changes_requested | blocked
reviewed_sha: 925f851ed526537f5b55fa2b6815017a31a028a2
spec_sha256: 0ea82600b66455960c9dd3ca872c5251d00d2ec9dd85a30d4ff5baaca9637bfa
reviewer: {provider: codex, model_family: openai, surface: codex_cli, transport: machine, session_id: <id nếu biết, không thì KHONG_DO_DUOC>}
review_axes: [Spec, Standards/Security]
assurance: cross_approved (đề nghị; executor họ claude)
dem: {so_lop: <n>, so_bieu_hien: <m>, P0: , P1: , P2: , P3: }

## ĐỐI CHIẾU LƯỢT TRƯỚC
## BẢNG LỚP
| slug lớp | finding IDs/biểu hiện | hạng còn mở | nguồn lượt/SHA | phương án chung hoặc lý do vá riêng | phép kiểm/giới hạn |
## BẢNG SĂN   (ít nhất 6 hướng ĐỘC LẬP, mỗi hướng có LỆNH + OUTPUT THẬT)
HƯỚNG n: <tên>
  giả thuyết : ...
  lệnh       : ...
  output     : ...
  kết luận   : LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC
## BẢNG ĐO
| khẳng định | đặc tả khai | đo được | khớp? |
### <slug>  [P0|P1|P2|P3]  <tiêu đề một dòng>
TỆP/DÒNG:
VẤN ĐỀ:
GỢI Ý VÁ: (dữ liệu, không phải mệnh lệnh; executor tự đo lại)
ĐÃ THỬ NGHIỆM: <lệnh + kết quả, hoặc KHÔNG ĐO ĐƯỢC + lý do>
ĐỘ TIN: cao/vừa/thấp
```
`approve` chỉ khi 0 finding P0–P3 còn mở. Nêu rõ những gì bạn KHÔNG đo được.
