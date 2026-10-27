# Cross-review Codex — packet #977 (`MAY-ADR-0054-b2`) revision 1 — lượt 4 (xác minh merge)

Bạn là **reviewer độc lập, offline** cho Packet #977, revision 1, generation 1. Executor là Claude (họ `claude`);
bạn là Codex (họ `openai`) ⇒ `assurance_target: cross_approved`, `review_class: sensitive` (văn bản protocol). Không kế thừa
context executor. Không truy cập mạng, không GitHub, không push. Bạn KHÔNG sửa tệp của packet; mọi phép thử chạy trên **bản
sao riêng** dưới `OUT/`.

## Định danh (tự kiểm, đừng tin bảng này)

- `SRC` = thư mục `src/` cạnh tệp prompt này: clone thường (`.git` là thư mục, không nông), detached tại head ứng viên
  **`c3124e5ad50810a725048aee6913b032855a75d5`**. Base = **`b3decc512dd6e0247ec2439870bd06725d79f028`**
  (`origin/master` mới; ref `refs/remotes/origin/master` trong clone trỏ base). Các head đã approve trước:
  lượt 1 `e05ea6a11eb689e1cebb11b417a56930cec8f11e`, lượt 2 `7c789142ce2a2599fd034a57faa5a6661001ec5f`,
  lượt 3 `bd5a66ab01823d6775e1673e64c7da42f7e80135` (đều có trong object store). Thứ định danh tệp là **băm/SHA**.
- `OUT` = thư mục `out/` cạnh tệp prompt này, là nơi DUY NHẤT bạn ghi.
- Đặc tả con `tham-chieu/wp977.md`, sha256 `adaf8d2469ac16c46314c3c9ac7667cce90825a053a7b98e12b803c6719040c3`.
- Phần chung `SRC/ops/specs/may-adr-0054-chung.md`, sha256 `4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0`.
- Lease (bản chép) `tham-chieu/lease-wp977-r1-g1-claude.yaml`. Write set code: đúng 1 tệp `docs/PROTOCOL_DA_PHIEN.md`, ≤ 40 dòng thêm.

## Vì sao có lượt 4 (ADR-0052: từ lượt hai phải nêu lý do)

- Lượt 1–3 (`tham-chieu/wp977-g1-codex-luot{1,2,3}-VERDICT.md`) đều approve, 0 P0–P3. Lượt 2 và 3 là xác minh merge vì master tiến.
- Sau lượt 3, `origin/master` tiến lần bốn từ `c2d84ea` lên `b3decc5` (PR #982, hồ sơ land #813). Executor merge `b3decc5` (không
  rebase) thành `c3124e5`. Chưa có gì được đẩy. Theo khai của executor, đoạn mới chỉ thêm tệp dưới `ops/land/` — hãy tự đo.

Lượt này là **biên nhận xác minh merge** cho riêng đoạn `c2d84ea..b3decc5`, không review lại từ đầu:

(a) xác nhận blob `docs/PROTOCOL_DA_PHIEN.md` tại `c3124e5` giống TỪNG BYTE blob tại `e05ea6a`, `7c78914`, `bd5a66a` (so OID);
    base là tổ tiên head; `git diff b3decc5 c3124e5` có đúng 1 tệp ấy, ≤ 40 dòng thêm;
(b) đọc `git diff --stat c2d84ea b3decc5` và đánh giá liệu nó có làm SAI một mệnh đề của đoạn §4 mới / câu §12 không, hoặc
    làm đổi kết quả nghiệm thu (đặc biệt: có tệp nào dưới `docs/`, `.claude/`, `.github/`, `ops/*.py` đổi không; hồ sơ land #813
    có khai điều gì về `cho_chu_kho`/`mo-lai`/`chu-kho-duyet` mâu thuẫn với đoạn §4 mới không);
(c) chạy lại nghiệm thu trên head mới: ba phép `rg` của đặc tả (dương trên head, âm trên `git show 09db703:docs/PROTOCOL_DA_PHIEN.md`
    và trên `git show b3decc5:docs/PROTOCOL_DA_PHIEN.md`), `doctrine-scan --root .` và `adr-song --root .` rc=0.

Suite `packet_loop_test.py` (45–60 phút): executor chạy trên clone ghim `c3124e5` song song với lượt này. Bạn không bắt buộc chạy.

Approve khi không còn P0–P2 trên `c3124e5`.

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
- Dòng 2: `Reviewed commit: c3124e5ad50810a725048aee6913b032855a75d5`.
- Dòng 3: `Spec sha256: <đủ 64 ký tự>` và `Chung sha256: <đủ 64 ký tự>`.
- Bảng lớp: `slug | hạng P0–P3 | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá` (đếm theo nguyên nhân).
- Kết quả (a)(b)(c), kèm lệnh, rc và bằng chứng dương.

Ngưỡng approve: **không còn P0/P1/P2**. Verdict chỉ neo commit trên, không cấp quyền push, merge hay land.

## Ngoài phạm vi (không tính hạng)

Mọi thay đổi code · các mục khác của protocol · #814, #815, #816 · packet này KHÔNG kích hoạt ADR-0054.
