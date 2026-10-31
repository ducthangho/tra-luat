# Đặc tả packet `DIEU-KIEN-MERGE-VA-SO-SACH` r1: ADR-0060 — điều kiện merge, mốc ready, làn sổ sách

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

| trường | giá trị |
|---|---|
| packet_id | `DIEU-KIEN-MERGE-VA-SO-SACH`, revision 1, generation 1 |
| packet_issue | ghi ở comment đầu của Issue mở cùng đặc tả này (Issue trỏ ngược về tệp và băm) |
| nguon_cap_viec | chỉ thị chủ kho `ducthangho` trong phiên `session_015GtxrYPjZCTZeRiazdssgq` ngày 31-10-2026 ("đồng ý hết với các khuyến nghị", sau hai vòng phản biện Codex `gpt-6.1-sol` và `gpt-6-astra`) |
| review_class | `sensitive` — chạm `docs/PROTOCOL_DA_PHIEN.md`, workflow và thẩm quyền review/land (§8, dòng "`sensitive`: workflow/CI authority … review/land authority") |
| base | `origin/master` lúc cấp lease (đo khi soạn: `086f1b7`, merge PR #1064) |
| executor | `anthropic_claude` (Claude Code remote, Linux) |
| reviewer | `openai_codex` qua `launcher.py run`, phiên mới, neo đúng head, snapshot §8.2 đầu/cuối |
| depends_on | không |

## 1. Vì sao — số đo (31-10-2026)

| # | sự kiện | số đo | hệ quả |
|---|---|---|---|
| S1 | luật merge hiện hành | §8 bảng ngưỡng: P3 (và P2 ở `routine` chưa áp `ADR-0054`) được giữ dạng nợ do agent tự ghi | lỏng hơn chỉ thị chủ kho |
| S2 | Windows local | `ADR-0057` §2: chỉ áp khi đã chạy; máy offline thì "không áp" | lỏng hơn chỉ thị chủ kho |
| S3 | `ADR-0054` (push một lần, review theo lớp) | "CHƯA KÍCH HOẠT", chờ #812–#816 (cả hai Issue #814, #816 `open`, đo 31-10) | luật đã viết nhưng không áp |
| S4 | mốc bỏ draft | `rg -i "draft"` trên protocol/ADR/adapter: chỉ có "draft land PR" của mission | không có luật |
| S5 | PR mở tự động | `.github/workflows/ops-open-pr.yml:57` `gh pr create` không có `--draft` | PR ra đời ở trạng thái ready |
| S6 | PR sổ sách | 79 PR tiêu đề `land(`/`ghi-so(`/"ghi sổ" từ 24-10 đến 31-10 (tìm kiếm GitHub, đo 31-10) | đơn vị: PR |
| S7 | ghi sổ đệ quy | #1050→#1056→#1060 và #1058→#1071→#1075; #1056+#1060 thêm 14.778 dòng (Codex r2 đo trên diff merge) | ghi sổ sinh ghi sổ |
| S8 | PR sổ sách chạy Windows đầy đủ | #1071 chỉ chạm `ops/reviews/**` (73 tệp): 35 check run; `gate-packet-loop (windows-latest)` 84 phút, `gate-registry (windows-latest)` 82 phút (readback check run, đo 31-10) | `workflow_dispatch` luôn `day_du` |
| S9 | `landed: false` rồi PR "duyệt landed" | #949, #951, #953, #956 (merge trên master); mốc Workflow definition cần GraphQL, 403 trong phiên web | chờ người làm cầu nối dữ liệu |
| S10 | connector tự bắn khi bỏ draft | `ops/reviews/wp461-review-1-codex-verdict.receipt.yaml:337` `auto (Draft marked ready…)` | xung đột với "xong connector rồi mới bỏ draft" |
| S11 | `accept` khoá vào ADR-0054 | `.claude/dev/packet_loop.py:2908` | packet máy sau phải tách |
| S12 | thử bundle | xem §6 `B1` | đo trước khi ghi luật |

## 2. Thay đổi (mỗi mục chiếu vào một đường dẫn của write set)

1. **`docs/adr/0060-dieu-kien-merge-va-moc-ready.md` (mới)** — ADR độc lập, trạng thái `Accepted` khi chủ kho duyệt
   `spec_hash`. Không kích hoạt, không sửa, không mượn hiệu lực của `ADR-0054`. Nội dung bắt buộc, mỗi điểm một mục:
   - **M1 Severity.** Điều kiện merge: 0 finding P0, P1, P2 mở. Mỗi P3 hoặc **đóng có bằng chứng** (reviewer xác nhận
     theo bảng lớp §8.3), hoặc **chủ kho miễn** bằng một comment trên PR nêu slug finding, SHA, lý do, hướng xử lý.
     Agent không tự ghi nợ P3. Cấm giảm số lớp bằng gộp slug hoặc đổi hạng. Một vòng vá không giảm số lớp P3 ⇒ dừng,
     checkpoint chủ kho. Thay bảng ngưỡng §8 cho packet áp ADR-0060; P0 vẫn chặn như cũ.
   - **M2 Review theo lớp.** Reviewer khái quát biểu hiện thành lớp nguyên nhân và quét mọi biểu hiện cùng lớp trước
     khi báo. Cách ghi giữ nguyên §8.3.
   - **M3 Windows.** Phân loại `required` / `not_required` / `unknown`:
     `required` khi diff chạm `*.ps1`, `*.cmd`, `*.bat`, `scripts/deploy-*`, `.claude/dev/**`, `.github/workflows/**`;
     hoặc thêm/sửa dòng chứa `os.name`, `sys.platform`, `platform.system`, `subprocess`, `encoding=`, `os.sep`, `pathlib`;
     hoặc đặc tả khai `windows: required`.
     `not_required` khi diff **chỉ** chạm `*.md`, `docs/**`, `ops/land/**`, `ops/reviews/**`, `ops/specs/**`.
     Còn lại `unknown`: reviewer phải chốt `required` hoặc `not_required` kèm lý do trong verdict. Reviewer được nâng
     mức; agent không được hạ.
     `required` ⇒ chạy trên máy Windows của chủ kho qua Desktop Commander theo `ADR-0057`/`0058`/`0059` (khoá, kiểm tải,
     cô lập, sổ đo). Cộng thêm vào Windows CI, không thay. "Xanh" = tập test ID đỏ trên ứng viên **nằm trong** tập đỏ
     trên SHA nền, hai lượt cùng máy, dựng trong cùng một lệnh; ca đỏ thuộc tệp trong write set ⇒ chủ kho quyết.
     Máy không `Online`: sau **15 phút** báo chủ kho; sau **24 giờ** packet sang `blocked`. Không tự miễn.
     Với packet áp ADR-0060 điều này **thay** câu "máy offline thì vế này không áp" của `ADR-0057` §2.
   - **M4 Đưa ứng viên sang Windows.** Clone nền từ GitHub trong thư mục riêng của phiên, nhập git bundle của ứng viên,
     kiểm commit, tree và cha khớp, rồi mới test. Căn cứ: §6 `B1`.
   - **M5 Push.** Nhánh code đẩy một lần chính, sau khi review offline approve và gate trước push đạt trên đúng SHA.
     Tối đa **hai** lần push thêm cho mỗi PR, mỗi lần có checkpoint chủ kho và ghi biên nhận (SHA trước/sau, lý do).
     Quá hai lần ⇒ đóng PR, generation mới. Không có không gian tên nào được miễn đếm.
   - **M6 Draft và đề xuất merge.** PR mở ở draft. Khi chưa đủ mọi điều kiện, cấm cả bốn: bỏ draft; nói "sẵn sàng
     merge"/"có thể merge" ở bất kỳ đâu; gọi merge; bật auto-merge. Báo theo mẫu `CHƯA ĐỦ ĐIỀU KIỆN MERGE: thiếu …`.
     Điều kiện bỏ draft: CI bắt buộc xanh trên đúng head (bốn mốc §10.2.2 nếu đo được, thiếu thì ghi thiếu); connector
     đã review đúng commit (dòng `Reviewed commit:` cho đúng SHA, đã đọc các finding); M1 đạt; M3 đạt nếu `required`;
     PR head = SHA đã approve. Commit mới ⇒ về draft. Connector gọi bằng comment `@codex review` khi còn draft;
     điều khoản này chỉ có hiệu lực khi §6 `C1` có kết quả ĐẠT ghi trong ADR, trước đó ghi thẳng là chưa đo.
   - **M7 Một lần duyệt.** Chủ kho duyệt **một lần**, neo SHA H, bao gồm: merge, thu bằng chứng hậu merge, ghi sổ, nhả
     lease, đóng WP. Hậu kiểm thất bại ⇒ không `landed`, không đóng WP. Agent không tự duyệt.
   - **M8 Sổ sách.** Ghi sổ hoàn tất = một **bản ghi có cấu trúc** đăng lên Issue của WP và đọc lại khớp. Trường tối
     thiểu: packet/revision/generation/spec_hash; H và tree(H); biên nhận review và xử lý từng finding; Windows local và
     CI PR; duyệt của chủ kho; merge M, cha, tree(M), CI master; nghiệm thu từng mục; nhả lease. Bản ghi này là **điểm
     cuối**: không review model, không mở PR, không chạy Windows cho nó. Sửa = bản ghi mới trỏ bản cũ.
     **Làn lưu trữ**: một PR lưu trữ mỗi tuần, chỉ chứa bản ghi thụ động trong `ops/reviews/**` và `ops/land/**`
     (không `ops/leases/**`, không `ops/specs/**`), không cross-review model, không Windows, không chặn đóng WP.
     Lease và đặc tả đi làn thường.
   - **M9 CI.** Giữ CI PR và CI master hậu merge; gate local không thay CI. `full_mutant_audit` bắt buộc khi diff chạm
     `.claude/dev/**`, `ops/**/*.py` hoặc `.github/workflows/**`; còn lại không bắt buộc. Ghi thẳng: chú thích
     `ci.yml:869` hiện rộng hơn luật này và chưa sửa (nợ, ngoài write set).
   - **M10 Hiệu lực.** Luật áp cho một packet khi và chỉ khi blob đặc tả có đúng một dòng
     `^dieu_kien_merge: ADR-0060@([0-9a-f]{40})$` và OID qua ba phép đo của `ADR-0053` mục *Hiệu lực* (thay đường dẫn).
     Không hồi tố.
   - **M11 Cưỡng chế.** Lúc land: 0 cổng. Đo trên đủ các vị trí cổng mà §20 liệt kê, ghi lệnh và kết quả từng vị trí.
     Nêu tên ba packet kế nhiệm: B (collector bốn mốc, phần còn lại của #899), C (cổng điều kiện merge và đóng WP trong
     `packet_loop.py`, tách khỏi `ADR-0054`), D (gọn hiện vật review và validator làn lưu trữ).
2. **`docs/PROTOCOL_DA_PHIEN.md`** — đúng ba chỗ, câu trung tính, không chép doctrine: một dòng ADR-0060 vào bảng §20
   (cột cổng: `không cổng — kỷ luật executor/reviewer`); một câu con trỏ ngay dưới bảng ngưỡng §8; một câu con trỏ trong
   §10.2.4 cạnh câu con trỏ `ADR-0057`.
3. **`.github/workflows/ops-open-pr.yml`** — thêm `--draft` vào lệnh `gh pr create`. Không đổi gì khác.
4. **`.claude/skills/cross-review/SKILL.md`** — một dòng con trỏ tới ADR-0060 (M1–M3, M6).
5. **`.claude/skills/work-packet/SKILL.md`** — một dòng con trỏ tới ADR-0060 (M5, M6).
6. **`.claude/skills/land-packets/SKILL.md`** — một dòng con trỏ tới ADR-0060 (M7, M8).

## 3. Write set
`docs/adr/0060-dieu-kien-merge-va-moc-ready.md` (planned) · `docs/PROTOCOL_DA_PHIEN.md` ·
`.github/workflows/ops-open-pr.yml` · `.claude/skills/cross-review/SKILL.md` · `.claude/skills/work-packet/SKILL.md` ·
`.claude/skills/land-packets/SKILL.md`. Không ký tự đại diện. `ai-dang-giu` đo 31-10 sau khi fetch đủ 724/724 nhánh:
`NGƯỜI_GIỮ 0` cho cả sáu tệp. Phải đo lại trước khi cấp lease.

## 4. Nghiệm thu (mỗi tiêu chí kèm phép đo làm nó ĐỎ)
- **A1** `python .claude/dev/packet_loop.py adr-song --root .` rc=0. Đỏ: bỏ dòng §20 của ADR-0060.
- **A2** `python .claude/dev/packet_loop.py doctrine-scan --root .` rc=0. Đỏ: chép một đoạn luật M-x vào adapter.
- **A3** `python scripts/tl.py doc-claims-check --json` cho `ok`.
- **A4** `actionlint .github/workflows/ops-open-pr.yml` rc=0, và đúng một dòng khớp `--draft` trong khối
  `gh pr create`. Đỏ: xoá `--draft`.
- **A5** `git diff --numstat <base>..<head>`: đúng 6 tệp của §3, tổng dòng thêm ≤ 450. Đỏ: chạm tệp thứ bảy.
- **A6** Vế dương (đo trên văn bản ADR đã gộp khoảng trắng trong từng đoạn): có đủ các cụm
  `CHƯA ĐỦ ĐIỀU KIỆN MERGE`, `15 phút`, `24 giờ`, `required`, `not_required`, `unknown`, `hai lần push thêm`,
  `dieu_kien_merge: ADR-0060@`. Vế âm: ADR không chứa câu kích hoạt ADR-0054 (`kích hoạt \`ADR-0054\``).
  Đỏ: xoá một cụm; thêm câu kích hoạt.
- **A7** Các bộ test đang ghim workflow vẫn đạt: `python ops/lease_publish_test.py` và
  `python .claude/dev/ci_dang_ky_test.py` (N/N, hai số bằng nhau). Đỏ: đột biến đổi `on:` của `ops-open-pr.yml`.
- **A8** Cross-review Codex tới 0 P0–P2 và mọi P3 đóng hoặc được chủ kho miễn (chính M1). Reviewer đi qua văn bản
  ADR theo bốn ca và phải ra đúng kết luận: (i) còn một P2 mở ⇒ không đề xuất merge; (ii) Windows `required` đang
  chạy ⇒ PR ở draft; (iii) `unknown` chưa được chốt ⇒ chặn; (iv) PR "lưu trữ" có sửa `ops/leases/**` ⇒ không thuộc
  làn lưu trữ.
- **A9** Windows: packet này **`required`** theo chính M3, vì chạm `.github/workflows/ops-open-pr.yml` và
  `.claude/**`. Chạy A1, A2, A4 (nếu máy có `actionlint`) và A7 trên máy Windows theo M3/M4, ghi sổ đo. Đỏ: một ca
  đỏ trên ứng viên mà không đỏ trên nền.

## 5. Ngoài phạm vi
- Không viết cổng máy (packet C), collector (packet B), validator làn lưu trữ (packet D).
- Không sửa `ci.yml` (kể cả chú thích dòng 869), `ci-dot-bien-du.yml`, `ADR-0054`, `ADR-0057`/`0058`/`0059`.
- Không đổi branch protection hay required checks.

## 6. Đo trước khi đóng băng
- **B1 — git bundle sang Windows.** Kết quả: xem phụ lục §8 (điền trước khi tính băm).
- **C1 — connector chạy trên PR draft bằng `@codex review`.** `chua_do_duoc` lúc đóng băng; đo trên PR đầu tiên của
  packet này. Chưa đo ⇒ M6 ghi điều khoản connector là chưa hiệu lực.
- Branch protection của `master`: `GET …/branches/master/protection` ⇒ HTTP 403 "Resource not accessible by
  integration" (đo 31-10). `chua_do_duoc`.

## 7. hinh_dang_ke_thua
`khong_ap_dung` — không phải packet khắc phục.

## 8. Phụ lục B1 — kết quả thử bundle (ĐẠT)

Đo 31-10-2026 12:54:59Z–12:55:28Z trên `tra-luat-win` (`Online` trong `list_devices`; ASUS-LAPTOP `Offline`), theo
`ADR-0057`/`0058`/`0059`: khoá `C:\tl-win\KHOA.txt` rỗng trước khi lấy, 0 `python.exe` lúc kiểm tải, lấy khoá 5 trường,
thư mục riêng `C:\tl-win\session_015GtxrYPjZCTZeRiazdssgq\`, nhả khoá (0 byte) sau khi đọc lại, một dòng `do-luong.csv`.

| bước | kết quả |
|---|---|
| ứng viên (chỉ cục bộ, không push) | H `2a984ec33db68f660918e4a998b4f013b7cec8b6`, tree `cd711764a877187e0966658a753a8acb826043f0`, cha `086f1b7` |
| bundle | `git bundle create … 086f1b7..HEAD`: 882 byte, sha256 `26fdd01c1fb9d862e2dcc374b40be7434f384b8c845b66a79e59532eadf74576`; chuyển dạng base64 qua `write_file` của Desktop Commander; giải mã trên máy, sha256 khớp |
| clone nền | `git clone --filter=blob:none --no-checkout https://github.com/ducthangho/tra-luat.git`: 4 s; nền `086f1b7` có |
| nhập | `git bundle verify` ⇒ `is okay`; `git fetch <bundle> HEAD:refs/ung-vien/thu`; H, tree, cha khớp từng hash |
| checkout | 20 s (blob tải muộn) |
| kiểm nhẹ | `python .claude/dev/packet_loop.py adr-song --root .` trên H ⇒ rc=0 |
| tổng | 28 s |

Giới hạn của phép đo: một commit, bundle 882 byte. Bundle lớn hơn phải chia nhiều lần `write_file`; chưa đo trần
kích thước. Log PowerShell hiển thị lỗi mã hoá ký tự (`sß║ích`) do chuyển hướng `*>`; không ảnh hưởng hash hay rc.
