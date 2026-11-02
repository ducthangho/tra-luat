# Handoff #825 CODEX-REJECTED-STATE-KHONG-GHI-DUOC-ADR — lease wp825-r1-g1-claude

Trạng thái lúc 01:30Z 02-11-2026: Codex lượt 3/10 cho **`approve`** trên `f46115b`, kết quả 0 P0 · 0 P1 · 0 P2 · 0 P3.
A5 (CI trên đúng head) xem mục Nghiệm thu. Merge thuộc quyền chủ kho: `uy_quyen_merge: false`. Phiên này chưa merge.

- PR: #1138 (draft). Nhánh `agent/wp825-g1-claude`, head `f46115b42220620bb681abcad6399542c9b7c7b0`, base `c7174bf`.
- Diff: 2 tệp. ADR mới `docs/adr/0061-codex-trang-thai-tu-choi-khong-ghi-duoc.md` và đúng 1 dòng bảng §20 của
  `docs/PROTOCOL_DA_PHIEN.md`. Không sửa runtime hay test.
- Spec `ops/specs/wp825.md`, sha256 `dee36a11…812e`. Quyết định chủ kho: "ADR chấp nhận (Recommended)" cho #825.

## Lệch tiền đề spec (reviewer yêu cầu ghi lại; KHÔNG sửa spec đóng băng)
Mục "Sự thật đã đo" của spec ghi rằng mỗi lần gọi tốn thêm **đúng 1** probe, và lần nào cũng cho cùng lý do CHẶN.
Codex lượt 1 bác tính tuyệt đối của câu này bằng chèn lỗi I/O, ở cả ba lối và trên cả base lẫn head:

| lỗi chèn | probe qua hai lượt | state chứa đúng id |
|---|---|---|
| trước `os.replace` | [1,1] | không |
| `os.fsync` thư mục SAU `os.replace` (`launcher.py:3389–3390`) | [1,0] | có |
| state không đọc được (`_dang_cho_snapshot` trả True, `:3615–3616`) | [1,0] | không |
| ghi thành công (đối chứng) | [1,0] | có |

Executor đọc lại mã và xác nhận hai dòng trên. ADR nay chỉ chấp nhận probe lặp khi state vẫn đọc được mà chưa nhớ
danh tính đã bị từ chối. ADR cũng nói rõ lỗi ghi sau `replace` và lỗi đọc state cho 0 probe, kèm một lý do khác.
Tiêu chí A1–A5 không đòi "đúng 1", nên quyết định chấp nhận của chủ kho không đổi. Muốn đổi nghĩa vụ nghiệm thu thì
phải làm revision spec theo protocol.

## hint_provenance
- `17d3606` (executor): bỏ backtick ở 3 con trỏ mà `doc-claims-check` không phân giải được (L1 `PATH_MISSING` cho đặc tả
  chỉ có ở nhánh lease, 2 L12 `TEST_ID_UNKNOWN` cho ca `launcher_test`), theo tiền lệ `ADR-0059`. Lỗi này làm
  `gate-ops` đỏ qua `t56`.
- `df3e103`: áp NGUYÊN `luot1/HINT.patch` (sửa F1 P1 và F2 P2).
- `f46115b`: áp NGUYÊN `luot2/HINT.patch` (đổi tiêu đề ADR, P2 còn sót của F1).

## Nghiệm thu
- **A1** `adr-song`: 60/60, rc=0. Đột biến bỏ dòng ADR-0061 ⇒ rc=9 (Codex lượt 1 đo).
- **A2** `doctrine-scan`: rc=0, quét 10 tệp, 0 chỗ chép doctrine.
- **A3**: ADR nêu đủ `CODEX_HOME`, `_danh_dau_auth_hong`, tên ca và đột biến của ba lối, `#825`. Mục Cưỡng chế tách
  hai phép đo: khớp định danh ADR = 0 ở cả sáu vị trí cổng; khớp khái niệm = `launcher.py`×4. Cột §20 ghi "có nhắc".
- **A4**: executor đo trên `f46115b` lúc 01:26Z với `TMPDIR=/var/tmp/a4825` (ngoài `/tmp`, vì `/tmp/.git` rỗng do
  sandbox Codex để lại làm constructor `_KhoCodex` từ chối):
  - `r484_g7_khong_ghi_duoc_trang_thai_tu_choi_phai_noi_ra`: `1/1 qua`;
  - `r484_g7_materializer_khong_ghi_duoc_trang_thai_noi_dung_ly_do`: `1/1 qua`;
  - `codex_cred_test.py`: `ca 18 · đột biến 18 · TỔNG: ĐẠT`.
  Sandbox reviewer không ghi được ngoài `/tmp`, nên A4 nguyên trạng là phép đo của executor.
- **A5**: CI `ci.yml` trên `f46115b`, run 41371804862 — CHỜ (cập nhật khi xong).
- `doc-claims-check --strict --json`: `ok: true`, `flags: []` trên `f46115b`.

## Codex — 3/10 lời gọi (trần ADR-0055)
| lượt | head | verdict (P0/P1/P2/P3) | ghi chú |
|---|---|---|---|
| 1 | `46421d7` | changes_requested 0/1/1/0 | F1 `loi-ghi-khong-suy-ra-probe-lap`, F2 `grep-ten-khong-do-khai-niem` |
| 2 | `df3e103` | changes_requested 0/0/1/0 | tiêu đề ADR vẫn suy rộng |
| 3 | `f46115b` | **approve 0/0/0/0** | — |

Hiện vật của từng lượt nằm ở `wp825-g1-claude/luot{1,2,3}/`, gồm PROMPT, VERDICT, HINT và `run/`, kèm `SHA256SUMS`.
`HINT.patch` của lượt 3 rỗng.
