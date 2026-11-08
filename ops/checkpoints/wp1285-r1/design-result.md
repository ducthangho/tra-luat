# Tư vấn thiết kế P1-S3 → P6, Mission #1238 / Packet #1285 (chỉ đọc)

Phạm vi: chỉ là tư vấn. Tôi không vá mã, không duyệt mã, không chạy gì. Mọi khảo sát làm trên `/workspace/scratch/proxima-remaining-canonical` (bf9914c / tree 247971f).

## 0. Sự thật quan sát được (đọc mã, chưa chạy)

| # | Quan sát | Nguồn |
|---|---|---|
| F1 | `.agents/skills/proxima-control/` có 6 tệp: `ProximaConfig.psm1` (S1), `ProximaControl.psm1` và `Run-Px.ps1` (S2), `config.example.json`, hai harness `tests/*.Tests.ps1`. Chưa có `SKILL.md` và chưa có `.psd1`. | Glob |
| F2 | Header S2 tự khai: *"Not exposed by SKILL/manifest until S3; imported directly from this .psm1"*. Run-Px cũng ghi *"no PSD1 until S3"*. | `ProximaControl.psm1:3`, `Run-Px.ps1:2` |
| F3 | `ConfigSha` được ghim trong psm1 và kiểm **trước** khi import S1. Endpoint body chỉ kiểm băm `control\ProximaControl.psm1` và `control\ProximaConfig.psm1`; psd1 không nằm trong chuỗi băm nào. | `ProximaControl.psm1:29,65-74,392-397` |
| F4 | `.agents` nằm trong `_RELEASE_EXCLUDE_DIRS`, tức không vào gói Package. Vì vậy S3 **không cần** đụng `VERSION`, `RELEASE_MANIFEST.json`, golden hay selftest. | `scripts/tl_core/release.py:395` |
| F5 | `doctrine-scan` quét mọi `*.md` dưới `.agents/skills` với ngưỡng n-gram **10 từ** so với protocol. `SKILL.md` mới sẽ bị cổng này đo. | `.claude/dev/packet_loop.py:1635-1682` |
| F6 | D1 (P0 §f) đã chốt: Playwright dùng **CLI trước**, MCP chỉ khi được duyệt, **chưa làm library hay adapter Python**, không thêm dependency vào core. | `docs/research/2026-11-05-proxima-playwright-p0.md:59` |
| F7 | Theo P0, đường dẫn dưới `.agents/skills/` thuộc class `sensitive`. Trần mặc định ≤3 tệp và ≤300 dòng thêm. Trần ≤6/≤450 chỉ áp khi spec có **đúng một** dòng `tran_kich_thuoc_sensitive: ADR-0053@<oid>`. | P0 §g, `docs/adr/0053-*.md:51-58` |
| F8 | Không có mảnh `changelog.d/wp-1271*` hay `wp-1279*`, tức tiền lệ S1/S2 là không viết changelog fragment. | Glob |
| F9 | Module đã cài trên f728 mang metadata version **1.0.1** và khai PS 5.1 (`doc_ma` + `da_quan_sat`). Probe trên 810 từng báo `Import-PowerShellDataFile unavailable`. | P0 §b |

---

## 1. P1-S3: đề xuất spec sẵn sàng đóng băng

### 1.1 Ranh giới

- **Publication** trong S3 chỉ có nghĩa là `SKILL.md` và manifest được merge vào repo, để agent đọc từ checkout tìm thấy skill.
- S3 **không** cài lên host nào, **không** chép control tree sang `<basePath>\control`, **không** đăng ký endpoint hay `configurationName`, không đụng service hay profile. Mọi việc đó là **activation**, thuộc P3/P5 và cần lease riêng.
- Gói Package không mang skill này (F4). SKILL.md phải nói thẳng điều đó.

### 1.2 Write set: 3 tệp, đều tạo mới

Không sửa tệp nào của S1/S2.

| Tệp | Vai trò | Ước lượng dòng thêm |
|---|---|---|
| `.agents/skills/proxima-control/scripts/ProximaControl.psd1` | Manifest chỉ chứa dữ liệu | ~20–25 |
| `.agents/skills/proxima-control/SKILL.md` | Hợp đồng skill | ~100–120 |
| `.agents/skills/proxima-control/tests/ProximaManifest.Tests.ps1` | Harness hẹp, không Pester, cùng quy ước rc 0/1/2 với S2 | ~120–150 |

- **Tổng ước lượng ~250–295 dòng thêm**, nằm trong trần sensitive mặc định 3 tệp/300 dòng. Đây là ước lượng; phải đo `git diff --numstat` trước review.
- Nếu vượt 300: dừng trước review và tách ra. Hoặc spec mang dòng ADR-0053 đã kiểm đủ 3 phép đo OID; khi đó đây là quyết định của người giữ, không tự nâng.

**Chủ ý KHÔNG đụng:** `ProximaControl.psm1`, `ProximaConfig.psm1`, `Run-Px.ps1`, `config.example.json`, hai harness S1/S2, `VERSION`, `RELEASE_MANIFEST.json`, workflow, launcher, `SKILL.md` gốc. Không thêm changelog fragment (theo F8; người giữ có thể đổi điều này).

### 1.3 Nội dung manifest (quyết định đề xuất)

- `RootModule = 'ProximaControl.psm1'`, `ModuleVersion = '2.0.0'`, `GUID` cố định mới.
- `PowerShellVersion = '5.1'`, `CompatiblePSEditions = @('Desktop','Core')`.
- `FunctionsToExport = @('px','Invoke-ProximaOperation')`. `CmdletsToExport`, `VariablesToExport`, `AliasesToExport` đều `@()`.
- **CẤM** các khoá `NestedModules`, `RequiredModules`, `ScriptsToProcess`, `RequiredAssemblies`, `TypesToProcess`, `FormatsToProcess`. Lý do: `NestedModules`/`RequiredModules` nạp S1 **trước** chốt băm (F3), còn `ScriptsToProcess` chạy mã trong scope người gọi trước mọi chốt. Không liệt kê `ProximaConfig.psm1` ở đâu cả.
- Chọn `2.0.0` (major) vì API công khai đã khác bản bundle 1.0.1 trên f728 (F9): bắt buộc `-ConfigPath/-RepositoryRoot/-TargetId`, không có mặc định. Lý do thứ hai: phân biệt được *repo* với *bản đã cài cũ* chỉ bằng nhìn version.

### 1.4 Ngữ nghĩa phiên bản (SKILL.md phải ghi ba lớp, không lớp nào thay được lớp nào)

1. **Add-on trong repo** = `ModuleVersion` cộng commit/tree git. Hoàn toàn độc lập với `VERSION` của tra-luat.
2. **Control tree đã cài trên endpoint** = cặp `moduleSha256` / `configModuleSha256` lấy từ `handshake`. Đây là danh tính thật; chuỗi version ở đầu kia **không** được dùng làm danh tính.
3. **Gateway runtime** (FileVersion của `Proxima.exe`) = **S2/S3 không đo**.
   - Đề xuất: **không** sửa psm1 trong S3 để thêm phép đọc này, vì sửa là đổi SelfSha và đụng chốt S2.
   - Dời sang P4: updater dù sao cũng phải đọc version của binary đang cài, kèm kiểm chữ ký.
   - SKILL.md ghi `not_measured` cho lớp này. `status`/`models` không chứng minh version, quota, xác thực hay danh tính model.
   - ⚠ Đây là **điểm cần chủ kho/người giữ chốt trước freeze**. Nếu họ coi "target/version remainder" bắt buộc gồm runtime version ngay trong S3, thì phải mở psm1 và làm lại toàn bộ đo S2; đó là mở rộng boundary, tôi không khuyến nghị.

### 1.5 SKILL.md: hợp đồng tối thiểu

- Frontmatter: `name: proxima-control`, `description: …`, có dòng version khớp `ModuleVersion`.
- Hai lối vào, cùng một module:
  - `scripts/Run-Px.ps1` cho agent.
  - `Import-Module <skill>\scripts\ProximaControl.psd1` cho phiên tương tác.
- Đối số target bắt buộc. Một config cho mỗi target, nằm **ngoài repo**. Không mặc định, không dò tìm, không tự kết nối.
- `-WhatIf` / `-Confirm` áp cho mọi hành động. Không fallback gateway/model/device, không retry inference (D3).
- Câu trả lời model là `untrusted_data`. Nguyên văn pháp luật chỉ lấy từ nguồn đã verify. **Trỏ** tới `SKILL.md` gốc và protocol thay vì chép lại, vì `doctrine-scan` ở F5 sẽ bắt n-gram ≥10 từ.
- Skill là tuỳ chọn; core chạy bình thường khi skill vắng hoặc lỗi (D6).
- Không đường dẫn thật của máy, không hostname, không device ID; chỉ placeholder `<...>`.
- Danh sách "chưa chứng minh": copy nguyên từ header psm1, viết lại ngắn gọn.

### 1.6 Map ID nghiệm thu → tệp → test

| ID | Tính chất | Tệp | Test (token đỏ) |
|---|---|---|---|
| S3-A1 | psd1 là **một hashtable literal**, đọc bằng AST. Không dùng `Import-PowerShellDataFile` (F9). Khoá nằm trong allow-list; khoá cấm vắng mặt. | psd1 | M01 `MANIFEST_NOT_DATA`, M02 `MANIFEST_KEY` |
| S3-A2 | Export đúng bằng `{px, Invoke-ProximaOperation}` (Ordinal) sau khi import psd1 trong **process con mới**. `px help` chạy được. Không thay đổi env/fs ngoài scratch. | psd1 | M03 `EXPORT_SET` |
| S3-A3 | Import qua psd1 vẫn giữ chốt *hash-before-import*: bản sao có `ProximaConfig.psm1` bị sửa phải ra `ProximaControl.DependencyMismatch`. | psd1 (nhờ không có NestedModules) | M04 `HASH_GUARD_BYPASSED` |
| S3-A4 | `ModuleVersion` ⇔ version trong SKILL.md khớp **cả hai chiều**. `Test-ModuleManifest` đạt trên PS 5.1 và 7. | psd1 + SKILL.md | M05 `VERSION_PARITY` |
| S3-A5 | Trộn hai lối vào (import psd1 rồi gọi `Run-Px.ps1 help` trong cùng process): **không bao giờ re-import âm thầm** làm mất session. Kết quả hợp lệ chỉ là *reuse* hoặc `ModuleConflict`. | (đo hành vi) | M06 `SILENT_REIMPORT` |
| S3-A6 | SKILL.md: frontmatter `name` đúng; mọi đường dẫn có ký tự ổ đĩa đều chứa `<`; có đủ các mục bắt buộc ở 1.5 (kiểm bằng **allow-list tiêu đề mục**, không kiểm câu chữ). | SKILL.md | M07 `SKILL_CONTRACT` |
| S3-A7 | Năm tệp của S1/S2 giữ nguyên byte. | — | **gate** `git diff --name-only base..head` ⊆ write set |
| S3-A8 | Không đổi core/VERSION/manifest/workflow/launcher. | — | gate như trên |

⚠ **Phải đo trước freeze (chưa biết):** sau khi import qua psd1, `(Get-Module ProximaControl).Path` trả đường dẫn psd1 hay psm1, trên PS 5.1 và trên PS 7? Run-Px so `Path` với psm1 (`Run-Px.ps1:17`).

- Nếu trả **psm1**: M06 kỳ vọng *reuse*.
- Nếu trả **psd1**: kết quả là `ModuleConflict`. Vẫn an toàn (fail-closed) nhưng khó dùng. Muốn reuse thì phải sửa `Run-Px.ps1`, tức đụng tệp S2.
- Khuyến nghị: chấp nhận `ModuleConflict` và ghi rõ trong SKILL.md là "đừng trộn hai lối vào trong một process", thay vì mở rộng write set.
- Phép đo này là một lệnh `Import-Module` trong scratch. Executor S3 làm ngay ở bước đầu, trước khi đóng băng kỳ vọng của M06.

**Phản chứng cho harness mới**, dùng cùng cơ chế CX của S2: chạy trên **bản sao**, chỉ được tính điểm khi rc=1 **kèm đúng token có tên**.
- CX01: thêm `ScriptsToProcess` → M02.
- CX02: `FunctionsToExport='*'` → M03.
- CX03: thêm `NestedModules='ProximaConfig.psm1'` → M02 và M04. Chính cấu hình này làm M04 đỏ, vì S1 bị nạp trước chốt băm.
- CX04: lệch version → M05.

### 1.7 Cô lập trước/sau trên Windows (focused, không cần CI Windows)

- **Baseline B** = tree đã land S2 (M0166d306…). Chạy `ProximaManifest.Tests.ps1 -ModulePath B\…\ProximaControl.psm1` trên PS 5.1 và PS 7. Kỳ vọng **rc=1**, mọi ca đỏ với `MANIFEST_ABSENT` / `SKILL_ABSENT`, mọi ca vẫn được chạy.
- **Candidate H**: rc=0 trên cả hai PS, cộng CX01–04 đều tính được điểm.
- **Không hồi quy** trên H:
  - Harness S2: 26 ca bình thường + 38 focused trên PS 5.1 và 7. Kỳ vọng y hệt số đo S2, vì S2 không đổi.
  - Harness S1: 21 ca bắt buộc.
  - Ca chỉ có trên Windows mà bị bỏ qua thì ghi `skipped`, **không** tính là pass.
- ScratchRoot, ReportPath và EvidenceRoot nằm ngoài tree. Chụp env/user-state trước và sau như harness S2.

### 1.8 Gate

- **Cục bộ:**
  - `python .claude/dev/packet_loop.py doctrine-scan --root .` rc=0 (F5, rủi ro thật vì SKILL.md mới).
  - `adr-song` không đổi.
  - Ruff delta 0. Không có Python đổi nên đây là bằng chứng phụ.
- **CI:** 23/23 Ubuntu trên đúng head của PR. Đọc **nhãn job**, không suy ra từ tên sự kiện.
- **Review:** Codex CLI độc lập, trên **đúng head/tree đã test**. Đọc finding trước khi merge; gate xanh không phải đã review.
- **M8:** theo protocol. Tôi chưa đọc định nghĩa M8 trong phiên này nên không khai nội dung của nó.
- **Hồ sơ land:** theo CLAUDE.md, phiên web không đo được mốc Workflow definition vì GraphQL trả 403. Mặc định `landed: false` và liệt kê các mốc `not_measured`, trừ khi chủ kho chạy lệnh `gh api graphql` bản `cmd`.

---

## 2. P2: Playwright tuỳ chọn

**Quyết định (không mở lại):** dùng **Playwright CLI chính thức** theo D1 (F6). Không dùng library, không dùng MCP, không adapter Python. Lý do thêm: CLI có bề mặt lệnh cố định, nên không có chỗ để "mã web tuỳ ý" thành thứ được thực thi.

**Bước đầu của P2 là một phép đo, chưa phải mã:** liệt kê bề mặt lệnh của CLI ở bản ghim (P0 ghi ứng viên `v0.1.23`, **chưa kiểm**, U10), đối chiếu với các trường bằng chứng cần thu: `requestedUrl`, `finalUrl`, `capturedAtUtc`, bytes của tài liệu tải về, sha256, ảnh hoặc PDF.
- Thiếu trường nào thì **dừng và đưa người giữ sửa D1**, không tự chuyển sang library.
- Tôi không khẳng định CLI có hay không có lệnh tải xuống hay đọc status; chưa đọc upstream.

**Bố cục đề xuất (tách hai packet để vừa trần sensitive):**

- **P2a, chạy offline, làm được ngay.** `.agents/skills/playwright-browser/`: `SKILL.md`, `playwright-browser.lock.json`, `scripts/Invoke-PwCapture.ps1`, `tests/PwCapture.Tests.ps1` với một CLI giả **giữ trạng thái**. Tổng 4 tệp, cần dòng ADR-0053 nếu vượt 3.
  - **Lock contract:** gồm tên package, version, integrity, major của Node đã test, revision Chromium.
  - **Lúc runtime:** chỉ gọi binary theo **đường dẫn tuyệt đối** trong cache đã cài. Cấm `npx …@latest`, cấm mọi tải mạng (ví dụ ép `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD`). Kiểm `package.json` version, integrity và thư mục revision trình duyệt. Lệch thì fail-closed (`NotInstalled` / `VersionMismatch`), **không tự cài**.
  - **Allow-list lệnh CLI** do lần đo ở trên quyết định. Cấm mọi lệnh kiểu eval/run-code.
  - **Profile:** mỗi lần capture một thư mục profile tạm mới, nằm ngoài repo, xoá sau khi xong. Không bao giờ dùng profile của Proxima hay của người dùng; không nhập cookie.
  - **Đầu ra:** `evidence.json` với `trust: untrusted_source_document`, liệt kê artifact theo role, đường dẫn, sha256 và số byte. Trace và ảnh ở ngoài repo; báo cáo chỉ ghi băm.
  - **Pháp lý:** tài liệu bắt được chỉ là ứng viên nguồn. tra-luat đối chiếu qua extract hoặc trang chính thức. Adapter không bao giờ sinh nguyên văn điều luật.
- **P2b, cần runtime và có blocker.** `scripts/Install-PwAddon.ps1` (cài và gỡ ngoài repo bằng `npm ci --ignore-scripts` từ lockfile chép sang; cài trình duyệt đúng revision ghim; giữ lại revision trước để rollback), cộng bằng chứng cài/gỡ **thật trên Desktop canary**. Đóng U10 ở đây.
  - Cài vào cache user-space là **thay đổi trên host**: cần lease hoặc uỷ quyền riêng cho đúng máy đó.
  - U9 (ổ D trên ASUS) để sang P5.

**Bốn tổ hợp:**
- **none**: đã được bảo đảm về cấu trúc nhờ F4 (gói core loại `.agents`), selftest đo được.
- **Proxima-only / Playwright-only**: chạy test của từng skill trên bản sao tree đã gỡ thư mục skill kia.
- **both**: chạy cả hai.
- Đo đủ bốn trong P2a ở mức offline, rồi P3 đo lại ở runtime.

---

## 3. P3–P6: bản thiết kế

| Packet | Đầu ra cụ thể | Phụ thuộc / blocker | Làm ngay hay cần đo runtime |
|---|---|---|---|
| **P3** Desktop canary kết hợp | (1) Xác định danh tính Desktop bằng MachineGuid + BIOS UUID, đọc chỉ-đọc. (2) Config Desktop đặt ngoài repo. (3) Chạy `px status/models` theo hướng **không inference**. (4) Một capture Playwright từ một nguồn chính thức, tra-luat đối chiếu. (5) Ma trận 4 tổ hợp trên máy thật. (6) Biên nhận ghi máy, version ba lớp, passed / failed / skipped / not_run. | S3, P2b, U11 (auth thật) | Cần runtime. **Không** gửi prompt. `ask` chỉ chạy khi người dùng yêu cầu rõ trong phiên đó. |
| **P4a** Khảo sát updater upstream | Đọc lại upstream tại commit ghim. Đo chỉ-đọc trên Desktop: `Get-AuthenticodeSignature` của installer v5.5.0 (sha `959c…` chỉ chứng minh toàn vẹn), có hay không file metadata kèm checksum của electron-updater, kiểu cài (per-user hay per-machine, có UAC không). Kết luận có **cách được hỗ trợ** để tắt hoặc ghim auto-update hay không (P0: `autoDownload=true`, `autoInstallOnAppQuit=true`, mới là `doc_ma`). | U4, U5, U12 | Phần đọc làm được ngay; phần đo cần quyền đọc trên Desktop. |
| **P4b** Updater stage-only | Kiểm định kỳ, tải về staging **ngoài repo**, xác minh theo chính sách chữ ký (thiếu thì dừng, D5), khoá chống chạy trùng, hoãn khi máy bận hoặc đĩa đầy. **Không kích hoạt.** Test bằng mock: nguồn lỗi, khoá trùng, đĩa đầy, file bị khoá. | P4a | Làm được offline. |
| **P4c** Kích hoạt + rollback | Kích hoạt trên Desktop qua cơ chế đã kiểm. Rollback cả binary lẫn dữ liệu và profile, thử bằng **profile thử**. Rollback lỗi thì dừng, không lặp. | U4 (cần bằng chứng kiểm soát được updater), U5, U7, U8, U12 | **Blocker đo được.** Nếu không có đường kiểm soát được hỗ trợ (ví dụ chỉ chặn được bằng tường lửa) thì đó là đổi endpoint và cần thẩm quyền; không có bằng chứng thì P4c dừng. Không giả vờ "xong offline". |
| **P5a** ASUS | Đo dung lượng và ACL ổ D (U9), rồi promote **đúng artifact** đã đạt trên Desktop, giữ nguyên cấu hình hiện có. | P3, P4c, U6 (license, xác nhận bằng văn bản), probe ASUS thật (lần probe AGY vừa MCP timeout, không phải bằng chứng) | Cần runtime. |
| **P5b** VM | Giải U2 trước: f728 và 810 trùng hostname và boot time. Đọc MachineGuid/BIOS UUID qua **từng** device connection, người giữ xác nhận máy đích **trước** mọi thao tác ghi. VM giữ vai gateway. | P5a, U2, U11 | Cần runtime. Cấm suy ra máy thay thế. |
| **P6** Review + bàn giao | Codex review độc lập trên đúng head/tree. Tài liệu vận hành, gỡ bỏ và giới hạn: gộp vào hai `SKILL.md` cộng một runbook dưới `docs/` (dev-side). | Toàn bộ các packet trước | Làm được sau khi các packet trước land. |

---

## 4. Khả thi về ngân sách (ước lượng, không phải số đo)

- **Mỗi packet:** 1 lượt author (Claude) khoảng 45–75 phút, cộng 1–2 vòng Codex mỗi vòng khoảng 15–30 phút, cộng native PS 5.1/7 focused, cộng CI khoảng 20–40 phút.
  - S3: khoảng 2–3 giờ wall, 1 author + 1–2 lời gọi review.
  - Số packet còn lại: S3, P2a, P2b, P3, P4a, P4b, P4c, P5a, P5b, P6 = **10 packet**.
  - Tổng dự phóng: khoảng **10–14 lượt author + 10–20 lượt review, khoảng 20–30 giờ wall**, chưa tính thời gian chờ blocker runtime.
- **Giới hạn cần dispatcher có thẩm quyền cụ thể, không tự nâng:**
  - (a) **Trần lời gọi Codex:** theo CLAUDE.md, mặc định là 2 (ADR-0036/0037) trừ khi spec mang dòng `tran_loi_goi_codex: ADR-0052@<oid>`. "2 vòng chính thức" khớp với trần này. Cần vòng thứ 3 thì phải xin `nang_tran` **trước** khi gọi.
  - (b) Trần kích thước sensitive (F7).
  - (c) Tổng lời gọi và phút trong vòng đời Mission **chưa đo, không bằng 0, không được reset**. Tôi không có số nên không khẳng định còn đủ.
  - (d) Mọi packet có runtime (P2b, P3, P4c, P5a, P5b) cần uỷ quyền host riêng cho đúng máy. Tư vấn này không cấp quyền đó.
- **Test:** chỉ test thuộc tính và an ninh cộng các gate bắt buộc. Harness S3 khoảng 7 ca và 4 CX. Không viết test soi gương lại cách hiện thực.

---

## Trạng thái

**HOÀN TẤT TƯ VẤN, chỉ đọc.** Không ghi tệp, không chạy lệnh, không gọi model hay mạng.

**Chưa chắc chắn / phải đo:**
1. `ModuleInfo.Path` khi import qua psd1 trên PS 5.1 và 7. Kết quả quyết định kỳ vọng của M06 (§1.6).
2. Người giữ có chấp nhận dời việc đọc runtime FileVersion sang P4 không (§1.4). Nếu không, S3 phải mở psm1 và đo lại S2.
3. Số dòng thật của S3 so với trần 300.
4. Bề mặt lệnh của Playwright CLI ở bản ghim. Chưa đọc upstream.
5. Định nghĩa chính xác của M8: chưa đọc trong phiên này.
6. Ngân sách vòng đời Mission: chưa có số đo.
7. U2, U4, U5, U6, U8, U9, U11, U12 vẫn mở như trong P0. Bản hash 959c… của installer không chứng minh publisher.