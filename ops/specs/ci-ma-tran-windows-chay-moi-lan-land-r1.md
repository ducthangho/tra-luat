# ĐẶC TẢ PACKET — `CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND`, revision 1

> **ĐÃ ĐÓNG BĂNG.** Tệp này có băm; lease neo vào băm ấy. Cần đổi ⇒ **revision 2**, không sửa đè.
> Mọi con số dưới đây kèm **thời điểm đo**. Số không có thời điểm là số không đo được — không có số nào như thế trong tệp này.

| | |
|---|---|
| `packet_id` | `CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND` |
| `packet_issue` | 548 |
| `revision` | 1 |
| `review_class` | **`sensitive`** |
| `hinh_dang_ke_thua` | `khong_ap_dung` |

## `nguon_cap_viec`

Chỉ thị chủ kho, phiên điều phối 16-09-2026: *"Mở packet sửa ma trận Windows trong ci.yml đi"* · *"Viết spec packet #548 đi"*, nối tiếp ràng buộc thường trực *"CI Window gặp lỗi đã biết, để đỡ tốn tiền, không chạy CI Windows"*.

Chín quyết định đã duyệt qua hai vòng `soan-spec` (*"Đồng ý cả năm khuyến nghị"*, *"Đồng ý cả bốn"*) — ghi lại vì đặc tả này **là hệ quả của chúng**, không phải một thiết kế tự chọn:

| # | quyết định |
|---|---|
| Q1 | Hướng **B** — đổi **CÒ**, và khai thẳng đó là **đổi tiêu chuẩn gate**. Không chọn C (`paths:` = danh sách đoán trước). |
| Q2 | Khử trùng lặp bằng **job `chuan-bi` xuất `outputs`** — một nguồn sự thật theo cấu trúc, không phải "được canh". |
| Q3 | Nghiệm thu bằng **bộ đo offline** làm chính, **đo sau merge** làm xác nhận. Không xin ngoại lệ `workflow_dispatch`. |
| Q4 | Duyệt trước **ngoại lệ ADR-0044 lên 4 tệp**; dòng thêm vẫn `≤ 300`. |
| Q5 | Executor **agy**, reviewer **claude**, `human_audited`; **xếp SAU #546**, không song song. |
| Q6 | Cò phát hành = **cổng tại chỗ của `deploy-package.*`**, không dựng quy ước tag mới. |
| Q7 | Bỏ Windows khỏi **cả ba** job `ci.yml`; bù bằng cách nới battery của `deploy-package.*` là **nợ có tên**, không làm ở đây. |
| Q8 | **`launcher-windows.yml` GIỮ NGUYÊN**, không đụng — và ADR phải khai rằng *"land không còn chạy Windows"* là **KHÔNG đúng tuyệt đối**. |
| Q9 | Hai chốt: **chốt nguồn duy nhất** (cấu trúc) + **evaluator TỐI GIẢN fail-close**; **không** viết evaluator tổng quát. |

## Nền đo — mọi con số kèm thời điểm và ĐƠN VỊ

Nền: `origin/master` = `f27a28f`, đo **18:0x–18:3xZ 16-09-2026**.

| # | phép đo | đơn vị | kết quả |
|---|---|---|---|
| Đ1 | job có biểu thức ma trận trong `ci.yml` | **job** | **3** (`gate` `:43` · `gate-registry` `:602` · `gate-packet-loop` `:666`), ba bản chép nguyên văn cùng một biểu thức |
| Đ2 | lần xuất hiện chuỗi `windows-latest` trong `ci.yml` | **lần** | **6** (3 trong biểu thức, 3 trong chú thích) |
| Đ3 | nguồn sinh job Windows trên một push `master` | **workflow job** | **4** — ba job trên + `launcher-windows.yml` |
| Đ4 | wall-clock `gate (windows-latest)` trên `2e84f3f` | **giây tường** | **27m19s**, kết quả **failure** |
| Đ5 | wall-clock `gate-packet-loop (windows-latest)` trên `2e84f3f` | **giây tường** | **14m52s**, **success** |
| Đ6 | wall-clock `launcher (Windows that)` run `35125176975` | **giây tường** | ~**4m51s**, **success** |
| Đ7 | `run_duration_ms` của run `35125176821` | **ms** | **2 927 000** (48m47s) |
| Đ8 | phút TÍNH TIỀN của run ấy | — | **KHÔNG ĐO ĐƯỢC**: `get_workflow_run_usage` trả `duration_ms: 0` cho **cả 6** job |
| Đ9 | ca ĐỎ của `lease_publish_test` trên `gate (windows-latest)` | **ca test** | **15/148** đỏ (`133/148 đạt`, bỏ qua 7); trùng từng chữ với nền `19de5669` ⇒ **delta = 0** |
| Đ10 | workflow bắt `tags:` | **workflow** | **0**; cả **39** tag đều là `luu-tru/*` · `archive/*` (lưu trữ verdict) |
| Đ11 | cổng trong `deploy-package.ps1` | **cổng** | **8**, và `:234` `Bad 'GATE ĐỎ — DỪNG, không build/không đẩy'` ⇒ **chặn thật** |
| Đ12 | bộ nào ĐÁNH GIÁ được `fromJSON(cond && A \|\| B)` | **bộ** | **0**. `_ly_do_bo_qua_workflow` (`t70`/`t71`) chỉ đọc ma trận dạng **danh sách tường minh** |
| Đ13 | lease đang giữ `ci.yml` · `launcher-windows.yml` · `lease_publish_test.py` · `scripts/tl.py` | **lease** | **0** cả bốn. Ca hiệu chỉnh `launcher.py` ⇒ **1** (`moi-truong-r1-g1-antigravity`) — bộ quét trả đúng cho câu đã biết đáp án |
| Đ14 | ADR trên đĩa / dòng trong `§20` | **ADR** · **dòng** | **48 / 48**, khớp 1–1 |
| Đ15 | thêm một ADR mà **không** thêm dòng `§20` | — | `adr-song` **rc=9**, *"2 chỗ lệch"* — **phản chứng đã chạy**, không phải suy từ tài liệu |

**Bất biến neo quyết định (không trôi theo số):** *lane Windows của `master` chạy SAU merge, không cổng nào chặn theo nó, và cổng phát hành thật nằm ở `deploy-package.*`.* Các số Đ1–Đ15 chỉ để đối chiếu.

## `review_class`

**`sensitive`.** `docs/PROTOCOL_DA_PHIEN.md:668` nêu **đích danh** *"workflow/CI authority"*. Không khai thấp hơn được; executor không được hạ lớp.

`assurance_target`: **`human_audited`** (Q5). Đo sống 16-09: `codex` kiểm sống HỎNG `rc=1` + hết quota · `claude` `CHƯA_XÁC_THỰC` · `doctor --kiem-song` `rc=12`. `antigravity` xuất hiện **0 lần** trong protocol ⇒ nợ `PROTOCOL-CHUA-BIET-ANTIGRAVITY` vẫn mở.

## `write_set` — ĐÚNG BỐN đường, liệt kê tường minh

```
.github/workflows/ci.yml
ops/lease_publish_test.py
docs/adr/0049-cong-hai-nen-truoc-phat-hanh-khong-phai-moi-lan-land.md
docs/PROTOCOL_DA_PHIEN.md
```

**Đường thứ tư phải được chủ kho gật RIÊNG trước khi cấp lease, và đây là phát hiện của chính lượt soạn spec.** Lúc duyệt ngoại lệ 4 tệp (Q4), tệp thứ tư được hình dung là **ADR**. Đo lại (Đ15) cho thấy thêm ADR mà không thêm một dòng vào `§20` làm `adr-song` **rc=9** ⇒ tệp thứ tư thật ra là **`docs/PROTOCOL_DA_PHIEN.md`**, và ADR thành tệp thứ **ba**. `docs/PROTOCOL_DA_PHIEN.md` nằm trong `khong_duoc_cham` của nhiều lease khác, nên **không được im lặng coi nó đã nằm trong ngoại lệ đã duyệt**.

Phạm vi cho phép trên đường thứ tư là **ĐÚNG MỘT DÒNG**: một hàng mới trong bảng `§20` cho `ADR-0049`. Chạm bất kỳ dòng nào khác của protocol ⇒ **DỪNG**, đi qua revision mới.

Đã quét lease toàn kho trước khi đóng băng (Đ13): `NGƯỜI_GIỮ 0` cho cả bốn; so tập tên ref hai nguồn (`ls-remote` vs `for-each-ref`) ⇒ `comm -23` **RỖNG**, không mù.

## `ngoai_pham_vi` — CỐ Ý không làm

| thứ | vì sao |
|---|---|
| `.github/workflows/launcher-windows.yml` | Q8. Đã hẹp sẵn bằng `paths: .claude/dev/**`, rẻ nhất (Đ6), và là cổng Windows **duy nhất** viết riêng cho `launcher` — đúng thứ #546 sắp sửa |
| `scripts/deploy-package.sh` · `.ps1` | Q7. Nới battery 8 cổng (Đ11) để bù phần Windows mất đi là **nợ có tên** `BATTERY-DEPLOY-HEP-HON-LANE-CI`, không làm ở đây — thêm hai tệp là vượt cả ngoại lệ 4 tệp |
| vá 15 ca đỏ của `lease_publish_test` trên Windows (Đ9) | đó là packet **#546**, lớp lỗi L4 `encoding=` |
| `ops/lease_publish.py` `:1106` `/usr/bin:/bin` | packet **#541** |
| evaluator tổng quát cho ngôn ngữ biểu thức Actions | Q9. Tự dựng một **danh sách đoán trước** khác — đúng hình dạng kho đã trả giá bốn lần |
| quy ước tag phát hành | Q6. Không gian tag đang dùng cho lưu trữ (Đ10); thêm một quy ước là thêm một thứ phải canh |

## `muc_tieu` — mỗi mục chiếu vào MỘT đường dẫn của `write_set`

| # | mục tiêu | đường dẫn |
|---|---|---|
| **M1** | Thêm job `chuan-bi` (ubuntu, không checkout mã sản phẩm) tính **một lần** danh sách nền và xuất qua `outputs.os`. Điều kiện Windows **bỏ `github.ref == 'refs/heads/master'`**, giữ `workflow_dispatch` và nhãn `windows` | `ci.yml` |
| **M2** | Ba job `gate` · `gate-registry` · `gate-packet-loop` đọc `needs.chuan-bi.outputs.os`; **xoá cả ba biểu thức chép** (Đ1) | `ci.yml` |
| **M3** | Chốt **NGUỒN DUY NHẤT**: quét `ci.yml`, ĐỎ khi có bất kỳ job nào khai `os:` riêng ngoài `needs.<chuan-bi>.outputs.os` | `ops/lease_publish_test.py` |
| **M4** | **Evaluator TỐI GIẢN** cho đúng hình biểu thức của `chuan-bi`, **fail-close** (`KHÔNG ĐO ĐƯỢC` ⇒ ĐỎ) khi gặp hình khác; bảng ca `push master` · `PR thường` · `PR nhãn windows` · `workflow_dispatch` | `ops/lease_publish_test.py` |
| **M5** | ADR-0049 ghi **đổi tiêu chuẩn gate**: cổng hai nền trước phát hành = cổng tại chỗ của `deploy-package.*` (Đ11), KHÔNG phải lane `master` của `ci.yml`; kèm phần **mất mát** (~22 bước mất soi Windows) và câu khai ở M6 | `docs/adr/0049-*.md` |
| **M6** | ADR-0049 khai rõ: *"land không còn chạy Windows"* **KHÔNG đúng tuyệt đối** — diff chạm `.claude/dev/**` vẫn sinh ~5 phút Windows qua `launcher-windows.yml` (Đ6) | `docs/adr/0049-*.md` |
| **M7** | Một hàng mới cho `ADR-0049` trong bảng `§20`, **đúng một dòng** | `docs/PROTOCOL_DA_PHIEN.md` |

## `nghiem_thu` — mỗi tiêu chí nêu phép đo làm nó ĐỎ

| # | tiêu chí | cái gì làm nó ĐỎ |
|---|---|---|
| **A1** (M1,M2) | `grep -c 'os: ${{ fromJSON'` trên `ci.yml` = **1** (chỉ `chuan-bi`), giảm từ **3** (Đ1) | số khác 1 ⇒ ĐỎ |
| **A2** (M3) | Ca `rXX_` mới: dựng `ci.yml` giả có **một** job lén khai `os:` riêng ⇒ cổng ĐỎ; bản không lén ⇒ `rc=0` | **đột biến**: gỡ chốt nguồn-duy-nhất ⇒ ca "job lén khai `os:`" phải chuyển sang ĐẠT. Không chuyển màu ⇒ chốt không có răng |
| **A3** (M4) | Bảng ca của evaluator: `push master` ⇒ `["ubuntu-latest"]` · `PR thường` ⇒ `["ubuntu-latest"]` · `PR nhãn windows` ⇒ hai nền · `workflow_dispatch` ⇒ hai nền. **Bốn ca, bốn kết quả tường minh** | sai một ca ⇒ ĐỎ. **đột biến**: đưa `github.ref == 'refs/heads/master'` trở lại biểu thức ⇒ ca `push master` phải ĐỎ |
| **A4** (M4) | Fail-close: đưa evaluator một biểu thức **hình khác** (ví dụ lồng `fromJSON` hai tầng) ⇒ in `KHÔNG ĐO ĐƯỢC` và ĐỎ | trả một đáp án đoán thay vì ĐỎ ⇒ hỏng. **đột biến**: đổi nhánh fail-close thành `return ["ubuntu-latest"]` ⇒ ca ấy phải ĐỎ |
| **A5** (M5,M6,M7) | `packet_loop.py adr-song --root .` ⇒ **49 ADR / 49 dòng**, khớp 1–1 | thiếu dòng `§20` ⇒ `rc=9` — **đã dựng phản chứng**, Đ15 |
| **A6** (toàn packet) | `actionlint` trên **cả 6** workflow: `rc` và **số finding**, kèm nền đo trên `origin/master` sạch ⇒ khẳng định **delta**. Thiếu `actionlint` ⇒ **ĐỎ**, không phải bỏ qua | delta finding ≠ 0 ⇒ ĐỎ. Lưu ý đo được 23-08: có `shellcheck` ⇒ `rc=1` 1 finding · vắng ⇒ `rc=0` — **phải khai nền đo có `shellcheck` hay không** |
| **A7** (toàn packet) | `ops/lease_publish_test.py` chạy trọn: **N/N**, hai số BẰNG NHAU, `rc=0`; và `packet_loop.py doctrine-scan` · `adr-song` · `tl.py doc-claims-check --strict` · `git diff --check` · `tl.py --selftest` · `release-verify --strict` đều `rc=0` | bất kỳ cổng nào khác 0, hoặc `N/M` hai số khác nhau ⇒ ĐỎ |
| **A8** (ADR-0044) | `git diff --numstat` so `base_sha`: **≤ 4 tệp** và **≤ 300 dòng thêm** | vượt ⇒ **DỪNG**, xin ngoại lệ **TRƯỚC** khi đẩy. Con số này chống đỡ một câu về **THẨM QUYỀN** — đo lại ngay trước khi đăng, không chép lại |
| **A9** (sau merge) | Đếm job Windows sinh bởi push `master` đầu tiên sau land, bằng `actions_list` lọc `head_sha`: phải là **0** từ `ci.yml`. Job từ `launcher-windows.yml` **không tính** nếu diff chạm `.claude/dev/**` | > 0 job Windows từ `ci.yml` ⇒ packet **chưa đạt**, dù A1–A8 xanh |

**A9 chỉ đo được SAU merge.** Đó là điều kiện của bài toán (Q3), không phải thiếu sót: câu hỏi *"một push `master` sinh mấy job Windows"* không có đường đo nào khác khi `manual_ci_budget = 0`. A1–A8 là thứ mua được **trước** merge; A9 là phép xác nhận.

## `hinh_dang_ke_thua`

**`khong_ap_dung`.** Đây không phải packet khắc phục một packet trước; không có bộ đếm hình dạng lỗi nào để chép sang (L4). Điều kiện dừng *"cùng một hình dạng lỗi lặp lần thứ BA"* vì thế **bắt đầu từ 0** ở packet này — và nói thẳng ra đây để không ai tưởng nó mang nợ từ #543 hay #546.

## `chua_do_duoc` — ghi thẳng, không giấu sau chữ "có thể"

| # | thứ không đo được từ phiên này | vì sao |
|---|---|---|
| **K1** | **Phút TÍNH TIỀN** tiết kiệm được | `get_workflow_run_usage` trả `duration_ms: 0` cho cả 6 job (Đ8). Mọi con số phút-tiền trong hồ sơ packet là **THUẬT LẠI** từ chú thích `ci.yml` (r245: ~8 100 phút/tháng so với hạn mức 2 000, **đã cạn thật** 12-08), không phải phép đo của phiên này |
| **K2** | **Tần suất push `master`** mỗi ngày | bộ lọc `workflow_id` của `actions_list` **bị bỏ qua** (tái hiện được), nên không đếm được rẻ. Không có nó thì không quy ra tổng tiết kiệm |
| **K3** | GitHub Actions có nhận **YAML anchor** trong cùng tệp không | không chạy được workflow để thử. Không ảnh hưởng: thiết kế đã chọn `outputs` (Q2), không dùng anchor |
| **K4** | Mất Windows cho **~22 bước** kia có làm lọt lỗi nền thật không | chỉ biết được bằng một lỗi lọt trong tương lai. ADR-0049 phải khai đây là **rủi ro đã nhận**, không phải rủi ro đã loại |
| **K5** | `gate-registry (windows-latest)` trên `2e84f3f` kết thúc lúc nào | đo được giờ bắt đầu (16:57:45), không đo được giờ kết thúc trong phiên này |

## Ràng buộc và điều kiện dừng

**Ràng buộc:**

- **KHÔNG CI tay**: `manual_ci_budget = 0`; cấm `workflow_dispatch`, cấm gắn nhãn `windows`, cấm full CI tay. Nghịch lý đã biết và đã chọn cách sống chung: packet sửa đường Windows mà không được chạy Windows để nghiệm thu (Q3 ⇒ A1–A8 offline, A9 sau merge).
- **KHÔNG viết cú pháp biểu thức Actions trong comment của `run`** — một cặp rỗng trong dòng chú thích từng làm cả tệp không hợp lệ, và dấu hiệu là một run mang **tên đường dẫn tệp, 0 job, `conclusion: failure`**, không phải một job đỏ.
- **KHÔNG viết `[skip` + `ci]` nguyên văn trong thông điệp commit**, kể cả khi trích dẫn (`t24` canh workflow, **không** canh commit sắp tạo — đây thuần là kỷ luật viết).
- **KHÔNG hạ tiêu chuẩn gate mà không khai**: M5 bắt buộc, không phải tuỳ chọn.
- **Xếp SAU #546** (Q5). Lý do cấu trúc, không phải lịch: #548 gỡ đúng lane CI mà #546 dùng để chứng minh bản vá của nó. Nghiệm thu của #546 phải xong **trước** khi #548 land.

**Điều kiện dừng:**

1. **Vượt 4 tệp hoặc 300 dòng thêm** ⇒ DỪNG, xin chủ kho khai ngoại lệ **TRƯỚC** khi đẩy.
2. **Cần chạm dòng nào khác của `docs/PROTOCOL_DA_PHIEN.md` ngoài một hàng `§20`** ⇒ DỪNG; đó là phát hiện về chính đặc tả, đi qua revision mới (§3.2).
3. **Cùng một hình dạng lỗi lặp lần thứ BA** ⇒ DỪNG, hỏi *"có nên làm việc này không"*, không hỏi *"vá thế nào"*.
4. **Chủ kho chưa gật riêng cho `docs/PROTOCOL_DA_PHIEN.md`** ⇒ **KHÔNG cấp lease**.

---

**ĐẶC TẢ KHÔNG PHẢI LEASE.** Đọc được tệp này không phải là được giao việc. Thứ cấp việc là Packet Issue kèm lease còn hiệu lực (`docs/PROTOCOL_DA_PHIEN.md` §3.2 và §4).
