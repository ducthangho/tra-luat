# wp55 revision 3 · lượt review 9 · REVIEWER `codex`

Bạn là **reviewer** cross-provider. Executor là `claude` (§8 đòi khác nền). Vai này
**read-only**: KHÔNG sửa tệp của packet, KHÔNG commit, KHÔNG push, KHÔNG merge/land.
Bạn được phép ghi tệp tạm và ghi ĐÚNG MỘT tệp verdict nêu ở cuối.

## BƯỚC 0 — xác minh. Lệch bất kỳ mục nào ⇒ DỪNG, báo lại, không review.

```bash
git rev-parse HEAD                       # ĐÒI 427021049bc8677f5915da13b8ac38a53c949b93
git rev-parse --is-shallow-repository    # ĐÒI false
```

| | |
|---|---|
| head đang review | `427021049bc8677f5915da13b8ac38a53c949b93` |
| base | `fbe5ab9e1ece3b45c065879bfd59dee2554db3e2` |
| master bất biến để đo AC 20 | `2531366e1abc6cbca0a6c2765e40e54be38d1fb7` |
| spec | `ops/specs/wp55-r3-spec.md` trên `ops/wp55-r3-spec`, sha256 `e321f811724fae97b19d523a3e5159bc13b425cd15fc6c753c7439fe28cae22d` |

Đọc spec TRỌN VẸN (21 AC) trước khi kết luận:
`git show origin/ops/wp55-r3-spec:ops/specs/wp55-r3-spec.md`

## HỒ SƠ CỦA HEAD NÀY — bất thường, khai thẳng, đừng để bạn tự phát hiện rồi mất tin

**Sổ có khoảng trống, và nó lớn hơn lease trước ghi.** Lease `review-8` neo `91780cb`
ghi `unleased_commits_on_branch: 2`. Từ lúc đó phiên executor đẩy thêm **hai commit
nữa cũng không lease** (`3c4fbc2` g7, `4270210` g8), nâng tổng lên **bốn**. Chủ kho đã
biết và chọn neo lease này vào `4270210` thay vì lùi nhánh. Con số `attempts_used`
trong sổ vì thế KHÔNG phản ánh số lượt thật.

**Lượt review 8 đã cấp lease nhưng KHÔNG chạy theo lease.** Phiên executor tự phát
động một bản review riêng trên `91780cb` bằng prompt tự soạn, không dùng
`ops/prompts/wp55-r3-review-8-codex-20260815.md`. Bản ấy nằm ở
`ops/reviews/wp55-r3-review-8-codex-verdict-NGOAI-LEASE.md` trên nhánh
`ops/wp55-r3-review-8-ngoai-lease`. Nó **KHÔNG** thoả §8. Bạn được đọc nó để biết chỗ
nào đã soi, nhưng **đừng chép kết luận** — lượt của bạn mới là lượt tính.

**Ba điều trên là BỐI CẢNH, không phải finding sẵn.** Nếu bạn thấy chúng làm bản giao
không đủ tư cách duyệt thì nêu bằng một finding có lập luận, đừng chỉ dẫn lại.

## Con lắc đã đánh quá BỐN lần — trục đáng dồn sức nhất

```
g4  thêm miễn trừ để thôi bắt oan   ⇒ quá rộng: heading trần lọt rc=0
g5  thu về "chỉ tha khi ngắt dòng"  ⇒ vẫn quá rộng: heading/bullet/bảng/fence đều lọt
g6  thu về "chỉ tha cho VĂN XUÔI"   ⇒ vẫn lọt: fence lồng cấp, ô bảng HTML
g7+g8 thêm chốt fence lồng cấp + bảng HTML  ⇒ CHƯA AI SOI ĐỘC LẬP
```

Bốn lần liên tiếp bản vá được khai là "đóng ở tầng" rồi lượt sau tìm ra hình dạng mới.
**Việc của lượt này là tìm cú đánh quá THỨ NĂM, ở CẢ HAI chiều.**

Executor tự khai một **giới hạn còn lại**: chốt "văn xuôi bọc hai phía" nhận bất kỳ
chữ nào ở hai bên, nên `x người có␤thẩm quyền y` vẫn `rc=0`. Lập luận: phân biệt nó
với câu thật của `CLAUDE.md` cần hiểu NGHĨA, mà AC 19 chính là lệnh phải tha hạng đó.
**Phán định giới hạn ấy có đúng bề rộng AC 19 không, hay đã thành cửa lọt.** Reviewer
lượt 8 cho là hợp lý; bạn không bị ràng buộc bởi phán định đó.

## Chốt MỚI của g7/g8 — chưa ai soi

1. `_go_dau_dong_tho` — gỡ dấu khối (`>`, `-`, `1.`) khỏi dòng THÔ trước khi dò hàng
   rào mã. **Cố ý KHÔNG gỡ `#`.** Thử: `#` mở đầu dòng trong khối shell; dấu khối lồng
   nhiều cấp; `---` đường kẻ ngang; `1.5` không phải số thứ tự.
2. `_RE_HANG_RAO` nới từ `^\s{0,3}` sang `^\s*`. Lệch CommonMark có chủ đích, khai là
   fail-closed. **Thử chiều BẮT OAN:** một dòng thụt sâu bắt đầu bằng ``` trong văn
   xuôi bình thường có bị đọc nhầm thành hàng rào và nuốt phần còn lại của tệp không?
3. `_dong_bang_html` — dò `<table>` … `</table>` theo SPAN, tính cả bảng KHÔNG đóng
   thẻ (tới hết tệp). **Đây là chỗ rủi ro nhất của chiều bắt oan:** một `<table>` thiếu
   thẻ đóng sẽ đánh dấu MỌI dòng còn lại là "trong bảng", tức tước miễn trừ AC 19 của
   cả phần đuôi tệp. Thử: `<table>` trong khối mã; `<table>` trong câu văn xuôi nói VỀ
   bảng; thẻ đóng viết hoa/có khoảng trắng; hai bảng lồng nhau.
4. `_khuc_chuan` dùng chung cho cả quét lẫn miễn trừ. Số dòng trong thông điệp lỗi có
   còn trỏ đúng chỗ sau khi gỡ dấu đầu dòng không?

Ngoài ra hãy tự tìm — đừng giới hạn ở danh sách này.

## Gate — chạy lại, đừng nhận số của executor

```bash
python3 .claude/dev/packet_loop_test.py            # khai nền 157/157 · 39 đột biến · 0 ngoại lệ
python3 .claude/dev/packet_loop.py doctrine-scan --root .
python3 scripts/tl.py --selftest                   # khai 1696/1696
python3 scripts/tl.py doc-claims-check --strict --json
python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --root . --strict --json
python3 scripts/tl.py golden-test
python3 .githooks/eol_policy.py --all --json
git diff --name-status fbe5ab9e1ece3b45c065879bfd59dee2554db3e2 427021049bc8677f5915da13b8ac38a53c949b93
```

Executor khai: `release-verify` checked=179 failed=0 extra=0; phạm vi đúng 6 tệp.

**AC 20 — cây ĐÃ MERGE, neo SHA BẤT BIẾN, đừng dùng `origin/master`:**

```bash
MASTER=2531366e1abc6cbca0a6c2765e40e54be38d1fb7
TREE=$(mktemp -d)
git archive "$MASTER" | tar -x -C "$TREE"
git diff --binary fbe5ab9e1ece3b45c065879bfd59dee2554db3e2..427021049bc8677f5915da13b8ac38a53c949b93 | git -C "$TREE" apply
python3 -B "$TREE/.claude/dev/packet_loop.py" doctrine-scan --root "$TREE"
GIT_DIR="$PWD/.git" python3 -B "$TREE/.claude/dev/packet_loop_test.py"
```

`GIT_DIR` là cách đo hợp lệ đã được lượt 6 xác nhận — công thức spec thiếu điều kiện
đó và việc sửa spec đã hoãn sang revision 4. Đừng tính đó là finding mới.

## Bốn chuyện đã trả giá — đừng mất thời gian lại

1. **`release-verify` trong cây làm việc sẽ trả `rc=2`** vì tệp nhiệm vụ này nằm ngoài
   manifest. KHÔNG phải finding. Muốn số sạch thì đo trên `git archive` của đúng head.
2. **Sandbox từ chối `rm -rf`.** Dùng thư mục có hậu tố SHA thay vì dọn bằng `rm -rf`.
3. **`tl.py --selftest`**: lượt 7 và 8 đều không xác nhận độc lập được `1696/1696`
   (`pyo3_runtime.PanicException` trong `cryptography`, hoặc `1694/1696` do ngữ cảnh
   git). Executor đo được `1696/1696` sau khi sửa `cffi`. Chạy được thì báo số; không
   chạy được thì ghi là **ranh giới**, đừng đoán và đừng tính là finding của packet.
4. **Đừng chạy `pip install`** — một lần cài giữa phiên đã làm hỏng `cryptography`.

## Finding đã HOÃN — đừng nêu lại

`ac20-archive-tree-suite-not-self-contained`, chủ kho chốt hoãn sang revision 4. Chỉ
nêu nếu bạn đo được điều KHÁC với mô tả đó.

## Lịch sử finding — kiểm đã đóng thật chưa

| lượt | finding_id | executor khai |
|---|---|---|
| 7 | `doctrine-line-break-exemption-bypasses-non-prose` | đóng ở g6 |
| 7 | `ac18-overlap-exceptions-have-no-killing-mutant` | đóng ở g6 — bỏ `PHU_NHIEU_LOP`, đột biến phối hợp |
| 8 (ngoài lease) | `doctrine-line-break-exemption-still-bypasses-structured-content` | đóng ở g7 + g8 |

## Giao kết quả

Ghi verdict ra ĐÚNG một tệp: `VERDICT_REVIEW_9.md` ở gốc thư mục làm việc.
KHÔNG commit, KHÔNG push — phiên executor sẽ đưa vào kho.

Định dạng: `changes_requested` | `approve` | `blocked`, mỗi finding có `finding_id`
(slug kebab-case), `severity`, `disposition`, và **bằng chứng CHẠY ĐƯỢC neo SHA bất
biến** — lệnh cụ thể, rc cụ thể, đầu ra cụ thể. Mọi lệnh trong verdict phải neo SHA
bất biến: không `origin/master`, không `HEAD`, không tên nhánh. Finding không tái lập
được thì ghi rõ là **nghi vấn**. Kèm khối `Evidence §7` dạng YAML với `reviewed_sha`,
`base_sha`, `spec_sha256`, danh sách `tests` (tên/status/evidence), và `findings`.

**Nói thẳng chỗ bạn KHÔNG chạy được.** Ranh giới của bản review quan trọng ngang kết luận.
