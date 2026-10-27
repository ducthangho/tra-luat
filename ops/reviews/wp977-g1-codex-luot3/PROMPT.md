# Cross-review Codex — packet #977 (`MAY-ADR-0054-b2`) revision 1 — lượt 3 (xác minh merge)

Bạn là **reviewer độc lập, offline** cho Packet #977, revision 1, generation 1. Executor là Claude (họ `claude`);
bạn là Codex (họ `openai`) ⇒ `assurance_target: cross_approved`, `review_class: sensitive` (văn bản protocol). Không kế thừa
context executor. Không truy cập mạng, không GitHub, không push. Bạn KHÔNG sửa tệp của packet; mọi phép thử chạy trên **bản
sao riêng** dưới `OUT/`.

## Định danh (tự kiểm, đừng tin bảng này)

- `SRC` = thư mục `src/` cạnh tệp prompt này: clone thường (`.git` là thư mục, không nông), detached tại head ứng viên
  **`bd5a66ab01823d6775e1673e64c7da42f7e80135`**. Base = **`c2d84ea7c20e835968b630a4fb1b8daa29ac12c7`**
  (`origin/master` mới; ref `refs/remotes/origin/master` trong clone trỏ base). Head đã approve ở lượt 1 = `e05ea6a11eb689e1cebb11b417a56930cec8f11e`;
  head đã approve ở lượt 2 = `7c789142ce2a2599fd034a57faa5a6661001ec5f` (cả hai có trong object store). Thứ định danh tệp là **băm/SHA**.
- `OUT` = thư mục `out/` cạnh tệp prompt này, là nơi DUY NHẤT bạn ghi.
- Đặc tả con `tham-chieu/wp977.md`, sha256 `adaf8d2469ac16c46314c3c9ac7667cce90825a053a7b98e12b803c6719040c3`.
- Phần chung `SRC/ops/specs/may-adr-0054-chung.md`, sha256 `4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0`.
- Lease (bản chép) `tham-chieu/lease-wp977-r1-g1-claude.yaml`. Write set code: đúng 1 tệp `docs/PROTOCOL_DA_PHIEN.md`, ≤ 40 dòng thêm.

## Vì sao có lượt 3 (ADR-0052: từ lượt hai phải nêu lý do)

- Lượt 1 (`tham-chieu/wp977-g1-codex-luot1-VERDICT.md`) approve `e05ea6a`, 0 P0–P3.
- Lượt 2 (`tham-chieu/wp977-g1-codex-luot2-VERDICT.md`) approve `7c78914`, xác minh hai merge master (`7f19424`, `4488444`), 0 P0–P3.
- Trong lúc executor chạy suite trên `7c78914`, `origin/master` tiến lần ba lên `c2d84ea` (PR #991, #986, #993). Đoạn mới này
  **chạm `.claude/skills/cross-review/SKILL.md`** — một adapter mà `doctrine-scan` đọc. Executor merge `c2d84ea` (không rebase)
  thành `bd5a66a`. Chưa có gì được đẩy.

Lượt này là **biên nhận xác minh merge** cho riêng đoạn `4488444..c2d84ea`, không review lại từ đầu:

(a) xác nhận blob `docs/PROTOCOL_DA_PHIEN.md` tại `bd5a66a` giống TỪNG BYTE blob tại `e05ea6a` và `7c78914` (so OID); base là tổ
    tiên head; `git diff c2d84ea bd5a66a` có đúng 1 tệp ấy, ≤ 40 dòng thêm;
(b) đọc `git diff 4488444 c2d84ea` và đánh giá liệu nó có làm SAI một mệnh đề của đoạn §4 mới / câu §12 không, hoặc làm đổi kết
    quả nghiệm thu: `packet_loop.py` có đổi không; thay đổi ở adapter `cross-review` có mâu thuẫn với protocol §4/§12 không;
(c) chạy lại nghiệm thu trên head mới: ba phép `rg` của đặc tả (dương trên head, âm trên `git show 09db703:docs/PROTOCOL_DA_PHIEN.md`
    và trên `git show c2d84ea:docs/PROTOCOL_DA_PHIEN.md`), `doctrine-scan --root .` và `adr-song --root .` rc=0.

Suite `packet_loop_test.py` (45–60 phút): executor đạt 981/981 trên clone ghim `7c78914` và đang chạy lại trên `bd5a66a` song song
với lượt này. Bạn không bắt buộc chạy cả suite, nhưng nên chạy chọn lọc các ca đọc `.claude/skills/` (tìm bằng
`rg -n 'skills/' .claude/dev/packet_loop_test.py`).

Approve khi không còn P0–P2 trên `bd5a66a`.

## Luật phân hạng (chủ kho — BẮT BUỘC áp)

- Một đột biến độ phủ **MỚI** do reviewer tự dựng mà mã/văn bản vẫn xử lý đúng ở probe A/B ⇒ **P3** (nợ có tên, owner,
  hướng xử lý), KHÔNG xếp P2.
- Chỉ xếp **P2 trở lên** khi: có hành vi sai thật (một mệnh đề văn bản SAI so với mã, khai luật mà mã không cưỡng chế, hay mâu
  thuẫn phần protocol khác); hoặc một đột biến/phản chứng đã nêu ở lượt TRƯỚC vẫn sống; hoặc thiếu mục bắt buộc của
  `muc_tieu`/`nghiem_thu`.
- Nói rõ cho mỗi lớp lý do xếp hạng theo luật này.

## Cách chạy

`export PYTHONDONTWRITEBYTECODE=1`. Nếu git toàn cục có `commit.gpgsign=true`, cô lập bằng
`GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`.

## Dạng verdict — ghi TĂNG DẦN vào `OUT/VERDICT.md`

- Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`.
- Dòng 2: `Reviewed commit: bd5a66ab01823d6775e1673e64c7da42f7e80135`.
- Dòng 3: `Spec sha256: <đủ 64 ký tự>` và `Chung sha256: <đủ 64 ký tự>`.
- Bảng lớp: `slug | hạng P0–P3 | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá` (đếm theo nguyên nhân).
- Kết quả (a)(b)(c), kèm lệnh, rc và bằng chứng dương.

Ngưỡng approve: **không còn P0/P1/P2**. Verdict chỉ neo commit trên, không cấp quyền push, merge hay land.

## Ngoài phạm vi (không tính hạng)

Mọi thay đổi code · các mục khác của protocol · #814, #815, #816 · packet này KHÔNG kích hoạt ADR-0054.
