# wp55 revision 3 · lượt review 10 · REVIEWER `codex`

Bạn là **reviewer** cross-provider. Executor là `claude` (§8 đòi khác nền). Vai này
**read-only**: KHÔNG sửa tệp của packet, KHÔNG commit, KHÔNG push, KHÔNG merge/land.
Bạn được phép ghi tệp tạm và ghi ĐÚNG MỘT tệp verdict nêu ở cuối.

## BƯỚC 0 — xác minh. Lệch bất kỳ mục nào ⇒ DỪNG, báo lại, không review.

```bash
git rev-parse HEAD                       # ĐÒI 1a4525a20aa360476a6f59cb157c21097919c457
git rev-parse --is-shallow-repository    # ĐÒI false
```

| | |
|---|---|
| head đang review | `1a4525a20aa360476a6f59cb157c21097919c457` |
| base | `fbe5ab9e1ece3b45c065879bfd59dee2554db3e2` |
| head generation TRƯỚC | `427021049bc8677f5915da13b8ac38a53c949b93` |
| master bất biến (AC 20) | `2531366e1abc6cbca0a6c2765e40e54be38d1fb7` |
| spec | `ops/specs/wp55-r3-spec.md` trên `ops/wp55-r3-spec`, sha256 `e321f811724fae97b19d523a3e5159bc13b425cd15fc6c753c7439fe28cae22d` |
| verdict lượt 9 | `ops/reviews/wp55-r3-review-9-codex-verdict.md` trên `ops/wp55-r3-review-9-verdict` |

Đọc spec TRỌN VẸN (21 AC) trước khi kết luận:
`git show origin/ops/wp55-r3-spec:ops/specs/wp55-r3-spec.md`

## ⚠ LƯỢT NÀY CÓ THỂ LÀ LƯỢT CUỐI CỦA REVISION 3

Sổ ghi `attempts_used: 3/3` sau generation 9. `changes_requested` ở đây nghĩa là
revision 3 **hết lượt** và packet chuyển sang revision 4 với spec sửa lại.

Điều đó **KHÔNG** phải lý do hạ chuẩn. Chuyển sang revision 4 là một đường ra bình
thường, không phải thất bại — và ba trong bốn P1 của lượt 9 chạm tới chính câu chữ
AC 19, nên sửa spec có thể mới là đường đúng. Nhưng cũng đừng phóng đại một chỗ chưa
hoàn hảo thành finding: phân biệt rạch ròi **lỗi** với **giới hạn đã khai**.

Sổ có khoảng trống: **bốn commit** trên nhánh chạy không lease (hai `g6`, cộng
`3c4fbc2` và `4270210`). Con số `3/3` vì thế THẤP HƠN số lượt thật. Đây là bối cảnh,
không phải finding sẵn.

## Việc generation 9 khai đã làm — đóng SÁU finding của lượt 9

Executor tái lập đủ sáu trước khi vá; danh sách đóng đo nền **16/34**, sau vá **34/34**.

| finding_id | hướng | cách đóng |
|---|---|---|
| `doctrine-arbitrary-prose-wrapper-bypass` | siết | thêm điều kiện (3): hai dòng biên phải mang **dấu hiệu phép đo** |
| `doctrine-fence-invalid-closer-bypass` | siết | `_dong_khoi_ma` nhớ **độ dài** rào; rào đóng phải cùng ký tự, không ngắn hơn, **trống đuôi** |
| `doctrine-nested-html-table-bypass` | siết | `_dong_bang_html` **đếm lồng nhau** |
| `doctrine-structural-opener-poisons-ac19-tail` | **nới** | trả `_RE_HANG_RAO` về `^ {0,3}`; xoá trắng khối mã/mã inline/comment trước khi dò bảng; thẻ mở chưa đóng dừng ở **dòng trống** |
| `lease-schema-allows-extra-keys` | siết | `_kiem_luoc_do_lease` kiểm CẢ HAI chiều |
| `packet-suite-mutation-count-mismatch` | đính chính | suite nay **in số liệu đếm bằng máy** ở cuối |

## Nơi đáng dồn sức — ba chỗ executor tự khai là đáng ngờ

**A. `_DAU_HIEU_PHEP_DO` — mặt tấn công MỚI và RỘNG NHẤT.** Miễn trừ AC 19 nay đòi hai
dòng biên chứa một trong: `rc=`, `đo`, `đếm`, `v<số>.<số>`, `PR #<số>`, `<số>/<số>`.
Executor tự khai residual: kẻ gian cố tình rắc `rc=0` vào câu vẫn qua được. **Phán
định: mỏ neo ấy có đúng bề rộng AC 19 không, hay chỉ dời cửa lọt từ "hai ký tự" sang
"bốn ký tự"?** Thử: `rc=` trong một câu hoàn toàn không phải phép đo; `1/2` trong văn
xuôi thường; chữ `đo` trong từ khác (`đo lường`, `đỏ`, `đó`); dấu hiệu nằm ở dòng biên
nhưng thuộc một câu KHÁC.

**B. ĐỔI HÀNH VI — ca chuyển từ BẮT-OAN sang LỌT.** Câu
*"Quyết định này thuộc về người có␤thẩm quyền, không thuộc phiên worker."* trước `rc=0`,
nay `rc=6`. Executor chuyển `oan_term_ngat_dong` sang `LOP_LACH` với tên
`cum_don_van_xuoi_khong_ke_phep_do`, căn cứ: AC 19 tha đúng *"văn xuôi KỂ LẠI KẾT QUẢ
ĐO"*, câu ấy là khẳng định doctrine chứ không kể phép đo. **Phán định: đọc đúng AC, hay
dời cột gôn cho vừa bản vá?** Đây là lần thứ hai trong revision này một ca đổi ma trận —
lần trước (lượt 7) được chấp nhận. Đừng chấp nhận chỉ vì tiền lệ.

**C. MỘT LỚP BỊ BỎ + residual khai thẳng.** `cum_don_fence_thut_bon_dau_cach` bị bỏ vì
sau khi trả `^ {0,3}` thì thụt 4 dấu cách không còn là hàng rào. Executor khai residual:
**khối mã THỤT LỀ (CommonMark) chưa được dò**, không cài vì rủi ro bắt oan với dòng nối
tiếp của danh sách. **Phán định: bỏ lớp ấy có để hở một đường lọt thật không?** Thử đặt
cụm cấm kèm dấu hiệu phép đo trong một khối thụt 4 dấu cách.

Ngoài ra hãy tự tìm — đừng giới hạn ở danh sách này. Gợi ý các mặt chưa ai soi:

- `_dong_bang_html` xoá trắng theo thứ tự comment → khối mã → mã inline. Thứ tự ấy có
  chỗ hở nào không? Comment lồng trong khối mã? Mã inline nhiều backtick? Thẻ `<table`
  bị cắt ngang bởi ranh giới xoá trắng?
- Luật "thẻ mở chưa đóng dừng ở dòng trống": bảng thật trải qua một dòng trống thì sao?
- `_dong_khoi_ma` nay dùng `m.group(1)`/`group(2)` — dòng chỉ có ``` và khoảng trắng
  đuôi? Rào trong rào?
- Số dòng trong thông điệp lỗi có còn đúng sau tất cả các phép xoá trắng không?

## Con lắc đã đánh quá SÁU lần

```
g4    thêm miễn trừ                    ⇒ quá rộng
g5    "chỉ tha khi ngắt dòng"          ⇒ vẫn quá rộng
g6    "chỉ tha cho VĂN XUÔI"           ⇒ lọt fence lồng cấp, bảng HTML
g7+g8 thêm chốt fence + bảng           ⇒ lọt closer sai, bảng lồng; VÀ bắt oan đuôi tệp
g9    luật CommonMark + dấu hiệu đo    ⇒ CHƯA AI SOI ĐỘC LẬP
```

Việc của lượt này là tìm cú đánh quá **thứ bảy**, ở **cả hai** chiều.

## Gate — chạy lại, đừng nhận số của executor

```bash
python3 .claude/dev/packet_loop_test.py       # khai nền 173/173 · 44 đột biến · 0 ngoại lệ
python3 .claude/dev/packet_loop.py doctrine-scan --root .
python3 scripts/tl.py --selftest              # khai 1696/1696
python3 scripts/tl.py doc-claims-check --strict --json
python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --root . --strict --json
python3 scripts/tl.py golden-test
python3 .githooks/eol_policy.py --all --json
git diff --name-status fbe5ab9e1ece3b45c065879bfd59dee2554db3e2 1a4525a20aa360476a6f59cb157c21097919c457
```

Suite nay tự in khối `SỐ LIỆU (đếm bằng máy)` ở cuối — đối chiếu số ấy với số executor
khai, đó chính là chốt sinh ra từ finding `packet-suite-mutation-count-mismatch`.

**AC 20 — cây ĐÃ MERGE, neo SHA BẤT BIẾN:**

```bash
MASTER=2531366e1abc6cbca0a6c2765e40e54be38d1fb7
TREE=$(mktemp -d)
git archive "$MASTER" | tar -x -C "$TREE"
git diff --binary fbe5ab9e1ece3b45c065879bfd59dee2554db3e2..1a4525a20aa360476a6f59cb157c21097919c457 | git -C "$TREE" apply
python3 -B "$TREE/.claude/dev/packet_loop.py" doctrine-scan --root "$TREE"
GIT_DIR="$PWD/.git" python3 -B "$TREE/.claude/dev/packet_loop_test.py"
```

`GIT_DIR` là cách đo hợp lệ đã xác nhận từ lượt 6 — spec thiếu điều kiện đó, sửa spec đã
hoãn sang revision 4. Đừng tính là finding mới.

## Bốn chuyện đã trả giá — đừng mất thời gian lại

1. **`release-verify` trong cây làm việc trả `rc=2`** vì tệp nhiệm vụ này ngoài manifest.
   KHÔNG phải finding. Muốn số sạch thì đo trên `git archive` của đúng head.
2. **Sandbox từ chối `rm -rf`.** Dùng thư mục có hậu tố SHA.
3. **Đừng chạy `pip install`** — một lần cài giữa phiên đã làm hỏng `cryptography` và
   khiến hai lượt review không xác nhận được `selftest`.
4. **`tl.py --selftest`**: lượt 7 và 8 không xác nhận độc lập được. Chạy được thì báo số;
   không chạy được thì ghi là **ranh giới**, đừng đoán.

## Finding đã HOÃN — đừng nêu lại

`ac20-archive-tree-suite-not-self-contained`, chủ kho chốt hoãn sang revision 4.

## Giao kết quả

Ghi verdict ra ĐÚNG một tệp: `VERDICT_REVIEW_10.md` ở gốc thư mục làm việc.
KHÔNG commit, KHÔNG push.

Định dạng: `changes_requested` | `approve` | `blocked`, mỗi finding có `finding_id`
(slug kebab-case), `severity`, `disposition`, và **bằng chứng CHẠY ĐƯỢC neo SHA bất
biến** — lệnh cụ thể, rc cụ thể, đầu ra cụ thể. Mọi lệnh phải neo SHA bất biến: không
`origin/master`, không `HEAD`, không tên nhánh. Finding không tái lập được thì ghi rõ là
**nghi vấn**. Kèm khối `Evidence §7` dạng YAML với `reviewed_sha`, `base_sha`,
`spec_sha256`, danh sách `tests` (tên/status/evidence), và `findings`.

**Nếu kết luận là `changes_requested`, nói rõ finding nào cần SỬA SPEC** (revision 4)
và finding nào chỉ cần sửa mã — chủ kho cần phân biệt đó để quyết định bước tiếp.

**Nói thẳng chỗ bạn KHÔNG chạy được.** Ranh giới của bản review quan trọng ngang kết luận.
