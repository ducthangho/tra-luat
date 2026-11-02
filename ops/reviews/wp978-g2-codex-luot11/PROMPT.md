# Cross-review Codex — packet #978 (`CI-PROVENANCE-COMMIT-ENCODING`) revision 2 — lượt 11 (lời gọi 11/11)

Bạn là **reviewer độc lập, offline** cho Packet #978, revision 2, generation 2 (lease `wp978-r2-g2-claude`).
Executor là Claude (họ `claude`); bạn là Codex (họ `openai`) ⇒ `assurance_target: cross_approved`,
`review_class: sensitive`. Không mạng, không GitHub, không push. KHÔNG sửa `SRC`; mọi phép thử chạy trên bản sao
riêng dưới `OUT/`. Chủ kho nâng trần lời gọi Codex từ 10 lên **11** ngày 02-11-2026 để xác minh đúng commit này;
đây là lời gọi cuối.

**Ưu tiên kết luận:** viết `OUT/VERDICT.md` SỚM, cập nhật dần; dòng 1 luôn là kết luận tốt nhất theo bằng chứng đã đo.
KHÔNG chạy suite mặc định đầy đủ; executor chạy nó trên clone riêng của đúng head.

## Ngưỡng hạng (giữ từ lượt 8–10)

- **P1/P2 (chặn approve):** lỗi SẢN PHẨM; vi phạm hợp đồng; hồi quy nghiệm thu; ca/đột biến cấp TÍN DỤNG GIẢ hoặc kỳ
  vọng test SAI; bộ chạy đột biến trả `HONG`; ca mất răng; chốt mới tự đỏ giả (flaky, phụ thuộc nền/cấu hình).
- **P3 (không chặn, phải liệt kê):** đột biến không tương đương còn sống mà sản phẩm vẫn đúng. Nợ
  `wp978-git-reader-differential-fuzz`, owner `ducthangho`.

## Định danh (tự kiểm)

- `SRC` = `src/`, detached tại head ứng viên **`516a33467b1212a90153bb25ed44f28b16d5fac9`**.
  Chuỗi: `e5ca45b` → `ad0d3a1` → `b659eae` → head. `refs/remotes/origin/master` = `9091cf52cf20ac197c1a356d6a33cac6bab0b318`.
- **Lượt trước neo theo commit KHÁC SHA nhưng CÙNG TREE**, tự kiểm bằng `git rev-parse <x>^{tree}`:
  - `ad0d3a1` (do một phiên khác đẩy lên nhánh PR) có tree `77f4b6c8…` = tree của `aebc808` (lượt 9 approve);
  - `b659eae` (cherry-pick của executor lên trên `ad0d3a1`) có tree `3676c40e…` = tree của `db2c1f5` (lượt 10 approve).
  - Hai commit tham chiếu có trong object store tại `refs/tham-chieu/aebc808` và `refs/tham-chieu/db2c1f5`.
- `OUT` = `out/`, nơi DUY NHẤT bạn ghi. Đặc tả `tham-chieu/specs-wp978-r2.md` sha256
  `9fe94ad05cc1129e663cf77706db92685d6130c08c6a375454781a9aca188060`. Verdict trước: `tham-chieu/luot9-VERDICT.md`,
  `tham-chieu/luot10-VERDICT.md`.

## Lời khai executor (tự đo)

`b659eae` → head chỉ đổi thân `c62_git_commit_khong_utf8` trong `ops/ci_provenance_test.py`, +10/-5. Mục tiêu là đóng ba P3
của lượt 10:
1. `git-reader-oracle-coverage-unlocked`: `da_so` đếm số mục đã so với Git native, rồi
   `bang(da_so == sum(type(k) is dict for _, k in ca) + 1)`. Số kỳ vọng đếm độc lập từ `ca`, không từ `hop`.
2. và 3. `git-reader-write-receipt-assertion-unlocked`, `git-reader-negative-fixture-existence-unchecked`: `cm()` ghi
   `so_dung.append((oid, len(b)))` lúc dựng, cho cả commit thường lẫn `--literally`. Sau lượt ghi, một lần
   `git cat-file --batch-check` trên mọi OID trong `so_dung` phải trả đúng `"<oid> commit <cỡ>"`.

Phản chứng executor đo trên Linux, `--mot-ca c62`:

| Đột biến | rc | Thông báo |
|---|---|---|
| bỏ mục oracle đầu (`hop[1:]`) | 3 | `oracle chỉ so 454 mục` |
| bỏ mục SHA-256 khỏi vòng so | 3 | `oracle chỉ so 454 mục` |
| gỡ chốt OID và đổi byte fixture #25 lúc ghi | 3 | `… missing` |
| gỡ chốt OID và bỏ ghi fixture #25 | 3 | `… missing` |
| gỡ riêng từng chốt mới (đếm / tồn tại / OID) | 0 | — |

Executor cho rằng dòng cuối là tương đương: chốt không bắn trên head đúng. Hãy kiểm lời khai này.

## Việc (viết VERDICT sau mỗi bước)

1. Băm đặc tả; xác nhận chuỗi commit và hai đẳng thức tree; `git -C src diff b659eae HEAD`.
2. Ba P3 lượt 10 đã ĐÓNG thật chưa: tái dựng chính các biến thể của lượt 10 trên head, mỗi biến thể phải đỏ đúng ca
   (`DO:c62_…`). Ghi rõ biến thể nào còn sống.
3. Chốt mới có tự đỏ giả không: thứ tự `--batch-check` đầu ra, OID trùng trong `so_dung` (fixture trùng byte),
   `--literally`, cỡ object, `core.autocrlf=true`, TMPDIR có khoảng trắng/Unicode. Các chốt mới có đổi gì ở ngữ nghĩa hay
   kỳ vọng cũ không.
4. Răng của catalogue: 55 `F13_*` + 6 `B2_*` qua `chay_dot_bien` phải `GIET` đúng ca; N1′ trên reader `c8d92ba`.
5. Thời gian `--mot-ca c62` Linux trên `b659eae` và head (chi phí thêm của `--batch-check`).
6. Bảng N1′–N3′, N4–N7 như lượt 10 (N3′ của bạn là `not_run`; N6 `not_measured`; N7 không áp dụng).
7. Hướng thử nào đòi soạn nội dung dạng đường dẫn thoát khỏi cây thư mục thì **mô tả bằng lời**, đừng tự soạn.

## Cách chạy

`export PYTHONDONTWRITEBYTECODE=1`; `TMPDIR=$PWD/out/tmp`; `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null` khi cần.

## Dạng verdict — `OUT/VERDICT.md`

- Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`.
- Dòng 2: `Reviewed commit: 516a33467b1212a90153bb25ed44f28b16d5fac9`.
- Dòng 3: `Spec sha256: <đủ 64 ký tự của spec r2>`.
- `ĐỐI CHIẾU LƯỢT TRƯỚC`; bảng lớp (`slug | hạng | file:dòng | phép đo | hướng vá`); mỗi P3 còn mở ghi nợ có tên, owner,
  hướng xử lý; bảng nghiệm thu kèm rc và bằng chứng dương.

Ngưỡng approve: **P0 = P1 = P2 = 0**. Verdict chỉ neo commit trên, không cấp quyền push, merge hay land.

## Ngoài phạm vi

D02, F10/D05 của #899; `.claude/dev/ci_dang_ky_test.py`; mốc Workflow definition; LIVE CI; Windows native (executor đo
riêng trên `tra-luat-win`); nội dung master ngoài hai tệp; timeout 300 s của `chay_con` (code master, không thuộc diff).
