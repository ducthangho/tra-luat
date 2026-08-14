# wp55 revision 3 · generation 4 · CROSS-REVIEW lượt 6 — reviewer `codex`

Bạn là **reviewer độc lập**. Vai này **CHỈ ĐỌC**: không sửa tệp, không commit, không push,
không merge, không land, không deploy. Đầu ra là **verdict** + **evidence §7**.

§8 đòi reviewer khác provider với executor. Executor là `claude` ⇒ reviewer phải là `codex`.
Nếu bạn không phải `codex`, **DỪNG** và báo lại.

---

## BƯỚC 0 — xác minh. Lệch bất kỳ mục nào ⇒ DỪNG, báo lại, không review.

```bash
git rev-parse --is-shallow-repository        # ĐÒI false
git remote -v                                # ĐÒI github.com/ducthangho/tra-luat
git config core.abbrev 7

# spec revision 3 — NGUỒN SỰ THẬT là TỆP, không phải thân Issue
git fetch origin ops/wp55-r3-spec
git show origin/ops/wp55-r3-spec:ops/specs/wp55-r3-spec.md | sha256sum
#   ĐÒI e321f811724fae97b19d523a3e5159bc13b425cd15fc6c753c7439fe28cae22d

# head phải review
git fetch origin claude/wp55-r3g4-f3-03
git rev-parse origin/claude/wp55-r3g4-f3-03
#   ĐÒI e6e4b73dc940fcd04e9030e353e0e5fe7f3f0af8
#   Khác ⇒ executor đã đẩy tiếp ⇒ DỪNG, hỏi bên điều phối.

# tệp này
sha256sum ops/prompts/wp55-r3-review-6-codex-20260814.md   # ĐÒI khớp prompt_sha256_required
```

**KIỂM ĐƯỜNG GIAO VERDICT TRƯỚC KHI LÀM VIỆC.** Đây không phải thủ tục — đã hỏng **bốn**
lượt liên tiếp: vòng 3 và lượt 4 review xong không ghi được; lượt 5 phải nhờ đăng hộ;
executor generation 4 vừa rồi cũng `403` và phải ghi handoff vào kho.

Thử ngay đường bạn định dùng. Không ghi được thì **vẫn review**, nhưng ghi verdict vào kho
theo mục *Giao kết quả* và nói rõ ngay ở ĐẦU báo cáo rằng cần người đăng hộ. Tuyệt đối
không im lặng bỏ qua.

---

## Đối tượng

| | |
|---|---|
| head | `e6e4b73dc940fcd04e9030e353e0e5fe7f3f0af8` |
| base | `fbe5ab9e1ece3b45c065879bfd59dee2554db3e2` |
| nhánh · PR | `claude/wp55-r3g4-f3-03` · **#115** |
| spec | `ops/specs/wp55-r3-spec.md` · `e321f811…` — **đọc TRỌN, 21 AC nằm ở đó** |
| handoff §7 | `ops/handoffs/wp55-r3g4-exec-4-claude-handoff.md` (nhánh `ops/wp55-r3g4-exec-4-evidence`) · sha256 bắt đầu `e23873341d530977` |
| danh sách đóng AC 18 | `ops/evidence/wp55-r3g4-ac18-danh-sach-dong.md` · `861514ef4722fc2e` |
| ba probe | `ops/evidence/wp55-r3g4-probe-{doctrine,lease,oan}.py` |
| verdict lượt 5 | `ops/reviews/wp55-r2-review-5-codex-verdict.md` (nhánh `ops/wp55-verdict-5`) · `d1d04452d0ab…` |

Đây là **revision 3, attempt 1/3**. Trần đếm lại từ 0 — bạn không bị ép duyệt vì hết lượt.

---

## NEO SHA BẤT BIẾN — bài học vừa trả giá ở lượt 5

Verdict lượt 5 **khai** `master_sha_checked: 3d2c52d…` trong evidence, nhưng **lệnh tái hiện
lại neo `origin/master`** — một ref DI ĐỘNG. Master tiến lên là lệnh dựng ra cây khác, và
bản review không tái lập được nữa.

**Ghi số và neo số là hai việc khác nhau.** Cái thứ nhất chứng minh lượt đo đã xảy ra; chỉ
cái thứ hai làm nó tái lập được.

Nên lượt này: **mọi lệnh trong verdict của bạn phải neo SHA bất biến**, không dùng
`origin/master`, `HEAD`, `@{u}` hay tên nhánh. Ghi rõ SHA master bạn dùng để đo. Verdict nào
còn ref di động thì chính bạn tự hạ giá trị bằng chứng của mình.

---

## Nơi đáng dồn sức

### 1. Bản vá `_chuan_hoa` — chiều LỌT có thật sự đóng, và chiều BẮT OAN có bị hở ra không

Executor mở rộng chuẩn hoá rất mạnh: NFKC, lọc `Cf`, giải entity một lần, gấp đồng tự
Cyrillic/Hy Lạp, gấp mũi tên, bỏ nháy cong, gộp phân cách, bỏ tag/comment HTML, rút text
link, gỡ backslash escape — áp **cả hai vế**.

Chuẩn hoá càng mạnh, **chiều bắt oan càng dễ hở**. Đó là đánh đổi thật, và AC 19 đòi đo cả hai.

- Danh sách đóng khai **18 lớp lọt**. Nó **ĐÓNG THẬT** chưa? Tìm lớp thứ 19. Gợi ý chỗ chưa
  chắc đã xét: tổ hợp dấu (combining marks) và thứ tự chuẩn hoá; chữ số/ký tự đóng khung;
  ligature hiếm; entity lồng nhiều tầng; `<!-- -->` lồng; bảng Markdown có ô rỗng; footnote;
  HTML `<wbr>`; ký tự điều khiển hai chiều (bidi override) — **đặc biệt bidi**, vì nó đổi
  thứ tự HIỂN THỊ mà không đổi thứ tự byte.
- Chiều ngược: gấp đồng tự có nuốt nhầm chữ Hy Lạp/Cyrillic **dùng đúng nghĩa** không?
  Rút text link có làm mất phân biệt giữa *nhắc tới* và *chép lại* không? Gộp phân cách có
  làm hai cụm khác nghĩa trùng nhau không?
- Giải entity **đúng một lần**: kiểm `&amp;#58;` (hiển thị nguyên văn `&#58;`, KHÔNG phải
  dấu hai chấm) không bị báo nhầm.
- `_co_ngu_canh_doctrine` là chốt **mềm** nhất trong ba bản vá — nó quyết định bằng *ngữ
  cảnh*. Tìm một đoạn **thật sự chép doctrine** mà lọt qua vì thiếu ngữ cảnh, và một đoạn
  vô hại bị bắt vì thừa ngữ cảnh.

### 2. `_kiem_luoc_do_lease` — một hàm chung có thật sự là MỘT không

- Cả `record-lease` lẫn `begin-attempt` có **thật sự** gọi cùng hàm, hay còn nhánh nào tự
  kiểm sót lại? Đọc mã, đừng tin tên hàm.
- 28 ca khai phủ hết hình dạng chưa? Thử: `lease` là bool; là dict lồng dict; khoá thừa;
  khoá đúng nhưng giá trị toàn khoảng trắng; `expires_utc` đúng dạng nhưng **quá khứ**;
  múi giờ lệch; nhiều `Z`; `granted_by` hợp lệ nhưng viết hoa/thường khác; ký tự `Cf` chèn
  giữa tên người có thẩm quyền (**chuẩn hoá mạnh ở doctrine có được áp cho tên không?**).
- Chiều bắt oan: một state **hợp lệ** có bị chặn khiến packet kẹt cứng không?
- Traceback: còn đường nào vỡ ra traceback thô thay vì mã thoát kiểm soát không?

### 3. Bộ test — ca có MẶT khác ca có ĐO

Suite khai `109/109` + `23` đột biến. Hỏi ngược:

- Có ca nào **`return` sớm** rồi vẫn được đếm ĐẠT (đường dẫn sai, fixture vắng, thư mục
  không có)? Kho này đã trả giá đúng lỗi đó ở `t24`.
- 23 đột biến có phủ **mọi** chốt mới không? Thử gỡ từng chốt trong `_chuan_hoa` và trong
  `_kiem_luoc_do_lease`, đo xem suite có ĐỎ. Chốt nào gỡ mà suite vẫn xanh là một finding.
- Đột biến **sống sót** thì ĐO xem vì sao, đừng kết luận ngay là test yếu.

### 4. AC 20 — và một khuyết của chính công thức

Executor **tự báo**: `git archive` + `git apply` sinh ra thư mục **không có `.git`**, nên ca
`legacy_state_khong_co_lease_bi_chan` (đọc blob lịch sử tại `22d2cc9`) không chạy được và
suite ra **108/109**; với `GIT_DIR` trỏ kho thật thì **109/109**.

Kiểm hai điều, chúng khác nhau:
- Lời khai ấy **đúng không** — tự dựng cây đã merge và đo.
- Cách chữa bằng `GIT_DIR` có **hợp lệ** không, hay nó làm ca đó đo một cây KHÁC với cây
  đang được kiểm? Nếu có, đây là finding mức spec.

Dựng cây đã merge bằng **SHA bất biến**, không dùng `origin/master`:

```bash
MASTER=3d2c52d62696b0c7c190fd891115f543b0f9cb55     # hoặc SHA master lúc BẠN đo, ghi rõ
merged=$(mktemp -d)
git archive "$MASTER" | tar -x -C "$merged"
git diff --binary fbe5ab9e1ece3b45c065879bfd59dee2554db3e2..e6e4b73dc940fcd04e9030e353e0e5fe7f3f0af8 \
  | git -C "$merged" apply
python3 "$merged/.claude/dev/packet_loop.py" doctrine-scan --root "$merged"
```

### 5. Số executor khai mà CHƯA ai chạy lại

Phiên đăng hộ chỉ chạy lại ba mục: suite `109/109` + 23 đột biến, `doctrine-scan` rc=0, và
phạm vi đúng 6 tệp. **Những mục dưới đây chưa ai kiểm** — chúng là phần việc của bạn:

```bash
python3 scripts/tl.py --selftest                                  # ĐÒI hai số BẰNG NHAU
python3 scripts/tl.py doc-claims-check --strict --json            # ĐÒI flags = []
python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --root . --strict --json
python3 scripts/tl.py golden-test                                 # KHÔNG --write
python3 .githooks/eol_policy.py --all --json                      # ĐÒI violations = 0
# release-bundle ×2 trên head + ×1 từ fbe5ab9e — ĐÒI cả BA cùng sha256
```

`rc` của một pipe là `rc` của lệnh **cuối** — đọc rc trực tiếp từng lệnh. Đòi **bằng chứng
dương**, đừng tin `rc=0`.

### 6. Phạm vi và artifact phái sinh

`git diff --name-status fbe5ab9e e6e4b73` phải cho **ĐÚNG 6 tệp** write_set. `VERSION`,
`CHANGELOG`, `RELEASE_MANIFEST.json`, `references/golden/**`,
`scripts/tl_test_fragments_bundled.py` **không được đổi** — kiểm bằng số.

---

## Verdict và evidence

`approve` · `changes_requested` · `blocked`.

- **`approve`** chỉ khi bạn đã tự chạy, tự tìm, và không ra P1/P2 chặn.
- **`changes_requested`** khi có finding cần vá. Còn **2/3 attempt**, nên đừng ngại.
- **`blocked`** khi chính spec/prompt thiếu, hoặc bạn không chạy được phần thiết yếu.

Mỗi finding phải có `finding_id` (slug kebab-case ổn định), `severity`, `disposition`, và
**bằng chứng CHẠY ĐƯỢC neo SHA bất biến** — lệnh cụ thể, mã thoát cụ thể, đầu ra cụ thể.
Finding không tái lập được thì ghi rõ là **nghi vấn**, đừng để lẫn với cái đã đo.

**Nói thẳng chỗ bạn KHÔNG chạy được.** Lượt 4 và 5 đều làm vậy và nhờ thế người đọc biết
ranh giới của bản review.

### Giao kết quả

Ưu tiên: review trên **PR #115** neo `commitID = e6e4b73dc940fcd04e9030e353e0e5fe7f3f0af8`,
kèm evidence §7 lên issue #55.

Không ghi được lên GitHub thì ghi vào kho — **đúng khuôn lượt 5, nó chạy được**:

```
ops/reviews/wp55-r3-review-6-codex-verdict.md            # NGUYÊN VĂN verdict, không sửa
ops/reviews/wp55-r3-review-6-codex-verdict.receipt.yaml  # chỗ đăng + băm, tệp RIÊNG
```

Xuất **thẳng `stdout` ra tệp**, đừng chép tay — lượt 4 chép tay và đã lệch một chỗ; lượt 5
bỏ khâu chép và byte-identical. Rồi push lên một nhánh `ops/**` và báo `sha256` + số byte.

---

## Stop conditions

Head đổi giữa chừng · lease hết hạn · bạn không phải `codex` · BƯỚC 0 lệch · bị đòi sửa
tệp/commit/push/merge/land (**không phải vai của bạn**) · không chạy được phần thiết yếu
(báo `blocked` kèm lý do đo được, đừng đoán rồi `approve`) · chạm quota (ghi lý do allowlist,
**không** tiêu attempt nội dung).

Heartbeat **mỗi 30 phút** lên #55. Nếu đường ghi bị chặn, ghi nhịp vào tệp trong kho và nói
rõ — đừng để im lặng bị đọc nhầm thành phiên chết.
