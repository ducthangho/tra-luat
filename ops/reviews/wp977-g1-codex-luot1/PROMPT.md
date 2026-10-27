# Cross-review Codex — packet #977 (`MAY-ADR-0054-b2`) revision 1 — lượt 1

Bạn là **reviewer độc lập, offline** cho Packet #977, revision 1, generation 1. Executor là Claude (họ `claude`);
bạn là Codex (họ `openai`) ⇒ `assurance_target: cross_approved`, `review_class: sensitive` (văn bản protocol). Bạn không kế thừa
context của executor. Không truy cập mạng, không GitHub, không push. Bạn KHÔNG sửa tệp của packet; mọi phép thử chạy trên
**bản sao riêng** dưới `OUT/`.

## Định danh (tự kiểm, đừng tin bảng này)

- `SRC` = thư mục `src/` cạnh tệp prompt này: clone thường (`.git` là thư mục, không nông), detached tại head ứng viên
  **`e05ea6a11eb689e1cebb11b417a56930cec8f11e`**. Base = **`09db70350414d767b793a71cb630e643f216a1b1`**
  (`origin/master`; ref `refs/remotes/origin/master` trong clone trỏ base). Head ứng viên là commit merge base vào nhánh
  packet, đè lên commit nội dung `8770ab3`. Thứ định danh tệp là **băm/SHA**, không phải tên nhánh.
- `OUT` = thư mục `out/` cạnh tệp prompt này, là nơi DUY NHẤT bạn ghi.
- Đặc tả con `tham-chieu/wp977.md`, sha256 `adaf8d2469ac16c46314c3c9ac7667cce90825a053a7b98e12b803c6719040c3`
  (chỉ có trên nhánh đặc tả nên được chép sang đây; hãy băm lại).
- Phần chung (ràng buộc) `SRC/ops/specs/may-adr-0054-chung.md`, sha256 `4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0`.
- Lease (bản chép) `tham-chieu/lease-wp977-r1-g1-claude.yaml`. Write set của nhánh code: đúng **1** tệp
  `docs/PROTOCOL_DA_PHIEN.md`, chỉ §4 và §12. Diff ≤ 40 dòng thêm.

## Packet này là gì

Chỉ sửa **văn bản**: mô tả trong protocol hành vi mà mã đã có trên master (`.claude/dev/packet_loop.py`, do #813 r2 thêm —
PR #969). Đặc tả cấm thêm luật mà mã chưa cưỡng chế. Vì vậy câu hỏi trung tâm của review là: **mỗi mệnh đề trong đoạn §4
mới có neo đúng vào mã không** — không rộng hơn mã, không hẹp đến mức sai, không mâu thuẫn với phần còn lại của protocol.

## Luật phân hạng (chủ kho — BẮT BUỘC áp từ lượt này)

- Một đột biến độ phủ **MỚI** do reviewer tự dựng mà mã/văn bản vẫn xử lý đúng ở probe A/B ⇒ **P3** (nợ có tên, owner,
  hướng xử lý), KHÔNG xếp P2.
- Chỉ xếp **P2 trở lên** khi: có hành vi sai thật (ở đây: một mệnh đề văn bản SAI so với mã, hoặc khai một luật mà mã không
  cưỡng chế, hoặc mâu thuẫn với phần protocol khác); hoặc một đột biến/phản chứng đã nêu ở lượt TRƯỚC vẫn sống; hoặc thiếu
  một mục bắt buộc của `muc_tieu`/`nghiem_thu`.
- Nói rõ cho mỗi lớp lý do xếp hạng theo luật này. Câu chữ/văn phong mà không sai nghĩa ⇒ P3.

## Việc

1. Băm lại hai đặc tả. Xác nhận base là tổ tiên head. Đọc `git diff 09db703 e05ea6a` (phải đúng 1 tệp) và
   `git diff --numstat` (≤ 40 dòng thêm).
2. Đối chiếu **từng mệnh đề** của đoạn §4 mới và câu §12 với mã trong `SRC/.claude/dev/packet_loop.py`: `cmd_mo_lai`,
   `cmd_chu_kho_duyet`, `_xet_dung`, `CUA_DI_TIEP`, bảng `CHUYEN_HOP_LE` (cạnh `transition`), bất biến `mo-lai` trong `_load`,
   và mọi cửa khác có thể ghi `state` khi đang ở `cho_chu_kho` hoặc `approved_pending`. Với mỗi mệnh đề: neo được (file:dòng)
   hay không. Gợi ý soi (không giới hạn):
   - "rời `cho_chu_kho` chỉ bằng `chu-kho-duyet`": còn cửa nào khác (void-attempt, record-review, record-codex-call, transition,
     rescue) ghi state từ `cho_chu_kho` không?
   - `ci-do`: điều kiện check đỏ thật, attempt/run mới nhất, connector không còn P0–P2 — đúng như văn bản nói?
   - `connector` từ `running`: đủ ba điều kiện (quyền `ci-do` cùng generation, chưa `begin_attempt` sau `mo_lai` cuối, SHA đã mở lại)?
     Văn bản có ngụ ý một phép so head mà mã không làm không?
   - `chu-kho-duyet`: lược đồ, người có thẩm quyền, bốn trường khớp, phạm vi, dùng một lần theo cặp (hiện vật, phạm vi).
   - `cho_phep_day` thật sự chưa có cửa nào tiêu thụ?
   - "cùng qua hàm xét dừng ... về `blocked`": đúng cho cả ba cửa? Có cửa nào trong `CUA_DI_TIEP` bị văn bản bỏ sót hay khai thừa?
   - Câu §12: có làm mâu thuẫn chỗ nào khác của protocol (ví dụ đồ thị state đầu §4, §10.2, §13) không?
3. Chạy nghiệm thu của đặc tả trên `SRC`: ba phép `rg` (dương trên head, âm trên base — dùng `git show 09db703:docs/PROTOCOL_DA_PHIEN.md`),
   `python .claude/dev/packet_loop.py doctrine-scan --root .` và `adr-song --root .` (rc=0). Suite đầy đủ
   `packet_loop_test.py` mất 45–60 phút; executor đã chạy nó trên clone ghim đúng head này — bạn KHÔNG bắt buộc chạy lại, nhưng
   nếu chạy thì chạy chọn lọc các ca đọc protocol (tìm bằng `rg -n 'PROTOCOL_DA_PHIEN' .claude/dev/packet_loop_test.py`).
4. Phản chứng chạy được được khuyến khích: dựng state tối thiểu trên bản chép dưới `OUT/` để kiểm một mệnh đề nghi ngờ (ví dụ thử
   `transition` từ `cho_chu_kho`). Hướng thử nào đòi soạn nội dung dạng đường dẫn thoát khỏi cây thư mục thì **mô tả bằng lời**.

## Cách chạy

- `export PYTHONDONTWRITEBYTECODE=1`. Nếu git toàn cục của sandbox có `commit.gpgsign=true`, cô lập bằng
  `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`.

## Dạng verdict — ghi TĂNG DẦN vào `OUT/VERDICT.md`

- Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`.
- Dòng 2: `Reviewed commit: e05ea6a11eb689e1cebb11b417a56930cec8f11e`.
- Dòng 3: `Spec sha256: <đủ 64 ký tự>` và `Chung sha256: <đủ 64 ký tự>`.
- Bảng lớp, đếm theo nguyên nhân chứ không theo số biểu hiện:
  `slug | hạng P0–P3 | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá`.
- Bảng đối chiếu từng mệnh đề §4/§12 ↔ neo mã (file:dòng) ↔ khớp/không.
- Kết quả các lệnh nghiệm thu đã chạy, kèm rc và bằng chứng dương.

Slug kebab-case ổn định, đặt theo nguyên nhân. Ngưỡng approve: **không còn P0/P1/P2**. P3 còn lại thì nêu tên và hướng xử lý.
Verdict chỉ neo commit trên, không cấp quyền push, merge hay land.

## Ngoài phạm vi (không tính hạng)

- Mọi thay đổi code; các mục khác của protocol ngoài §4/§12.
- Vòng P3 (#814), generation kế tiếp (#815), ghi đẩy và tiêu thụ `checkpoint_day`/`mo_lai_tu` (#816).
- Packet này KHÔNG kích hoạt ADR-0054.
