# ĐẶC TẢ — `DANG-LEASE-DAU-TRUOC-KIEM-SAU` — **revision 1, ĐÓNG BĂNG**

| trường | giá trị |
|---|---|
| `packet_id` | `DANG-LEASE-DAU-TRUOC-KIEM-SAU` |
| `revision` | 1 |
| `packet_issue` | **CHƯA ĐĂNG** — đặc tả không cấp việc (soan-spec §5). Issue + lease còn hiệu lực mới giao được. |
| `nguon_cap_viec` | Chỉ thị chủ kho 20-09-2026 ~15:5xZ, gõ văn xuôi: *"Mở packet riêng vá bước đăng lease đi"*. Bốn quyết định biên giới chốt cùng phiên (§0). Hiện vật gốc: hai lượt `ops — đăng lease bằng git` ĐỎ — [`35519177197`](https://github.com/ducthangho/tra-luat/actions/runs/35519177197) (#568) và [`35519243379`](https://github.com/ducthangho/tra-luat/actions/runs/35519243379) (#566) — đã mổ xẻ tại `#568` [`issuecomment-5750735364`](https://github.com/ducthangho/tra-luat/issues/568#issuecomment-5750735364). |
| `review_class` | **`sensitive`** — chạm `ops/lease_publish.py`, tức **cổng đọc lease** (protocol §8). Vế đo được của `ADR-0044:5`: **3 tệp = đúng trần 3**; dòng thêm là **ƯỚC**, chưa đo (xem `chua_do_duoc` #1). |
| `assurance_target` | **`human_audited`** — quyết định chủ kho. `cross_approved` **KHÔNG ĐẠT ĐƯỢC**, không phải *"chưa đo"*: codex đăng *"You have reached your Codex usage limits for code reviews"* trên PR #577 lúc 10:52Z 20-09; agy hết quota; claude là executor. |

**GIỚI HẠN LỜI KHAI:** mọi khẳng định chỉ chứng minh tới đúng phép đo ghi kèm.
**Ba trạng thái:** có · không · **KHÔNG ĐO ĐƯỢC** — trạng thái thứ ba làm cổng ĐỎ.

---

## 0. Bốn quyết định biên giới — vòng 1 đã đóng

| câu | quyết định |
|---|---|
| **Q1** vá ở đâu | `kiem_github`: **dò dấu "đã đăng" TRƯỚC, gọi `kiem()` SAU** |
| **Q2** phạm vi | **vá cổng + ghi nếp vào `CLAUDE.md`**; `_kiem_bia_mo` giữ nguyên |
| **Q3** đường qua chặn write set | **hỏi #578 và #570 nhả sớm**; không cấp lease trước khi đo `NGƯỜI_GIỮ 0` |
| **Q4** bảo chứng | **`human_audited`** như #566/#568 |

## 1. Bệnh — định vị đến từng dòng, `origin/master` `700ca8c7`, đo **16:08Z 20-09-2026**

```
ops/lease_publish.py:893   def kiem_github(lease, tep=None, goc=None):
ops/lease_publish.py:894       lease, neo = kiem(lease, tep, goc)      ← GỌI TRƯỚC
ops/lease_publish.py:895       repo = _repo_github()
ops/lease_publish.py:896       _kiem_loai_so_hieu(repo, lease["packet_issue"])
ops/lease_publish.py:897       _kiem_comment_da_co(repo, lease)        ← CHỐT rc=9 NẰM SAU

ops/lease_publish.py:885       han = _doc_han(lease["lease_expires_at_utc"])
ops/lease_publish.py:886       if han <= datetime.now(timezone.utc):
ops/lease_publish.py:887           raise Chan(RC_NOI_DUNG, "lease đã hết hạn lúc … ")   ← rc=8
ops/lease_publish.py:686       raise Chan(RC_DA_DANG, "lease … đã có comment … — bỏ qua")  ← rc=9
```

**Hệ quả:** một lease **ĐÃ ĐĂNG rồi mới hết hạn** không bao giờ tới được đường `rc=9`; nó chết ở
`rc=8` trước đó. Bước `đăng` của `.github/workflows/ops-publish-lease.yml` **có sẵn** nhánh
`if [ "$rc" = "9" ]; then echo "đã đăng trước đó — bỏ qua"` — nhánh ấy đúng, nó chỉ **không bao
giờ được gọi** cho hình dạng này.

### Cửa vào: bia mộ hai chiều buộc phải sửa tệp lease CHẾT

`_kiem_bia_mo` (`ops/lease_publish.py:595`) đòi lease cũ mang dòng `da_bi_thay_the: <lease mới>`.
Bước `tìm lease vừa đổi` chọn **tệp lease đổi trong `before..sha`**. Nên viết bia mộ vào một lease
đã hết hạn = đưa một tệp chết vào tập quét = `rc=8` = cả lượt `exit 1`.

Đo được 20-09-2026: cả hai lượt đỏ đều **sau khi** lease mới đã đăng xong.

| lượt | lease mới ĐÃ đăng | comment | tệp làm đỏ |
|---|---|---|---|
| `35519177197` (#568) | `chan-doan-tin-dung-gia-r1-g2-claude` | [`5750701018`](https://github.com/ducthangho/tra-luat/issues/568#issuecomment-5750701018) | `…-g1-claude.yaml`, hết hạn `13:35Z` |
| `35519243379` (#566) | `human-audited-khai-ai-dang-r1-g2-claude` | [`5750710091`](https://github.com/ducthangho/tra-luat/issues/566#issuecomment-5750710091) | `…-g1-claude.yaml`, hết hạn `14:30Z` |

Hai comment đã được **đọc ngược về qua API** để đo thứ ĐÃ ĐẾN, không dừng ở lời khai của log.

### Chỗ đắt nhất: chính tài liệu của kho khai NGƯỢC

`ops/lease_publish_test.py:1312` `t32_buoc_chon_lease_KHONG_duoc_quet_CA_THU_MUC`, nguyên văn
docstring:

> Chú thích cũ khai "chốt `posted_comment_id` lo phần không đăng trùng": **đúng cho lease ĐÃ đăng
> (rc=9)**, sai cho lease CHƯA TỪNG đăng.

**Vế in đậm SAI**, và hôm nay là lần đầu nó bị đo. Fixture của `t32` (`:1245`) khai thẳng
*"Chính hình dạng đã giết cổng ngày 20-08: hết hạn, KHÔNG `posted_comment_id`"* — tức bộ test phủ
đúng **một** nửa, và nửa bù (*hết hạn, ĐÃ có dấu*) chưa có ai viết.

Đây là **bản vá #195 ĐÚNG mà HẸP**: nó thu phạm vi quét từ cả `ops/leases/` xuống tệp đã đổi, và
bỏ sót đường vào thứ hai. Cùng hình dạng `VA-DUNG-CHO-DUOC-CHI-ROI-BO-SOT-DUONG-THU-BA` của #513.

## 2. `write_set`

```
ops/lease_publish.py
ops/lease_publish_test.py
CLAUDE.md
```

Đúng **ba** đường = **đúng trần** `ADR-0044:5` cho class `sensitive`. **Không xin ngoại lệ tệp.**

| đường | dòng (master) | `ai-dang-giu` 16:08Z |
|---|---|---|
| `ops/lease_publish.py` | 2042 | `rc=0` · **NGƯỜI_GIỮ 0** |
| `ops/lease_publish_test.py` | 7043 · **166** ca | `rc=11` · **NGƯỜI_GIỮ 2** (xem dưới) |
| `CLAUDE.md` | 926 | `rc=0` · **NGƯỜI_GIỮ 0** |

Tập tên ref hai nguồn so bằng `comm -23`/`comm -13`: **481/481**, cả hai chiều rỗng.

**`.github/workflows/ops-publish-lease.yml` CỐ Ý ngoài write set.** Q1 chốt vá ở `kiem_github`;
bước `đăng` đã có sẵn nhánh `rc=9` đúng, nên không phải sửa một dòng YAML nào.

## 3. `ngoai_pham_vi`

| thứ CỐ Ý không làm | lý do |
|---|---|
| Sửa `_kiem_bia_mo` để thôi đòi bia mộ ở lease đã hết hạn | **Q2**: đổi một cổng an toàn của hệ lease ⇒ §3.2 đòi packet RIÊNG. |
| Sửa `.github/workflows/ops-publish-lease.yml` | Q1 chốt vá ở cổng đọc; bước `đăng` không cần đổi. |
| Nới `_kiem_bia_mo` cho chạm XUYÊN PACKET | Đó là khe `AG-T0-01B` đã lách **BẢY** lần; packet này không đụng tới và **không** đếm thêm lần nào. |
| Sửa hai tệp lease gen 1 của #566/#568 | Hiện vật ĐÃ CÔNG BỐ. Bản vá làm cổng thôi đỏ ở lượt SAU, không viết lại lịch sử. |
| Chạy CI tay / `workflow_dispatch` / lane `windows` | `manual_ci_budget: 0` đang hiệu lực. |
| Đăng lại hai lease gen 2 | Đã đăng rồi (`rc=9` là đường đúng cho chúng sau bản vá). |

## 4. `muc_tieu` — mỗi dòng chiếu vào MỘT đường của `write_set` (L2)

| # | mục tiêu | đường dẫn |
|---|---|---|
| **M1** | `kiem_github` dò dấu **"đã đăng"** TRƯỚC khi gọi `kiem()`: có dấu ⇒ `Chan(RC_DA_DANG)` ngay, không chạm `kiem()`. | `ops/lease_publish.py` |
| **M2** | Phần tiền kiểm của M1 **fail-close**: lease thiếu `packet_issue` hoặc `lease_id`, hoặc `packet_issue` sai kiểu, ⇒ `Chan` sạch (`RC_NOI_DUNG`), **không** `KeyError`/`TypeError` trần. Hôm nay `kiem()` chạy trước nên nó che các ca ấy; đảo thứ tự là gỡ tấm che. | `ops/lease_publish.py` |
| **M3** | Không dấu ⇒ hành vi **KHÔNG ĐỔI** so `origin/master`: vẫn `kiem()` → `_repo_github()` → `_kiem_loai_so_hieu` → `_kiem_comment_da_co`, cùng thứ tự lỗi, cùng mã thoát. | `ops/lease_publish.py` |
| **M4** | Khai thẳng trong docstring `kiem_github` **giá phải trả**: lease đã đăng thì các chốt của `kiem()` (tự cấp, neo prompt, băm) **KHÔNG** chạy nữa trên đường này. | `ops/lease_publish.py` |
| **M5** | Sửa docstring `t32` — bỏ vế sai *"đúng cho lease ĐÃ đăng (rc=9)"* và ghi lại đúng phép đo 20-09. | `ops/lease_publish_test.py` |
| **M6** | Ca mới phủ nửa còn thiếu: **hết hạn + ĐÃ có dấu** ⇒ `rc=9`; và **hết hạn + KHÔNG dấu** ⇒ `rc=8` (giữ nguyên, chống hồi quy #195). | `ops/lease_publish_test.py` |
| **M7** | Ca mới cho M2: ba ca âm (thiếu `lease_id` · thiếu `packet_issue` · `packet_issue` sai kiểu). | `ops/lease_publish_test.py` |
| **M8** | Nếp vào `CLAUDE.md`: **bia mộ hai chiều chỉ dùng cho lease CÒN SỐNG.** Lease đã hết hạn thì write-set exclusion đã nhả — ghi kế vị bằng bia mộ chỉ mua một lượt đỏ. Kèm ca 20-09 làm bằng chứng, và nêu rằng **máy KHÔNG canh** nếp này. | `CLAUDE.md` |

## 5. `nghiem_thu` — mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3)

| # | tiêu chí | phép đo làm nó **ĐỎ** |
|---|---|---|
| **A1** | Lease **hết hạn + ĐÃ có dấu** ⇒ `kiem_github` ném `Chan` mã **9**. | Đột biến đưa `_kiem_comment_da_co` về lại SAU `kiem()` ⇒ ca ĐỎ (nhận 8 thay vì 9). Ca phải so **mã thoát**, không so chuỗi thông điệp. |
| **A2** | Lease **hết hạn + KHÔNG dấu** ⇒ vẫn mã **8**. | Đột biến trả 9 vô điều kiện ⇒ ca ĐỎ. **Cặp A1/A2 phải ĐỎ NGƯỢC CHIỀU nhau** — chỉ một trong hai đỏ nghĩa là bộ tương đương, đang đo một thứ. Đây là chốt chống hồi quy #195. |
| **A3** | Lease **còn hạn + ĐÃ có dấu** ⇒ mã **9** (hành vi cũ, không đổi). | Đột biến bỏ hẳn tiền kiểm ⇒ ca ĐỎ. |
| **A4** | Lease **còn hạn + KHÔNG dấu** ⇒ `rc=0`, và **mọi chốt của `kiem()` vẫn chạy**. | Ba ca tiêm: `granted_by` là tên provider ⇒ **4**; neo prompt sai băm ⇒ **6**; thiếu trường bắt buộc ⇒ **8**. Đột biến cho tiền kiểm nuốt cả bốn ca ⇒ cả ba ĐỎ. |
| **A5** | **M2 fail-close**: thiếu `lease_id` · thiếu `packet_issue` · `packet_issue` sai kiểu ⇒ `Chan(RC_NOI_DUNG)`. | Đột biến bỏ tiền kiểm miền ⇒ ca ném `KeyError`/`TypeError` trần ⇒ ĐỎ. Phân hạng bằng **LỚP ngoại lệ**, không bằng chuỗi — bài học tín dụng giả #355/#359: một `except` đổi kiểu giả được chuỗi. |
| **A6** | `t32` vẫn ĐẠT nguyên vẹn sau khi sửa docstring. | Chạy `t32`; đột biến quét cả `ops/leases/` ⇒ `t32` ĐỎ. |
| **A7** | Suite `ops/lease_publish_test.py` **N/N hai số BẰNG NHAU**, `N ≥ 166 + (số ca mới)`, `bỏ qua = 0`. | `rc` đọc **trực tiếp**, không qua pipe (nợ `RC-QUA-PIPE-KHONG-CO-CHOT`). |
| **A8** | `numstat` chạm **đúng ba** đường của `write_set`, không đường thứ tư. | Đột biến thêm một đường ⇒ tiêu chí ĐỎ. Chốt write-set exclusion §5. |
| **A9** | `doctrine-scan` `rc=0` sau khi thêm mục vào `CLAUDE.md`. | `CLAUDE.md` là **nguồn** doctrine, không phải adapter — nhưng phải chạy để chứng minh, không được suy. |
| **A10** | `adr-song` · `doc-claims-check --strict` · `git diff --check` `rc=0`; `actionlint` **DELTA so `origin/master` = 0**. | Nền 23-08-2026 từng `rc=1` (1 finding `SC1003:info`) khi **có** `shellcheck`, `rc=0` khi **vắng** ⇒ tiêu chí là DELTA, không phải `rc=0` tuyệt đối. Thiếu `actionlint` **hoặc** `shellcheck` ⇒ in **KHÔNG ĐO ĐƯỢC** và ĐỎ. |
| **A11** | **Phản chứng hai chiều trên hiện vật thật:** dựng lại đúng hình dạng của lượt `35519177197` — một tệp lease đã đăng + đã hết hạn nằm trong tập "lease vừa đổi" — và đo `kiem_github` trả **9** thay vì **8**. | Chạy trên `origin/master` sạch ⇒ phải ra **8** (tái hiện bệnh); chạy trên ứng viên ⇒ phải ra **9**. Thiếu vế nền thì không chứng minh được gì — đó là đối chứng âm. |

**Không tiêu chí nào đóng bằng `rc=0`.** Mỗi dòng đòi bằng chứng dương: hai số bằng nhau, một mã
thoát cụ thể, hoặc một đột biến ĐỔI MÀU đúng ca đích — phân hạng bằng **lớp ngoại lệ riêng + tên
ca**, không bằng chuỗi thông điệp.

## 6. `hinh_dang_ke_thua` (L4) — chép từ #566/#568, cộng ca mới

| hình dạng | số lần | nguồn |
|---|---|---|
| `LOI-KHAI-RONG-HON-PHEP-DO` | 3 → **4** | Chép 3 từ #551 r4 / #566 / #568. **+1**: docstring `t32` khai *"đúng cho lease ĐÃ đăng (rc=9)"* — một lời khai rộng hơn phép đo đứng sau nó, và hôm nay bị đo là sai. |
| `VA-BANG-REGEX-RONG-HON-Y-DINH` | 1 | Chép từ #566. |
| `TIN-HIEU-DO-CHINH-MA-TEST-GIA-MAO` | 2 | Chép từ #566. |
| `VA-DUNG-CHO-DUOC-CHI-ROI-BO-SOT-DUONG-THU-BA` | **1** | #513 lượt 10→13 là gốc; ca mới: bản vá #195 đóng *"hết hạn + chưa đăng"* rồi bỏ sót *"hết hạn + đã đăng"*. |

`LOI-KHAI-RONG-HON-PHEP-DO` **chạm 4 — đã quá ngưỡng ba lần.** Hệ quả bắt buộc cho packet này:
mọi câu trong docstring và trong `CLAUDE.md` mà bản vá thêm vào **phải nêu phép đo đứng sau nó**,
hoặc nói thẳng **KHÔNG ĐO ĐƯỢC**. Gặp lần thứ **5** ⇒ DỪNG và hỏi có nên tiếp cách làm này không.

## 7. `chua_do_duoc`

1. **Số dòng thêm.** Ước **+110…+190** (M1–M4 ~25 trong `lease_publish.py`; M5–M7 ~90 trong test;
   M8 ~20 trong `CLAUDE.md`). Trần `sensitive` `ADR-0044:5` là **300**. **Chưa đo** vì chưa có mã.
   Chốt: `numstat` thật vượt **300** ⇒ executor **DỪNG** và xin một dòng quyết định bền của chủ
   kho — **không** tự đi tiếp, và **không** viết vào thân PR rằng cổng `ADR-0044` "ĐẠT". Tiền lệ
   đã trả giá (`PLAT-X8`): con số trôi lần thứ tư khai sai rằng **một thẩm quyền đã có**.
2. **`ops/lease_publish_test.py` đang bị GIỮ.** Đo 16:08Z: `rc=11` · **NGƯỜI_GIỮ 2** —
   `windows-fixture-posix-r1-g1-claude` (#578, hết `2026-09-21T10:30:00Z`) và
   `wp570-bash-nen-r4-g4-claude` (#570). **Chồng lấn ấy ĐÃ ĐƯỢC KHAI**: lease #578 mang khối
   `CHONG_LAN_DA_BIET` nêu đích danh lease #570 — **không** phải một khe bị lọt, và đặc tả này
   **không** ghi nó thành vi phạm.
   Đã xin nhả sớm: [#578 `5750948356`](https://github.com/ducthangho/tra-luat/issues/578#issuecomment-5750948356) ·
   [#571 `5750949384`](https://github.com/ducthangho/tra-luat/pull/571#issuecomment-5750949384).
   **Không cấp lease cho packet này trước khi `ai-dang-giu` trả `NGƯỜI_GIỮ 0`** — đo lại, đừng
   suy từ giờ hết hạn.
   Kèm một phép đo về ĐỘ TRÔI, đúng thứ L5 cảnh báo: lease giữ đường ấy đi
   `r2-g2` → `r3-g3` → `r4-g4` trong khoảng **90 phút** của chiều 20-09. Chép lại tên generation
   từ đặc tả này mà không đo lại là chép một con số đã chết.
3. **Bẫy `ai-dang-giu` `rc=12`.** Lượt gọi đầu của phiên 20-09 trả `rc=12`
   `NHÁNH_CỤC_BỘ_TỤT_SAU` vì hai nhánh **cục bộ** tụt 18 commit. Đó là **fail-close**, KHÔNG phải
   *"không có người giữ"* — đọc nhầm là cấp lease đè lên đường đang bị giữ. Chữa: kiểm
   `rev-list --count origin/master..<nhánh>` **= 0** rồi mới `git branch -f`.
4. **Bản vá có làm hai lượt đỏ kia thôi đỏ không** — **KHÔNG ĐO ĐƯỢC** trực tiếp: hai lượt ấy đã
   chạy xong trên head cũ và `manual_ci_budget: 0` cấm gọi lại. `A11` đo **cơ chế** bằng phản
   chứng hai chiều tại chỗ; nó **không** thay được một lượt CI thật. Lời khai đúng sau khi vá là
   *"cơ chế đã đóng, chưa có lượt workflow nào chạy lại để xác nhận"*.
5. **`gate (windows-latest)`** — `manual_ci_budget: 0`. Đây là **CHỌN KHÔNG ĐO**, không phải
   không đo được.
6. **`_kiem_bia_mo` vẫn đòi sửa tệp lease chết.** Q2 chốt không đụng. Nên sau packet này, viết bia
   mộ vào một lease đã hết hạn **vẫn** là một việc nên tránh — chỉ khác là nó không còn làm cả
   lượt `exit 1`. Nếp ở M8 là thứ duy nhất canh chỗ đó, và **máy không canh nó**.
