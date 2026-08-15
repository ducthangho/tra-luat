# wp55 revision 3 · generation 9 · EXECUTOR `claude`

Đóng **sáu finding** của verdict lượt 9 (`ops/reviews/wp55-r3-review-9-codex-verdict.md`
trên nhánh `ops/wp55-r3-review-9-verdict`). Xuất phát từ `4270210`.

## BƯỚC 0 — xác minh trước khi sửa một dòng nào

```bash
git rev-parse HEAD                       # ĐÒI 427021049bc8677f5915da13b8ac38a53c949b93
git rev-parse --is-shallow-repository    # ĐÒI false
git fetch origin 'refs/heads/ops/*:refs/remotes/origin/ops/*'   # BẮT BUỘC, xem §CHỐT dưới
```

| | |
|---|---|
| head xuất phát | `427021049bc8677f5915da13b8ac38a53c949b93` |
| base | `fbe5ab9e1ece3b45c065879bfd59dee2554db3e2` |
| master bất biến (AC 20) | `2531366e1abc6cbca0a6c2765e40e54be38d1fb7` |
| spec | `ops/specs/wp55-r3-spec.md` trên `ops/wp55-r3-spec`, sha256 `e321f811724fae97b19d523a3e5159bc13b425cd15fc6c753c7439fe28cae22d` |

## CHỐT MỚI — sinh ra từ sự cố có thật của lượt trước, ĐỌC TRƯỚC KHI PUSH

Generation 6/7/8 đẩy **bốn commit không lease** lên nhánh packet, và hai trong số đó
(`3c4fbc2`, `4270210`) được đẩy **khi lease reviewer lượt 8 đang neo `91780cb`** — làm
tip nhánh rời khỏi SHA mà reviewer đang được thuê để soi. Phải cấp lại lease lượt 9.

**Trước MỌI lần push lên `claude/**`:**

```bash
git fetch origin 'refs/heads/ops/*:refs/remotes/origin/ops/*'
# rồi tự trả lời: có lease nào đang neo một SHA trên nhánh này không?
# có ⇒ DỪNG, hỏi chủ kho. Đẩy trước rồi báo sau là sai thứ tự.
```

## Sáu finding — TÁI LẬP TRƯỚC KHI VÁ

Executor lượt trước đã tái lập đủ sáu trên `4270210`; vẫn phải tự chạy lại, đừng nhận
theo lời kể. Ma trận `doctrine-matrix` nguyên văn nằm trong verdict.

### P1 — bốn cái, và chúng KÉO NGƯỢC NHAU

| id | hình dạng | đòi | đang |
|---|---|---|---|
| `doctrine-arbitrary-prose-wrapper-bypass` | `x người có␤thẩm quyền y` | 6 | **0** |
| `doctrine-fence-invalid-closer-bypass` | ` ```` ` đóng bằng ` ``` `; ` ``` not-a-close ` | 6 | **0** |
| `doctrine-nested-html-table-bypass` | `<table>` lồng `<table></table>` trong `<td>` | 6 | **0** |
| `doctrine-structural-opener-poisons-ac19-tail` | `<table>` trong inline code / fence; dòng thụt lề mở đầu backtick | 0 | **6** |

**ĐỌC KỸ CHỖ NÀY.** Ba cái đầu đòi SIẾT, cái thứ tư đòi NỚI. Vá từng cái một sẽ đẩy
con lắc sang cú thứ sáu. Con lắc đã đánh quá **năm** lần:

```
g4  thêm miễn trừ            ⇒ quá rộng
g5  "chỉ tha khi ngắt dòng"  ⇒ vẫn quá rộng
g6  "chỉ tha cho VĂN XUÔI"   ⇒ vẫn lọt fence lồng cấp, bảng HTML
g7+g8 thêm chốt fence + bảng ⇒ lọt closer sai, bảng lồng; VÀ bắt oan đuôi tệp
```

**Phải vá ở TẦNG, một lượt, cho cả bốn.** Hướng đáng cân nhắc — không bắt buộc, nhưng
phải có lập luận nếu chọn khác:

* `_dong_khoi_ma` nhớ **độ dài** rào mở, không chỉ loại ký tự, và dòng đóng phải **không
  có phần đuôi** (CommonMark: closing fence chỉ được có khoảng trắng sau nó);
* `_RE_HANG_RAO` trả lại `^\s{0,3}` — lập luận "fail-closed" của g8 đã bị bác, xem dưới;
* `_dong_bang_html` phải **loại code span và fenced code** trước khi dò `<table>`, và
  phải đếm lồng nhau thay vì non-greedy tới `</table>` đầu tiên;
* miễn trừ AC 19 neo vào **dấu hiệu phép đo** hẹp hơn thay vì "có chữ hai phía".

### "Fail-closed" KHÔNG phải lý lẽ ở đây — chốt doctrine cho revision này

Generation 8 nới `_RE_HANG_RAO` về `^\s*` và biện minh: nhận thừa một dòng là khối mã thì
chỉ khiến cổng đỏ nhiều hơn, nên an toàn. **Sai.** AC 19 nói thẳng: chuẩn hoá mạnh hơn mà
**bắt oan văn bản bình thường là KHÔNG ĐẠT, ngang với để lọt**. Ở packet này hai chiều
CÂN NHAU; không có chiều nào là chiều an toàn để nghiêng về. Đừng dùng lại lý lẽ đó.

### P2 — `lease-schema-allows-extra-keys`

`_kiem_luoc_do_lease` kiểm thiếu khoá nhưng không kiểm **thừa** khoá. State có đủ bốn khoá
cộng `unexpected: true` vẫn mở được lượt (`rc=0`). Trái bất biến AC 21: `record-lease` là
nguồn sự thật của TOÀN schema. Siết cả hai chiều, và giữ **một** hàm chung cho
`record-lease` lẫn `begin-attempt` (AC 21 đòi đúng thế).

### P2 — `packet-suite-mutation-count-mismatch`

Hồ sơ khai **39** đột biến; `len(MUTANTS)` thật là **38**.

Đây là lỗi khai báo của executor, và nó lộ ra một chỗ hở lớn hơn con số: **suite không
assert con số nó khai**. Bộ test dựng ra để chống lời khai sai lại không chặn được lời
khai sai của chính người viết nó.

**Sửa cả hai:** đính chính mọi chỗ khai 39, **và** thêm chốt để suite tự in/kiểm
`len(MUTANTS)` sao cho một lời khai lệch không thể im lặng đi qua.

## Kỷ luật bắt buộc — AC 18/19, không được bỏ

1. **DANH SÁCH ĐÓNG TRƯỚC KHI VÁ.** Với mỗi họ finding, liệt kê CÁC HÌNH DẠNG có thể lách,
   viết ca chạy được cho từng hình dạng, ĐO trên `4270210` để lấy nền, rồi mới vá. Ba lượt
   vừa rồi danh sách đóng đều tìm ra nhiều hơn reviewer nêu (18 so với 2, 18 so với 4).
2. **ĐO CẢ HAI CHIỀU.** Mỗi lớp siết phải có ca bắt-oan đối xứng. Finding thứ tư của lượt
   này sinh ra vì g8 chỉ đo chiều lọt.
3. **MỖI LỚP MỘT ĐỘT BIẾN GIẾT ĐÚNG CA ĐÓ.** Lớp bị nhiều đường cùng phủ thì dùng đột biến
   PHỐI HỢP, KHÔNG khai ngoại lệ — cửa ngoại lệ đã bị bác ở lượt 7 và việc bỏ nó lập tức
   phơi ra một lời khai sai.
4. **Không nới phạm vi.** Đúng 6 tệp `write_set`. Phát hiện ngoài spec ⇒ xuất successor
   rồi dừng, không tự mở write set.

## Gate — đọc rc trực tiếp từng tiến trình, không qua pipe

```bash
python3 .claude/dev/packet_loop_test.py
python3 .claude/dev/packet_loop.py doctrine-scan --root .
python3 scripts/tl.py --selftest
python3 scripts/tl.py doc-claims-check --strict --json
python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --root . --strict --json
python3 scripts/tl.py golden-test
python3 .githooks/eol_policy.py --all --json
git diff --name-status fbe5ab9e1ece3b45c065879bfd59dee2554db3e2 <head-mới>
```

**AC 20 — cây ĐÃ MERGE, neo SHA BẤT BIẾN:**

```bash
MASTER=2531366e1abc6cbca0a6c2765e40e54be38d1fb7
TREE=$(mktemp -d)
git archive "$MASTER" | tar -x -C "$TREE"
git diff --binary fbe5ab9e1ece3b45c065879bfd59dee2554db3e2..<head-mới> | git -C "$TREE" apply
python3 -B "$TREE/.claude/dev/packet_loop.py" doctrine-scan --root "$TREE"
GIT_DIR="$PWD/.git" python3 -B "$TREE/.claude/dev/packet_loop_test.py"
```

`GIT_DIR` là cách đo hợp lệ đã xác nhận từ lượt 6; công thức spec thiếu điều kiện đó và
việc sửa spec đã hoãn sang revision 4 — đừng tính là finding mới.

## Bàn giao

Xuất handoff §7 (máy đọc) kèm: từng finding → cách đóng → **lệnh tái lập và rc thật**;
danh sách đóng đầy đủ với nền trước/sau; số ca, số đột biến (**đếm bằng máy, đừng gõ
tay**), 0 ngoại lệ; phạm vi 6 tệp. Nói thẳng chỗ nào KHÔNG đóng được và vì sao.

Đẩy handoff lên nhánh `ops/**`, KHÔNG nhét vào nhánh packet.
