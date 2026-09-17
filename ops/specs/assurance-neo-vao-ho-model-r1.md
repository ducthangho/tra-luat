# ĐẶC TẢ PACKET — `ASSURANCE-NEO-VAO-HO-MODEL` revision 1

| | |
|---|---|
| `packet_id` | `ASSURANCE-NEO-VAO-HO-MODEL` |
| `packet_issue` | *(chưa mở — điền khi có Issue)* |
| `revision` / `generation` | 1 / 1 |
| `review_class` | **`sensitive`** |
| `base_sha` dự kiến | `f27a28ffa3cc` (`origin/master`, đo 10:41Z 17-09-2026) |
| `executor` | `claude` |
| `reviewer` | `codex` |
| `assurance_target` | `cross_approved`; **fallback `human_audited`** nếu codex chặn |

## `nguon_cap_viec`

Nợ **`PROTOCOL-CHUA-BIET-ANTIGRAVITY`**, khai lần đầu trong lease
`ops/leases/moi-truong-r1-g1-antigravity.yaml` (trường `assurance_target_vi_sao`), nhắc lại ở
verdict lượt 1/2/3 của #546 và ở chỉ thị chủ kho phiên 17-09-2026:

> **Mở packet sửa PROTOCOL để nhận antigravity đi**

Nó chặn `cross_approved` của **ba** packet: #546, #538, #540 (đơn vị: packet).

## `review_class` — vì sao `sensitive`

`docs/PROTOCOL_DA_PHIEN.md` §8 nêu đích danh *"review/land authority"*. Packet này sửa **chính luật
assurance** và **chính cổng đọc luật ấy**. Không khai thấp hơn được.

## `write_set` — ĐÚNG BỐN đường, liệt kê tường minh

```
docs/PROTOCOL_DA_PHIEN.md
ops/bien_nhan_v2.py
ops/bien_nhan_v2_test.py
docs/adr/0050-assurance-neo-vao-ho-model-khong-phai-hang-cong-cu.md
```

**Vì sao BỐN, không phải một.** Phản chứng đã chạy (10:35Z 17-09-2026): `ops/bien_nhan_v2.py:145`
neo **nguyên văn** câu `` `cross_approved`: Claude review Codex hoặc Codex review Claude `` vào
PROTOCOL qua `_NEO_LUAT_CHEP_TAY`. Đột biến đúng câu ấy trong PROTOCOL ⇒

```
TỔNG: KHÔNG ĐO ĐƯỢC
"luật chép tay mất neo; mọi phép kiểm suy từ provider (danh sách CHO PHÉP, bề mặt/vận chuyển,
 giới hạn assurance theo provider) KHÔNG chạy lượt này"
124 ĐẠT v2 · 0 vi phạm · 1 KHÔNG ĐO ĐƯỢC · tổng 177   →   rc=0
```

Sửa PROTOCOL mà không sửa cổng là **làm câm cổng**, không phải đổi luật. `bien_nhan_v2_test.py`
bắt buộc theo `L3`: tiêu chí phải ĐỎ được. ADR bắt buộc vì đây là quyết định kiến trúc, và
`adr-song` đòi **mỗi ADR một dòng §20** (nền 10:41Z: **48 ADR / 48 dòng**, khớp 1–1).

**Trần ADR-0044 `sensitive` là ≤ 3 tệp / ≤ 300 dòng thêm** ⇒ packet này **cần ngoại lệ 4 tệp**,
phải xin **TRƯỚC** khi bắt tay. Trần dòng thêm đề xuất **≤ 250** (packet văn bản + một bảng).

## `ngoai_pham_vi` — cố ý KHÔNG làm

| thứ | vì sao |
|---|---|
| Nới `same_provider_approved` cho `sensitive` | §8 có dòng cứng *"`same_provider_approved` vẫn không thay `cross_approved` cho class `sensitive`"*. Đó là **bất biến an toàn**, không phải thứ vướng chân. |
| Đảo `ASSURANCE_CAM_THEO_PROVIDER` từ CẤM sang CHO PHÉP | Đụng `openai_chatgpt` và mọi biên nhận cũ ⇒ packet riêng. Nợ: **`DANH-SACH-CAM-THEO-PROVIDER-CHUA-DAO`**. |
| Nối `bien_nhan_v2` vào CI như cổng chặn | Đo 10:35Z: CI chỉ chạy `ops/bien_nhan_v2_test.py`, **không** chạy chính cổng; và cổng trả `rc=0` cả khi `KHÔNG ĐO ĐƯỢC` ⇒ mất neo luật là chuyện **im lặng**. Khuyết của **đường CI**, không phải của luật. Nợ: **`CONG-BIEN-NHAN-KHONG-CHAY-TRONG-CI`**. |
| Đọc lại verdict đã giao của #546/#538/#540 | Luật mới **KHÔNG hồi tố**. Sửa verdict đã giao là viết lại lịch sử. Muốn nâng thì chạy **lượt review mới** dưới luật mới. |
| Cho `agy` phát ra định danh model từng lượt | Đó là việc của `agy` CLI / của `launcher.py`, ngoài write set. Nợ: **`AGY-CHUA-ATTEST-MODEL-TUNG-LUOT`**. |

## `muc_tieu`

| # | mục tiêu | chiếu vào |
|---|---|---|
| **M1** | §8 định nghĩa `cross_approved` neo vào **HỌ MODEL đã phục vụ lượt chạy**, không vào **HÃNG CÔNG CỤ**. Câu neo cũ (*"Claude review Codex hoặc Codex review Claude"*) thay bằng phát biểu theo họ model, và **nêu `Codex`/`Claude` làm VÍ DỤ**, không làm định nghĩa. | `docs/PROTOCOL_DA_PHIEN.md` |
| **M2** | §8 khai **ba mức bằng chứng model** và nói rõ mức nào yếu hơn: `do_may` (máy đo từng lượt, vd `modelUsage[*].canonicalModel`) · `khai_co_audit` (người khai + người audit xác nhận) · `khong_do_duoc`. Mức `khai_co_audit` **phải** tự khai là yếu hơn `do_may` ngay tại chỗ dùng. | `docs/PROTOCOL_DA_PHIEN.md` |
| **M3** | §20 thêm **đúng một dòng** cho ADR-0050. | `docs/PROTOCOL_DA_PHIEN.md` |
| **M4** | ADR-0050 ghi quyết định + căn cứ: mâu thuẫn `doctrine-scan-…-r1.md:13` ↔ `ag-t0-01b-r3.md:47-51`, và vì sao neo vào họ model. | `docs/adr/0050-…md` |
| **M5** | `bien_nhan_v2.py`: `_NEO_LUAT_CHEP_TAY` neo vào **câu MỚI**; thêm một **BẢNG CHO PHÉP** ánh xạ `provider → họ model mặc định` và cho biên nhận khai đè bằng trường model có bằng chứng. `ASSURANCE_CAM_THEO_PROVIDER` **giữ nguyên**. | `ops/bien_nhan_v2.py` |
| **M6** | `bien_nhan_v2.py`: biên nhận khai `cross_approved` mà **hai bên cùng họ model** ⇒ **từ chối**; khai `cross_approved` với `khai_co_audit` mà **thiếu người audit** ⇒ **từ chối**. | `ops/bien_nhan_v2.py` |
| **M7** | `bien_nhan_v2_test.py`: mỗi chốt của M5/M6 có **ca riêng** và **đột biến riêng** đổi màu đúng ca ấy. | `ops/bien_nhan_v2_test.py` |

## `nghiem_thu` — mỗi tiêu chí nêu phép đo làm nó ĐỎ

| # | tiêu chí | ĐỎ khi |
|---|---|---|
| **A1** (M1) | `grep` câu neo cũ trong PROTOCOL ⇒ **0**; câu mới có mặt **đúng 1 lần**; `_NEO_LUAT_CHEP_TAY` trỏ câu mới | còn câu cũ, hoặc câu mới ≠ 1 lần, hoặc neo lệch |
| **A2** (M1,M5) | `python3 ops/bien_nhan_v2.py` ⇒ **`TỔNG: ĐẠT`**, và **không** có dòng `KHÔNG ĐO ĐƯỢC` nào về mất neo | sửa PROTOCOL mà quên sửa neo ⇒ `KHÔNG ĐO ĐƯỢC` xuất hiện (phản chứng đã chạy 10:35Z) |
| **A3** (M5,M6) | Số biên nhận **KHÔNG đổi** so nền: `124 ĐẠT v2 · 11/11 miễn trừ · 42 NỢ · 0 vi phạm · tổng 177` (đo 10:41Z 17-09-2026) | luật mới từ chối một biên nhận cũ ⇒ con số lệch ngay |
| **A4** (M6) | Ca dựng biên nhận giả: `cross_approved` + hai bên **cùng họ model** ⇒ cổng **từ chối** | cổng nhận ⇒ ĐỎ |
| **A5** (M6) | Ca dựng biên nhận giả: `cross_approved` + `khai_co_audit` **không có người audit** ⇒ cổng **từ chối** | cổng nhận ⇒ ĐỎ |
| **A6** (M7) | Mỗi chốt M5/M6 có **một** mục đột biến; gỡ chốt ⇒ **đúng ca đích** ĐỎ, ca khác họ vẫn XANH | đột biến sống sót, hoặc giết nhầm ca khác |
| **A7** (M3) | `python3 .claude/dev/packet_loop.py adr-song --root .` ⇒ **rc=0**, và số ADR **49 / 49** | thêm ADR mà quên dòng §20 ⇒ `rc=9` |
| **A8** | `doctrine-scan` · `doc-claims-check --strict` · `git diff --check` ⇒ **rc=0** cả ba (`core.abbrev=7`) | bất kỳ cái nào khác 0 |
| **A9** | `numstat` vs `f27a28f`: **đúng 4 tệp**, **≤ 250 dòng thêm** | tệp thứ năm, hoặc vượt 250 |
| **A10** | Spec này khai thẳng: packet **KHÔNG hứa** #546 đạt `cross_approved` — xem `chua_do_duoc` C1 | verdict/biên nhận nào khai ngược lại |

## `hinh_dang_ke_thua`

**`khong_ap_dung`** — đây **không** phải packet khắc phục của một packet đã chạy; nó là packet mới
sinh từ một nợ. Không có biên nhận tiền nhiệm để chép bộ đếm hình dạng lỗi (`L4`). Bộ đếm của
packet này bắt đầu từ **0**.

## `chua_do_duoc` — ghi thẳng, không giấu sau chữ "có thể"

| # | thứ | vì sao |
|---|---|---|
| **C1** | Packet này có **gỡ được trần cho #546 không** | **KHÔNG BIẾT, và nghiêng về KHÔNG.** Nếu agy chạy model **họ Claude** thì cặp agy↔claude là `same_provider_approved`, mà `sensitive` **không nhận** mức đó (`ngoai_pham_vi` dòng 1). Packet làm cái trần **đo được và có tên**, không hứa gỡ nó. |
| **C2** | Model nào agy đã thật sự chạy ở #546/#538/#540 | Không có bằng chứng máy. `_do_antigravity` chạy `agy models` — **đếm model KHẢ DỤNG**, không nói model ĐÃ CHẠY (đo 10:41Z). Chỉ `khai_co_audit` mới trả lời được, và nó là mức yếu. |
| **C3** | Có biên nhận cũ nào bị luật mới từ chối không | Chưa đo từng biên nhận. `A3` là phép đo **tổng** sẽ bắt được, nhưng không nói trước biên nhận nào. |
| **C4** | Codex có chạy được lượt review không | Đo nhiều lần trong chuỗi 16→17-09: codex `SAP_HET_HAN` / hết quota. Nếu chặn thì `assurance` tụt về `human_audited` với chủ kho là người audit. |
| **C5** | Ngưỡng `≤ 250` dòng thêm có đủ không | Ước lượng, chưa có packet tương đương để đo. Packet sửa luật + bảng + test; nếu vượt thì **DỪNG và xin lại**, không vá hờ. |

## Thứ tự với các packet đang mở

`docs/PROTOCOL_DA_PHIEN.md` đang bị lease **`ci-windows-r1-g1-antigravity`** (#548) giữ —
`ai-dang-giu` ⇒ `NGƯỜI_GIỮ 1` (đo 10:30Z 17-09-2026). §5 buộc **chạy tuần tự**.

Chuỗi đã chốt: **#546 → #548 → packet này.** Không cấp lease cho packet này khi #548 còn giữ
`PROTOCOL`.
