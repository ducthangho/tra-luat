# Đặc tả packet — `CLOUD-SETUP-P3B-NLM-401` (revision 10)

- `packet_id`: **CLOUD-SETUP-P3B-NLM-401** · `packet_issue`: **#1099** (Issue cha #1008; tách từ #1089 theo vòng 1 Q1 của đặc tả
  P3) · `revision`: **10** · trạng thái: r1–r3 land qua PR #1101 (merge `47ee1b20`); r4–r9 ở PR #1188 (merge `1813bfd`); r4–r8 đều bị review độc lập
  Codex request_changes — r8 (`079868c4…`): `8191331a` (lời gọi 6/8 của #1099, head `8014baf0`, 1 P2 + 1 P3, hai lớp MỚI, không
  thuộc lớp Markdown đã hạ ở r8). Chưa revision nào được cấp lease hay thi hành. r9 soạn 04-11-2026 bởi phiên
  `session_015GtxrcPNaayykBErdfcNUB` (mục `errata_r9` cuối tệp). Giữ nguyên `errata_r2`…`errata_r8`. Băm `sha256` của r9 ghi trên
  Issue #1099 và PR #1188, không ghi trong tệp. r9 được cấp lease `wp1099-cloud-setup-p3b-r9-g1-claude` và thi hành ở PR #1197.
  **r10** soạn 05-11-2026 bởi cùng phiên (mục `errata_r10` cuối tệp): đổi số ADR (chủ kho, #1099 issuecomment-6650250003) và
  khai năng lực nền cho hai đột biến (K6 Windows đỏ trên head `6f35ad14`). Băm `sha256` của r10 ghi trên Issue #1099, không ghi
  trong tệp. Lease phải neo **r10**. Sửa nội dung từ đây ⇒ revision 11.
- `nguon_cap_viec`: chỉ thị chủ kho "soạn tiếp spec P3b NLM 401" (01-11 ~01:57Z) trong phiên nói trên; phạm vi gốc ở dòng P3 của
  bảng chuỗi #1008 ("NLM tải lại jar khi gặp 401"). Chốt trong phiên soạn: vòng 1 Q1–Q8 và vòng 2 Q9–Q17, chủ kho trả lời cả hai
  vòng "Đồng ý tất cả khuyến nghị". Không có dòng kế hoạch nào trong `ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md`.
- `review_class`: **sensitive** — ghi đè jar cookie NLM (`~/.notebooklm-mcp-cli`) và đổi doctrine (`RASOAT_HOSO_LOOP.md` §4b,
  ADR mới, bảng §20 của protocol) (protocol §8).
- Base dự kiến: `origin/master` lúc cấp lease (đo lại 15:2xZ 04-11: `1f0941e9`, merge PR #1186). Mọi phép đo kích thước/delta đo so
  merge-base (`git diff origin/master...HEAD`).
- **Điều kiện cấp lease (vòng 2 Q15, đo lại cho r2):** bất biến là *không lease nào còn hiệu lực giữ một đường dẫn của
  `write_set`*. Đo 01:0xZ 02-11 bằng `ops/lease_publish.py ai-dang-giu` sau khi fetch đủ ref: `RELEASE_MANIFEST.json` và
  `scripts/tl_test_fragments_bundled.py` ⇒ `NGƯỜI_GIỮ 1: wp1134-r2-g1-claude` (`CHANGELOG-D-NGOAI-GOI`, hạn
  `2026-11-02T23:53:00Z`); `docs/PROTOCOL_DA_PHIEN.md` ⇒ `NGƯỜI_GIỮ 1: wp825-r1-g1-claude` (hạn `2026-11-03T00:46:00Z`); sáu
  đường dẫn còn lại ⇒ `NGƯỜI_GIỮ 0`. Lease P3 `wp1089-…-r2-g1` nay `ĐÃ_BỊ_THAY_THẾ`. Chỉ cấp khi cả 9 đường dẫn ra
  `NGƯỜI_GIỮ 0`; đo lại ngay trước khi cấp (L5). **Thêm cho r2:** đo lại trên MỌI ref `refs/remotes/origin/*` rằng không tệp
  nào khác mang tiền tố `docs/adr/0064-` (r10 đo ~05:10Z 05-11 sau khi fetch đủ 865/865 nhánh, lệch `ls-remote` 0: 0 tệp
  `docs/adr/006[4-9]-*`, 0 chỗ nhắc `ADR-0064` trong `ops/specs`/`docs` của mọi ref); bị chiếm ⇒ DỪNG, ra revision mới đổi số —
  không tự chọn số khác.
- `nang_tran`: chủ kho đồng ý vòng 2 Q13. Trần packet này: **≤ 9 tệp / ≤ 550 dòng thêm** theo `git diff --numstat` (thay
  `ADR-0053` CHỈ cho packet này). Vượt ⇒ bỏ bớt ca phụ, KHÔNG xin nâng thêm.

tran_loi_goi_codex: ADR-0052@8ab100793df9831505f495543a74044b91c2c9ab
tran_kich_thuoc_sensitive: nang_tran vòng 2 Q13 (≤ 9 tệp / ≤ 550 dòng thêm; thay ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab)

(OID là commit LAND của `ADR-0052` và `ADR-0053` — merge PR #791; cùng giá trị các đặc tả P1 r4, P2a, P2b, P3.)

## Vấn đề (một đoạn)

Phiên Claude Code web nạp cookie NLM một lần lúc `bootstrap`, từ `nlm_auth` trong `tl_secrets.enc` (log hook 02:21Z 01-11:
*"cookie ~1 ngày tuổi"*). Khi jar chết giữa phiên, mọi lệnh `nlm` qua `scripts/nlm_cli.py` chỉ trả `auth_hint`
(`nlm_cli.py:143`, `:162`, `:229`) rồi người gọi rơi về MCP hoặc chế độ không-NLM. Trong khi đó laptop chạy WP710 mỗi 30 phút
và từ wp726 chỉ stage `nlm_cred.enc` **sau canary LIVE dương**, nên nguồn ấy thường tươi hơn bản trong `tl_secrets.enc`. Kho đã
từng BÁC việc tự nạp lại (chú thích r208c trong `_nlm_auth_load`, `scripts/tl_gws.py`; điều cấm ở
`references/RASOAT_HOSO_LOOP.md:118–119` và `references/QUY_TRINH_RA_SOAT_3_TANG.md:49`) vì bundle có thể **cũ hơn** hoặc **cũng
chết**, khiến vòng nạp-thử-lại quay vô ích. Packet này đảo quyết định ấy **có điều kiện, chỉ ở phiên cloud**: chỉ nạp khi canary
LIVE xác nhận jar hiện tại CHẾT, chỉ từ `nlm_cred.enc` qua lệnh có sẵn `tl nlm-auth-load` (giữ chốt chống hạ cấp), tối đa một lần
mỗi tiến trình, cố gắng (best effort, không bảo đảm khi hai tiến trình cạnh tranh) cách nhau ít nhất 10 phút giữa các tiến trình, và chỉ tự chạy lại lệnh ĐỌC.

## `write_set`

Đúng 9 đường dẫn (vòng 2 Q9). Không ký tự đại diện.

1. `scripts/nlm_cli.py` — cơ chế tự nạp lại trong `_run`
2. `scripts/test_fragments/wp1099_nlm_nap_lai.py` — **mới**: ca + đột biến
3. `scripts/tl_test_fragments_bundled.py` — sinh lại từ `scripts/test_fragments/` (CI PR chạy `bundled-fragment check`)
4. `references/RASOAT_HOSO_LOOP.md` — một câu ngoại lệ ở §4b
5. `references/QUY_TRINH_RA_SOAT_3_TANG.md` — cùng câu ngoại lệ ở dòng "Sửa xác thực" (dòng 49, đo 02:2xZ 01-11)
6. `docs/adr/0064-nlm-tu-nap-lai-co-dieu-kien-phien-cloud.md` — **mới**
7. `docs/PROTOCOL_DA_PHIEN.md` — đúng 1 dòng `ADR-0064` trong bảng §20 (cổng `adr-song`)
8. `changelog.d/wp-1099.md` — **mới**
9. `RELEASE_MANIFEST.json` — tái sinh vì (1), (3), (4), (5) nằm trong gói (manifest đo 15:2xZ 04-11 trên `1f0941e9`: 184 tệp; đo lại lúc cấp lease rằng cả bốn còn trong manifest)

Không tệp nào khác. Cần sửa một tệp ngoài danh sách ⇒ DỪNG, hỏi chủ kho (L2). Cụ thể **KHÔNG** sửa `scripts/tl_selftest.py`
(ca `r213_auth_carve_out_khong_pha_thu_tu`, `tl_selftest.py:24829` trên `1f0941e9`, phải xanh NGUYÊN TRẠNG), `scripts/tl_gws.py`,
`scripts/tl_core/**` (kể cả `_AUTH_FIX_FALLBACK` khai báo ở `nlm_ops.py:297`), `SKILL.md`, golden, CHANGELOG, VERSION. Hằng
`AUTH_FIX_HINT`, `AUTH_FIX_HINT_SHORT`, `_AUTH_FIX_ORDER`, `_AUTH_FIX_RASOAT_CARVE` trong `nlm_cli.py` giữ nguyên byte.

## `ngoai_pham_vi`

- **Cowork và laptop/Windows** (vòng 1 Q2): cơ chế chỉ bật khi `CLAUDE_CODE_REMOTE == "true"`. Laptop là máy giữ cookie (WP710);
  nạp từ `nlm_cred.enc` ở đó là nạp lại chính bản của nó. Cowork để packet sau, khi M1 đã chứng minh đường này.
- **Tự chạy lại lệnh GHI** (vòng 1 Q3): `source add/delete/sync/rename`, `notebook create`, `chat configure`, và mọi argv ngoài
  danh sách cho phép.
- **Nạp từ `tl_secrets.enc` / `nlm-auth-pull` / `--force`** (vòng 1 Q5).
- **Đổi điều cấm dành cho AGENT** (vòng 2 Q10): agent vẫn KHÔNG được tự gõ `nlm-auth-load` trong lượt rà; câu trừ
  `_AUTH_FIX_RASOAT_CARVE` giữ nguyên.
- **Siết bộ nhận diện chuỗi auth** ở ba chỗ hiện có: giữ nguyên làm tín hiệu ỨNG VIÊN; quyết định nằm ở canary (vòng 1 Q4).
- **Import `tl_gws` vào TIẾN TRÌNH của `nlm_cli`** (vòng 1 Q5, vòng 2 Q11): `_nlm_auth_alive` (`tl_gws.py:308`) tự gọi
  `nlm_cli` ⇒ đệ quy. r3 chỉ gọi nó trong một tiến trình CON có `TL_NLM_NAP_LAI_TAT=1` (mục tiêu 1, bước Xác nhận).
- **Sửa `_nlm_preflight_report`/`nlm-auth-status`** (`scripts/tl_core/nlm_ops.py:1424–1430`, gộp mọi lỗi probe thành
  `alive: False`): r3 không dùng lệnh ấy làm canary nữa nên không cần sửa; nếu muốn lệnh ấy phân loại đúng thì là packet khác.
- **Ghi ngược Codex** (P3 #1089), **bump hợp đồng webapp** (P3c), **`doctor` gọi `agy`**: packet khác.

## `muc_tieu`

Mỗi dòng chiếu vào đúng một đường dẫn ở `write_set` (L2).

1. → `scripts/nlm_cli.py`: cơ chế **tự nạp lại** đặt trong `_run` (mọi lệnh `nlm` đi qua đây).
   - **Cổng bật** (Q2, Q11): chỉ khi `CLAUDE_CODE_REMOTE == "true"` VÀ `TL_NLM_NAP_LAI_TAT` không phải `"1"`. Khác ⇒ hành vi
     `_run` giữ nguyên từng byte đầu ra, 0 tiến trình con thêm, không in gì thêm.
   - **Ứng viên** (Q4): rc ≠ 0 và `(err + out).lower()` chứa một trong `auth`, `401`, `login`, `unauthor`, `credential` (đúng
     bộ chuỗi đang dùng ở `nlm_cli.py:143`). rc 124 (quá hạn) và rc 127 (không có `nlm`) KHÔNG phải ứng viên.
   - **Giới hạn** (Q6, Q16), kiểm TRƯỚC canary: mỗi tiến trình Python tối đa **1** lần nạp; tệp dấu
     `~/.notebooklm-mcp-cli/.tra-luat-nap-lai.json` có `ts` trong vòng **600 s** trước `now` ⇒ `BỎ QUA — đã nạp lúc <ts>`.
     `ts > now + 60` hoặc tệp hỏng/không phải object ⇒ coi như không có dấu.
   - **Xác nhận** (Q4; r3 đổi lệnh của Q11 — xem `errata_r3`): tiến trình con `[sys.executable, "-c", <CANARY>]`, `cwd` = thư
     mục cha của thư mục chứa `nlm_cli.py`, môi trường kế thừa cộng `TL_NLM_NAP_LAI_TAT=1`, stdin `DEVNULL`, timeout **120 s**
     (`_nlm_auth_alive` thử tối đa 3 lần, mỗi lần 30 s, cộng 4,5 s chờ). `<CANARY>` là hằng chuỗi trong `nlm_cli.py`, cùng thân với
     hàm `_canary_song` của `scripts/nlm-auto-refresh.sh` (đo 01:5xZ 02-11 trên `c7174bfe`): chèn thư mục chứa `nlm_cli.py` vào
     `sys.path`, `import tl`, `tg = tl._imp("tl_gws")`, `tg.bind(tl)`,
     `alive, _ = tg._nlm_auth_alive(tg._nlm_canary_notebook(None), require_notebook_body=True)`; ngoại lệ ⇒ `alive = None`;
     thoát **0** khi `alive is True`, **3** khi `alive is False`, **2** khi khác. Chỉ mã **3** mới đi tiếp. Mã 0 ⇒ `BỎ QUA — canary
     sống, lỗi không do auth`; mã 2, mã khác, quá hạn, `OSError` ⇒ `KHÔNG ĐO ĐƯỢC — canary <lý do>`. Hai nhánh này không nạp.
     Hành vi THẬT của `_nlm_auth_alive` (`tl_gws.py:308–363` trên `1f0941e9`; r4 sửa lời khai sai của r3 — `errata_r4` E7): thử tối
     đa 3 lần, lần thử lỗi có `auth_hint`/`clientauthentication`/chuỗi mạng thì thử lại; kết luận chỉ dựa trên kết quả của lần thử
     CUỐI — có `auth_hint` ⇒ `False`, chuỗi mạng/tạm thời ⇒ `None`, lỗi khác (vd quyền notebook không mang chuỗi auth) ⇒ `None`.
     Hệ quả đã chấp nhận (chủ kho chọn 04-11-2026, `errata_r4`): chuỗi trộn có lần CUỐI là auth (vd `mạng → mạng → auth`) ra
     `False` ⇒ có thể nạp lại một lần thừa. Trần BẢO ĐẢM chỉ là **1 lần nạp mỗi tiến trình**; cửa sổ 600 s giữa các tiến trình là
     best effort (tệp dấu không có khoá — xem `chua_do_duoc`, "Hai tiến trình cùng nạp"). Mỗi lần nạp vẫn chỉ từ `nlm_cred.enc`,
     vẫn qua chốt chống hạ cấp và không `--force`. Không đổi `_nlm_auth_alive`, không dựng bộ phân loại thứ hai.
   - **Nạp** (Q5, Q16): ghi tệp dấu `{ "ts": <epoch giây>, "ket_qua": "dang_nap" }` (0600, nguyên tử) **trước**, rồi tiến trình
     con `[sys.executable, <thư mục chứa nlm_cli.py>/tl.py, "nlm-auth-load"]` (không `--force`), cùng môi trường như trên,
     timeout **60 s**. rc ≠ 0 và đầu ra chứa
     `TỪ CHỐI HẠ CẤP` ⇒ `TỪ CHỐI HẠ CẤP`; rc ≠ 0 khác ⇒ `KHÔNG ĐO ĐƯỢC — nlm-auth-load rc=<N>`. Không chuyển tiếp đầu ra của con.
   - **Kiểm lại**: rc 0 ⇒ chạy canary lần hai như trên. Mã 0 ⇒ nạp thành công; mã 3 ⇒ `BUNDLE CŨNG CHẾT — laptop WP710 cần
     đăng nhập lại`; khác ⇒ `KHÔNG ĐO ĐƯỢC — canary sau nạp <lý do>`. Cập nhật `ket_qua` trong dấu.
   - **Thử lại** (Q3): chỉ khi nạp thành công VÀ `args[:2]` thuộc danh sách CHO PHÉP
     `(source,list)`, `(source,get)`, `(source,content)`, `(notebook,get)`, `(notebook,list)`, `(notebook,query)` ⇒ chạy lại
     ĐÚNG MỘT lần cùng `args`/`timeout`, trả kết quả lần chạy lại; trạng thái `ĐÃ NẠP, THỬ LẠI ĐẠT` khi rc 0, `ĐÃ NẠP, THỬ LẠI
     VẪN LỖI rc=<N>` khi khác. argv ngoài danh sách ⇒ `ĐÃ NẠP, KHÔNG THỬ LẠI (lệnh ghi)` và trả kết quả lần ĐẦU.
   - **Báo** (Q7): đơn vị đếm là MỘT LỜI GỌI `_run` (r6, E16): mỗi lời gọi in tối đa một dòng; lời gọi nào chạy qua bước
     "Giới hạn" in **đúng một** dòng ra **stderr của tiến trình**, ghi qua đối tượng `sys.stderr` của Python (không ghi thẳng fd 2,
     để phép đo thay `sys.stderr` theo từng lời gọi bắt được) (không vào chuỗi
     `err` trả về, không vào stdout) dạng `nlm_nap_lai: <TRẠNG THÁI> — <chi tiết>`; chi tiết không chứa đường dẫn cookie, giá
     trị cookie hay đầu ra của con. Kết quả `_run` giữ kiểu `tuple[int, str, str]`; trạng thái cuối được lưu vào biến mô-đun
     `NAP_LAI_GAN_NHAT` (dict `{trang_thai, ts}` hoặc `None`). Các hàm dict sẵn có (`_run_json`, `_auth_fail`, `source_list`…)
     thêm khoá `nap_lai` = giá trị ấy khi khác `None` (Q7); mọi khoá cũ giữ nguyên.
2. → `scripts/test_fragments/wp1099_nlm_nap_lai.py`: các ca ở `nghiem_thu` A/D + bảng đột biến (Q12), theo khuôn fragment
   sẵn có (`TEST_ID = "wp1099_nlm_nap_lai"`, hàm `run(tl_module)`). Ca chép `nlm_cli.py` THẬT vào cây tạm, đặt cạnh nó `tl.py`
   **giả** — vừa là MÔ-ĐUN cho canary (`_imp`, `bind`, `_nlm_canary_notebook`, `_nlm_auth_alive` trả `True`/`False`/`None` theo
   trạng thái), vừa là CLI cho `nlm-auth-load`, đúng khuôn `tl.py` giả của fragment `wp726_script_nlm_canary` — và `nlm` **giả**
   trên `TL_NLM_BIN`; ba đồ giả dùng chung một tệp trạng
   thái `{jar: song|chet, bundle: song|chet|cu_hon}` — `nlm-auth-load` giả chỉ đổi `jar` thành `song` khi `bundle == "song"`, in
   `TỪ CHỐI HẠ CẤP` và rc 2 khi `cu_hon` — và ghi nhật ký mọi lời gọi (argv + giá trị `TL_NLM_NAP_LAI_TAT`). Đột biến chạy
   trên bản sao tạm của `nlm_cli.py`, không ghi tệp thật.
3. → `scripts/tl_test_fragments_bundled.py`: sinh lại bằng `tl_core.test_fragments.generate_bundled_module_bytes`.
4. → `references/RASOAT_HOSO_LOOP.md`: sau câu "CẤM tự `nlm-auth-load` …" ở §4b, thêm đúng một câu: *"Ngoại lệ duy nhất:
   cơ chế tự nạp có điều kiện bên trong `nlm_cli` ở phiên cloud (`ADR-0064`) — agent vẫn không tự gõ lệnh nạp."* Mọi chữ cũ giữ.
5. → `references/QUY_TRINH_RA_SOAT_3_TANG.md`: cùng câu ấy, nguyên văn, ở cuối gạch đầu dòng "Sửa xác thực". Mọi chữ cũ giữ.
6. → `docs/adr/0064-nlm-tu-nap-lai-co-dieu-kien-phien-cloud.md`: `Trạng thái: Accepted`; nêu nó **thay r208c ở đúng điểm "tự nạp
   khi hết hạn", chỉ cho phiên cloud**; dòng trạng thái đúng khuôn mà cổng `adr-song` đọc (regex `_ADR_TRANG_THAI`,
   `.claude/dev/packet_loop.py:1887` trên `1f0941e9`; khuôn của `docs/adr/0060-*.md` và `0062-*.md` dòng 3), nguyên văn
   `- **Trạng thái:** Accepted` (r6, E17); tiền đề đã đổi (WP710 30 phút + canary trước stage của wp726; chốt chống hạ cấp còn);
   năm điều kiện (canary chết · chỉ `nlm_cred.enc` không `--force` · 1 lần/tiến trình (bảo đảm) + 600 s giữa tiến trình (best effort) · chỉ thử lại lệnh đọc · nạp xong
   vẫn chết ⇒ §4b); mục Cưỡng chế trỏ fragment `wp1099_nlm_nap_lai`. Mục "Quyết định" của ADR chứa NGUYÊN VĂN, mỗi câu một gạch
   đầu dòng riêng, đúng sáu câu sau (r5, E11; từ r8 nội dung này do reviewer PR code xác nhận ở R1, máy không đo — E23):
   - `Chỉ áp dụng khi biến môi trường CLAUDE_CODE_REMOTE có giá trị true.`
   - `Chỉ nạp khi canary _nlm_auth_alive trong tiến trình con trả mã 3 (jar đã chết).`
   - `Chỉ nạp từ nlm_cred.enc bằng tl.py nlm-auth-load, không dùng cờ --force.`
   - `Mỗi tiến trình nạp tối đa 1 lần; cửa sổ 600 giây giữa các tiến trình là best effort, không bảo đảm khi cạnh tranh.`
   - `Chỉ tự chạy lại các lệnh đọc trong danh sách cho phép.`
   - `Nạp xong mà vẫn lỗi xác thực thì dừng và làm theo §4b của RASOAT_HOSO_LOOP.md.`
7. → `docs/PROTOCOL_DA_PHIEN.md`: đúng 1 dòng mới trong bảng §20 cho `ADR-0064`, cột cổng = `wp1099_nlm_nap_lai (selftest
   fragment)`.
8. → `changelog.d/wp-1099.md`: mục tóm tắt theo khuôn các tệp `changelog.d/wp-*.md` sẵn có — một đoạn văn tiếng Anh bắt đầu
   bằng `WP1099 (CLOUD-SETUP-P3B-NLM-401): ` (khuôn của `changelog.d/wp-1038.md`), nêu hành vi của packet (nghiệm thu H1).
9. → `RELEASE_MANIFEST.json`: tái sinh sau mục 1, 3, 4, 5 (CLAUDE.md, Quy ước deploy mục 5).

## `nghiem_thu`

Mỗi tiêu chí kèm đột biến làm nó đổi màu (L3). Mọi ca A chạy `nlm_cli` bản THẬT đã chép vào cây tạm (import theo đường dẫn,
`HOME` tạm, `CLAUDE_CODE_REMOTE=true` trừ khi ca nói khác); đếm lời gọi bằng nhật ký của đồ giả.

| # | mục tiêu | tiêu chí | phép đo làm ĐỎ (đột biến) |
|---|---|---|---|
| A1 | 1 | `CLAUDE_CODE_REMOTE` vắng · `false` · có `TL_NLM_NAP_LAI_TAT=1` (ba ca riêng), `nlm` giả rc 1 + `Authentication expired` ⇒ `_run` trả đúng `(rc, out, err)` như bản base trên cùng đồ giả (so tuple), 0 lời gọi `tl.py`, stderr tiến trình không có `nlm_nap_lai:` | bỏ cổng `CLAUDE_CODE_REMOTE` ⇒ ĐỎ; bỏ cổng `TL_NLM_NAP_LAI_TAT` ⇒ ĐỎ |
| A2 | 1 | rc 1 không chứa chuỗi auth · rc 124 · rc 127 (ba ca) ⇒ 0 lời gọi `tl.py` | coi rc 124 là ứng viên ⇒ ĐỎ |
| A3 | 1 | jar chết, bundle sống, argv `source list NB -j` ⇒ nhật ký đúng thứ tự `nlm` → `canary` → `tl nlm-auth-load` → `canary` → `nlm`; `_run` trả rc 0 của lần chạy lại; stderr có đúng 1 dòng `nlm_nap_lai: ĐÃ NẠP, THỬ LẠI ĐẠT — …`; `source_list` trả dict có `nap_lai.trang_thai == "ĐÃ NẠP, THỬ LẠI ĐẠT"` | bỏ bước chạy lại ⇒ ĐỎ |
| A4 | 1 | mọi lời gọi `tl.py` trong nhật ký mang `TL_NLM_NAP_LAI_TAT=1`; `tl.py` giả của ca này gọi ngược `nlm_cli._run` với lỗi auth ⇒ tổng lời gọi `nlm-auth-load` = **1** (không đệ quy) | không đặt biến cho con ⇒ ĐỎ (đếm > 1 hoặc quá hạn) |
| A5 | 1 | `_nlm_auth_alive` giả trả `True` · `None` · ném ngoại lệ · con ngủ quá hạn (hạn đặt nhỏ qua tham số test) (bốn ca) ⇒ 0 lời gọi `nlm-auth-load`; trạng thái lần lượt `BỎ QUA — canary sống…`, `KHÔNG ĐO ĐƯỢC — canary …` ×3 | coi mã thoát khác 0 là chết (thay vì chỉ mã 3) ⇒ ĐỎ ở ca `None` |
| A13 | 1 | phân loại của canary THẬT (finding Codex PR #1101): gọi `tl_gws._nlm_auth_alive(nb, require_notebook_body=True)` bản THẬT với `nlm_cli` giả (đặt qua `_imp`) trả lần lượt `connection refused` · `HTTP 403 permission denied` (không chuỗi auth) · `Authentication expired` có `auth_hint` (ba ca riêng, chờ giữa lần thử bị thay bằng hàm rỗng) ⇒ `None`, `None`, `False`; cộng ba chuỗi TRỘN (r4, E7), mỗi chuỗi là kết quả của lần thử 1/2/3: `[refused, refused, auth]` ⇒ `False` · `[auth, refused, auth]` ⇒ `False` · `[auth, auth, refused]` ⇒ `None` (khoá đúng hành vi "chỉ lần cuối quyết định" mà r4 khai). Cùng sáu ca chạy qua `<CANARY>` của `nlm_cli.py` (tiến trình con) ⇒ mã 2, 2, 3, 3, 3, 2 | đổi `<CANARY>` sang `tl.py nlm-auth-status` ⇒ ĐỎ ở hai ca đầu (ra chết thay vì không kết luận); ca `[auth, auth, refused]` canh lời khai r4 — `_nlm_auth_alive` mà đổi sang "lần ĐẦU quyết định" thì ca ấy ĐỎ (đột biến trên bản sao tạm của `tl_gws.py` trong fragment, không sửa tệp thật) |
| A6 | 1 | bundle `chet` ⇒ 1 lời gọi `nlm-auth-load`, 0 lần chạy lại `nlm`, trạng thái `BUNDLE CŨNG CHẾT — …`, `_run` trả kết quả lần ĐẦU | chạy lại bất kể canary sau nạp ⇒ ĐỎ |
| A7 | 1 | bundle `cu_hon` ⇒ trạng thái `TỪ CHỐI HẠ CẤP`; argv của `nlm-auth-load` trong nhật ký không chứa `--force` (ở mọi ca A) | thêm `--force` ⇒ ĐỎ |
| A8 | 1 | argv `source add NB --url x` (lệnh ghi), jar chết, bundle sống ⇒ nạp 1 lần, `nlm` được gọi đúng **1** lần, trạng thái `ĐÃ NẠP, KHÔNG THỬ LẠI (lệnh ghi)`; argv `notebook query NB q -j` ⇒ có chạy lại | đổi danh sách cho phép thành danh sách cấm `(source,add)` ⇒ ĐỎ ở ca bổ sung `source sync` (phải KHÔNG thử lại) |
| A9 | 1 | hai lời gọi `_run` liên tiếp cùng tiến trình, jar vẫn chết sau lần nạp ⇒ lời gọi thứ hai: 0 lời gọi `tl.py`, `BỎ QUA — đã nạp …`; tiến trình MỚI với dấu `ts = now − 300` ⇒ `BỎ QUA`; dấu `ts = now − 700` ⇒ nạp; dấu `ts = now + 3600` ⇒ nạp; dấu là `[1]` ⇒ nạp (năm ca riêng) | đổi 600 thành 60 ⇒ ĐỎ ở ca −300; bỏ chốt đồng hồ lệch ⇒ ĐỎ ở ca +3600 |
| A10 | 1 | dấu được ghi TRƯỚC lời gọi `nlm-auth-load`: `tl.py` giả đọc tệp dấu lúc nhận `nlm-auth-load` và ghi vào nhật ký `dau_co=1`; quyền tệp 0600 (POSIX) | ghi dấu sau khi nạp ⇒ ĐỎ |
| A11 | 1 | (r6, E16 — đơn vị là LỜI GỌI `_run`, không phải tiến trình) mọi ca A, mỗi lời gọi `_run` đo riêng bằng cách thay `sys.stderr` bằng một bộ đệm mới trước lời gọi: bộ đệm ấy có ≤ 1 dòng `nlm_nap_lai:`, và đúng 1 dòng khi nhật ký đồ giả cho thấy lời gọi đã tới bước Giới hạn (có lời gọi `canary` hoặc trạng thái `BỎ QUA — đã nạp`); ca đầu của A9 (hai lời gọi cùng tiến trình) ⇒ đúng 2 dòng, theo thứ tự `BUNDLE CŨNG CHẾT` rồi `BỎ QUA — đã nạp`, mỗi bộ đệm một dòng; stdout và chuỗi `err` trả về không chứa `nlm_nap_lai:`; không chứa sentinel cookie mà `tl.py` giả in ra | chuyển tiếp đầu ra của con ⇒ ĐỎ; in hai dòng trong một lời gọi ⇒ ĐỎ; ghi thẳng fd 2 thay vì `sys.stderr` ⇒ ĐỎ (bộ đệm rỗng ở lời gọi đã tới Giới hạn) |
| A12 | 1 | `AUTH_FIX_HINT`, `AUTH_FIX_HINT_SHORT`, `_AUTH_FIX_ORDER`, `_AUTH_FIX_RASOAT_CARVE` của head bằng base (so từng hằng, giá trị đọc từ `git show <base>:scripts/nlm_cli.py`) | sửa câu trừ ⇒ ĐỎ |
| D1 | 4, 5 | (r8, E23 — hạ từ r7) hai tệp `RASOAT_HOSO_LOOP.md`, `QUY_TRINH_RA_SOAT_3_TANG.md`, đo riêng từng tệp (L6c), trên văn bản THÔ của cả tệp đã gộp mọi chuỗi khoảng trắng thành một dấu cách (`' '.join(text.split())`): (a) câu ngoại lệ của mục tiêu 4 xuất hiện đúng 1 lần; vế âm trên base: 0 lần; (b) bảo toàn chữ cũ (giữ từ r5, E12): ở head xoá đúng MỘT lần câu ngoại lệ kèm một dấu cách liền trước ⇒ BẰNG base từng ký tự. D1 KHÔNG chứng minh vị trí của câu (đúng §4b / gạch "Sửa xác thực") hay việc câu hiển thị khi render — hai điều ấy thuộc R1 | không chèn ⇒ ĐỎ; chèn hai lần ⇒ ĐỎ; bỏ ngoặc "(ghi đè jar bằng bản cũ/cũng chết)" (RASOAT) / bỏ `**` quanh `CẤM` (QUY_TRINH) ⇒ ĐỎ; ĐỐI CHỨNG XANH: chèn sau dấu cách; chèn sau xuống dòng; đổi ngắt dòng đoạn cũ (chạy thử phiên 04-11 trên bản base thật: đúng như vậy ở cả hai tệp) |
| D2 | 6, 7 | `python .claude/dev/packet_loop.py adr-song --root .` rc 0; bảng §20 có đúng 1 dòng mà ô đầu là `ADR-0064` trong dấu nháy ngược, cùng dạng dòng `ADR-0060` sẵn có (vế âm trên base: 0) | xoá dòng §20 ⇒ `adr-song` ĐỎ |
| D3 | 6 | (r8, E23 — hạ từ r7) trên văn bản THÔ của tệp ADR, KHÔNG che, KHÔNG gộp: số dòng khớp `_ADR_TRANG_THAI` (regex nguồn của D2, `.claude/dev/packet_loop.py:1887` trên `1f0941e9`, cờ `re.M`) bằng đúng 1, và dòng ấy sau khi cắt khoảng trắng hai đầu BẰNG `- **Trạng thái:** Accepted`. Vì không che, một dòng trạng thái thứ hai ở BẤT KỲ đâu (kể cả trong comment hay khối mã) cũng làm ĐỎ — chủ ý thiên về ĐỎ. Vế âm trên base: tệp `docs/adr/0064-*` vắng. Nội dung ADR (sáu câu, `r208c`, `wp1099_nlm_nap_lai`) thuộc R1 | `Trạng thái: Accepted` trần ⇒ D3 ĐỎ và D2 ĐỎ; `Proposed` ⇒ ĐỎ; giữ Accepted rồi thêm dòng `- **Trạng thái:** Proposed` ở bất kỳ đâu ⇒ ĐỎ; nhân đôi Accepted ⇒ ĐỎ; ĐỐI CHỨNG XANH (D2 + D3): ADR đúng mục tiêu 6 |
| H1 | 8 | (r8, E23 — hạ từ r7) `changelog.d/wp-1099.md` tồn tại và dòng đầu tiên không rỗng của tệp bắt đầu bằng `WP1099 (CLOUD-SETUP-P3B-NLM-401): `. Vế âm trên base: tệp vắng. Nội dung (mô tả đúng hành vi) thuộc R1 | tệp vắng hoặc rỗng ⇒ ĐỎ; bỏ tiền tố ⇒ ĐỎ |
| R1 | 4, 5, 6, 8 | (r8, E23 — tiêu chí NGƯỜI ĐỌC, không phải phép đo máy) reviewer độc lập của PR code (provider khác executor) đọc bản render của bốn tệp và ghi vào VERDICT từng dòng, mỗi dòng `đạt`/`không đạt` kèm trích dẫn: (i) câu ngoại lệ nằm trong §4b của `RASOAT_HOSO_LOOP.md` và trong gạch "Sửa xác thực" của `QUY_TRINH_RA_SOAT_3_TANG.md`, hiển thị như văn bản thường; (ii) mục "Quyết định" của ADR-0064 có đúng sáu gạch đầu dòng nguyên văn của mục tiêu 6, không thêm quyết định; ADR nêu `r208c` và trỏ fragment `wp1099_nlm_nap_lai`; (iii) `changelog.d/wp-1099.md` là đoạn văn tiếng Anh mô tả đúng hành vi của mục tiêu 1 | một dòng `không đạt` ⇒ finding P2, PR code không approve. Thiếu bất kỳ dòng nào trong VERDICT ⇒ coi như chưa review |
| F1 | 2, 3 | `python scripts/tl.py --selftest` (Ubuntu, `core.abbrev=7`) in `N/N` với hai số bằng nhau; N = N của base + số ca của fragment mới; dòng `wp1099_nlm_nap_lai` có mặt và ĐẠT; bảng đột biến của fragment: mọi đột biến bị giết đúng lý do (ca đích nhận diện bằng lớp ngoại lệ riêng kèm tên ca — CLAUDE.md, bài học "đột biến bị giết không phải đột biến bị giết đúng lý do") (r10, E27) đột biến nào cần năng lực nền (`doc_dau_chan`: `os.O_NONBLOCK` + `os.mkfifo`; `doc_dau_ro_fd`: `os.open` mở được thư mục, đo bằng `/dev/fd`) khai năng lực ấy trong bảng; nền thiếu năng lực ⇒ đột biến ghi `BỎ QUA` kèm lý do trong dòng tổng, KHÔNG tính giết; trên `os.name == "posix"` danh sách `BỎ QUA` phải rỗng | một đột biến sống ⇒ ĐỎ; trên posix có `BỎ QUA` ⇒ ĐỎ; gỡ khai năng lực ⇒ `run` trên Windows trả False (đo 05-11, `tra-luat-win`, head `6f35ad14`: hai đột biến trên SỐNG) |
| F2 | — | ca `r213_auth_carve_out_khong_pha_thu_tu` ĐẠT trên head mà KHÔNG sửa `tl_selftest.py` | sửa câu trừ hay xoá chữ `CẤM` ở `QUY_TRINH` ⇒ ĐỎ |
| F3 | 3 | (r9, E24) HAI phép, cả hai phải đạt trên head: (a) độ tươi — `python scripts/tl.py test-fragments-check --root . --json` rc 0, `ok=true`, `status=current` (`expected_sha256 == actual_sha256`; hàm `_test_fragments_check`, `scripts/tl_core/release.py:206` trên `1f0941e9`, so byte bundle với bộ sinh); (b) topology/hành vi — bước CI `bundled-fragment check (topology gói)` (`python .github/checks/bundle_fragment_check.py --json`) `ok`. (b) chỉ so tập `TEST_ID` và chạy bản trong bundle, KHÔNG chứng minh bundle khớp nguồn — đó là việc của (a). Đo trên base `1f0941e9` (04-11): (a) rc 0, `status=current` | sửa THÂN fragment, giữ `TEST_ID`, không sinh lại bundle ⇒ (a) ĐỎ (`ok=false`, lỗi `GENERATED_BUNDLE_STALE`) trong khi (b) vẫn XANH; đổi `TEST_ID` không sinh lại ⇒ (b) ĐỎ (`TEST_ID_SET_MISMATCH`); sinh lại bundle ⇒ (a) XANH (reviewer `8191331a` đo cả ba ca trên hàm nguồn) |
| J1 | 9 | `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` ⇒ `ok=true`, `expected == checked` | sửa một byte `nlm_cli.py` sau tái sinh ⇒ ĐỎ |
| G1 | — | selftest delta so base = 0 ca đỏ mới (đơn vị: ca selftest; nền đo lại trên base lúc cấp lease) | một ca đạt trên base mà đỏ trên head ⇒ ĐỎ |
| G2 | — | `python .claude/dev/packet_loop.py doctrine-scan --root .` rc 0 (canh bất biến; đo trên base `1f0941e9` 04-11: rc 0, quét 10 tệp, 0 chỗ chép) | (r9, E25) đối chứng âm, tệp NGOÀI cây kho: tệp Markdown tạm chứa cụm `3 attempt/packet`, truyền thêm bằng `--path <tệp tạm>` ⇒ rc 6, nhóm `nguong-so-stop-conditions` (đo phiên 04-11 trên `1f0941e9`: đúng như vậy); bỏ cụm ⇒ rc 0. Không chèn câu thử vào tài liệu thật của kho |
| K1 | — | `ruff check --select F scripts/nlm_cli.py scripts/test_fragments/wp1099_nlm_nap_lai.py` ⇒ delta so base = 0 | thêm tên chưa định nghĩa ⇒ ĐỎ |
| K2 | — | `git diff --numstat origin/master...HEAD` ⇒ đúng các tệp của `write_set`, ≤ 9 tệp, ≤ 550 dòng thêm | vượt hoặc có tệp lạ ⇒ ĐỎ; DỪNG hỏi chủ kho |
| L1 | — | lượt CI PR (Ubuntu) trên head ứng viên: mọi job bắt buộc theo `ci.yml` lúc nghiệm thu `success`; đọc nhãn job (CLAUDE.md, bài học (c)) | một job bắt buộc đỏ do packet ⇒ ĐỎ |
| W1 | 2, 3 | (r10, E27) lượt `ci.yml` `runner_set=windows-only` (`workflow_dispatch`, do điều phối hoặc chủ kho bấm — lease executor cấm) trên ĐÚNG head ứng viên: job `gate (windows-latest)` `success` (gồm `.githooks/eol_policy_test.py`, nơi fragment chạy trong gói đã giải nén); và `run(tl)` của fragment trên cây dev Windows trả True với dòng tổng liệt kê `BỎ QUA` đúng hai đột biến của F1. Dùng làm bằng chứng K6 (`--windows-json`) | gỡ khai năng lực ⇒ `eol_policy_test` 27/30 như run `41969252966` ⇒ ĐỎ |
| M1 | 1 (LIVE, sau land) | phiên Claude Code web trên master sau land; chủ kho duyệt riêng trước khi chạy. (i) sao lưu `~/.notebooklm-mcp-cli`; (ii) thay `profiles/default/cookies.json` bằng một bản đã hết hạn; (iii) một lệnh `tl` đọc đi qua `nlm_cli.source_list` ⇒ stderr có `nlm_nap_lai: ĐÃ NẠP, THỬ LẠI ĐẠT` và lệnh thành công; (iv) làm hỏng jar lần nữa, chạy lại trong vòng 10 phút ⇒ `nlm_nap_lai: BỎ QUA — đã nạp …`, 0 lần nạp; (v) khôi phục bản sao lưu. Biên nhận chỉ ghi rc, trạng thái, thời điểm; không ghi cookie | `chưa đo được` cho tới khi chạy thật. Vế (iii) là phép đo DUY NHẤT xác nhận `nlm_cred.enc` LIVE đủ tươi để hồi sinh jar; không thay bằng phép đo khác. Ai đo: phiên điều phối hoặc executor, sau khi chủ kho duyệt |

Ghi chú L6. D1, D2, D3, H1 có vế dương trên head và vế âm trên base (L6a). D1 gộp khoảng trắng TOÀN tệp vì nó chỉ đếm một câu
và bảo toàn chữ cũ, không khẳng định cấu trúc đoạn (L6b; khai rõ ở D1 điều nó KHÔNG chứng minh). D3, H1 đo trên văn bản thô, không
gộp. D1 đếm từng tệp; D3 đếm dòng trạng thái; A1, A2, A5, A9 đếm từng ca riêng; A11 đếm theo từng lời gọi `_run` (L6c). R1 là
tiêu chí người đọc, ghi rõ là không phải phép đo máy. Không có lời khai số lượng dạng chữ (L6d). Không có lời khai
"không cổng nào cưỡng chế" (L6e).

Chạy thử trên nền (đo lại 15:2xZ 04-11, `1f0941e9`; r3 đo trên `90c101b8` với số ADR cũ): `rg -c "ADR-0064" docs/PROTOCOL_DA_PHIEN.md` ⇒ 0; `docs/adr/0064-*` vắng; câu
ngoại lệ 0 lần ở cả hai tài liệu; `rg -c "NAP_LAI|nap_lai" scripts/nlm_cli.py` ⇒ 0 — tức D1, D2, D3, A* ra "chưa làm". G2, F2
xanh sẵn vì canh bất biến.

## Kích thước

**Ước tính, chưa đo** (02:2xZ 01-11). `nlm_cli.py` ~120 · fragment ~280 · ADR ~70 · changelog ~10 · manifest ~6 · bundle ~2
(mỗi fragment là một dòng chuỗi trong bundle) · hai tài liệu doctrine ~6 · protocol 1 ⇒ **~495 dòng thêm / 9 tệp**. Đối chiếu:
fragment `wp726_script_nlm_canary.py` 260 dòng, `wp727_tl_gws_refresh.py` 259 dòng. Lời gọi Codex theo `ADR-0052`: **8** (vòng 2
Q14). Lời gọi thứ 8 chưa approve ⇒ Review Rescue Checkpoint (`ADR-0037`). Trước MỖI lời gọi Codex, đếm số đã dùng.

## `hinh_dang_ke_thua`

`khong_ap_dung` — packet này không khắc phục packet nào. Ghi chú cho người thi hành:
- Packet này **đảo một quyết định đã được viết ra để chặn đúng nó** (r208c). Hai hình dạng lỗi r208c đã đo thật ngày 25-07 —
  **bundle cũ hơn jar** (chặn bằng `_nlm_auth_load_downgrade`, ca A7) và **bundle cũng chết** (ca A6) — là hai lớp dễ tái phát
  nhất. Lớp thứ ba dễ gặp là **đệ quy canary → `nlm_cli` → canary** (ca A4). Một finding cùng hình dạng lần thứ ba ⇒ dừng, hỏi
  chủ kho có nên đổi cấu trúc không, đừng vá tiếp.
- Chuỗi cloud-setup: P2a dùng hết 8/8 lời gọi Codex; P1 vượt trần ba lần vì thiếu tệp cơ học — ở đây bundle fragment và
  manifest đã nằm sẵn trong write set.

## `chua_do_duoc`

- **`nlm_cred.enc` LIVE có thực sự tươi hơn `tl_secrets.enc`**: chỉ suy từ lịch WP710 (30 phút) và log bootstrap ("~1 ngày
  tuổi"); phiên soạn không đọc Drive. Đo ở M1 vế (iii).
- **Đầu ra thật của `nlm` khi jar chết**: bộ chuỗi ứng viên lấy từ mã hiện có, chưa đo lại trên CLI `notebooklm-mcp-cli` đang
  ghim. Nếu CLI đổi thông điệp mà không còn chuỗi nào khớp, cơ chế IM LẶNG (không nạp) — fail-close, đo ở M1.
- **Chú thích nguồn `tl_gws.py` khai "bền qua 3 lần"** trong khi mã chỉ xét lần cuối (E7): packet này KHÔNG sửa chú thích ấy (ngoài
  write set); nợ ghi lại cho packet chạm `tl_gws.py` sau.
- **Canary `_nlm_auth_alive` chạy được trong cây phát hành ở phiên cloud**: ba script WP710/wp726 gọi nó trên laptop; trên phiên
  cloud chưa đo. (Câu r1/r2 ở chỗ này — "`nlm-auth-status` ra `alive` ba trạng thái" — là SAI: `None` chỉ khi không probe;
  mọi lỗi probe ra `False`, `nlm_ops.py:1424–1430`. Đó chính là finding Codex của PR #1101.)
- **Hai tiến trình cùng nạp trong cùng một giây**: tệp dấu không có khoá; cả hai có thể cùng qua bước "Giới hạn" và nạp hai lần.
  Hậu quả: hai lần ghi đè jar bằng cùng một bản. Chấp nhận ở r1. Vì vậy trần 600 s giữa tiến trình chỉ là best effort (r5, E13).
- **Cowork, Windows**: hành vi runtime trên Windows không đo (cơ chế chỉ bật khi `CLAUDE_CODE_REMOTE == "true"`). Từ r10 chỉ
  FRAGMENT được đo trên Windows (W1), vì nó chạy trong selftest trên laptop của chủ kho.

## `errata_r2`

Soạn 02-11-2026 ~01:1xZ trên `origin/master` = `c7174bfe`. Mỗi sửa đổi kèm phép đo đã chạy. Không sửa đổi nào đổi phạm vi, mục
tiêu, tiêu chí hay trần; chỉ làm văn bản khớp với kho hiện tại.

| # | chỗ sửa trong r1 | r1 viết | r2 viết | phép đo |
|---|---|---|---|---|
| E1 | `write_set` mục 6, `muc_tieu` 4, 6, 7, `nghiem_thu` D2, D3, mọi chỗ nhắc ADR | `ADR-0061`, `docs/adr/0061-nlm-tu-nap-lai-co-dieu-kien-phien-cloud.md` | `ADR-0062`, `docs/adr/0062-nlm-tu-nap-lai-co-dieu-kien-phien-cloud.md` | số `0061` đã bị lease `wp825-r1-g1-claude` (packet #825) chiếm: tệp `docs/adr/0061-codex-trang-thai-tu-choi-khong-ghi-duoc.md` có trên `refs/remotes/origin/ops/wp825-r1-g1-lease` và trong `write_set` của lease ấy. Quét mọi ref `origin/*` tìm `docs/adr/006[1-9]-*` ⇒ đúng 1 tệp (số 0061); số 0062 trống. r1 đo lúc soạn chỉ trên `master` (ADR mới nhất `0060`) — đúng bệnh "sổ không nằm một chỗ" CLAUDE.md đã ghi |
| E2 | điều kiện cấp lease | lease P3 `wp1089-…-r2-g1` giữ `RELEASE_MANIFEST.json` | `wp1134-r2-g1-claude` giữ manifest + bundle; `wp825-r1-g1-claude` giữ `docs/PROTOCOL_DA_PHIEN.md`; thêm chốt số ADR | `ai-dang-giu` trên 9 đường dẫn, 01:0xZ 02-11 |
| E3 | base dự kiến | `90c101b8` | `c7174bfe` | `git log -1 origin/master` 01:0xZ 02-11. `git diff --stat 90c101b8 c7174bfe` trên `nlm_cli.py`, `RASOAT_HOSO_LOOP.md`, `QUY_TRINH_RA_SOAT_3_TANG.md`, `tl_gws.py`, `tl_core/nlm_ops.py` ⇒ 0 dòng đổi, nên mọi neo dòng vào các tệp ấy (vd `nlm_cli.py:143`, `QUY_TRINH…:49`, `nlm_ops.py:296`, `:1398`) còn đúng |
| E4 | neo dòng selftest r213 | `tl_selftest.py:24836` | `tl_selftest.py:24827` | `git show c7174bfe:scripts/tl_selftest.py \| grep -n _c213_auth` ⇒ dòng 24827 (`def`), 24850 (đăng ký) |
| E5 | số tệp manifest | 197 | 198 | `json.load` trên `c7174bfe:RELEASE_MANIFEST.json` |

Không đổi: số đếm và thời điểm đo ở mục *Vấn đề*, *Kích thước*, *chua_do_duoc* (đó là phép đo lúc soạn r1, ghi kèm giờ); dòng
"Chạy thử trên nền" giữ nguyên vì `nlm_cli.py` và hai tài liệu doctrine không đổi giữa hai base (E3).

## `errata_r3`

Soạn 02-11-2026 ~01:5xZ trên `origin/master` = `c7174bfe`, xử finding P2 duy nhất của Codex connector trên PR #1101 (review
`5731324565`, comment `4438275720`, neo commit `1570b442`, tệp r2 dòng 90).

| # | chỗ sửa | r2 viết | r3 viết | phép đo |
|---|---|---|---|---|
| E6 | `muc_tieu` 1, bước Xác nhận / Kiểm lại; `muc_tieu` 2 (đồ giả); `nghiem_thu` A3, A5; thêm A13; `ngoai_pham_vi`; `chua_do_duoc` | canary = `tl.py nlm-auth-status`, đọc `alive is False` từ JSON, timeout 60 s | canary = tiến trình con chạy `_nlm_auth_alive(..., require_notebook_body=True)` cùng thân `_canary_song` của `nlm-auto-refresh.sh`; chỉ mã 3 (chết) mới nạp; timeout 120 s (nạp vẫn 60 s) | đọc `c7174bfe:scripts/tl_core/nlm_ops.py:1424–1430`: `rep["alive"] = bool(r.get("ok"))`, và nhánh `except` gán `False` ⇒ `nlm-auth-status` gộp lỗi mạng/quyền với auth chết, đúng như finding. Đọc `c7174bfe:scripts/tl_gws.py:332–363`: thử 3 lần, `auth_hint` bền ⇒ `False`, chuỗi mạng/tạm thời ⇒ `None`, khác ⇒ `None` ("không phải auth"). `c7174bfe:scripts/nlm-auto-refresh.sh:93–105` gọi đúng hàm ấy với `require_notebook_body=True`, thoát 0/3/2 |

Hệ quả cho quyết định đã duyệt: **vòng 2 Q11** chọn lệnh `tl.py nlm-auth-status` làm canary. r3 thay lệnh ấy vì nó không thực
hiện được **vòng 1 Q4** ("chỉ khi canary trả chết chắc mới nạp; không kết luận thì không nạp"). Ý định Q4/Q11 (canary LIVE ba
trạng thái, chạy trong tiến trình con, chống đệ quy bằng `TL_NLM_NAP_LAI_TAT=1`) giữ nguyên; chỉ đổi lệnh con và timeout. Write
set, trần, mục tiêu 2–9 và mọi tiêu chí khác không đổi. `nlm_ops.py` không bị sửa.

## `errata_r4`

Soạn 04-11-2026 ~15:2xZ trên `origin/master` = `1f0941e9`. Nguồn: review độc lập Codex trên r3 (`launcher.py run 981acca8`, head
`c6e4388a`, lời gọi 1/8 của #1099), `VERDICT` ghi dở với 2 finding P2; và phép đo số ADR. Không đổi phạm vi, write set (vẫn 9
đường dẫn, chỉ đổi số ADR trong tên tệp), trần, hay mục tiêu.

| # | chỗ sửa | r3 viết | r4 viết | phép đo |
|---|---|---|---|---|
| E7 | `muc_tieu` 1 (Xác nhận), `nghiem_thu` A13, `chua_do_duoc` | `_nlm_auth_alive` "chỉ trả False khi auth_hint bền qua 3 lần probe" | chỉ lần thử CUỐI quyết định; chuỗi trộn kết thúc bằng auth ra `False` — CHẤP NHẬN theo quyết định chủ kho 04-11 (giữ canary chuẩn, sửa lời khai, thêm 3 ca trộn vào A13) | đọc `1f0941e9:scripts/tl_gws.py:308–363`: vòng `for _att in range(3)` thử lại khi lỗi auth/mạng rồi `break`; sau vòng chỉ xét `r` của lần cuối. Reviewer tái hiện bằng AST + đồ giả: `[refused, refused, auth]` và `[auth, refused, auth]` ⇒ `False`/mã 3 (finding F01) |
| E8 | `nghiem_thu` D1 | mẫu chung `CẤM tự` ở mỗi tệp | mẫu riêng từng tệp (`CẤM tự` ở RASOAT, `**CẤM** tự` ở QUY_TRINH), đo head == base | `1f0941e9:references/QUY_TRINH_RA_SOAT_3_TANG.md:49` viết `**CẤM** tự`; gộp khoảng trắng không bỏ `**` (finding F02). Reviewer cũng đo: ca r213 xanh trên cả base lẫn bản thêm câu ngoại lệ — không cần sửa `tl_selftest.py` |
| E9 | mọi chỗ nhắc ADR mới | `ADR-0062`, `docs/adr/0062-nlm-tu-nap-lai-co-dieu-kien-phien-cloud.md` | `ADR-0063`, `docs/adr/0063-nlm-tu-nap-lai-co-dieu-kien-phien-cloud.md` | `1f0941e9` có `docs/adr/0062-adr-0060-mac-dinh-va-dong-bang-adr-0054.md`; quét mọi ref `origin/*` (đủ ref, so tập `ls-remote` với `for-each-ref`) tìm `docs/adr/006[3-9]-*`/`007*` ⇒ 0 |
| E10 | base, neo dòng r213, manifest | `c7174bfe`, `tl_selftest.py:24827`, 198 tệp | `1f0941e9`, `24829`, 184 tệp | `git log -1 origin/master`; `grep -n _c213_auth`; `json.load` manifest. `git diff --stat 90c101b8 1f0941e9` trên `nlm_cli.py`, `RASOAT_HOSO_LOOP.md`, `QUY_TRINH_RA_SOAT_3_TANG.md`, `tl_gws.py`, `tl_core/nlm_ops.py` ⇒ 0 dòng đổi, nên các neo dòng vào năm tệp ấy còn đúng |

Lời gọi Codex của #1099 đã dùng: **1/8** (lượt review r3, cắt giữa chừng nhưng vẫn tính là một lời gọi theo cách đếm của
`ADR-0052`). Lượt review độc lập r4 sẽ là 2/8.

## `errata_r5`

Soạn 04-11-2026 ~16:2xZ, base vẫn `1f0941e9` (`origin/master`). Nguồn: review độc lập Codex `c095ffa5` trên r4 (head
`bbb0ec83`, tree `f16c7c75`, lời gọi 2/8 của #1099, `thoi_luong_giay` 782, verdict `request_changes`: F01 P2, F02 P3, F03 P2,
F04 P3). Không đổi phạm vi, write set (9 đường dẫn), trần, hay quyết định giữ canary "lần thử cuối quyết định".

| # | finding | chỗ sửa | r4 viết | r5 viết | phép đo |
|---|---|---|---|---|---|
| E11 | F01 (biểu hiện D3) | `muc_tieu` 6, `nghiem_thu` D3 | D3 đếm bảy token (`600`, `--force` …) | ADR chứa đúng sáu câu nguyên văn; D3 khớp nguyên câu | reviewer: fixture đủ bảy token vẫn ĐẠT khi đổi `600` → `1600` (khớp chuỗi con) |
| E12 | F01 (biểu hiện D1) | `nghiem_thu` D1 | đếm từ khoá `CẤM tự`/`**CẤM** tự` + `nlm-auth-load` head == base | gộp khoảng trắng toàn tệp, xoá đúng một câu ngoại lệ kèm một dấu cách liền trước ⇒ phải bằng base từng ký tự | reviewer: bỏ ngoặc giải thích cũ vẫn qua phép đếm r4. Chạy thử r5 (04-11) trên bản base của hai tệp: chèn câu ⇒ ĐẠT (cả khi chèn sau dấu cách lẫn sau xuống dòng); không chèn ⇒ ĐỎ; chèn hai lần ⇒ ĐỎ; bỏ ngoặc ở RASOAT / bỏ `**` ở QUY_TRINH ⇒ ĐỎ; đổi ngắt dòng đoạn cũ ⇒ ĐẠT |
| E13 | F03 | `van_de`, `muc_tieu` 1 (Xác nhận), 6, `chua_do_duoc` | "trần thiệt hại là một lần nạp … trong cửa sổ 10 phút" | trần BẢO ĐẢM: 1 lần/tiến trình; 600 s giữa tiến trình là best effort | reviewer mô hình hoá các bước đặc tả: hai tiến trình cùng đọc dấu vắng ⇒ `loads_same_window=2`, `per_process_loads=[1,1]` — khớp ngoại lệ r1 đã chấp nhận |
| E14 | F02 | `write_set` (đoạn không sửa), `van_de` | `nlm_ops.py:296`; `RASOAT_HOSO_LOOP.md:119` | `nlm_ops.py:297` (dòng khai báo `_AUTH_FIX_FALLBACK`); `RASOAT_HOSO_LOOP.md:118–119` (câu "CẤM tự" bắt đầu ở 118) | đo TỪNG neo trên `1f0941e9`, không suy từ diff rỗng: `nlm_cli.py:143/162/229` là dòng `auth = any(...)` ✓; `QUY_TRINH…:49` là gạch "Sửa xác thực" ✓; `tl_gws.py:308` là `def _nlm_auth_alive` và `:363` là `return` cuối ✓; `nlm_ops.py:1424–1430` là nhánh `notebook_get`/ngoại lệ gán `alive=False` ✓; `tl_selftest.py:24829` là `_c213_…` ✓; `nlm_ops.py:296` là chú thích ✗ ⇒ 297; `RASOAT…:119` là nửa sau câu ✗ ⇒ 118–119 |
| E15 | F04 | `muc_tieu` 8, `nghiem_thu` H1 (mới) | mục tiêu 8 không có tiêu chí | H1: tiền tố `WP1099 (CLOUD-SETUP-P3B-NLM-401): ` + bốn cụm, đếm riêng | reviewer: `unmapped_goals=[8]`. Khuôn đo trên `1f0941e9:changelog.d/wp-1038.md` (một đoạn bắt đầu `WP1038 (CLOUD-SETUP-P2A-EXEC): `) |

Errata lịch sử (`errata_r2` E1–E5, `errata_r3` E6, `errata_r4` E7–E10) giữ nguyên văn, kể cả neo `nlm_ops.py:296` nếu có. Lời gọi
Codex của #1099 đã dùng: **2/8**. Lượt review độc lập r5 sẽ là 3/8.

## `errata_r6`

Soạn 04-11-2026 ~16:3xZ, base vẫn `1f0941e9`. Nguồn: review độc lập Codex `9f127a0e` trên r5 (head `dc693d25`, tree `7211ec9b`,
lời gọi 3/8 của #1099, `thoi_luong_giay` 796, verdict `request_changes`: 2 finding P2 / 2 lớp). Lượt ấy xác nhận E11–E15 của
r5 đóng đúng biểu hiện được giao: D1, D3, H1 đỏ/xanh đúng với đột biến/đối chứng đã khai; A13 ra `None,None,False,False,False,None`
(mã `2,2,3,3,3,2`) trên hai hàm nguồn với đồ giả. Không đổi phạm vi, write set (9 đường dẫn), trần hay quyết định của chủ kho.

| # | finding | chỗ sửa | r5 viết | r6 viết | phép đo |
|---|---|---|---|---|---|
| E16 | F01 P2 `nghiem-thu-khac-don-vi-dem-log` | `muc_tieu` 1 (Báo), `nghiem_thu` A11 | A11: stderr TIẾN TRÌNH ≤ 1 dòng trong mọi ca A — mâu thuẫn A9 (2 lời gọi cùng tiến trình, mục tiêu 1 đòi mỗi lời gọi 1 dòng) | đơn vị là lời gọi `_run`; đo bằng bộ đệm `sys.stderr` riêng mỗi lời gọi; A9 ca đầu đòi đúng 2 dòng theo thứ tự; thêm ràng buộc ghi qua `sys.stderr` để phép đo bắt được | reviewer: mô hình nghĩa vụ `invocations_in_one_process=2`, `diagnostic_lines_required_by_goal_1=2`, `A11_at_most_one_line_per_process=false` |
| E17 | F02 P2 `thuoc-do-chuoi-khong-khop-markdown-nguon` | `muc_tieu` 6, `nghiem_thu` D3 | D3 đòi dòng nguyên văn `Trạng thái: Accepted` (gộp khoảng trắng) | ADR viết `- **Trạng thái:** Accepted`; D3 so nguyên dòng ấy, không gộp; D2 và D3 chạy cùng fixture | reviewer chạy `cmd_adr_song` nguồn trên bản sao docs: dòng trạng thái theo D3 r5 ⇒ D3 đạt, gate rc 9 ("không có dòng Trạng thái đọc được"); dòng `- **Trạng thái:** Accepted` ⇒ gate rc 0, D3 r5 trượt. Đo lại 04-11: `_ADR_TRANG_THAI = ^[-*]\s*\*\*Tr[aạ]ng th[aá]i:?\*\*:?\s*(\S.*)$` (`packet_loop.py:1887–1889`); `docs/adr/0060-…md:3`, `0062-…md:3` đều viết `- **Trạng thái:** Accepted (…)` |
| E18 | cùng lớp E17 (phiên tự quét) | `nghiem_thu` D1 | vế đầu "gộp khoảng trắng theo đoạn", vế sau so toàn tệp | cả D1 đo trên toàn tệp; câu ngoại lệ còn phải nằm đúng mục (§4b / "Sửa xác thực") | đọc lại r5 dòng 170: hai vế dùng hai đơn vị văn bản khác nhau trong cùng một tiêu chí |

Quét cùng lớp (phiên, 04-11): mọi tiêu chí còn lại khớp chuỗi trên Markdown nguồn — D2 (ô `ADR-0063` trong dấu nháy ngược, khuôn
dòng `| \`ADR-0060\` |` ở `docs/PROTOCOL_DA_PHIEN.md:1517` trên `1f0941e9`), H1 (changelog là văn xuôi thuần, khuôn
`changelog.d/wp-1038.md`) — không thấy biểu hiện khác. Lời gọi Codex của #1099 đã dùng: **3/8**; review độc lập r6 sẽ là 4/8.

## `errata_r7`

Soạn 04-11-2026 ~17:0xZ, base vẫn `1f0941e9`. Nguồn: review độc lập Codex `ca2338b5` trên r6 (head `c0c0f4d6`, tree `b03bf845`,
lời gọi 4/8 của #1099, `thoi_luong_giay` 678, `request_changes`: 2 P2 cùng ở D3). Lượt ấy xác nhận E16–E18 đóng đúng biểu hiện
được giao. Không đổi phạm vi, write set (9 đường dẫn), trần hay quyết định của chủ kho.

**Vì sao r7 đổi cách đo thay vì vá thêm.** Ba lượt liền (r4 F01, r5 F02, r6 F01+F02) ra finding cùng lớp: phép đo khớp chuỗi trên
Markdown thô — đếm từ khoá, gộp toàn tệp, bỏ qua khuôn mà cổng đọc, đếm cả chỗ không render. Mỗi lượt vá đúng biểu hiện được chỉ
và để lộ biểu hiện kế tiếp (CLAUDE.md: "VÁ ĐÚNG CHỖ ĐƯỢC CHỈ RỒI BỎ SÓT ĐƯỜNG THỨ BA"; "đếm hình dạng lỗi, đừng chỉ đếm lỗi"). r7
liệt kê trước mọi đường vào của lớp — (1) vùng không render, (2) nối xuyên đoạn, (3) sai mục, (4) đếm một giá trị thay vì đếm
tổng, (5) khuôn Markdown khác khuôn cổng đọc — và đóng cả loạt bằng một thủ tục chung (V) dựa trên hàm nguồn của kho, mỗi đường một
đột biến riêng trong cột ĐỎ của D1/D3/H1.

| # | finding | chỗ sửa | r6 viết | r7 viết |
|---|---|---|---|---|
| E19 | lớp chung | `nghiem_thu` (đầu mục) | mỗi tiêu chí tự gộp khoảng trắng theo cách riêng | Thủ tục V: `_che_khong_render` → khối → gộp trong khối |
| E20 | tự quét (đường 1–3 ở D1) | D1 | câu ngoại lệ đếm trên văn bản thô gộp toàn tệp ⇒ câu trong comment hay thành đoạn riêng vẫn đếm | D1(a) theo V, khối chứa câu phải bằng đúng khối §4b/"Sửa xác thực" của base; D1(b) bảo toàn chữ cũ giữ nguyên |
| E21 | F01 P2 (đường 4) + F02 P2 (đường 1–3) | D3 | đếm dòng bằng `Accepted`; sáu câu đếm trên toàn tệp gộp | mọi dòng trạng thái gom thành danh sách phải bằng đúng một phần tử; sáu câu là đúng danh sách mục của `## Quyết định` sau V |
| E22 | tự quét (đường 1) ở H1 | H1 | cụm đếm trên văn bản thô | theo V |

Chạy thử (phiên, 04-11, đồ giả trong RAM, hàm nguồn `_che_khong_render`/`_ADR_TRANG_THAI` import từ `.claude/dev/packet_loop.py`
trên `1f0941e9`; hai tài liệu đọc bằng `git show 1f0941e9:<tệp>`): D1 — 2 tệp × (2 đối chứng XANH, 7 ca ĐỎ gồm base chưa chèn và 6 đột biến) đúng
như cột ĐỎ; D3 — 2 đối chứng XANH cả D2 lẫn D3, 11 đột biến ĐỎ ở D3 (trong đó 9 ca D2 vẫn XANH, tức D3 bắt được thứ D2 không
bắt); H1 — 2 đối chứng XANH, 4 đột biến ĐỎ. Đây là chạy thử thước đo trên đồ giả, không phải chạy tính năng (chưa tồn tại).
Lời gọi Codex của #1099 đã dùng: **4/8**; review độc lập r7 sẽ là 5/8.

## `errata_r8`

Soạn 04-11-2026 ~17:1xZ, base vẫn `1f0941e9`. Nguồn: review độc lập Codex `6488aa67` trên r7 (head `bc1d5e04`, tree `d72a43ce`,
lời gọi 5/8 của #1099, `thoi_luong_giay` 964, `request_changes`: 1 P2, lớp `thuoc-do-chuoi-khong-khop-markdown-nguon`). Phản chứng
của lượt ấy: `_che_khong_render` không hiểu inline code và code thụt lề; D3 chỉ lọc mục `- ` nên bỏ sót `*`/`+`/`1.`; không nhận
tiêu đề Setext; comment HTML hợp lệ có rào bên trong làm ĐỎ oan. Đây là lượt thứ TƯ liên tiếp cùng lớp (r4, r5, r6, r7).

| # | chỗ sửa | r7 viết | r8 viết | căn cứ |
|---|---|---|---|---|
| E23 | `nghiem_thu` (bỏ Thủ tục V), D1, D3, H1, R1 (mới), Ghi chú L6; `muc_tieu` 6 (chú thích) | máy đo cấu trúc Markdown bằng Thủ tục V | máy chỉ đo: D1 đếm câu + bảo toàn chữ cũ trên văn bản thô; D3 đúng 1 dòng trạng thái `Accepted` trên văn bản thô (D2 vẫn chạy `adr-song`); H1 tệp có tiền tố. Vị trí câu, nội dung ADR, nội dung changelog chuyển sang R1 — reviewer PR code đọc và ghi từng dòng vào VERDICT | quyết định chủ kho 04-11 ("Hạ D1/D3/H1"). Lý do: kiểm cấu trúc Markdown bằng văn xuôi trong đặc tả đòi một bộ phân tích Markdown đầy đủ; mỗi lượt vá chỉ đóng đường đã được chỉ (CLAUDE.md "đếm hình dạng lỗi, đừng chỉ đếm lỗi") |

Phạm vi, write set (9 đường dẫn), trần, mục tiêu 1–9 và quyết định giữ canary không đổi. Lời khai r7 "đóng cả lớp bằng Thủ tục V"
(`errata_r7`) là SAI theo phép đo của `6488aa67`; giữ nguyên văn như lịch sử, đính chính ở đây. Lời gọi Codex của #1099 đã dùng:
**5/8**; review độc lập r8 sẽ là 6/8.

## `errata_r9`

Soạn 04-11-2026 ~17:2xZ, base vẫn `1f0941e9`. Nguồn: review độc lập Codex `8191331a` trên r8 (head `8014baf0`, tree `604cdd8b`,
lời gọi 6/8 của #1099, `thoi_luong_giay` 1004, `request_changes`: F01 P2 lớp `phep-do-bundle-khong-kiem-do-tuoi-nguon`, F02 P3 lớp
`tieu-chi-khong-khai-dot-bien`). Lượt ấy không nêu finding nào về D1/D3/H1/R1 sau khi hạ. Không đổi phạm vi, write set (9 đường
dẫn), trần, mục tiêu hay các quyết định của chủ kho.

| # | finding | chỗ sửa | r8 viết | r9 viết | phép đo |
|---|---|---|---|---|---|
| E24 | F01 P2 | `nghiem_thu` F3 | chỉ `bundle_fragment_check.py`; khai "sửa fragment mà không sinh lại bundle ⇒ ĐỎ" | thêm (a) `tl.py test-fragments-check` (độ tươi, so byte với bộ sinh); khai rõ (b) chỉ canh tập ID + hành vi | reviewer: đổi thân giữ ID ⇒ (b) rc 0/ok true trong khi `_test_fragments_check` trả `GENERATED_BUNDLE_STALE`. Phiên đo lại 04-11 trên base: (a) rc 0, `status=current`, hai băm bằng nhau |
| E25 | F02 P3 | `nghiem_thu` G2 | cột đột biến `—` | đối chứng âm bằng tệp tạm ngoài cây qua `--path` | phiên 04-11: tệp tạm chứa `3 attempt/packet` ⇒ rc 6, `[nguong-so-stop-conditions]` |

Quét cùng lớp (phiên, 04-11): tiêu chí nào khác để `—` ở cột đột biến ⇒ chỉ có G2; tiêu chí nào khác dựa vào một cổng mà phạm vi
của cổng hẹp hơn lời khai ⇒ đã đọc lại F1, F2, J1, K1, K2, L1 — không thấy. Lời gọi Codex của #1099 đã dùng: **6/8**.

## `errata_r10`

Soạn 05-11-2026 ~05:2xZ trên base `e626648` (merge PR #1208). Nguồn: hai sự kiện SAU khi r9 đã thi hành ở PR #1197 (review độc
lập lượt 6 approve `781ef658`, lượt 8 approve head cuối `6f35ad14`).

| # | nguồn | chỗ sửa | r9 viết | r10 viết | phép đo |
|---|---|---|---|---|---|
| E26 | chủ kho, #1099 issuecomment-6650250003: `#1194 (Codex) giữ 0063` | điều kiện cấp lease, `write_set` mục 6–7, `muc_tieu` 4, 6, 7, `nghiem_thu` D2, D3, R1, chạy thử trên nền | `ADR-0063`, `docs/adr/0063-nlm-tu-nap-lai-co-dieu-kien-phien-cloud.md` | `ADR-0064`, `docs/adr/0064-nlm-tu-nap-lai-co-dieu-kien-phien-cloud.md` | nhánh `agent/pr1184-merge-contract-r2-g3-codex-service` (PR #1194) thêm `docs/adr/0063-merge-spec-ref-va-human-audit.md` ở `d40a45a` (04-11 11:04Z), trước phép đo r9 (15:2xZ 04-11) — phép đo r9 chỉ quét master, đúng bệnh "sổ không nằm một chỗ" mà E1 đã ghi. Quét r10: mục điều kiện cấp lease |
| E27 | K6 `kiem-merge` đỏ: run `41969252966`, job `gate (windows-latest)`, `eol_policy_test` 27/30 | `nghiem_thu` F1, thêm W1, `chua_do_duoc` | bảng đột biến không khai năng lực nền; Windows "không đo" | khai năng lực cho `doc_dau_chan`, `doc_dau_ro_fd`; W1 | chẩn đoán trên `tra-luat-win` (Python 3.12.10), head `6f35ad14`, `run(tl)` trên cây dev: ca A1–A13, D1–D3 ĐẠT; `FAIL đột biến không bị giết đúng lý do: doc_dau_ro_fd (SỐNG); doc_dau_chan (SỐNG)`. Cả hai TƯƠNG ĐƯƠNG trên Windows: không có `O_NONBLOCK` (getattr trả 0, mã y hệt) và không `os.open` được thư mục (không có fd để rò) |

Errata lịch sử (`errata_r2`…`errata_r9`) giữ nguyên văn, kể cả `ADR-0063` ở E9 và `errata_r6`. Trần kích thước KHÔNG đổi
(≤ 9 tệp / ≤ 550 dòng thêm). Lời gọi Codex của #1099: 8/8 đã dùng (lượt 7 bị container restart cắt, vẫn tính); chủ kho nâng trần
thêm **2** lời gọi (05-11, trả lời trong phiên executor) cho review bản vá này và một lượt dự phòng.
