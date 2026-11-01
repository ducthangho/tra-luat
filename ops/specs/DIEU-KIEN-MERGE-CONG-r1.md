# Đặc tả packet `DIEU-KIEN-MERGE-CONG` r1: cổng điều kiện merge và đóng WP trong `packet_loop.py` (ADR-0060 packet C)

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587

| trường | giá trị |
|---|---|
| packet_id | `DIEU-KIEN-MERGE-CONG`, revision 1, generation 1 |
| packet_issue | #1106 |
| nguon_cap_viec | packet kế nhiệm **C** của `ADR-0060` mục *Cưỡng chế — M11*. Chủ kho mở theo chỉ thị 01-11-2026, phiên `session_015GtxrYPjZCTZeRiazdssgq` (*"Mở packet tiếp theo của ADR-0060 luôn"*); cây quyết định chốt qua ba vòng hỏi, rồi chủ kho duyệt **bản gọn** sau hai lượt Codex (review đặc tả + phản biện thiết kế, cùng ngày) |
| ưu tiên | chủ kho: gọn nhẹ, tốc độ chạy, hiệu năng quy trình **hơn** độ chặt của vật chứng. Chỉ giữ chốt chặn lỗi đã xảy ra hoặc sửa rẻ |
| review_class | `sensitive` — thêm cổng vào `.claude/dev/packet_loop.py` (vị trí cổng §20) |
| base | `origin/master` lúc cấp lease (đo khi soạn, 06:20Z 01-11: `a284f8a`) |
| executor / reviewer | `anthropic_claude` (Claude Code remote, Linux) / `openai_codex` qua `launcher.py run` + connector `@codex review` trên PR draft |
| windows | `required` (M3 bước 2: diff chạm `.claude/dev/**`) |

## 1. Vì sao — số đo (05:40Z–06:20Z 01-11-2026)

| # | sự kiện | số đo |
|---|---|---|
| S1 | cổng của `ADR-0060` | **0** dòng nhắc `ADR-0060`/`dieu_kien_merge` ở cả sáu vị trí cổng §20 (bảng M11); §20 khai *"không cổng"* |
| S2 | cửa ra hiện có | `cmd_accept` chỉ chạy khi state có `luat_adr0054 is True`; `ADR-0054` vừa được đóng băng (Issue #813–#816, #834 đóng 01-11) |
| S3 | packet B (#1094) | điều kiện bỏ draft/merge kiểm tay; P3 đối chiếu tay qua 10 lượt offline; biên bản M8 thiếu `generation`, `spec_hash`, `tree_h`, `tree_m` mà không cổng nào bắt |
| S4 | khuôn dùng lại | `_kiem_ci`, `_doc_connector`, `_doc_json` (đã chống khoá JSON trùng), khuôn land-OID của `_che_do_0054`; `launcher.py run` đã ghi `stdout_sha256` trong `run.json` (đo: khớp `sha256sum stdout.log` của run `b4a7887d`) |
| S5 | tham chiếu kích thước | `cmd_accept` #834: +303 dòng thêm (143 mã + 160 test) |

## 2. Thay đổi

Hai lệnh mới trong `.claude/dev/packet_loop.py`, **không đọc, không ghi state**, không đụng máy trạng thái hay `ADR-0054`.
Mỗi lệnh đo MỌI điều kiện đo được, rồi trả 0 khi đủ hết; thiếu ⇒ `RC_GATE` và in `CHƯA ĐỦ ĐIỀU KIỆN MERGE: thiếu …`
(lệnh `kiem-merge`) hoặc `CHƯA ĐÓNG ĐƯỢC WP: thiếu …` (lệnh `kiem-dong-wp`), liệt kê từng điều kiện thiếu (M6).
Đối số sai dạng ⇒ `RC_ARG`. Hằng `CHU_KHO = "ducthangho"` trong mã; **không** có cờ đổi chủ kho.

Mọi YAML đầu vào đọc qua `yaml.compose` trước: khoá phải là scalar chuỗi, không trùng khoá trong cùng mapping, không
anchor/alias; rồi mới `safe_load`. Mọi số nguyên kiểm `type(x) is int` (không nhận `bool`/`float`).

### 2.1 `kiem-merge`

Đối số: `--root`, `--repo`, `--pr`, `--head H` (40 hex), `--base B` (40 hex), `--spec` (đường dẫn trong cây tại H), `--lease <tệp lease>`,
`--workflow-runs`, `--workflow-jobs` (lặp), `--check-runs`, `--connector`, `--offline-run-json`, `--offline-stdout`,
`--p3-offline <slug>` (lặp, có thể vắng), `--chu-kho-comment <readback JSON>` (có thể vắng), `--windows-json <tệp>` (có thể vắng).

| # | điều kiện | phép đo |
|---|---|---|
| K0 | đầu vào neo | `B` là tổ tiên của `H` và `B ≠ H`; `git merge-base --is-ancestor B refs/remotes/origin/master`; `git ls-remote origin refs/pull/<pr>/head` trả đúng H (PR head hiện hành = H, M6; cùng khuôn đối chiếu remote của `cmd_accept`) |
| K1 | hiệu lực M10 | `sha256(blob --spec tại H)` = `spec_hash` của `--lease` (M10: chính blob lease trỏ tới); blob ấy có **đúng một** dòng `^dieu_kien_merge: ADR-0060@([0-9a-f]{40})$`; OID L: `cat-file -e L:docs/adr/0060-…md` rc 0, `cat-file -e L^1:…` rc ≠ 0, L ∈ `rev-list --first-parent refs/remotes/origin/master`; kho không shallow |
| K2 | CI | `_kiem_ci` trên H, `required_checks` = `CHECK_BAT_BUOC` (gọi nguyên hàm) |
| K3 | connector | `_doc_connector(…, repo, pr, H)`: xong trên H, không P0–P2; trả tập P3 connector |
| K4 | review offline M12 | `run.json`: `head` = H, `trang_thai` = `xong`, `ma_thoat` là `int` 0; `sha256(--offline-stdout)` = `run.json.stdout_sha256`; dòng không rỗng cuối của stdout đúng `KET_LUAN: approve` |
| K5 | P3 (M1) | tập P3 mở = P3 connector (K3, khoá `<endpoint>:<id>`) ∪ `--p3-offline`. Rỗng ⇒ đạt. Không rỗng ⇒ `--chu-kho-comment` có `user.login` = `CHU_KHO` và thân có **một** dòng khớp `^mien_p3: H <khoá>(,<khoá>)*$` mà tập khoá **bằng đúng** tập P3 mở |
| K6 | Windows M3 | phân loại §2.3 trên `B..H`. `not_required` ⇒ đạt. `unknown` ⇒ đạt chỉ khi comment chủ kho có dòng `^windows: H not_required$`. `required` ⇒ đạt khi comment chủ kho có dòng `^windows: H mien$`, **hoặc** `--windows-json` = `{sha: H, os: "Windows", tests: [{id, ket_qua}]}` với `tests` khác rỗng, id phân biệt, mọi `ket_qua` ∈ {`passed`, `failed`}, và không `failed` nào |

### 2.2 `kiem-dong-wp`

Đối số: `--root`, `--bien-ban <YAML>`, `--lease <tệp lease>`.

| # | điều kiện | phép đo |
|---|---|---|
| D1 | trường M8 | có đủ, đúng kiểu: `packet` (str), `revision` (int ≥ 1), `generation` (int ≥ 1), `spec_hash` (64 hex), `head_da_review` (40 hex), `tree_h` (40 hex), `review` (map), `windows` (map), `duyet_chu_kho` (URL `https://github.com/…`), `merge_commit` (40 hex), `tree_m` (40 hex), `ci_master` (map `{run_id: int, conclusion: str}`), `nghiem_thu` (map khác rỗng), `lease_cuoi` (str), `landed` (bool), `moc_10_2_2` (map đúng 4 khoá `run`/`checkout`/`workflow_definition`/`gate_output`) |
| D2 | đã land | `landed is True` **và** mọi mốc ∈ {`passed`, `owner_waived`} **và** mọi giá trị của `nghiem_thu` ∈ {`passed`, `owner_waived`} **và** `ci_master.conclusion` = `success`. `landed: false` (dù trung thực) ⇒ chưa đóng được |
| D3 | git | `merge_commit^2` = `head_da_review`; `merge_commit` ∈ `rev-list --first-parent refs/remotes/origin/master`; `rev-parse head_da_review^{tree}` = `tree_h`, `rev-parse merge_commit^{tree}` = `tree_m` |
| D4 | lease đã nhả | tệp lease: `lease_id` = `lease_cuoi`, `packet_id` = `packet`, `generation` = `generation`, và `lease_until` (UTC, hậu tố `Z`) **≤ giờ hiện tại** |

### 2.3 Bộ phân loại Windows (K6) — chép M3, thứ tự, dừng ở bước đầu khớp

1. **Làn lưu trữ:** mọi tệp của diff nằm trong `ops/reviews/**` hoặc `ops/land/**`, **và** mỗi tệp có mode `100644` (không symlink, không thực thi) **và** đuôi thuộc `.md` `.yaml` `.yml` `.json` `.txt` `.log` hoặc tên `SHA256SUMS` ⇒ `not_required`.
2. `required` khi một tệp khớp `*.ps1` `*.cmd` `*.bat` `*.sh` `scripts/deploy-*` `.claude/dev/**` `.github/workflows/**`; hoặc một dòng thêm (`+`, không phải `+++`) trong tệp `*.py` `*.ps1` `*.sh` `*.yml` chứa `os.name` `sys.platform` `platform.system` `subprocess` `encoding=` `os.sep` `pathlib`; hoặc blob `--spec` có dòng `windows: required`.
3. `not_required` khi mọi tệp là `*.md`, hoặc nằm trong `docs/**` `ops/land/**` `ops/reviews/**` `ops/specs/**` mà không mang đuôi `*.py` `*.ps1` `*.sh` `*.cmd` `*.bat`.
4. Còn lại `unknown`.

Bảo đảm cố ý **không** làm (theo ưu tiên gọn): không chạy lượt nền Windows thường lệ (M3(a)); ứng viên đỏ thì
executor tự chạy nền để phân biệt hồi quy và hỏi chủ kho (M3(b)(c)) — lệnh không tự so hai lượt.

### 2.4 Tài liệu

- `docs/adr/0060-…md` mục *Cưỡng chế — M11*: dòng `.claude/dev/packet_loop.py` của bảng đổi thành số đo mới, câu
  *"0 cổng"* thành *"1 cổng"*, packet C đánh dấu đã làm. Không đổi M1–M10, M12.
- `docs/PROTOCOL_DA_PHIEN.md` §20 dòng `ADR-0060`: cột cổng đổi từ *"không cổng — kỷ luật executor/reviewer"* thành
  `packet_loop.py kiem-merge, kiem-dong-wp`.
- `.claude/skills/land-packets/SKILL.md`: thêm một dòng trỏ tới hai lệnh.

## 3. Write set

`.claude/dev/packet_loop.py` · `.claude/dev/packet_loop_test.py` · `docs/adr/0060-dieu-kien-merge-va-moc-ready.md` ·
`docs/PROTOCOL_DA_PHIEN.md` · `.claude/skills/land-packets/SKILL.md`. Năm tệp.

```yaml
nang_tran:
  ai_nang: ducthangho   # chủ kho, protocol §2; chỉ thị 01-11-2026 phiên session_015GtxrYPjZCTZeRiazdssgq: "bản gọn, 6/500"
  can_cu: >-
    Hai lệnh cổng cùng ca test và đột biến đích. Tham chiếu: cửa `accept` của #834 là +303 dòng thêm; phản biện
    thiết kế Codex 01-11 ước bản gọn 250–400 dòng thêm. Khai trần ngay khi đóng băng để khỏi mở PR đặc tả và cấp
    lease giữa chừng (packet B phải nâng hai lần). Không tách: hai lệnh dùng chung readback và khép một quy trình.
  tran_cu: "ADR-0053@8ab1007: <= 6 tệp / <= 450 dòng thêm"
  tran_moi: "<= 6 tệp / <= 500 dòng thêm"
```

## 4. Nghiệm thu

Ca mới trong `.claude/dev/packet_loop_test.py`, tiền tố `cong_c_`. Đột biến đích chỉ cho các chốt trọng yếu, phải
bị giết **đúng lý do** (tín hiệu assertion của ca đích); đột biến làm lệnh traceback không được tính là giết.

| # | tiêu chí | phép đo làm ĐỎ |
|---|---|---|
| A1 | `packet_loop_test.py` N/N, hai số bằng nhau | bất kỳ ca đỏ |
| A2 | `kiem-merge` trên bộ fixture đủ điều kiện ⇒ rc 0; mỗi K0–K6 một ca thiếu ⇒ rc `RC_GATE` và tên điều kiện có trong thông báo; gồm ca PR head ở H2 mà evidence ở H (K0) và ca `--spec` của packet khác có dòng khai hợp lệ nhưng băm khác `spec_hash` của lease (K1) | — |
| A3 | M6: hai điều kiện cùng thiếu ⇒ thông báo nêu cả hai | — |
| A4 | đột biến đích `kiem-merge` (mỗi cái giết ca tương ứng): bỏ so `head` = H (K4) · bỏ so `stdout_sha256` (K4) · không gọi `_doc_connector` (K3) · nhận comment không phải `CHU_KHO` (K5) · so tập khoá bằng ⊆ (K5) · `--windows-json` `tests` rỗng vẫn đạt (K6) · bỏ điều kiện mode/đuôi ở bước 1 §2.3, để `ops/land/x.py` lọt làn lưu trữ (K6) · bỏ phép `L^1` (K1) | đột biến sống ⇒ đỏ |
| A5 | §2.3 bảng ca: `ops/land/a.yaml` ⇒ `not_required`; `ops/land/x.py` ⇒ `unknown` (không trigger) và `required` khi dòng thêm có `subprocess`; `docs/x.ps1` ⇒ `required`; `README.md` thêm chữ `subprocess` ⇒ `not_required`; symlink trong `ops/reviews/` ⇒ không phải bước 1 | — |
| A6 | `mien_p3:` có dòng phủ định ("không miễn") hoặc thiếu H ⇒ không khớp regex ⇒ đỏ; khoá YAML trùng trong `--bien-ban` ⇒ `RC_ARG` | — |
| A7 | `kiem-dong-wp` (đột biến đích thêm: bỏ kiểm `nghiem_thu`; bỏ so PR head ở K0; bỏ so `spec_hash` ở K1): fixture đủ ⇒ rc 0; `landed: true` + một mốc `not_measured` ⇒ đỏ; `landed: false` trung thực ⇒ đỏ; `generation: true` ⇒ đỏ; lease `lease_until` tương lai ⇒ đỏ; `merge_commit^2` ≠ H ⇒ đỏ; `nghiem_thu: {A9: failed}` ⇒ đỏ; `nghiem_thu: {}` ⇒ đỏ; `ci_master.conclusion: failure` ⇒ đỏ | đột biến đích: bỏ D2 · bỏ so `lease_until` với giờ hiện tại · nhận `bool` cho `generation` |
| A8 | canary sau land trên dữ liệu thật: `kiem-dong-wp` trên khối YAML biên bản M8 packet B (#1094 issuecomment-6553638237) ⇒ **đỏ ở D1** (thiếu `generation` `spec_hash` `tree_h` `tree_m`); trên biên bản M8 của chính packet này ⇒ rc 0 trước khi đăng | `chưa đo được` tới sau land; ai đo: executor; ghi lệnh + rc + stdout vào biên bản M8. B mà rc 0 ⇒ D1 mù |
| A9 | `git diff --numstat <base> <ứng viên>`: đúng năm tệp §3, ≤ 500 dòng thêm | tệp thứ sáu ⇒ đỏ |
| A10 | tài liệu, vế dương và vế âm: bảng M11 của ADR-0060 có `kiem-merge` và không còn *"0 cổng"*; dòng §20 `ADR-0060` có `kiem-merge` và không còn *"không cổng — kỷ luật executor/reviewer"*; skill có `kiem-dong-wp`. Đo trên văn bản đã gộp khoảng trắng từng đoạn (L6 b) | khôi phục câu cũ ở từng chỗ ⇒ đỏ chỗ ấy |
| A11 | `doctrine-scan`, `adr-song`, `doc-claims-check` xanh | canh bất biến |
| A12 | Windows (M3 `required`): **một** lượt ca `cong_c_*` trên `tra-luat-win` tại ứng viên, > 0 ca, không ca `skipped` | 0 ca ⇒ đỏ. Lượt nền và phần còn lại của `packet_loop_test.py` trên Windows: **chủ kho miễn** (chỉ thị 01-11) |
| A13 | M9 `full_mutant_audit`: **chủ kho miễn**, thay bằng A4 + A7 + CI Linux xanh | đột biến A4/A7 sống ⇒ đỏ |

## 5. Ngoài phạm vi

- Đo bốn mốc §10.2.2 ở bước merge: collector packet B (`ci_provenance.py thu --wd-run`) làm ở bước land.
- Kiểm `full_mutant_audit` hay required check bổ sung theo lease trong `kiem-merge`.
- Đếm số lần push (M5); đọc P3 từ văn bản tự do của review offline; gắn lệnh vào workflow; sửa `cmd_accept`/`ADR-0054`.
- Biến ADR-0060 thành mặc định (bỏ dòng khai M10) và chuyển bất biến của `ADR-0054` sang protocol: packet tài liệu
  riêng, chủ kho đã duyệt, làm SAU khi packet này land (cùng sửa ADR-0060 và §20).

## 6. `chua_do_duoc`

- Độ đủ của `--p3-offline`: máy chỉ kiểm từng khoá người gọi khai; reviewer offline phải đối chiếu.
- Byte comment trên GitHub: readback qua MCP chuẩn hoá thực thể HTML (CLAUDE.md, đo 22-08-2026). K5/K6 khớp dòng có
  cấu trúc và `user.login`, không so byte.
- `--windows-json` do executor dựng từ log Windows: lệnh kiểm nội dung, không chứng minh nguồn.
- A8 cho tới sau land.

## 7. hinh_dang_ke_thua

`khong_ap_dung` — packet mới. Lớp đã lặp ở packet B (#1094), reviewer quét sớm: *kiểm sau khi bộ phân tích đã
chuẩn hoá* (khoá YAML) **3** lượt; *tin TÊN ref thay vì đo OID* **2** lượt; *so bằng mà Python coi `1 == True == 1.0`*
**2** lượt.
