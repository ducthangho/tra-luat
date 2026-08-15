# wp55 revision 3 · lượt review 8 · REVIEWER `codex`

Bạn là **reviewer** cross-provider. Executor là `claude` (§8 đòi khác nền). Vai này
**read-only**: KHÔNG sửa tệp của packet, KHÔNG commit, KHÔNG push, KHÔNG merge/land.
Bạn được phép ghi tệp tạm và ghi ĐÚNG MỘT tệp verdict nêu ở cuối.

## BƯỚC 0 — xác minh. Lệch bất kỳ mục nào ⇒ DỪNG, báo lại, không review.

```bash
git rev-parse HEAD                       # ĐÒI 91780cb0df3c898b2ca92bc17d14107547d944c6
git rev-parse --is-shallow-repository    # ĐÒI false
```

| | |
|---|---|
| head đang review | `91780cb0df3c898b2ca92bc17d14107547d944c6` |
| base | `fbe5ab9e1ece3b45c065879bfd59dee2554db3e2` |
| head generation TRƯỚC | `2cccf1ea61859f1b051adb646294ead285dac39c` |
| master bất biến để đo AC 20 | `2531366e1abc6cbca0a6c2765e40e54be38d1fb7` |
| spec | `ops/specs/wp55-r3-spec.md` trên nhánh `ops/wp55-r3-spec`, sha256 `e321f811724fae97b19d523a3e5159bc13b425cd15fc6c753c7439fe28cae22d` |
| verdict lượt 7 | `ops/reviews/wp55-r3-review-7-codex-verdict.md` trên nhánh `ops/wp55-r3-review-7` |

Đọc spec TRỌN VẸN (21 AC) trước khi kết luận:
`git show origin/ops/wp55-r3-spec:ops/specs/wp55-r3-spec.md`

⚠ **Đây là attempt 3/3 — LƯỢT CUỐI của revision 3.** Không còn lượt dự phòng.
Điều đó **KHÔNG** phải lý do hạ chuẩn: nếu còn lỗi thật thì `changes_requested` vẫn là
kết luận đúng, và packet sẽ sang revision 4. Nhưng cũng đừng phóng đại một chỗ chưa
hoàn hảo thành finding — hãy phân biệt rạch ròi **lỗi** với **giới hạn đã khai**.

## Việc generation 6 khai đã làm

Đóng **2 finding** của verdict lượt 7.

**P1 `doctrine-line-break-exemption-bypasses-non-prose`.** Miễn trừ ngắt dòng của g5 tha
MỌI hình dạng ngắt dòng, nên chỉ cần xuống dòng giữa cụm cấm là qua cổng. Vá ở tầng, hai
chốt mới trong `_duoc_tha_vi_ngat_dong`:

1. **loại khối mã rào** khỏi miễn trừ (`_dong_khoi_ma`, đo trên dòng THÔ vì hàng rào sau
   chuẩn hoá thành chuỗi rỗng nên tầng đã chuẩn hoá không thấy nó);
2. **đòi văn xuôi BỌC HAI PHÍA** — dòng mở còn chữ trước mảnh cụm, dòng đóng còn chữ sau
   nó, sau khi gỡ dấu đầu dòng (`_go_dau_dong`).

**Cộng một lỗ executor tự tìm, verdict 7 KHÔNG nêu:** ba ca trích dẫn lọt vì lý do khác
hẳn — `_chuan_hoa` GIỮ dấu `>`, nên chuỗi phẳng ra `> người có > thẩm quyền` và cụm cấm
không khớp lần nào. Scanner **không thấy**, chứ không phải miễn trừ tha nhầm. Vá bằng
cách gỡ dấu đầu dòng ở tầng phẳng hoá, và `_phang_ca_tep` cùng miễn trừ nay dùng CHUNG
`_khuc_chuan` để hai bên không lệch offset.

**P2 `ac18-overlap-exceptions-have-no-killing-mutant`.** Bỏ HẲN `PHU_NHIEU_LOP`. Đột biến
nay nhận DANH SÁCH cặp thay thế (`_cap_thay_the`), nên lớp bị nhiều đường cùng phủ dùng
đột biến PHỐI HỢP thay vì khai miễn. Executor khai: việc đòi có đột biến lập tức phơi ra
một **lời khai SAI** — lớp `nbsp` khai "hai đường phủ", dựng đủ hai vế vẫn không giết
được ca, đường thứ ba là `str.split()` không đối số tách theo khoảng trắng Unicode. Đổi
tên thành `ac18_nbsp_phu_ba_lop`.

## Nơi đáng dồn sức

**A. Chốt "văn xuôi bọc hai phía" có lách được không?** Đây là chốt rộng nhất và mới
nhất. Executor tự khai một **giới hạn**: câu văn xuôi BẤT KỲ có cụm bị ngắt dòng vẫn
được tha — `Ghi chú người có␤thẩm quyền đây.` lọt — vì phân biệt nó với ca thật của
`CLAUDE.md` cần hiểu NGHĨA, mà AC 19 chính là lệnh phải tha hạng đó. **Phán định: đó là
giới hạn ĐÃ KHAI đúng bề rộng AC 19, hay là lỗ còn lại?** Thử: một chữ vô nghĩa hai bên
(`x người có␤thẩm quyền y`), dấu câu thay chữ, chữ nằm trong tag HTML, chữ là số.

**B. `_dong_khoi_ma` — máy trạng thái hàng rào tự viết.** Thử: fence không đóng; fence
đóng bằng loại rào KHÁC (` ``` ` mở, `~~~` đóng); rào 4 dấu trở lên; rào thụt 4 dấu cách
(theo CommonMark thì không còn là rào); fence lồng trong bullet; `>` + fence. Có ca nào
làm SỐ DÒNG trong thông điệp lỗi sai không?

**C. Gỡ dấu đầu dòng ở tầng PHẲNG HOÁ — chiều BẮT OAN.** `_go_dau_dong` nay chạy cho MỌI
dòng của MỌI tệp được quét, không riêng đường miễn trừ. Nó có nối oan hai dòng vốn không
liên quan không? Ví dụ một bảng Markdown mà `|` bị gỡ, một dòng bắt đầu bằng `#` là thẻ
băm chứ không phải heading, một dòng bắt đầu bằng `1.` là số thứ tự trong văn xuôi, một
dòng bắt đầu bằng `>` là dấu lớn hơn trong mã. Chiều này ít được đo nhất.

**D. `_cap_thay_the` và ba đột biến phối hợp.** Đột biến phối hợp có thể mạnh quá tay:
gỡ nhiều đường một lúc thì ca đích chết vì đường nào? Kiểm `noi_mien_tru_nhu_generation_4`
(2 vế, 13 ca đích), `ha_NFKC_va_bo_moi_duong_gop_nbsp` (3 vế), `ha_NFKC_va_bo_casefold`
(2 vế). **Phán định: chúng có còn "giết đúng ca đó" theo AC 18, hay đã thành đột biến
diện rộng?** Đối chứng khác họ có đủ để bắt việc giết lan không?

**E. Lời khai "phơi ra một lời khai SAI".** Executor nói đột biến hai vế không giết được
`ac18_nbsp_phu_ba_lop` nên mới lộ đường thứ ba. **Tự dựng lại đột biến hai vế và kiểm.**
Nếu hai vế ĐÃ đủ giết thì lời khai này sai, và tên lớp `phu_ba_lop` cũng sai.

Ngoài ra hãy tự tìm — đừng giới hạn ở danh sách này.

## Gate — chạy lại, đừng nhận số của executor

```bash
python3 .claude/dev/packet_loop_test.py            # khai nền 149/149 + 35 đột biến + 0 ngoại lệ
python3 .claude/dev/packet_loop.py doctrine-scan --root .
python3 scripts/tl.py --selftest                   # khai 1696/1696
python3 scripts/tl.py doc-claims-check --strict --json      # khai flags=[]
python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --root . --strict --json
python3 scripts/tl.py golden-test
python3 .githooks/eol_policy.py --all --json       # khai scanned=304 violations=0
git diff --name-status fbe5ab9e1ece3b45c065879bfd59dee2554db3e2 91780cb0df3c898b2ca92bc17d14107547d944c6
```

Executor khai `release-verify` checked=179 failed=0 extra=0; phạm vi đúng 6 tệp.

**AC 20 — cây ĐÃ MERGE, neo SHA BẤT BIẾN, đừng dùng `origin/master`:**

```bash
MASTER=2531366e1abc6cbca0a6c2765e40e54be38d1fb7
TREE=$(mktemp -d)
git archive "$MASTER" | tar -x -C "$TREE"
git diff --binary fbe5ab9e1ece3b45c065879bfd59dee2554db3e2..91780cb0df3c898b2ca92bc17d14107547d944c6 | git -C "$TREE" apply
python3 -B "$TREE/.claude/dev/packet_loop.py" doctrine-scan --root "$TREE"
GIT_DIR="$PWD/.git" python3 -B "$TREE/.claude/dev/packet_loop_test.py"
```

`GIT_DIR` là cách đo hợp lệ đã được lượt 6 xác nhận — công thức spec thiếu điều kiện đó
và việc sửa spec đã hoãn sang revision 4. Đừng tính đó là finding mới.

## Ba chuyện đã trả giá ở lượt 7 — đừng mất thời gian lại

1. **`release-verify` trong cây làm việc sẽ trả `rc=2`** vì chính tệp `NHIEM_VU_REVIEW_8.md`
   này nằm ngoài manifest. Đó KHÔNG phải finding. Muốn số sạch thì đo trên
   `git archive` của đúng head.
2. **Sandbox từ chối `rm -rf`.** Dùng thư mục có hậu tố SHA thay vì dọn bằng `rm -rf`.
3. **`tl.py --selftest` từng vấp `pyo3_runtime.PanicException` trong `cryptography`.**
   Nguyên nhân đã tìm ra: một lần `pip install` giữa phiên nâng `cffi` lên bản không khớp
   `cryptography` 41.0.7 bản Debian. Nay đã lành — executor đo lại được `1696/1696`.
   **Đừng chạy `pip install`.** Nếu vẫn vấp panic, ghi là ranh giới, đừng tính là finding
   của packet.

## Hai finding của lượt 7 — kiểm đã đóng thật chưa

| finding_id | severity | executor khai |
|---|---|---|
| `doctrine-line-break-exemption-bypasses-non-prose` | P1 | đóng — 2 chốt mới + gỡ dấu đầu dòng |
| `ac18-overlap-exceptions-have-no-killing-mutant` | P2 | đóng — bỏ `PHU_NHIEU_LOP`, 3 đột biến phối hợp |

Finding `ac20-archive-tree-suite-not-self-contained` đã được chủ kho HOÃN sang revision 4
— executor KHÔNG được đụng, đừng tính là thiếu sót.

## Số executor khai — đối chiếu

| | g5 `2cccf1e` | g6 `91780cb` |
|---|---|---|
| nền suite | 133/133 | 149/149 |
| đột biến | 30 | 35 (3 phối hợp) |
| lớp lách có đột biến | 39/41 + 2 ngoại lệ | 53/53, 0 ngoại lệ |
| lớp lách có ca bắt-oan | 41/41 | 53/53 (23 ca riêng biệt) |

## Giao kết quả

Ghi verdict ra ĐÚNG một tệp: `VERDICT_REVIEW_8.md` ở gốc thư mục làm việc.
KHÔNG commit, KHÔNG push — phiên executor sẽ đưa vào kho.

Định dạng: `changes_requested` | `approve` | `blocked`, mỗi finding có `finding_id`
(slug kebab-case), `severity`, `disposition`, và **bằng chứng CHẠY ĐƯỢC neo SHA bất
biến** — lệnh cụ thể, rc cụ thể, đầu ra cụ thể. Finding không tái lập được thì ghi rõ là
**nghi vấn**. Kèm khối `Evidence §7` dạng YAML với `reviewed_sha`, `base_sha`,
`spec_sha256`, danh sách `tests` (tên/status/evidence), và `findings`.

**Nói thẳng chỗ bạn KHÔNG chạy được.** Ranh giới của bản review quan trọng ngang kết luận.
