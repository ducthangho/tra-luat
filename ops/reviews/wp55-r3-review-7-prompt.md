# wp55 revision 3 · lượt review 7 · REVIEWER `codex`

Bạn là **reviewer** cross-provider. Executor là `claude` (§8 đòi khác nền). Vai này
**read-only**: KHÔNG sửa tệp của packet, KHÔNG commit, KHÔNG push, KHÔNG merge/land.
Bạn được phép ghi tệp tạm và ghi ĐÚNG MỘT tệp verdict nêu ở cuối.

## BƯỚC 0 — xác minh. Lệch bất kỳ mục nào ⇒ DỪNG, báo lại, không review.

```bash
git rev-parse HEAD          # ĐÒI 2cccf1ea61859f1b051adb646294ead285dac39c
git rev-parse --is-shallow-repository   # ĐÒI false
git config core.abbrev 7
```

| | |
|---|---|
| head đang review | `2cccf1ea61859f1b051adb646294ead285dac39c` |
| base | `fbe5ab9e1ece3b45c065879bfd59dee2554db3e2` |
| head generation TRƯỚC | `e6e4b73dc940fcd04e9030e353e0e5fe7f3f0af8` |
| spec | `ops/specs/wp55-r3-spec.md` trên nhánh `ops/wp55-r3-spec`, sha256 `e321f811724fae97b19d523a3e5159bc13b425cd15fc6c753c7439fe28cae22d` |
| verdict lượt 6 | `ops/reviews/wp55-r3-review-6-codex-verdict.md` trên nhánh `ops/wp55-verdict-6` |

Đọc spec TRỌN VẸN (21 AC) trước khi kết luận:
`git show origin/ops/wp55-r3-spec:ops/specs/wp55-r3-spec.md`

Đây là **attempt 2/3** của revision 3. Còn một lượt dự phòng — `changes_requested` là
đường bình thường, không phải đường cùng. Nhưng cũng đừng hạ chuẩn vì thương.

## Việc generation 5 khai đã làm

Đóng **7 finding** của verdict lượt 6 (finding thứ 8 `ac20-archive-tree-suite-not-self-contained`
đã được chủ kho HOÃN sang revision 4 — executor KHÔNG được đụng, đừng tính là thiếu sót).

Bốn P1 — mã:
1. `review-transition-bypasses-record-review` → `CHUYEN_HOP_LE["reviewing"] = ()`
2. `void-reviewing-accepts-attempt-zero` → `void` rời `reviewing`; `record-review` đòi
   `attempt_open` và `attempts_used > 0`
3. `doctrine-html-quoted-angle-bypass` → regex tag phân tích thuộc tính theo cấu trúc
4. `doctrine-common-term-fail-open` → miễn trừ thu về "CHỈ tha khi cụm bị ngắt qua dòng"

Ba P2 — bộ test:
5. `ac18-mutation-not-per-class` → đối chứng khác họ + `PHU_NHIEU_LOP` + chốt mỗi lớp một đột biến
6. `ac19-false-positive-matrix-incomplete` → `ANH_XA_LOP_BAT_OAN` + chốt đỏ khi thiếu ánh xạ
7. `ac14-codepage-void-attempt-uncovered` → kịch bản sinh từ `build_parser()` + `LENH_KHONG_CO_STDOUT`

## Nơi đáng dồn sức — executor tự khai ba chỗ nghi ngờ chính mình

Đừng chỉ kiểm bảy finding đã đóng. Ba chỗ dưới đây executor tự sửa THIẾT KẾ của mình
giữa chừng; chúng chưa ai soi:

**A. Đổi KỲ VỌNG của một ca test.** Ca `oan_term_giua_cau` (câu *"Chỉ người có thẩm quyền
mới cấp được lease; phiên worker thì không."*) trước ở ma trận BẮT-OAN (đòi `rc=0`), nay
chuyển sang ma trận LỌT (đòi `rc=6`), đổi tên thành `cum_don_cau_van_xuoi_mot_dong`.
Lý lẽ executor đưa ra: AC 2 đòi bơm một cụm trong danh sách là phải ĐỎ; AC 19 chỉ đòi tha
câu KỂ LẠI KẾT QUẢ ĐO bị ngắt dòng. **Phán định: đó là đọc đúng AC, hay là dời cột gôn
cho vừa bản vá?** Đây là câu hỏi quan trọng nhất của lượt này.

**B. Bỏ chốt "đột biến không được giết lan".** Executor thêm rồi bỏ, lý do: chạy toàn bộ
suite dưới mỗi đột biến thì `init_tu_cap_lease_nhu_bug_goc` giết 42 ca vì phụ thuộc
fixture. Thay bằng "đối chứng khác họ" (3 ca doctrine ↔ 3 ca máy trạng thái). **Phán
định: thay thế ấy có đủ mạnh để thoả AC 18 "giết đúng ca đó" không, hay là làm yếu đi?**

**C. Thu hẹp chốt "mọi ca phải có đột biến" xuống chỉ `LOP_LACH`.** Lý do: áp cho mọi ca
thì 65 ca bị báo, gần hết là ca chiều THA (`rc=0`) mà đột biến GỠ chốt không thể giết.
**Phán định: phạm vi ấy đúng với câu chữ AC 18 chưa?**

Ngoài ra hãy tự tìm — đừng giới hạn ở danh sách này:

- Miễn trừ `_duoc_tha_vi_ngat_dong` mới: có lách được không? Thử cụm bị ngắt dòng NHƯNG
  đứng một mình (heading ngắt dòng, bullet ngắt dòng), cụm trong code fence ngắt dòng,
  cụm ngắt dòng trong ô bảng nhiều dòng.
- Regex tag mới: thuộc tính không nháy chứa `>`? nháy lồng? tag tự đóng? `<!DOCTYPE`?
  `<?xml`? CDATA? Tag trong code fence có bị gỡ oan không (chiều BẮT OAN)?
- `_dong_sau_khi_go` nuốt xuống dòng: có làm SỐ DÒNG trong thông điệp lỗi sai không?
  Có nối oan hai đoạn văn cách nhau bởi một comment HTML không?
- `CHUYEN_HOP_LE["reviewing"] = ()`: packet có kẹt cứng ở tình huống nào không? Ví dụ
  verdict `blocked`, hay lease hết hạn khi đang `reviewing`.
- `record-review` đòi `attempts_used > 0`: có chặn oan đường hợp lệ nào không?

## Gate — chạy lại, đừng nhận số của executor

```bash
python3 .claude/dev/packet_loop_test.py            # executor khai 133/133 + 30 đột biến
python3 .claude/dev/packet_loop.py doctrine-scan --root .
python3 scripts/tl.py --selftest                   # khai 1696/1696
python3 scripts/tl.py doc-claims-check --strict --json      # khai flags=[]
python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --root . --strict --json
python3 scripts/tl.py golden-test
python3 .githooks/eol_policy.py --all --json       # khai scanned=304 violations=0
git diff --name-status fbe5ab9e1ece3b45c065879bfd59dee2554db3e2 2cccf1ea61859f1b051adb646294ead285dac39c
```

Executor khai `release-verify` checked=179 failed=0 extra=0; bundle ×3 cùng
`20c89545566b7682b3ecd2ac2ac0283add5af8a4d6ca377d9acbcde4487f8590`; phạm vi đúng 6 tệp.

**AC 20 — cây ĐÃ MERGE, neo SHA BẤT BIẾN, đừng dùng `origin/master`:**

```bash
MASTER=2531366e1abc6cbca0a6c2765e40e54be38d1fb7
TREE=$(mktemp -d)
git archive "$MASTER" | tar -x -C "$TREE"
git diff --binary fbe5ab9e1ece3b45c065879bfd59dee2554db3e2..2cccf1ea61859f1b051adb646294ead285dac39c | git -C "$TREE" apply
python3 -B "$TREE/.claude/dev/packet_loop.py" doctrine-scan --root "$TREE"
GIT_DIR="$PWD/.git" python3 -B "$TREE/.claude/dev/packet_loop_test.py"
```

`GIT_DIR` là cách đo hợp lệ đã được lượt 6 xác nhận — công thức spec thiếu điều kiện đó
và việc sửa spec đã hoãn sang revision 4. Đừng tính đó là finding mới.

## Tám con số executor khai — đối chiếu

| ma trận | nền `e6e4b73` | sau `2cccf1e` |
|---|---|---|
| lọt | 42/54 | 54/54 |
| bắt-oan | 14/14 | 14/14 |
| lease | 28/28 | 28/28 |
| codepage | 24/28 | 28/28 |

## Giao kết quả

Ghi verdict ra ĐÚNG một tệp: `VERDICT_REVIEW_7.md` ở gốc thư mục làm việc.
KHÔNG commit, KHÔNG push — phiên executor sẽ đưa vào kho.

Định dạng: `changes_requested` | `approve` | `blocked`, mỗi finding có `finding_id`
(slug kebab-case), `severity`, `disposition`, và **bằng chứng CHẠY ĐƯỢC neo SHA bất
biến** — lệnh cụ thể, rc cụ thể, đầu ra cụ thể. Finding không tái lập được thì ghi rõ là
**nghi vấn**. Kèm khối `Evidence §7` dạng YAML với `reviewed_sha`, `base_sha`,
`spec_sha256`, danh sách `tests` (tên/status/evidence), và `findings`.

**Nói thẳng chỗ bạn KHÔNG chạy được.** Ranh giới của bản review quan trọng ngang kết luận.
