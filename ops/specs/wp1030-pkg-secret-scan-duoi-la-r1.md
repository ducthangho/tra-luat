# Đặc tả packet wp1030 r1 — `pkg_secret_scan`: tệp có đuôi lạ đi cùng phép lọc nhị phân như tệp không đuôi

Đặc tả đóng băng. Muốn đổi thì soạn `wp1030-pkg-secret-scan-duoi-la-r2.md`, không sửa đè.
Đặc tả KHÔNG cấp việc: cần Issue #1030 + lease còn hiệu lực (`docs/PROTOCOL_DA_PHIEN.md` §3.2, §4).
Chỗ nào đặc tả không nói thì executor DỪNG và hỏi trên #1030, không tự nới.

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

| trường | giá trị |
|---|---|
| `packet_id` · `packet_issue` | `wp1030` · #1030 · revision 1 · generation 1 |
| mission | #748 (chủ kho chỉ định 30-10-2026); tuyến land = mặc định §5 (`mission/748/integration` → draft land PR). Không có ngoại lệ tuyến. |
| `nguon_cap_viec` | chỉ thị chủ kho trong phiên soạn spec 30-10-2026 (đồng ý Q1–Q9; mở Issue #1030, mission #748). Lỗi do executor packet `WINDOWS-LOCAL-MAY-CHU-KHO` r1 phát hiện bằng đọc mã 29-10-2026; phiên soạn spec dựng phản chứng chạy được (mục *Hiện trạng*). |
| `review_class` | **sensitive**: ranh giới security/credential (§8). Reviewer `openai_codex` ⇒ `cross_approved`. |
| base | `origin/master` lúc cấp lease (đo khi soạn: `5f3855ea`, 04:02Z 30-10). |
| executor | `anthropic_claude`, phiên cloud **MỚI**, không phải phiên soạn spec. |
| depends_on | không |

## Hiện trạng (đo 04:02–04:13Z 30-10-2026 trên `5f3855ea`)

- `scripts/pkg_secret_scan.py:36-47` `_is_scannable`: đuôi ∈ `TEXT_SUFFIXES` ⇒ quét không điều kiện. Không đuôi ⇒ quét
  nếu `size ≤ MAX_BYTES` và không có NUL trong 8192 byte đầu. **Đuôi khác ⇒ `return False` (dòng 39–40), bỏ qua
  hoàn toàn.**
- Phản chứng chạy được (bản sao trong scratch, khoá giả dựng lúc chạy từ các mảnh nhỏ): một khoá dạng `GOCSPX-` +
  28 ký tự được bơm vào `a.log`, `b.patch`, `c.csv`, `d.txt`. Bản master chỉ báo `d.txt`. Bản bỏ hai dòng 39–40
  báo cả 4 tệp, và không báo `e.bin` mang NUL đứng trước khoá.
- Toàn cây kho (8168 tệp, trừ `.git`): master quét 6173 tệp, bản bỏ hai dòng quét 8168, tức thêm 1995 tệp (đông
  nhất: `.log` 1115 · `.stdout` 295 · `.stderr` 214 · `.patch` 120). Cả hai bản đều **0 hit**.
- Gói thật (`tl.py release-bundle`, `file_count` 192, giải nén ra 193 tệp): cả hai bản đều 0 hit, delta = 0. Mọi đuôi
  trong `RELEASE_MANIFEST.json` hiện thuộc `TEXT_SUFFIXES` hoặc là rỗng, nên **hôm nay lỗ này chưa làm lọt gì**; nó
  là lỗ tiềm ẩn.
- Bộ quét chưa có ca test nào gọi `_is_scannable`/`scan`.
- Thử trong một clone nháp (thêm fragment rỗng + `changelog.d` → sinh lại bundle + manifest): `test-fragments-check`
  `current`, `golden-test` ok, `release-verify --strict` ok, `determinism-audit` rc=0, `doc-claims-check --strict`
  rc=0 ⇒ **không** phải ghi lại golden.

## `write_set` (exact, 5 tệp)

1. `scripts/pkg_secret_scan.py`
2. `scripts/test_fragments/wp1030_pkg_secret_scan_duoi_la.py` (tệp mới)
3. `scripts/tl_test_fragments_bundled.py` (sinh lại bằng `tl_core.test_fragments.generate_bundled_module_bytes`,
   không sửa tay)
4. `changelog.d/wp-1030.md` (tệp mới)
5. `RELEASE_MANIFEST.json` (sinh lại bằng `tl.py release-manifest --out RELEASE_MANIFEST.json`, không sửa tay)

## `muc_tieu`

- **M1** → `scripts/pkg_secret_scan.py`: trong `_is_scannable`, tệp có đuôi ∉ `TEXT_SUFFIXES` đi **cùng** nhánh với
  tệp không đuôi: quét khi `st_size ≤ MAX_BYTES` và không có `b"\x00"` trong 8192 byte đầu. Lỗi `OSError` vẫn trả
  `False`. Sửa chú thích tại chỗ theo idiom "vX.Y.Z (bằng chứng) — fix": mặc định của bộ quét là QUÉT, chỉ bỏ theo
  thuộc tính ĐO được (nhị phân, quá trần), không bỏ theo tên đuôi.
- **M2** → `scripts/test_fragments/wp1030_pkg_secret_scan_duoi_la.py`: fragment `TEST_ID = "wp1030_pkg_secret_scan_duoi_la"`,
  nạp `scripts/pkg_secret_scan.py` theo đường dẫn tương đối với `tl_module.__file__`, dựng fixture trong
  `tempfile.TemporaryDirectory()`. Khoá giả phải dựng lúc chạy từ các mảnh (không viết nguyên chuỗi khớp mẫu trong
  mã nguồn), để bản thân fragment không thành hit của bộ quét.
- **M3** → `scripts/tl_test_fragments_bundled.py`: sinh lại cho khớp, `test-fragments-check` = `current`.
- **M4** → `changelog.d/wp-1030.md`: một đoạn tiếng Anh theo khuôn `changelog.d/wp-727.md`. Nói rõ phạm vi (đuôi lạ),
  thứ đã đo, và thứ chưa đo.
- **M5** → `RELEASE_MANIFEST.json`: sinh lại sau M2–M4.

## `nghiem_thu`

Mỗi tiêu chí kèm phép đo làm nó ĐỎ.

- **A1 — ca dương theo TỪNG vị trí (M1, M2).** Fixture: `a.log`, `b.patch`, `c.csv` (mỗi tệp một khoá giả ở dòng 2);
  `d.txt` (đối chứng, cùng khoá); `e.dat` = `b"\x00\x01"` + khoá (nhị phân, đuôi lạ); `f.log` lớn hơn `MAX_BYTES`
  một byte, khoá ở đầu tệp (quá trần, đuôi lạ). Khẳng định **bằng tập, không bằng số đếm** (L6c):
  `{đường_dẫn_tương_đối}` của `scan(root)` == `{"a.log","b.patch","c.csv","d.txt"}`, và mỗi hit mang đúng
  `:2: google_oauth_client_secret`. Thêm `main([..., root])` == 1, và `main` trên thư mục chỉ có `e.dat` + `f.log` == 0.
  - Màu trên nền: **ĐỎ** (master trả `{"d.txt"}`, đã đo trên bản sao 04:02Z).
  - **Đột biến M-a**: khôi phục `if f.suffix != "": return False` ⇒ ca ĐỎ.
  - **Đột biến M-b**: bỏ kiểm NUL cho nhánh đuôi lạ ⇒ `e.dat` thành hit ⇒ ca ĐỎ.
  - **Đột biến M-c**: bỏ trần `MAX_BYTES` cho nhánh đuôi lạ ⇒ `f.log` thành hit ⇒ ca ĐỎ.
  - Mỗi đột biến chạy trên **bản sao tạm** (clone nháp của head ứng viên), không ghi vào tệp thật. Ca phải chết vì
    **assertion của chính nó**: thông báo lỗi mang `TEST_ID` và tên tệp lệch, không phải `ImportError`/`AttributeError`.
    Ghi lệnh, rc và dòng FAIL cho từng đột biến.
- **A2 — không đổi hành vi nhánh cũ.** Cùng fixture: tệp không đuôi `credentials` (có khoá) vẫn là hit, tệp `.txt` vẫn
  là hit; `pkg_secret_scan.py` (tên trong `SELF_SKIP`, có khoá) vẫn không là hit.
  - Đột biến: xoá `SELF_SKIP` ⇒ ĐỎ; thêm `return False` cho tệp không đuôi ⇒ ĐỎ.
- **A3 — delta trên đầu vào thật = ∅.** Đo trên (i) gói dựng bằng `tl.py release-bundle` từ head ứng viên, giải nén,
  và (ii) toàn cây kho trừ `.git`. Chạy bộ quét bản master và bản head trên **cùng** thư mục; tiêu chí là tập hit head
  trừ tập hit master = ∅, so bằng `diff` tập dòng, không bằng rc. Ghi số tệp mỗi bản quét được và thời điểm đo.
  - ĐỎ khi: có hit mới. Đó là **phát hiện thật**: executor DỪNG, báo chủ kho trên #1030, KHÔNG xoá hay sửa dữ liệu.
- **A4 — parity sh/ps1 trên cùng đầu vào.** Thư mục fixture của A1 cộng gói của A3(i). Chạy đúng khối 3c của
  `scripts/deploy-package.sh` (dòng `SCAN="$($PY scripts/pkg_secret_scan.py "$PKG")"; SCAN_RC=$?`) và khối 3c của
  `scripts/deploy-package.ps1` (dòng `& $PY @PYARGS … pkg_secret_scan.py $pkg`; `$LASTEXITCODE`), trích nguyên văn từ
  tệp thay vì chép tay. So rc và tập dòng hit; hai bên phải bằng nhau.
  - Nền ps1, theo thứ tự ưu tiên: (1) máy Windows của chủ kho theo `ADR-0057`, nếu `list_devices` báo `Online` và
    khoá rảnh; (2) PowerShell 7 tải vào container theo tiền lệ r244, ghi rõ là "pwsh trên Linux, không phải Windows".
    Không đường nào đo được ⇒ A4 = `chưa đo được`, không phải đạt.
  - ĐỎ khi: rc hoặc tập hit lệch.
- **A5 — gate.** `python scripts/tl.py --selftest` ra `N/N`, hai số bằng nhau, và tăng đúng 1 so với base đo cùng
  phiên. `test-fragments-check --json` `status: current`. `release-verify RELEASE_MANIFEST.json --strict --json`
  `ok: true`. `golden-test --json` ok, KHÔNG `--write`. `ruff check --select F` trên hai tệp `.py` sửa tay: delta so
  base = 0. `core.abbrev=7`.
  - ĐỎ khi: một trong các số trên lệch. Chạy lại trên base sạch để tách lỗi đỏ sẵn khỏi lỗi do diff gây ra.
- **A6 — kích thước.** `git diff --numstat <base>..<head>` chỉ chạm đúng 5 tệp của write set, ≤ 450 dòng thêm theo
  ADR-0053 (ước lượng khi soạn: ~170).
  - ĐỎ khi: có tệp ngoài write set, hoặc vượt trần ⇒ DỪNG, xin `nang_tran` trước khi tiếp.
- **A7 — review chéo.** Codex qua `.claude/dev/launcher.py run`, đường dẫn CLI đã resolve, prompt truyền bằng tệp kèm
  `--expected-prompt-sha256`, neo đúng head. Lặp tới khi 0 P0–P3. Trần 10 lời gọi theo dòng khai ADR-0055. Đếm số
  lời gọi đã dùng TRƯỚC mỗi lời gọi.
  - ĐỎ khi: còn finding P0–P3, hoặc hết trần ⇒ Review Rescue Checkpoint, không gọi tiếp.

## `ngoai_pham_vi`

- **Trần `MAX_BYTES` cho tệp thuộc `TEXT_SUFFIXES`.** Hiện các tệp này không có trần. Thêm trần là đổi hành vi của
  đúng đường đang bắt được bí mật, nên cố ý không làm.
- Bảng `PATTERNS`, `SELF_SKIP`, `TEXT_SUFFIXES` giữ nguyên. Bộ quét thành "quét mọi tệp không nhị phân", nên
  `TEXT_SUFFIXES` chỉ còn tác dụng miễn kiểm NUL/trần; không xoá nó trong packet này.
- Bí mật mã hoá (base64, nén) hoặc nằm trong tệp nhị phân: ngoài khả năng của bộ quét theo regex.
- `deploy-package.sh`, `deploy-package.ps1`: không sửa. A4 chỉ đo, không vá.
- `VERSION`, `CHANGELOG.md`: không bump. Bộ quét là dev-side, không vào gói.

## `hinh_dang_ke_thua`

`khong_ap_dung`: không phải packet khắc phục của một packet nào. Có họ hàng doctrine: bài học CLAUDE.md "Quét
secrets: lọc theo PHẦN MỞ RỘNG là mù ĐÚNG CHỖ secrets nằm" (tệp không đuôi, đã vá trước đây). Packet này là lần thứ
**hai** cùng một hình dạng lỗi: quyết định quét bằng danh sách tên đuôi, không bằng thuộc tính đo được. Lần thứ ba
thì phải hỏi lại thiết kế (bỏ hẳn `TEXT_SUFFIXES`), không vá tiếp.

## `chua_do_duoc`

- Lúc soạn spec chưa đo ps1 trên Windows: phiên này không có `pwsh`, và không kiểm máy chủ kho.
- Câu "không có bí mật thật nào nằm trong các tệp đuôi lạ đã từng được đẩy lên Package trước đây" không đo được từ
  phiên này: các bản Package cũ không có ở đây, và manifest hiện tại không có đuôi lạ.
