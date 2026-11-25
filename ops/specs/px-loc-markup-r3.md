tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# PX-LOC-MARKUP r3 — `proxima-control` lọc khối `<ElicitationsGroup>` khỏi câu trả lời (đặc tả, thay r2)

## packet_id · packet_issue
- `packet_id`: `px-loc-markup`. Revision 3, generation 1. Role `executor` (Claude).
- `packet_issue`: #1529.

## nguon_cap_viec
- Đặc tả r2 `ops/specs/px-loc-markup-r2.md` (sha256 `5584a9f19b257de5e9896bc000e957945123d026305e3f7f23746ee783b91876`, duyệt
  `issuecomment-7172132991`), chưa land. r1: `631a8beb…` (commit `b01f3dd`).
- Review offline §8.3 trên ứng viên r2: lượt 2 `c4e9711` (4/5, `issuecomment-7172718120`), lượt 3 `86fc431` (1/3, `7173165528`),
  lượt 4 `8060930` (0/3, `7173867201`). Hai chuyển tiếp liên tiếp dưới 50% ⇒ dừng vòng vá (§12), mục sổ `7173867678`; lớp
  `markup-leak-test-loses-evidence` lặp cả sau khi đổi thiết kế ở lượt 3 (mục sổ `7173166115`) ⇒ E1.
- Chủ kho chọn A (đặc tả r3 theo đề xuất): https://github.com/ducthangho/tra-luat/issues/1529#issuecomment-7173910620.
- Lượt 1 trên ứng viên r1 `8a33ddb`: `7171976816`. Gốc việc #1457 r2 (hồ sơ có khối đính chính), đề xuất `issuecomment-7053599823`;
  Q1–Q8 chủ kho chốt 25-11-2026; tiền lệ cấu trúc `ops/specs/px-ask-r3.md`.

## r3 đổi gì so với r2 (gốc rễ: câu chữ của N1, `reportedModel`, M3)
1. **N1 thu hẹp thành hợp đồng đo được trên BẢN CÀI ĐẶT ĐƯỢC GIAO.** r2 đòi chứng minh nội dung đã bỏ không xuất hiện "ở bất kỳ trường,
   luồng hay bản ghi nào" — một mệnh đề phổ quát mà reviewer phá bằng đột biến **cố ý chuyển dữ liệu ra ngoài** trong chính mã module
   (ghi vào `mode`, gắn thuộc tính ETS, khoá JSON trùng, comment JSON). Không harness nào chứng minh được một cài đặt tuỳ ý KHÔNG làm thế.
   r3: harness khẳng định hành vi quan sát được của mã giao là đúng **trọn vẹn và tuyệt đối** (mục N1); đột biến cố ý chuyển dữ liệu ra
   ngoài thuộc phạm vi **review mã** (người review đọc diff), không thuộc harness.
2. **`reportedModel` chỉ trả khi giá trị nằm trong danh sách id mà CHÍNH lời gọi ấy nhận từ `GET /v1/models`** (so Ordinal); ngược lại
   `$null`. Bỏ phép kiểm "trông giống model id" của r2.
3. **M3 (ADR-0060):** mỗi vế chạy tập test bắt buộc của CHÍNH cây ấy; id chỉ ứng viên có xét theo N6 (đòi ứng viên 0 đỏ), nên M3(b) trên
   TOÀN tập đỏ của ứng viên tự thoả.
4. Hai ca cũ đổi kỳ vọng vì luật `reportedModel` mới (mục N3). Write set đổi đặc tả/lease/RESULTS sang r3.

## review_class
`sensitive` — mã PowerShell của skill chạy trên máy chủ kho/VM, cùng lớp với tiền lệ `px-ask-r3`.

## nang_tran
```yaml
nang_tran:
  ai_nang: ducthangho (chủ kho, thẩm quyền §2 protocol; quyết định ghi hộ issuecomment-7172063543)
  can_cu: >-
    git diff --numstat d0868db..8776803 (đo ~19:2xZ 25-11-2026): 8 tệp, 329 dòng thêm. Phần mã đúng 5 tệp của module
    (SKILL.md, ProximaControl.psm1, ProximaControl.psd1, ProximaControl.Tests.ps1, ProximaManifest.Tests.ps1, cộng 116 dòng);
    3 tệp còn lại là sổ sách bắt buộc của packet (đặc tả, lease, RESULTS). Tách mã ra nhiều packet sẽ tách hành vi khỏi ca test và
    khỏi phiên bản của nó; bỏ RESULTS khỏi kho vẫn còn 7 tệp.
  tran_cu: 6 tệp / 450 dòng thêm (ADR-0053)
  tran_moi: 8 tệp / 450 dòng thêm
```
Giữ nguyên quyết định nâng trần của r2 (`issuecomment-7172063543`); r3 không đổi số tệp (đặc tả/lease/RESULTS r3 thay bản r2 trên nhánh).
Đo ứng viên r2 cuối `8060930` (~20:16Z): 8 tệp, 395 dòng thêm.

## Số đo nền (đo 25-11-2026 ~18:40Z trên `origin/master` `d0868db`; không đổi so với r1)
- Câu trả lời đi qua đúng một chỗ: `Invoke-PxcAsk` (`.agents/skills/proxima-control/scripts/ProximaControl.psm1`), gán `answer` từ
  `choices[0].message.content` và trả kèm `answerTrust = 'untrusted_data'`.
- Hình dạng khối (ĐÚNG MỘT mẫu, lượt C3 chủ kho dán 20-11-2026; chỉ ghi cấu trúc): `<ElicitationsGroup message="…">`, bên trong các
  `<Elicitation label="…" query="…"/>`, đóng bằng `</ElicitationsGroup>`; không có dạng tự đóng của thẻ nhóm.
- `ModuleVersion` = `2.1.0`. Harness `ProximaControl.Tests.ps1`: 27 ca bắt buộc, counterexample `CX00`–`CX13`.
- CI không chạy harness này; container phiên web không có `pwsh` sẵn.
- Module không có trong `RELEASE_MANIFEST.json` ⇒ không tái sinh manifest.

## write_set
- `.agents/skills/proxima-control/scripts/ProximaControl.psm1`
- `.agents/skills/proxima-control/scripts/ProximaControl.psd1`
- `.agents/skills/proxima-control/SKILL.md`
- `.agents/skills/proxima-control/tests/ProximaControl.Tests.ps1`
- `.agents/skills/proxima-control/tests/ProximaManifest.Tests.ps1`
- `ops/specs/px-loc-markup-r3.md`
- `ops/leases/px-loc-markup-r3-g1-claude.yaml`
- `ops/acceptance/px-loc-markup/r3/RESULTS.md`

Đặc tả, lease và RESULTS của r1/r2 không có trong diff cuối của nhánh (gỡ khỏi nhánh trước push); bản cũ tra được qua commit và các
comment trên #1529.

## ngoai_pham_vi
- Chặn bằng mã các model `gemini:<biến thể>` khác `auto` (Q4: chỉ hướng dẫn trong `SKILL.md`).
- Lọc thẻ markup nào khác ngoài `ElicitationsGroup`/`Elicitation` (Q1), kể cả dạng tự đóng của thẻ nhóm (chưa quan sát; coi là thẻ hỏng).
- Sửa gateway Proxima. Đổi HTTP, timeout 300 s, nhật ký `px-active`, WhatIf, kiểm runtime, Remote, dịch vụ.
- Mọi lời gọi model thật; kiểm thật sau merge là revision riêng (Q7). Đồng bộ phiên bản module trên VM.

## muc_tieu
1. `ProximaControl.psm1` — trong `Invoke-PxcAsk`, khi `answer` là chuỗi, bỏ mọi khối hoàn chỉnh. Một khối hoàn chỉnh khi:
   - thẻ mở bắt đầu bằng `<ElicitationsGroup` (Ordinal), tên kết thúc ngay sau đó bằng khoảng trắng, `>`, `/` hoặc hết chuỗi;
   - thẻ mở kết thúc bằng `>` nằm ngoài dấu nháy kép, không gặp `<` ngoài dấu nháy trước đó, và ký tự trước `>` không phải `/`;
   - thẻ đóng `</ElicitationsGroup>` (Ordinal) đầu tiên sau `>` ấy đến trước bất kỳ thẻ mở `<ElicitationsGroup` nào khác.
   Khoảng trắng cuối chuỗi chỉ được cắt khi sau khối cuối cùng không còn gì ngoài khoảng trắng; khi ấy cắt mọi khoảng trắng ở cuối phần
   văn bản còn lại. Không đổi byte nào khác.
2. `ProximaControl.psm1` — gặp bất kỳ thẻ mở nào không thoả mục 1 (cụt, thiếu `>`, dấu nháy chưa đóng, tự đóng, thiếu thẻ đóng, lồng):
   **không** sửa `answer` chút nào, kể cả các khối hợp lệ đứng trước nó (Q2).
3. `ProximaControl.psm1` — `data` của kết quả `ask` thêm `answerMarkup` ∈ {`none`, `removed`, `unterminated`} và `answerMarkupRemoved`
   (`[int]` ≥ 0). Nội dung đã bỏ không được đưa vào kết quả, luồng hay bản ghi nào bởi mã giao (Q3); `answer` không phải chuỗi ⇒ `none`, 0.
   `reportedModel` = giá trị `model` của phản hồi **chỉ khi** nó là chuỗi bằng (Ordinal) một id trong danh sách `GET /v1/models` mà chính
   lời gọi `ask` ấy đã nhận; ngược lại `$null`.
4. `ProximaControl.psm1` — help của `px` nêu hai trường mới.
5. `ProximaControl.psd1` — `ModuleVersion` `2.1.0` → `2.2.0` (Q5).
6. `SKILL.md` — phiên bản 2.2.0; mô tả hai trường, luật cắt đuôi và luật `reportedModel` của mục 3; hướng dẫn chạy tự động với Gemini thì nên dùng `gemini:auto`, nêu
   căn cứ đúng mức: #1457 r2 là lời khai chưa xác minh, kể một lời gọi model chỉ định HTTP 500 vì luồng treo và một lời gọi
   `gemini:auto` trả được câu trả lời; không khẳng định cơ chế gateway hay nguồn gốc khối như sự thật đã đo; ghi hệ quả handshake Remote.
7. `ProximaManifest.Tests.ps1` — `$Want` và `CX04` theo 2.2.0.
8. `ProximaControl.Tests.ps1` — ca bắt buộc `X5-11` (27 → 28 id), `CX14`, `CX15`, `CX16`; đổi kỳ vọng `reportedModel` của `X5-01`, `X6-01` (mục `nghiem_thu`).
9. `ops/acceptance/px-loc-markup/r3/RESULTS.md` — biên nhận phép đo và chạy test Windows.
10. `ops/specs/px-loc-markup-r3.md`, `ops/leases/px-loc-markup-r3-g1-claude.yaml` — đặc tả này và lease.

## nghiem_thu
"Ca" = một id trong `$Ids` của harness; "CX" = một counterexample.

- **N1 (mục tiêu 1–3; hợp đồng trên bản cài đặt được giao)** — `X5-11` dựng phản hồi giả qua cơ chế HTTP giả của harness (không gateway
  thật), với các ca: không khối; một khối ở cuối (`OK`); hai khối (giữa và cuối); khối giữa câu, đuôi space + CRLF (giữ nguyên); khối giữa
  câu, đuôi NBSP (giữ nguyên); thẻ mở không có thẻ đóng; khối lồng; thẻ mở thiếu `>`; dấu nháy chưa đóng; thẻ nhóm tự đóng; tên
  `ElicitationsGroupX`; tên viết thường; văn bản giữ lại có marker riêng; `model` của phản hồi bằng nguyên khối; `model` bằng một nhãn của
  khối bị bỏ (chuỗi không được quảng bá); `model` là id được quảng bá. Với mỗi ca, so khớp TUYỆT ĐỐI:
  - **luồng:** khi bật verbose, debug, information, mọi luồng gộp lại có đúng MỘT đối tượng, là kết quả;
  - **kết quả:** đúng tập khoá cấp ngoài và của `data`; MỌI giá trị so Ordinal/kiểu với giá trị kỳ vọng, gồm `mode`, `targetFingerprint`
    (lấy từ `config` của cùng đích), `recordId` (giá trị mà bộ sinh id giả của ca trả ra), `answer` (chuỗi không mang thuộc tính mở
    rộng), `answerMarkup`, `answerMarkupRemoved` (`[int]`), `reportedModel`, `httpStatus`, `requestedModel`, `answerTrust`, `recordState`;
  - **journal:** sau khi dọn journal của ca, cây `results` của đích có đúng MỘT tệp, đường dẫn bằng bản ghi của `recordId`, và **byte** của
    tệp bằng đúng byte kỳ vọng dựng từ năm trường đã biết (không parse JSON để so).
  ĐỎ khi: một khoá/giá trị/byte lệch; thêm hay thiếu đối tượng trên luồng; thêm hay thiếu tệp journal; `CX14`/`CX15`/`CX16` (N2) làm ca đỏ
  với token có tên.
  **Ngoài phạm vi N1:** đột biến cố ý chuyển dữ liệu ra ngoài theo đường mà các khẳng định trên không quan sát được (ví dụ một tệp ngoài
  cây `results`, một biến toàn cục). Những đường ấy thuộc review mã: reviewer đọc diff của `ProximaControl.psm1` và báo nếu mã giao đưa
  nội dung đã bỏ đi đâu ngoài các bề mặt trên.
- **N2** — `CX14` (bỏ bước lọc) `credited` với token `X5-11:MARKUP_ANSWER[one block]`; `CX15` (so tên thẻ `OrdinalIgnoreCase`) với
  `X5-11:MARKUP_STATE[case variant]`; `CX16` (bỏ điều kiện "nằm trong danh sách quảng bá" của `reportedModel`) với
  `X5-11:MARKUP_REPORTED_MODEL[model is dropped label]`. ĐỎ khi một mutant sống.
- **N3** — 27 ca cũ vẫn đạt; `CX00`–`CX13` vẫn `credited`. Kỳ vọng được phép đổi, và chỉ đổi, ở hai ca do luật `reportedModel` mới:
  `X5-01` và `X6-01` — gateway giả trả `model` là một id được quảng bá trong chính ca ấy, kỳ vọng `reportedModel` bằng id đó. Mọi thay đổi
  khác ở ca cũ là vi phạm N3. ĐỎ khi một ca/CX cũ đổi màu, hoặc diff chạm ca cũ ngoài hai ca trên.
- **N4** — `ProximaManifest.Tests.ps1` đạt với `2.2.0`; ĐỎ khi để `.psd1` ở `2.1.0` (đột biến tay, ghi vào RESULTS).
- **N5 (mục tiêu 6)** — trên `SKILL.md` nối dòng theo từng đoạn: vế dương — có câu hướng dẫn dùng `gemini:auto` khi chạy tự động, có
  cụm "lời khai chưa xác minh" trong cùng đoạn ấy, có tên `answerMarkup` và `answerMarkupRemoved`; vế âm — không còn `2.1.0` ở frontmatter
  và ở mục *Phiên bản* (đếm từng vị trí). ĐỎ khi xoá câu hướng dẫn, xoá cụm lời khai, hay để lại `2.1.0`.
- **N6 (nền chạy) và M3 (ADR-0060)** — trên một máy Windows của chủ kho, dựng trong một lệnh hai cây: nền B (`base_sha` của lease r3) và
  ứng viên H (head của PR lúc chạy). **Mỗi vế chạy harness của chính cây ấy** (chép ra ngoài cây): `ProximaControl.Tests.ps1` với PS 7 và
  PS 5.1, mỗi bản `en-US` và `tr-TR`, `-Counterexamples` ở PS 7 `en-US`; `ProximaManifest.Tests.ps1` với PS 7 và PS 5.1. Báo cáo JSON
  lưu ngoài cây, băm ghi vào RESULTS.
  Đạt khi: (N6) mọi lượt của H rc 0, `passed == total`, mọi CX của H `credited`; (M3a) đủ lượt ở cả hai vế, không lỗi setup, không ca bắt
  buộc `skipped`/`not_run`/`NOT_EXECUTED` ở vế nào; (M3b) tập id đỏ của H ⊆ tập id đỏ của B — với H 0 đỏ theo N6 thì điều này đúng trên
  toàn tập; (M3c) H có ca đỏ thuộc write set thì chủ kho quyết. Id chỉ H có (`X5-11`, `CX14`–`CX16`) không có lượt B theo nghĩa của
  chính cây B; chúng được xét theo N6. ĐỎ khi thiếu lượt nào hoặc một điều kiện trên sai.
- **N7 (gate kho)** — `python3 scripts/tl.py --selftest` N/N, `git diff --check` sạch, `ops/lease_publish.py check` rc 0 cho lease r3.
- **N8 (phạm vi và trần)** — `git diff --name-only <base>..<H>` ⊆ `write_set` và `git diff --numstat` ≤ 8 tệp / ≤ 450 dòng thêm
  (`tran_moi`). ĐỎ khi có đường dẫn ngoài danh sách hoặc vượt `tran_moi`.

Windows M3 (ADR-0060): `required`; N6 là lượt Windows của packet.

## luat_dung
- Điểm dừng của `docs/PROTOCOL_DA_PHIEN.md` §12 — dẫn, không chép. Lịch sử lớp ở `hinh_dang_ke_thua`; r3 KHÔNG reset bộ đếm.
- Trần lời gọi Codex theo dòng khai `ADR-0055`; đã dùng 4 (offline lượt 1–4). Chạm trần mà cần thêm ⇒ **E2**.
- Trần kích thước theo `nang_tran`; vượt `tran_moi` ⇒ **E2**.
- Máy Windows của chủ kho không sẵn sàng cho N6 ⇒ **E2**, mang theo ma trận lượt còn thiếu.
- Mẫu thật mâu thuẫn Q1–Q8 ⇒ **E3**, mang theo mẫu đã che.
- Lease r3 chỉ cấp khi `ai-dang-giu` ra 0 cho cả write set r3: tức sau khi lease r2 (`px-loc-markup-r2-g1-claude`, chưa push) hết hạn lúc
  2026-11-25T23:28:04Z, hoặc sớm hơn nếu chủ kho chỉ thị rút hạn (khối `thu_hoi_bang_rut_han`). Không bia mộ.

## pham_vi_e
Không chạm E4, không chạm E5. Packet không thuộc Mission đã duyệt hướng ⇒ đặc tả chờ chủ kho duyệt băm trước khi cấp lease.

## hinh_dang_ke_thua
Số lượt review mà mỗi lớp xuất hiện (lượt 1 trên `8a33ddb`, lượt 2 `c4e9711`, lượt 3 `86fc431`, lượt 4 `8060930`):
- `markup-leak-test-loses-evidence`: **4** (L1–L4), còn mở — vá lặp ba lần rồi đổi thiết kế ở L3, vẫn mở ở L4 ⇒ gốc ở N1, r3 đổi N1.
- `windows-m3-baseline-omitted`: **3** (L2–L4), còn mở — r3 đổi N6/M3.
- `markup-echo-in-reported-model`: **2** (L3–L4), còn mở — r3 đổi luật `reportedModel`.
- Đã đóng: `markup-trims-unrelated-tail` (1, L1), `markup-pairs-incomplete-opener` (1, L1), `runtime-claims-exceed-evidence` (1, L1),
  `sensitive-diff-exceeds-file-cap` (1, L1), `lease-expiry-prerequisite-stale` (1, L2). L4 xác nhận không lớp đã đóng nào mở lại.
Tỷ lệ §12 theo chuyển tiếp: L1→L2 4/5, L2→L3 1/3, L3→L4 0/3. Lượt review đầu của r3 là chuyển tiếp thứ ba tính từ L2; nếu lại dưới 50%
thì §12 dừng lần nữa.

## chua_do_duoc
- Biến thể khác của khối `ElicitationsGroup`: **KHÔNG ĐO ĐƯỢC** — một mẫu, phản hồi thô của gateway không được lưu.
- Markup khác trong câu trả lời Gemini: **KHÔNG ĐO ĐƯỢC** trong r3.
- Hành vi trên gateway thật sau khi lọc: chỉ đo ở revision kiểm thật sau merge (Q7).
- Trạng thái đăng nhập Google của gateway lúc thi hành: không đo.
