# DOC-CLAIMS-DAU-CHAM r3 — doc-claims-check L1 kiểm đúng đường dẫn bắt đầu bằng dấu chấm

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

Đặc tả đóng băng. Muốn đổi thì soạn `DOC-CLAIMS-DAU-CHAM-r4.md`, không sửa đè. Đặc tả KHÔNG cấp việc: cần Packet Issue
#1326 và lease còn hiệu lực (`docs/PROTOCOL_DA_PHIEN.md` §3.2, §4).

| trường | giá trị |
|---|---|
| packet_id | `DOC-CLAIMS-DAU-CHAM`, revision 3, generation 1. Lease khai đúng `packet_id: DOC-CLAIMS-DAU-CHAM` và `revision: 3`; tiêu đề H1 của tệp này là khai báo định danh theo grammar của `ADR-0063`. Thay r2 (sha256 `bf8557c2bfd26cfa4e554f8e0481f6633bebd4321f86d080f5ad43583a3b6382`, review đặc tả lượt 2 approve, được chủ kho duyệt băm ngày 15-11-2026 trên #1326; sau đó `master` land #1265 thêm `ADR-0066` trỏ tệp policy change-impact, mục 11; lời duyệt ấy neo băm r2 nên không chuyển sang bản này) và r1 (sha256 `f7d308db1119299dcfffa0d8c31d18f7db5b49334a60c965a31bc3037a7be738`, review đặc tả lượt 1 `changes_requested`: một P2, năm P3; chưa được chủ kho duyệt); thay đổi ở mục 10 và 11 |
| packet_issue | #1326 |
| nguon_cap_viec | Chủ kho chỉ đạo trong phiên điều phối GIAM-HOI ngày 15-11-2026 (giờ Việt Nam), nguyên văn: *"Mở packet sửa lỗi doc-claims-check"*. Lỗi lộ ra khi ứng viên `GIAM-HOI-P2-ADR-E1-E5` r10 (H `093acd430da9328725e5a91d177e4b45338137cc`) làm đỏ bước `doc-claims-check --strict` của CI; mục 21 của `ops/specs/GIAM-HOI-P2-ADR-E1-E5-r11.md` (nhánh `ops/spec-giam-hoi-p2-r11`, commit `d26151370b9a86eb495457193e1a440e0bbeb764`) ghi nguyên nhân. Vòng hỏi 1 (ba câu Q1–Q3, mục 3) chủ kho trả lời *"Theo khuyến nghị"*; câu hỏi E3 về `ADR-0066` (mục 11) chủ kho trả lời *"Thêm cặp thứ 9 (Recommended)"* |
| review_class | `sensitive`: packet đổi hành vi của bước gate CI `doc-claims-check --strict` (job `gate`, `.github/workflows/ci.yml`), tức gate lifecycle (protocol §8). Cùng lớp với tiền lệ `DOC-CLAIMS-XOA` (#1121) |
| base | `origin/master` lúc cấp lease. r3 đo trên `815b9ac76a10fdd30516c9cef7ca93448cbbd923` (tree `b76a912d76e911b697de235934f0362e49750d56`, 16-11-2026); r1, r2 đo trên `116d7767a1ac5628663ef11d1287fce83f491892`. Giữa hai base, `.gitignore` và `scripts/tl_core/workflow.py` không đổi |
| executor | `claude`: Claude Code CLI, model yêu cầu `claude-fable-5-2`, effort `high`, môi trường `local`, theo Q3. Adapter `.claude/skills/work-packet/SKILL.md`. Model thực phục vụ lấy từ `modelUsage` của lượt chạy, không suy từ cấu hình |
| reviewer | `codex`: Codex CLI qua `.claude/dev/launcher.py run`, phiên mới, chỉ đọc, không fork context của executor, model yêu cầu `gpt-6-astra`, effort `xhigh`. Họ `openai` khác họ `claude` của executor ⇒ mức `cross_approved`, đủ cho lớp `sensitive` (protocol §8) mà không cần chủ kho audit SHA ứng viên. Biên nhận của lượt (`run.json`, stdout) là đầu vào K4 đường model của `kiem-merge`. Cộng connector `@codex review` trên PR (`ADR-0060` M6) |
| luật merge | `ADR-0060`, mặc định theo `ADR-0062`. Chủ kho duyệt merge một lần neo SHA (M7) — E2: quyền duyệt merge còn thuộc chủ kho theo M7 cho tới khi cơ chế tự merge của `ADR-0067` có hiệu lực theo bảng chuyển tiếp của ADR ấy |
| windows | `required`: `ADR-0060` M3 bước 2 — tệp test mới thêm dòng chứa `subprocess` và `pathlib` để dựng kho git tạm (cùng lý do với tiền lệ #1121). Cách chạy ở nghiệm thu N6 |
| full_mutant_audit | không áp: diff không chạm `.claude/dev/**`, `ops/**/*.py`, `.github/workflows/**` (`ADR-0060` M9) |
| pham_vi_e | không chạm E4, không chạm E5 (`docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md`): không hành động ra ngoài kho, không đổi thẩm quyền, không sửa cổng cấp lease hay cổng merge. Packet không thuộc Mission nên đặc tả chờ chủ kho duyệt băm — E2: quyền duyệt băm đặc tả ngoài Mission thuộc chủ kho (L7 của `.claude/skills/soan-spec/SKILL.md`) |

## 1. Số đo

Đo trên base r3 ở trên (16-11-2026), clone đủ lịch sử, trừ chỗ ghi khác, bằng một probe dùng chính `_doc_claims_targets`, `_doc_claims_mask`,
`_DOC_CLAIMS_SPAN_RE`, `_DOC_CLAIMS_PATH_RE`, `_DOC_CLAIMS_EXT_RE`, `_DOC_CLAIMS_TRIM`, `_doc_claims_noisy`,
`_doc_claims_is_historical` của `scripts/tl_core/workflow.py`. "Lần" là **lần xuất hiện của một token trong span backtick**
(một token trên một dòng là một lần); "claim phân biệt" là số chuỗi khác nhau. Mốc giờ (UTC) ghi ở từng dòng. Checkout đo là
**checkout sạch**: không có thư mục fixture sinh tại chỗ `references/golden/fixtures/` (thư mục ấy chỉ có sau khi chạy
`golden-test`, và khớp `.gitignore:19`), trừ chỗ ghi khác.

| # | sự kiện | số đo |
|---|---|---|
| S1 | tệp được quét (01:49Z 16-11) | 131 tệp (targets mặc định của `doc-claims-check`) |
| S2 | token đường dẫn bắt đầu bằng dấu chấm, không phải `./`, `../` (`.claude/…`, `.github/…`, `.agents/…`…), qua được bộ lọc nhiễu, `_DOC_CLAIMS_PATH_RE` và luật phần mở rộng (01:4xZ 16-11) | **189** lần; L1 hiện tại không kiểm đúng lần nào: `strip(_DOC_CLAIMS_TRIM)` cắt dấu chấm đầu, đoạn đầu còn lại không khớp mục gốc nào nên bị bỏ qua; riêng đoạn đầu `agents` trùng thư mục gốc `agents/` nên token `.agents/…` bị kiểm dưới tên sai (ca của P2 r10) |
| S3 | S2 nếu giữ dấu chấm và kiểm theo gốc kho với cùng bộ lọc mục gốc (01:4xZ 16-11) | 157 lần có thật (cả 157 nằm trong tree của base); 17 lần đoạn đầu không phải mục gốc (`.docx/.pdf`, `.exe/.cmd/.bat`, `.md/.txt`…; `.metaswarm/…`, `.tl_state/…`); 4 lần thiếu ở tài liệu lịch sử (3 lần tệp đã xoá trong `CHANGELOG.md`: `.claude/dev/duyet_danh_tinh.py` hai lần, `.github/workflows/duyet-khac-danh-tinh.yml` một lần; 1 lần `.claude/.packet_state/gen2`); 11 lần thiếu ở tài liệu sống (10 lần `.github/coordination/…`, 1 lần `.claude/.packet_state/` ở `docs/research/2026-10-16-y-tuong-tu-context-mode.md`) |
| S4 | `.gitignore` và dấu `/` cuối (07:3xZ 15-11; `.gitignore` không đổi tới base r3) | `git check-ignore --no-index -- .claude/.packet_state` rc 1; `… -- .claude/.packet_state/` rc 0 (`.gitignore:32`); `… -- .claude/.packet_state/gen2` rc 0. Mẫu thư mục chỉ khớp khi chuỗi hỏi giữ `/` cuối hoặc là đường bên trong |
| S5 | 10 lần `.github/coordination/…` ở tài liệu sống (01:4xZ 16-11) | đúng 9 cặp (tài liệu, đường dẫn) ở mục 2 M1(e): cặp 1–8 mỗi cặp một lần, cặp 9 (`ADR-0066`, dòng 30 và 49) hai lần. `ADR-0066` trỏ tệp policy có chủ đích: thuật toán admission của nó coi mục ấy là vắng hoặc có mode, kiểu, OID. Hai tệp đích không có trong tree base và không có trong lịch sử đi được từ base; chúng có trên nhánh bên `codex/f3-02-impact-policy` (commit `a55efcdfe18f8e924335e1d2d030e8fd65f6c077`, 09-08-2026), chưa land. Đó là policy change-impact mà `ADR-0032` (Accepted) mô tả |
| S6 | token `./`, `../` qua được bộ lọc (01:50Z 16-11) | 13 lần; L1 hiện tại kiểm **0** (dấu chấm bị cắt nên không khớp `_DOC_CLAIMS_RELPATH_RE`, nhánh `body.startswith(".")` không bao giờ chạy). Nếu kiểm theo thư mục của tài liệu: 7 có, 3 thiếu ở tài liệu lịch sử, 3 thiếu ở tài liệu sống (`./tl_secrets.enc` hai lần ở `references/COWORK_PROJECT.md` — đường trong thư mục dự án Cowork, không trong kho; `./claude-code-best-practice/best-practice` ở `references/DEV_TOOLING_GUIDE.md` — khớp `.gitignore:31`) |
| S7 | advisory L1 trên base (01:49Z 16-11, checkout sạch; cùng số trên `116d776` lúc 07:40Z 15-11) | 162 lần, 98 claim phân biệt (lý do `PATH_DELETED_IN_HISTORICAL_DOC`, `PATH_MISSING_IN_HISTORICAL_DOC`); trong đó 2 lần, 1 claim phân biệt — `references/golden/fixtures/` ở `CHANGELOG.md:1278` và `:10985` — khớp `.gitignore:19`. Trong checkout đã chạy `golden-test` (thư mục fixture tồn tại) cùng lệnh ra 160 lần, 0 khớp `.gitignore`: con số phụ thuộc thư mục sinh tại chỗ, không phụ thuộc tree |
| S8 | `doc-claims-check --strict --json` toàn kho trên base (01:49Z 16-11) | rc 0, `flags: []`, 131 tệp |
| S9 | fixture golden `doc_claims_check_fixture` (sinh từ mã, `scripts/tl_core/workflow.py` khối `doc_claims = (...)`) (04:5xZ 15-11; `workflow.py` không đổi tới base r3) | 0 token đường dẫn bắt đầu bằng dấu chấm trong span; cờ L1 duy nhất của fixture là `references/KHONG_CO_FILE.md`, không khớp `.gitignore` ⇒ `golden-test` không đổi |
| S10 | người giữ write set (08:09:52Z 15-11) | `python ops/lease_publish.py ai-dang-giu` trên kho bare khớp 233/233 nhánh máy chủ: bốn đường dẫn của mục 4 đều `NGƯỜI_GIỮ 0`. Đo lại trước lúc cấp lease |
| S11 | kích thước tiền lệ | `DOC-CLAIMS-XOA` (PR #1125, merge `70ab34e`): 4 tệp, +179/−11 (manifest +7/−7, fragment +152/−0, `workflow.py` +19/−4, bundle +1/−0) |

## 2. Thay đổi

**M1 → `scripts/tl_core/workflow.py`, lớp L1 của `_doc_claims_scan_one`** (chỉ lớp L1; không đổi lớp nào khác):

- (a) **Cắt token giữ dấu chấm đầu.** Đầu token cắt bằng tập ký tự `_DOC_CLAIMS_TRIM` bỏ dấu chấm; cuối token cắt bằng đúng
  `_DOC_CLAIMS_TRIM` như cũ (dấu chấm cuối câu vẫn bị cắt).
- (b) **`./`, `../` giữ hành vi hiện tại: không kiểm.** Token sau bước (a) bắt đầu bằng `./` hay `../` thì bỏ qua, không
  sinh phát hiện nào (Q1). Nhánh `if body.startswith("."):` cũ (kiểm tương đối theo thư mục tài liệu) bị bỏ: sau (b),
  token bắt đầu bằng dấu chấm còn lại đều là đường dẫn có đoạn đầu dạng `.ten`.
- (c) **Đường dẫn có đoạn đầu dạng `.ten` đi cùng luồng với mọi đường dẫn khác:** đoạn đầu không thuộc `ctx["toplevel"]`
  thì bỏ qua; có ở gốc kho hay theo thư mục tài liệu thì không phát hiện; còn lại qua (d), (e) rồi phân loại đã xoá / lịch
  sử / sống như hiện hành (`PATH_DELETED`, `PATH_DELETED_IN_HISTORICAL_DOC`, `PATH_MISSING_IN_HISTORICAL_DOC`,
  `PATH_MISSING`).
- (d) **Đường dẫn khớp `.gitignore` không sinh phát hiện.** Áp cho MỌI token đường dẫn của L1 (không riêng dạng `.ten`),
  ngay sau phép kiểm tồn tại thất bại và trước mọi phân loại. Chuỗi hỏi là `q = body + slash`, tức giữ nguyên dấu `/` cuối
  của token (S4): token có `/` cuối là thư mục, token không có `/` cuối là tệp. Gọi `_doc_claims_git(root, ["check-ignore",
  "-q", "--no-index", "--", q])`; rc 0 ⇒ bỏ qua token; rc khác 0 (kể cả 1, 128, 127) ⇒ phân loại tiếp như (c). Kết quả
  được nhớ trong `ctx` cho cả lượt quét với **khoá là chính `q`** (hai chuỗi `x` và `x/` là hai khoá khác nhau).
- (e) **Danh sách miễn trừ đúng 9 cặp** `_DOC_CLAIMS_MIEN_TRU_L1` (hằng mức module, `frozenset` các bộ đôi
  `(tài liệu tương đối, đường dẫn)`), có chú thích dẫn `ADR-0032`, `ADR-0066` và #1326. Token ở tài liệu sống mà phân loại ra
  `PATH_MISSING` và cặp `(rel tài liệu, body)` thuộc tập ⇒ advisory lý do `PATH_MISSING_MIEN_TRU` thay cho cờ. Không áp cho
  `PATH_DELETED` hay tài liệu lịch sử. Chín cặp, theo đúng thứ tự này:
  1. `docs/PROTOCOL_DA_PHIEN.md` · `.github/coordination/change-impact.v1.json`
  2. `docs/PROTOCOL_DA_PHIEN.md` · `.github/coordination/schemas/change-impact.v1.schema.json`
  3. `docs/adr/0032-change-impact-rule-co-huong.md` · `.github/coordination/change-impact.v1.json`
  4. `docs/adr/0032-change-impact-rule-co-huong.md` · `.github/coordination/schemas/change-impact.v1.schema.json`
  5. `docs/adr/0056-lease-no-progress-six-hours.md` · `.github/coordination/change-impact.v1.json`
  6. `docs/research/2026-08-03-danh-gia-gop-y-adr-0017-0032-cuoi.md` · `.github/coordination/change-impact.v1.json`
  7. `docs/research/2026-08-03-danh-gia-gop-y-adr-0017-0032-cuoi.md` · `.github/coordination/schemas/change-impact.v1.schema.json`
  8. `docs/research/2026-08-15-chien-luoc-gate-nang-theo-vong-doi.md` · `.github/coordination/change-impact.v1.json`
  9. `docs/adr/0066-admission-thu-hoi-theo-merge-base.md` · `.github/coordination/change-impact.v1.json`
- (f) `claim` của phát hiện là token sau bước (a), tức giữ dấu chấm đầu và dấu `/` cuối nếu có. Schema JSON của lệnh không
  đổi, chỉ thêm một mã lý do. `layers`, `layers_skipped`, `files_scanned` không đổi.

**M2 → `scripts/test_fragments/wp1326_doc_claims_dau_cham.py` (tệp mới)**, `TEST_ID = "wp1326_doc_claims_dau_cham"`, theo
khuôn `scripts/test_fragments/wp1121_doc_claims_xoa.py`: dựng một kho git THẬT trong thư mục tạm, gọi đường sản xuất
`tl_module._doc_claims_check(root=kho)`, so TẬP các phát hiện L1 `(lớp, tài liệu, claim, mã lý do, là advisory)` với tập
mong đợi; thông báo FAIL nêu TÊN ca lệch. Fixture tối thiểu: tệp giữ `.claude/giu.md`, `.agents/skills/x/SKILL.md`,
`agents/giu.md`, `.github/giu.md`, `du-lieu/giu.md`, `SKILL.md`; `.gitignore` có hai dòng `.claude/.state/` và
`du-lieu/sinh/`; `.claude/da-xoa.py` được commit rồi `git rm` + commit. Không tạo thư mục `.claude/.state/` hay
`du-lieu/sinh/` trên đĩa. Các ca:

| ca | tài liệu | token | mong đợi |
|---|---|---|---|
| a | `CONTEXT.md` (sống) | `.agents/skills/x/SKILL.md` (có thật) | không phát hiện |
| b | `CONTEXT.md` | `.claude/khong-co.py` | cờ `PATH_MISSING`, claim `.claude/khong-co.py` |
| c | `CHANGELOG.md` (lịch sử) | `.claude/khong-co.py` | advisory `PATH_MISSING_IN_HISTORICAL_DOC` |
| d | `docs/adr/0001-t.md` (sống) | `.claude/da-xoa.py` | cờ `PATH_DELETED` |
| e | `CONTEXT.md` | `.claude/.state/x.json` (tệp bên trong thư mục bị ignore) | không phát hiện |
| e2 | `CONTEXT.md` | `.claude/.state/` (chính thư mục bị ignore, có `/` cuối) | không phát hiện |
| e3 | `references/a.md` rồi `references/b.md` (cả hai sống, quét cùng một lượt) | `references/a.md` có `.claude/.state` ở dòng trước `.claude/.state/`; `references/b.md` có hai token ấy theo thứ tự ngược lại | mỗi tài liệu đúng một cờ `PATH_MISSING` claim `.claude/.state`; không phát hiện nào cho `.claude/.state/` |
| e4 | `docs/adr/0002-u.md` (tài liệu trong thư mục con) | `.claude/khong-co-2.py` | cờ `PATH_MISSING` |
| e5 | `CONTEXT.md` | `du-lieu/sinh/` (đường thường, thư mục bị ignore, có `/` cuối) | không phát hiện |
| f | `CONTEXT.md` | `.docx/.pdf` | không phát hiện (đoạn đầu không phải mục gốc) |
| g | `CONTEXT.md` | `./khong-co.md` và `../khong-co.md` | không phát hiện |
| h1 | `docs/PROTOCOL_DA_PHIEN.md` (sống) | `.github/coordination/change-impact.v1.json` | advisory `PATH_MISSING_MIEN_TRU` |
| h2 | `CONTEXT.md` | `.github/coordination/change-impact.v1.json` | cờ `PATH_MISSING` (miễn trừ gắn với tài liệu) |

Tiền điều kiện (sai ⇒ FAIL có tên, không bao giờ trả True): `.claude`, `.agents`, `agents`, `.github`, `du-lieu` thuộc
`ctx["toplevel"]`; `.claude/da-xoa.py` thuộc tập đã xoá; mọi tài liệu của bảng thuộc targets mặc định; `references/a.md`
được quét trước `references/b.md`. Không dựng được fixture (git thiếu, lệnh git rc ≠ 0) ⇒ FAIL; fragment không có nhánh bỏ
qua.

**M3 → `scripts/tl_test_fragments_bundled.py`**: chỉ tái sinh bằng `generate_bundled_module_bytes` của
`scripts/tl_core/test_fragments.py` (tiền lệ wp1030 `a1bbb44`, wp1121); không sửa tay.

**M4 → `RELEASE_MANIFEST.json`**: chỉ tái sinh (`python scripts/tl.py release-manifest --root . --out RELEASE_MANIFEST.json`);
không bump `VERSION`, không sửa `CHANGELOG.md` (tiền lệ wp1030, wp1121).

## 3. Quyết định của chủ kho (vòng hỏi 1, 15-11-2026, trả lời *"Theo khuyến nghị"*)

- **Q1 (A)** Kiểm đúng đường dẫn bắt đầu bằng dấu chấm theo gốc kho như mọi đường dẫn khác; đường dẫn khớp `.gitignore` là
  đường runtime, bỏ qua; `./`, `../` giữ cách xử lý hiện tại. Đo sau vòng hỏi (S6): cách xử lý hiện tại của `./`, `../` là
  **không kiểm**; M1(b) giữ đúng điều đó.
- **Q2 (a)** 8 con trỏ `.github/coordination/…` vào danh sách miễn trừ đúng 8 cặp, hạ xuống advisory; chỗ mới vẫn là cờ;
  thi công hay sửa chữ `ADR-0032` để packet khác. **Câu hỏi E3 ngày 16-11-2026** (mục 11): `ADR-0066` land sau lời duyệt r2
  và trỏ tệp policy hai lần; chủ kho chọn *"Thêm cặp thứ 9 (Recommended)"* ⇒ danh sách đúng 9 cặp; chỗ mới sau khi packet
  land vẫn là cờ.
- **Q3 (a)** Executor Claude, reviewer Codex qua `launcher.py run`, `cross_approved`.

Người soạn tự quyết (không thuộc E1–E5) và ghi lại: `packet_id`; Windows theo `ADR-0060` M3 bước 2 là `required` (lúc hỏi
vòng 1 người soạn đoán `not_required`, đo lại thấy tệp test phải dùng `subprocess` để dựng kho git — M3 không cho agent hạ
mức); không bump `VERSION`; mã lý do `PATH_MISSING_MIEN_TRU`; phép kiểm `.gitignore` áp cho mọi đường dẫn L1: trên checkout
sạch nó làm biến mất đúng 2 advisory hiện có, cả hai trỏ thư mục fixture sinh tại chỗ `references/golden/fixtures/` (S7) — đó
là tác động có chủ ý.

## 4. Write set

```yaml
write_set:
  - scripts/tl_core/workflow.py
  - scripts/test_fragments/wp1326_doc_claims_dau_cham.py
  - scripts/tl_test_fragments_bundled.py
  - RELEASE_MANIFEST.json
```

Diff PR đúng 4 tệp. Ước lượng (chưa đo, theo tiền lệ S11 cộng các ca thêm của M2): khoảng +250 dòng thêm, trong trần
`ADR-0053` cho packet `sensitive`. `RELEASE_MANIFEST.json` khoá `scripts/tl_core/workflow.py` và bundle; tệp fragment KHÔNG
nằm trong manifest (`_release_should_include`, `scripts/tl_core/release.py:570–571`, loại `scripts/test_fragments/**`) — nó vào
gói dưới dạng nguồn nhúng trong bundle. Manifest được tái sinh ở M4.

## 5. Nghiệm thu (mỗi tiêu chí kèm phép làm nó ĐỎ)

- **N1** `python scripts/tl.py --selftest` ra N/N hai số BẰNG nhau trên đúng SHA sẽ đẩy; fragment `wp1326_doc_claims_dau_cham`
  được auto-discover và ĐẠT (ghi dòng output chứng minh nó chạy). Chạy fragment trên mã base ⇒ FAIL, ghi tên các ca lệch
  (kỳ vọng: a, b, c, d, e3, e4, e5, h1, h2). Đỏ khi: các đột biến N2.
- **N2** Đột biến trên BẢN SAO TẠM, mỗi cái đọc TÊN ca lệch trong thông báo FAIL, không chỉ rc; baseline không đột biến phải
  ĐẠT trước:
  D1 khôi phục `strip(_DOC_CLAIMS_TRIM)` cho đầu token ⇒ a, b, c, d, e3, e4, h1, h2 lệch;
  D2 thay bước bỏ qua `./`, `../` (M1(b)) bằng phép kiểm tương đối theo thư mục tài liệu của nhánh cũ `body.startswith(".")`
  ⇒ g lệch (chỉ bỏ M1(b) thì không đủ làm đỏ: đoạn đầu `.`, `..` không thuộc `ctx["toplevel"]` nên bộ lọc mục gốc vẫn bỏ qua
  token; M1(b) là chốt tường minh, răng của g nằm ở việc không có nhánh kiểm tương đối);
  D3 bỏ phép kiểm `.gitignore` (M1(d)) ⇒ e, e2, e3, e5 lệch;
  D4 so miễn trừ chỉ theo đường dẫn, bỏ vế tài liệu ⇒ h2 lệch;
  D5 làm rỗng `_DOC_CLAIMS_MIEN_TRU_L1` ⇒ h1 lệch;
  D6 bỏ bộ lọc `ctx["toplevel"]` cho đường dẫn dạng `.ten` ⇒ f lệch;
  D7 không tái sinh bundle (giữ `scripts/tl_test_fragments_bundled.py` của base) ⇒ `python .github/checks/bundle_fragment_check.py --json`
  rc ≠ 0, `TEST_ID_SET_MISMATCH` nêu `wp1326_doc_claims_dau_cham`;
  D8 hỏi `git check-ignore` bằng `body` (bỏ `/` cuối) thay cho `q` ⇒ e2, e3, e5 lệch;
  D9 khoá cache của M1(d) bằng `body` thay cho `q` ⇒ e3 lệch (thừa cờ claim `.claude/.state/` hoặc thiếu cờ `.claude/.state`,
  tuỳ thứ tự).
- **N3** Kho thật trên head, checkout sạch (clone đủ lịch sử, `core.abbrev=7`, không có `references/golden/fixtures/`):
  `python scripts/tl.py doc-claims-check --strict --json` rc 0, `flags: []`; đếm theo TỪNG cặp của M1(e): cặp 1–8 mỗi cặp đúng
  một advisory `PATH_MISSING_MIEN_TRU` ở đúng tài liệu ấy, cặp 9 đúng hai (dòng 30 và 49 của `ADR-0066`) — 9 vị trí, không
  đếm gộp; advisory `PATH_DELETED_IN_HISTORICAL_DOC` có
  claim bắt đầu bằng dấu chấm đúng 3 (S3); không advisory nào có claim `references/golden/fixtures/`; tổng advisory L1 = 173
  (= 162 − 2 + 3 + 10, S7, đo trên base r3). Trên base: 0 advisory `PATH_MISSING_MIEN_TRU`, 162 advisory L1. Đo lại lúc thi công; lệch thì ghi
  số mới kèm lý do (L5 của skill `soan-spec`). Đỏ khi: D5 (rc 2, 10 cờ `PATH_MISSING`); D3 hay D8 (rc 2, cờ claim
  `.claude/.packet_state/` ở `docs/research/2026-10-16-y-tuong-tu-context-mode.md`).
- **N4** Tái hiện lỗi của P2 r10 (vế dương mới, vế âm cũ): một bản ADR đặt trong thư mục tạm, chép blob
  `docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md` của head rồi đưa lại dấu nháy ngược quanh đường dẫn adapter Codex
  `land-packets` ở hàng *Tự merge*; `doc-claims-check --path <bản ấy> --strict --json` chạy ở gốc kho: trên base rc 2, cờ L1
  `PATH_MISSING` claim `agents/skills/land-packets/SKILL.md`; trên head rc 0, không phát hiện L1. Đỏ khi: D1.
- **N5** Các cổng tại chỗ, mỗi cổng kèm phép làm đỏ:
  - `python -m ruff check --select F` trên `scripts/tl.py`, `scripts/tl_core/workflow.py` và tệp fragment mới: DELTA so base = 0.
    Đỏ khi: thêm một `import` không dùng vào `scripts/tl_core/workflow.py` (F401, delta 1).
  - `git diff --check <base> HEAD` rc 0. Đỏ khi: thêm một khoảng trắng cuối dòng vào tệp fragment.
  - `python .claude/dev/packet_loop.py doctrine-scan --root .` rc 0. Đỏ khi: chép một đoạn của `docs/PROTOCOL_DA_PHIEN.md` vào
    `.claude/skills/work-packet/SKILL.md` trên bản sao tạm (rc 6).
  - `python scripts/tl.py golden-test --json` `ok: true` (S9). Đỏ khi: thêm một dòng có token `.claude/khong-co.py` vào khối
    `doc_claims = (...)` của `scripts/tl_core/workflow.py` (fixture sinh từ mã) ⇒ `doc_claims_check_fixture` lệch.
  - `python scripts/tl.py workflow-audit --strict --json`, `determinism-audit --strict --json` `ok: true`: tiêu chí canh bất
    biến, xanh sẵn trên base; packet không đặt phép làm đỏ riêng cho hai cổng này, răng của chúng là các ca selftest sẵn có của
    chính chúng — ghi thẳng là packet không chứng nhận lại.
  - `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` `ok: true`, `expected == checked`. Đỏ khi: bỏ
    M4 (`failed` nêu `scripts/tl_core/workflow.py`).
  - `python .github/checks/bundle_fragment_check.py --json` rc 0. Đỏ khi: D7.
- **N6** Windows (`ADR-0060` M3, `required`): trên máy Windows local của chủ kho có trong `list_devices` (hiện ASUS-LAPTOP)
  theo `ADR-0057`/`0058`/`0059`: lấy khoá `D:\tl-win\KHOA.txt` (dòng năm trường, hạn ≤ 2 giờ, nhịp tim ≤ 30 phút), kiểm tải
  `python.exe`, clone cô lập ở `D:\tl-win\<session_id>\` (`core.abbrev 7`), rồi trong MỘT lệnh chạy `python scripts/tl.py
  --selftest` trên SHA base và SHA ứng viên, ghi danh sách test ID kèm kết quả của từng lượt và một dòng sổ đo. Xanh theo đủ
  (a)–(c) của M3: (a) đủ hai lượt cùng máy dựng trong cùng một lệnh, mỗi lượt chạy trọn tập test và có danh sách test ID kèm kết
  quả; (b) tập test đỏ trên ứng viên nằm trong tập đỏ trên base; (c) ca đỏ thuộc tệp trong write set ⇒ chủ kho quyết (E2). Đỏ
  khi: thiếu một lượt, thiếu báo cáo, lỗi setup, test bắt buộc `skipped`/`not_run` ở bất kỳ lượt nào, ứng viên chạy 0 test,
  hay SHA của một lượt khác SHA khai trong sổ đo. Trạng thái `chưa đo được` cho tới khi chạy thật.
- **N7** CI lượt PR xanh trên head cuối, đọc bằng check run từng job (job `gate` có bước `doc-claims-check strict`). Đỏ khi:
  một job bắt buộc có `conclusion` khác `success`, vắng mặt, hay `head_sha` của run khác head PR.
- **N8** `git diff --name-only <base> HEAD` bằng đúng bốn đường dẫn của mục 4; `git diff --numstat <base> HEAD` trong trần
  `ADR-0053` (số tệp và tổng dòng thêm). Đỏ khi: thêm một tệp ngoài write set; hay tổng dòng thêm vượt trần của `ADR-0053`.

## 6. `luat_dung`

- (i) Trần lời gọi Codex review của PR thi công theo dòng khai `ADR-0055` ở đầu tệp; một sổ chung cho lời gọi offline và
  connector, ghi trên #1326, mỗi lời gọi một dòng (số thứ tự, đường, SHA, hiện vật neo). Chạm trần mà chưa approve ⇒ Review
  Rescue Checkpoint (`ADR-0037`); đó là E2.
- (i) Push thêm và điều kiện merge: `ADR-0060` M5, M7 (mặc định theo `ADR-0062`). Cùng hình dạng lỗi lần thứ ba: protocol §12.
- (ii) E2: máy Windows local không có trong `list_devices` hay khoá do phiên khác giữ quá hạn mà còn tiến trình sống
  (`ADR-0059` §2) — mang theo dòng khoá, PID, giờ đo; credential Codex chết. E3: phép đo cho thấy danh sách miễn trừ của Q2
  hay cách giữ `./`, `../` của Q1 làm `doc-claims-check` hô sai trên tài liệu có thật — mang theo token, tài liệu, rc.

Không có ngân sách mềm.

## 7. `ngoai_pham_vi`

- Kiểm `./`, `../` (S6: 13 lần, 3 sẽ thành cờ ở tài liệu sống, trong đó `./tl_secrets.enc` trỏ thư mục dự án Cowork): cần một
  quy ước phân biệt đường trong kho với đường ở môi trường khác; packet khác.
- Thi công policy change-impact của `ADR-0032` (có bản trên nhánh bên `codex/f3-02-impact-policy`, S5) hay sửa chữ mười chỗ của
  M1(e). Packet làm việc ấy xoá cặp tương ứng khỏi `_DOC_CLAIMS_MIEN_TRU_L1`.
- Các lớp L2–L12 của `doc-claims-check`; phép cắt token ở lớp khác (nếu có) chưa đo.
- `VERSION`, `CHANGELOG.md`, `changelog.d/` (tiền lệ wp1030, wp1121).

## 8. `hinh_dang_ke_thua`

`khong_ap_dung`: không phải packet khắc phục của một packet thất bại. Lỗi được phát hiện qua packet
`GIAM-HOI-P2-ADR-E1-E5` (đã land); packet ấy né lỗi bằng đặc tả r11, không sửa bộ kiểm.

## 9. `chua_do_duoc`

- N6 Windows: chỉ đo được khi chạy thật trên máy local.
- Số advisory của N3 sẽ trôi khi tài liệu đổi giữa lúc soạn và lúc thi công; số đúng là số đo lại lúc thi công, trên checkout
  sạch.
- Thời gian chạy thêm của M1(d): mỗi khoá `q` phân biệt một tiến trình git; trên base checkout sạch khoảng 104 khoá (98 claim
  phân biệt của advisory hiện có cộng 6 đường dẫn dạng `.ten` thiếu phân biệt, đo 01:4xZ 16-11), chưa đo thời gian.

## 10. Thay đổi so với r1

Review đặc tả Codex lượt 1 (lời gọi 1/10 của packet, `gpt-6-astra` xhigh, `changes_requested`):

- **S1-01 (P2, `mat-ngu-nghia-thu-muc-khi-kiem-ignore`)**: M1(d) của r1 hỏi `git check-ignore` bằng `body` đã mất `/` cuối, nên
  `.claude/.packet_state/` không khớp mẫu thư mục và N3 đỏ dù thi công đúng; cache khoá theo `body` làm `x` và `x/` dùng chung
  kết quả. Sửa: chuỗi hỏi và khoá cache là `q = body + slash` (M1(d)); thêm S4; thêm ca e2, e3, e4, e5 và đột biến D8, D9;
  N3 thêm điều kiện checkout sạch và tổng 171.
- **S1-02 (P3)**: S7 của r1 (160 / 0) đo trên checkout đã có thư mục fixture sinh tại chỗ. Sửa: đo lại trên checkout sạch
  (162 lần / 98 claim; 2 lần / 1 claim khớp `.gitignore`), ghi điều kiện, nêu tác động có chủ ý ở mục 3; mục 9 đếm khoá phân biệt.
- **S1-03 (P3)**: lời khai "chưa từng tồn tại" rộng hơn phép đo. Sửa S5: không có trong tree và lịch sử đi được từ base; có trên
  nhánh bên `codex/f3-02-impact-policy` (`a55efcd`), chưa land.
- **S1-04 (P3)**: tệp fragment không nằm trong manifest. Sửa mục 4.
- **S1-05 (P3)**: N5–N8 thiếu phép làm đỏ. Sửa: mỗi cổng của N5 kèm đột biến hay ghi thẳng là canh bất biến không chứng nhận
  lại; N6 dẫn đủ (a)–(c) của M3 và các điều kiện đỏ; N7, N8 thêm điều kiện đỏ.
- **S1-06 (P3)**: hai điểm chờ chủ kho chưa mang mã E. Sửa: hàng luật merge và `pham_vi_e` gắn E2 kèm căn cứ.

## 11. Thay đổi so với r2

Sau khi chủ kho duyệt băm r2 (15-11-2026), `master` land #1265 (`6e1047e`, rồi `815b9ac`) thêm
`docs/adr/0066-admission-thu-hoi-theo-merge-base.md`. ADR ấy trỏ `.github/coordination/change-impact.v1.json` hai lần (dòng 30
và 49) có chủ đích. Đo lại trên `815b9ac` (01:4xZ 16-11): thi công đúng r2 sẽ sinh 2 cờ `PATH_MISSING` ở `ADR-0066`, N3 đỏ, CI
đỏ. Đây là bằng chứng mâu thuẫn quyết định Q2 (*"đúng 8 cặp; chỗ mới vẫn là cờ"*), tức E3; phiên hỏi chủ kho, chủ kho chọn
*"Thêm cặp thứ 9 (Recommended)"*. Thay đổi so với r2:

- M1(e): thêm cặp 9 (`ADR-0066`, `.github/coordination/change-impact.v1.json`); danh sách đúng 9 cặp.
- Mục 1: số đo trên base mới (S1 131 tệp, S2 189, S3 157 / 17 / 4 / 11, S5 10 lần trên 9 cặp, S7 và S8 đo lại, S6 không đổi).
- N3: cặp 9 đúng hai advisory; tổng advisory L1 173; D5 cho 10 cờ.
- Mục 3 ghi câu hỏi E3 và lựa chọn; mục 7 bỏ câu `docs/PROTOCOL_DA_PHIEN.md` đang bị lease #1265 giữ (#1265 đã land).

Các khối hành vi khác của M1, M2–M4, write set và N1, N2, N4–N8 không đổi.
