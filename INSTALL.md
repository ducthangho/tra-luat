# tra-luat — GÓI REFACTOR v1.22.0 — HƯỚNG DẪN CÀI

Refactor TẤT ĐỊNH HÓA VẬN HÀNH (giữ nguyên tư duy lõi): cô đọng bề mặt thao tác, chống
"đoán tham số", đánh số trình tự, gộp script. **Không đổi** nguyên tắc lõi (VBHN-first, dedup
nhiều lớp, verify nguyên văn, không bịa).

> ⚠ **Manifest dưới đây là layout GỐC v1.x (tham chiếu lịch sử).** Từ v1.22.34: bản `.gs` đời trước (2.21.1→2.21.2h) và
> các ghi chú dev cũ (MERGE_/DELTA_/PATCH_REPORT/…) ĐÃ chuyển ra `tra-luat-references-archive/` ngoài skill để gọn gói
> (≤200 file/import). Skill chỉ giữ bản LIVE `Code.2.21.2i.gs` + tài liệu được SKILL.md/RUNBOOK/code dẫn chiếu. Nguồn
> chân lý hiện hành: **VERSION + SKILL.md + CHANGELOG.md** (KHÔNG phải file-list này).

## Nội dung gói (overlay lên skill `tra-luat` hiện có)
```
SKILL.md                          ← LÕI MỚI (mệnh lệnh ngắn, ~140 dòng) — THAY file cũ
VERSION                           ← 1.19.3
references/API_CONTRACT.md        ← (1) hợp đồng API sống, target webapp 2.21.2i  [MỚI]
references/PATCH_v2.21.1.gs.md    ← vá .gs F1–F16c → webapp 2.21.1                  [MỚI]
references/CODE_2.21.2_FIXES.md   ← 7 fix Apps Script thật + VBHN-first 2.21.2b → bump [MỚI]
references/REALRUN_4LAWS_SOURCE_MAP_FIXES.md ← ghi chú source-map theo log chạy thật 4 luật [MỚI]
references/VBHN_QT5_VERIFICATION.md ← cổng verify VBHN theo trích yếu/gốc/năm [MỚI]
references/VBHN_OFFICIAL_FIRST.md ← không tự ghép VBHN làm bản dùng; official-first [MỚI]
references/VBHN_HYGIENE_GUARDS.md ← guard hygiene/source-map theo log 4 luật [MỚI]
references/APPSSCRIPT_MANIFEST.open-egress.json / .restricted-egress.json         [MỚI]
references/RUNBOOK.md             ← (2) trình tự khởi động + cổng, đánh số          [MỚI]
references/DOCTRINE_APPENDIX.md   ← thân SKILL.md CŨ (changelog v1.x→v1.15.7) giữ nguyên [MỚI]
scripts/tl.py                     ← (3) CLI hợp nhất (lệnh con)                      [MỚI]
scripts/gen_instructions.py       ← sinh/audit Instruction Claude/NLM có SKILL_OF_RECORD [MỚI]
scripts/nlm_cli.py                ← adapter CLI `nlm` (fast-lane NLM, --skip-freshness, không qua MCP) [MỚI]
scripts/contract_check.py         ← tự bắt trôi version webapp vs hợp đồng          [MỚI]
scripts/apply_gs_patches.py       ← áp patch .gs (anchor nghiêm ngặt) → Code.gs 2.21.1     [MỚI]
references/Code.2.21.1.gs         ← FULL Code.gs đã hợp nhất + node --check (deploy thẳng)  [MỚI]
references/Code.2.21.2b.gs        ← FULL Code.gs deploy-ready sau 7 fix + VBHN-first rank     [MỚI]
references/Code.2.21.2c.gs        ← FULL Code.gs hotfix regen2/reg_clear/manifest VBHN       [MỚI]
references/Code.2.21.2d.gs        ← FULL Code.gs (lịch sử): safe issue_year parser            [MỚI]
references/Code.2.21.2e.gs        ← FULL Code.gs (lịch sử): slot theo nlm_notebook_id base-fallback [MỚI]
references/Code.2.21.2f.gs        ← FULL Code.gs (lịch sử): Cách B chưa kèm writeconfig [MỚI]
references/Code.2.21.2g.gs        ← FULL Code.gs (lịch sử): Cách B + writeconfig giữ/merge block profiles v2 [MỚI]
references/Code.2.21.2i.gs        ← FULL Code.gs target (regen2 own-scope + blowup guard) [MỚI]
references/Code.2.21.2h.gs        ← bản trước guard, giữ tham chiếu lịch sử
references/VBHN_YEAR_PARSER_SAFE.md ← ghi chú lỗi parser năm VBHN và quy tắc an toàn         [MỚI]
references/RA_SOAT_LESSONS_2026_06.md ← bài học HD06: không đi tắt qua reg_get raw           [MỚI]
references/STALE_RELATION_GUARD.md ← guard sửa đổi đã có nhưng registry thiếu goc/sua_doi      [MỚI]
references/EXTERNAL_INGEST_GATE.md ← research_* chỉ discovery; Instruction buộc đọc skill/QT-3 [MỚI]
references/MULTI_CORPUS_PROFILE_V1_18.md ← profile đa-corpus, link tải, slot theo notebook [MỚI]
references/GS_2.21.2E_MULTI_CORPUS_SLOT.md ← ghi chú deploy .gs slot notebook v1.18           [MỚI]
references/DELTA_v1.19.md         ← Cách B: registry/manifest riêng theo profile + doctrine §C.1 [MỚI]
references/PROFILE_SCOPE_V1.19.2.md ← fallback env-driven tôn trọng profile + writeconfig 2.21.2h [MỚI]
references/MERGE_V1.19.2.md       ← quyết định best-of-both v1.19.2                            [MỚI]
references/PATCH_REPORT.sample.md ← report thật khi áp (32/32, audit 5/5, node OK)          [MỚI]
```

> Deploy `references/Code.2.21.2p.gs`; sau deploy webapp phải là **2.21.2p**. Chạy `tl ping` + `contract_check.py --audit` để xác minh.

## 4 hướng đã làm
1. **Hợp đồng API sống** (`references/API_CONTRACT.md`): ~70 action, GET/POST + tham số bắt buộc/
   tùy chọn + khóa response + gotcha; bảng BẪY THAM SỐ; danh sách `confirm=yes` & action POST.
   Đóng dấu **2.21.2h** (xác minh `ping.version`). Đã sửa 3 lệch so với ghi chú bàn giao:
   - `reg_upsert`/registry dùng **`sohieu`** (KHÔNG `so_hieu`); chỉ manifest JSON mới `so_hieu`.
   - `find`→`rows`, `search`→`matches`.
   - `move`: `folderId`\|`cat`, KHÔNG `destFolderId`; `removeFromParent` bị bỏ qua (tự tính).
2. **Runbook đánh số** (`references/RUNBOOK.md`): config→token→ping(cổng)→manifest→index→các cổng
   vận hành; gắn cố định quy tắc đọc-cache-tiết-kiệm-token + hành vi ĐỐI CHIẾU NGAY.
3. **CLI `tl`** (`scripts/tl.py`): `ping/boot/locate/instruction-audit/status/extract/ingest/register/manifest/rasoat`,
   bọc `gas.py` + module đã kiểm thử (boot, preingest_gate, manifest_build), không reimplement.
   `contract_check.py` chống trôi version. Gói đóng dấu live/post-deploy **2.21.2i** (đã xác minh `ping.version=2.21.2i`, `registry_schema=reg_cols_row_kind_v1`).
4. **Tinh giản doctrine**: SKILL.md 1544 dòng changelog → LÕI mệnh lệnh + `DOCTRINE_APPENDIX.md`
   (biện luận/lịch sử giữ nguyên văn). Khi mâu thuẫn: LÕI + API_CONTRACT + RUNBOOK thắng phụ lục.

## Apps Script — bản vá v2.21.1 (TÙY CHỌN, có deploy)
`references/PATCH_v2.21.1.gs.md` — HỢP NHẤT F1–F7 rà soát được trên webapp 2.20.0:
- **F1** `meta_find` + `find`-fulltext đang CHẾT (doSearch_ đổi sang registry v2.17.0 nhưng 2 chỗ này
  vẫn truyền Drive-query) → thêm `driveSearch_` khôi phục.
- **F2** alias `configView` (boot.py gọi action không tồn tại).
- **F3** một hằng `APP_VERSION` (đang rải rác 2.20.0/2.14.0/2.11.0/2.15.0).
- **F5** treeHash manifest_export cùng cơ sở corpus với regen2 (đang lệch → so luôn khác).
- **F4** appProperties về chữ thường (regen2 nhặt đúng sohieu). **F6** khai tử regen legacy. **F7** gỡ public-share mirror chứa token.
> Phần LÕI vận hành (SKILL/CLI/reference) đóng dấu live/post-deploy 2.21.2i (bản `.gs` hiện hành = `Code.2.21.2i.gs`).
> Các bản `.gs` tới 2.21.2o là lịch sử; bản cần deploy là `Code.2.21.2p.gs` và `ping` phải trả `2.21.2p`.

## Tạo `Code.gs` 2.21.1 hợp nhất (hướng (2) — apply_gs_patches.py)
Thay vì dán tay 25 cụm vá, dùng script có ANCHOR NGHIÊM NGẶT (dry-run mặc định):
```bash
# 1) DRY-RUN: xem áp được gì, còn gì MANUAL, audit, không ghi
python scripts/apply_gs_patches.py --in /duong/dan/Code.gs
#    → đọc PATCH_REPORT.md: phần "Tự động" (✅/❌ theo anchor), "MANUAL", "Static audit", node --check
# 2) GHI (chỉ khi mọi patch auto ✅; --force để ép ghi dù có ❌):
python scripts/apply_gs_patches.py --in /duong/dan/Code.gs --write --out Code.2.21.1.gs
# 3) Áp các mục MANUAL (rewrite hàm lớn/định-vị-đơn) theo references/PATCH_v2.21.1.gs.md
# 4) node --check (script tự chạy) + Deploy New version (giữ URL+token)
# 5) RUNTIME checklist (chỉ verify thật được sau deploy):
#    ping→2.21.1 · perm_list config (hết 'anyone') · organize cat=99 (ok:false) · regen2+manifest_export treeHash khớp
```
> Script TỰ ĐỘNG phần DỄ SÓT nhất (thống nhất version, global `rootId_()` nhiều vị trí, chèn helper, F8 scoped,
> các vá ngắn). Phần MANUAL là rewrite hàm khu trú (1 chỗ/hàm) — anchor lớn nên để dán theo doc, tránh gõ nhầm.
> Anchor khớp 0/≥2 lần ⇒ patch FAIL, KHÔNG ghi nửa với (an toàn hơn dán tay).
> ĐÃ CHẠY trên code.gs deploy thật: **41/41 tự động, audit 24/24 (gồm F5), node --check PASS, status DEPLOYABLE_CANDIDATE** → xem `references/Code.2.21.1.gs`
> (deploy thẳng được) và `references/PATCH_REPORT.sample.md`. MANUAL còn lại CHỈ F16c (chọn manifest). Script có gate DEPLOYABLE_CANDIDATE/NOT_DEPLOYABLE_YET + exit code nghiêm.

## Cài (chỉ chạm bộ skill — KHÔNG deploy gì lên Google)
> ⚠️ **ĐÂY LÀ GÓI OVERLAY, KHÔNG phải full package.** `scripts/tl.py` + `contract_check.py` import các
> script NỀN của skill `tra-luat` đã có sẵn: **`gas.py`, `boot.py`, `manifest_build.py`, `preingest_gate.py`,
> `standardize_name.py`, `nlm_push.py`, `nlm_sources.py`, `registry_orchestrator.py`, `backfill_*`, `rasoat_*`**.
> Chép overlay vào skill ĐẦY ĐỦ hiện có — KHÔNG copy vào project trống (sẽ vỡ import ngay).
> Hai script overlay (`tl.py`, `contract_check.py`) chỉ dùng **thư viện chuẩn** — không cần `pip install`.
> `requirements.txt` mà SKILL.md nhắc là của BỘ SKILL NỀN (cho normalize_document/keywords… ), không thuộc overlay.
1. Sao lưu skill hiện tại (đề phòng): copy `tra-luat/` ra chỗ khác.
2. Chép đè theo cây trên vào bộ skill `tra-luat` (giữ các script/reference cũ khác nguyên vẹn —
   gói này chỉ THÊM file mới + THAY `SKILL.md` và `VERSION`).
3. Cập nhật lại bộ skill ở nơi anh vẫn quản lý/đăng skill (cùng chỗ đã version v1.15.x).
4. Webapp cần deploy **2.21.2p** (từ `references/Code.2.21.2p.gs`); contract + `tl.py EXPECT_VERSION` đồng bộ 2.21.2p.

## Config (kèm trong gói) — `tra_luat_config.v2.json`
> ⚠️ **File này CHỨA TOKEN webapp (bí mật).** KHÔNG chia sẻ/đẩy gói lên nơi công khai. Chỉ dùng cục bộ.

Gói có sẵn `tra_luat_config.v2.json` (schema 2: `webappUrl` + `token` + `profiles`). Dùng theo 1 trong 2 cách:
```powershell
# (A) trỏ trực tiếp mỗi lệnh:
python scripts\tl.py --config tra_luat_config.v2.json ping
# (B) lưu về vị trí mặc định (khỏi gõ --config):
Copy-Item tra_luat_config.v2.json "$HOME\.tra_luat_config.json"
python scripts\tl.py ping
```

## Kiểm sau cài (offline trước, rồi online)
```bash
cd tra-luat
python scripts/tl.py --selftest             # kỳ vọng 66/66
python scripts/gen_instructions.py --selftest # kỳ vọng 14/14
python scripts/contract_check.py --selftest # kỳ vọng 2/2
# online (creds từ tra_luat_config.v2.json kèm gói, hoặc ~/.tra_luat_config.json):
python scripts/tl.py --config tra_luat_config.v2.json ping   # version PHẢI 2.21.2i
python scripts/contract_check.py             # ✓ KHỚP 2.21.2i
python scripts/tl.py --config tra_luat_config.v2.json boot   # dựng manifest_index.json
```

## Quy trình DUY TRÌ (khi webapp .gs đổi sau này)
1. Dán `.gs` mới → Deploy New version (giữ URL+token) → `regen2 confirm=yes` → `manifest_export`.
   Gói đã khép post-deploy `2.21.2i` (đã xác minh `tl ping`=2.21.2i, cột `row_kind` có). Nếu deploy lại, kiểm `ping` và chạy `contract_check.py --audit`.
4. `python scripts/contract_check.py` phải báo ✓. (Nó tự đọc version từ API_CONTRACT.md.)

## Lưu ý còn mở (không chặn cài)
- **NLM `source_list_drive`**: MCP wrapper VẪN chưa cho `skip_freshness` → timeout trên VBQPPL.
  Đã ghi vào RUNBOOK §A4 + API_CONTRACT §9. Khi nào wrapper vá xong thì cập nhật 2 chỗ đó.
- **`tl ingest`** mặc định DRY (an toàn QT-2/QT-3); `--apply` chạy `copy_convert`+`organize`, còn
  bước NLM (`source_add`+`map_set`) vẫn làm qua MCP (đúng thiết kế, KHÔNG webapp).
- **External ingest gate:** `research_start/research_status` chỉ để phát hiện URL. Không dùng
  `research_import`/`source_add(url)` nạp thẳng VBQPPL vào notebook tạm hoặc notebook chính; phải đi
  Drive → convert → tên chuẩn → folder đúng → verify → `nlm_push`, sau khi người dùng duyệt đích.
- **Multi-corpus profile:** dùng `--profile vbthuong profile-info --json` cho văn bản thường/dự án; profile quyết định folder/notebook/registry/manifest. `vbqppl` chỉ là nền lấy token/webapp và fallback.
- **Drive MCP ngoài corpus:** wrapper chỉ hỗ trợ query `fullText contains '...'` và `parentId = '...'`; không dùng `name/title contains` (sẽ lỗi `Unsupported query field: name`).
- **`tl rasoat`** hiện là passthrough tới script rà soát hiện có; gộp sâu hơn (merge
  rasoat_index/backfill/nlm_describe_cache thành một pipeline) là bước tiếp theo nếu cần.

## Vận hành sau khi boot — rà soát/hygiene trong overlay

```bash
python scripts/tl.py --config config.json boot --json
python scripts/tl.py --config config.json extract --sohieu 18-VPQH --dieu 119 --dieu 205
python scripts/tl.py --config config.json exists "06/2022/QH15" --json
python scripts/tl.py --config config.json source-map "74/2025/QH15" "41/2024/QH15" "84/2015/QH13" "Bảo hiểm y tế"
python scripts/tl.py --config config.json vbhn-check --subject "an toàn vệ sinh lao động" --goc "84/2015/QH13" --year 2024 --json
python scripts/tl.py --config config.json vbhn-verify --text-file official.txt --expect-title "an toàn vệ sinh lao động" --expect-goc "84/2015/QH13" --expect-year 2024 --official-required --json
python scripts/tl.py vbhn-compare --official-text official.txt --candidate-text assembled.txt --focus "Điều 53" --json
python scripts/tl.py instruction-audit --generate --target nlm --print-text
python scripts/tl.py --profile vbthuong profile-info --json
python scripts/tl.py link-priority "https://thuvienphapluat.vn/..." "https://congbao.chinhphu.vn/..." --json
python scripts/tl.py --profile vbthuong slot-audit --notebook-id fec6c125-e01c-433d-aed5-666c16540dd8 --json
python scripts/tl.py --config config.json hygiene scan --json
python scripts/tl.py --config config.json hygiene plan 18-VPQH --json
python scripts/tl.py --config config.json locate "bảo hiểm y tế" --refresh
# Chỉ khi đã kiểm danh sách và muốn move vào QUARANTINE:
python scripts/tl.py --config config.json hygiene plan 18-VPQH --apply --confirm yes --json
```

`source-map`/`locate`/`hygiene` dùng manifest cache nếu có; không trash, chỉ `move cat=QUARANTINE` khi có `--apply --confirm yes`.
Nếu `source-map` báo `NO_VERIFIED_VBHN_IN_CORPUS`, không được kết luận "không có VBHN"; chạy `tl vbhn-check` và QT-5 web theo trích yếu/chủ đề + "hợp nhất". Nếu báo `VBHN_NUMBER_REUSE_RISK`, phải chạy `tl vbhn-verify --official-required` hoặc verify ngày ban hành + tiêu đề + dòng hợp nhất vì số VBHN có thể tái sử dụng theo năm.
Nếu chưa có VBHN chính thức, hỏi người dùng nạp vào `_HOP_NAP`; không tự ghép VBHN để register/NLM làm bản dùng. Bản tự ghép chỉ được dùng tạm và phải so bằng `tl vbhn-compare` khi official xuất hiện.
Nếu kết quả có `WARN=OMNIBUS_NARROW_TITLE_CHECK` hoặc `TITLE_METADATA_MISMATCH`, không dùng ngay theo tên file; chạy `tl status <sohieu>` và/hoặc `tl hygiene plan <query> --json` để chọn canonical/VBHN.

Ưu tiên mọi thao tác qua `python scripts/tl.py ...`. Client fallback tối thiểu, nếu cần debug thấp, dùng `python scripts/_fallback/gas.py ACTION key=value`; cú pháp cũ `gas.py get ACTION` không còn là đường chuẩn.


## v1.17.15 — ghi chú cài đặt
```bash
pip install -r requirements.txt  # overlay core (tl.py/contract_check.py) vẫn stdlib; dòng này
                                 # cài `pypdf` cho ĐƯỜNG NẠP PDF — thiếu là CHẶN mọi .pdf (r319)
python scripts/tl.py --config config.json ping  # phải ra 2.21.2i
python scripts/tl.py --config config.json extract --sohieu 18-VPQH --find "Phụ lục IV"
```


## v1.17.17 — kiểm tra sau boot

```bash
python scripts/tl.py --config config.json boot --json
python scripts/tl.py --config config.json vbhn-normalize --json
python scripts/tl.py --config config.json hygiene scan --json
```

`vbhn-normalize` chỉ báo cáo, không ghi Drive/NLM.

## v1.17.18 — VBHN cấp Bộ và năm ban hành

Văn bản loại E/cấp Bộ cũng phải có năm trong metadata và tên chuẩn. Mẫu tên report-only:

```text
VBHN_<so>-VBHN-<co_quan>_<year>_<ten_rut_gon>
```

Ví dụ: `VBHN_09-VBHN-BYT_2024_<ten_rut_gon>`, `VBHN_05-VBHN-BGDDT_2023_<ten_rut_gon>`.
Nếu thiếu `issue_year`, phải backfill từ tên file hoặc dòng địa danh-ngày tháng trong văn bản trước khi đổi tên. `tl vbhn-normalize --json` và `hygiene scan` sẽ gắn cờ `VBHN_MINISTRY_MISSING_YEAR`/`VBHN_MINISTRY_NAME_MISSING_YEAR`; mọi rename/quarantine vẫn là thao tác ghi riêng, chờ xác nhận.


### v1.17.19 safe issue_year parser
- (Lịch sử v1.17.19) `references/Code.2.21.2d.gs` sửa parser `issue_year`; logic này tiếp tục được giữ trong `2.21.2i`.
- Gói hiện đã giữ live/EXPECT `2.21.2d`; nếu ping khác thì dừng và đối chiếu deploy.

### v1.17.25 external-ingest + Instruction gate
- Từ log Nghị định 129/2025: không được tạo notebook tạm/nạp PDF thẳng bằng `research_import`; `research_*` chỉ discovery.
- Thêm `scripts/gen_instructions.py` thật và `tl instruction-audit`; Instruction sinh ra phải có `SKILL_OF_RECORD`, `ingest_handoff`, `confirm_gate_web`, official-first, ưu tiên docx/GDoc, notebook đang dùng.
- Nếu đã có notebook tạm, coi là quarantine: hỏi người dùng trước khi xóa/chuyển nguồn; không tự xóa.

### v1.17.24 amendment gate best-combined
- Hợp nhất thêm nhánh `amendment_gate`: `source-map` tự phát hiện `AMENDMENT_CANDIDATE_IN_CORPUS`/`UNLINKED_AMENDMENT_CANDIDATE` và trả `PAUSE_AND_ASK_USER`.
- Thêm `tl exists <query> --json`: tìm hiện diện/nguồn liên quan bằng `source-map` chuẩn hóa; không thấy thì `UNKNOWN_NOT_ABSENT`, không kết luận vắng mặt.
- `tl vbhn-check --goc <số hiệu>` tự suy trích yếu từ manifest nếu thiếu `--subject`, giúp sinh query web tốt hơn.

### v1.17.22 stale relation guard
- Thêm `tl relation-check --base <số hiệu gốc> --subject <trích yếu> [--amendment <số hiệu sửa đổi>] --json` để bắt văn bản sửa đổi đã có trong corpus/NLM nhưng registry thiếu `goc/sua_doi`.
- Khi phát hiện văn bản đang rà đã bị sửa đổi/lỗi thời, phải hỏi người dùng nạp/ghi registry ngay; không đưa vào mục xử lý sau nếu chưa chốt nguồn.
- `vbhn-check`/`relation-check` gợi ý cả query web đơn giản kiểu `"luật <chủ đề>" "hợp nhất"` và `site:thuvienphapluat.vn ...` để không bỏ sót VBHN ngoài corpus.

### v1.17.21 lessons hardening
- Không kết luận "không có trong nguồn" từ `gas.py reg_get name_contains=...`. Lệnh này khớp chuỗi nguyên văn, phân biệt dấu/gạch nối/gạch dưới và có thể bị cắt kết quả.
- Quy trình bắt buộc: `tl source-map "<tên/chủ đề>"` + `tl locate/status <số hiệu>` trước khi kết luận vắng mặt.
- `hygiene scan --json` có thêm `duplicate_identity_groups` để giảm nhiễu so với `duplicate_sohieu_groups_raw`; `NLM_STATUS_MISMATCH` chỉ là cảnh báo chuẩn hóa metadata, không phủ nhận khả năng query nếu có `nlm_source_id`.

### v1.17.20 registry hygiene parity
- `registry_hygiene.py` dùng cùng nguyên tắc parser năm an toàn như `tl.py`.
- Khi chạy hygiene độc lập, entry VBHN thiếu năm trong tên/ngày ban hành nhưng có `tukhoa = Luật 84/2015/QH13` vẫn phải bị gắn cờ thiếu năm.
- Nếu metadata đã có `issue_year=2024` nhưng tên chỉ chứa năm nguồn như `84-2015`, vẫn gắn `VBHN_NAME_MISSING_YEAR`; tên phải có đúng năm ban hành VBHN.


## v1.18.0 multi-corpus profile + link priority + slot guard

- Thêm config v2/profile: đọc `tra_luat_config.json` VBQPPL trước để lấy `webappUrl/token`, rồi overlay `--profile`/`TL_PROFILE`.
- Văn bản thường dùng profile riêng (`vbthuong`) với folder/notebook/registry/manifest riêng; không mặc định nạp vào VBQPPL.
- Thêm `tl profile-info`, `tl link-priority`, `tl slot-audit`; cache manifest tách theo profile.
- Link tải cho người dùng ưu tiên TVPL → LuatVietnam → Công báo → official khác; canonical vẫn official-first.
- Đặc tả .gs/registry: ghi `nlm_notebook_id`, `nlm_slots/nlm_preflight` chỉ đếm notebook đích. Gói này không tự deploy .gs.

## v1.17.26 combined external-ingest + instruction-audit gate

- Trước mọi nạp nguồn web/NLM-native, chạy `tl external-ingest <url> ... --json` để kiểm kế hoạch. Lệnh này chỉ kiểm, không ghi Drive/NLM.
- `research_start/research_status` chỉ dùng để phát hiện URL; `research_import/source_add(url)` không được dùng để nạp VBQPPL làm nguồn canonical.
- Instruction dùng cho Claude Project/NLM phải qua `tl instruction-audit` hoặc sinh bằng `tl instructions`/`scripts/gen_instructions.py`; thiếu `SKILL_OF_RECORD`, `ingest_handoff`, `confirm_gate_web` thì không dùng.
