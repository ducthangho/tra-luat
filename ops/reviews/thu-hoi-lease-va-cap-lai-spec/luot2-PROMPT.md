# Cross-review ĐẶC TẢ — `THU-HOI-LEASE-VA-CAP-LAI` **revision 2** · REVIEWER codex · lượt 2

Bạn là reviewer cross-provider (tác giả spec là `claude`). Cùng vai, cùng cấm như lượt 1: **read-only với kho**
(không commit/push/sửa `cay-kho` ngoài bản sao/đột biến trong `scratch/` dưới cwd); **CẤM đọc ra ngoài cwd**;
**CẤM tự soạn** đường thoát cây / đồng tự Unicode / chuỗi thoát — mô tả bằng lời. Không có mạng. Tối đa 60 phút;
phút 50 bắt đầu ghi verdict.

## Thư mục
- `SPEC.md` — **revision 2**, sha256 `9e775a154dd83741fd4e7af85aaeae1f5693ceabc5c5763cf6890ff4f2606c80`; cùng nội dung tại `cay-kho/ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` (untracked).
- `SPEC.r1.md` — bản r1 bạn đã review (sha256 `43844cb2…`).
- `VERDICT.luot1.md` (sha256 `b60a755f…`) và `HINT.luot1.patch` (`1aeb9621…`) — verdict + hint của CHÍNH BẠN lượt 1.
  r2 KHÔNG áp patch nguyên văn; nó viết lại thiết kế theo finding. §0 của SPEC.md có bảng "finding → r2 làm gì".
- `cay-kho/` — mirror đầy đủ (302 ref remote, detached tại `b416830ef2a509d60203d55552ce17950afcf67c`, `core.abbrev 7`). `origin` là bare cục bộ `../../rv1/kho.git` — `ls-remote` chạy offline, KHÔNG phải nguồn có thẩm quyền về độ tươi GitHub (bạn đã ghi đúng điều này ở lượt 1).
- `EVIDENCE.md` — lời khai lượt 1 + phần bổ sung lượt 2 (đo phía điều phối, có mạng). ĐO LẠI những gì đo được offline.

## Việc phải làm
1. **Từng finding lượt 1 (14)**: đọc §0 SPEC.md, đối chiếu thân spec. Phân loại: ĐÓNG (r2 sửa đúng và đủ) · ĐÓNG-MỘT-PHẦN (nêu phần thiếu) · CHƯA ĐÓNG · **ĐÓNG SAI** (bản vá tạo lỗ mới). Với mỗi finding từng có phản chứng D3/D4: **chạy lại phản chứng ấy dưới luật r2** (mô phỏng bằng script trong `scratch/`, như lượt 1) và ghi kết quả mới.
2. **Tấn công r2 ở chỗ MỚI**: Q4 (symref máy chủ + ghim OID), Q2 (khối lệnh JSON so bằng nhau, cổng `kiem-thu-hoi-github`), M9 (workflow là cổng tiếp nhận — đọc `cay-kho/.github/workflows/ops-publish-lease.yml` hiện có, bước "neo bộ kiểm", và chỉ ra chỗ nào cách gắn của r2 hỏng), Q6 (danh sách đóng neo canonical, áp toàn ID), M7 (guard 5 cửa), A8 (map đường→blob ứng viên). Dựng phản chứng git thật + mô phỏng luật r2.
3. **A1–A12 r2**: có đơn vị? phép đỏ thật? đột biến đúng ca? có ca nào không thể đỏ / không thể xanh?
4. **Nhất quán luật** (§3.2 §4 §5 §8 §12; ADR-0025/0028/0044; CLAUDE.md) và **kích thước/Q7** (ước 655–945, tách A/B/C).
5. **Q7–Q12**: câu nào còn thiếu, câu nào đã có đáp án bắt buộc từ luật.
6. **Đo lại con số mới của r2** (7/11 tệp bia mộ, 31 commit #468, +409/+368/+328, 2 cặp r2, 5 ref mang `26f07b4` sau PR #475 …) bằng lệnh trong `cay-kho`; số nào không đo được offline ghi CHƯA ĐO.

## Xếp hạng
P1 = spec như đang viết sẽ sinh mã sai/fail-open, mâu thuẫn luật, tiêu chí không thể đỏ, hoặc con số chống đỡ lời khai THẨM QUYỀN mà sai. P2 = thiếu/mơ hồ khiến executor tự quyết. P3 = chữ nghĩa. **Finding lượt 1 chưa đóng thì giữ nguyên hạng.**

## Đầu ra — BẮT BUỘC, ghi vào cwd
1. `VERDICT.md`:
```
verdict: approve | changes_requested | blocked
reviewed_spec_sha256: <64 hex>
model_tu_khai: <nói thật>
## Bảng finding lượt 1 → trạng thái   (14 hàng: id · hạng cũ · ĐÓNG/ĐÓNG-MỘT-PHẦN/CHƯA/ĐÓNG SAI · bằng chứng)
## Findings mới                        (id-kebab · P · mục spec · TÁI HIỆN · vì sao · GỢI Ý VÁ)
## Phản chứng đã chạy lại + mới
## Tiêu chí A1–A12
## Bảng đo lại
## chua_do_duoc
```
2. `HINT.patch` — unified diff áp được bằng `patch -p0` lên `SPEC.md` cho MỌI finding P1/P2 còn lại. Không áp được = không có patch.
Dòng cuối stdout: `XONG VERDICT sha256=<sha256 của VERDICT.md>`.
Bắt đầu lúc: 2026-09-07T14:29:29Z
