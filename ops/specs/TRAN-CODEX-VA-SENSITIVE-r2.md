# Đặc tả packet — TRAN-CODEX-VA-SENSITIVE (revision 2)

- `packet_id`: **TRAN-CODEX-VA-SENSITIVE** · `packet_issue`: **#782** · `mission_issue`: **#782**
- `revision`: **2** · `generation`: **2** · soạn **18:2xZ 16-10-2026**
- `tien_nhiem`: revision 1 — `ops/specs/TRAN-CODEX-VA-SENSITIVE.md`, `spec_sha256 56a0bf28e9a9916a7eccd483a028b7c0e2858e24f3199b6d0e542f87df8e5008`
  (commit `abc5486e`). Đặc tả r1 **không sửa**; tệp này là bản sửa đổi theo §3.2.
- `risk` / `review_class`: **sensitive** (không đổi)
- `base`: `origin/master` @ `653fef3f` (không đổi)

## Revision này giữ NGUYÊN gì

Mọi mục của r1 giữ nguyên nghĩa, trừ đúng những mục ghi dưới đây: nguồn cấp việc, quyết định Q1–Q6, mục tiêu M1–M7,
tiêu chí A1–A6 và A8, `ngoai_pham_vi` #1–#6, `chua_do_duoc`. Người đọc r2 phải đọc r1 trước.

## Vì sao có revision 2 — đo được, không suy

Lần push duy nhất của nhánh code (`agent/tran-codex-va-sensitive-r1-g1-claude` @ `4711e874`, PR #789) làm CI
`gate (ubuntu-latest)` ĐỎ: `== tl selftest 1730/1731 ==`, ca đỏ duy nhất `r291_docs_ngoai_goi` (run `38945289558`,
job `117122881612`). Nền: PR #783 trên cùng base `653fef3f` có `gate` XANH ⇒ delta là của packet.

Nguyên nhân: `r291` ghim cứng số tệp `docs/*.md` = **75**; packet thêm hai ADR ⇒ **77** (đo 18:2xZ 16-10-2026:
`git ls-tree -r --name-only 653fef3f docs | rg -c '\.md$'` = 75; cây packet = 77). Sửa con số buộc chạm
`scripts/tl_selftest.py`, và tệp ấy có trong `RELEASE_MANIFEST.json` (`file_count` 187) nên manifest phải tái
sinh vì băm đổi. Hai tệp ngoài write set r1 ⇒ r1 không kham được ⇒ revision.

Lỗi quy trình của executor, ghi thẳng: trước lần push, executor chạy `adr-song`, `doctrine-scan`, `git diff
--check` nhưng **không chạy `python scripts/tl.py --selftest`** mà `CLAUDE.md` bước 4 đòi. Đây đúng hình dạng
"bốn cổng xanh trả lời một câu hỏi KHÁC" mà `scripts/tl_selftest.py` đã ghi cho ADR-0048.

**Hình dạng lỗi kế thừa (L4):** nợ `R291-DAM-SO-CUNG` — ghi trong `scripts/tl_selftest.py` là **3** lần
(#522, #548, #551). Packet này là lần thứ **4**. Doctrine: lặp ≥ 3 lần thì câu hỏi đúng là có nên tiếp tục
cách làm không; chủ kho đã được hỏi và chọn đường kê khai slot cho packet này (quyết định R1 dưới), chữa nợ
gốc là packet riêng.

## Quyết định của chủ kho cho revision này (16-10-2026, phiên `session_01XaeBSkW4R49AEWj6x4uqff`)

| # | câu hỏi | quyết định (nguyên văn lựa chọn) |
|---|---|---|
| R1 | Đường xử lý CI đỏ r291 | **"Revision r2 + nâng trần (Khuyến nghị)"** — đặc tả r2 + lease gen 2 thêm hai tệp; nâng trần kích thước cho packet này 3→5 tệp bằng `nang_tran`; ratchet 75→77 kèm kê khai slot; tái sinh manifest; push vá CI theo ngoại lệ Q2 |
| R2 | Ai xác minh delta sau head đã approve `4711e874` | **"Codex lượt 5 cho delta (Khuyến nghị)"** — `nang_tran` lời gọi 4→5; Codex chỉ review delta |

## `write_set` (thay mục cùng tên của r1)

| # | đường dẫn | vì sao |
|---|---|---|
| 1 | `docs/adr/0052-tran-loi-goi-codex-len-tam.md` | như r1 |
| 2 | `docs/adr/0053-tran-kich-thuoc-sensitive-len-sau-tep.md` | như r1 |
| 3 | `docs/PROTOCOL_DA_PHIEN.md` | như r1 |
| 4 | `scripts/tl_selftest.py` | ca `r291_docs_ngoai_goi`: ratchet 75→77 ở `ok3`/`ok4`, kê khai slot, `R291-DAM-SO-CUNG = 4` |
| 5 | `RELEASE_MANIFEST.json` | tái sinh vì băm `scripts/tl_selftest.py` đổi; `file_count` phải giữ **187** |

## `nang_tran` kích thước (mới ở r2)

Trần áp cho packet này vẫn là trần CŨ của `ADR-0044` (đặc tả không có dòng khai của `ADR-0053`).

```yaml
nang_tran:
  truc: kich_thuoc_sensitive
  ai_nang: ducthangho
  can_cu: >-
    Ratchet r291 dem cung so docs/*.md; them hai ADR buoc sua scripts/tl_selftest.py va tai sinh
    RELEASE_MANIFEST.json (tien le ADR-0048, ADR-0050). Khong tach duoc: hai tep moi khong co
    nghia neu thieu hai ADR, va CI do neu thieu hai tep moi.
  tran_cu: '3 tep / 300 dong them'
  tran_moi: '5 tep / 300 dong them'
```

Trần số dòng **không** nâng: tổng thêm của r2 phải vẫn ≤ 300.

## `nang_tran` lời gọi Codex (cập nhật)

`tran_cu: 2` → `tran_moi: 5` (lịch sử 2→3→4 ở Issue #782; 4→5 theo R2). Lượt 5 CHỈ review delta
`4711e874..<head mới>`.

## `nghiem_thu` bổ sung (thêm vào A1–A8 của r1)

**A7 (thay A7 của r1).** `git diff --numstat 653fef3f..<head>` ⇒ đúng **5** đường dẫn ở `write_set` trên, tổng
thêm ≤ **300**. **Đỏ khi:** thêm đường dẫn thứ sáu, hoặc vượt 300.

**A9 — selftest đủ.** `python scripts/tl.py --selftest` (ghim `core.abbrev 7`) ⇒ `N/N` với **hai số bằng
nhau**, chạy trên đúng head sẽ push. **Đỏ khi:** đặt lại ratchet về 75 ⇒ `r291_docs_ngoai_goi` FAIL.

**A10 — manifest đúng.** `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` ⇒
`"ok": true` và `expected == checked`; `file_count` = **187**. **Đỏ khi:** sửa `scripts/tl_selftest.py` mà không
tái sinh manifest.

**A11 — chỉ một tệp `.py` đổi, delta ruff = 0.** `python -m ruff check --select F scripts/tl_selftest.py` ⇒ cùng
số đếm với master (`CLAUDE.md`: nền **3914 F821 + 1 F401**, đo lại trước khi kết luận).

## `chua_do_duoc` bổ sung

Không chữa nợ `R291-DAM-SO-CUNG` ở packet này: mỗi `docs/*.md` mới vẫn sẽ làm `r291` đỏ cho packet kế tiếp
(gồm packet #784, thêm `ADR-0054`).
