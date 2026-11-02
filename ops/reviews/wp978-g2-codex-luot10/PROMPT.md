# Cross-review Codex — packet #978 (`CI-PROVENANCE-COMMIT-ENCODING`) revision 2 — lượt 10 (lời gọi CUỐI, 10/10)

Bạn là **reviewer độc lập, offline** cho Packet #978, revision 2, generation 2 (lease `wp978-r2-g2-claude`).
Executor là Claude (họ `claude`); bạn là Codex (họ `openai`) ⇒ `assurance_target: cross_approved`,
`review_class: sensitive`. Không mạng, không GitHub, không push. KHÔNG sửa `SRC`; mọi phép thử chạy trên bản sao
riêng dưới `OUT/`. Trần 10 lời gọi theo `ADR-0055`; đây là lời gọi cuối.

**Ưu tiên kết luận:** viết `OUT/VERDICT.md` SỚM, cập nhật dần; dòng 1 luôn là kết luận tốt nhất theo bằng chứng đã đo.
KHÔNG chạy suite mặc định đầy đủ; executor chạy nó trên clone riêng của đúng head.

## Ngưỡng hạng (giữ từ lượt 8–9)

- **P1/P2 (chặn approve):** lỗi SẢN PHẨM; vi phạm hợp đồng; hồi quy tiêu chí nghiệm thu; ca/đột biến cấp TÍN DỤNG GIẢ
  hoặc kỳ vọng test SAI; bộ chạy đột biến trả `HONG`; **ca mất răng** (phép kiểm trước đây đỏ nay không đỏ nữa).
- **P3 (không chặn, phải liệt kê):** đột biến không tương đương còn sống mà sản phẩm vẫn đúng. Nợ
  `wp978-git-reader-differential-fuzz`, owner `ducthangho`.

## Định danh (tự kiểm)

- `SRC` = `src/`, detached tại head ứng viên **`db2c1f50bee7c866ad9bea01a3895842bd85cb69`**, cha **`aebc808ea45408c827e753827b97f94689969db5`**
  (lượt 9 đã **approve** `aebc808`, verdict ở `tham-chieu/luot9-VERDICT.md`). `refs/remotes/origin/master` = `9091cf52cf20ac197c1a356d6a33cac6bab0b318`.
- `OUT` = `out/`, nơi DUY NHẤT bạn ghi. Đặc tả `tham-chieu/specs-wp978-r2.md` sha256
  `9fe94ad05cc1129e663cf77706db92685d6130c08c6a375454781a9aca188060`.

## Vì sao có `db2c1f5` (lời khai executor — tự đo)

Chạy trên **Windows thật** (VM `tra-luat-win`, Python 3.12.10, Git for Windows, 2 vCPU), suite mặc định của `aebc808`
chết `subprocess.TimeoutExpired` trong `chay_con(c62_git_commit_khong_utf8)` (timeout 300 s của bộ chạy đột biến).
Đo `--mot-ca c62_git_commit_khong_utf8` trên cùng máy, cùng tải: `aebc808` **482 s**, `db2c1f5` **186 s**, cả hai rc 0.
Linux: ~6,9 s → ~1,9 s. Nguyên nhân: ~2.200 tiến trình git mỗi lần chạy ca (Windows spawn đắt).

`aebc808` → `db2c1f5` chỉ đổi `ops/ci_provenance_test.py`, trong thân `c62`, +20/-4:
1. `cm(b)` (không `--literally`) KHÔNG gọi git ngay: đẩy bytes vào `cho`, trả OID tính trước bằng
   `sha1(b"commit %d\0" % len(b) + b)`. Trước khi dựng blob/tag, ghi cả lượt bằng
   `git hash-object -t commit -w --stdin-paths` (mỗi commit một tệp trong thư mục tạm) và `bang(...)` đòi danh sách OID
   Git trả về == danh sách OID tính trước. `cm(..., ("--literally",))` vẫn gọi lẻ như cũ.
2. Oracle Git native: thay `git log -1 --no-walk` từng commit bằng MỘT `git log --no-walk=unsorted --stdin
   --format=%H%x00%T%x00%P` mỗi kho (SHA-1 và SHA-256), lập `nat[oid]`.
3. Phép so oracle dùng lại `kq[i]` (đầu ra reader đã đo ở dòng `bang(kq == mong, ...)`) thay vì gọi `doc()` lần hai.

Executor đã đo (Linux): `--mot-ca c62` rc 0; với `CI_PROVENANCE_MA=<ops/ci_provenance.py tại c8d92ba>` rc 3, có
`DO:c62_…:git_cuc_bo` và `UnicodeDecodeError`. Năm đột biến TEST do executor tự dựng: `nat` cắt parent ⇒ rc 3;
`nat` parent rỗng ⇒ rc 3; OID tính sai công thức ⇒ rc 3; **bỏ phép so OID ghi ⇒ rc 0 (sống)**; **bỏ một phần tử
khỏi vòng oracle ⇒ rc 0 (sống)**. Executor cho rằng hai survivor này là tương đương/độ phủ (OID sai đã bị bắt ở
`kq == mong`; bỏ một phần tử oracle cũng sống ở bản cũ). **Hãy kiểm lời khai này**, nhất là: (a) bản cũ có bắt được
"bỏ một phần tử oracle" không; (b) có đường nào khiến OID tính trước đúng mà object ghi sai/không ghi mà test vẫn xanh.

## Việc (viết VERDICT sau mỗi bước)

1. Băm đặc tả; xác nhận `db2c1f5` cha `aebc808`; `git -C src diff aebc808 db2c1f5`.
2. **Tương đương ngữ nghĩa** của ba thay đổi với bản `aebc808`: cùng tập commit được ghi, cùng kỳ vọng, cùng phép so
   oracle; `--no-walk=unsorted --stdin` có bỏ sót OID trùng/thứ tự không; tách dòng `\0` có an toàn với `%P` rỗng
   (commit gốc nằm trong oracle chỉ khi kỳ vọng là dict — kiểm); `nat.get(x)` thiếu khoá có làm phép so đỏ không.
   `--stdin-paths` với đường dẫn Windows (`\`, ổ đĩa) và với `core.autocrlf=true` có đổi byte object không.
3. **Răng:** chạy lại mọi đột biến `F13_*` (55) và `B2_*` (6) qua `chay_dot_bien` như lượt 9 — tất cả phải `GIET`
   đúng ca; N1′ trên reader `c8d92ba`. So kết quả với lượt 9.
4. Đột biến test của executor (mục trên) và đột biến riêng của bạn trên ba thay đổi.
5. Thời gian: đo `--mot-ca c62` trên `aebc808` và `db2c1f5` (Linux) để xác nhận chiều giảm; không suy ra số Windows.
6. Bảng N1′–N3′, N4–N7 như lượt 9 (N3′ của bạn `not_run`; N6 `not_measured`; N7 không áp dụng).
7. Hướng thử nào đòi soạn nội dung dạng đường dẫn thoát khỏi cây thư mục thì **mô tả bằng lời**, đừng tự soạn.

## Cách chạy

`export PYTHONDONTWRITEBYTECODE=1`; `TMPDIR=$PWD/out/tmp`; `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null` khi cần.

## Dạng verdict — `OUT/VERDICT.md`

- Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`.
- Dòng 2: `Reviewed commit: db2c1f50bee7c866ad9bea01a3895842bd85cb69`.
- Dòng 3: `Spec sha256: <đủ 64 ký tự của spec r2>`.
- `ĐỐI CHIẾU LƯỢT TRƯỚC`; bảng lớp (`slug | hạng | file:dòng | phép đo | hướng vá`); mỗi P3 ghi nợ có tên, owner,
  hướng xử lý; bảng nghiệm thu kèm rc và bằng chứng dương.

Ngưỡng approve: **P0 = P1 = P2 = 0**. Verdict chỉ neo commit trên, không cấp quyền push, merge hay land.

## Ngoài phạm vi

D02, F10/D05 của #899; `.claude/dev/ci_dang_ky_test.py`; mốc Workflow definition; LIVE CI; Windows native (executor
đo riêng); nội dung master ngoài hai tệp; `chay_con` timeout 300 s của master (không thuộc diff).
