# Đặc tả packet `CLOUD-SETUP-P3C-CONTRACT` r1: nâng hợp đồng client lên webapp `2.21.2q`

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

| trường | giá trị |
|---|---|
| packet_id | `CLOUD-SETUP-P3C-CONTRACT`, revision 1, generation 1 |
| packet_issue | #1223 |
| nguon_cap_viec | `ops/specs/cloud-setup-p3-writeback-r1.md` mục `ngoai_pham_vi` (dòng "Bump `EXPECT_VERSION`, `API_CONTRACT.md`, SKILL/RUNBOOK … packet `CLOUD-SETUP-P3C-CONTRACT`, mở ngay sau M1"). Chủ kho giao mục 2 ngày 04-11-2026 trong phiên điều phối `session_015GtxraXfMD1t2FJLzzGDr4`; vòng hỏi 05-11-2026 Q1–Q10 chủ kho trả "theo khuyến nghị" (Q4 đính chính ở vòng 2 sau phản biện Codex + GPT; Q8 tách packet tài liệu sang #1224) |
| review_class | `sensitive` — `scripts/tl.py` + hợp đồng webapp; classifier `ops/lease_publish.py:58–66,360–382` mặc định `sensitive` cho đường dẫn không có trong bảng |
| base | `origin/master` lúc cấp lease |
| executor | `anthropic_claude` (Claude Code remote, Linux) |
| reviewer | `openai_codex` qua `launcher.py run` (offline, neo SHA ứng viên, ADR-0060 M12) + connector `@codex review` trên PR draft |
| luật merge | ADR-0060 mặc định theo ADR-0062 |
| windows | `not_required` — diff gồm Markdown và hai literal Python; không chạm `.claude/dev/**`, `.github/**`, script đa nền (ADR-0060 M3) |
| packet anh em | #1224 `CLOUD-SETUP-P3C-DOCS` (`ops/specs/cloud-setup-p3c-docs-r1.md`) — write set rời nhau |

## 1. Vì sao — số đo (05-11-2026, `origin/master` = `48d2665`)

| # | sự kiện | số đo |
|---|---|---|
| S1 | webapp LIVE | `tl ping` 08:21Z: `version=2.21.2q`, `schema_version=2.21.2q`, `registry_cols=27`; client in `⚠ CẢNH BÁO: webapp version=2.21.2q ≠ 2.21.2p` |
| S2 | client | `scripts/tl.py:98` `EXPECT_VERSION = "2.21.2p"`; `references/API_CONTRACT.md:3` đóng dấu `2.21.2p` |
| S3 | action thiếu trong hợp đồng | `set(re.findall(r"case '([^']+)'", …))` trên `references/Code.2.21.2q.gs` ⇒ **77** tên phân biệt; tên nào không có dạng `` `<tên>` `` trong `API_CONTRACT.md` ⇒ thiếu **3**: `agent_creds_put`, `configView`, `regenRegistry` (đo 09:1xZ, Codex phản biện đo cùng số). Hai tên sau là bí danh camelCase sẵn có từ trước (`configView` ⇒ `doConfigView_`; `regenRegistry` chỉ trả `deprecated:true`), ngoài phạm vi; chỉ `agent_creds_put` là action mới của 2.21.2q |
| S4 | công cụ bump | `scripts/contract_check.py --bump 2.21.2q` trên bản sao: 4 tệp (`SKILL.md`, `API_CONTRACT.md`, `tl.py`, `tl_selftest.py`), +14/−14 dòng; thay CẢ ghi chú lịch sử (xem M1) |
| S5 | ca sẽ đỏ | `scripts/tl_selftest.py:24308` (`r210_skill_tro_kich_ban_va_gas_dung_ban`) đòi `sk.count("2.21.2p") >= 3` trên `SKILL.md` — bump xong số đếm 5 → 0 (Codex phản biện 05-11, tôi đo lại) |
| S6 | hướng dẫn deploy cũ | `INSTALL.md:52,78,110` bảo deploy `Code.2.21.2p.gs` / webapp `2.21.2p` |

## 2. Thay đổi (mỗi mục chiếu vào một đường dẫn ở §3)

- **M1 → `references/API_CONTRACT.md`**: dấu phiên bản hiện hành sang `2.21.2q` ở dòng đóng dấu (dòng 3: `(LIVE): \`2.21.2q\``,
  `ping.version=2.21.2q`, `tl.py EXPECT_VERSION=2.21.2q`) và đoạn cảnh báo lệch (dòng 5–6: `` `2.21.2q`: server đã trôi version ``,
  `Code.2.21.2q.gs` qua clasp -i). Dòng 3 thêm vế `⊕ **2.21.2q** +agent_creds_put (#1089)`.
  **GIỮ `2.21.2p`** ở sáu cụm lịch sử (tính năng RA ĐỜI ở 2p), mỗi cụm nguyên văn như trên base:
  1. `**2.21.2p ATOMIC registry RMW**` (dòng 3)
  2. `v2.21.2p tự khai \`expect_shrink\`` (dòng `reg_delete`)
  3. `**v2.21.2p KI-27** CHỈ ĐỌC` (dòng `reg_bak_list`)
  4. `**v2.21.2p KI-27**: thay TOÀN BỘ registry` (dòng `reg_bak_restore`)
  5. `v2.21.2p (r198/ADR-0014)` và `feature-detect ≥2.21.2p` (dòng `ingest_commit` — hai lần, cùng dòng)
  6. `` `regen2` (v2.21.2p: nhận thêm `` (dòng `regen2`)
  Được chạy `contract_check.py --bump 2.21.2q` rồi trả tay, hoặc sửa tay; kết quả đo bằng A1/A2. Duyệt TOÀN BỘ diff của tệp này,
  vì công cụ còn có regex sửa câu cảnh báo `HỎNG ở deploy` (`scripts/contract_check.py:76–80`).
- **M2 → `references/API_CONTRACT.md`**: thêm đúng một dòng bảng cho `agent_creds_put`, cạnh các action ghi khác: GET/POST =
  `**POST**`; bắt buộc `fileId, expect_md5, b64`; response `ok, md5, size` (khi ghi xong) và `ok=false, error` với sáu mã
  `AGENT_CREDS_NOT_CONFIGURED`, `AGENT_CREDS_FILEID_MISMATCH`, `EXPECT_MD5_REQUIRED`, `BLOB_SIZE`, `LOCK_BUSY`, `CAS_CONFLICT`
  (kèm `md5` hiện tại); ghi chú: chỉ ghi đè NỘI DUNG đúng tệp Script Property `TL_AGENT_CREDS_FILEID`, CAS theo `md5Checksum`
  trong script lock, không có chế độ ghi mù; v2.21.2q (#1089). Nội dung chép từ mục *Hợp đồng `agent_creds_put`* của
  `ops/specs/cloud-setup-p3-writeback-r1.md`, đối chiếu thân hàm `references/Code.2.21.2q.gs:344–364` (dispatch ở dòng 331).
- **M3 → `scripts/tl.py`**: `EXPECT_VERSION = "2.21.2q"`. Không đổi hằng `VERSION`.
- **M4 → `scripts/tl_selftest.py`**: literal ca `expect_version` sang `"2.21.2q"` (giữ chú thích, thêm "2.21.2q: +agent_creds_put");
  ca `r210_skill_tro_kich_ban_va_gas_dung_ban`: `sk.count("2.21.2p") >= 3` → `sk.count("2.21.2q") >= 3`, thêm vế
  `and "2.21.2p" not in sk` (cùng hình dạng vế `"2.21.2m" not in sk` sẵn có), chú thích "bản LIVE là 2.21.2q".
- **M5 → `SKILL.md`**: bốn dòng 22, 244, 247, 249 sang `2.21.2q` / `Code.2.21.2q.gs`. KHÔNG đổi header version (dòng 18).
- **M6 → `INSTALL.md`**: dòng 52, 110 sang `2.21.2q` / `Code.2.21.2q.gs`; dòng 78 thành "Các bản `.gs` tới 2.21.2p là lịch sử;
  bản cần deploy là `Code.2.21.2q.gs` và `ping` phải trả `2.21.2q`" — chuỗi `2.21.2p` DUY NHẤT được giữ trong `INSTALL.md` là
  cụm lịch sử `` Các bản `.gs` tới 2.21.2p là lịch sử ``.
- **M7 → `changelog.d/wp-1223.md`**: ghi chú thay đổi (protocol: worker không sửa `CHANGELOG.md`).

## 3. Write set

```yaml
write_set:
  - INSTALL.md
  - SKILL.md
  - changelog.d/wp-1223.md
  - ops/handoff/wp1223-g1-claude.md
  - references/API_CONTRACT.md
  - scripts/tl.py
  - scripts/tl_selftest.py
```

Diff PR: đúng **6 tệp** (handoff chỉ sống trên nhánh lease/handoff). Dự kiến ≤ 40 dòng thêm. Trần `ADR-0053` (`sensitive`: ≤ 6 tệp /
≤ 450 dòng thêm): **đạt**, không cần `nang_tran`.

**Worker KHÔNG sửa** `VERSION`, hằng `VERSION` trong `tl.py`, header `SKILL.md`, `CHANGELOG.md`, `RELEASE_MANIFEST.json`
(`docs/PROTOCOL_DA_PHIEN.md:855–865`, `docs/adr/0017-pr-github-la-ban-giao-va-dieu-phoi-chinh.md:54–61`). CI lane worker dùng
manifest tạm (`.github/workflows/ci.yml`, khối "LANE LAND vs LANE WORKER"); **phiên land** tái sinh `RELEASE_MANIFEST.json` trên
head PR trước khi merge, kẻo `release-verify strict (lane LAND)` đỏ trên master (CLAUDE.md §Quy ước deploy mục 5). Vì vậy packet
này không giao write set với lease #1099 (giữ `RELEASE_MANIFEST.json`, đo 08:3xZ 05-11) hay với #1224.

Trần lời gọi Codex: dòng khai `ADR-0055` ⇒ trần cứng **10**; ngân sách mềm **2**. Hai lượt liên tiếp chưa approve ⇒ Review
Rescue Checkpoint (`ADR-0037`), hỏi chủ kho trước lời gọi kế tiếp.

## 4. Nghiệm thu

Phép đo chuỗi theo L6 của `soan-spec`: mỗi tiêu chí có vế dương trên nội dung MỚI và vế âm trên nội dung CŨ; đếm theo TỪNG tệp
và TỪNG cụm; đo trên blob ứng viên (`git show <cand>:<path>`), cụm khớp là toàn bộ lời khẳng định trên một dòng của blob đã
neo băm.

| ID | phép đo | đột biến làm ĐỎ |
|---|---|---|
| A1 | `API_CONTRACT.md`: 400 byte đầu chứa `` `2.21.2q` `` (dương) và KHÔNG chứa `` (LIVE): `2.21.2p` `` (âm); `python scripts/contract_check.py --audit` rc 0 và in khớp `2.21.2q` | để dấu `2p` ở dòng 3 ⇒ ĐỎ |
| A2 | sáu cụm lịch sử của M1 có mặt NGUYÊN VĂN với `2.21.2p`, đếm từng cụm, mỗi cụm đúng số lần như base (cụm 5: hai lần trên dòng `ingest_commit`); không cụm nào xuất hiện dạng thay `2p`→`2q` | chạy `--bump` mà không trả tay ⇒ ĐỎ; trả tay sót một cụm ⇒ ĐỎ |
| A3 | `API_CONTRACT.md` có đúng 1 dòng bảng bắt đầu `` | `agent_creds_put` | ``, chứa `POST`, đủ 3 tham số và đủ 6 mã lỗi (đếm từng mã); phép đo S3 (tên `case` của `Code.2.21.2q.gs` không có dạng `` `<tên>` `` trong hợp đồng) ⇒ tập thiếu ĐÚNG BẰNG `{configView, regenRegistry}` (base: `{agent_creds_put, configView, regenRegistry}`) | xoá dòng ⇒ tập thiếu có `agent_creds_put` ⇒ ĐỎ; bỏ `CAS_CONFLICT` ⇒ ĐỎ |
| A4 | `scripts/tl.py`: dòng `EXPECT_VERSION = "2.21.2q"` đúng 1 lần, không còn dòng `EXPECT_VERSION = "2.21.2p"`; dòng `VERSION = ` không đổi so base | đổi lại `2p` ⇒ `r119_*` + `expect_version` ĐỎ |
| A5 | `python scripts/tl.py --selftest` N/N hai số bằng nhau; gồm `r119_api_contract_version_stamp_matches_expect`, `expect_version`, `r210_skill_tro_kich_ban_va_gas_dung_ban` | trên ứng viên, chèn lại một dòng `2.21.2p` vào `SKILL.md` ⇒ `r210` ĐỎ (vế âm mới có răng); trả `EXPECT_VERSION` về `2p` ⇒ `expect_version` ĐỎ |
| A6 | `SKILL.md`: `2.21.2p` = 0 lần, `2.21.2q` ≥ 4. `INSTALL.md`: `2.21.2p` đúng 1 lần và lần ấy nằm trong cụm `` Các bản `.gs` tới 2.21.2p là lịch sử ``; `2.21.2q` ≥ 3; ba chỉ dẫn hiện hành (dòng deploy `.gs`, dòng `ping` phải trả, dòng "Webapp cần deploy") mỗi dòng chứa `2.21.2q` (đếm từng dòng) | để sót một dòng chỉ dẫn ở `2p` ⇒ ĐỎ; xoá cụm lịch sử ⇒ ĐỎ |
| A7 | `git diff --numstat <base> <cand>`: đúng 6 tệp của write set (trừ handoff), không tệp nào ngoài; ≤ 450 dòng thêm; KHÔNG có `VERSION`, `CHANGELOG.md`, `RELEASE_MANIFEST.json` | thêm tệp thứ 7 hoặc sửa manifest ⇒ ĐỎ |
| A8 | bất biến (a): `git diff --check` rc 0; `python .claude/dev/packet_loop.py doctrine-scan --root .` rc 0; doc-claims-check như gate rc 0; delta `ruff check --select F scripts/tl.py` so base = 0 | — |
| A9 | lane worker: `release-verify` với manifest tạm như CI PR | — |
| A10 (sau land, phiên land) | trước merge: tái sinh `RELEASE_MANIFEST.json` trên head PR và `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` ⇒ `ok=true`, `expected == checked`; sau merge: gate master xanh gồm `release-verify strict (lane LAND)`; `tl ping` trên môi trường đã đo ở S1 KHÔNG còn in cảnh báo lệch | — |

Chạy thử trên base (05-11): A1, A3, A4, A6 ĐỎ đúng "chưa làm"; A2 vế dương xanh sẵn (cụm có trên base), răng đến từ đột biến
"bump không trả tay"; A5 xanh trên base (canh bất biến). A10 `chưa đo được` cho tới khi land.

## 5. Ngoài phạm vi (nợ có tên)

- `P3C-BUMP-THAY-CA-LICH-SU`: `contract_check.py --bump` thay mọi chuỗi phiên bản cũ, kể cả ghi chú lịch sử
  (`scripts/contract_check.py:64–80`). Sửa công cụ = packet riêng (Q10). GPT phản biện khuyên sửa; giữ nợ vì A2 đã bắt đúng lỗi này.
- `P3C-KHOA-CU-KHOA-MOI`: ca "khoá cũ → khoá mới" sửa `scripts/tl_gws.py` (dời từ P3, vòng 2 Q11 của P3). Packet riêng (Q5).
- Tài liệu dev-side (`references/DEV_TOOLING_GUIDE.md`, `references/DELTA_v1.19.md`, `docs/GOI_AGENT_DA_NEN.md`, `CLAUDE.md`):
  packet anh em #1224.
- Bump `VERSION` / `CHANGELOG.md` / manifest: việc của phiên land.

## 6. Hệ quả hành vi đã biết

Sau land, client đòi `2.21.2q` khớp tuyệt đối: môi trường nào còn webapp `2.21.2p` thì `tl ping` rc 3 + cảnh báo, và `profile_mgmt`
dừng phục hồi registry kể cả dry-run (`scripts/tl_core/profile_mgmt.py:99–109`, `scripts/tl_core/ops_misc.py:304–315`). Chủ kho xác
nhận (Q9, 05-11) chỉ có MỘT deployment webapp, deploy bằng `clasp deploy -i` giữ URL, và S1 đo nó đã ở `2.21.2q` ⇒ đây là hành vi
đúng, không phải hồi quy.

## 7. `hinh_dang_ke_thua`

`khong_ap_dung` — không phải packet khắc phục.

## 8. `chua_do_duoc`

- Endpoint của môi trường khác `env=code` của phiên soạn: chưa đo trực tiếp; dựa trên xác nhận Q9 của chủ kho (một deployment).
- Golden/doc-claims-check trên ứng viên: chưa có ứng viên; đo ở A8 khi thi hành.
