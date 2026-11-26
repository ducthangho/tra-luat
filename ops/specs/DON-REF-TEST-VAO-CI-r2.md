# DON-REF-TEST-VAO-CI r2 — đưa phản chứng của `ops-don-ref.yml` vào CI qua sổ đăng ký
packet_id: DON-REF-TEST-VAO-CI
revision: 2
tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587

Trạng thái: `proposed`, chưa đóng băng, chưa có lease. Đặc tả không cấp việc (protocol §3.2, §4).
Soạn 26-11-2026 trên `origin/master` `b1db69429d272cfde43681b4a9de1184c452c0f1` qua skill `soan-spec`, bởi
phiên Claude Code trên web nhận bàn giao ở #1540 issuecomment-7197522583. Giờ ghi cạnh số là UTC ngày 26-11-2026.
Đo lại trước mỗi bước công bố (đăng băm, cấp lease, push, merge).

Thay r1 (`ops/specs/DON-REF-TEST-VAO-CI-r1.md` @ `2daffe8a9cfcb5cfa7c722dd0350091c4f693517`, băm
`467397aa…ef266`, chủ kho đã duyệt). r1 không sửa đè. Quyết định thiết kế của r1 giữ nguyên: wrapper
`ops/don_ref_chot_test.py` + mục `MOI`; không sửa `ci.yml`; nợ `CI-PROVENANCE-KHONG-DOC-KET-QUA-CHAY`; chạm E5.

Đổi so với r1, kèm căn cứ:

| # | đổi | căn cứ |
|---|---|---|
| D1 | thêm dòng `dieu_kien_merge` | chủ kho đồng ý (bàn giao, điểm 1). Theo `ADR-0062` N1, ADR-0060 đã áp mặc định; dòng này đúng một dòng, qua ba phép đo (N8), nên không đổi luật áp, chỉ ghi tường minh |
| D2 | M3 Windows `required`, chạy local bằng bundle trước push | ADR-0060 M3 bước 2 (diff chạm `.claude/dev/**`), M4 |
| D3 | M9 `full_mutant_audit` | ADR-0060 M9 (diff chạm `.claude/dev/**`, `ops/**/*.py`) |
| D4 | M5, M6, M8, M12 vào `luat_dung` | chủ kho đồng ý; ADR-0060 |
| D5 | định danh: H1 và `packet_id` cùng là `DON-REF-TEST-VAO-CI` | r1 khai H1 `DON-REF-TEST-VAO-CI` nhưng `packet_id: DON-REF-TEST-VAO-CI-r1`. Với lease có `spec_ref`, `_spec_merge` (`.claude/dev/packet_loop.py`, K1 theo `ADR-0063`) gom cả hai giá trị và đòi đúng một ⇒ r1 làm K1 ĐỎ |
| D6 | wrapper tìm `bash` qua `ops/bash_nen.py::tim_bash()` | N9. r1 chỉ ghi "tìm `bash`"; lời gọi trần bị cổng `bash_nen.py quet` chặn, và trên Windows `shutil.which("bash")` trả bộ phóng WSL |
| D7 | A1 bỏ con số `148/149` | N1b: đo lại ra `145/149`; con số phụ thuộc rig, tín hiệu ổn định là dòng `KHÔNG ĐO ĐƯỢC` và hai số khác nhau |

## 1. `packet_id` · `packet_issue`

| trường | giá trị |
|---|---|
| packet | `DON-REF-TEST-VAO-CI`, revision 2, generation 1 |
| `packet_issue` | #1540 (`open`, đọc qua MCP lúc 16:21Z) |
| mission | không |
| base | `origin/master` lúc cấp lease; phải là tổ tiên của `origin/master` lúc đó |
| lease | khai `spec_ref` `refs/heads/ops/don-ref-test-vao-ci-spec@<OID40 của commit chứa r2>`, `spec_path` `ops/specs/DON-REF-TEST-VAO-CI-r2.md`, `packet_id` `DON-REF-TEST-VAO-CI`, `revision` 2 (ADR-0063) |

## 2. `nguon_cap_viec`

Không thuộc dòng kế hoạch nào. Nguồn: hồ sơ land #1532 (PR #1537, merge `c4d707e`), mốc Gate output §10.2.2 ra
`not_measured` vì không log CI nào có dấu hiệu dương của `ops/don_ref_chot_test.sh` —
https://github.com/ducthangho/tra-luat/issues/1532#issuecomment-7180017463. Chủ kho giao packet ở #1540.

## 3. `review_class`

`sensitive`. Packet chạm `.claude/dev/ci_dang_ky_test.py`, mã của bước `test registry (phạm vi + các bộ chưa được
nối)` trong job `gate-registry`, một cổng chặn merge (protocol §8, fail-closed).

## 4. Số đo nền (để quyết, không phải để nghiệm thu)

Clone **không shallow** (đã `fetch --unshallow` lúc 16:22Z), `origin/master` `b1db694`. So tập tên ref lúc 16:22:46Z:
máy chủ 375 nhánh, cục bộ 375, thiếu cục bộ 0.

- N0. Trôi từ nền r1 (`1260fa0`) tới `b1db694`, trên năm tệp liên quan: chỉ `.claude/dev/ci_dang_ky_test.py` đổi
  (+11/−4, commit `f23feeb` của wp1463, thêm `ops/ci_provenance_test.py` vào `NHE`/`MAU_DAY_DU`/`MAU_NHE`/`VUNG_THEM`).
  Không đụng `MOI`, `CACH_LY`, `tim()`, `kiem()`, `_chay_co_lap`.
- N1. `bash ops/don_ref_chot_test.sh </dev/null` lúc 16:24:46Z: rc=0, dòng cuối `don_ref: 149/149 đạt (chốt + bước
  làm)`, 2,3 giây tường. Đơn vị của 149: phép kiểm (`QUA+HONG`) bộ test tự đếm.
- N1b. Cùng lệnh với `PATH` là thư mục symlink tới mọi tệp chạy được trên `PATH` trừ `actionlint` (khoảng 16:27Z): rc=1,
  có dòng `KHÔNG ĐO ĐƯỢC: thiếu actionlint`, dòng tổng `don_ref: 145/149`. Ba phép kiểm đỏ thêm (`xoá HAI ref`, `đếm
  push có lease`, `stale info`) không liên quan `actionlint`; nguyên nhân của ba ca ấy trong rig: KHÔNG ĐO ĐƯỢC.
- N2. Bộ test gọi `"$AL" -shellcheck= -pyflakes= "$YML"` (dòng 577): cần `actionlint`, không cần `shellcheck`.
- N3. `ops/cai_actionlint.sh` chỉ được gọi ở job `gate`, `gate-cong-cu`, `gate-registry`, `gate-packet-loop-manh`
  (`ci.yml` dòng 174, 613, 1082, 1162); `gate-registry` gọi nó trước bước `test registry`. Job `gate-ops` không có.
- N4. `tim()` chỉ quét `*_test.py`; `ops/` chỉ nhận tệp mức đỉnh. Mục `MOI` không có tệp ⇒ `kiem()` báo `mục đăng
  ký không có tệp`; tệp `ops/*_test.py` không đăng ký ⇒ `test sống chưa đăng ký`.
- N5. `MOI` có 18 khoá (16:26Z); 17 khoá không có lời gọi `python <đường>` trực tiếp trong `.github/workflows/*.yml`
  (chỉ `ops/nhanh_don_duoc_test.py` có), nên `ops/ci_provenance.py` (`RE_LOI_GOI`, dòng 50) ra `not_measured` cho chúng.
- N6. `--chay` gọi mỗi bộ bằng `_chay_co_lap([sys.executable, path], …)`: env là bản sao `os.environ` chỉ đổi
  `TMPDIR/TEMP/TMP` và biến mốc. `actionlint` mà bước cài đưa lên `PATH` thấy được trong bộ con.
- N7. `python ops/lease_publish.py ai-dang-giu <đường>` lúc 16:23:38Z: `NGƯỜI_GIỮ 0` cho
  `.claude/dev/ci_dang_ky_test.py`, `ops/don_ref_chot_test.py`, `ops/don_ref_chot_test.sh`, `.github/workflows/ci.yml`,
  `ops/specs/DON-REF-TEST-VAO-CI-r2.md`. Lease `wp1463-r17-g5-claude` ra `HẾT_HẠN` (PR #1551 đã merge vào `b1db694`).
- N8. Ba phép đo hiệu lực (16:22Z, clone không shallow), mỗi OID L: `git cat-file -e L:<adr>` · `git cat-file -e
  L^1:<adr>` · `L` có trên `git rev-list --first-parent origin/master`.
  `ADR-0060@36d7c5dc…` 0 · 128 · có. `ADR-0055@d2e3052d…` 0 · 128 · có. `ADR-0053@8ab10079…` 0 · 128 · có.
- N9. `ops/bash_nen.py` là bộ giải `bash` dùng chung (`tim_bash()` trả `(đường, chẩn_đoán)`, `None` = KHÔNG ĐO ĐƯỢC)
  kèm cổng `python ops/bash_nen.py quet` chặn lời gọi `bash` trần mới trong `ops/**`. Trên nền khoảng 16:24Z: `quet` in `DAT:
  không có lời gọi trần mới`, rc=0. Mẫu dùng: `ops/cloud_agent_creds_test.py` dòng 17 (`import bash_nen`) và 740.
- N10. `python3 -m ruff check --select F .claude/dev/ci_dang_ky_test.py` trên nền: `All checks passed!` (0 F).
- N11. `python .claude/dev/ci_dang_ky_test.py </dev/null` trên nền, 16:25:16Z–16:30:51Z: `ĐĂNG KÝ: 33/33`,
  `PHẢN CHỨNG: 1677/1677 đỏ đúng` (đơn vị: ca phản chứng của `phan_chung()`), `TỔNG: ĐẠT`, rc=0. A6 đo N(H) − 1677.
- N12. `list_devices` của Desktop Commander khoảng 16:28Z: bốn máy `Online` (`ASUS-LAPTOP`, `DESKTOP-T9R33P2`, hai bản ghi
  `tra-luat-win`). Máy nào thuộc phạm vi do `ADR-0058` quyết, không do đặc tả này.
- N13. K1 trên r1 (16:29Z, `_spec_merge` với lease giả có `spec_ref` @ `2daffe8a`, `spec_hash` `467397aa…`):
  `packet_id` `DON-REF-TEST-VAO-CI` ⇒ ném `spec packet_id không khớp lease`; `DON-REF-TEST-VAO-CI-r1` ⇒ ném cùng lỗi.
  Căn cứ của D5.

## 5. `write_set`

1. `ops/don_ref_chot_test.py` — tệp MỚI.
2. `.claude/dev/ci_dang_ky_test.py`
3. `ops/specs/DON-REF-TEST-VAO-CI-r2.md` — chính đặc tả này, nguyên byte đã duyệt (ADR-0063: blob tại H phải cùng
   bytes với blob ở `spec_ref`).

`ops/leases/**`, biên nhận review và sổ sách đi đường của protocol, không thuộc write set mã. Dự kiến 3 tệp, dưới
400 dòng thêm tính cả đặc tả; trần `ADR-0053` 6 tệp / 450 dòng thêm. Vượt trần thì dừng theo `luat_dung`.

## 6. `ngoai_pham_vi`

- **Không sửa `.github/workflows/ci.yml`.** Đăng ký vào `MOI` thì bước `--chay` sẵn có chạy bộ mới.
- **Không dạy `ops/ci_provenance.py` đọc kết quả `--chay`** (N5). Ghi nợ `CI-PROVENANCE-KHONG-DOC-KET-QUA-CHAY` và mở
  Issue riêng (M5). Không thêm bước gọi thẳng vào `gate-registry` (khoá bằng `LENH_REGISTRY`, `BAM_GATE_REGISTRY`).
- **Không mở rộng sổ hay `ci_provenance` để nhận `.sh`.**
- **Không sửa `ops/don_ref_chot_test.sh`, không port nó sang Windows.** Đỏ trên Windows thì cách ly (M4), không vá.
- **Không sửa `ops/bash_nen.py`.** Wrapper chỉ gọi nó.
- **Không thêm khối đột biến tự chạy vào bộ `don_ref`.**

## 7. `muc_tieu`

| # | mục tiêu | đường dẫn |
|---|---|---|
| M1 | Wrapper `ops/don_ref_chot_test.py`: lấy `bash` bằng `ops/bash_nen.py::tim_bash()` (nạp theo đường tính từ chính tệp); `None` ⇒ in `KHÔNG ĐO ĐƯỢC: không tìm được bash` kèm chẩn đoán, thoát 2. Có `bash` thì chạy `ops/don_ref_chot_test.sh` (đường tính từ chính tệp) với `stdin=DEVNULL`, chuyển nguyên stdout/stderr, thoát bằng đúng rc của bộ con. Ép stdout/stderr sang UTF-8 trước khi in. Không gọi `shutil.which("bash")`, không pipeline, không cắt output, không tự in dòng `don_ref:` | `ops/don_ref_chot_test.py` |
| M2 | Mục `MOI` cho `ops/don_ref_chot_test.py`, mẫu `^don_ref: ([1-9]\d*)/(\1) đạt \(chốt \+ bước làm\)$` | `.claude/dev/ci_dang_ky_test.py` |
| M3 | Ca tự kiểm tiền tố `p1540-` trong `phan_chung()`, đo M1 và M2 (mục 8) | `.claude/dev/ci_dang_ky_test.py` |
| M4 | Windows. Lượt local (ADR-0060 M3) chạy trước push. Wrapper ĐỎ trên Windows local ⇒ E2 (ADR-0060 M3(c): ca đỏ thuộc write set, chủ kho quyết), mang theo log và đề xuất thêm vào `CACH_LY` mục `moi_truong: github-actions/windows`, `slug` `don-ref-test-chua-chay-duoc-tren-windows`, `ly_do`, `log` — thêm vào ứng viên TRƯỚC push nếu chủ kho chọn. Sau push, một lượt `workflow_dispatch` `ci.yml` `runner_set=windows-only` cộng thêm, đo A7 | `.claude/dev/ci_dang_ky_test.py` |
| M5 | Ghi nợ `CI-PROVENANCE-KHONG-DOC-KET-QUA-CHAY` trong chú thích ngay trên mục `MOI` của M2, mở Issue mô tả nợ (dẫn N5) | `.claude/dev/ci_dang_ky_test.py` |

## 8. `nghiem_thu`

Đo trên SHA ứng viên H, trừ khi ghi khác. Đột biến chạy trên bản sao tạm của cây, không trên tệp thật.

| # | tiêu chí | phép đo dương | đột biến / điều kiện làm nó ĐỎ |
|---|---|---|---|
| A1 (M1) | Wrapper chạy bộ thật, giữ rc | `python ops/don_ref_chot_test.py </dev/null` ⇒ rc=0, đúng một dòng khớp mẫu M2 | (a) `PATH` thiếu `actionlint` (rig N1b): bộ con in `KHÔNG ĐO ĐƯỢC: thiếu actionlint`, dòng tổng hai số khác nhau ⇒ wrapper rc≠0. (b) Đột biến wrapper luôn `sys.exit(0)` ⇒ ca `p1540-rc-giu-nguyen` ĐỎ |
| A2 (M1) | Không có `bash` dùng được là fail-close | ca `p1540-thieu-bash`: wrapper với `tim_bash` bị thay để trả `(None, [...])` ⇒ rc≠0, stdout có `KHÔNG ĐO ĐƯỢC` | Đột biến nhánh `None` thành `sys.exit(0)` ⇒ ca ĐỎ |
| A3 (M1) | Không gọi `bash` trần | `python ops/bash_nen.py quet` ⇒ rc=0, `DAT` | Đột biến wrapper dùng `shutil.which("bash")` ⇒ `quet` rc≠0 nêu `ops/don_ref_chot_test.py` |
| A4 (M2) | Mẫu chỉ nhận dòng tổng đủ | ca `p1540-mau`: `bang_chung_xanh` với mẫu M2 nhận `don_ref: 149/149 đạt (chốt + bước làm)`; từ chối `don_ref: 148/149 đạt (chốt + bước làm)`, `don_ref: 0/0 đạt (chốt + bước làm)`, `don_ref: 149/149 đạt`, `don_ref: 149/149 đạt (chốt + bước làm) x`, và văn bản không có dòng ấy | Nới mẫu thành `don_ref: (\d+)/(\d+)` ⇒ ĐỎ ở vế `0/0`; bỏ `$` ⇒ ĐỎ ở vế hậu tố `x` |
| A5 (M2) | Sổ thấy wrapper | `kiem()` trả danh sách lỗi rỗng trên H | Xoá mục `MOI` ⇒ `test sống chưa đăng ký: ops/don_ref_chot_test.py`; xoá wrapper ⇒ `mục đăng ký không có tệp: ops/don_ref_chot_test.py` |
| A6 (M2, M3) | Bộ ca sổ đăng ký đạt | `python .claude/dev/ci_dang_ky_test.py </dev/null` ⇒ `PHẢN CHỨNG: N/N đỏ đúng` hai số bằng nhau, `TỔNG: ĐẠT`, rc=0; N(H) − N(nền) = số ca `p1540-*` đã thêm | Một ca `p1540-*` đỏ, hoặc số ca nền giảm |
| A7 (M2, M4) | CI có dấu hiệu dương | Log `gate-registry (ubuntu-latest)` của lượt PR trên H có `don_ref: N/N đạt (chốt + bước làm)` (N>0, hai số bằng nhau) và dòng kết quả `ĐẠT` của mục `ops/don_ref_chot_test.py`. Lượt `windows-only` cộng thêm: mục ra `ĐẠT`, hoặc `CÁCH LY` với `slug` của M4 | Dòng vắng, hai số khác nhau, `ĐỎ`; hoặc có `CACH_LY` mà lượt ĐẠT (sổ tự báo đã xanh). **Chưa đo được** tới khi có lượt sau push |
| A8 (M4) | Windows local xanh theo ADR-0060 M3 | Trên máy Windows thuộc phạm vi `ADR-0058`, theo `ADR-0057`/`0058`/`0059`: một lệnh dựng hai thư mục (nền = base của lease, ứng viên = bundle của H, kiểm commit/tree/cha khớp) rồi chạy trên mỗi thư mục tập bắt buộc: `python .claude/dev/ci_dang_ky_test.py`, `python ops/bash_nen.py quet`, và trên ứng viên `python ops/don_ref_chot_test.py`. Có danh sách ID kèm kết quả; tập đỏ ứng viên ⊆ tập đỏ nền | Thiếu lượt, lỗi setup, ca `skipped`/`not_run`, ứng viên đỏ ngoài tập nền. Wrapper ĐỎ thuộc write set ⇒ E2 (M4) |
| A9 (M5) | Nợ có tên và có Issue | `rg -n 'CI-PROVENANCE-KHONG-DOC-KET-QUA-CHAY' .claude/dev/ci_dang_ky_test.py` ⇒ ≥1 dòng trong khối chú thích ngay trên mục M2; Issue mới tồn tại và nêu tên nợ | Vắng ở vị trí ấy, hoặc không có Issue. Vế âm trên nền: 0 dòng |
| A10 | Delta cổng chung = 0 | `python3 -m ruff check --select F` trên hai tệp `.py`: số F(H) − số F(nền) = 0; `python .claude/dev/packet_loop.py doctrine-scan --root .` rc=0; `python scripts/tl.py --selftest` N/N bằng nhau; `actionlint` trên `.github/workflows/*.yml` delta = 0 | Delta khác 0 |
| A11 (D3) | `full_mutant_audit` (ADR-0060 M9, K7) | một lượt `ci-dot-bien-du.yml` `workflow_dispatch` trên H, run và mọi job `success` | Run hoặc job khác `success`. **Chưa đo được** tới khi có lượt sau push |
| A12 (D5) | Định danh spec qua K1 | trước khi đăng băm: gọi `_spec_merge` (với `PYTHONPATH=.claude/dev`) của `.claude/dev/packet_loop.py` trên commit chứa r2 với lease giả có `spec_ref`, `spec_path`, `packet_id` `DON-REF-TEST-VAO-CI`, `revision` 2, `spec_hash` = băm r2 ⇒ không ném | Đổi `packet_id` lease thành `DON-REF-TEST-VAO-CI-r2` ⇒ ném `spec packet_id không khớp lease` |

Giới hạn của A1–A5: wrapper tự in một dòng `don_ref:` giả thì mẫu M2 vẫn khớp. Không cổng nào phân biệt dòng do bộ
`.sh` in với dòng giả; bảo đảm duy nhất là review mã wrapper (M1 cấm tự in). Đừng đọc A4 thành chống giả mạo.

## 9. `tran_*`

Ba dòng khai ở đầu tệp: `ADR-0055` (trần lời gọi Codex), `ADR-0053` (kích thước `sensitive`), `ADR-0060` (điều kiện
merge). Không có dòng `ADR-0052`. Không khai ngân sách mềm. Trước mỗi lời gọi Codex: đếm số đã dùng, đọc trần theo
bảng của `ADR-0055`, và gọi `packet_loop.py record-codex-call` cho TỪNG lời gọi.

## 10. `luat_dung`

- Điểm dừng của `docs/PROTOCOL_DA_PHIEN.md` §12, theo đúng ngưỡng ở đó.
- ADR-0060 M1: điều kiện merge 0 P0/P1/P2 mở; P3 đóng có bằng chứng hoặc chủ kho miễn — xin miễn là **E2** (quyền
  miễn thuộc chủ kho), mang slug, SHA, lý do, hướng xử lý. Vòng vá vì P3 không giảm số lớp P3 ⇒ dừng, **E1**.
- ADR-0060 M2 và §8.3: reviewer khái quát mỗi biểu hiện thành lớp và quét cả lớp; executor vá theo lớp, mỗi đường vào
  của lớp một chốt riêng. Một hình dạng lỗi lặp lại sau khi đã đổi thiết kế ⇒ **E1**.
- ADR-0060 M3: máy Windows không `Online` quá hạn báo của *Tham số* ⇒ **E2**; quá hạn chờ ⇒ packet `blocked`. Ca đỏ
  thuộc write set ⇒ **E2** (M4).
- ADR-0060 M12 (review offline trước push): mỏ neo là SHA ứng viên cục bộ và bundle; handoff, verdict, biên nhận đăng
  lên Packet Issue #1540; review Codex offline qua `launcher.py run`.
- ADR-0060 M5: nhánh code push MỘT lần chính, sau khi review offline approve và gate trước push đạt trên đúng SHA,
  và sau lượt Windows local (A8). Mỗi lần push thêm là **E2** (checkpoint chủ kho) kèm một dòng biên nhận SHA
  trước/sau và lý do; quá số lần ở *Tham số* ⇒ đóng PR, generation mới.
- ADR-0060 M6: PR mở ở draft. Chưa đủ điều kiện thì không bỏ draft, không nói "sẵn sàng merge", không gọi merge, không
  bật auto-merge; báo bằng `CHƯA ĐỦ ĐIỀU KIỆN MERGE: thiếu …`. Commit mới ⇒ PR về draft. Kiểm bằng
  `packet_loop.py kiem-merge` trước khi bỏ draft. Chủ kho tự merge.
- ADR-0060 M8: sổ sách là bản ghi có cấu trúc đăng lên #1540 và đọc lại khớp. Không commit bằng chứng vào nhánh code
  sau approve.
- Trần lời gọi Codex của `ADR-0055` chạm ⇒ **E2**, mang mức đã dùng, còn thiếu bao nhiêu, để làm gì.
- Diff vượt trần `ADR-0053` ⇒ **E2**, mang số tệp và số dòng thêm (`git diff --numstat`) và khối `nang_tran`.
- Lượt `workflow_dispatch` (A7, A11) không gọi được, hoặc hết phút CI ⇒ **E2**, mang lỗi gọi và số phút đã dùng.
- Muốn đạt A7 mà buộc phải sửa `ci.yml` ⇒ **E3** (đảo quyết định của chủ kho ở r1), mang bằng chứng và hậu quả.

## 11. `pham_vi_e`

- **E5: chạm.** `.claude/dev/ci_dang_ky_test.py` là mã của một cổng chặn merge. Hệ quả: chủ kho duyệt băm đặc tả,
  chủ kho audit, chủ kho merge.
- **E4: không chạm.** Không xoá ref, không đẩy Package, không đọc/ghi secrets, không đổi ruleset. Hai lượt
  `workflow_dispatch` chỉ đọc, huỷ được. Lượt Windows local làm trong thư mục riêng của phiên trên máy chủ kho.

## 12. `hinh_dang_ke_thua`

`khong_ap_dung`. Không phải packet khắc phục của một lượt review; hồ sơ #1532 không ghi hình dạng lỗi nào cho chỗ trống
này. Lỗi định danh của r1 (D5) là lỗi của đặc tả, ghi ở đây để lượt review biết: lớp "hai khai báo định danh không
nhất quán".

## 13. `chua_do_duoc`

- Wrapper trong `--chay` với `actionlint` của bước cài: suy từ N3, N6, chưa chạy thật. Đo ở A1, A5, A6; trên runner ở A7.
- Bộ `don_ref` trên Windows: chưa từng chạy. Máy Windows có `actionlint` và Git Bash không: chưa đo. Thiếu
  `actionlint` thì bộ con tự ĐỎ (N1b) ⇒ đặt `actionlint` 1.7.7 trong thư mục phiên cho lượt ấy, không cài hệ thống;
  không đặt được ⇒ **E2**.
- Thời gian thêm vào `gate-registry` trên runner: chưa đo (container: 2,3 giây).
- `ci_provenance` cho mốc Gate output của packet này vẫn ra `not_measured` (N5). Hồ sơ land đo mốc ấy bằng dấu hiệu
  dương từng bước (A7).
