# wp55 revision 2 · generation 3 · CROSS-REVIEW lượt 5 — reviewer `codex`

Bạn là **reviewer độc lập** cho work packet **wp55** (issue #55), mission #54 revision 6.
Vai này **CHỈ ĐỌC**: không sửa tệp, không commit, không push, không merge, không land,
không deploy. Đầu ra là **verdict** + **evidence §7**.

§8 đòi reviewer khác provider với executor. Executor là `claude` ⇒ reviewer phải là
`codex`. Nếu bạn không phải `codex`, **DỪNG** và báo lại.

---

## BƯỚC 0 — xác minh danh tính TRƯỚC khi đọc bất cứ gì

Sai bất kỳ mục nào ⇒ **DỪNG**, báo lại, không review.

```bash
# 0a. đúng kho
git remote -v                       # phải là github.com/ducthangho/tra-luat

# 0b. đúng prompt — tệp này, không phải bản chép trong comment
#     Tìm ở `master` trước; chưa thấy thì fetch nhánh ops đang mang nó:
#     git fetch origin ops/wp55-lease-review-5
sha256sum ops/prompts/wp55-r2-review-5-codex-20260814.md
#   PHẢI khớp `prompt_sha256_required` trong lease. Lệch ⇒ DỪNG.

# 0c. đúng head phải review
git fetch origin claude/wp55-r2g2-f3-03
git rev-parse origin/claude/wp55-r2g2-f3-03
#   PHẢI = 546ecf9fd4dfe889d0cd3ee77b9589d8bed0465f
#   Khác ⇒ executor đã đẩy tiếp ⇒ DỪNG, hỏi bên điều phối.
```

**Kiểm đường giao verdict TRƯỚC khi làm việc.** Đây không phải thủ tục: vòng 3 của
revision 1 review xong rồi **không ghi được verdict**, và lượt 4 cũng vậy — mọi lời gọi
ghi qua MCP trả `user cancelled MCP tool call`, `gh` không có, `api.github.com` trả 403
qua proxy. Verdict lượt 4 phải nhờ phiên khác đăng hộ.

Nên **thử ngay** đường bạn định dùng (MCP GitHub, `gh`, hay git push). Không giao được
thì **vẫn review**, nhưng ghi verdict vào một tệp trong kho theo mẫu ở mục "Giao kết
quả" và nói rõ ai cần đăng hộ — đừng bỏ dở.

---

## Đối tượng review

| | |
|---|---|
| head | `546ecf9fd4dfe889d0cd3ee77b9589d8bed0465f` |
| base | `fbe5ab9e1ece3b45c065879bfd59dee2554db3e2` |
| nhánh | `claude/wp55-r2g2-f3-03` · PR **#92** |
| diff cần soi | `git diff cf39109c9e5167516c53f2071e5fa7ec5c6afff5..546ecf9` — **đúng 2 tệp** |

Generation 3 vá **ba finding P1** do chính lượt review 4 nêu. Bản verdict lượt 4 nằm
trong kho, neo băm — **đọc nó trước, đừng chỉ đọc prompt này**:

```
ops/reviews/wp55-r2-review-4-codex-verdict.md
sha256 = d58088bec10ad36a912b64749cbe8a41af5de0b3f70033d9109f12bb6647e82f
```

| finding_id | executor khai đã vá thế nào |
|---|---|
| `lease-authority-spoof` | `--granted-by` đảo danh sách CẤM → CHO PHÉP (`NGUOI_CO_THAM_QUYEN`), giữ chốt `PROVIDERS` cũ song song |
| `legacy-lease-bypass` | `begin-attempt` đổi fail-open → fail-closed khi `lease` thiếu/hỏng |
| `doctrine-rendering-bypass` | `_chuan_hoa` thêm `html.unescape` một lần + lọc ký tự Unicode `Cf` |

---

## Số đã có — ĐỪNG chép lại, hãy tìm chỗ chúng KHÔNG đủ

Một phiên `claude` khác đã chạy lại và đối chiếu; các số dưới đây **khớp** lời khai của
executor. Chép lại chúng không thêm giá trị nào — **giá trị của bạn nằm ở chỗ chúng
chưa phủ.**

```
packet_loop_test.py      54/54  (nền cũ 48/48)
đột biến                 11/11 giết đúng ca đích
tl.py --selftest         1696/1696, 0 FAIL
doc-claims --strict      ok, flags rỗng
release-verify --strict  ok, 179/179, failed 0, extra 0
golden-test              ok (không --write)
doctrine-scan --root .   sạch, 4 tệp
merge-tree với master    rc=0
git diff --check         rc=0
phạm vi                  đúng 2 tệp, cả hai trong write_set
```

Hai phép đo hành vi cũng đã làm: bốn tên giả mạo `rc=7` / chủ kho `rc=0`; zero-width và
HTML entity `rc=6` / dòng sạch `rc=0`.

**Ba số này do phiên CÙNG PROVIDER với executor chạy.** Chúng không thay được lượt
cross-review, và bạn được yêu cầu **tự kiểm lại** thay vì tin.

---

## Hướng tấn công — nơi đáng dồn sức

Lượt 4 tìm ra ba P1 bằng cách đi tìm **hình dạng khác của cùng một lỗ**. Làm lại đúng
tinh thần đó, đừng dừng ở "bản vá có chạy không".

### 1. `NGUOI_CO_THAM_QUYEN` — danh sách cho phép có thật sự đóng không

- Chuẩn hoá tên: khoảng trắng đầu/cuối, hoa/thường, NFC vs NFD, ký tự Unicode định dạng
  (`Cf`) chèn giữa, chữ cái đồng tự (Cyrillic `а`, Hy Lạp `ο`). Có tên nào **lọt vào**
  danh sách cho phép mà đáng ra không được?
- Chiều ngược: có tên **hợp lệ** nào bị chặn oan?
- Chốt `PROVIDERS` cũ chạy **trước** hay **sau** danh sách cho phép? Thứ tự có tạo ra
  thông điệp sai lệch, hay một đường vòng không?
- **Giới hạn executor tự khai:** danh sách chứng minh cái *tên*, không chứng minh *người*.
  Lời khai ấy có được viết đúng trong chú thích, hay ở đâu đó vẫn khai rộng hơn?

### 2. `begin-attempt` fail-closed — đóng hết hay chỉ đóng ca đã biết

- `lease` thiếu hẳn · `lease` là `null` · là chuỗi · là mảng · là dict rỗng · thiếu
  `expires_utc` · `expires_utc` rỗng / sai định dạng / thiếu múi giờ / là số.
- State cũ sinh bởi **các head khác** ngoài `22d2cc9` — còn hình dạng state nào lọt?
- Chiều bắt oan: có state **hợp lệ** nào nay bị chặn khiến packet kẹt cứng?
- `record-lease` và `begin-attempt` có **cùng** định nghĩa "lease hợp lệ" không? Lệch
  nhau là một đường vòng.

### 3. `_chuan_hoa` — giải entity một lần + lọc `Cf`

- Còn lớp ký tự nào **render ra cùng cụm cấm** mà chưa bị quy về một mối? Dấu nháy cong,
  NBSP và các khoảng trắng Unicode khác, dấu gạch nối mềm, chữ toàn rộng, đồng tự, thực
  thể **thập phân** vs **thập lục** vs **tên** (`&#58;` `&#x3A;` `&colon;`), thực thể
  không có dấu chấm phẩy.
- **Chống double-decode:** `&amp;#58;` hiển thị nguyên văn `&#58;`, KHÔNG phải dấu hai
  chấm. Giải một lần là đúng — nhưng hãy **kiểm nó thật sự chỉ một lần**, và kiểm chiều
  bắt oan: một tài liệu viết `&amp;#58;` hợp lệ có bị báo nhầm không?
- Lọc `Cf` có nuốt nhầm ký tự cần thiết cho tiếng Việt hay cho Markdown không?

### 4. Bộ test — "ca có mặt" khác "ca có đo"

Suite tự khai 54/54 và 11 đột biến. Hãy hỏi ngược:

- Có ca nào **`return` sớm** rồi vẫn được đếm là ĐẠT (đường dẫn sai, thư mục không có,
  fixture vắng)? Kho này đã trả giá đúng lỗi đó ở `t24`.
- 11 đột biến có phủ hết **mọi** chốt mới không, hay còn chốt nào gỡ đi mà suite vẫn xanh?
  Thử gỡ từng chốt và đo.
- Ca `case_legacy_state_khong_co_lease_bi_chan` đòi lịch sử không-shallow. Trên clone
  shallow nó **báo lỗi rõ** hay **âm thầm bỏ qua**? Executor khai là báo rõ — kiểm.

### 5. Tương tác với master

`master` nay ở `3d2c52d`, đã đi rất xa kể từ base. Trong 6 tệp write_set nó **chỉ chạm
`CLAUDE.md`**, và `merge-tree` cho `rc=0`. Nhưng:

- `doctrine-scan` quét `.claude/skills/**` + `CLAUDE.md`. Chạy nó trên **cây ĐÃ MERGE**
  với master — `CLAUDE.md` của master nay dài hơn nhiều và có nhắc tới các cụm doctrine
  trong phần bài học. Có bắt oan không?
- Master đã thêm `.claude/skills/goi-claude-cli/` (nếu PR #110 đã land). Nó có vào phạm
  vi `doctrine-scan` không, và có gây đỏ sau khi merge không?

---

## Verdict và evidence

Verdict là một trong: `approve` · `changes_requested` · `blocked`.

- **`approve`** chỉ khi bạn đã tự chạy và tự tìm, không tìm ra P1/P2 chặn nào.
- **`changes_requested`** khi có finding cần vá.
- **`blocked`** khi chính spec/prompt thiếu, hoặc bạn không chạy được phần thiết yếu.

Mỗi finding phải có: `finding_id` (slug ổn định), `severity`, `disposition`, và **bằng
chứng CHẠY ĐƯỢC** — lệnh cụ thể, mã thoát cụ thể, đầu ra cụ thể. Một finding không tái
lập được thì ghi rõ là **nghi vấn**, đừng để lẫn với cái đã đo.

**Nói thẳng chỗ bạn KHÔNG chạy được.** Lượt 4 làm đúng vậy và nhờ thế người đọc biết
ranh giới của bản review.

### Giao kết quả

Ưu tiên: **review trên PR #92** neo `commitID = 546ecf9fd4dfe889d0cd3ee77b9589d8bed0465f`,
kèm evidence §7 đăng lên issue #55.

Không ghi được lên GitHub thì **ghi vào kho**:
`ops/reviews/wp55-r2-review-5-codex-verdict.md` — phần 1 là review cho PR #92, phần 2 là
evidence §7 dạng YAML, phân cách bằng một dòng `---`. Rồi push lên một nhánh `ops/**` và
báo băm `sha256` của tệp. Đó là đường mà lượt 4 đã dùng; nó chạy được.

**Nếu có người đăng hộ:** con băm là thứ duy nhất chứng minh họ đăng đúng lời bạn. Lượt
4 đã có một chỗ lệch vì lớp mã hoá JSON của đường MCP giải mã chuỗi thoát — nên nếu
verdict của bạn chứa chuỗi thoát hay ký tự vô hình, **nói rõ ngay trong verdict** rằng
chúng là cố ý.

---

## Stop conditions — gặp thì DỪNG và báo, đừng tự xoay

- BƯỚC 0 lệch bất kỳ mục nào.
- Bạn không phải provider `codex`.
- Head đổi giữa chừng — review một head đang trôi là review vô nghĩa.
- Lease hết hạn giữa chừng.
- Bị đòi sửa tệp, commit, push code, merge hay land: **không phải vai của bạn**.
- Không chạy được phần thiết yếu (vd bộ test) — báo `blocked` kèm lý do đo được, đừng
  đoán rồi `approve`.
