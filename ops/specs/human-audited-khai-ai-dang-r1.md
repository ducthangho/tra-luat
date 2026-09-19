# ĐẶC TẢ PACKET — `HUMAN-AUDITED-KHAI-AI-DANG` revision 1

| | |
|---|---|
| `packet_id` | `HUMAN-AUDITED-KHAI-AI-DANG` |
| `packet_issue` | **#566** |
| `revision` / `generation` | **1** / 1 |
| `review_class` | **`sensitive`** — xem `Đ1` |
| `base_sha` | **`dc85dd0a34188238aa6537ce843ff3688e488fd3`** (`origin/master`, đo `10:5xZ 19-09-2026`) |
| `executor` | **chưa gán** — xem `chua_do_duoc` `C1` |
| `assurance_target` | **chưa chốt** — xem `chua_do_duoc` `C1` |

## `nguon_cap_viec`

Chỉ thị chủ kho, phiên điều phối `19-09-2026`, **nguyên văn**:

> Land xong thì mở nợ r330 luôn

(mở #565), rồi:

> Dựng PR bookkeeping đi. Cấp lease và xử lý #565, #566

Cộng **hai quyết định hỏi–đáp** cùng phiên, ghi vì chúng định đúng phạm vi packet:

1. **Siết tới đâu** → *"Bắt buộc `dang_boi` + khai ADR"* — tức **không** chọn phương án hạ mức
   khi `phien_agent_dang_ho`, vì phương án ấy hồi tố lên một packet đã land.
2. **Khe mỏ neo v2** → *"Đưa vào #566"* — cùng gốc, cùng tập đường.

Nợ gốc: Issue **#566**. Nợ họ hàng đã có tên: **#338** (tách danh tính).

## VÌ SAO — ba căn cứ ĐO ĐƯỢC, không phải lo xa

### `Đ1` — `author_association` KHÔNG phân biệt được người với máy

Đo `19-09-2026 04:11Z`: phiên agent đăng [comment `5739262446`](https://github.com/ducthangho/tra-luat/pull/557#issuecomment-5739262446)
trên PR #557, rồi **đọc ngược về qua API**. Phản hồi:

```
"user": {"login": "ducthangho"},  "author_association": "OWNER"
```

**Y hệt** một comment chủ kho tự gõ. Nguyên nhân đã được kho ghi từ `2026-08-26` và in ra trong
chính `packet_loop.py guard`: *"phiên chạy bằng credential của chủ kho (`get_me` → ducthangho)"*.

Hệ quả: biên nhận `plat-m4-human-audit-ducthangho-verdict.receipt.yaml` khai
`tac_gia: … không phải bot, không phải phiên agent` — một câu **không dữ liệu nào trong biên
nhận chứng minh được**. Đây là *lời khai rộng hơn phép đo*, nằm trong chính hiện vật dựng ra
để làm bằng chứng.

`review_class` là **`sensitive`** vì packet sửa **chính cổng đọc luật assurance**
(`ops/bien_nhan_v2.py`) — cùng căn cứ `Đ4` của `ops/specs/assurance-neo-vao-ho-model-r4.md`.

### `Đ2` — cổng KHÔNG ĐỌC `dang_boi`, nên lời khai quan trọng nhất không có chốt nào canh

Đo `19-09-2026 10:4xZ`, và đây là **phản chứng chạy được**, không phải suy luận:

Biên nhận `human_audited` mới dựng cho #551 bị một regex làm **thụt nhầm bốn khoá** — gồm
`dang_boi` — vào trong `model_reviewer_identity`. `yaml.safe_load` trả `dang_boi = None` ở
top-level trong khi tệp **có** dòng ấy.

**Cổng `bien_nhan_v2` vẫn XANH, cả trước lẫn sau khi sửa: `132 ĐẠT v2 / tổng 185`, y hệt.**

⇒ Một biên nhận `human_audited` có thể khai `dang_boi` **sai chỗ**, hoặc **không khai**, mà
không cổng nào kêu. Đó chính là lớp *"cổng vắng mặt trông giống cổng xanh"*.

### `Đ3` — lược đồ v2 không có mỏ neo ĐO ĐƯỢC cho audit của người

`ANCHOR_LOAI_CHO_PHEP = {canonical_ancestry, protected_evidence_ref, check_object}`.
Nhưng `ops/bien_nhan_v2.py` (khoảng dòng 848) đưa `protected_evidence_ref` và `check_object`
vào **trạng thái thứ ba** — *"cổng CHƯA có đường đo cho loại mỏ neo này"* — và trạng thái thứ ba
làm cổng **ĐỎ**.

Hệ quả đo được khi dựng biên nhận #551: `protected_evidence_ref` là **đúng** loại cho một audit
neo vào comment GitHub, nhưng dùng nó thì cổng đỏ. Nên biên nhận phải neo `canonical_ancestry`
vào **bản chiếu** và tách `nguon_co_tham_quyen_url` ra trường riêng — tức **thứ được neo yếu hơn
thứ có thẩm quyền**, và điều đó chỉ được cứu bằng một câu chữ trong `gioi_han`.

## Nền đo tại lúc soạn — `10:5xZ 19-09-2026`, trên `dc85dd0a3418`

| phép đo | kết quả |
|---|---|
| tổng biên nhận | **185** (đơn vị: tệp `*.receipt.yaml` đọc được) |
| khai `human_audited` | **3** — `plat-m4` (schema v1), `slice-b-c` (v1), `assurance-ho-model-audit-nguoi` (v2) |
| đã có trường `dang_boi` | **0/185** tại thời điểm mở nợ; **1** sau khi PR #567 land |
| ca test trong `bien_nhan_v2_test.py` | **56** hàm `c*_` |
| đột biến trong `bien_nhan_v2_test.py` | **76** |

**Mọi con số trên là NỀN, không phải tiêu chí** (`L5`). `A1` và `A2` so **DELTA** với nền **đo
lại tại thời điểm cấp lease**. Nhắc riêng: nền sẽ trôi khi PR #567 land — `tổng` lên **185+**,
và số biên nhận có `dang_boi` lên **1**. Ghim con số vào tiêu chí là tái tạo đúng lỗi mà
`ADR-0044`/`L5` đã trả giá.

## `write_set` — BỐN đường

```
ops/bien_nhan_v2.py
ops/bien_nhan_v2_test.py
docs/adr/0051-human-audited-khai-ai-dang-va-gioi-han-cua-no.md   (MỚI)
docs/PROTOCOL_DA_PHIEN.md                                        (đúng MỘT hàng §20)
```

### `XIN_NGOAI_LE_ADR_0044` — phải xin TRƯỚC, không đụng rồi mới kêu

`ADR-0044:5` đặt trần class `sensitive` ở **≤ 3 tệp và ≤ 300 dòng thêm**. Packet này cần **4**
tệp. Xin nới **số TỆP 3 → 4**, giữ nguyên trần dòng **300**.

Căn cứ: ba đường đầu là **một** thay đổi không tách được — thêm một chốt vào cổng thì phải có ca
test và đột biến cho nó (`M14` của #551 cấm gộp chốt để lách), và một luật mới phải có ADR thì
`adr-song` mới xanh. Đường thứ tư là **đúng một hàng** §20 cho ADR mới, và không thêm nó thì
`adr-song` **ĐỎ** (`rc=9`) — tức nó là hệ quả bắt buộc của đường thứ ba, không phải mở rộng phạm vi.

**Chưa có ngoại lệ ⇒ packet DỪNG ở 3 tệp**, và khi ấy phải bỏ ADR hoặc bỏ §20 — cả hai đều làm
cổng đỏ. Nên đây là điều kiện dừng thật, không phải thủ tục.

### `RUI_RO_TRAN_DONG`

Ước lượng: chốt `dang_boi` trong `_thieu` (~15) · đường đo `protected_evidence_ref` (~35) ·
hằng + chú thích (~25) · ca test (~60) · đột biến (~15) · ADR-0051 (~45) · §20 (1).
Tổng **~196**, dưới trần 300. Vượt 300 ⇒ **DỪNG và xin**, không gộp chốt để lách.

## `ngoai_pham_vi` — cố ý KHÔNG làm

| thứ | vì sao |
|---|---|
| Hạ mức assurance khi `dang_boi: phien_agent_dang_ho` | Chủ kho **đã chọn không** (quyết định 1). Nó hồi tố lên #551 đã land |
| Sửa `plat-m4-…receipt.yaml` để bỏ câu `không phải phiên agent` | Hiện vật **ĐÃ GIAO**; đính chính đi bằng verdict MỚI có back-link, không sửa đè |
| Tách danh tính agent khỏi credential chủ kho | Nợ **#338**. Đó là hạ tầng, không phải một chốt trong cổng |
| Đảo `ASSURANCE_CAM_THEO_PROVIDER` sang CHO PHÉP | nợ `DANH-SACH-CAM-THEO-PROVIDER-CHUA-DAO` |
| Nối `bien_nhan_v2` vào CI làm cổng chặn | nợ `CONG-BIEN-NHAN-KHONG-CHAY-TRONG-CI` |
| Vá `r330` | **#565**, khác packet |

## `muc_tieu`

| # | mục tiêu | đóng | chiếu vào |
|---|---|---|---|
| **M1** | Biên nhận khai `human_audited` **PHẢI** có `dang_boi` ở **top-level**, giá trị trong danh sách CHO PHÉP `{chu_kho_tu_dang, phien_agent_dang_ho}`. Thiếu, rỗng, sai giá trị, hoặc **đặt sai chỗ** (chỉ có trong một ánh xạ con) ⇒ cổng **TỪ CHỐI** | `Đ2` | `ops/bien_nhan_v2.py` |
| **M2** | `dang_boi: phien_agent_dang_ho` **PHẢI** kèm `dang_boi_chi_thi_nguyen_van` khác rỗng — một lời khai "agent đăng hộ" mà không trích được chỉ thị thì không kiểm được. Thiếu ⇒ **TỪ CHỐI** | `Đ1` | `ops/bien_nhan_v2.py` |
| **M3** | Cấp **đường đo** cho `anchor.loai: protected_evidence_ref`: neo một comment GitHub thì cổng đọc `posted_comment_id` + `nguon_co_tham_quyen_url`, đòi chúng **khớp nhau** và URL đúng dạng comment. Đo được ⇒ **thoát** trạng thái thứ ba | `Đ3` | `ops/bien_nhan_v2.py` |
| **M4** | `ADR-0051` khai **THẲNG** `human_audited` đạt được gì và **KHÔNG** đạt được gì: (a) nó **không** chứng minh được ai gõ, vì `author_association` trả `OWNER` cho cả hai; (b) `dang_boi` đóng được *"im lặng"*, **không** đóng được *"cố tình"* khi credential dùng chung; (c) mỗi mục kèm **ca đo chạy được** | `Đ1` | `docs/adr/0051-…md` |
| **M5** | Đúng **một** hàng §20 cho `ADR-0051`, cột *"cổng nào ĐỌC luật ấy"* ghi `ops/bien_nhan_v2.py` | — | `docs/PROTOCOL_DA_PHIEN.md` |
| **M6** | Mỗi chốt của `M1`–`M3` có **ca test RIÊNG** và **đột biến RIÊNG**; gỡ từng cái làm **đúng một** ca ĐỎ, phân hạng `giet_that`. Hai chốt không phân biệt được bằng đầu vào là **bộ tương đương** ⇒ hỏng | tất cả | `ops/bien_nhan_v2_test.py` |

## `nghiem_thu` — mỗi tiêu chí nêu phép đo làm nó ĐỎ

| # | tiêu chí | ĐỎ khi |
|---|---|---|
| **A1** | `ops/bien_nhan_v2.py` trên **NỀN** (đo lại tại lease) **và** trên ỨNG VIÊN: `0 vi phạm`, `0 KHÔNG ĐO ĐƯỢC`, `TỔNG: ĐẠT` ở cả hai; số `ĐẠT v2`/`tổng` **KHÔNG ĐỔI** giữa hai vế | luật mới từ chối một biên nhận cũ ⇒ hai vế lệch. **Chú ý:** hai biên nhận `human_audited` v1 được miễn trừ legacy nên **không** bị chạm; nếu chúng ĐỎ thì chốt đã bỏ qua danh sách miễn trừ |
| **A2** | `bien_nhan_v2_test.py`: `N/N ca` với **hai số bằng nhau**, `M/M đột biến CÓ RĂNG`, `TỔNG: ĐẠT`; và **mỗi** đột biến của `M6` khai `giet_that` | một đột biến `tin_dung_gia` ⇒ tín dụng giả; hai đột biến giết cùng một ca ⇒ bộ tương đương |
| **A3** *(M1)* | Bốn ca: (a) `human_audited` + `dang_boi: chu_kho_tu_dang` ⇒ **QUA** (**đối chứng biết trước đáp án**); (b) **thiếu** `dang_boi` ⇒ **CHẶN**; (c) `dang_boi` **rỗng** ⇒ **CHẶN**; (d) `dang_boi` chỉ nằm **trong** `model_reviewer_identity`, không ở top-level ⇒ **CHẶN** | (b)/(c)/(d) QUA ⇒ chốt không có răng. **(a) CHẶN ⇒ rig hỏng, đừng tin ba ca kia** |
| **A4** *(M1)* | Một giá trị **BỊA ĐẶT** (`dang_boi: ai_do_dang`) ⇒ **CHẶN** | QUA ⇒ đang là danh sách CẤM chứ không phải CHO PHÉP — đúng lỗi `v1.36.68` |
| **A5** *(M2)* | `phien_agent_dang_ho` **không** kèm `dang_boi_chi_thi_nguyen_van` ⇒ **CHẶN**; có kèm ⇒ **QUA** (đối chứng) | ca thiếu QUA |
| **A6** *(M3)* | `anchor.loai: protected_evidence_ref` + `posted_comment_id` khớp `nguon_co_tham_quyen_url` ⇒ **QUA**, **không** rơi vào `KHÔNG ĐO ĐƯỢC`; lệch nhau ⇒ **CHẶN** | ca khớp vẫn ra `KHÔNG ĐO ĐƯỢC` ⇒ đường đo chưa nối; ca lệch QUA ⇒ đo hình thức |
| **A7** | `adr-song --root .` ⇒ **rc=0**, số ADR = **(nền + 1)**, khớp 1–1 §20. Đo nền **ngay trước** ứng viên | quên hàng §20 ⇒ `rc=9` |
| **A8** | `numstat` vs `base_sha` đo lại: **đúng 4 tệp**, **≤ 300 dòng thêm** | tệp thứ năm, hoặc vượt 300 ⇒ DỪNG, xin |
| **A9** | `doctrine-scan` · `doc-claims-check --strict` · `git diff --check` · `release-verify --strict` (`ok=true`, `expected == checked`) ⇒ **rc=0** | bất kỳ cái nào khác 0 |
| **A10** | `tl.py --selftest` **N/N hai số bằng nhau** trên Linux; trên Windows đòi **không tệ hơn nền** | ứng viên tệ hơn nền ⇒ hồi quy. **`r330` là nợ #565, không tính vào đây** |

## `hinh_dang_ke_thua` — chép từ biên nhận tiền nhiệm (`L4`)

| hình dạng | đếm | nguồn |
|---|---:|---|
| `TIEU-CHI-THEO-GIA-TRI-TUYET-DOI` | **3** | #522 · #548 · #551 `A7` của r1 |
| `R291-DAM-SO-CUNG` | **3** | #522 · #548 · #551 |
| `DANH-SACH-CAM-KHONG-DAO-SANG-CHO-PHEP` | **3** | `v1.36.68` · `doctrine-scan` · #551 `P1-3` của r2 |
| `FAIL-OPEN-KHI-THIEU-DU-KIEN` | **3** | #551 `P1-1` · `P1-3` · `P2-1` |
| `LOI-KHAI-RONG-HON-PHEP-DO` | **3** ← **TĂNG** | #551 `S2` · #551 giả thuyết `P2` bị bác · **#566 `Đ1`: `tac_gia: không phải phiên agent`** |
| `TIEU-CHI-MAT-DOI-TUONG-MA-KHONG-AI-RUT` | **1** | #551 `S1` |
| **`VA-BANG-REGEX-RONG-HON-Y-DINH`** | **1** *(MỚI)* | `19-09` — regex chuyển `phien_doc_lap` cuốn theo 4 khoá, `dang_boi` nằm sai chỗ |

**`LOI-KHAI-RONG-HON-PHEP-DO` nay ở mức BA.** Chốt *"lặp lần thứ BA ⇒ hỏi CÓ NÊN LÀM KHÔNG"*
áp vào đây, và packet **trả lời ngay trong `M1`–`M2`**: không vá từng lời khai, mà **bắt cổng
ĐỌC** trường ấy. Một lời khai không có cổng đọc thì sớm muộn sẽ rộng hơn phép đo — `Đ2` là
phản chứng chạy được cho chính câu này.

## `chua_do_duoc` — ghi thẳng

| # | thứ | vì sao |
|---|---|---|
| **C1** | Ai là executor, và `assurance_target` nào | **CHƯA CHỐT.** Packet sửa cổng assurance nên class `sensitive`; `cross_approved` cần hai họ model độc lập, mà lúc soạn thì `codex` hết quota review, `agy` hết quota. Nếu tới lúc cấp lease vẫn thế thì đường duy nhất là `human_audited` — và khi ấy packet **tự chứng minh chính vấn đề nó đang sửa**. Chủ kho quyết tại thời điểm cấp lease, không quyết ở đây |
| **C2** | Packet có đóng được *"cố tình khai sai"* không | **KHÔNG.** Khi credential dùng chung, một phiên cố tình vẫn khai được `chu_kho_tu_dang`. `M1`–`M2` chỉ đóng *"im lặng"* và *"nhầm chỗ"*. Đóng `cố tình` cần **#338**. Nói thẳng để đừng ai tưởng vá xong là hết |
| **C3** | Nền `bien_nhan_v2` lúc cấp lease | **sẽ trôi** — PR #567 đang mở sẽ đẩy `tổng` lên. `A1` so DELTA đo lại, không ghim số |
| **C4** | Hai biên nhận `human_audited` **v1** có bị luật mới chạm không | **Nghiêng về KHÔNG** (miễn trừ legacy theo băm), nhưng `A1` là phép đo **tổng**, không phải phép đo từng cái. Nếu chúng đỏ thì chốt đã bỏ qua danh sách miễn trừ ⇒ DỪNG |
| **C5** | Ngoại lệ ADR-0044 cho tệp thứ tư | **CHƯA CẤP.** Chưa có ⇒ packet DỪNG ở 3 tệp |
| **C6** | Reviewer có độc lập với đặc tả này không | Phiên soạn đặc tả này cũng là phiên phát hiện `Đ1`/`Đ2`/`Đ3` và là executor của #551. Phiên review kế tiếp **PHẢI** khai `xung_dot_loi_ich_da_khai`, và nên là một phiên **KHÁC** |

## Băm để lease neo vào

```
sha256sum ops/specs/human-audited-khai-ai-dang-r1.md
```
