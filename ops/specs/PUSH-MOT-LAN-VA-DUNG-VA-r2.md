# Đặc tả packet — wp784 `PUSH-MOT-LAN-VA-DUNG-VA` (revision 2)

- `packet_id`: **wp784** · bí danh `PUSH-MOT-LAN-VA-DUNG-VA` · `packet_issue`: **#784** · `mission_issue`: **#784**
- `revision`: **2** · `generation`: **2** · soạn **07:5xZ 17-10-2026**
- `executor`: claude (`model_family: claude`, `execution_surface: claude_code`) · `environment`: cloud
- `reviewer`: codex (`model_family: openai`, `execution_surface: codex_cli`) · `assurance_target`: `cross_approved`
- `risk` / `review_class`: **sensitive** (đổi luật review, điều kiện dừng vá và đường push, tức review/land authority)
- `branch`: `agent/wp784-g2-claude` · `base`: `origin/master` @ `8ab100793df9831505f495543a74044b91c2c9ab`
- `depends_on`: packet #782, **đã land** ở `8ab1007` (PR #791) và `25cda36` (PR #783)

Tệp này **tự đứng được**, thay hoàn toàn revision 1. Không có quy tắc "giữ nguyên trừ…".

## Dòng khai trần (luật `ADR-0052`, `ADR-0053`)

tran_loi_goi_codex: ADR-0052@8ab100793df9831505f495543a74044b91c2c9ab
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

Hai dòng trên, mỗi dòng đứng riêng, đầu dòng, đúng một lần. `8ab1007` chứa cả hai ADR, cha thứ nhất `25cda36` chưa
có, và nằm trên chuỗi first-parent của `origin/master` (đo 07:5xZ 17-10-2026). Áp dụng: trần lời gọi Codex là
**tám**, trần kích thước `sensitive` là **≤ 6 tệp / ≤ 450 dòng thêm**.

## Hồ sơ revision

| revision | tệp | `spec_sha256` | commit |
|---|---|---|---|
| r1 | `ops/specs/PUSH-MOT-LAN-VA-DUNG-VA.md` | `04cf39c1…` | `ae13ed7` |
| r2 | tệp này | (băm ghi ở lease) | (commit chứa tệp) |

**Vì sao có r2 (đo được):**
1. r1 viết trước khi #782 land, khai trần mới mà không có dòng khai. Theo luật land-OID của `ADR-0052`/`0053`,
   như thế là trần **cũ** (2 lời gọi, 3 tệp/300 dòng).
2. Thêm `docs/adr/0054-*` làm ratchet `r291_docs_ngoai_goi` đỏ (đếm cứng `docs/*.md` = 77). Đó là cách sập đã làm
   CI #789 đỏ, nợ `R291-DAM-SO-CUNG`. Packet này phải sửa `scripts/tl_selftest.py` và tái sinh `RELEASE_MANIFEST.json`
   (write set 2 → 4 tệp).
3. r1 thiếu `packet_issue`, `executor`/`reviewer`, `branch`. Số dòng của protocol mà r1 trích đã trôi sau khi #782 land.

## `nguon_cap_viec`

Chỉ thị chủ kho `ducthangho` **16-10-2026** (phiên `session_01XaeBSkW4R49AEWj6x4uqff`), nguyên văn:

> "Ngoài ra tôi muốn bổ sung một số yêu cầu trong packet loop. Theo đó là sẽ không được push vào cho đến khi
> đủ điều kiện để merge. Làm sao để mỗi packet hoặc là WP thì chỉ push vào GitHub duy nhất một lần.
> Điều kiện để dừng vá là khi hết P1 và P2. Tùy trường hợp, bạn có thể vá thêm một vài vòng nếu thấy có khả
> năng làm giảm sâu số P3 còn lại, hoặc xóa hoặc giải quyết hết được các P3.
> cross review thì luôn tìm theo phân lớp, không tìm theo các lỗi riêng lẻ. Nếu những yêu cầu nào mà đã có
> sẵn thì hãy bỏ qua."

Chủ kho trả lời *"Đồng ý với các khuyến nghị"* cho Q1–Q8. Ngày 17-10-2026 chủ kho: *"Đã merge #783 và #791, tiếp
tục packet 2"*, và trước đó *"Đồng ý cấp lease"* cho packet này.

## Đối chiếu với thứ đã có (đo trên `origin/master` @ `8ab1007`)

| yêu cầu | đã có ở đâu | phần còn thiếu |
|---|---|---|
| R1: push một lần, khi đủ điều kiện merge | **Không có.** Gần nhất là `docs/PROTOCOL_DA_PHIEN.md` §12: *"khi owner yêu cầu đợi tới đủ điều kiện merge, không chạy CI/fullCI giữa vòng vá"* (có điều kiện). §8 có câu *"Codex vẫn là Reviewer read-only trên exact PR head"*, tức giả định đã push | toàn bộ |
| R2: dừng vá khi hết P1 và P2; vá thêm vì P3 tuỳ trường hợp | **Một phần.** Bảng ngưỡng severity ở §8: `systemic` đòi hết P2; `routine` cho giữ P2 kèm nợ; `sensitive` chỉ đòi hết P0. Không có luật vòng vá thêm vì P3 | siết `routine`/`sensitive`; luật vòng thêm |
| R3: review tìm theo lớp | **Gần như đủ.** §8.3: slug lớp, bảng lớp mỗi lượt, chỉ tính *đã vá* khi đóng cả lớp | một câu chỉ thị CÁCH TÌM |

## Quyết định đã chốt với chủ kho (16-10-2026)

| # | câu hỏi | quyết định |
|---|---|---|
| Q1 | "Push một lần" tính cho nhánh nào | **Chỉ nhánh code của packet.** Nhánh `ops/**` (lease, biên nhận) và PR đặc tả là sổ sách, push như hiện nay |
| Q2 | CI đỏ sau lần push duy nhất | Trước push bắt buộc chạy đủ cổng tại chỗ trên đúng commit sẽ push, gồm `python scripts/tl.py --selftest`. CI vẫn đỏ thì **được push vá chỉ để sửa CI**, mỗi lần ghi vào biên nhận kèm nguyên nhân; không dùng lần push ấy để vá thêm finding review |
| Q3 | Review ở đâu khi chưa push | Mọi vòng review chạy **offline** trên bundle/mirror, neo **SHA commit cục bộ**; push đúng commit ấy |
| Q4 | "Hết P1 và P2 mới dừng" áp class nào | **Mọi class.** `sensitive` vẫn giữ thêm yêu cầu approval tường minh đúng assurance. P0 vẫn chặn ở mọi class |
| Q5 | Giới hạn vòng vá thêm vì P3 | Executor tự quyết, **tối đa 2 vòng thêm**, vẫn tính vào trần lời gọi (`ADR-0052`) và trần vòng (`ADR-0048`). Dừng ngay nếu một vòng không giảm số **lớp** P3 |
| Q6 | Thêm câu "quét theo lớp" | **Một câu** vào §8.3 |
| Q7 | Tài liệu hay mã | **Chỉ tài liệu** (ADR + protocol), cộng phần kê khai ratchet bắt buộc. Cổng mã đếm push là packet riêng sau |
| Q8 | Gộp với #782 hay tách | **Tách**, làm sau khi #782 land (đã land) |

## Số ADR

Quét **578** ref `refs/remotes/origin/*` (bằng `git ls-remote --heads origin`: 578; đo 07:5xZ 17-10-2026). Các
`docs/adr/005x` đang có: `0050`–`0053`; **không** ref nào có `docs/adr/0054-*`. Dùng **`0054`**. Đo lại trước khi
commit; số đã bị chiếm thì DỪNG hỏi.

## `write_set`

| # | đường dẫn | vì sao |
|---|---|---|
| 1 | `docs/adr/0054-push-mot-lan-dung-va-theo-hang-va-review-theo-lop.md` | ADR mới: R1, R2, R3 |
| 2 | `docs/PROTOCOL_DA_PHIEN.md` | bảng ngưỡng §8 (Q4); câu reviewer trên PR head ở §8 (Q3); §8.3 thêm một câu (Q6); §12 con trỏ luật push và vòng thêm (Q1, Q2, Q5); §20 thêm dòng `0054` |
| 3 | `scripts/tl_selftest.py` | ca `r291_docs_ngoai_goi`: ratchet 77 → 78 ở `ok3`/`ok4` (264 → 265), kê khai slot, `R291-DAM-SO-CUNG` = **5** |
| 4 | `RELEASE_MANIFEST.json` | tái sinh vì băm `scripts/tl_selftest.py` đổi; `file_count` phải giữ **187** |

Không ký tự đại diện. Ước lượng ~250 dòng thêm.

## `ngoai_pham_vi`

1. **KHÔNG cổng mã** đếm số lần push hay cưỡng chế điều kiện dừng (Q7). Ghi nợ có tên.
2. **KHÔNG sửa adapter** (`.claude/skills/*`, `.agents/skills/*`, `AGENTS.md`). Đo ra adapter MÔ TẢ push giữa vòng
   vá thì DỪNG hỏi.
3. **KHÔNG đổi** trần lời gọi (`ADR-0052`), trần vòng (`ADR-0048`), trần kích thước (`ADR-0053`).
4. **KHÔNG sửa** `ADR-0037`/`0038`/`0041`/`0052`/`0053` hay đặc tả đóng băng nào.
5. **KHÔNG chữa nợ gốc `R291-DAM-SO-CUNG`** (vẫn đếm cứng); chỉ kê khai slot.

## `muc_tieu`

| # | mục tiêu | chiếu vào |
|---|---|---|
| M1 | `ADR-0054` khai luật push một lần cho nhánh code packet (Q1), điều kiện trước push gồm selftest (Q2), ngoại lệ push chỉ-vá-CI có ghi biên nhận (Q2), nhánh `ops/**` ngoài luật (Q1) | #1 |
| M2 | `ADR-0054` khai review offline neo SHA commit cục bộ, push đúng SHA đã review (Q3); finding của connector GitHub sau push không mở vòng vá tự động mà về checkpoint chủ kho | #1 |
| M3 | `ADR-0054` khai điều kiện dừng vá: hết P0/P1/P2 ở mọi class (Q4); tối đa hai vòng thêm vì P3 và điều kiện dừng sớm (Q5) | #1 |
| M4 | Protocol: ba dòng class của bảng ngưỡng §8 khớp Q4; câu reviewer §8 neo SHA ứng viên; §8.3 có câu quét theo lớp (Q6); §12 trỏ `ADR-0054`; §20 có dòng `0054`. Protocol **không chép con số** của `ADR-0054` | #2 |
| M5 | `ADR-0054` khai hiệu lực không hồi tố bằng cùng luật land-OID của `ADR-0052` với dòng khai riêng `luat_push_va_dung_va: ADR-0054@<oid40>`, và khai **không cổng nào cưỡng chế** (Q7) | #1 |
| M6 | Ratchet và manifest đúng (write set #3, #4) | #3, #4 |

## `nghiem_thu`

Mọi lệnh chạy ở gốc kho trên đúng commit sẽ push; `git config core.abbrev 7`. Mỗi tiêu chí có vế **dương** (nội dung
mới có mặt) và vế **âm** (nội dung cũ vắng mặt) khi áp dụng được. Phép khớp chuỗi dùng `rg -c -F` (chuỗi cố định).

**A1 (M4) — `adr-song` xanh.** `python .claude/dev/packet_loop.py adr-song --root .` ⇒ rc=0, số ADR trên đĩa bằng
số dòng §20. **Đỏ khi:** bỏ dòng `0054` ở §20.

**A2 (M3, M4) — bảng ngưỡng đòi hết P2 ở mọi class.**
- Dương: `rg -c '^\| `(routine|systemic|sensitive)` \| Không còn P0/P1/P2' docs/PROTOCOL_DA_PHIEN.md` ⇒ **3**.
- Âm: `rg -c -F 'P2/P3 còn lại phải có nợ' docs/PROTOCOL_DA_PHIEN.md` ⇒ **0** (rc=1), và
  `rg -c -F 'Không còn P0; cần approval' docs/PROTOCOL_DA_PHIEN.md` ⇒ **0** (rc=1).
- **Đỏ khi:** một dòng class còn cho giữ P2, hoặc dòng `sensitive` cũ còn nguyên.

**A3 (M2, M4) — reviewer neo SHA ứng viên, không neo PR head đã push.**
- Âm: `rg -c -F 'Reviewer read-only trên exact PR head' docs/PROTOCOL_DA_PHIEN.md` ⇒ **0**.
- Dương: `rg -c -F 'Reviewer read-only trên exact SHA ứng viên' docs/PROTOCOL_DA_PHIEN.md` ⇒ **1**.
- **Đỏ khi:** câu cũ còn, hoặc câu mới vắng.

**A4 (M1) — luật push đọc ra đúng MỘT câu trả lời** cho bốn ca: (a) đẩy nhánh code lần đầu khi đủ điều kiện ⇒ được;
(b) đẩy nhánh code giữa vòng vá ⇒ không; (c) CI đỏ sau lần đẩy, vá CI ⇒ được, phải ghi biên nhận; (d) đẩy nhánh
`ops/**` ⇒ ngoài luật. Vế đo được trên `docs/adr/0054-*.md`, mỗi phép ⇒ ≥ **1**:
`rg -c -F 'đẩy nhánh code của packet đúng một lần'` · `rg -c -F 'chỉ để sửa CI'` · `rg -c -F 'ghi vào biên nhận'` ·
`rg -c -F 'nhánh `ops/**`'` · `rg -c -F 'python scripts/tl.py --selftest'`.
**Đỏ khi:** một ca có hai cách đọc khi đọc nghĩa, hoặc một phép trên ra 0.

**A5 (M3) — luật vòng P3 có điểm dừng đo được.** Trên `docs/adr/0054-*.md`, mỗi phép ⇒ ≥ **1**:
`rg -c -F 'tối đa hai vòng vá thêm'` · `rg -c -F 'không giảm số lớp P3'` · `rg -c -F 'Không còn P0/P1/P2'`.
**Đỏ khi:** thiếu một trong ba (vòng thêm thành không giới hạn, hoặc điều kiện dừng không đổi).

**A6 (M5) — hiệu lực và lời khai cưỡng chế.** Trên `docs/adr/0054-*.md`:
- `rg -c -F 'luat_push_va_dung_va: ADR-0054@'` ⇒ ≥ 1;
- `rg -c -F 'không cổng nào cưỡng chế'` ⇒ ≥ 1.

Không tệp cổng nào cưỡng chế luật ấy: `rg -cw 'luat_push_va_dung_va' ops/lease_publish.py .claude/dev/packet_loop.py`
⇒ **0** ở cả hai tệp.
**Đỏ khi:** ADR khai một cổng mà phép trên không tìm ra.

**A7 (M4) — protocol trỏ, không chép số, đúng từng vị trí.** Đếm dòng chứa `ADR-0054` theo mục, bằng
`awk '/^## /{s=$2} /ADR-0054/{c[s]++} END{for(k in c) print k, c[k]}' docs/PROTOCOL_DA_PHIEN.md`:
mục `8.` ⇒ ≥ **2** (bảng ngưỡng + câu reviewer) · mục `12.` ⇒ ≥ **1** · mục `20.` ⇒ ≥ **1**.
Câu §8.3: `rg -c -F 'quét mọi biểu hiện cùng lớp' docs/PROTOCOL_DA_PHIEN.md` ⇒ **1**.
Không chép số: `rg -n -i '(hai|2) vòng (vá )?thêm|đúng một lần' docs/PROTOCOL_DA_PHIEN.md` ⇒ **0**.
**Đỏ khi:** một mục thiếu con trỏ, hoặc protocol chép con số / cụm luật của ADR-0054.

**A8 — trần `ADR-0053`.** `git diff --numstat 8ab1007..<head>` ⇒ đúng **4** đường dẫn ở `write_set`, tổng thêm
≤ **450**. **Đỏ khi:** đường dẫn thứ năm, hoặc vượt 450.

**A9 (M6) — selftest đủ.** `python scripts/tl.py --selftest` ⇒ `N/N`, **hai số bằng nhau**, chạy trên đúng head sẽ
push, TRƯỚC lần push. **Đỏ khi:** ratchet để 77 ⇒ `r291_docs_ngoai_goi` FAIL.

**A10 (M6) — manifest đúng.** `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` ⇒
`"ok": true`, `expected_file_count == checked_file_count == 187`. **Đỏ khi:** sửa selftest mà không tái sinh manifest.

**A11 — `doctrine-scan` xanh và `git diff --check` sạch.** Delta ruff F trên `scripts/tl_selftest.py` so master = 0.

## Điều kiện dừng và push

- **Review:** Codex CLI, offline trên clone trong scratchpad, neo SHA commit cục bộ, prompt nêu `spec_sha256` của
  r2. Dừng vá khi **P0/P1/P2 = 0** theo lớp; tối đa hai vòng thêm vì P3, dừng sớm nếu số lớp P3 không giảm. Mọi
  lời gọi tính vào trần **tám** của `ADR-0052`; lượt sau lượt đầu chỉ khi còn P0/P1, finding cắt ngang, hoặc cần
  xác minh lại.
- **Push:** đúng **một** lần nhánh `agent/wp784-g2-claude`, sau khi A1–A11 xanh tại chỗ và review approve trên SHA
  ấy. Mở PR **draft** rồi chuyển ready để connector GitHub review.
- **Sau push:** CI đỏ ⇒ chỉ push vá CI, ghi biên nhận. Connector báo P1/P2 trên head đã push ⇒ **không tự push vá**;
  DỪNG, đưa checkpoint cho chủ kho kèm phép đo.
- **Không merge, không land.** Chủ kho merge.

## `hinh_dang_ke_thua`

Lớp lịch sử từ packet #782 phải coi là đã biết và chặn sẵn trong tiêu chí trên:
- `dac-ta-tu-mau-thuan-hoac-thuoc-do-mu`: phép khớp thiếu vế dương, khớp tiền tố cụm bị cắt, đếm gộp không theo vị
  trí, regex thiếu dạng chữ số. Ở r2: mọi tiêu chí có vế dương; A7 đếm theo mục.
- `tu-danh-gia-gan-revision-cu-the`: ADR liệt kê revision rồi gọi một revision là "đang hiệu lực". `ADR-0054` không
  được gọi một revision của đặc tả này là "đang hiệu lực"; câu tự đánh giá chỉ nêu phạm vi đã đo.
- `nham-file-count-voi-entry-zip`: kê khai khe phải tính entry manifest (187 record ⇒ 188 entry ZIP).

## `chua_do_duoc`

1. **Không đo được** số lần push của một nhánh từ trong kho (GitHub không giữ lịch sử push theo nhánh ở dạng
   đọc được qua MCP; reflog là cục bộ). Lý do Q7 chọn tài liệu trước.
2. **Không đo được** việc review offline có bắt được mọi thứ CI bắt không; Q2 thừa nhận bằng ngoại lệ vá CI.
3. Tác động lên tốc độ hội tụ: chưa có số đo.
