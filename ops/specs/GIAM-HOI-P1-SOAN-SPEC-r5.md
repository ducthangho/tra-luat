# GIAM-HOI-P1-SOAN-SPEC r5 — skill soan-spec mặc định dòng khai ADR-0055, cấm ngân sách mềm, luật dừng E1–E3; cột cổng ở §20

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

| trường | giá trị |
|---|---|
| packet_id | `GIAM-HOI-P1-SOAN-SPEC`, revision 5, generation 1. Lease khai đúng `packet_id: GIAM-HOI-P1-SOAN-SPEC` và `revision: 5`: tiêu đề H1 của tệp này là khai báo định danh theo grammar của `ADR-0063` (mục 11). Thay r4 (sha256 `e1b565548b82e1c00fb65b04a61c84845c98957398c8471000aa805b60fbd25b`, được review lượt 6 approve kèm một P3), r3 (sha256 `b8d86a204b369d9e53ccc1fa50aee883cf494dacb352081b5bf19d5614092dbc`, được review lượt 4 approve), r2 (sha256 `6d2c9c667b4f08f102643fe493bef24f84b943e799b2943e6d0e90d9b9c5def8`) và r1 (sha256 `ff2ff8d222d6817d3d39012a7e55c9eb5761ff4030f92e92f7cbb11990595cf1`), không bản nào được chủ kho duyệt; thay đổi ở mục 12 tới 15 |
| packet_issue | chưa tạo. Issue trỏ đặc tả này bằng `spec_hash`; đặc tả không ghi số Issue để băm không phụ thuộc thứ tự tạo Issue. Nháp thân Issue nằm ngoài tệp này |
| mission | lộ trình "Giảm việc hỏi chủ kho", packet 1/5. Chưa có Mission Issue |
| nguon_cap_viec | Chủ kho đồng ý cả năm khuyến nghị của tài liệu https://claude.ai/artifact/6JUF8DsbHxfN5GjsbdAtHT ("Giảm việc hỏi chủ kho") trong phiên chat ngày 08-11-2026, nguyên văn: *"Bạn làm hộ cho tôi luôn. TÔi đồng ý duyệt 5 điểm và chốt nâng trần theo đề xuất"*. Packet này là mục 1 của phần *Lộ trình* trong tài liệu ấy. Ba mã E1–E3 là chỉ đạo của chủ kho ngày 07-11-2026: *"chỉ hỏi những vấn đề thực sự quan trọng như hướng đi bế tắc, không đủ tài nguyên để chạy, hoặc có phát hiện đảo ngược chỉ đạo của tôi"* (chép ở `ops/specs/THU-HOI-ADMISSION-MERGE-BASE-A-r13.md` trên `master`) |
| review_class | `sensitive`. Bộ phân lớp `ops/lease_publish.py` (`_BANG_LOP` dòng 59–67, `_tinh_lop_tu_write_set` dòng 360–382) trả `sensitive` cho mọi đường dẫn không có trong bảng, gồm cả hai tệp của write set |
| base | `origin/master` lúc cấp lease. Soạn trên `e3c639be40dba644ecbf9d729d72837691f59ff4` (đo 10:30Z 08-11-2026) |
| executor | `google_antigravity` (Antigravity, model `4.0 argon`), theo chỉ đạo chủ kho ngày 08-11-2026 vì quota Claude sắp hết. Lease và evidence lượt chạy khai `provider: google_antigravity`, `execution_surface: antigravity`, `transport: machine/local` và `model_family` của model thực chạy, đo ở lượt chạy chứ không suy từ tên model hay tên ứng dụng (đầu protocol); thiếu một trong ba thuộc tính ấy thì lượt chạy dừng. Môi trường `local`. Adapter `.agents/skills/work-packet/SKILL.md` chỉ được dùng lại phần cú pháp PowerShell: identity của lượt chạy và các đối số provider của `packet_loop.py init`, `begin-attempt` lấy từ lease Antigravity, không chép giá trị Claude hay Codex trong ví dụ của adapter ấy |
| reviewer | `codex` offline qua `.claude/dev/launcher.py run` trên commit cục bộ (`ADR-0060` M12), cộng connector `@codex review` trên PR draft (`ADR-0060` M6). Reviewer Codex là họ `openai`: nếu `model_family` đo được của lượt thi công cũng là `openai` thì review Codex không cho `cross_approved` (protocol §8) và `packet_loop.py init` từ chối cặp executor và reviewer cùng họ, nên reviewer phải đổi sang một họ khác, định tuyến xong trước `init`; không ghi tay state để vượt chốt ấy |
| luật merge | `ADR-0060`, mặc định theo `ADR-0062` |
| windows | `not_required`: mọi tệp của diff là `*.md` (`ADR-0060` M3 bước 3) |
| full_mutant_audit | không áp: diff không chạm `.claude/dev/**`, `ops/**/*.py`, `.github/workflows/**` (`ADR-0060` M9) |
| packet anh em | `GIAM-HOI-P2-ADR-E1-E5` (đặc tả `ops/specs/GIAM-HOI-P2-ADR-E1-E5-r8.md`). Hai packet cùng sửa `docs/PROTOCOL_DA_PHIEN.md` và `.claude/skills/soan-spec/SKILL.md`, nên chạy tuần tự: packet này trước, packet 2 lấy base chứa commit land của packet này |

## 1. Vì sao — số đo

Đo trên `origin/master` `e3c639b` lúc 10:30Z 08-11-2026, trừ chỗ ghi khác.

| # | sự kiện | số đo |
|---|---|---|
| S1 | trần lời gọi Codex mặc định là hai | `.claude/dev/packet_loop.py:60` `MAC_DINH_TRAN_CODEX = 2`. Bảng ở mục *Hiệu lực* của `ADR-0055`: đặc tả không có dòng khai `ADR-0055` và không có dòng `ADR-0052` hợp lệ thì trần là hai. Skill `soan-spec` §3 (dòng 131–141) chỉ nói *"đặc tả muốn áp trần … thì khai"*, không đặt dòng khai làm mặc định, và trỏ trần lời gọi về `ADR-0052` (tám) |
| S2 | dòng khai `ADR-0055` hợp lệ | OID `d2e3052d479d140b7e7b91df41ec4914fab7d544` (merge PR #926): `git cat-file -e <L>:docs/adr/0055-tran-loi-goi-codex-len-muoi.md` rc 0; cùng lệnh với `<L>^1` rc 128; `<L>` có trong `git rev-list --first-parent origin/master`; clone không shallow. 72 trong 581 tệp `ops/specs/` có dòng khai này ở đầu dòng |
| S3 | dòng khai `ADR-0053` hợp lệ | OID `8ab100793df9831505f495543a74044b91c2c9ab` (merge PR #791) qua đủ ba phép đo trên với `docs/adr/0053-tran-kich-thuoc-sensitive-len-sau-tep.md` |
| S4 | mẫu "ngân sách mềm" | Đếm tệp: 0 tệp trong `.claude/`, `docs/`, `CLAUDE.md`, `AGENTS.md`, `.agents/` có cụm "ngân sách mềm"; 36 trong 581 tệp `ops/specs/` có cụm ấy (kể cả câu phủ định "không có ngân sách mềm"); 18 tệp có cụm ấy theo sau là một chữ số trong vòng 12 ký tự; 26 tệp có cụm "liên tiếp chưa approve". Không ADR, protocol hay skill nào đặt ra mẫu này, nên **không có dòng nào để xoá**: thứ cần làm là thêm một luật cấm vào skill |
| S5 | "hỏi chủ kho" trong đặc tả | 173 trong 581 tệp `ops/specs/` có cụm này (không phân biệt hoa thường, kể cả câu phủ định) |
| S6 | cột cổng ở §20 đã cũ | Bảng §20 mục A ghi **0 cổng** cho `ADR-0037`, `ADR-0038`, `ADR-0043`, `ADR-0048`. Đo trên mã: `ADR-0037` có `record-codex-call`, `record-review`, `record-rescue` (`.claude/dev/packet_loop.py` dòng 697–702, 1296–1345, 3050–3074); `ADR-0043` có `TRUC_TRAN` và `nang-tran` (dòng 56–62, 1315–1326); `ADR-0048` có `MAC_DINH_TRAN_VONG_REVIEW = 10` (dòng 59); `ADR-0038` có `_kiem_lop_review` trong `ops/lease_publish.py` (dòng 385–420, từ commit `67a7fbe`) |
| S7 | `ADR-0038` không có cổng trong `packet_loop.py` | Lời giao việc nói cổng của bốn ADR nằm trong `.claude/dev/packet_loop.py`. Đo: `review_class` và `systemic` xuất hiện 0 lần ở `.claude/dev/packet_loop.py`, `.claude/dev/launcher.py`, `.claude/dev/gate_lifecycle.py`, `.github/workflows/ci.yml`, `.github/workflows/ops-publish-lease.yml`; `ops/lease_publish.py` có `review_class` 3 lần, `systemic` 1 lần. Dòng `ADR-0038` mới ghi cổng ở `ops/lease_publish.py` |
| S8 | câu đầu `ADR-0037` | *"khi đã dùng hết hai lượt Codex"* (dòng 5). Dòng §20 hiện nói con số đã bị `ADR-0052` thay nhưng không nhắc `ADR-0055`, và không nói đặc tả thiếu dòng khai thì trần vẫn là hai |
| S9 | người đang giữ write set | `python ops/lease_publish.py ai-dang-giu` trên clone đủ 745 nhánh máy chủ (đã so tập tên với `git ls-remote --heads`): `.claude/skills/soan-spec/SKILL.md` 0 người giữ (10:37Z). `docs/PROTOCOL_DA_PHIEN.md`: lượt quét đầu ra 0 người giữ; fetch lại rồi quét (10:4xZ) ra `NGƯỜI_GIỮ 1: wp1174-r17-g14-codex` (nhánh `ops/wp1174-r17-g14-lease`, commit `ccc1c3a`, cấp 10:36Z, `lease_until` 18:03:01Z 08-11-2026). PR #1275 (wp1174) và packet #1265 (`ADR-0066`) cũng sửa tệp này. Lease của packet này chỉ cấp được khi `ai-dang-giu` cho tệp ấy ra 0 người giữ; đo lại ngay trước khi cấp |

## 2. Thay đổi

Mỗi thay đổi là một cặp khối `cu`/`moi`. Khối `cu` là nguyên văn trên base, tính cả ký tự xuống dòng cuối; khối `moi`
là thứ thay vào, đúng từng byte, kể cả chỗ ngắt dòng. Mỗi khối `cu` xuất hiện đúng một lần trong tệp của nó trên base.
Vị từ ở §4 đọc chính các khối này, nên văn bản chỉ có một nguồn là tệp đặc tả.

**M1 → `.claude/skills/soan-spec/SKILL.md` §3.** Trỏ trần lời gọi về `ADR-0055` và đặt dòng khai `ADR-0055` làm mặc định
cho mọi đặc tả mới, kèm OID land đã đo.

~~~ thay SKILL S1 cu
- kích thước dự kiến (`git diff --numstat` trên phạm vi tương đương gần nhất) — đối chiếu
  ngưỡng thường ở `docs/adr/0044-nguong-kich-thuoc-packet-theo-do-luong.md`; packet `sensitive`
  đối chiếu cặp số ở `docs/adr/0053-tran-kich-thuoc-sensitive-len-sau-tep.md`; số lời gọi Codex
  review dự kiến đối chiếu trần ở `docs/adr/0052-tran-loi-goi-codex-len-tam.md`. Skill này
  không chép ngưỡng; đặc tả ghi số đo, trần hay khối vượt trần (`nang_tran`) theo đúng dạng ADR
  tương ứng quy định. Đặc tả muốn áp trần của `ADR-0052`/`ADR-0053` thì khai dòng `tran_*` theo
  mục *Hiệu lực* của chính ADR ấy — giá trị sau `@` là OID 40 ký tự của commit LAND ADR trên nhánh
  mặc định, không phải một commit bất kỳ có chứa ADR (base của packet chứa ADR mà không phải
  commit land). Hai dạng khai, mỗi dòng đứng riêng ở đầu đặc tả, `<OID land>` thay bằng OID thật:
  `tran_loi_goi_codex: ADR-0052@<OID land>` và `tran_kich_thuoc_sensitive: ADR-0053@<OID land>`.
  ADR nào đang hiệu lực thì hỏi bảng định tuyến ADR của `docs/PROTOCOL_DA_PHIEN.md`;
~~~

~~~ thay SKILL S1 moi
- kích thước dự kiến (`git diff --numstat` trên phạm vi tương đương gần nhất) — đối chiếu
  ngưỡng thường ở `docs/adr/0044-nguong-kich-thuoc-packet-theo-do-luong.md`; packet `sensitive`
  đối chiếu cặp số ở `docs/adr/0053-tran-kich-thuoc-sensitive-len-sau-tep.md`; số lời gọi Codex
  review dự kiến đối chiếu trần ở `docs/adr/0055-tran-loi-goi-codex-len-muoi.md`. Skill này
  không chép ngưỡng; đặc tả ghi số đo, trần hay khối vượt trần (`nang_tran`) theo đúng dạng ADR
  tương ứng quy định;
- dòng khai trần: **mọi đặc tả mới đều có dòng khai của `ADR-0055`**, đứng riêng một dòng ở đầu tệp:
  `tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544`
  OID ấy là commit land `ADR-0055` trên nhánh mặc định (merge PR #926). Trước khi đóng băng, chạy lại
  ba phép đo ở mục *Hiệu lực* của `ADR-0055`. Trần lời gọi do bảng ở mục ấy chọn theo các dòng khai
  của đặc tả: thiếu dòng này thì `ADR-0055` không áp và trần theo luật của `ADR-0052`, thấp hơn trần
  của `ADR-0055`, nên trần chạm sớm hơn và mỗi lần chạm là một lần hỏi chủ kho. Đừng thêm dòng
  `ADR-0052` cạnh dòng `ADR-0055`: bảng ấy chọn trần thấp hơn khi có cả hai. Skill này không chép con
  số của bảng. Packet `sensitive` khai thêm dòng của `ADR-0053`:
  `tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab`
  Giá trị sau `@` luôn là OID 40 ký tự của commit LAND ADR trên nhánh mặc định, không phải một commit
  bất kỳ có chứa ADR (base của packet chứa ADR mà không phải commit land). ADR nào đang hiệu lực thì
  hỏi bảng định tuyến ADR của `docs/PROTOCOL_DA_PHIEN.md`;
~~~

**M2 → `.claude/skills/soan-spec/SKILL.md` §2.** Thêm luật L7 ngay trước `## 3`, và đổi tiêu đề §2 từ sáu thành bảy luật.

~~~ thay SKILL S2 cu
## 2. Sáu luật riêng của kho — chúng sinh ra từ những lần đã trả giá
~~~

~~~ thay SKILL S2 moi
## 2. Bảy luật riêng của kho — chúng sinh ra từ những lần đã trả giá
~~~

~~~ thay SKILL S3 cu
## 3. Đo trước khi hỏi
~~~

~~~ thay SKILL S3 moi
**L7 — Đặc tả không tự đặt điểm hỏi chủ kho.** Một mẫu đã lan từ đặc tả này sang đặc tả khác mà
không ADR, protocol hay skill nào đặt ra: "ngân sách mềm N lời gọi; hai lượt liên tiếp chưa approve ⇒
Review Rescue Checkpoint". Đo 08-11-2026 trên `origin/master` `e3c639b`, đếm tệp trong 581 tệp của
`ops/specs/`: 26 tệp có cụm "liên tiếp chưa approve", 173 tệp có cụm "hỏi chủ kho" (kể cả câu phủ
định). Mỗi điểm hỏi tự đặt là một lần chủ kho phải dừng việc để trả lời.

- **Không khai ngân sách mềm** dưới trần của dòng khai, và không đặt luật kiểu "N lượt liên tiếp chưa
  approve thì dừng hay hỏi chủ kho". Mức dành sẵn của `ADR-0041` là ngân sách giữ trước, không phải
  trần hay điểm dừng. Lượt thứ hai trở đi theo điều kiện của `ADR-0052` và không cần hỏi ai.
- **Mục `luat_dung` chỉ có hai loại dòng.** (i) Điểm dừng mà protocol hay một ADR đang hiệu lực đã
  đặt: dẫn bằng tên mục hay ADR, không chép lại, không hạ ngưỡng. (ii) Một trong ba mã dưới đây, kèm
  thứ phải mang theo khi hỏi:
  - **E1 — hướng đi bế tắc:** đã xét lại cách làm mà không còn phương án nào có phép đo chống đỡ.
    Mang theo gốc rễ, các phương án đã thử và vì sao hỏng, một đề xuất.
  - **E2 — thiếu tài nguyên:** chạm trần cứng, hoặc thiếu máy, quota hay quyền. Mang theo mức đã
    dùng, còn thiếu bao nhiêu, để làm gì.
  - **E3 — phát hiện đảo ngược chỉ đạo:** bằng chứng mâu thuẫn với một quyết định của chủ kho. Mang
    theo quyết định nào, bằng chứng, hậu quả nếu giữ nguyên.
- **Câu nào trong đặc tả nói tới việc hỏi, báo hay chờ chủ kho thì phải mang một mã E.** Điểm dừng
  loại (i) chỉ dừng phiên; khi nó cần chủ kho quyết thì câu hỏi ấy cũng mang mã, thường là E2 vì quyền
  quyết thuộc chủ kho (chạm trần cứng, việc protocol giao chủ kho duyệt). Không gắn được mã nào thì đó
  không phải điểm hỏi: phiên đang giữ việc tự quyết, rồi ghi gốc rễ, phương án chọn và phép đo chống đỡ
  vào revision kế tiếp hay handoff.

Ba mã lấy từ chỉ đạo của chủ kho ngày 07-11-2026, được chủ kho đồng ý thành danh sách ngày 08-11-2026
(quyết định số 1 của tài liệu "Giảm việc hỏi chủ kho"). Khi ADR của danh sách đóng land, định nghĩa
chuyển về ADR ấy và mục này chỉ còn con trỏ.

## 3. Đo trước khi hỏi
~~~

**M3 → `.claude/skills/soan-spec/SKILL.md` §4.** Thêm hai hàng vào bảng các mục bắt buộc, ngay sau hàng `nghiem_thu`.

~~~ thay SKILL S4 cu
| `nghiem_thu` | mỗi mục tiêu ≥1 tiêu chí, mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3) |
~~~

~~~ thay SKILL S4 moi
| `nghiem_thu` | mỗi mục tiêu ≥1 tiêu chí, mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3) |
| `tran_*` | dòng khai trần ở đầu tệp theo mục 3; mặc định có dòng của `ADR-0055` |
| `luat_dung` | điểm dừng của protocol hay ADR dẫn bằng tên, và mã E1–E3 theo L7; không có ngân sách mềm |
~~~

**M4 → `docs/PROTOCOL_DA_PHIEN.md` §20 mục A.** Thay bốn dòng bảng. Dòng `ADR-0037` ghi rõ con số "hai lượt" đã bị thay
và trần do bảng của `ADR-0055` chọn, không chép con số của bảng; cột cổng của cả bốn dòng ghi cổng đo được, kèm
ngày đo và commit.

~~~ thay PROTOCOL P37 cu
| `ADR-0037` | Review Rescue Checkpoint và tách Stable Slice | Accepted — con số lượt Codex của nó **đã bị thay** bởi `ADR-0052` (2026-10-16) | **0 cổng** |
~~~

~~~ thay PROTOCOL P37 moi
| `ADR-0037` | Review Rescue Checkpoint và tách Stable Slice | Accepted — câu đầu ghi *"hai lượt Codex"*; con số ấy **đã bị thay** bởi `ADR-0052` (2026-10-16) rồi `ADR-0055` (2026-10-25). Trần lời gọi do dòng khai của đặc tả chọn theo bảng ở mục *Hiệu lực* của `ADR-0055`, kể cả khi đặc tả không khai dòng nào; đừng chép *"hai lượt"* vào đặc tả mới | `packet_loop.py`: `record-codex-call` và `record-review` đưa packet về `blocked` với `ly_do: rescue_required` (`RC_TRAN`) khi chạm trần trục; `record-rescue` là cửa ra duy nhất và chỉ mở lại khi có bản ghi `nang_tran` khớp trần mới. Trần trong state do lệnh `init` nhận (hằng `MAC_DINH_TRAN_CODEX` khi không truyền); không gì đọc dòng khai của đặc tả. Tách Stable Slice: **0 cổng**. Đo 08-11-2026 trên `e3c639b` |
~~~

~~~ thay PROTOCOL P38 cu
| `ADR-0038` | Review Class fail-closed và phân bổ quota Codex | Accepted — điều kiện cấp *"lượt hai"* của `systemic` **đã mở rộng** sang mọi lượt sau lượt đầu, mọi class, bởi `ADR-0052` (2026-10-16) | **0 cổng** — `review_class` khai 10/49 lease |
~~~

~~~ thay PROTOCOL P38 moi
| `ADR-0038` | Review Class fail-closed và phân bổ quota Codex | Accepted — điều kiện cấp *"lượt hai"* của `systemic` **đã mở rộng** sang mọi lượt sau lượt đầu, mọi class, bởi `ADR-0052` (2026-10-16) | `ops/lease_publish.py` `_kiem_lop_review`, cho lease `schema_version` từ 2: `effective_review_class` phải bằng lớp cao hơn giữa lớp khai và lớp tính từ write set; đường dẫn ngoài `_BANG_LOP`, write set rỗng hay không đọc được đều thành `sensitive`; lệch thì `RC_LOP`. `packet_loop.py` không đọc lớp review. Phân bổ quota Codex theo class: **0 cổng**. Đo 08-11-2026 trên `e3c639b` |
~~~

~~~ thay PROTOCOL P43 cu
| `ADR-0043` | Trần vòng review canon là HAI, và nó chỉ có một chỗ ở | Accepted — con số trục VÒNG **đã bị thay** bởi `ADR-0048` (2026-09-12); ba trục, trần độc lập, `nang_tran` và luật một-chỗ-ở vẫn hiệu lực | **0 cổng** — `so-canon` chưa tồn tại |
~~~

~~~ thay PROTOCOL P43 moi
| `ADR-0043` | Trần vòng review canon là HAI, và nó chỉ có một chỗ ở | Accepted — con số trục VÒNG **đã bị thay** bởi `ADR-0048` (2026-09-12); ba trục, trần độc lập, `nang_tran` và luật một-chỗ-ở vẫn hiệu lực | `packet_loop.py`: trục VÒNG và trục LỜI GỌI có bộ đếm và trần riêng trong state (`TRUC_TRAN`), trục ATTEMPT có trần riêng; `nang-tran` chỉ nhận `--ai-nang` thuộc `NGUOI_CO_THAM_QUYEN`, `--can-cu` là URL comment GitHub và trần mới lớn hơn trần cũ. Câu *"không có khối ấy thì cổng đăng lease từ chối"*: **0 cổng**, `ops/lease_publish.py` không đọc `nang_tran`. `so-canon` chưa tồn tại. Đo 08-11-2026 trên `e3c639b` |
~~~

~~~ thay PROTOCOL P48 cu
| `ADR-0048` | Trần trục VÒNG nâng theo chỉ thị chủ kho 12-09-2026, thay số của `ADR-0043`; hiệu lực neo theo `spec_hash` đóng băng, không hồi tố | Accepted | **0 cổng** — `so-canon` vẫn chưa tồn tại (nợ cùng tên) |
~~~

~~~ thay PROTOCOL P48 moi
| `ADR-0048` | Trần trục VÒNG nâng theo chỉ thị chủ kho 12-09-2026, thay số của `ADR-0043`; hiệu lực neo theo `spec_hash` đóng băng, không hồi tố | Accepted | `packet_loop.py`: trần vòng mặc định `MAC_DINH_TRAN_VONG_REVIEW = 10`, đổi được qua `init --review-rounds-limit`; `record-review` đưa packet về `rescue_required` khi trần vòng đã chạm. Không gì đọc `spec_hash` để chọn trần; `so-canon` vẫn chưa tồn tại (nợ cùng tên). Đo 08-11-2026 trên `e3c639b` |
~~~

## 3. Write set

```yaml
write_set:
  - .claude/skills/soan-spec/SKILL.md
  - docs/PROTOCOL_DA_PHIEN.md
```

Diff PR: đúng **2 tệp**. Đo trên ứng viên dựng từ các khối ở §2 trên base `0166d30`: `SKILL.md` thêm 45 dòng, bớt 8;
`PROTOCOL_DA_PHIEN.md` thêm 4, bớt 4.
Trần `ADR-0053` cho packet `sensitive` (≤ 6 tệp, ≤ 450 dòng thêm): **đạt**. Hai tệp không nằm trong
`RELEASE_MANIFEST.json` (đo trên `e3c639b`: 184 mục, không có `.claude/**` hay `docs/**`), nên không tái sinh manifest.
Handoff theo protocol §7 đăng thành comment trên Packet Issue, không thành tệp trong kho. Không sửa `VERSION`,
`CHANGELOG.md`, `changelog.d/`.

## 4. Nghiệm thu

Vị từ có một dạng duy nhất là script dưới đây. Người đo chép nó ra thư mục tạm (không đưa vào kho), rồi chạy ở gốc
một clone không shallow của ứng viên, sau `git fetch origin`:

```
python kiem_p1.py ops/specs/GIAM-HOI-P1-SOAN-SPEC-r5.md <OID base>
```

`ops/specs/GIAM-HOI-P1-SOAN-SPEC-r5.md` là bản đặc tả đúng băm trong lease, đọc từ ref/OID do lease chỉ. Mã thoát: 0 ĐẠT,
1 ĐỎ, 3 KHÔNG ĐO ĐƯỢC. KHÔNG ĐO ĐƯỢC không phải ĐẠT.

```python
# kiem_p1.py: vị từ nghiệm thu của GIAM-HOI-P1-SOAN-SPEC r5.
# Ứng viên là commit HEAD của checkout hiện tại; base là đối số thứ hai.
import re
import subprocess
import sys

TEP = {"SKILL": ".claude/skills/soan-spec/SKILL.md", "PROTOCOL": "docs/PROTOCOL_DA_PHIEN.md"}
DONG_KHAI = {
    "docs/adr/0055-tran-loi-goi-codex-len-muoi.md":
        "tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544",
    "docs/adr/0053-tran-kich-thuoc-sensitive-len-sau-tep.md":
        "tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab",
}


def git(*doi_so, rc_nhan=(0,)):
    p = subprocess.run(["git", *doi_so], capture_output=True)
    if p.returncode not in rc_nhan:
        loi = p.stderr.decode("utf-8", "replace").strip()
        raise LookupError(f"git {' '.join(doi_so)} rc={p.returncode}: {loi}")
    return p


def doc_tep(rev, duong):
    return git("show", f"{rev}:{duong}").stdout.decode("utf-8")


def cac_khoi(van_ban):
    """{(tệp, mã): {"cu": ..., "moi": ...}} từ các khối `~~~ thay <tệp> <mã> <cu|moi>`."""
    ket_qua, dang_mo, dem = {}, None, []
    for dong in van_ban.splitlines(keepends=True):
        if dang_mo is None:
            m = re.fullmatch(r"~~~ thay (SKILL|PROTOCOL) (\S+) (cu|moi)\n", dong)
            if m:
                dang_mo, dem = m.groups(), []
        elif dong == "~~~\n":
            tep, ma, loai = dang_mo
            muc = ket_qua.setdefault((tep, ma), {})
            if loai in muc:
                raise LookupError(f"khối trùng: {dang_mo}")
            muc[loai] = "".join(dem)
            dang_mo = None
        else:
            dem.append(dong)
    if dang_mo is not None or not ket_qua or any(set(v) != {"cu", "moi"} for v in ket_qua.values()):
        raise LookupError("khối thay bị hở, rỗng hoặc thiếu cặp cu/moi")
    return ket_qua


def ky_vong(goc, cap):
    """Thay từng khối `cu` (đúng một lần trên base) bằng `moi`, theo vị trí trên base."""
    vi_tri = []
    for ma, v in cap:
        so_lan = goc.count(v["cu"])
        if so_lan != 1:
            raise LookupError(f"{ma}: khối cu có {so_lan} lần trên base, cần đúng 1")
        dau = goc.index(v["cu"])
        vi_tri.append((dau, dau + len(v["cu"]), v["moi"]))
    vi_tri.sort()
    for (_, cuoi, _), (dau_sau, _, _) in zip(vi_tri, vi_tri[1:]):
        if dau_sau < cuoi:
            raise LookupError("hai khối cu chồng nhau")
    phan, con_tro = [], 0
    for dau, cuoi, moi in vi_tri:
        phan += [goc[con_tro:dau], moi]
        con_tro = cuoi
    return "".join(phan) + goc[con_tro:]


def main():
    duong_spec, base = sys.argv[1], sys.argv[2]
    try:
        with open(duong_spec, "rb") as f:
            byte_spec = f.read()
    except OSError as e:
        raise LookupError(f"không đọc được tệp đặc tả: {e}") from None
    if b"\r" in byte_spec:
        raise LookupError("đặc tả có ký tự CR; K1 của ADR-0063 chỉ nhận LF")
    khoi = cac_khoi(byte_spec.decode("utf-8"))
    loi = []
    for ten, duong in TEP.items():
        cap = sorted((ma, v) for (t, ma), v in khoi.items() if t == ten)
        if not cap:
            raise LookupError(f"không có khối nào cho {ten}")
        if doc_tep("HEAD", duong) != ky_vong(doc_tep(base, duong), cap):
            loi.append(f"{duong} khác bản kỳ vọng dựng từ base")
    doi = set(git("diff", "--name-only", base, "HEAD").stdout.decode("utf-8").split())
    if doi != set(TEP.values()):
        loi.append(f"tập tệp đổi {sorted(doi)} khác write set")
    if git("rev-parse", "--is-shallow-repository").stdout.strip() != b"false":
        raise LookupError("clone shallow")
    first_parent = set(git("rev-list", "--first-parent", "origin/master").stdout.decode().split())
    skill = doc_tep("HEAD", TEP["SKILL"])
    for adr, dong_khai in DONG_KHAI.items():
        so_dong = sum(1 for d in skill.splitlines() if dong_khai in d)
        if so_dong != 1:
            loi.append(f"{dong_khai!r} nằm trên {so_dong} dòng của SKILL.md, cần 1")
        oid = dong_khai.rsplit("@", 1)[1]
        co_adr = git("cat-file", "-e", f"{oid}:{adr}", rc_nhan=(0, 1, 128)).returncode == 0
        cha_co_adr = git("cat-file", "-e", f"{oid}^1:{adr}", rc_nhan=(0, 1, 128)).returncode == 0
        if not co_adr or cha_co_adr or oid not in first_parent:
            loi.append(f"{oid} không qua ba phép đo land của {adr}")
    for x in loi:
        print("ĐỎ:", x)
    print("ĐẠT" if not loi else f"ĐỎ: {len(loi)} lỗi")
    return 1 if loi else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        sys.exit(main())
    except (LookupError, IndexError, UnicodeDecodeError) as e:
        print("KHÔNG ĐO ĐƯỢC:", e)
        sys.exit(3)
```

| ID | mục tiêu | phép đo | đột biến làm ĐỎ |
|---|---|---|---|
| A1 | M1–M4 | `kiem_p1.py` rc 0: mỗi tệp của write set ở ứng viên bằng **đúng từng byte** bản dựng từ base bằng cách thay mọi khối `cu` bằng khối `moi` | xoá một vế bất kỳ của L7 (mỗi gạch đầu dòng, mỗi mã E là một đột biến); giữ khối §3 cũ; trả một dòng §20 về bản cũ; sửa một dòng protocol ngoài bốn dòng; ngắt dòng lại một đoạn của L7 ⇒ rc 1. Ngắt dòng lại ĐỎ là cố ý: đặc tả quy định cả chỗ ngắt dòng, nên phép so cả tệp đúng byte thay cho phép khớp cụm sau khi nối dòng (L6 vế b) |
| A2 | phạm vi | cùng script: `git diff --name-only <base> HEAD` bằng đúng hai tệp của write set | thêm tệp thứ ba ⇒ rc 1 |
| A3 | M1 | cùng script: mỗi dòng khai nằm trọn trên đúng một dòng của `SKILL.md`, và OID của nó qua đủ ba phép đo land của ADR tương ứng | đổi một ký tự hex của OID trong khối `moi` S1 và trong `DONG_KHAI` (giữ hai chỗ khớp nhau để A1 vẫn xanh) ⇒ rc 1 |
| A4 | neo | cùng script: mỗi khối `cu` có đúng một lần trên base, các khối không chồng nhau; tệp đặc tả đưa vào là LF thuần | base có một khối `cu` hai lần hoặc vắng ⇒ rc 3; bản đặc tả đổi sang CRLF ⇒ rc 3; đường dẫn đặc tả vắng hay là thư mục ⇒ rc 3 |
| A5 | bất biến | `python .claude/dev/packet_loop.py doctrine-scan --root .` rc 0; `python .claude/dev/packet_loop.py adr-song --root .` rc 0; `git diff --check <base> HEAD` rc 0 | chép một câu 10 từ của protocol vào `SKILL.md` ⇒ `doctrine-scan` rc 6 |
| A6 | bất biến (a) §12 | trên đúng SHA sẽ đẩy: `python scripts/tl.py --selftest` ra N/N với hai số bằng nhau | — (canh bất biến) |

Chạy thử trên base (ứng viên = base): A1 ĐỎ, đúng màu "chưa làm"; A5 xanh sẵn (canh bất biến, răng từ đột biến). Bằng
chứng chạy thử của từng đột biến ghi ở biên nhận review đặc tả.

## 5. `luat_dung`

- (i) Trần lời gọi Codex review của PR thi công: mười, theo dòng khai ở đầu tệp. Chạm trần mà chưa approve ⇒ Review
  Rescue Checkpoint (`ADR-0037`); đó là E2.
- (i) Số lần push thêm và điều kiện merge: `ADR-0060` M5, M7 (mặc định theo `ADR-0062`).
- (i) Cùng hình dạng lỗi lần thứ ba, hay tín hiệu không hội tụ: protocol §12. Phiên thi công tự xét lại cách làm và ghi lý
  do vào handoff; chỉ hỏi khi rơi vào E1 hay E3.
- (ii) E1: không còn phương án có phép đo chống đỡ, ví dụ khối `moi` không qua được `doctrine-scan` mà mọi cách viết lại
  đều đổi nghĩa. E2: thiếu tài nguyên, ví dụ không có clone không shallow để chạy A3. E3: bằng chứng mâu thuẫn với một
  quyết định của chủ kho, ví dụ văn bản L7 trái với chỉ đạo 07-11-2026.

Không có ngân sách mềm. Lỗi văn bản trong khối `moi` mà reviewer chỉ ra không sửa tại chỗ được, vì vị từ A1 đòi đúng
byte: phiên thi công dừng và đề xuất revision đặc tả kèm văn bản mới; đó không phải điểm hỏi chủ kho.

## 6. Review và ngân sách

- Review đặc tả này (trước khi đóng băng): Codex offline trên commit cục bộ, chung một lượt với đặc tả packet 2; nhánh
  đặc tả chỉ được đẩy khi review approve. Trần theo dòng khai ở đầu tệp.
- Review mã: Codex offline qua `launcher.py run`, mỗi lời gọi ghi `record-codex-call`; khởi tạo state packet bằng
  `init --codex-review-calls-limit 10` cho khớp dòng khai, vì `packet_loop.py` không tự đọc dòng khai (S1).
- Connector `@codex review` trên PR draft theo `ADR-0060` M6.
- CI: không tự kích `workflow_dispatch`; lượt CI tự động của PR là đủ (Windows `not_required`, M9 không áp).

## 7. `ngoai_pham_vi`

- Sửa `ADR-0037` hay bất kỳ ADR nào: ADR đã Accepted không sửa hồi tố; ghi chú nằm ở §20.
- Sửa các dòng §20 khác (`ADR-0036`, `ADR-0052`, `ADR-0055`…): dòng `ADR-0052` và `ADR-0055` đã nói đúng chuyện thay
  số; dòng `ADR-0036` trỏ `ADR-0052`, từ đó đọc tiếp được.
- Mã đọc dòng khai trong `packet_loop.py` (`init` tự lấy trần từ đặc tả): packet 3 của lộ trình.
- Cổng quét đặc tả đỏ khi thêm điểm hỏi ngoài E1–E5: packet 3 của lộ trình.
- E4, E5, sổ quyết định uỷ quyền, đóng băng đặc tả không cần chủ kho duyệt băm: packet 2.
- Sửa các đặc tả cũ đã đóng băng: protocol §3.2 cấm sửa đè; luật mới chỉ áp đặc tả soạn sau land.

## 8. `hinh_dang_ke_thua`

`khong_ap_dung`: không phải packet khắc phục.

## 9. `chua_do_duoc`

- Số lần chủ kho bị hỏi giảm bao nhiêu sau khi land: chỉ đo được sau land, bằng cách đếm lại comment quyết định như tài
  liệu "Giảm việc hỏi chủ kho" đã làm. Không có cổng nào bắt đặc tả mới tuân L7 cho tới packet 3.
- A3 đòi clone không shallow và `origin/master` vừa fetch. Phiên không có điều kiện ấy thì A3 là KHÔNG ĐO ĐƯỢC (rc 3),
  không phải ĐẠT.

## 10. Phân loại theo danh sách đóng (dùng khi ADR của packet 2 có hiệu lực)

Không E4: không hành động nào ra ngoài kho hay không hoàn tác được; merge commit hoàn tác được. Không E5: không sửa mã
cổng, danh sách cho phép hay điểm dừng của protocol; packet chỉ cấm đặc tả tự thêm điểm hỏi. Cho tới khi packet 2 land,
merge vẫn theo `ADR-0060` M7: chủ kho duyệt một lần, neo SHA.

## 11. Tiền kiểm định danh trước đóng băng

Đặc tả này sẽ đi qua K1 (`ADR-0063`) qua nguồn `spec_ref` ghim OID, nên định danh của nó phải đúng grammar trước khi đóng
băng. Người soạn gọi chính hàm `_spec_merge` của `.claude/dev/packet_loop.py` với một lease giả có `packet_id`
`GIAM-HOI-P1-SOAN-SPEC`, `revision` 5, `spec_path` là đường dẫn tệp này, `spec_ref` ghim OID commit chứa nó và
`spec_hash` là sha256 của tệp: hàm phải trả về không lỗi. Kết quả ghi ở biên nhận review đặc tả. Lượt review 1 đo được
r1 bị từ chối (`spec identity H1 sai grammar`) vì tiêu đề H1 cũ bắt đầu bằng chữ `Đặc tả`.

## 12. Thay đổi so với r1

Theo verdict review Codex lượt 1 (08-11-2026, `changes_requested`, 9 finding chung cho hai đặc tả):

- F01 (P1): tiêu đề H1 viết lại theo grammar `# <id> r<N> — <tiêu đề>` của `ADR-0063`; hàng `packet_id` nói rõ lease
  phải khai đúng định danh ấy; thêm mục 11.
- F07 (P2): khối `moi` S1 bỏ các con số trần lời gọi và trỏ về bảng *Hiệu lực* của `ADR-0055`; L7 bỏ con số mức dành
  sẵn của `ADR-0041`; dòng §20 `ADR-0037` bỏ các con số trần ở cột luật (chỉ còn trích dẫn lịch sử *"hai lượt Codex"*),
  cột cổng gọi tên hằng thay cho giá trị. Cột cổng của `ADR-0048` giữ tên và giá trị hằng
  `MAC_DINH_TRAN_VONG_REVIEW = 10` vì đó là mô tả mã có ngày đo, không phải luật trần.
- Các finding còn lại (F02–F06, F08, F09) thuộc packet 2. Write set, M1–M4 về đích, A1–A6 và các khối `cu` không đổi.

## 13. Thay đổi so với r2

Theo verdict review Codex lượt 2 (08-11-2026, `changes_requested`, 5 finding chung cho hai đặc tả):

- G01 (P2): khối `moi` S1 không còn nói đặc tả thiếu dòng khai *"rơi về trần thấp nhất"*: thiếu dòng `ADR-0055` thì trần theo
  luật của `ADR-0052` (có thể là trần của một dòng `ADR-0052` hợp lệ), thấp hơn trần của `ADR-0055`. Vẫn không chép con số.
- G03 (P2): gạch đầu dòng thứ ba của L7 đòi mọi câu hỏi chủ kho mang mã E, kể cả câu sinh từ một điểm dừng loại (i);
  loại (i) chỉ dừng phiên.
- G05 (P2, phát hiện ở packet 2, áp cả ở đây cho nhất quán): `kiem_p1.py` đọc byte thô của đặc tả và trả rc 3 khi có CR,
  thay vì đổi CRLF thành LF; A4 thêm đột biến tương ứng.
- G02, G04 thuộc packet 2. Write set, M2–M4 trừ hai câu trên, A1–A3, A5, A6 và các khối `cu` không đổi.

## 14. Thay đổi so với r3

Chủ kho chỉ đạo ngày 08-11-2026, sau khi r3 đã được review lượt 4 approve: *"Do CLaude sắp hết quota, hãy chuyển sang agy
4.0 argon làm executor"*. Executor là trường của đặc tả đóng băng (protocol §3.2), nên đổi nó cần revision mới. Chỉ đổi hai
hàng `executor` và `reviewer` ở bảng đầu, tham chiếu tới đặc tả packet 2, và định danh r4. Mọi khối `thay`, write set, mục
tiêu, vị từ (trừ số revision trong chú thích và đường dẫn) và tiêu chí không đổi.

## 15. Thay đổi so với r4

Verdict review Codex lượt 6 (08-11-2026): **approve** P1 r4, kèm một P3 chung cho hai packet (K01). Sửa để PR đặc tả không
còn P3 mở.

- K01 (P3): hàng `executor` nói rõ adapter `.agents/skills/work-packet/SKILL.md` chỉ được dùng lại phần cú pháp; identity và đối
  số provider lấy từ lease Antigravity. Hàng `reviewer` nói rõ `init` từ chối cặp cùng họ, nên nếu executor đo được là họ
  `openai` thì reviewer phải đổi họ trước `init`.
- `kiem_p1.py` trả rc 3 khi không đọc được tệp đặc tả, như `kiem_p2.py` từ P2 r6 (lớp mà lượt 6 ghi là còn ở P1); A4 thêm đột
  biến tương ứng. Các khối `thay`, write set và tiêu chí khác không đổi.
