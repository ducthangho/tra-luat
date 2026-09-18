# ĐẶC TẢ PACKET — `ASSURANCE-NEO-VAO-HO-MODEL` revision 3

| | |
|---|---|
| `packet_id` | `ASSURANCE-NEO-VAO-HO-MODEL` |
| `packet_issue` | **#551** |
| `revision` / `generation` | **3** / 3 |
| `thay_the_cho` | **revision 2** (`sha256 567e68745b6d22aa4e095062f886f90810ff5f004a6b74b6da967d5dcff54192`, 11 936 B) — r2 **giữ nguyên trên đĩa** làm hồ sơ |
| `review_class` | **`sensitive`** (không đổi) |
| `base_sha` | **`eb15657dae7a5f0e494a1dca50fdd6d8a55ed7d3`** (`origin/master`, đo `10:23Z 18-09-2026`) |
| `start_from_sha` | **`f4684e45d77bf7c4aa9144b92b8043bb1774de68`** — bản vá r2/g2 ĐÃ CÓ, không bỏ |
| `executor` | **`antigravity` (agy)** ← ĐỔI (r2: `claude`) |
| `reviewer` | **`claude`** ← ĐỔI (r2: `codex`) |
| `assurance_target` | `cross_approved` — **CÓ ĐIỀU KIỆN**, xem `Đ3` |

## `nguon_cap_viec`

Chỉ thị chủ kho, phiên điều phối `18-09-2026` `10:2xZ`, **nguyên văn**:

> **Do codex hết quota, review bằng chính claude, executor để cho agy**

Mỏ neo bền: bản chiếu chỉ thị tại
[#551 comment `5728658540`](https://github.com/ducthangho/tra-luat/issues/551#issuecomment-5728658540).

Nợ gốc **`PROTOCOL-CHUA-BIET-ANTIGRAVITY`** không đổi; r3 **không** đổi mục tiêu của packet.

## VÌ SAO PHẢI CÓ REVISION 3 — §3.2, ba căn cứ

### `Đ1` — đổi `executor` và `reviewer`, đúng hai trường §3.2 nêu đích danh

§3.2: *"Đổi objective, acceptance, write set, dependency, **executor** hoặc environment tạo revision
mới và làm lease cũ mất hiệu lực."* Chỉ thị đổi **cả hai**. Lease `assurance-ho-model-r2-g2-claude`
mất hiệu lực, đặt bia mộ **HAI CHIỀU** (`thay_the_cho` ở gen 3 **và** `da_bi_thay_the` ở gen 2 —
chốt `_kiem_bia_mo` đòi cả hai).

Căn cứ đo được cho vế "codex hết quota": `chatgpt-codex-connector[bot]` đăng `08:11Z` trên #553 và
#557 — *"You have reached your Codex usage limits for code reviews."* Cộng `launcher.py doctor`:
`codex` **`SAP_HET_HAN`** (ảnh chụp cũ 210,1h). Hai tín hiệu độc lập, cùng hướng. So với `C4` của r2
(*"Chặn ⇒ `human_audited`"*): nay chủ kho chọn đường **thứ ba** — reviewer `claude`.

### `Đ2` — acceptance phải đổi: verdict lượt 1 ra `changes_requested` với 7 LỚP

Verdict lượt 1 (`sha256 e039649cfb9d95845f5335456907a3c9b1d2d0fa12f9a579072a8fa0913fa789`, 14 780 B,
neo `f4684e45`) mở **3 P1 · 3 P2 · 1 P3**. `nghiem_thu` của r2 **không có tiêu chí nào** đóng được
chúng — `A1`–`A12` đều ĐẠT trên `f4684e45` mà bản vá vẫn có ba lỗ fail-open. Đó chính là ca §3.2
gọi tên: *"finding cho thấy chính spec thiếu thì verdict là `blocked` và đi qua revision mới"*.

### `Đ3` — `base_sha` trôi, và `assurance_target` phải gắn ĐIỀU KIỆN

`origin/master` đã đi từ `d705623` sang `eb15657` (merge PR #553). `f4684e45` **không** còn là hậu
duệ của master ⇒ cổng `thu-hoi` sẽ `CHAN [12]`.

Quan trọng hơn: cặp **`claude` review `agy`** là **đúng cặp mà packet này đang tranh luận**.
`docs/adr/0050-…md` của chính bản vá trích `ops/specs/ag-t0-01b-r3.md:47-51`: *"Một phiên AG đặt
`--model claude-opus-4-6-thinking` rồi được một phiên Claude Code review là cùng một họ model, khác
vỏ công cụ — tức `same_provider_approved` đội lốt `cross_approved`"*. Và `P1-2` đo được rằng bảng
mặc định `google_antigravity → gemini` cho cặp ấy **QUA** mà không ai đo gì:

```
agy KHONG khai model   <- claude review   rev=claude exec=gemini  -> QUA   (mac dinh, chua ai do)
agy KHAI  model claude <- claude review   rev=claude exec=claude  -> CHAN  (do that)
```

Nên `assurance_target: cross_approved` của r3 **CÓ ĐIỀU KIỆN**, và điều kiện dùng đúng cơ chế mà
packet đang dựng chứ không phải một luật mới bịa ra:

> Biên nhận của executor `agy` **PHẢI** khai `executor_model` là họ model **thật** đã phục vụ lượt
> chạy. Thiếu trường ấy ⇒ lượt review chỉ được khai **`advisory_review`**, **không** được khai
> `cross_approved`. Đây là `M16`, và nó có tiêu chí `A16` đo được.

## `write_set` — SÁU đường, KHÔNG ĐỔI so r2

```
docs/PROTOCOL_DA_PHIEN.md
ops/bien_nhan_v2.py
ops/bien_nhan_v2_test.py
docs/adr/0050-assurance-neo-vao-ho-model-khong-phai-hang-cong-cu.md
scripts/tl_selftest.py
RELEASE_MANIFEST.json
```

Cả 7 LỚP của verdict lượt 1 đều chiếu vào bốn đường đầu — **không đường nào mới**. Ngoại lệ
ADR-0044 (`ai_nang: ducthangho`, `tran_moi: 6 tệp`, `tran_dong_them: 250`) **giữ nguyên hiệu lực**.

### `RUI_RO_TRAN_DONG` — khai TRƯỚC, không để đụng rồi mới kêu

`f4684e45` đã dùng **165 / 250** dòng thêm. Bảy lớp cần thêm: chốt fail-close cho ba đường vào ·
bảng CHO PHÉP mức bằng chứng · đổi bảng mặc định provider đa model · ca test + đột biến cho từng
đường · một dòng §20 · một mỏ neo trong ADR. Ước lượng **80–120** dòng ⇒ tổng **245–285**.

**Có thể VƯỢT.** Chốt: vượt 250 thì **DỪNG và xin nới**, tuyệt đối không tự nới, và **không** gộp
bớt chốt để lách trần — gộp ba chốt thành một là tạo bộ tương đương, đúng thứ `M14` cấm.

## `ngoai_pham_vi` — cố ý KHÔNG làm (kế thừa r2, thêm một mục)

| thứ | vì sao |
|---|---|
| Nới `same_provider_approved` cho `sensitive` | §8 có dòng cứng; bất biến an toàn |
| Đảo `ASSURANCE_CAM_THEO_PROVIDER` sang CHO PHÉP | nợ `DANH-SACH-CAM-THEO-PROVIDER-CHUA-DAO` |
| Nối `bien_nhan_v2` vào CI làm cổng chặn | nợ `CONG-BIEN-NHAN-KHONG-CHAY-TRONG-CI` |
| Đọc lại verdict đã giao của #546/#538/#540 | luật mới **KHÔNG hồi tố** |
| Đóng nợ `R291-DAM-SO-CUNG` | hình dạng đã ở mức BA, cần packet riêng — chủ kho quyết |
| *(mới)* Vá `m46` / bộ phân hạng đột biến | nợ `PHAN-HANG-DOT-BIEN-PHU-THUOC-MOI-TRUONG` (đo trên PR #556) — **khác packet**, dù cùng tệp |

## `muc_tieu`

`M1`–`M9` **ĐÃ THI CÔNG** ở `f4684e45` và **GIỮ NGUYÊN**; r3 không làm lại. Bảy mục mới, mỗi mục
đóng đúng một LỚP của verdict lượt 1:

| # | mục tiêu | đóng lớp | chiếu vào |
|---|---|---|---|
| **M10** | Thiếu họ model của **một trong hai bên** ⇒ `khong_do_duoc` ⇒ **TỪ CHỐI** `cross_approved`. Không được im lặng bỏ qua | `P1-1` | `ops/bien_nhan_v2.py` |
| **M11** | Bảng mặc định `provider → họ model` **CHỈ** áp cho provider hãng cố định một họ (`openai_codex`, `anthropic_claude`). Vỏ công cụ **đa model** (`google_antigravity`, `openai_api`, …) ⇒ `khong_do_duoc`, đòi khai model tường minh | `P1-2` | `ops/bien_nhan_v2.py` |
| **M12** | `MUC_BANG_CHUNG_MODEL` là **danh sách CHO PHÉP** `{do_may, khai_co_audit, khong_do_duoc}`; giá trị ngoài tập ⇒ ĐỎ. `khong_do_duoc` và RỖNG **không** đủ cho `cross_approved`. `do_may` phải trỏ được một hiện vật đo (`model_evidence_ref`) | `P1-3` | `ops/bien_nhan_v2.py` |
| **M13** | Tên model **không** nằm trong bảng nhận diện ⇒ `khong_do_duoc` ⇒ ĐỎ, **không** coi là "một họ riêng". Bỏ khớp chuỗi con `o1`/`o3` | `P2-1` · `P3-1` | `ops/bien_nhan_v2.py` |
| **M14** | Mỗi đường vào của `M10`–`M13` có **chốt RIÊNG**; đột biến gỡ từng cái phải làm **đúng một** ca ĐỎ. Ba chốt không phân biệt được bằng đầu vào là bộ tương đương ⇒ **hỏng** | tất cả | `ops/bien_nhan_v2_test.py` |
| **M15** | §20 sửa dòng `ADR-0050`: cột "cổng nào ĐỌC luật ấy" từ `**0 cổng**` thành `ops/bien_nhan_v2.py`. Và ADR-0050 neo `granted_on_instruction` (URL comment) thay cho câu *"chỉ thị chủ kho"* không có mỏ neo | `P2-2` · `P2-3` | `docs/PROTOCOL_DA_PHIEN.md` · `docs/adr/0050-…md` |
| **M16** | Biên nhận của executor `agy` khai `executor_model` là họ model **thật** đã phục vụ. Thiếu ⇒ lượt review chỉ được `advisory_review` | `Đ3` | biên nhận (ngoài write set — là **hành vi**, không phải mã) |

## `nghiem_thu` — mỗi tiêu chí nêu phép đo làm nó ĐỎ

`A1`, `A2`, `A4`, `A5`, `A6`, `A8`, `A10`, `A11` **giữ NGUYÊN VĂN r2/r1**. `A3`, `A7`, `A9`, `A12`
nêu lại theo nền mới. Bốn tiêu chí MỚI:

| # | tiêu chí | ĐỎ khi |
|---|---|---|
| **A3** *(nền mới)* | `ops/bien_nhan_v2.py` trên **NỀN** `eb15657` **và** trên ỨNG VIÊN: `0 vi phạm` **và** `0 KHÔNG ĐO ĐƯỢC` ở cả hai, `TỔNG: ĐẠT` cả hai, số `ĐẠT v2`/`tổng` **KHÔNG ĐỔI** giữa hai lần | luật mới từ chối một biên nhận cũ ⇒ hai vế lệch |
| **A7** *(nền mới)* | `adr-song --root .` ⇒ **rc=0**, số ADR = **(nền + 1)**, khớp 1–1 §20. Đo nền NGAY TRƯỚC ứng viên | quên dòng §20 ⇒ `rc=9` |
| **A9** *(nền mới)* | `numstat` vs `base_sha` `eb15657`: **đúng 6 tệp**, **≤ 250 dòng thêm** | tệp thứ bảy, hoặc vượt 250 ⇒ DỪNG, xin |
| **A12** *(nền mới)* | `release-verify … --strict --json` ⇒ `ok=true`, **`expected_file_count` == `checked_file_count` == 180**, `errors=0` | quên tái sinh manifest |
| **A13** *(MỚI — `M10`+`M11`)* | Dựng bốn ca: (a) đủ hai họ, khác nhau ⇒ QUA; (b) đủ hai họ, giống nhau ⇒ CHẶN; (c) **thiếu** họ executor ⇒ **CHẶN**; (d) `executor_provider: google_antigravity` **không** khai model ⇒ **CHẶN**. Ca (a) là **ĐỐI CHỨNG BIẾT TRƯỚC ĐÁP ÁN** — nó phải QUA, nếu không thì rig hỏng | (c) hoặc (d) QUA ⇒ fail-open còn nguyên; (a) CHẶN ⇒ rig hỏng, đừng tin ba ca kia |
| **A14** *(MỚI — `M12`)* | Năm ca mức bằng chứng: `do_may` **không có** `model_evidence_ref` ⇒ CHẶN · `khai_co_audit` thiếu người audit ⇒ CHẶN · `khong_do_duoc` ⇒ CHẶN · RỖNG ⇒ CHẶN · một chuỗi **BỊA ĐẶT** ⇒ CHẶN | bất kỳ ca nào QUA |
| **A15** *(MỚI — `M13`+`M14`)* | Ba cặp tên lạ cùng họ (`grok-4`/`grok-3`, `llama-70b`/`llama-8b`, `deepseek-v3`/`deepseek-r1`) ⇒ **CHẶN** (`khong_do_duoc`). Và **mỗi** chốt của `M10`–`M13` có một đột biến **RIÊNG**, mỗi đột biến làm **đúng một** ca đích ĐỎ, phân hạng **`giet_that`** — không phải `tin_dung_gia` | hai đột biến giết cùng một ca ⇒ bộ tương đương; `tin_dung_gia` ⇒ tín dụng giả |
| **A16** *(MỚI — `M16`)* | Biên nhận executor có `executor_model` khai họ model thật, và verdict lượt sau **nêu lại** giá trị ấy. Thiếu ⇒ verdict **phải** khai `advisory_review` | verdict khai `cross_approved` mà biên nhận executor không có `executor_model` |

### Nền đo tại lúc đóng băng — `10:23Z 18-09-2026`, trên `eb15657dae7a`

```
bien_nhan_v2 : 125 ĐẠT v2 · 11/11 miễn trừ legacy · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 178
adr-song     : sạch — 49 ADR trên đĩa, 49 dòng §20, khớp 1–1
docs/**/*.md : 74
RELEASE_MANIFEST.json file_count : 180
```

**Mọi con số trên là NỀN, không phải tiêu chí.** `A3` và `A7` so **DELTA** với nền **đo lại**, đúng
`L5`. Ghim con số vào tiêu chí là tái tạo đúng `Đ3` của r2. Nhắc riêng: nền `bien_nhan_v2` đã đi
`124/177` → `125/178` chỉ trong ba giờ, và PR #555/#556/#558 đang mở sẽ đẩy nó lên nữa.

## `hinh_dang_ke_thua`

| hình dạng | đếm | nguồn |
|---|---:|---|
| `TIEU-CHI-THEO-GIA-TRI-TUYET-DOI` | **3** | #522 · #548 · #551 `A7` của r1 |
| `R291-DAM-SO-CUNG` | **3** | #522 · #548 · #551 |
| `TIEU-CHI-NEU-TRUONG-CHUA-AI-DO` | **1** | #548 `A7` của r2 |
| **`DANH-SACH-CAM-KHONG-DAO-SANG-CHO-PHEP`** | **3** | `v1.36.68` (PR #104) · `doctrine-scan` · **#551 `P1-3` của r2** |
| **`FAIL-OPEN-KHI-THIEU-DU-KIEN`** | **3** | `P1-1` · `P1-3` · `P2-1` — **ba đường vào của MỘT lỗ, trong CÙNG một bản vá** |

**`FAIL-OPEN-KHI-THIEU-DU-KIEN` chạm mức BA ngay trong một lượt.** Chốt *"lặp lần thứ BA ⇒ hỏi CÓ
NÊN LÀM KHÔNG"* áp vào đây thành câu hỏi thiết kế, và r3 **trả lời ngay trong `M10`–`M14`**: không
vá ba chỗ rời, mà đảo cả lớp sang **fail-close mặc định** — thiếu dữ kiện thì `khong_do_duoc`, và
`khong_do_duoc` **không** mua được `cross_approved`. Đó là đổi KIẾN TRÚC, không phải ba bản vá.

## `chua_do_duoc` — ghi thẳng

| # | thứ | vì sao |
|---|---|---|
| **C1** | Packet có gỡ được trần cho #546 không | **KHÔNG BIẾT, nghiêng về KHÔNG** — giữ nguyên văn r1/r2 |
| **C2** | Model nào agy đã chạy ở #546/#538/#540 | không có bằng chứng máy; nợ `AGY-CHUA-ATTEST-MODEL-TUNG-LUOT` |
| **C3** | Có biên nhận cũ nào bị luật mới từ chối không | `A3` là phép đo **tổng** |
| **C4** *(viết lại)* | Cặp `claude`↔`agy` có thật sự khác họ model không | **KHÔNG ĐO ĐƯỢC cho tới khi `M16` chạy.** Đây là lý do `assurance_target` có điều kiện, chứ không phải một chi tiết thủ tục |
| **C5** | Trần 250 dòng có đủ không | ước lượng **245–285** — **có thể vượt**. Vượt ⇒ DỪNG, xin lại |
| **C6** | `M8` có phải lần cuối phải kê khai slot không | phụ thuộc nợ `R291-DAM-SO-CUNG` |
| **C7** *(mới)* | Reviewer `claude` lượt sau có độc lập với đặc tả này không | **KHÔNG** — phiên soạn r3 cũng là phiên viết verdict lượt 1 và r2. Phiên review kế tiếp **PHẢI** khai `xung_dot_loi_ich_da_khai`, và nên là một phiên `claude` **KHÁC** |
| **C8** *(mới)* | Trần vòng review còn bao nhiêu | `ADR-0048` nâng trục VÒNG lên **10**; packet này mới ở **lượt 1**. Không chạm trần |

## Băm để lease neo vào

```
sha256sum ops/specs/assurance-neo-vao-ho-model-r3.md
```
