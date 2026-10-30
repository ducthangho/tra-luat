# Đặc tả packet wp1030 r6 — `pkg_secret_scan`: tệp có đuôi lạ đi cùng phép lọc nhị phân như tệp không đuôi

Đặc tả đóng băng. Muốn đổi thì soạn `wp1030-pkg-secret-scan-duoi-la-r7.md`, không sửa đè.
**Thay cho r5** (`ops/specs/wp1030-pkg-secret-scan-duoi-la-r5.md`, sha256 `bcc14c2f…ed07`, blob `45f98f3a`; lease
`wp1030-r5-g1-claude` neo r5 và bị thay bởi lease r6 g1), r4 (sha256 `2ee97b57…11d6`; lease r4 g1 đã bị thay bởi
r5 g1), r3 (sha256 `fc8037e2…31df`), r2 (sha256 `536d0706…9327`) và
r1 (sha256 `832dec22…9158`). Lịch sử thay đổi:
- **r1 → r2:** M2 định nghĩa hành vi khi fragment chạy trong **gói đã giải nén**, và thêm A8 để đo nó. Nguồn: finding
  P2 của Codex connector trên PR #1031 (review comment 4420440394, neo `61f87f9`). Kiểm lại:
  `_release_should_include(scripts/pkg_secret_scan.py)` = `False`; bản giải nén của gói (04:13Z) không có tệp ấy,
  trong khi `scripts/tl_test_fragments_bundled.py` vẫn có trong gói.
- **r2 → r3:** đổi tuyến land sang thẳng `master` theo quyết định chủ kho (mục *mission* bên dưới). Base đo lại.
  A4 trỏ thêm `ADR-0058`, đã land trên master từ sau r2. Mọi mục tiêu và tiêu chí khác giữ nguyên chữ.
- **r3 → r4:** điều kiện (ii) của M2 đo CHÍNH SÁCH trên một tệp sentinel có thật, không đo trên tệp đang vắng; M-e
  dùng hàm thật thay cho stub. Nguồn: finding P2 của Codex connector trên PR #1031 (review comment 4420614904, neo
  `77801c3`). Kiểm lại: `_release_should_include` kết thúc bằng `return path.is_file()`
  (`scripts/tl_core/release.py:595`), nên với tệp vắng mặt hàm luôn trả `False` bất kể chính sách. Điều kiện (ii)
  của r2/r3 vì thế đúng rỗng nghĩa, và M-e của r2/r3 dùng một stub có hành vi khác hàm thật.
- **r4 → r5:** thêm `scripts/tl_selftest.py` vào write set (tệp thứ sáu), phạm vi hẹp ở M6. Nguồn: executor lease r4 g1
  DỪNG (#1030 issuecomment-6517603469) vì `changelog.d/wp-1030.md` (M4) vào gói, làm `file_count` 193 → 194. Hai ca
  ratchet ghim `len(paths) == 193` thì ĐỎ: `r291_docs_ngoai_goi` (`scripts/tl_selftest.py:22518`) và
  `r357_agents_ngoai_goi` (`:22573`). Phiên soạn spec đã kiểm lại hai dòng ấy trên master `757bde5`, và
  `RELEASE_MANIFEST.json` `file_count` = 193. Chủ kho chọn phương án 1, "thêm tl_selftest.py vào write set"
  (ghi lại ở #1030 issuecomment-6517889151). Phép thử clone nháp lúc soạn r1 chỉ chạy golden, release-verify,
  determinism và doc-claims, KHÔNG chạy selftest, nên không thấy hai ca này. M1–M5 và A1–A4, A7, A8 giữ nguyên chữ;
  A5 và A6 đổi số tệp; thêm A9.
- **r5 → r6:** A9 đo dòng bị XOÁ theo AST của base và dòng được THÊM theo AST của head. Nguồn: finding P2 của Codex
  connector trên PR #1036 (review comment 4421868868, neo `a44f492`). Phép đo của r5 chỉ dùng dải dòng phía head,
  nên hunk chỉ-xoá `@@ -a,b +c,0 @@` có dải head rỗng và lọt qua. Phiên soạn spec đã đo lại trên chính
  `scripts/tl_selftest.py` của master `757bde5` (`_c357_agents_ngoai_goi` = dòng 22532..22597; dòng 22598 là
  `_t110("r357_agents_ngoai_goi", …)`, nằm NGOÀI hàm). Xoá dòng 22598..22633: phép đo r5 XANH (lọt), phép đo r6 ĐỎ
  với 36 dòng xoá ngoài phạm vi. Sửa hợp lệ `193 → 194` ở hai chỗ: phép đo r6 XANH. Chèn một dòng ở biên trong
  hàm: phép đo r6 XANH, không chặn nhầm. Chỉ A9 đổi; mọi mục khác giữ nguyên chữ của r5.
Đặc tả KHÔNG cấp việc: cần Issue #1030 + lease còn hiệu lực (`docs/PROTOCOL_DA_PHIEN.md` §3.2, §4).
Chỗ nào đặc tả không nói thì executor DỪNG và hỏi trên #1030, không tự nới.

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

| trường | giá trị |
|---|---|
| `packet_id` · `packet_issue` | `wp1030` · #1030 · revision 6 · generation 1 |
| mission | #748 (chủ kho chỉ định 30-10-2026). #748 thực chất là một Packet Issue đã đóng (`completed` 20-10), không phải Mission §3.1, và được dùng làm ô chứa theo tiền lệ `WINDOWS-LOCAL-MAY-CHU-KHO` r1/r2 (land qua #1022, #1029). Không mở lại #748. **Ngoại lệ tuyến (§5):** PR của packet đi thẳng vào `master`, không qua `mission/748/integration` (nhánh này không tồn tại; đo `git ls-remote` 05:02Z 30-10). Chủ kho quyết định ngoại lệ trong phiên soạn spec 30-10-2026, theo khuyến nghị của phiên. Tiền lệ ngoại lệ: wp728 r2 (#755); quy tắc "ngoại lệ chỉ hợp lệ khi chủ kho quyết định và ghi trong spec/lease của chính packet" ở `ops/specs/wp727-nlm-refresh-va-goi-y-tl-gws-r2.md`. |
| `nguon_cap_viec` | chỉ thị chủ kho trong phiên soạn spec 30-10-2026 (đồng ý Q1–Q9; mở Issue #1030, mission #748). Lỗi do executor packet `WINDOWS-LOCAL-MAY-CHU-KHO` r1 phát hiện bằng đọc mã 29-10-2026; phiên soạn spec dựng phản chứng chạy được (mục *Hiện trạng*). |
| `review_class` | **sensitive**: ranh giới security/credential (§8). Reviewer `openai_codex` ⇒ `cross_approved`. |
| base | `origin/master` lúc cấp lease (đo khi soạn r3: `11204f55`, 05:02Z 30-10; từ `5f3855ea` tới đó không commit nào chạm write set, `scripts/tl_core/{release,test_fragments}.py` hay hai script deploy). |
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

## `write_set` (exact, 6 tệp)

1. `scripts/pkg_secret_scan.py`
2. `scripts/test_fragments/wp1030_pkg_secret_scan_duoi_la.py` (tệp mới)
3. `scripts/tl_test_fragments_bundled.py` (sinh lại bằng `tl_core.test_fragments.generate_bundled_module_bytes`,
   không sửa tay)
4. `changelog.d/wp-1030.md` (tệp mới)
5. `RELEASE_MANIFEST.json` (sinh lại bằng `tl.py release-manifest --out RELEASE_MANIFEST.json`, không sửa tay)
6. `scripts/tl_selftest.py` (r5; CHỈ trong hai khối `_c291_docs_ngoai_goi` và `_c357_agents_ngoai_goi`, xem M6)

## `muc_tieu`

- **M1** → `scripts/pkg_secret_scan.py`: trong `_is_scannable`, tệp có đuôi ∉ `TEXT_SUFFIXES` đi **cùng** nhánh với
  tệp không đuôi: quét khi `st_size ≤ MAX_BYTES` và không có `b"\x00"` trong 8192 byte đầu. Lỗi `OSError` vẫn trả
  `False`. Sửa chú thích tại chỗ theo idiom "vX.Y.Z (bằng chứng) — fix": mặc định của bộ quét là QUÉT, chỉ bỏ theo
  thuộc tính ĐO được (nhị phân, quá trần), không bỏ theo tên đuôi.
- **M2** → `scripts/test_fragments/wp1030_pkg_secret_scan_duoi_la.py`: fragment `TEST_ID = "wp1030_pkg_secret_scan_duoi_la"`,
  nạp `scripts/pkg_secret_scan.py` theo đường dẫn tương đối với `tl_module.__file__`, dựng fixture trong
  `tempfile.TemporaryDirectory()`. Khoá giả phải dựng lúc chạy từ các mảnh (không viết nguyên chuỗi khớp mẫu trong
  mã nguồn), để bản thân fragment không thành hit của bộ quét.
  **Topo phát hành (r2).** Fragment được bundle vào `scripts/tl_test_fragments_bundled.py`, mà tệp này nằm TRONG gói,
  còn `pkg_secret_scan.py` bị loại khỏi gói (`_RELEASE_EXCLUDE_NAMES_ANYWHERE`). Fragment chỉ được trả `True` mà không
  đo khi **cả ba** điều sau cùng đúng: (i) `scripts/pkg_secret_scan.py` không tồn tại; (ii) chính sách phát hành
  loại tệp ấy THEO THIẾT KẾ, đo trên một **sentinel có thật**: trong một `tempfile.TemporaryDirectory()` riêng, tạo
  tệp rỗng `<tạm>/scripts/pkg_secret_scan.py`, rồi `tl_module._release_should_include(<tạm>/scripts/pkg_secret_scan.py,
  <tạm>)` phải trả `False`. KHÔNG được gọi hàm ấy trên đường dẫn đang vắng, vì hàm kết thúc bằng
  `return path.is_file()` nên tệp vắng luôn ra `False` bất kể chính sách; (iii) gốc không có `.git`, tức cây rõ ràng là bản sao rời (bài học CLAUDE.md "Ca có MẶT khác ca có ĐO").
  Thiếu bộ quét trong một checkout có `.git` ⇒ fragment trả `False` (ĐỎ), không bao giờ bỏ qua. Mọi lỗi khi kiểm ba
  điều kiện (ném ngoại lệ, `tl_module` thiếu `_release_should_include`) ⇒ `False`, fail-closed. Khi tha, fragment in
  đúng một dòng `[wp1030_pkg_secret_scan_duoi_la] BỎ QUA (<lý do>)`, theo tiền lệ `wp726_script_nlm_canary`.
- **M3** → `scripts/tl_test_fragments_bundled.py`: sinh lại cho khớp, `test-fragments-check` = `current`.
- **M4** → `changelog.d/wp-1030.md`: một đoạn tiếng Anh theo khuôn `changelog.d/wp-727.md`. Nói rõ phạm vi (đuôi lạ),
  thứ đã đo, và thứ chưa đo.
- **M5** → `RELEASE_MANIFEST.json`: sinh lại sau M2–M4.
- **M6** (r5) → `scripts/tl_selftest.py`: trong `_c291_docs_ngoai_goi` và `_c357_agents_ngoai_goi`, đổi ratchet
  `len(paths) == 193` thành `== 194`. Mỗi khối thêm một dòng "KÊ KHAI SLOT (packet #1030)" theo khuôn #868/#886/#1009,
  và được sửa con số đã cũ trong chú thích ratchet của chính khối ấy. Không đổi gì khác trong tệp.

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
    khoá rảnh, theo đủ `ADR-0057` và `ADR-0058` (khoá theo máy, hạn khoá 2 giờ); (2) PowerShell 7 tải vào container theo tiền lệ r244, ghi rõ là "pwsh trên Linux, không phải Windows".
    Không đường nào đo được ⇒ A4 = `chưa đo được`, không phải đạt.
  - ĐỎ khi: rc hoặc tập hit lệch.
- **A5 — gate.** `python scripts/tl.py --selftest` ra `N/N`, hai số bằng nhau, và tăng đúng 1 so với base đo cùng
  phiên. `test-fragments-check --json` `status: current`. `release-verify RELEASE_MANIFEST.json --strict --json`
  `ok: true`. `golden-test --json` ok, KHÔNG `--write`. `ruff check --select F` trên hai tệp `.py` sửa tay: delta so
  base = 0. `ruff check --select F` trên `scripts/tl_selftest.py` (r5): delta so base = 0, so theo tập
  `(code, message)` chứ không theo tổng. `core.abbrev=7`.
  - ĐỎ khi: một trong các số trên lệch. Chạy lại trên base sạch để tách lỗi đỏ sẵn khỏi lỗi do diff gây ra.
- **A6 — kích thước.** `git diff --numstat <base>..<head>` chỉ chạm đúng 6 tệp của write set, ≤ 450 dòng thêm theo
  ADR-0053 (ước lượng khi soạn r5: ~176). ADR-0053 trần 6 tệp, nên write set r5 chạm đúng trần.
  - ĐỎ khi: có tệp ngoài write set, hoặc vượt trần ⇒ DỪNG, xin `nang_tran` trước khi tiếp.
- **A7 — review chéo.** Codex qua `.claude/dev/launcher.py run`, đường dẫn CLI đã resolve, prompt truyền bằng tệp kèm
  `--expected-prompt-sha256`, neo đúng head. Lặp tới khi 0 P0–P3. Trần 10 lời gọi theo dòng khai ADR-0055. Đếm số
  lời gọi đã dùng TRƯỚC mỗi lời gọi.
  - ĐỎ khi: còn finding P0–P3, hoặc hết trần ⇒ Review Rescue Checkpoint, không gọi tiếp.
- **A8 — selftest trong gói đã giải nén (r2).** Dựng gói bằng `tl.py release-bundle` từ head ứng viên, giải nén vào
  thư mục tạm ngoài checkout (không có `.git`), chạy `python scripts/tl.py --selftest` ở đó. Cùng phiên, chạy cùng lệnh
  trên gói dựng từ base. Tiêu chí, so bằng TẬP tên ca chứ không bằng rc: (a) tập ca `[FAIL]` của head == tập ca
  `[FAIL]` của base; (b) `[OK] wp1030_pkg_secret_scan_duoi_la` có mặt; (c) dòng `[wp1030_pkg_secret_scan_duoi_la] BỎ QUA`
  có mặt đúng một lần; (d) tổng của head = tổng của base + 1. Ghi lệnh, rc, dòng tổng, hai tập ca đỏ.
  Nền đo khi soạn r2 (04:29–04:32Z 30-10, gói từ `5f3855ea`, `python3`, Linux): **1733/1738**, rc=1; 5 ca `[FAIL]`
  đỏ sẵn: `r291_docs_ngoai_goi` · `r330_deploy_msg_khong_chay_lenh` · `r378_l7_duong_dan_an_co_that_im` ·
  `r378_l7_duong_dan_an_van_kiem_dong` · `r264_doc_claims_phu_docs`. Không phải nợ của packet này; đo lại trên base
  lúc thi công, đừng chép con số.
  - Đột biến **M-d**: bỏ điều kiện (iii) (`.git`). Phép đo: trong một clone nháp của head (có `.git`), xoá
    `scripts/pkg_secret_scan.py` rồi gọi `run(tl)` của fragment. Bản đúng trả `False` (ĐỎ); bản đột biến trả `True` ⇒
    phép đo đổi màu, tức điều kiện (iii) có răng.
  - Đột biến **M-e** (r4): bỏ điều kiện (ii), hoặc thay nó bằng phép gọi `_release_should_include` trên đường dẫn
    đang vắng (dạng của r2/r3). Phép đo dùng **hàm thật**, không dùng stub: trong một bản sao rời (không `.git`),
    xoá `scripts/pkg_secret_scan.py`, bỏ `"pkg_secret_scan.py"` khỏi ĐÚNG đối tượng
    `tl_core.release._RELEASE_EXCLUDE_NAMES_ANYWHERE` trong bộ nhớ của tiến trình đo (khôi phục trong `finally`), tức
    chính sách đổi sang GIỮ bộ quét trong gói, rồi gọi `run()` của fragment. Đo khi soạn r4 (05:08Z 30-10, `11204f55`):
    `tl._release_should_include.__globals__` KHÔNG chứa tên ấy và module `tl` cũng không, nhưng bỏ tên khỏi tập
    trong `tl_core.release` thì sentinel đổi từ `False` sang `True`, khôi phục lại thì về `False`. Chỗ vá nào khác
    chưa được đo; muốn dùng thì phải đo lại cặp `False`→`True` trước, kẻo phép đo im lặng mất răng. Bản đúng: sentinel ra `True` ⇒ không tha ⇒ trả `False` (ĐỎ). Cả hai dạng đột biến đều trả `True`.
    Đối chứng cùng phép đo khi KHÔNG vá chính sách: bản đúng tha (in dòng `BỎ QUA`, trả `True`).
  - Đột biến **M-f**: bỏ điều kiện (i) (tệp tồn tại thì vẫn tha). Phép đo: chạy fragment trong gói đã giải nén nhưng
    chép `scripts/pkg_secret_scan.py` bản master (chưa vá) vào; bản đúng phải ĐO và trả `False` (vì A1 đỏ trên bản
    chưa vá); bản đột biến trả `True`.
  - ĐỎ khi: (a)–(d) có vế sai. Ca đỏ sẵn trên base ghi `đỏ sẵn, delta = 0`; không đọc rc trần làm kết luận.

- **A9 — phạm vi M6 (r6).** Lấy `git diff -U0 <base>..<head> -- scripts/tl_selftest.py`, đọc từng hunk
  `@@ -a,b +c,d @@` (thiếu `,n` nghĩa là n = 1). Có hai phía, đo riêng từng phía:
  - mọi dòng bị **xoá** `a .. a+b-1` phải nằm trong dải `FunctionDef.lineno .. end_lineno` của `_c291_docs_ngoai_goi`
    hoặc `_c357_agents_ngoai_goi`, tính theo `ast.parse` của tệp ở **base**;
  - mọi dòng được **thêm** `c .. c+d-1` phải nằm trong dải của hai hàm ấy, tính theo `ast.parse` của tệp ở **head**.
  Phía nào có độ dài 0 thì phía đó không có dòng nào để kiểm. KHÔNG coi dòng neo của một dải rỗng là dòng được sửa:
  làm vậy vừa để lọt xoá ngoài phạm vi, vừa chặn nhầm chèn hợp lệ ở biên. Không đo bằng grep chuỗi. Thiếu một trong
  hai hàm, hoặc một tên hàm xuất hiện hơn một lần ở base hay head, thì ra `KHÔNG ĐO ĐƯỢC`, và đó là ĐỎ. Selftest trên
  head có `[OK] r291_docs_ngoai_goi` và `[OK] r357_agents_ngoai_goi`.
  - ĐỎ khi: có dòng xoá hoặc dòng thêm nằm ngoài hai hàm, phép đo `KHÔNG ĐO ĐƯỢC`, hoặc một trong hai ca không `[OK]`.
  - Đột biến **M-i** (r6): xoá mã ngay SAU một hàm được phép, ví dụ dòng đăng ký
    `_t110("r357_agents_ngoai_goi", …)` cùng hàm kế tiếp ⇒ A9 phải ĐỎ. Đối chứng bắt buộc: phép đo kiểu r5 (chỉ
    phía head) trên cùng diff phải ra XANH, chứng tỏ M-i nhắm đúng lỗ đã vá.
  - Đối chứng biên: chèn một dòng bên trong hàm, ngay trước `return` cuối ⇒ A9 phải XANH.
  - Đột biến **M-g**: trả một ratchet về `== 193` ⇒ ca tương ứng ĐỎ trong selftest dev.
  - Đột biến **M-h**: bỏ M4 (xoá `changelog.d/wp-1030.md`, sinh lại manifest) mà giữ `== 194` ⇒ hai ca ĐỎ. Đột biến
    này cho thấy ratchet đếm thật, không phải hằng số.

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
- Executor đo trên base `09e0594` cùng phiên (trước 07:44Z, #1030 issuecomment-6517603469): selftest dev 1758/1758, selftest
  gói 1753/1758; trước khi sửa ratchet, head cho 1757/1759 (dev) và 1753/1759 (gói). Phiên soạn r5 KHÔNG đo lại các số
  này; executor phải đo lại trên base và head cuối.
- Năm ca đỏ sẵn trong selftest của gói (A8) chưa có nợ có tên trong phiên này; phiên soạn spec không truy nguyên nhân.
- Câu "không có bí mật thật nào nằm trong các tệp đuôi lạ đã từng được đẩy lên Package trước đây" không đo được từ
  phiên này: các bản Package cũ không có ở đây, và manifest hiện tại không có đuôi lạ.
