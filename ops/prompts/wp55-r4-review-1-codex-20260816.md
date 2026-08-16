# Prompt REVIEWER — wp55 revision 4, generation 1, lượt review 1

**Vai:** `codex`. §8 bắt reviewer khác provider với executor, và executor lượt này là `claude`.
**Quyền:** `read-only`. `write_set: []`, `branch_ownership: none`. KHÔNG commit, KHÔNG push lên
`claude/wp55-r4g1-f3-03`, KHÔNG sửa spec. Verdict đi bằng một tệp trên nhánh `ops/**` của riêng
bạn.

**Neo bất biến.** Đọc bằng SHA, không bằng tên nhánh. Tên nhánh dời được; SHA thì không.

| | |
|---|---|
| head để review | `2432e3f64f05739741dfe6f49081e9aaa140799f` |
| nhánh | `claude/wp55-r4g1-f3-03` (chỉ là cái tên — đo bằng SHA) |
| `base_sha` | `18da1da6a07ab2c86d716cef1d74ff2cd0e3218a` (tip master sau PR "#129") |
| `start_from_sha` | `b0e3e3b6a4c630ba0652b8fc939025d9c4031c67` |
| spec | `ops/specs/wp55-r4-spec.md` trên `ops/wp55-r4-spec-draft` |
| `spec_hash` | `86d9627caf55ea2cb8e4caa29ef036fd490c190d8481fb4f79dd5d1703eb1afd` |
| bàn giao §7 | `ops/handoff/wp55-r4g1-handoff.md` trên `ops/wp55-r4g1-handoff` |

Không có pull request cho nhánh này. Review neo thẳng vào SHA, đừng đi tìm PR.

---

## BƯỚC 0 — ba phép đo trước khi đọc một dòng diff

```bash
git fetch origin ops/wp55-r4-spec-draft
git show origin/ops/wp55-r4-spec-draft:ops/specs/wp55-r4-spec.md | sha256sum
# ĐÒI: 86d9627caf55ea2cb8e4caa29ef036fd490c190d8481fb4f79dd5d1703eb1afd

git fetch origin claude/wp55-r4g1-f3-03
git rev-parse origin/claude/wp55-r4g1-f3-03
# ĐÒI: 2432e3f64f05739741dfe6f49081e9aaa140799f

git merge-base --is-ancestor 4085bbf2 2432e3f6; echo "rc=$?"
# ĐÒI rc=0 — bản vá P1 an ninh cho SKILL.md phải nằm trong tổ tiên
```

Lệch bất kỳ dòng nào ⇒ **DỪNG, hỏi chủ kho.** Một spec khác spec được duyệt không phải spec
được duyệt, và một head khác head được neo thì verdict của bạn nói về vật khác.

`4085bbf2` vá chỗ `SKILL.md` nối `${VAR:+…}` với `${VAR:-…}` — nhánh "đã đặt" bung ra CHÍNH GIÁ
TRỊ biến bí mật. `SKILL.md` nằm trong `write_set`, nên nếu nó không phải tổ tiên thì lượt này đã
mở lại lỗ ấy trong im lặng.

---

## Bốn mục kiểm — đây là chỗ đáng soi nhất của lượt này

Executor đã tự khai đường đi. Nhiệm vụ của bạn KHÔNG phải đọc lại lời khai mà là **đo lại**.

### 1 · Cặp cùng-hình-dạng có phủ MỌI hình dạng không

Mười hai ca đổi ma trận nằm ở `LOP_LACH` với đuôi `_tha_cu`; mười hai ca CÙNG TÊN GỐC ở lại
`LOP_BAT_OAN`, được viết lại nội dung nhưng **khai là giữ y hệt hình dạng**: bảng chưa đóng thẻ,
rào bốn backtick, dòng thụt lề, mã inline, comment, bullet, danh sách số, trích dẫn.

Cặp ấy là thứ duy nhất chứng minh cổng phân biệt **NỘI DUNG** chứ không phân biệt **CẤU TRÚC
Markdown**. Đã đo sẵn cho bạn một nửa: cả 12 ca `_tha_cu` đều có một ca cùng gốc tên bên
`LOP_BAT_OAN`, tức **không thiếu ca nào theo TÊN**. Đó là phần dễ, và nó đã xanh.

Phần khó, và là phần bạn phải làm: **tên khớp không có nghĩa hình dạng khớp.** Với từng cặp, so
cấu trúc chứ đừng so tên — cùng số dòng, cùng loại rào, cùng mức thụt lề, cùng thẻ mở/đóng, cùng
vị trí ngắt dòng — và chỉ khác đúng ở cụm chữ. Một hình dạng chỉ có mặt ở MỘT vế là **finding
thật**: nó nghĩa là với hình dạng ấy, cổng chưa bao giờ được đo ở chiều bắt oan.

Soi kỹ hai chỗ đã thấy có mùi:

- `cum_don_van_xuoi_sau_bang_html_tha_cu` và `cum_don_van_xuoi_sau_bang_html_chua_dong_tha_cu` là
  hai ca khác nhau, nhưng khớp tên lại đụng chung `oan_van_xuoi_sau_bang_html_chua_dong`. Kiểm
  xem hai ca lọt có đúng hai ca bắt-oan RIÊNG BIỆT không, hay hai ca dùng chung một đối chứng.
- `oan_claude_md_master` là ca THẬT lấy từ `CLAUDE.md` của master. Kiểm bản `_tha_cu` của nó có
  còn giữ đúng cấu trúc thụt lề bốn dòng đó không.

### 2 · Hai đột biến mới có nhắm đúng tầng không

Mười hai đột biến cũ mất mỏ neo vì máy dò cấu trúc phục vụ miễn trừ đã bị xoá. Thay bằng hai cái:

| đột biến | giết | executor khai nó phủ |
|---|---|---|
| `mo_lai_mien_tru_ngat_dong` | 37 ca | mọi hình dạng ngắt dòng, generation 6–9 |
| `tha_vo_dieu_kien_nhu_generation_4` | 43 ca | thêm 6 lớp MỘT DÒNG mà cái trên không với tới |

Con số 37 và 43 **lớn bất thường** so với đột biến thường. Executor giải thích rằng đó là đúng
chứ không phải nhắm sai tầng, vì miễn trừ vốn tha theo HÌNH DẠNG nên mở lại nó thì mọi hình dạng
cùng lọt một lượt. Lời giải thích ấy hợp lý — nhưng nó là lời giải thích, không phải phép đo.

Việc của bạn: chạy từng đột biến rồi đối chiếu tập ca chết THỰC TẾ với danh sách phải-chết ghi
trong tệp. Đòi hai chiều:

- Mọi ca trong danh sách có chết thật không (thiếu ⇒ danh sách kê tay, không đo).
- Có ca nào chết mà KHÔNG có trong danh sách không (thừa ⇒ đột biến giết cả đối chứng khác họ,
  tức nó không nhắm đúng tầng).

Đặc biệt: đột biến nào giết một ca của `LOP_BAT_OAN` là **finding**. Hai đột biến này chỉ được
phép chạm ma trận LỌT.

Và kiểm chỗ executor tự khai là lý do cần cả hai: suite báo thẳng *"6 lớp KHÔNG đột biến nào
giết"* khi mới có `mo_lai_mien_tru_ngat_dong`. Tái lập câu báo ấy — bỏ
`tha_vo_dieu_kien_nhu_generation_4` đi thì đúng sáu lớp `cum_don_heading`, `dong_tran`,
`gach_dau_dong`, `in_dam`, `dinh_nghia`, `cau_van_xuoi_mot_dong` phải hở. Không hở đúng sáu lớp
ấy ⇒ một trong hai đột biến đang thừa.

### 3 · Tái lập `280 dòng / 18,6%` và `37 / 43` — đừng nhận theo lời kể

Spec ước lượng `~241 dòng, ≈16%`. Executor đo ra `280 dòng, 18,6%`. Số liệu suite tự in:

```
ca               : 185
đột biến         : 34
lớp lách         : 78
ca bắt-oan       : 35
ngoại lệ AC 18   : 0
```

Nền trước lượt này: `173 / 44 / 66 / 35 / 0`.

Chạy suite, đọc khối `SỐ LIỆU (đếm bằng máy)` mà AC 25 bắt nó tự in, so từng con số. Con số nào
lệch với lease/handoff/commit là finding — AC 25 sinh ra đúng vì một lượt trước khai `39 đột
biến` trong khi thật là `38`.

`18,6%` là tỉ lệ trên tệp nào, tử số mẫu số là gì — đòi executor đã nói rõ, và tự tính lại.
`packet_loop.py` ở head này đo được **1223 dòng**; handoff khai nó từ `1503` xuống. `1503 − 1223
= 280`, và `280 / 1503 = 18,6%`. Kiểm xem `1503` có đúng là số dòng ở `start_from_sha` không —
nếu mẫu số lấy nhầm tệp hoặc nhầm SHA thì cả hai con số cùng sai.

### 4 · Còn mã miễn trừ nào chỉ bị VÔ HIỆU chứ không bị XOÁ không

AC 19 mục 2 đòi **XOÁ**, không đòi vô hiệu. Executor khai đã xoá:

`_duoc_tha_vi_ngat_dong`, `_dong_khoi_ma`, `_dong_bang_html`, `_go_dau_dong_tho`, `_CO_CHU`,
`_RE_DAU_DONG_THO`, `_RE_HANG_RAO`, `_RE_MO_BANG`, `_RE_DONG_BANG`, `_RE_MA_INLINE`,
`_RE_COMMENT_MOT_DONG`, `_DAU_HIEU_PHEP_DO`, `CUM_NGON_NGU_THUONG`.

và khai GIỮ CÓ CHỦ Ý: `_go_dau_dong` (còn dùng bởi `_khuc_chuan`), `_RE_DAU_DONG`, `_dong_tai`.

Quét cả cây, không chỉ `packet_loop.py`. Tìm ba dạng sót:

- Hàm/hằng còn ĐỊNH NGHĨA mà không còn ai gọi (mã chết — đúng thứ AC 19 mục 2 cấm).
- Nhánh `if` bị ép `False`, cờ đặt cứng, tham số mặc định làm miễn trừ tắt mà thân vẫn còn.
- Ba cái khai là "giữ có chủ ý" — kiểm chúng thật sự còn người dùng. `_go_dau_dong` có đúng là
  `_khuc_chuan` gọi không, hay lời khai ấy cũng chỉ là lời khai.

Executor giữ lại một **khối chú thích lịch sử** về ba lớp lỗi sẽ quay lại nếu revision sau mở
lại miễn trừ. Khối ấy được phép giữ. Nhưng kiểm nó chỉ là chú thích, không phải mã bị comment ra
— mã bị comment ra là mã chết ở dạng khó thấy nhất.

---

## Ba chỗ executor tự khai NGƯỢC VỚI SPEC — kiểm lại cả ba, đừng nhận

Executor khai thẳng ba chỗ lệch spec. Khai thẳng là đúng nếp và đáng ghi nhận, nhưng **khai
không phải là chứng minh**. Cả ba đều phải đo lại:

1. **Spec đoán HAI ca đổi ma trận; đo thật MƯỜI HAI.** Executor khai phân hoạch sạch: 12 ca đỏ
   đúng bằng 12 ca CÓ chứa cụm cấm, 23 ca không chứa vẫn xanh, không ca nào đỏ vì lý do khác.
   Đo lại chính câu đó — đếm ca chứa cụm cấm, đếm ca đỏ, đòi hai tập TRÙNG KHÍT. Lệch một ca là
   hợp đồng cơ học không chạy đúng thiết kế.
2. **`~241 / ~16%` → `280 / 18,6%`, và `_RE_BANG_HTML` KHÔNG TỒN TẠI trong tệp.** Spec liệt kê
   `_RE_BANG_HTML` trong danh sách phải xoá. Kiểm nó thật sự chưa bao giờ có ở
   `start_from_sha` — nếu nó CÓ mà bị bỏ sót thì lời khai "không tồn tại" đang che một chỗ chưa
   xoá.
3. **Mười hai đột biến mất mỏ neo, thay bằng hai.** Kiểm việc thay thế không làm mất độ phủ:
   `34` đột biến ở head so với `44` ở nền. Mười hai mất, hai thêm — con số ra `34` chứ không
   phải `44 − 12 + 2 = 34`; nó khớp. Nhưng khớp số không phải khớp độ phủ. Đòi: mọi lớp trong
   `LOP_LACH` vẫn có ít nhất một đột biến giết đúng nó (AC 18), và suite tự chốt điều đó chứ
   không để người kê.

---

## Phải đo trên CÂY ĐÃ MERGE, không chỉ trên nhánh (AC 20)

Công thức đã sửa. `GIT_DIR` là phần **bắt buộc**, không phải trang trí:

```bash
MASTER=18da1da6a07ab2c86d716cef1d74ff2cd0e3218a
TREE=$(mktemp -d)
git archive "$MASTER" | tar -x -C "$TREE"
git diff --binary 18da1da..2432e3f6 | git -C "$TREE" apply
python3 -B "$TREE/.claude/dev/packet_loop.py" doctrine-scan --root "$TREE"
GIT_DIR="$PWD/.git" python3 -B "$TREE/.claude/dev/packet_loop_test.py"
```

Executor báo `rc=0` cả hai, và kèm một **chứng đường**: bỏ `GIT_DIR` thì suite phải ĐỎ
(`fatal: not a git repository`), và nó đỏ thật — nên finding
`ac20-archive-tree-suite-not-self-contained` hoãn từ verdict lượt 6 đã đóng THẬT. Chạy lại cả
ba dòng ấy, kể cả dòng cố ý đỏ. **Nếu bỏ `GIT_DIR` mà vẫn xanh thì điều kiện spec vừa thêm là
thừa và cả AC 20 chỉ là nghi lễ** — đó là finding, và là finding lớn.

Kiểm thêm: phạm vi diff đúng 6 tệp `write_set`, không ra ngoài.

`18da1da` là tip master **tại lúc soạn spec**. Master tiến thêm thì phải đo lại AC 20 trên tip
mới — AC 20 nói *cây đã merge*, không nói *cây tại base_sha*. Kiểm master còn ở `18da1da` không,
và nếu đã tiến thì nói ra.

---

## AC 26 — sổ commit

Đúng hai commit ở lượt này, cả hai khai cùng `lease_id`
`wp55-r4-exec-1-claude-20260816`:

| sha | nội dung |
|---|---|
| `179d5f37` | merge master `18da1da` vào nhánh packet |
| `2432e3f6` | AC 19 bỏ hẳn miễn trừ — xoá cơ chế, nối lại ma trận |

Đo `git log 18da1da..2432e3f6` và đòi KHÔNG có commit thứ ba. Revision 3 hỏng đúng ở chỗ này —
bốn commit chạy không lease — và AC 26 sinh ra để chặn. Commit không khai được lease là commit
ngoài sổ, và bạn có quyền tính đó là finding.

---

## Cạm bẫy đã trả giá — đọc trước khi gõ

**Đọc `rc` qua ống là đọc `rc` của lệnh cuối.** `cmd | head -1` cho `rc` của `head`. Bắt `rc`
ngay sau lệnh, hoặc dùng `PIPESTATUS`. Lỗi này đã lọt một lần và làm một cổng đỏ báo xanh.

**Phép đo rỗng còn tệ hơn không đo.** Một lượt trước dò một hàm bằng tên đoán, `hasattr` trả
`False`, cả bốn ca cùng ra `rc=0`, trông như "sạch". Mọi phép mô phỏng phải có **chứng đường**:
một ca BIẾT PHẢI ĐỎ. Nó không đỏ ⇒ phép đo hỏng, không phải cây sạch.

**Backtick trong `git commit -m` bị shell nuốt.** Dùng `-F` với tệp. Đã mất ba lần.

**In phản hồi thô trước, phân tích sau.** Một lời gọi API đã thành công nhưng trình phân tích
nuốt kết quả và in `PR "#None"`; lượt gọi lại trả `422 already exists`.

**Không in nội dung biến bí mật.** Kiểm bằng `-n` và `${#VAR}`, không bao giờ bằng expansion nối
chuỗi. Đây chính là lỗ `4085bbf2` vá, và nó đã bị vi phạm thật một lần — `CODEX_AUTH_JSON` phải
thu hồi và cấp lại trong phiên 15-08 vì một executor in nó ra transcript.

---

## Lỗ đã biết, NGOÀI phạm vi lượt này — đừng tính là finding mới

Executor nói ra trước thay vì để bạn phát hiện. Ghi nhận, đừng mở lại:

1. **Hook tin `codex login status`.** Chốt "không ghi đè khi đã đăng nhập" tin lệnh ấy, mà lệnh
   ấy chỉ đọc TỆP chứ không hỏi máy chủ — ngày 16-08 nó báo `Logged in` với một token ĐÃ THU
   HỒI. Lỗ thật, **ngoài `write_set`**, cố ý không đóng ở lượt này.
2. **Sổ attempts của revision 3 không khớp thực tế** — bốn commit chạy không lease. Revision 4
   không hồi tố sửa được; AC 26 chỉ chặn tái diễn.
3. **Chưa chạy `ruff` / gate phát hành đầy đủ** trên nhánh này. `packet_loop*.py` là công cụ
   dev-side, không vào gói. Nếu bạn muốn đó là phép đo thiếu thì cứ nêu — executor đã tự nhận là
   thiếu, nên nêu nó là bổ sung chứ không phải bắt lỗi giấu giếm.

`AGENTS.md`, wiring suite vào CI, `land-packets --apply`, và **cơ chế miễn trừ dưới mọi hình
thức** đều ngoài phạm vi theo spec. Đề xuất mở lại miễn trừ KHÔNG phải là finding hợp lệ ở lượt
này — chủ kho đã chốt BỎ, sau khi đo được rằng nó không có người dùng nào.

---

## Verdict — dạng và chỗ đặt

Đặt `ops/reviews/wp55-r4-review-1-codex-verdict.md` trên một nhánh `ops/**` của riêng bạn rồi
push. KHÔNG đẩy lên `claude/wp55-r4g1-f3-03`.

Verdict phải mang, tối thiểu:

- `reviewed_sha: 2432e3f64f05739741dfe6f49081e9aaa140799f` — đúng SHA bạn đã đo, không phải tên
  nhánh. Bạn đo một SHA khác thì nói SHA ấy ra.
- `spec_sha256` bạn đã xác minh.
- `verdict`: `approve` | `approve_with_findings` | `do_not_land`.
- `land_recommendation` nếu `approve`.
- Mỗi finding một `finding_id` dạng kebab, kèm **lệnh tái lập và `rc` thật**. Finding không tái
  lập được là ý kiến, không phải finding.
- Bốn mục kiểm ở trên: nói rõ từng mục **đã đo** hay **chưa đo**. Mục chưa đo phải khai là chưa
  đo. "Không kiểm được" khác "đạt", và gộp hai thứ ấy là đúng lỗi mà cả packet này sinh ra để
  chặn.

Nếu head dời khỏi `2432e3f6` giữa chừng: **DỪNG**, báo chủ kho. Duyệt một head rồi land một head
khác là đúng chỗ lượt review 8 đã hỏng.

## Trần lượt

`attempts_limit: 3`, `attempts_used: 1` (executor đã tiêu một lượt nội dung). Cạn trần ⇒ §12,
dừng và bàn giao, không tự gia hạn.
