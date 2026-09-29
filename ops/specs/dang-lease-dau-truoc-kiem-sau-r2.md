# ĐẶC TẢ — `DANG-LEASE-DAU-TRUOC-KIEM-SAU` — **revision 2, ĐÓNG BĂNG**

| trường | giá trị |
|---|---|
| `packet_id` | `DANG-LEASE-DAU-TRUOC-KIEM-SAU` |
| `revision` | **2** |
| `thay_the_cho` | revision 1, `7c8fb871a7f015720dc5ed7de4748dd23ea5ae614314c02b98e859aa9005419a` |
| `packet_issue` | **#579** |
| `nguon_cap_viec` | Chỉ thị chủ kho 21-09-2026: *"Anh soạn r2 gói cả ba đi"* — trả lời cho ba chặn mà phiên điều phối trình cùng lượt (§0.2). |
| `review_class` | **`sensitive`** — chạm `ops/lease_publish.py`, tức cổng đọc lease (protocol §8). |
| `assurance_target` | **`human_audited`** — không đổi so r1. `cross_approved` **KHÔNG ĐẠT ĐƯỢC**: codex đăng *"You have reached your Codex usage limits for code reviews"* trên PR #577 (10:52Z 20-09) và PR #580 (17:20Z 20-09); agy hết quota; claude là executor. |
| `executor` | `claude` |

**GIỚI HẠN LỜI KHAI:** mọi khẳng định chỉ chứng minh tới đúng phép đo ghi kèm.
**Ba trạng thái:** có · không · **KHÔNG ĐO ĐƯỢC** — trạng thái thứ ba làm cổng ĐỎ.

**r2 KHÔNG đổi bệnh, KHÔNG đổi Q1/Q2/Q4, KHÔNG đổi M1–M8.** Nó đổi đúng ba thứ, và cả ba đều
là chuyện của THẨM QUYỀN chứ không của mã. Chi tiết bệnh, cơ chế và hiện vật: đọc r1 §1.

---

## 0. Vì sao có revision 2

### 0.1 — Bốn quyết định của r1, GIỮ NGUYÊN

| câu | quyết định |
|---|---|
| **Q1** vá ở đâu | `kiem_github`: dò dấu "đã đăng" TRƯỚC, gọi `kiem()` SAU |
| **Q2** phạm vi | vá cổng + ghi nếp vào `CLAUDE.md`; `_kiem_bia_mo` giữ nguyên |
| **Q3** đường qua chặn write set | hỏi #578 và #570 nhả sớm; không cấp lease trước khi đo `NGƯỜI_GIỮ 0` |
| **Q4** bảo chứng | `human_audited` |

### 0.2 — Ba quyết định MỚI của r2

| câu | quyết định | mục |
|---|---|---|
| **Q5** write set trong lúc #578 còn giữ | **Thu hẹp tạm thời**: gỡ `ops/lease_publish_test.py` khỏi write set cho tới `2026-09-21T10:30:00Z`, rồi TRẢ LẠI | §2 |
| **Q6** vượt trần `ADR-0044` | **Khai lý do trong spec** — đúng một trong hai đường mà chính ADR cho phép | §8 |
| **Q7** chỗ lease lệch Q3 | **Hoà bằng r2**, không sửa r1 và không giả vờ Q3 đã được thoả mãn | §9 |

---

## 1. Bệnh — không đổi

Đọc r1 §1. Tóm đúng một câu để người đọc r2 không phải nhảy tệp: `kiem_github` gọi `kiem()` ở
dòng đầu, mà `kiem()` ném `rc=8` cho lease hết hạn **trước** khi chốt `rc=9` của
`_kiem_comment_da_co` kịp chạy — nên một lease **đã đăng rồi mới hết hạn** không bao giờ tới
được nhánh `rc=9` mà workflow đã có sẵn và viết đúng.

**Đo lại 21-09-2026 để câu trên không thành lời khai cũ** (L5), `kiem_github` với `_doc_gh` giả,
nền `origin/master` `a1bbdc1`:

```
còn hạn + ĐÃ có dấu   ->  rc=9
HẾT HẠN + ĐÃ có dấu   ->  rc=8     <- bệnh, chưa vá
HẾT HẠN + KHÔNG dấu   ->  rc=8
còn hạn + KHÔNG dấu   ->  rc=0
```

## 2. `write_set` — KHAI THEO THỜI GIAN, vì nó đổi giữa chừng

Đây là chỗ r2 khác r1 rõ nhất, và nó phải đọc được mà không cần mở tệp lease nào.

| giai đoạn | write set | generation | vì sao |
|---|---|---|---|
| tới `2026-09-21T10:30:00Z` | `ops/lease_publish.py` · `CLAUDE.md` | **g2** | §2.1 |
| từ `2026-09-21T10:30:00Z` | `ops/lease_publish.py` · `CLAUDE.md` · `ops/lease_publish_test.py` | **g3** | §2.2 |

Cả hai giai đoạn đều **≤ 3 tệp**, tức vế TỆP của `ADR-0044:5` đạt ở mọi thời điểm. Vế DÒNG
không đạt — xem §8.

### 2.1 — Vì sao thu hẹp (Q5), và nó gỡ một thế kẹt có thật

Phiên #578 trình ba đường cho chủ kho lúc `20:07Z` 20-09; chủ kho chọn đường 1 và bảo *"soạn
commit cho tôi duyệt"*. Bản nháp nằm ở `claude/nhap-thu-hep-579-20260921` (`c78991c`).

Thế kẹt, viết bằng lời của chính bản nháp ấy và đã kiểm lại:

- Lease #578 đòi *"không còn người giữ nào NGOÀI chính nó"* trên `ops/lease_publish_test.py`.
- Lease #579 g1 **là** một người giữ — mà chính nó khai ở `DIEU_KIEN_BAT_DAU` rằng **không**
  chạm đường ấy trước 10:30Z.
- Nên hai bên chờ nhau, và kết cục duy nhất là #578 hết hạn lúc 10:30Z **mà chưa ghi một dòng**.

Giữ một đường mình tự khai là không dùng đúng là thứ write-set exclusion sinh ra để chặn. Gỡ nó
**không làm #579 mất việc nào trong cửa sổ ấy**, vì `A1`–`A6` vốn đã không đạt được trước 10:30Z.

**XUNG ĐỘT LỢI ÍCH, khai thẳng:** bản sửa do phiên **#578** soạn, và #578 là bên HƯỞNG LỢI. Phiên
ấy trình ba đường chứ không tự chọn; chủ kho chọn. Và phiên ấy **không** đẩy lên `ops/**` — hành
vi CẤP là lần push, và lần push ấy là việc của chủ kho.

### 2.2 — Đường TRẢ LẠI (g3), và vì sao nó phải nằm trong đặc tả chứ không trong một dòng ghi chú

**Thu hẹp KHÔNG tự đảo ngược.** Sau 10:30Z, nếu không ai làm gì thì #579 vẫn thiếu
`ops/lease_publish_test.py`, `A1`–`A6` vẫn không đạt, và packet dừng ở một PR tự khai CHƯA ĐỦ.
Đó là kết cục xấu nhất của Q5, nên nó được viết to ở đây.

| trường | giá trị |
|---|---|
| khi nào | sớm nhất `2026-09-21T10:30:00Z`, **và** chỉ sau khi đo lại `ai-dang-giu ops/lease_publish_test.py` (`rc` đọc TRỰC TIẾP) thấy không còn người giữ nào ngoài lease của chính #579 |
| ai làm | chủ kho cấp; phiên #579 xin; phiên #578 không dính vào |
| hình thức | **generation 3** của revision 2 này — KHÔNG phải một revision mới, vì mục tiêu và nghiệm thu không đổi |

`docs/PROTOCOL_DA_PHIEN.md` §3.2 đòi revision mới khi đổi write set. r2 tuân thủ bằng cách khai
**cả hai** hình dạng write set ngay trong đặc tả, nên bước g2 → g3 là thi hành đúng r2 chứ không
phải một lần đổi phạm vi không có căn cứ.

## 3. `ngoai_pham_vi`

| thứ CỐ Ý không làm | lý do |
|---|---|
| Sửa `_kiem_bia_mo` | Q2 giữ nguyên: đổi một cổng an toàn của hệ lease ⇒ packet RIÊNG theo §3.2. |
| Sửa `.github/workflows/ops-publish-lease.yml` | Q1 chốt vá ở cổng đọc; bước `đăng` đã có sẵn nhánh `rc=9` đúng. |
| Nới `_kiem_bia_mo` cho chạm XUYÊN PACKET | Khe `AG-T0-01B` đã lách BẢY lần; packet này không đụng và không đếm thêm lần nào. |
| Sửa hai tệp lease gen 1 của #566/#568 | Hiện vật ĐÃ CÔNG BỐ. Bản vá làm cổng thôi đỏ ở lượt SAU, không viết lại lịch sử. |
| Chạy CI tay / `workflow_dispatch` / lane `windows` | `manual_ci_budget: 0` đang hiệu lực. |
| Đăng lại hai lease gen 2 của #566/#568 | Đã đăng rồi (`rc=9` là đường đúng cho chúng sau bản vá). |

### 3.1 — Một LỜI KHAI CŨ mà packet này CỐ Ý để lại, và phải khai vì nó sẽ sai sau khi vá

`.github/workflows/ops-publish-lease.yml`, khối chú thích của bước `tìm lease vừa đổi`, mang đúng
câu mà `M5` sửa trong `t32`: *"chốt `posted_comment_id` lo phần không đăng trùng — đúng cho lease
ĐÃ đăng (rc=9, bỏ qua), sai cho lease chưa từng đăng"*.

Tệp ấy **cố ý ngoài write set** (Q1: không phải sửa một dòng YAML nào). Hệ quả đo được: sau khi
`M1` land, câu ấy **sai ở cả hai vế** chứ không chỉ một, và không ai sửa nó trong packet này.
Ghi ra đây để lần sau nó không bị đọc thành một chỗ mù — nó là một chỗ **đã biết và đã chọn**.

## 4. `muc_tieu`

`M1`–`M8` **giữ nguyên byte nghĩa** của r1 §4. Chép lại để r2 tự đủ:

| # | mục tiêu | đường dẫn |
|---|---|---|
| **M1** | `kiem_github` dò dấu "đã đăng" TRƯỚC khi gọi `kiem()`: có dấu ⇒ `Chan(RC_DA_DANG)` ngay. | `ops/lease_publish.py` |
| **M2** | Tiền kiểm miền fail-close: thiếu `lease_id`/`packet_issue`, hoặc `packet_issue` sai kiểu ⇒ `Chan(RC_NOI_DUNG)`, không ngoại lệ trần. | `ops/lease_publish.py` |
| **M3** | Không dấu ⇒ hành vi KHÔNG ĐỔI so `origin/master`: cùng thứ tự lỗi, cùng mã thoát. | `ops/lease_publish.py` |
| **M4** | Docstring `kiem_github` khai GIÁ PHẢI TRẢ: lease đã đăng thì các chốt của `kiem()` không chạy nữa trên đường này. | `ops/lease_publish.py` |
| **M5** | Sửa docstring `t32` — bỏ vế sai *"đúng cho lease ĐÃ đăng (rc=9)"*, ghi lại đúng phép đo. | `ops/lease_publish_test.py` |
| **M6** | Ca mới phủ nửa còn thiếu: hết hạn + ĐÃ có dấu ⇒ `rc=9`; hết hạn + KHÔNG dấu ⇒ `rc=8`. | `ops/lease_publish_test.py` |
| **M7** | Ca mới cho M2: ba ca âm, và khai đúng ca nào THẬT SỰ có răng. | `ops/lease_publish_test.py` |
| **M8** | Nếp vào `CLAUDE.md`: bia mộ hai chiều chỉ dùng cho lease CÒN SỐNG. | `CLAUDE.md` |

### 4.1 — `M9`, MỚI ở r2: đóng nhánh mà không ca nào chạm

| # | mục tiêu | đường dẫn |
|---|---|---|
| **M9** | Một ca phủ nhánh NUỐT của phép dò: `_kiem_comment_da_co` ném một lớp **ngoài họ `OSError`** ⇒ phép dò phải nhường lại cho chuỗi cũ phán, KHÔNG được tự kết luận "đã đăng" và KHÔNG được tự ném lỗi của mình thay cổng. | `ops/lease_publish_test.py` |

**`M9` sinh ra từ một ĐỘT BIẾN SỐNG SÓT, và đó là lý do nó tồn tại.** Lượt đo 21-09 dựng năm đột
biến cho `M1`–`M7`; bốn cái chết đúng ca của nó, cái thứ năm — nhánh nuốt ném `Chan(RC_DA_DANG)`
— **sống sót 10/10**. Không phải vì mã đúng: vì năm ca kia chỉ dựng hai hình dạng
(`_kiem_comment_da_co` thấy dấu, hoặc trả về êm), nên nhánh nuốt **chưa từng được chạy**.

Thêm một ca cho endpoint hỏng "tử tế" vẫn **không** đủ — `_doc_gh` bắt `OSError` rồi bọc mọi thứ
khác thành `Chan`, nên đột biến vẫn sống (đo: `11/11`). Chỉ một ngoại lệ lọt qua `_doc_gh` mới
phơi được nhánh ấy.

Đột biến sống sót ở đây là một khoảng **TRỐNG của bộ test**, không phải một chứng cứ về mã — và
đó chính là bài học `ĐỘT BIẾN SỐNG SÓT KHÔNG LUÔN NGHĨA LÀ TEST YẾU` đọc theo chiều còn lại.

## 5. `nghiem_thu`

`A1`–`A11` của r1 §5 **giữ nguyên**, trừ `A7` được siết theo số ca thật, cộng `A12` mới.

| # | tiêu chí | phép đo làm nó **ĐỎ** |
|---|---|---|
| **A7** (siết) | Suite `ops/lease_publish_test.py` **N/N hai số BẰNG NHAU**, `bỏ qua = 0`, và `N ≥ 172`. | `rc` đọc **trực tiếp**, không qua pipe. Nền 166 ca + 6 ca mới = 172; ít hơn nghĩa là một ca đã rụng mà không ai khai. |
| **A12** (mới, cho `M9`) | Đột biến cho nhánh nuốt ném `Chan(RC_DA_DANG)` ⇒ ca `M9` **ĐỎ**. Và đột biến bỏ điều kiện `if c.ma == RC_DA_DANG` (ném lại MỌI `Chan`) cũng ⇒ ca ấy **ĐỎ**. | Hai đột biến ấy **cùng lớp** (phép dò tự phán thay cổng), nên đừng khai chúng là hai chốt độc lập. Chúng chứng minh ca có răng, không chứng minh có hai cửa. |

**Không tiêu chí nào đóng bằng `rc=0`.** Mỗi dòng đòi bằng chứng dương: hai số bằng nhau, một mã
thoát cụ thể, hoặc một đột biến ĐỔI MÀU đúng ca đích.

## 6. `hinh_dang_ke_thua`

| hình dạng | số lần | nguồn |
|---|---|---|
| `LOI-KHAI-RONG-HON-PHEP-DO` | 4 → **5** | r1 đếm 4. **+1**: docstring `_tien_kiem_mien_dang` do chính phiên thi hành viết, khai *"thiếu trường sẽ thành `KeyError` TRẦN thoát ra khỏi cổng"* — đột biến gỡ hàm ấy ra **BÁC** câu đó: thiếu `lease_id` và thiếu `packet_issue` vẫn ra `rc=8`, vì phép dò vốn nuốt `KeyError`. Chỉ ca `packet_issue` SAI KIỂU mới đổi. Docstring đã viết lại theo đúng phép đo. |
| `DOT-BIEN-SONG-SOT-VI-NHANH-CHUA-AI-CHAM` | **1** | MỚI. Xem §4.1. Khác hẳn *"đột biến chưa từng được chạy"* (va chạm `.pyc`): ở đây đột biến CÓ chạy, mã CÓ đổi, mà không ca nào đi qua dòng ấy. |
| `VA-BANG-REGEX-RONG-HON-Y-DINH` | 1 | Chép từ #566. |
| `TIN-HIEU-DO-CHINH-MA-TEST-GIA-MAO` | 2 | Chép từ #566. |
| `VA-DUNG-CHO-DUOC-CHI-ROI-BO-SOT-DUONG-THU-BA` | 1 | #513 là gốc; ca mới: bản vá #195 đóng *"hết hạn + chưa đăng"* rồi bỏ sót *"hết hạn + đã đăng"*. |

**`LOI-KHAI-RONG-HON-PHEP-DO` chạm 5.** r1 §6 chốt: gặp lần thứ 5 thì DỪNG và hỏi có nên tiếp
cách làm này không. **ĐÃ DỪNG, ĐÃ HỎI, chủ kho trả lời 21-09: *"M5 cứ sửa docstring theo đúng
phép đo"*.** Nên cách làm giữ nguyên, và ràng buộc cũng giữ nguyên: mọi câu bản vá thêm vào phải
nêu phép đo đứng sau nó, hoặc nói thẳng KHÔNG ĐO ĐƯỢC.

Đáng ghi vì nó tự chứng minh ràng buộc ấy có răng: **lần thứ 5 bị bắt bởi chính một đột biến của
packet này**, không phải bởi một lượt review.

## 7. `chua_do_duoc`

1. **Số dòng thêm — NAY ĐÃ ĐO, không còn là ước.** Xem §8.
2. **`ops/lease_publish_test.py` còn người giữ.** Đo `05:0xZ` 21-09: `rc=11` · **NGƯỜI_GIỮ 2** —
   lease của chính #579 (`dang-lease-dau-truoc-kiem-sau-r1-g1-claude`) và
   `windows-fixture-posix-r1-g1-claude` (#578, hết `2026-09-21T10:30:00Z`).
   `wp570-bash-nen-r4-g4-claude` đã được phiên khác **thu hồi** bằng bia mộ hai chiều — câu
   *"wp570 vẫn giữ"* của r1 §7.2 nay **HẾT HIỆU LỰC**. Đo lại, đừng chép.
3. **Bẫy `ai-dang-giu` `rc=12` có HAI dạng, cả hai đều FAIL-CLOSE.** `NHÁNH_CỤC_BỘ_TỤT_SAU`
   (chữa: `rev-list --count` = 0 rồi `git branch -f`) và `KHÔNG_XÁC_ĐỊNH: cache thiếu nhánh máy
   chủ` (chữa: fetch lại — phiên khác vừa đẩy nhánh). Gặp cả hai trong ngày 20/21-09; dạng thứ
   hai r1 chưa khai.
4. **Bản vá có làm hai lượt đỏ kia thôi đỏ không** — **KHÔNG ĐO ĐƯỢC**: hai lượt ấy đã chạy xong
   trên head cũ và `manual_ci_budget: 0` cấm gọi lại. `A11` đo **cơ chế**; nó không thay được một
   lượt CI thật. Lời khai đúng sau khi vá là *"cơ chế đã đóng, chưa có lượt workflow nào chạy lại
   để xác nhận"*.
5. **`gate (windows-latest)`** — **CHỌN KHÔNG ĐO** theo `manual_ci_budget: 0`, không phải không
   đo được.
6. **`_kiem_bia_mo` vẫn đòi sửa tệp lease chết.** Q2 giữ nguyên. Nếp ở `M8` là thứ duy nhất canh
   chỗ đó, và **máy không canh nó**.
7. **Ca `bool` của `M2`** — `isinstance(True, int)` là `True` trong Python, nên `packet_issue: true`
   lọt phép kiểm kiểu ngây thơ. Tiền kiểm loại `bool` tường minh, nhưng **chưa có phép đo riêng
   cho ca ấy**; nó suy từ cùng cơ chế với ca chuỗi, và suy không phải đo.

## 8. Ngoại lệ `ADR-0044` — Q6

`ADR-0044` (Accepted 21-08-2026): packet `sensitive` **≤ 3 tệp và ≤ 300 dòng thêm**; vượt thì
*"dừng TRƯỚC review để revision thiết kế, **hoặc khai lý do trong spec**"*. Mục này là đường thứ hai.

**Phép đo, `05:0xZ` 21-09-2026, `git diff --numstat origin/master` trên cây đã hoàn chỉnh:**

| tệp | dòng thêm |
|---|---|
| `CLAUDE.md` | 27 |
| `ops/lease_publish.py` | 77 |
| `ops/lease_publish_test.py` | 229 |
| **tổng** | **333** (xoá 2) |

**3 tệp ⇒ vế TỆP ĐẠT. 333 > 300 ⇒ vế DÒNG KHÔNG ĐẠT, vượt 33.**

Phân rã 229 dòng của tệp test: **93** dòng mã, **105** dòng docstring/chú thích, **31** dòng trống.

**Lý do, và nó phải chịu được phản bác:** cắt 33 dòng là cắt vào phần docstring, vì 93 dòng mã
không cắt được mà không bỏ một ca. Mà docstring ở đây **không phải văn trang trí** — chúng mang
chính các phép đo làm cho từng ca có nghĩa: số `rc` của từng hình dạng, tên đột biến làm ca ĐỎ, và
ở `M9` là câu chuyện đột biến sống sót. Cắt chúng để vừa một con số là **tối ưu thước đo chống lại
mục đích của thước đo** — đúng lớp bệnh mà chính kho này đặt tên.

**Điều ngoại lệ này KHÔNG cho phép:**

- Không cho vượt vế **TỆP**. Ba đường là trần cứng; đường thứ tư vẫn làm `A8` ĐỎ.
- Không cho gọi cổng `ADR-0044` là **"ĐẠT"** ở bất kỳ đâu — thân PR, comment, hay báo cáo. Nó
  **VƯỢT TRẦN, CÓ NGOẠI LỆ ĐÃ DUYỆT**. Tiền lệ đã trả giá (`PLAT-X8`): con số trôi lần thứ tư khai
  sai rằng một thẩm quyền đã có.
- Không cho gia hạn sang packet sau. Ngoại lệ này chỉ cho **#579**, chỉ cho con số **333**; vượt
  thêm thì phải dừng và xin lại.

| trường | giá trị |
|---|---|
| `ai_nang` | `ducthangho` (OWNER) |
| `can_cu` | Chỉ thị trong phiên 21-09-2026, chọn đường *"Revision 2 — khai lý do"* khi được trình ba đường (revision 2 · cắt xuống dưới 300 · tách slice thứ hai) |
| `tran_cu` | 300 dòng thêm |
| `so_do_that` | **333** dòng thêm, đo `05:0xZ` 21-09-2026 |
| `vuot` | 33 |

## 9. Hoà chỗ lease lệch Q3 — Q7

Lease `dang-lease-dau-truoc-kiem-sau-r1-g1-claude` được cấp `19:48Z` 20-09 trong lúc
`ai-dang-giu ops/lease_publish_test.py` vẫn trả **NGƯỜI_GIỮ 2** — ngược vế sau của Q3. Lease tự
khai chỗ lệch ấy ở khoá `LECH_SO_VOI_SPEC` thay vì giấu.

**r2 hoà bằng cách sửa LUẬT, không bằng cách sửa lời khai.** Q3 của r1 giả định đúng một đường:
chờ tới khi sạch. Thực tế cho thấy đường ấy có thể **không bao giờ tới** — hai lease chờ nhau
(§2.1). Nên Q5 thay nó bằng một luật mô tả được cả thế kẹt:

> Đường bị giữ mà packet tự khai là **không dùng trong cửa sổ này** thì **gỡ khỏi write set** của
> generation hiện tại, kèm một đường TRẢ LẠI có mốc thời gian và người cấp. Không giữ một đường
> mình không dùng, và không chờ một điều kiện mà chính mình đang làm cho nó không xảy ra.

**KHÔNG khai rằng Q3 "đã được thoả mãn".** Nó không được thoả mãn. Lịch sử không sửa được: lúc cấp
g1, đường ấy vẫn trong write set và vẫn có người giữ. Thứ r2 làm là khiến **trạng thái hiện tại**
không còn lệch, và nói rõ vì sao trạng thái quá khứ từng lệch.

## 10. Thứ phải có trước khi coi packet là xong

1. `g3` đã cấp và đã đăng, trả `ops/lease_publish_test.py` lại write set (§2.2).
2. `A1`–`A12` đều có phép đo dương, `rc` đọc TRỰC TIẾP.
3. Thân PR khai `ADR-0044` là **VƯỢT TRẦN + CÓ NGOẠI LỆ**, dẫn §8 — không khai "ĐẠT".
4. `human_audited`: một lượt thẩm định của NGƯỜI trên head thật. **Packet này KHÔNG LAND ĐƯỢC
   BẰNG MÁY**, và chữ ký không thay được phép đo.
