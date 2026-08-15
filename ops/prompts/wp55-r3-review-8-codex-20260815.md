# wp55 revision 3 · CROSS-REVIEW lượt 8 — reviewer `codex` · head `91780cb`

Bạn là **reviewer độc lập**. Vai này **CHỈ ĐỌC**: không sửa tệp, không commit, không push,
không merge, không land, không deploy. Đầu ra là **verdict** + **evidence §7**.

§8 đòi reviewer khác provider với executor. Executor là `claude` ⇒ reviewer phải là `codex`.
Không phải `codex` thì **DỪNG** và báo lại.

---

## BƯỚC 0 — xác minh. Lệch bất kỳ mục nào ⇒ DỪNG, báo lại, không review.

```bash
git rev-parse --is-shallow-repository        # ĐÒI false
git remote -v                                # ĐÒI github.com/ducthangho/tra-luat
git config core.abbrev 7

git fetch origin ops/wp55-r3-spec
git show origin/ops/wp55-r3-spec:ops/specs/wp55-r3-spec.md | sha256sum
#   ĐÒI e321f811724fae97b19d523a3e5159bc13b425cd15fc6c753c7439fe28cae22d

git fetch origin claude/wp55-r3g5-f3-03
git rev-parse origin/claude/wp55-r3g5-f3-03
#   ĐÒI 91780cb0df3c898b2ca92bc17d14107547d944c6
#   Khác ⇒ có phiên đẩy tiếp ⇒ DỪNG, hỏi bên điều phối.

sha256sum ops/prompts/wp55-r3-review-8-codex-20260815.md   # ĐÒI khớp prompt_sha256_required
```

**KIỂM ĐƯỜNG GIAO VERDICT TRƯỚC KHI LÀM VIỆC.** Đã hỏng nhiều lượt: `403` từ
`api.github.com`, `gh` không cài, MCP chưa xác thực. `git push` thì chạy. Không ghi được
lên GitHub thì **vẫn review**, ghi verdict vào kho theo mục *Giao kết quả* và nói rõ ngay ở
ĐẦU báo cáo là cần người đăng hộ. Tuyệt đối không im lặng bỏ qua.

---

## Đối tượng — và hoàn cảnh KHÔNG bình thường, đọc kỹ

| | |
|---|---|
| head | `91780cb0df3c898b2ca92bc17d14107547d944c6` |
| base | `fbe5ab9e1ece3b45c065879bfd59dee2554db3e2` |
| nhánh · PR | `claude/wp55-r3g5-f3-03` · **#120** |
| spec | `ops/specs/wp55-r3-spec.md` · `e321f811…` — **21 AC nằm ở đó, đọc TRỌN** |

**Ba điều bất thường về hồ sơ, bên điều phối khai thẳng chứ không giấu:**

1. **KHÔNG có handoff §7 cho head này.** Phiên đẩy nó không viết. Thứ thay thế là *bản ghi
   của phiên điều phối* ([#55 comment 5301382838](https://github.com/ducthangho/tra-luat/issues/55#issuecomment-5301382838),
   kèm [đính chính SHA](https://github.com/ducthangho/tra-luat/issues/55#issuecomment-5301384396)),
   và nó **không thay** được §7.
2. **Hai executor đã cùng sống trên một lease.** Nhánh này mang hai commit tự gắn nhãn `g6`
   **không có lease `exec-6`**. Chủ kho chốt lấy nhánh này — quyết định đó giải quyết *nhánh
   nào*, **không** hồi tố tạo lease. Sổ có khoảng trống.
3. **`attempts_used` trong sổ là 2/3**, nhưng hai commit `g6` không vào sổ. Con số thật có
   thể khác. **Đừng hạ chuẩn vì tưởng sắp hết lượt** — nếu bạn thấy vấn đề, `changes_requested`
   là đường bình thường.

Những điều trên là **bối cảnh**, không phải finding sẵn. Nếu bạn cho rằng chúng làm bản giao
không đủ tư cách để duyệt, hãy nói bằng một finding có lập luận, đừng chỉ dẫn lại.

## Lịch sử ba lượt — hiểu vì sao chỗ này khó

Bản vá doctrine đã **đánh quá ba lần liên tiếp**, mỗi lần theo một chiều:

| lượt | chữa gì | hỏng ra sao |
|---|---|---|
| g4 | thêm `_co_ngu_canh_doctrine` để thôi **bắt oan** câu văn xuôi ngắt dòng | quá rộng ⇒ **fail-open**: heading trần chép nguyên cụm lọt `rc=0` |
| g5 | thu về *"chỉ tha khi cụm bị NGẮT QUA DÒNG"* | vẫn quá rộng ⇒ heading/bullet/bảng HTML/code fence ngắt dòng đều lọt |
| head này | thu về *"miễn trừ chỉ dành cho VĂN XUÔI"* | **chưa ai soi độc lập** |

Đây là trục đáng dồn sức nhất: **tìm cú đánh quá thứ tư**, ở cả hai chiều.

---

## Nơi đáng dồn sức

### 1. Ranh giới "văn xuôi" — chiều LỌT và chiều BẮT OAN, ngang nhau

Định nghĩa mới quyết định bằng *dấu cấu trúc* (`#`, gạch đầu dòng, `|`, fence, thẻ HTML).
Hỏi ngược cả hai chiều:

- **Lọt:** còn cấu trúc nào **hiển thị ra cụm cấm** mà không mang dấu cấu trúc ở đầu dòng?
  Gợi ý chưa chắc đã xét: blockquote `>`; danh sách đánh số; định nghĩa `term : def`; bảng
  không có `|` ở đầu dòng; HTML block nhiều dòng; footnote; chú thích tham chiếu link;
  dòng thụt đầu bốn khoảng trắng (code block ngầm); dòng trống xen giữa hai nửa cụm;
  ký tự tiếp nối `\` cuối dòng; CRLF.
- **Bắt oan:** ca canonical AC 19 — `CLAUDE.md` master **dòng 82–83**, nằm trong một mục có
  **gạch đầu dòng** — có còn XANH không? Nếu định nghĩa mới loại mọi dòng có dấu cấu trúc thì
  ca ấy đáng lẽ ĐỎ. Kiểm bằng số, đừng suy luận.
- Văn xuôi thường của adapter viết đúng có bị bắt oan chỗ nào không?

### 2. Máy trạng thái — ba bản vá P1 của lượt 6 có đóng thật không

- `CHUYEN_HOP_LE["reviewing"] = ()`: còn đường nào rời `reviewing` mà không qua
  `record-review`? Kể cả `init` lại, sửa state tay, hay một lệnh con khác.
- `void-attempt`: mọi pha (`leased`/`running`/`reviewing`) có để state ở chỗ chạy tiếp được
  không? Có pha nào nay **kẹt cứng** — tức chữa lọt thành chữa quá tay?
- `record-review`: đòi lượt đang mở và `attempts_used > 0` — có chặn oan lượt hợp lệ nào không?
- Lược đồ lease: `_kiem_luoc_do_lease` có thật sự **một hàm chung** cho `record-lease` lẫn
  `begin-attempt`, hay còn nhánh tự kiểm sót lại? Đọc mã, đừng tin tên hàm.

### 3. Bộ test — ca có MẶT khác ca có ĐO

Suite khai `149/149` + `36` đột biến, `ANH_XA_LOP_BAT_OAN` phủ mọi lớp, ma trận codepage
sinh từ `build_parser()`. Hỏi ngược:

- Có ca nào `return` sớm rồi vẫn đếm ĐẠT (đường dẫn sai, fixture vắng)? Kho đã trả giá ở `t24`.
- Runner có đo **cả hai vế** — ca đích ĐỎ **và** ca ngoài tập vẫn XANH — hay chỉ vế đầu?
- Gỡ từng chốt mới trong `_chuan_hoa`, `_duoc_tha_*`, `_kiem_luoc_do_lease` và đo: chốt nào
  gỡ mà suite vẫn xanh là một finding.
- Ma trận codepage sinh từ parser: có lệnh con nào bị **khai miễn trừ** (`LENH_KHONG_CO_STDOUT`)
  mà thực ra CÓ in stdout không? Đó là chỗ liệt-kê-tay chui về dưới lớp áo tự động.

### 4. Phép đo mà bên điều phối KHÔNG chạy được — phần việc của bạn

`tl.py --selftest` trả **rc=1** trong container bên điều phối:
`pyo3_runtime.PanicException` từ `cryptography` rust bindings. Họ đo được **delta = 0** (cùng
lỗi trên cây khác cùng container) và nhánh **không đụng tệp nào dưới `scripts/`**, nhưng
**không xác minh được**. Hãy tự chạy:

```bash
python3 scripts/tl.py --selftest                 # ĐÒI hai số BẰNG NHAU
```

Chạy được thì báo số thật. Không chạy được thì nói rõ là **không chạy được**, đừng đoán.

Các gate còn lại bên điều phối đã chạy — **tự kiểm lại**, đừng chép:

```bash
python3 .claude/dev/packet_loop_test.py
python3 .claude/dev/packet_loop.py doctrine-scan --root .
python3 scripts/tl.py doc-claims-check --strict --json      # ĐÒI flags=[]
python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --root . --strict --json
python3 scripts/tl.py golden-test                            # KHÔNG --write
python3 .githooks/eol_policy.py --all --json                 # ĐÒI violations=0
# release-bundle ×2 trên head + ×1 từ base — ĐÒI cả BA cùng sha256
git diff --name-status fbe5ab9e1ece3b45c065879bfd59dee2554db3e2 91780cb0df3c898b2ca92bc17d14107547d944c6
```

`rc` của một pipe là `rc` của lệnh **cuối** — đọc rc trực tiếp từng lệnh. Đòi **bằng chứng
dương** (hai số bằng nhau, `ok: true`), đừng tin `rc=0`.

### 5. AC 20 — cây ĐÃ MERGE, neo SHA BẤT BIẾN

```bash
MASTER=2531366e1abc6cbca0a6c2765e40e54be38d1fb7     # hoặc SHA master lúc BẠN đo, ghi rõ
merged=$(mktemp -d)
git archive "$MASTER" | tar -x -C "$merged"
git diff --binary fbe5ab9e1ece3b45c065879bfd59dee2554db3e2..91780cb0df3c898b2ca92bc17d14107547d944c6 \
  | git -C "$merged" apply
python3 -B "$merged/.claude/dev/packet_loop.py" doctrine-scan --root "$merged"
GIT_DIR="$PWD/.git" python3 -B "$merged/.claude/dev/packet_loop_test.py"
```

`ac20-archive-tree-suite-not-self-contained` đã được ghi nhận và **HOÃN sang revision 4** —
đừng nêu lại như finding mới; nêu lại chỉ khi bạn đo được điều gì **khác** với mô tả đó.

**Mọi lệnh trong verdict phải neo SHA BẤT BIẾN** — không `origin/master`, không `HEAD`, không
tên nhánh. Ghi rõ SHA master bạn dùng. Verdict còn ref di động là verdict tự hạ giá trị bằng
chứng của chính nó (lượt 5 đã vấp, codex nêu P2 trên PR #114).

### 6. Phạm vi

`git diff --name-status` phải cho **ĐÚNG 6 tệp** write_set. `VERSION`, `CHANGELOG`,
`RELEASE_MANIFEST.json`, `references/golden/**`, `scripts/tl_test_fragments_bundled.py`,
`ops/specs/**` **không được đổi** — kiểm bằng số.

---

## Verdict và evidence

`approve` · `changes_requested` · `blocked`.

- **`approve`** chỉ khi bạn đã tự chạy, tự tìm, không ra P1/P2 chặn.
- **`changes_requested`** khi có finding cần vá.
- **`blocked`** khi chính spec/prompt thiếu, hoặc bạn không chạy được phần thiết yếu.

Mỗi finding: `finding_id` (slug kebab-case ổn định), `severity`, `disposition`, và **bằng
chứng CHẠY ĐƯỢC neo SHA bất biến** — lệnh, mã thoát, đầu ra cụ thể. Không tái lập được thì
ghi rõ là **nghi vấn**, đừng để lẫn với cái đã đo.

**Nói thẳng chỗ bạn KHÔNG chạy được.** Các lượt trước làm vậy và nhờ thế người đọc biết ranh
giới của bản review.

### Giao kết quả

Ưu tiên: review trên **PR #120** neo `commitID = 91780cb0df3c898b2ca92bc17d14107547d944c6`,
kèm evidence §7 lên issue #55.

Không ghi được lên GitHub thì ghi vào kho — **đúng khuôn lượt 5, nó chạy được**:

```
ops/reviews/wp55-r3-review-8-codex-verdict.md            # NGUYÊN VĂN, không sửa
ops/reviews/wp55-r3-review-8-codex-verdict.receipt.yaml  # nơi đăng + băm, tệp RIÊNG
```

Xuất **thẳng `stdout` ra tệp**, đừng chép tay — lượt 4 chép tay và đã lệch một chỗ; lượt 5 bỏ
khâu chép và byte-identical. Rồi push lên một nhánh `ops/**` và báo `sha256` + số byte.

---

## Stop conditions

Head đổi giữa chừng · lease hết hạn · bạn không phải `codex` · BƯỚC 0 lệch · bị đòi sửa
tệp/commit/push/merge/land (**không phải vai của bạn**) · không chạy được phần thiết yếu
(báo `blocked` kèm lý do đo được, đừng đoán rồi `approve`) · chạm quota (ghi lý do allowlist,
**không** tiêu attempt nội dung).

Heartbeat **mỗi 30 phút** lên #55. Đường ghi bị chặn thì ghi nhịp vào tệp trong kho và nói rõ
— im lặng không được đọc thành phiên chết, cũng không được đọc thành phiên còn sống.
