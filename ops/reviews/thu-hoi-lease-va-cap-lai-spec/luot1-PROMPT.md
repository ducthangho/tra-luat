# Cross-review ĐẶC TẢ (không phải mã) — `THU-HOI-LEASE-VA-CAP-LAI` · REVIEWER codex · lượt 1

Bạn là reviewer cross-provider (tác giả spec là `claude`). Vai **read-only với kho**: KHÔNG commit, KHÔNG push, KHÔNG sửa tệp trong `cay-kho` ngoài việc tạo bản sao/đột biến trong thư mục tạm CỦA sandbox. Bạn được ghi tệp bất kỳ trong thư mục sandbox hiện tại (cwd) — và PHẢI ghi đúng hai tệp kết quả nêu ở cuối.
**CẤM đọc ra ngoài cwd** (không `cd ..`, không đọc $HOME, không đọc transcript nào). **CẤM tự soạn** đường dẫn thoát cây thư mục, đồng tự Unicode, chuỗi thoát — hướng tấn công thuộc lớp ấy thì MÔ TẢ BẰNG LỜI trong verdict, phiên điều phối sẽ dựng.
Không có mạng. Thời gian: tối đa 60 phút; tới phút 50 phải bắt đầu ghi verdict dù chưa xong — verdict thiếu còn hơn verdict không có.

## Thư mục
- `SPEC.md` — đặc tả cần review. sha256 `43844cb2ea2653f502320a6f35a6e3ae7fd182770f02b62d4d73b9aa8dbea6f9`. Cùng nội dung tại `cay-kho/ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` (untracked).
- `cay-kho/` — mirror ĐẦY ĐỦ của kho (302 ref remote, detached tại `b416830ef2a509d60203d55552ce17950afcf67c` = origin/master, `core.abbrev 7`). Bạn ĐO được ở đây: `git`, `python3 ops/lease_publish.py ai-dang-giu <đường>`, `python3 ops/lease_publish_test.py`, `.claude/dev/packet_loop.py`, `docs/PROTOCOL_DA_PHIEN.md`, `docs/adr/*.md`, `CLAUDE.md`, `ops/specs/*.md` (tiền lệ: `lease-hoi-toan-kho.md`, `ag-t0-01b-r4.md`).
- `EVIDENCE.md` — lời khai phép đo của tác giả. ĐO LẠI, đừng tin.

## Bối cảnh một đoạn
Lease của kho là tệp YAML trong `ops/leases/`, được quét trên MỌI ref. Thu hồi hiện chỉ có "bia mộ hai chiều" ghi vào tệp cũ, nên bản sao của tệp cũ trên các ref khác vẫn sống. Spec đề xuất sổ thu hồi append-only `ops/thu-hoi/<lease_id>.yaml` có hiệu lực CHỈ khi nằm trên `origin/<mặc định>`, đổi `check`/`ai-dang-giu`/`packet_loop` để đọc sổ. Chủ kho là `ducthangho`; chưa có Issue, chưa có lease — spec đang ĐÓNG BĂNG TRƯỚC khi xin lease. Việc của bạn là làm nó ĐỦ CHẶT để mã viết theo nó không phải quay lại sửa spec.

## Việc phải làm — theo thứ tự, ghi bằng chứng cho từng mục
1. **Đo lại MỌI con số** trong SPEC.md và EVIDENCE.md bằng lệnh trong `cay-kho`. Bảng: con số khai · con số đo · lệnh · khớp/lệch. Số của mirror có thể khác kho nguồn (nhánh cục bộ) — nói rõ vì sao khi lệch.
2. **Phá thiết kế**, từng câu Q1–Q6: dựng trong một kho giả (bare + working copy trong sandbox, hoặc trên bản sao của `cay-kho`) một chuỗi thao tác git hợp lệ mà DƯỚI LUẬT SPEC ĐỀ XUẤT vẫn ra: (a) hai lease CÒN_HẠN cùng giữ một đường dẫn mà `check` lease mới trả rc=0; (b) một lease đã bị thu hồi mà vẫn được đếm là người giữ; (c) một bản ghi thu hồi giả/không thẩm quyền được cổng nhận; (d) fail-open ở bất kỳ nhánh KHÔNG ĐO ĐƯỢC nào. Bạn có thể MÔ PHỎNG luật mới bằng script nhỏ trong sandbox (spec chưa có mã). Không dựng được phản chứng thì nói "không dựng được", kèm đã thử gì.
3. **Từng tiêu chí nghiệm thu A1–A12**: có đơn vị đo không? phép đo làm nó ĐỎ có thật không? đột biến nêu ra có thật sự đổi màu ca ấy không, hay ca đo thứ khác? Có tiêu chí nào KHÔNG THỂ ĐỎ không?
4. **Nhất quán với luật**: `docs/PROTOCOL_DA_PHIEN.md` §3.2 §4 §5 §12 §8, `docs/adr/0025-*.md` `0028-*.md` `0044-*.md`, `CLAUDE.md` (mục "Bài học đắt giá", đặc biệt: danh sách cho phép; ca có MẶT ≠ có ĐO; ba trạng thái; đo thứ đã đến). Spec có chép doctrine thay vì trỏ không? Có hứa thứ ngoài write set không (L2)?
5. **Kích thước**: ước tính của spec (+450±100, 5 tệp) có hợp lý với các ca A1–A12 không; đề xuất tách slice của spec có làm slice A tự đủ không.
6. **Câu chủ kho phải chốt (Q7–Q9)**: thiếu câu nào? câu nào thật ra đã có đáp án bắt buộc từ luật?

## Xếp hạng
P1 = spec như đang viết sẽ sinh mã sai/fail-open, hoặc mâu thuẫn luật, hoặc tiêu chí không thể đỏ, hoặc con số chống đỡ một lời khai về THẨM QUYỀN mà sai. P2 = thiếu/mơ hồ khiến executor phải tự quyết. P3 = chữ nghĩa.

## Đầu ra — BẮT BUỘC, ghi vào cwd
1. `VERDICT.md`:
```
verdict: approve | changes_requested | blocked
reviewed_spec_sha256: <64 hex>
model_tu_khai: <bạn là gì, nói thật, kể cả "không chứng thực được">
## Bảng đo lại        (mục 1)
## Findings           mỗi finding: id-kebab · P1/P2/P3 · mục spec · TÁI HIỆN (lệnh + output) · vì sao · GỢI Ý VÁ (câu chữ cụ thể)
## Phản chứng đã thử  (mục 2, kể cả thất bại)
## Tiêu chí A1–A12    bảng: có đơn vị? có phép đỏ? đột biến đúng ca?
## chua_do_duoc       của CHÍNH BẠN
```
2. `HINT.patch` — unified diff áp được bằng `patch -p0` lên `SPEC.md`, chứa câu chữ vá cho MỌI finding P1/P2 (P3 tuỳ). Patch không áp được = không có patch.
Dòng cuối stdout: `XONG VERDICT sha256=<sha256 của VERDICT.md>`.
Bắt đầu lúc: 2026-09-07T13:49:41Z
