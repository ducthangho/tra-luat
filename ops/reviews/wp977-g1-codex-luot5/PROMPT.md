# Cross-review Codex — packet #977 (`MAY-ADR-0054-b2`) revision 1 — lượt 5 (xác minh merge, lượt cuối trước khi đẩy)

Bạn là **reviewer độc lập, offline** cho Packet #977, revision 1, generation 1. Executor là Claude (họ `claude`);
bạn là Codex (họ `openai`) ⇒ `assurance_target: cross_approved`, `review_class: sensitive` (văn bản protocol). Không kế thừa
context executor. Không truy cập mạng, không GitHub, không push. Bạn KHÔNG sửa tệp của packet; mọi phép thử chạy trên **bản
sao riêng** dưới `OUT/`.

## Định danh (tự kiểm, đừng tin bảng này)

- `SRC` = thư mục `src/` cạnh tệp prompt này: clone thường (`.git` là thư mục, không nông), detached tại head ứng viên
  **`4c73081474b1e2ab0800cc13992c8f86688532ed`**. Base = **`ef34d88838bc125727670f494b15213b6c6f0c8d`**
  (`origin/master` mới; ref `refs/remotes/origin/master` trong clone trỏ base). Các head đã approve trước:
  lượt 1 `e05ea6a11eb689e1cebb11b417a56930cec8f11e`, lượt 2 `7c789142ce2a2599fd034a57faa5a6661001ec5f`,
  lượt 3 `bd5a66ab01823d6775e1673e64c7da42f7e80135`, lượt 4 `c3124e5ad50810a725048aee6913b032855a75d5` (đều có trong object store).
  Thứ định danh tệp là **băm/SHA**.
- `OUT` = thư mục `out/` cạnh tệp prompt này, là nơi DUY NHẤT bạn ghi.
- Đặc tả con `tham-chieu/wp977.md`, sha256 `adaf8d2469ac16c46314c3c9ac7667cce90825a053a7b98e12b803c6719040c3`.
- Phần chung `SRC/ops/specs/may-adr-0054-chung.md`, sha256 `4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0`.
- Lease (bản chép) `tham-chieu/lease-wp977-r1-g1-claude.yaml`. Write set code: đúng 1 tệp `docs/PROTOCOL_DA_PHIEN.md`, ≤ 40 dòng thêm.

## Vì sao có lượt 5 (ADR-0052: từ lượt hai phải nêu lý do)

- Lượt 1–4 (`tham-chieu/wp977-g1-codex-luot{1,2,3,4}-VERDICT.md`) đều approve, 0 P0–P3. Lượt 2–4 là xác minh merge vì master tiến.
- Sau lượt 4, `origin/master` tiến lần năm từ `b3decc5` lên `ef34d88` (PR #990, #984). Executor merge `ef34d88` (không rebase)
  thành `4c73081`. Chưa có gì được đẩy. Theo khai của executor, đoạn mới đổi `ops/kiem_ho_so_land.py`,
  `ops/kiem_ho_so_land_test.py`, `ops/codex_cloud_setup_test.py` cùng một số tệp ngoài, không đụng `docs/`, `.claude/`,
  `.github/` — hãy tự đo.
- Chủ kho duyệt (27-10, trong phiên executor): vì master tiến nhanh hơn một vòng suite 60 phút, lượt này là lượt xác minh cuối rồi
  đẩy ngay; N/N của `packet_loop_test.py` trên đúng head đẩy sẽ lấy từ job CI `ci.yml`, không chạy lại suite cục bộ.

Lượt này là **biên nhận xác minh merge** cho riêng đoạn `b3decc5..ef34d88`, không review lại từ đầu:

(a) xác nhận blob `docs/PROTOCOL_DA_PHIEN.md` tại `4c73081` giống TỪNG BYTE blob tại `e05ea6a`, `7c78914`, `bd5a66a`, `c3124e5`
    (so OID); base là tổ tiên head; `git diff ef34d88 4c73081` có đúng 1 tệp ấy, ≤ 40 dòng thêm;
(b) đọc `git diff --stat b3decc5 ef34d88` và đánh giá liệu nó có làm SAI một mệnh đề của đoạn §4 mới / câu §12 không, hoặc làm đổi
    kết quả nghiệm thu (đặc biệt: có tệp nào dưới `docs/`, `.claude/`, `.github/` đổi không; `ops/kiem_ho_so_land.py` có đọc hay khai
    điều gì về `cho_chu_kho`/`mo-lai`/`chu-kho-duyet`/§12 mâu thuẫn với đoạn mới không);
(c) chạy lại nghiệm thu trên head mới: ba phép `rg` của đặc tả (dương trên head, âm trên `git show 09db703:docs/PROTOCOL_DA_PHIEN.md`
    và trên `git show ef34d88:docs/PROTOCOL_DA_PHIEN.md`), `doctrine-scan --root .` và `adr-song --root .` rc=0.

Suite `packet_loop_test.py` (45–60 phút): executor đạt 981/981 trên `e05ea6a`, `f8d7565`, `7c78914`; trên head này N/N lấy từ CI.
Bạn không bắt buộc chạy cả suite, nhưng nên chạy chọn lọc các ca đọc protocol hoặc `ops/` (tìm bằng
`rg -n 'PROTOCOL_DA_PHIEN|kiem_ho_so_land' .claude/dev/packet_loop_test.py`).

Approve khi không còn P0–P2 trên `4c73081`.

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
- Dòng 2: `Reviewed commit: 4c73081474b1e2ab0800cc13992c8f86688532ed`.
- Dòng 3: `Spec sha256: <đủ 64 ký tự>` và `Chung sha256: <đủ 64 ký tự>`.
- Bảng lớp: `slug | hạng P0–P3 | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá` (đếm theo nguyên nhân).
- Kết quả (a)(b)(c), kèm lệnh, rc và bằng chứng dương.

Ngưỡng approve: **không còn P0/P1/P2**. Verdict chỉ neo commit trên, không cấp quyền push, merge hay land.

## Ngoài phạm vi (không tính hạng)

Mọi thay đổi code · các mục khác của protocol · #814, #815, #816 · packet này KHÔNG kích hoạt ADR-0054.
