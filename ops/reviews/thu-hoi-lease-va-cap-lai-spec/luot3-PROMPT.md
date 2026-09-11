# Cross-review ĐẶC TẢ — `THU-HOI-LEASE-VA-CAP-LAI` **revision 3** · REVIEWER codex · lượt 3

Cùng vai, cùng cấm như lượt 1–2: **read-only với kho** (không commit/push/sửa `cay-kho` ngoài bản sao/đột biến trong
`scratch/` dưới cwd); **CẤM đọc ra ngoài cwd**; **CẤM tự soạn** đường thoát cây / đồng tự Unicode / chuỗi thoát — mô tả
bằng lời. Không có mạng. Tối đa 60 phút; phút 50 bắt đầu ghi verdict.

## Thư mục
- `SPEC.md` — **revision 3**, sha256 `ef9b3700514921d4cabe95947f86937fc36f4aecf2f4e2e39587cafe88a9bb20`; cùng nội dung tại `cay-kho/ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` (untracked).
- `SPEC.r2.md` (`9e775a15…`) — bản bạn đã review lượt 2. `VERDICT.luot2.md` (`bb293295…`) + `HINT.luot2.patch` (`02b562b3…`) — verdict + hint của CHÍNH BẠN lượt 2. `VERDICT.luot1.md` (`b60a755f…`) — lượt 1.
  r3 KHÔNG áp patch nguyên văn; nó viết lại theo finding. §0.1 của SPEC.md có bảng "finding N1–N11 → r3 làm gì".
- `cay-kho/` — mirror đầy đủ (302 ref remote, detached tại `b416830ef2a509d60203d55552ce17950afcf67c`, `core.abbrev 7`). `origin` là bare cục bộ — `ls-remote` offline, KHÔNG phải nguồn thẩm quyền độ tươi.
- `EVIDENCE.md` — lời khai lượt 1–2 + bổ sung lượt 3 (đo phía điều phối, có mạng). ĐO LẠI những gì đo được offline.

## Việc phải làm
1. **Từng finding lượt 2 (N1–N11) và 8 finding lượt 1 còn ĐÓNG-MỘT-PHẦN / 1 ĐÓNG SAI**: phân loại ĐÓNG · ĐÓNG-MỘT-PHẦN · CHƯA · ĐÓNG SAI, kèm bằng chứng. Với finding từng có phản chứng: **chạy lại dưới luật r3** (mô phỏng trong `scratch/`, như hai lượt trước) và ghi kết quả mới.
2. **Tấn công r3 ở chỗ MỚI**: (a) Q4 danh tính ghim trong mã `KHO_CANONICAL` so với `ls-remote --get-url` — có lách được bằng `url.<x>.insteadOf` / `pushInsteadOf` / remote helper không? (b) bootstrap A0→A1: hằng `SO_THU_HOI_KICH_HOAT` + cổng test "`ops/thu-hoi/` rỗng" chạy ở `ci.yml` lane PR (mã của PR — untrusted): một PR vừa thêm bản ghi vừa xoá ca test thì sao? Có cách nào rẻ hơn/chặt hơn không? (c) M9 `pull_request_target` + `git fetch origin refs/pull/<n>/head`: S = `base.sha` lúc chạy vs cây MERGE thật sẽ vào master khi base trôi — drift; đề xuất điều kiện ngoài kho (require branches up to date) có đủ không? (d) Q6 mốc "lúc A0 land" ghim trong mã: cách ghim nào đo được, và ca test nào bắt "danh sách tự mở rộng"? (e) Q3 giải symlink trong cây OID: symlink tương đối/tuyệt đối/vòng/trỏ ra ngoài; `effective_write_set` tự khai bởi lease (không phải dispatcher) có bị lợi dụng để THU HẸP tập không? (f) A5 CLI đòi "đã publish": ứng viên trên ref máy chủ nào — bất kỳ ref, hay chỉ `ops/**`? (g) M7 guard cùng routine Q4 có mạng: ca fail-close có làm executor hợp lệ bị chặn oan vì proxy như container này (REST 403 nhưng git OK)?
3. **A1–A12 r3**: đơn vị? phép đỏ thật? đột biến đúng ca? ca không thể đỏ / không thể xanh?
4. **Nhất quán luật** (§3.2 §4 §5 §8 §12; ADR-0025/0028/0044; CLAUDE.md), **kích thước theo slice A0/A1/B/C**, và câu về §12 trần 2 lượt review ở §0.
5. **Q7–Q12**: còn thiếu câu nào; câu nào đã có đáp án bắt buộc.
6. **Đo lại con số r3** đo được offline (7/3 lease còn hạn/chưa bia mộ lúc 14:33Z, 4 hạn gate-tach, policy vắng, 5 cửa packet_loop, …).

## Xếp hạng
P1 = spec như đang viết sẽ sinh mã sai/fail-open, mâu thuẫn luật, tiêu chí không thể đỏ, hoặc con số chống đỡ lời khai THẨM QUYỀN mà sai. P2 = thiếu/mơ hồ khiến executor tự quyết. P3 = chữ nghĩa. Finding cũ chưa đóng giữ nguyên hạng.

## Đầu ra — BẮT BUỘC, ghi vào cwd
1. `VERDICT.md`:
```
verdict: approve | changes_requested | blocked
reviewed_spec_sha256: <64 hex>
model_tu_khai: <nói thật>
## Bảng finding lượt 1–2 → trạng thái   (mỗi finding một hàng: id · hạng · trạng thái · bằng chứng)
## Findings mới                          (id-kebab · P · mục spec · TÁI HIỆN · vì sao · GỢI Ý VÁ)
## Phản chứng đã chạy lại + mới
## Tiêu chí A1–A12
## Bảng đo lại
## chua_do_duoc
```
2. `HINT.patch` — unified diff áp được bằng `patch -p0` lên `SPEC.md` cho MỌI finding P1/P2 còn lại. Không áp được = không có patch.
Dòng cuối stdout: `XONG VERDICT sha256=<sha256 của VERDICT.md>`.
Bắt đầu lúc: 2026-09-07T15:27:04Z
