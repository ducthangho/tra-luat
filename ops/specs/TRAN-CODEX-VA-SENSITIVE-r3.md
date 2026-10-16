# Đặc tả packet wp782 — TRAN-CODEX-VA-SENSITIVE (revision 3)

- `packet_id`: **wp782** (ID bền theo protocol §3.2) · tên mô tả / bí danh: `TRAN-CODEX-VA-SENSITIVE`
- `packet_issue`: **#782** · `mission_issue`: **#782**
- `revision`: **3** · `generation`: **3** · soạn **23:5xZ 16-10-2026**
- `risk` / `review_class`: **sensitive**
- `base`: `origin/master` @ `653fef3f52f3130dd6f597c1036430ffb807fef1`
- `depends_on`: `[]`

## Revision này THAY THẾ TOÀN BỘ r1 và r2

Tệp này **tự đứng được**: mọi mục có hiệu lực của packet nằm ở đây. r1 và r2 giữ nguyên làm hồ sơ (không sửa
đặc tả đã đóng băng — §3.2) nhưng **không còn là nguồn thi hành**. Không có quy tắc kế thừa kiểu "giữ nguyên
trừ…": bản r2 đã viết quy tắc ấy ngược nghĩa (cross-review connector trên PR #783, P1, comment 4300256143).

| revision | tệp | `spec_sha256` | commit đưa vào |
|---|---|---|---|
| r1 | `ops/specs/TRAN-CODEX-VA-SENSITIVE.md` | `56a0bf28e9a9916a7eccd483a028b7c0e2858e24f3199b6d0e542f87df8e5008` | `abc5486e` |
| r2 | `ops/specs/TRAN-CODEX-VA-SENSITIVE-r2.md` | `f54a18bed6e337e9bcf7d0ab3cf875132525880ec1aa267e9123373cfcc6ab7a` | `e1e5944e` |
| **r3** | tệp này | in bằng `sha256sum` sau commit | commit đưa tệp này vào |

Mỗi revision nằm trong **commit riêng** có thông điệp nêu đúng revision ấy; PR #783 chứa cả ba và tiêu đề/thân
PR liệt kê cả ba (P1 comment 4300256146).

## `nguon_cap_viec`

Chỉ thị chủ kho `ducthangho` 16-10-2026 (qua phiên điều phối `session_01CSM7GNazhN6uGJb4v1TqBT`, xác nhận trực
tiếp trong phiên `session_01XaeBSkW4R49AEWj6x4uqff`): (1) trần **lời gọi Codex mỗi PR** 2 → 8; (2) trần packet
**`sensitive`** của `ADR-0044` 3 tệp/300 dòng thêm → **6 tệp/450 dòng thêm** (gốc nêu 10 tệp, chủ kho đổi thành 6
ở Q1). Tiền lệ: `ADR-0048`.

## Quyết định của chủ kho (16-10-2026, nguyên văn lựa chọn ở Issue #782)

| # | quyết định |
|---|---|
| Q1 | `sensitive` ≤ 6 tệp / ≤ 450 dòng thêm; trần thường (≤ 6 tệp / ≤ 1.000 thêm+xoá) không đổi; khác đơn vị giữ nguyên |
| Q2 | Hai ADR: `0052` (lời gọi), `0053` (kích thước) |
| Q3 | Mỗi lượt Codex sau lượt đầu chỉ cấp khi còn P0/P1, finding cắt ngang hoặc cần xác minh lại; hết trần ⇒ Review Rescue Checkpoint |
| Q4 | Mức dành sẵn hai của `ADR-0041` không đổi |
| Q5 | Không hồi tố |
| Q6 | Protocol trỏ về ADR, không chép số |
| C3 | Checkpoint sau lượt Codex 3: hiệu lực neo vào **OID land** do đặc tả trích ("Trích OID land (Khuyến nghị)") |
| R1 | Sau CI đỏ `r291`: thêm `scripts/tl_selftest.py` + `RELEASE_MANIFEST.json` ("Revision r2 + nâng trần (Khuyến nghị)") |
| R2 | Lượt Codex 5 chỉ review delta ("Codex lượt 5 cho delta (Khuyến nghị)") |
| R3 | Sau review connector trên #783: ra r3 + lease g3 ("Cấp r3 + lease g3 (Khuyến nghị)") |

## Trần áp cho CHÍNH packet này, và hai khối `nang_tran`

Đặc tả này **không** có dòng khai `tran_loi_goi_codex: ADR-0052@…` hay `tran_kich_thuoc_sensitive: ADR-0053@…`,
nên theo luật của chính hai ADR nó chịu **trần cũ**: lời gọi Codex **2**, `sensitive` **3 tệp / 300 dòng thêm**.
Chủ kho nâng cả hai cho packet này, mỗi khối đủ trường (P1 comment 4300256139):

```yaml
nang_tran:
- truc: codex_review_calls_used
  ai_nang: ducthangho
  can_cu: >-
    Checkpoint sau luot 2 (2->3), sau luot 3 khi F02 lap lan 3 (3->4), sau CI do r291 cho luot 5
    chi review delta (4->5). Lua chon nguyen van o Issue #782.
  tran_cu: 2
  tran_moi: 5
- truc: kich_thuoc_sensitive
  ai_nang: ducthangho
  can_cu: >-
    Ratchet r291 dem cung so docs/*.md; hai ADR moi buoc sua scripts/tl_selftest.py va tai sinh
    RELEASE_MANIFEST.json (tien le ADR-0048, ADR-0050). Khong tach duoc.
  tran_cu: '3 tep / 300 dong them'
  tran_moi: '5 tep / 300 dong them'
```

Revision này **không** cấp thêm lời gọi Codex: 5/5 đã dùng (lượt 5 `approve` delta tại `2a42ac8c`). Xác minh
r3 dựa trên review connector GitHub trên PR #783/#789, không phải lời gọi Codex CLI của packet.

## `write_set` (5 tệp)

| # | đường dẫn | vì sao |
|---|---|---|
| 1 | `docs/adr/0052-tran-loi-goi-codex-len-tam.md` | ADR mới — trục LỜI GỌI 2 → 8 |
| 2 | `docs/adr/0053-tran-kich-thuoc-sensitive-len-sau-tep.md` | ADR mới — `sensitive` → 6/450 |
| 3 | `docs/PROTOCOL_DA_PHIEN.md` | năm chỗ chép số → trỏ `ADR-0052`; §20 thêm `0052`/`0053`, ghi chú thay số ở `0036`/`0037`/`0038`/`0044` |
| 4 | `scripts/tl_selftest.py` | ratchet `r291_docs_ngoai_goi` 75 → 77, kê khai slot, `R291-DAM-SO-CUNG = 4` |
| 5 | `RELEASE_MANIFEST.json` | tái sinh vì băm `scripts/tl_selftest.py` đổi; `file_count` = 187 |

Thi công hiện hành: nhánh `agent/tran-codex-va-sensitive-r1-g1-claude` @ `2a42ac8c` (PR #789). r3 không đòi đổi
mã ở đó; nghiệm thu dưới đây đo trên chính head ấy.

## `ngoai_pham_vi`

1. KHÔNG sửa ADR cũ (`0036`, `0037`, `0038`, `0041`, `0043`, `0044`) hay đặc tả đã đóng băng nào.
2. KHÔNG đổi trục VÒNG (`ADR-0048`) và trục ATTEMPT.
3. KHÔNG đổi trần packet thường, KHÔNG thống nhất đơn vị `thêm` / `thêm+xoá`.
4. KHÔNG sửa `.claude/skills/soan-spec/SKILL.md:89` (nợ `SOAN-SPEC-TRO-NGUONG-CU`).
5. KHÔNG đổi mức dành sẵn của `ADR-0041`.
6. KHÔNG viết cổng nào canh hai trần, KHÔNG chữa nợ `R291-DAM-SO-CUNG` (packet riêng).

## `muc_tieu`

| # | mục tiêu | chiếu vào |
|---|---|---|
| M1 | `ADR-0052`: trần LỜI GỌI Codex mỗi PR là **tám**; trục VÒNG và ATTEMPT không đổi | #1 |
| M2 | `ADR-0052`: luật cấp lượt theo Q3; mức dành sẵn **hai** của `ADR-0041` không đổi | #1 |
| M3 | `ADR-0052`: với reviewer Codex, trần 8 lời gọi chạm trước trần 10 vòng | #1 |
| M4 | `ADR-0053`: `sensitive` ≤ 6 tệp / ≤ 450 dòng thêm; trần thường không đổi | #2 |
| M5 | Cả hai ADR: hiệu lực **không hồi tố** neo vào OID land do đặc tả trích (C3) — đúng một dòng khai, OID chứa ADR, cha thứ nhất chưa có, OID trên chuỗi first-parent của nhánh mặc định; thiếu/không đo được ⇒ trần cũ | #1, #2 |
| M6 | Cả hai ADR: khối vượt trần `nang_tran` đủ bốn trường; nói thẳng không cổng nào cưỡng chế | #1, #2 |
| M7 | Protocol trỏ, không chép số; §20 đúng một dòng mỗi ADR mới | #3 |
| M8 | Ratchet `r291` khớp số `docs/*.md` thật; manifest khớp cây | #4, #5 |

## `nghiem_thu` — mỗi tiêu chí có phép làm ĐỎ

**A1 (M7).** `python3 .claude/dev/packet_loop.py adr-song --root .` ⇒ `rc=0`, số ADR = số dòng §20.
**Đỏ khi:** xoá dòng §20 của `0053`.

**A2 (M1, M7) — KHÔNG phân biệt hoa thường** (P1 comment 4300256156: bản r1 thiếu `-i` nên bỏ sót
`Hai lượt Codex review`):
`rg -n -i "hai lượt Codex|2 lượt Codex|tối đa hai trên một PR|tám lượt|8 lượt" docs/PROTOCOL_DA_PHIEN.md` ⇒ **0 dòng**;
cùng lệnh trên `docs/adr/0052-*.md` ⇒ ≥ 1. **Đỏ khi:** giữ `Hai lượt Codex review` (chữ H hoa) hoặc chép "tám lượt"
vào protocol.

**A3 (M4, M7).** `rg -n -i "450 dòng|6 tệp và" docs/PROTOCOL_DA_PHIEN.md` ⇒ **0 dòng**. **Đỏ khi:** chép ngưỡng mới.

**A4 (M5).** Đọc ra đúng MỘT câu trả lời trên các ca: (a) không dòng khai ⇒ cũ; (b) dòng khai trích OID không
nằm trên first-parent nhánh mặc định (nhánh chưa land) ⇒ cũ; (c) dòng khai trích OID land thật ⇒ mới;
(d) đổi `base_sha` của lease, rebase/xoá ref ⇒ không đổi kết quả; (e) chính đặc tả này ⇒ cũ.
**Đỏ khi:** điều kiện lấy từ ngày, từ thời điểm commit hay từ `base_sha` của lease.

**A5 (M2).** `ADR-0052` có câu "mức dành sẵn hai của `ADR-0041` không đổi". **Đỏ khi:** thiếu câu (kiểm bằng đọc).

**A6 (M6) — đếm NGUYÊN TỪ, TỪNG trường, trên MÃ CỔNG** (P1 comment 4300256160: bản r1 đếm chuỗi con trên mọi
`*.py`, nên khớp nhầm `tran_cung` và hai script trong `ops/reviews/`):
```
for t in nang_tran ai_nang tran_cu tran_moi codex_review_calls_used; do
  printf '%s ' "$t"; for f in ops/lease_publish.py .claude/dev/packet_loop.py; do
    printf '%s=%s ' "$f" "$(rg -cw "$t" "$f" || echo 0)"; done; echo; done
```
Mỗi ADR phải có khối `nang_tran` đủ bốn trường (`ai_nang`, `can_cu`, `tran_cu`, `tran_moi` — `can_cu` không đếm
ở vòng lặp vì cơ chế thu hồi lease cũng dùng nó) VÀ câu "không cổng nào cưỡng chế". Lời khai ấy đúng khi
năm tên trong vòng lặp đều **0** ở cả hai tệp cổng. **Đỏ khi:** ADR khai có cổng mà đếm ra 0, hoặc thiếu một trường.

**A7 (r2, giữ).** `git diff --numstat 653fef3f..<head>` ⇒ đúng **5** đường dẫn ở `write_set`, tổng thêm ≤ **300**.

**A8.** `python3 .claude/dev/packet_loop.py doctrine-scan --root .` ⇒ `rc=0`.

**A9 (M8).** `python scripts/tl.py --selftest` (`core.abbrev 7`) ⇒ `N/N`, hai số **bằng nhau**. **Đỏ khi:** đặt
ratchet về 75 ⇒ `r291_docs_ngoai_goi` FAIL.

**A10 (M8) — đúng TÊN KHOÁ** (P2 comment 4300256159: bản r2 dùng `expected`/`checked` không tồn tại):
`python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` ⇒ `"ok": true` VÀ
`expected_file_count == checked_file_count == 187`, `failed == []`, `extra_files == []`. **Đỏ khi:** sửa
`scripts/tl_selftest.py` mà không tái sinh manifest.

**A11.** `python -m ruff check --select F scripts/tl_selftest.py` ⇒ cùng số đếm với base (delta 0).

**Điều kiện dừng:** `sensitive` ⇒ cross-review khác nền `approve` tường minh trên exact head (đã có: Codex CLI
lượt 4 `approve` `4711e874`, lượt 5 `approve` delta `2a42ac8c`; connector GitHub trên #789 hoàn tất, không finding).

## `hinh_dang_ke_thua`

Lớp **`dac-ta-tu-mau-thuan-hoac-thuoc-do-mu`** — xuất hiện ở r1 (A2 thiếu `-i`, A6 đếm chuỗi con) và r2 (quy
tắc kế thừa ngược nghĩa, `nang_tran` thiếu trường, sai tên khoá). Đây là lần **thứ hai** lớp này lặp trong
packet; r3 đóng nó bằng cách viết lại đặc tả **đầy đủ** thay vì vá theo delta.

## `chua_do_duoc`

1. Không bộ đếm, không cổng cho hai trần (`SO-CANON-CHUA-TON-TAI`).
2. Con số 8 và 6/450 là quyết định của chủ kho; kho không có dữ liệu biện hộ.
3. Nợ P3 `nham-file-count-voi-entry-zip` (kê khai "còn 13 khe", đúng là 12) — sửa ở lần kê khai kế tiếp.
