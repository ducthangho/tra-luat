# Cross-review độc lập — Packet #773 (land-evidence-khai-phai-co-nguon), g1, lượt 9

Bạn là reviewer Codex, khác họ với executor (Claude). Vai READ-ONLY với mã: KHÔNG sửa tệp nào trong `KHO`. Chỉ ghi vào
thư mục ra (thư mục làm việc hiện tại) hoặc /tmp. `KHO` nằm NGOÀI vùng ghi được của sandbox; executor sẽ đo
`git status --porcelain --ignored` của nó sau lượt. Kết quả bắt buộc: tệp `VERDICT.md` trong thư mục ra.

## Định danh (băm là định danh, không phải tên nhánh)

- Kho `ducthangho/tra-luat`, bản sao sẵn tại `KHO` (cuối prompt), detached ở exact head.
- Exact head: `8b496f9e9909496ab6a66e502ed334e31b24c3b1` (nhánh `agent/wp773-g1-claude`).
- Base: `c73af7b0ba751bfbb974f5ba11147ccb555015dc`. Base gốc `c73af7b`, master hiện `1022a33`. Diff so master: `git -C KHO diff 1022a33 8b496f9` (vá lượt 1: `8ff40b1..bf5993a`; vá lượt 2: `bf5993a..5250883`; vá lượt 3: `5250883..a3cfc53`; vá lượt 4: `a3cfc53..a5dc392`; merge `origin/master` 1022a33 ở `32b441b` (chỉ để qua cổng thu-hoi); vá lượt 5: `32b441b..f9045bf`; vá lượt 6: `f9045bf..98d7d25`; vá connector: `98d7d25..93ef97e`; vá lượt 8: `93ef97e..8b496f9`) — hai tệp mới
  `ops/land_evidence_nguon.py`, `ops/land_evidence_nguon_test.py`.
- Đặc tả đóng băng: `ops/specs/land-evidence-khai-phai-co-nguon-r1.md`, sha256
  `063ccaa692372d8f431af07fcb86acccef32435e4b69e7a63e3b0a4ee67e02dd`. Không có trong cây head; bản sao ở `SPEC`. Kiểm
  băm trước khi tin. Đọc kỹ L1–L5, Q1–Q6, bảng `nghiem_thu`.
- Issue: https://github.com/ducthangho/tra-luat/issues/773.

## Lượt 1–8 và Codex connector

`VERDICT-luot1.md` … `-luot8.md` trong thư mục ra. Lượt 8 (trên `93ef97e`, bản vá P1+P2 của Codex connector và đường thứ ba
token thư mục chứa hồ sơ) còn P3=1: các ca độ lệch chỉ dùng giá trị 0 nên đột biến bỏ quy đổi múi giờ sống. Vá `8b496f9`: c06
thêm `02:00-01:00`, `02:00-0100` (= 03:00Z, sau merge ⇒ ĐỎ) và `03:00+0100` (= 02:00Z, trước merge ⇒ qua); đột biến
`P2_bo_quy_doi_do_lech` bị giết. Kiểm vá đóng thật, có răng, không mở lỗ mới; rồi soi lại toàn bộ.

**NGƯỠNG LƯỢT NÀY: chủ kho đòi hết cả P1, P2 VÀ P3.** Approve chỉ khi P1=0, P2=0, P3=0. Hãy báo đủ mọi P3 thật bạn đo
được, nhưng đừng thổi phồng: thứ không phải khiếm khuyết (lựa chọn đã khai, ngoài phạm vi spec, nợ g2) ghi ở mục riêng,
không tính P3.

## Nhiệm vụ

1. Đọc spec rồi diff. ĐO, đừng chỉ đọc. Có `python3.11`, `python3.12`, `python3.13`, `python3.14`. Chỉ 3.13 có PyYAML
   sẵn; cho bản khác dùng `PYTHONPATH=<SP>/yaml-python3.X` (SP ở cuối prompt). Ví dụ:
   `cd KHO && PYTHONDONTWRITEBYTECODE=1 python3.13 -B ops/land_evidence_nguon_test.py` (~50s) và
   `python3.13 ops/land_evidence_nguon.py --root KHO`.
2. Executor khai (kiểm lại, đừng tin):
   - test: `CA: 14/14`, `DOT BIEN: 37/37 bi giet dung ly do`, `TU KIEM PHAN HANG: DAT`, `TONG: DAT` trên 3.11–3.14;
   - cây thật: `0 ĐẠT · 28/28 miễn trừ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 28`, `TỔNG: ĐẠT`;
   - thực địa trên lịch sử #771 (commit có trong `KHO`): `git -C KHO archive <c> ops/land | tar -x -C <thư mục tạm>` rồi
     `--root <thư mục tạm> --tep ops/land/pr765-wp743-land-evidence.yaml`. `c6e2401` ⇒ 2 vi phạm L1 (gồm
     `khong_xung_dot` mergeable_state, lượt 1); `1a4c417` ⇒ L1 + 2×L2 + L3 (mốc 02:58:54Z ≥ merged_at 02:58:26Z, lượt 2);
     `d60b9e6` ⇒ 1 L1 (`$.spec.nguon`);
   - không miễn trừ (xoá `MIEN_TRU_CUTOVER` trong bản sao): 16 ĐẠT, 12 ĐỎ, 82 vi phạm, toàn L1, 0 KHÔNG ĐO ĐƯỢC;
   - 2 tệp / 723 dòng thêm; chủ kho nâng trần lên 750; chủ kho đã nâng trần ngoại lệ lên 700 (16-10-2026).
3. Đột biến để đo răng: chép bộ kiểm ra /tmp, sửa bản sao, chạy test với `LAND_EVIDENCE_NGUON_MA=<bản sao>`
   `--mot-ca <ca>` (rc 3 + dòng `DO:<ca>:` = giết thật; rc 4 = lỗi vô can). Tìm chốt không có đột biến nào canh.
4. Soi riêng:
   - Có đường nào cho ra ĐẠT (rc=0) khi lẽ ra phải ĐỎ hoặc KHÔNG ĐO ĐƯỢC (fail-open)? Ví dụ: token phân giải sai nền,
     glob, thư mục, khoá YAML trùng, giá trị không phải chuỗi, `positive` kiểu số, `pre_merge_checks` dạng dict, mốc có
     phần thập phân hay múi giờ, readback lân cận, symlink.
   - Phạm vi tuyên bố trong docstring có rộng hơn phép đo không? Lệch chữ của spec (vd so `measured` không phân biệt hoa
     thường, chọn `readback-pr-<N>.json` theo tên hồ sơ, coi tự trỏ hồ sơ không phải nguồn) có hợp lý và được khai không?
   - Ca test nào "có MẶT mà không ĐO" (xanh vì lý do khác)? Đột biến nào chết vì lỗi vô can mà vẫn đếm giết?
   - L5: vân tay danh sách trong test có thật sự độc lập và làm ĐỎ khi thêm/đổi tên? m = k có được đo?
   - Tiêu chí `nghiem_thu` nào chưa đáp ứng hoặc chưa đo?
5. Hướng thử cần SOẠN nội dung nhạy cảm (đường dẫn thoát cây kiểu khai thác, mã tấn công) thì đừng soạn — mô tả bằng lời
   trong VERDICT; ca `c03` đã có sẵn một token `../` để chạy.

## Định dạng VERDICT.md

- Dòng đầu: `Reviewed commit: 8b496f9e9909496ab6a66e502ed334e31b24c3b1`
- `verdict: approve` hoặc `verdict: changes_requested`; đếm `P1=`, `P2=`, `P3=`.
- Mỗi finding: mã (F01…), mức, tệp:dòng, mô tả, PHÉP ĐO đã chạy (lệnh + kết quả), HINT patch nếu phức tạp.
- Mục "Đã đo" (mọi lệnh + rc/kết quả) và "KHÔNG ĐO ĐƯỢC" (kèm lý do).
- Ngưỡng: approve chỉ khi P1=0, P2=0 và P3=0.

## Đường dẫn

- KHO: `/home/user/rv773`
- SPEC: `/home/user/rv773-spec-r1.md`
- SP: `/tmp/claude-0/-home-user-tra-luat/25822fa2-ac40-52b8-b361-6687f0dd1ccb/scratchpad`
- Thư mục ra (ghi VERDICT.md ở đây): `/tmp/claude-0/-home-user-tra-luat/25822fa2-ac40-52b8-b361-6687f0dd1ccb/scratchpad/rv773-out9`
