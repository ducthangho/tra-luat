
codex
## E1

**ĐỌC ĐƯỢC:** ADR-0044 gọi packet chạm authority là `sensitive`; protocol cũng xếp review authority, launcher và gate lifecycle vào lớp này.

**ĐO ĐƯỢC:** `record-review` là đường duy nhất vào `accepted`; kho đã từng có finding `review-transition-bypasses-record-review`.

**SUY LUẬN:** **CÓ, script đụng review authority.** Điều kiện receipt mới thay đổi trực tiếp vị từ được vào `accepted`, nên phải là `sensitive`, không phải `systemic`.

**SUY LUẬN:** Lượt dựng tay bị chặn ngay tại `cmd_record_review`: receipt thiếu, sai liên kết hoặc đã dùng phải thoát khác 0. Verdict dựng tay vẫn có thể tồn tại như comment, nhưng không được tính thành review có thẩm quyền.

## E3

Danh sách tối thiểu gồm đúng bốn check:

1. **ĐO ĐƯỢC:** Prompt từng trỏ spec không có trong cây reviewer. **SUY LUẬN:** mọi cặp `path + sha256` có cấu trúc trong lease/prompt phải nằm dưới bundle root, tồn tại và đúng băm trước khi gọi model. **SUY LUẬN — đột biến:** bỏ nhánh kiểm tồn tại/băm phải làm ca `missing-cited-spec` ĐỎ và chứng minh model stub không được gọi.

2. **ĐO ĐƯỢC:** Một bundle từng thiếu lease/lát X4. **SUY LUẬN:** script tự dựng closure từ vật lease liệt kê và tự sinh diff từ `base_sha..reviewed_sha`; không nhận diff/bundle ghép tay. **SUY LUẬN — đột biến:** cho phép diff truyền vào hoặc bỏ vật X4 khỏi manifest phải làm ca `incomplete-bundle-x4` ĐỎ.

3. **ĐO ĐƯỢC:** `| tail` từng nuốt mã thoát. **SUY LUẬN:** gọi launcher bằng argv trực tiếp, đọc `run.json` và mã thoát con; con đỏ không được sinh receipt dùng được. **SUY LUẬN — đột biến:** ép mã con thành `0` phải làm ca `child-rc-preserved` ĐỎ.

4. **ĐO ĐƯỢC:** Reviewer `-s read-only` từng không ghi được báo cáo. **SUY LUẬN:** runner phải write/read/delete-probe đích receipt trước khi gọi model và lấy verdict từ stdout do launcher giữ, không bắt reviewer ghi tệp. **SUY LUẬN — đột biến:** bỏ probe phải làm ca `unwritable-output-stops-before-model` ĐỎ.

**SUY LUẬN:** Receipt là dây nối chung, không phải check thứ năm: nó ràng packet/attempt/provider/reviewed SHA, kết quả chuẩn hóa, manifest/run/stdout hash và chỉ được tiêu thụ một lần; `record-review` phải đối chiếu toàn bộ.

**ĐỌC ĐƯỢC:** Prompt được workflow đọc từ head đã đẩy. **SUY LUẬN:** Không đòi PROMPT có ref bền tại lúc cấp; chỉ SPEC thuộc cổng grant-side. Không thêm post-run/tree/read-scope check riêng khi chúng không neo trực tiếp vào bốn sự cố.

## E2

**SUY LUẬN:** Không nên hứa toàn bộ E3 lọt an toàn trong `+300`; cắt thành hai packet `sensitive`, mỗi packet trần cứng `+300`.

**SUY LUẬN — P1a, đi trước:** write set `.claude/dev/packet_loop.py`, `.claude/dev/packet_loop_test.py`, `.claude/skills/cross-review/SKILL.md`. Thêm `review-run` dùng launcher sẵn có, check 3–4, parse output có cấu trúc, ghi receipt một-lần vào state; `record-review` bắt buộc receipt và đối chiếu verdict/finding/SHA. Mutant bỏ receipt gate cũng phải làm ca `record-review-without-receipt` ĐỎ.

**SUY LUẬN:** P1a một mình đã chặn hai sự cố: mã đỏ bị `tail` che không sinh receipt; sandbox read-only vẫn giao verdict qua stdout, còn đích receipt không ghi được thì dừng trước model. Đây không phải “script tùy chọn, siết sau”.

**SUY LUẬN — P1b, kế nhiệm tuần tự:** hai tệp `packet_loop.py` và `packet_loop_test.py`; thêm check 1–2 cùng manifest/hash và hai mutant tương ứng. Không bỏ test hoặc adapter để lách trần.

## E4

**ĐO ĐƯỢC:** Slice A đã land; phần lớn Slice B cũng đã land, nhưng packet C còn lại chưa xong: hai mục nợ chưa có trong `ops/NO_KY_THUAT.md`, và chưa có ca máy khóa năm dạng lọt của docstring `t34`.

**ĐO ĐƯỢC:** `t34` nằm trong `ops/lease_publish_test.py`; gói grant-side SPEC cũng phải sửa chính tệp này.

**ĐỌC ĐƯỢC:** ADR-0044 và quyết định Q4 đặt gói `lease_publish` sau cả Slice A/B.

**SUY LUẬN:** **Chưa mở song song P1 với gói grant-side ngay bây giờ.** Mở P1 song song với packet C còn lại. Sau khi C land, gói `spec_path + spec_sha256 + ref bền, rc=6` có thể chạy song song với P1 nếu P1 vẫn mở, vì write set khi ấy rời nhau.

## CHOT

**SUY LUẬN:** Packet 1 là P1a: `packet_loop review-run` bắt buộc, receipt một-lần và `record-review` fail-đóng; write set ba tệp `.claude` nêu ở E2; class `sensitive`; trần cứng `+300`. P1b nối tiếp để hoàn tất bundle checks. **SUY LUẬN:** Hiện mở P1 + packet C, không mở P1 + gói grant-side; sau C land thì hai gói sau có thể song song. **ĐO ĐƯỢC:** Không tệp nào được tạo hoặc sửa.

## TOI_KHONG_KY

1. **SUY LUẬN:** Helper tùy chọn trong `ops/` trong khi `record-review` vẫn nhận lượt thủ công.

2. **SUY LUẬN:** Phân loại `systemic` cho thay đổi điều kiện vào `accepted`.

3. **SUY LUẬN:** Nhét bốn check, receipt gate và mutant vào `+300` bằng cách bỏ test hoặc hạ phép kiểm.

4. **ĐỌC ĐƯỢC:** Đòi PROMPT resolve từ ref bền tại lúc cấp là báo động giả cấu trúc.

5. **SUY LUẬN:** Mở gói grant-side trước khi phần còn lại của Slice B land.

## KHONG_DO_DUOC

- **ĐỌC ĐƯỢC:** Chưa có diff nên chưa đo được numstat thật của P1a/P1b; `+300` là hard stop thiết kế, không phải lời khai đã đạt.

- **ĐỌC ĐƯỢC:** Chưa có bằng chứng OS cưỡng chế closed-read scope; receipt phải khai `read_scope_enforced: false`.

- **ĐỌC ĐƯỢC:** Không đo được Issue, lease và branch protection hiện hành ngoài worktree; quyết định mở packet vẫn cần authority bền của người giữ kho.
tokens used
242,100
