# Review chéo lượt 2/2 — `DONREF-XOA-AN-TOAN` (#217)

## Đối chiếu mỏ neo
- `sha256sum DAC_TA.md` = `1add3edf165faa2b53d6b52212ea34d7a73934367fd73bbca91e5518a9a664de` — khớp chính xác chuỗi trong prompt. Đặc tả không đổi ở lượt này.
- `.git/HEAD` trong `kho/` = `5f2ff8573ed259c1a4df3030428a4ec9b0f99e2e` — khớp "exact head". `git log --oneline -5` xác nhận đây là commit trên đúng nhánh, cha là `fa4b0dd8` (head lượt 1).
- `git status --porcelain=v1 -uall` rỗng — không có gì lấn cấn trong working tree.
- `git diff --stat fa4b0dd8..5f2ff857` = đúng **một tệp** `ops/nhanh_don_duoc_test.py`, `41 insertions(+), 18 deletions(-)` — khớp write set khai trong prompt.
- Đã tự chạy `git diff fa4b0dd8..5f2ff857 -- ops/nhanh_don_duoc_test.py` và `diff -u` với `diff_delta.patch` cung cấp: **byte-identical** (exit 0). Patch đưa cho tôi đúng là patch thật, không bị chỉnh sửa.
- **Không tin câu "mã sản phẩm không đổi byte nào" — đã đo bằng blob hash, không đọc diff**: `git rev-parse <sha>:ops/nhanh_don_duoc.py` ở cả hai commit đều ra `bc9f47860a80ea0bd569e9773bb0664f197b5bf1`. Xác nhận: byte-identical.

## Đã đo và sạch

**§3.5 — chạy thật, đọc rc trực tiếp (không qua ống):** dựng bản sao độc lập từ `git archive 5f2ff857`, tự `git init` một work-tree rồi chạy `python3 ops/nhanh_don_duoc_test.py` bằng `subprocess.run` (không pipe). Kết quả thật:
```
CASE T1..T8: DAT (8/8)
MUTANT dao-chieu-to-tien        | T1        | 1/1
MUTANT bo-kiem-commit-rieng     | T2        | 1/1
MUTANT noi-B-thanh-mot-commit   | T3        | 1/1
MUTANT loi-thanh-khong-commit-rieng | T4    | 1/1
MUTANT in-ca-C                  | T3,T5,T8  | 3/3
MUTANT bo-loai-mac-dinh         | T6        | 1/1
MUTANT xoa-khai-gioi-han        | T7        | 1/1
MUTANT bo-chan-fetch-loi        | T8        | 1/1
MUTANT go-nhanh-kho-nong        | T5        | 1/1
MUTANT dao-khop-base-remote     | T1,T3,T6  | 3/3
8/8
RC = 0
```
Hai số bằng nhau, không hồi quy. Bảy mutant cũ vẫn giết đúng ca cũ (một mutant — `in-ca-C` — mở rộng tập giết từ `{T5}` sang `{T3,T5,T8}`, đúng như DOT_BIEN khai lại; đây là mở rộng độ phủ do vá T3, không phải lỗi).

**§3.1 — `T8` đo THẬT, không chỉ CÓ MẶT:**
- Kho `remote` trong `T8` được dựng bằng `git init --bare` ở `kho_bare()`, và chính `T8` tự khẳng định lại độc lập: `assert run(["git","rev-parse","--is-bare-repository"], remote).stdout.strip() == "true"` — không tin cấu trúc thư mục, đo bằng git.
- Điều kiện A của `ops/a` (nhánh cũ, tách tại commit `S` trước khi `D` được thêm vào mặc định) được xác nhận **bằng git độc lập, không qua phép phân loại của tool**: `git rev-list --count base..tip == "0"` và `git merge-base --is-ancestor tip base` (rc=0) — cả hai chạy TRƯỚC khi phá remote.
- Sau khi `remote.rename(...)` (phá đường fetch): assert **cả hai** hậu điều kiện, không chỉ một — `nhom["ops/a"][0] == "C" and "fetch loi:" in nhom["ops/a"][1]` (đúng nhóm, đúng lý do) **và** `"ops/a" not in lenh` (không lọt lệnh xoá).
- Không có nhánh "không thấy thì bỏ qua" nào trong `T8` — mọi bước đều `assert` cứng, không `return` sớm kiểu `t24`. `tool()` cũng fail loud (`raise AssertionError`) khi `rc != 0` hoặc không tìm thấy dòng `git push `.
- Tự dựng lại đúng scenario này (đọc lại `VERDICT_LUOT_1.md` §3.5 của chính tôi) khớp 100% với những gì `T8` giờ làm — executor đã đóng đúng khoảng trống P2, không phải đóng bằng thứ khác.

**§3.2 — ba mutant mới nhắm đúng chỗ, có răng:**
- `bo-chan-fetch-loi` (`if fetch.returncode:` → `if False:`): neo xuất hiện đúng 1 lần trong `product.py` (harness tự assert `text.count(neo)==1`, chạy thật không lỗi ⇒ xác nhận). Gỡ nó ra khỏi mã thật vẫn còn dòng, nên đây không phải no-op.
- `go-nhanh-kho-nong` (xoá khối `elif shallow: ...`): neo là khối 2 dòng chính xác trong `main()`, thay bằng chuỗi rỗng — đã xác minh đây là **khối duy nhất** xử lý biến `shallow`.
- `dao-khop-base-remote` (`base_oid != remote_oid` → `base_oid == remote_oid`): neo xuất hiện đúng 1 lần, đúng dòng `elif loi_head or base_oid != remote_oid:`.
- Cả ba đều được chạy THẬT qua `chay_dot_bien()` (archive→tar cô lập từng bản sao, `sys.dont_write_bytecode=True` + `PYTHONDONTWRITEBYTECODE=1` chặn đúng bẫy `.pyc` đã trả giá trước đây) — kết quả khớp `1/1` từng con, không con nào "không bao giờ chạy tới dòng nó sửa" (nếu vậy `chay_dot_bien` đã tự raise `AssertionError` vì `text.count(neo) != 1` hoặc mutant không giết đúng ca, và cả hai đều tự làm `rc != 0`).

**§3.3 — hai mutant giết nhiều ca: đã kiểm, không phải ca-chưa-tách:**
- `dao-khop-base-remote` lật cờ tương đương "coi trạng thái KHỎE MẠNH (base khớp remote) là lỗi" — điều này phá vỡ MỘT tiền điều kiện dùng chung bởi T1 (đo nhóm A), T3 (đo nhóm B + lọc C), T6 (đo loại trừ mặc định) — ba test đo ba hành vi khác nhau của `phan_loai`, chỉ tình cờ đều cần "không có `loi_chung`" làm tiền đề. Không phải ba ca đo trùng một thứ.
- `in-ca-C` phá bỏ chốt loại C khỏi lệnh — bất kỳ ca nào có ít nhất một nhánh nhóm C SẼ bị lộ (T3, T5, T8 đều có). Đây cũng là tiền-điều-kiện dùng chung, không phải trùng lặp.
- Executor đã tự khai đúng hai mutant này trong bảng ở `nhiem_vu.txt` — khớp doctrine "giết nhiều ca ⇒ phải nói ra".

**§3.4 — kiểm lời khai bằng đo, không nhận cho xong:**
- `grep -n "rc=1\|return 1\|returncode == 1"` trên `test_new.py`: **chỉ một** chỗ `return 1`, tại `main()` dòng cuối tệp — đó là mã thất bại của **chính test runner** khi có ca ĐỎ (`if do: ... return 1`), hoàn toàn không liên quan câu "trên kho nông thì `rc=1`" trong `nhiem_vu.txt`. Lời khai của executor **đúng** — `nhiem_vu.txt` (không thuộc write_set) sai, tool thật chỉ `return 0`/`return 2`, và không có gì trong write_set khẳng định `rc=1` cho kịch bản shallow.
- Blob hash `ops/nhanh_don_duoc.py` — đã đo ở trên, khớp.

**Finding P3(b) của tôi (T3 thiếu assert loại C):** đã vá đúng — dòng mới `assert nhom["ops/c-mot"][0] == "C" and "ops/c-mot" not in lenh` xuất hiện trong `T3`, và mutant `in-ca-C` giờ giết cả T3 (xác nhận qua chạy thật ở trên: T3 nằm trong `3/3`).

## Quan sát phụ — không chặn duyệt
`bo-chan-fetch-loi` giết `T8` một phần nhờ trùng hợp: trong đúng fixture của `T8`, phá `remote` làm **cả** `git fetch` **lẫn** `git ls-remote --symref origin HEAD` (dùng trong `_mac_dinh`) cùng thất bại — nên khi tắt nhánh `if fetch.returncode:`, nhánh `elif loi_head or ...` vẫn bắt được (dù thông điệp lý do đổi, và chính vì thông điệp đổi mà assert của `T8` — đòi cụm `"fetch loi:"` — bị lật, nên mutant vẫn bị giết). Không có ca nào cô lập tình huống "fetch lỗi ĐỘC LẬP trong khi `ls-remote HEAD` vẫn thành công" (ví dụ fetch lỗi vì ghi `.git/objects` cục bộ hỏng, còn mạng vẫn tốt) — một khoảng trống RĂNG rất hẹp, không phải lỗ an toàn (nếu xảy ra, nhánh vẫn rơi vào C qua đường khác hoặc bị `T8` bắt gián tiếp như hiện tại). Không yêu cầu vá thêm; nêu ra theo đúng doctrine "chưa đo được thì nói thẳng".

## Ngoài phạm vi — xác nhận không nêu lại
Không có finding nào của tôi đòi đóng P1 lượt 2 của `#213`, sửa `ops-don-ref.yml`/`CLAUDE.md`, hay rà 76 nhánh C — đúng như `§ngoai_pham_vi` đã chốt.

---

Ba finding của lượt 1 đều đã đóng bằng đo (không phải bằng lời khai): `T8` là ca đo thật với tiền-điều-kiện xác nhận độc lập bằng git và hai hậu-điều-kiện đủ; ba mutant mới nhắm đúng dòng và có răng thật; `T3` đã vá đúng chỗ tôi chỉ ra. Không tìm thấy đường nào làm một nhánh còn commit riêng lọt vào lệnh xoá, kể cả sau khi tự chạy độc lập toàn bộ suite + mutation trên bản sao archive riêng của tôi.

VERDICT: approve
Reviewed commit: 5f2ff8573ed259c1a4df3030428a4ec9b0f99e2e
