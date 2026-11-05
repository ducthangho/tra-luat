# Đặc tả packet — `CLOUD-SETUP-P3B-NLM-401` (revision 5)

- `packet_id`: **CLOUD-SETUP-P3B-NLM-401** · `packet_issue`: **#1099** (Issue cha #1008; tách từ #1089 theo vòng 1 Q1 của đặc tả
  P3) · `revision`: **5** · trạng thái: r1 (sha256 `15fe242a…`), r2 (`c6e53a00…`), r3 (`e2246e90…`) land qua PR #1101 (merge
  `47ee1b20`); r4 (`d28d00b5…`) ở PR #1188, bị review độc lập Codex `c095ffa5` (lời gọi 2/8 của #1099, head `bbb0ec83`)
  request_changes với 2 P2 + 2 P3. Chưa revision nào được cấp lease hay thi hành. r5 soạn 04-11-2026 bởi phiên
  `session_015GtxrcPNaayykBErdfcNUB` để xử bốn finding ấy (mục `errata_r5` cuối tệp). Giữ nguyên `errata_r2`, `errata_r3`,
  `errata_r4`. Băm `sha256` của r5 ghi trên Issue #1099 và PR #1188, không ghi trong tệp. Lease phải neo **r5**. Sửa nội dung từ
  đây ⇒ revision 6.
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
  nào khác mang tiền tố `docs/adr/0063-` (đo 15:2xZ 04-11: 0); bị chiếm ⇒ DỪNG, ra revision mới đổi số — không tự chọn số khác.
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
6. `docs/adr/0063-nlm-tu-nap-lai-co-dieu-kien-phien-cloud.md` — **mới**
7. `docs/PROTOCOL_DA_PHIEN.md` — đúng 1 dòng `ADR-0063` trong bảng §20 (cổng `adr-song`)
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
   - **Báo** (Q7): mỗi lần cơ chế chạy qua bước "Giới hạn" in **đúng một** dòng ra **stderr của tiến trình** (không vào chuỗi
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
   cơ chế tự nạp có điều kiện bên trong `nlm_cli` ở phiên cloud (`ADR-0063`) — agent vẫn không tự gõ lệnh nạp."* Mọi chữ cũ giữ.
5. → `references/QUY_TRINH_RA_SOAT_3_TANG.md`: cùng câu ấy, nguyên văn, ở cuối gạch đầu dòng "Sửa xác thực". Mọi chữ cũ giữ.
6. → `docs/adr/0063-nlm-tu-nap-lai-co-dieu-kien-phien-cloud.md`: `Trạng thái: Accepted`; nêu nó **thay r208c ở đúng điểm "tự nạp
   khi hết hạn", chỉ cho phiên cloud**; tiền đề đã đổi (WP710 30 phút + canary trước stage của wp726; chốt chống hạ cấp còn);
   năm điều kiện (canary chết · chỉ `nlm_cred.enc` không `--force` · 1 lần/tiến trình (bảo đảm) + 600 s giữa tiến trình (best effort) · chỉ thử lại lệnh đọc · nạp xong
   vẫn chết ⇒ §4b); mục Cưỡng chế trỏ fragment `wp1099_nlm_nap_lai`. Mục "Quyết định" của ADR chứa NGUYÊN VĂN, mỗi câu một gạch
   đầu dòng riêng, đúng sáu câu sau (r5, E11 — D3 đo nguyên câu):
   - `Chỉ áp dụng khi biến môi trường CLAUDE_CODE_REMOTE có giá trị true.`
   - `Chỉ nạp khi canary _nlm_auth_alive trong tiến trình con trả mã 3 (jar đã chết).`
   - `Chỉ nạp từ nlm_cred.enc bằng tl.py nlm-auth-load, không dùng cờ --force.`
   - `Mỗi tiến trình nạp tối đa 1 lần; cửa sổ 600 giây giữa các tiến trình là best effort, không bảo đảm khi cạnh tranh.`
   - `Chỉ tự chạy lại các lệnh đọc trong danh sách cho phép.`
   - `Nạp xong mà vẫn lỗi xác thực thì dừng và làm theo §4b của RASOAT_HOSO_LOOP.md.`
7. → `docs/PROTOCOL_DA_PHIEN.md`: đúng 1 dòng mới trong bảng §20 cho `ADR-0063`, cột cổng = `wp1099_nlm_nap_lai (selftest
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
| A11 | 1 | mọi ca A: stderr tiến trình có ≤ 1 dòng `nlm_nap_lai:`; stdout và chuỗi `err` trả về không chứa `nlm_nap_lai:`; không chứa sentinel cookie mà `tl.py` giả in ra | chuyển tiếp đầu ra của con ⇒ ĐỎ |
| A12 | 1 | `AUTH_FIX_HINT`, `AUTH_FIX_HINT_SHORT`, `_AUTH_FIX_ORDER`, `_AUTH_FIX_RASOAT_CARVE` của head bằng base (so từng hằng, giá trị đọc từ `git show <base>:scripts/nlm_cli.py`) | sửa câu trừ ⇒ ĐỎ |
| D1 | 4, 5 | trên văn bản §4b của `RASOAT_HOSO_LOOP.md` và gạch "Sửa xác thực" của `QUY_TRINH_RA_SOAT_3_TANG.md`, đã gộp khoảng trắng theo đoạn (L6b): câu ngoại lệ ở mục tiêu 4 xuất hiện đúng 1 lần ở MỖI tệp (đếm riêng — L6c); vế âm trên base: 0 lần mỗi tệp; MỌI chữ cũ còn nguyên, đo trên TOÀN TỆP (r5, E12 — thay phép đếm từ khoá của r4): với mỗi tệp, gộp mọi chuỗi khoảng trắng của cả tệp thành một dấu cách (`' '.join(text.split())`) cho head và base; ở bản head xoá đúng MỘT lần xuất hiện của câu ngoại lệ kèm đúng một dấu cách liền trước nó; chuỗi còn lại phải BẰNG chuỗi base, so từng ký tự (mẫu `CẤM tự` của RASOAT và `**CẤM** tự` của QUY_TRINH, r4 E8, nay nằm trong phép so toàn tệp) | xoá câu ngoại lệ ở một tệp ⇒ ĐỎ; xoá/sửa hậu tố điều cấm cũ (vd bỏ ngoặc "(ghi đè jar bằng bản cũ/cũng chết)" ở RASOAT, hoặc bỏ `**` quanh `CẤM` ở QUY_TRINH) ⇒ ĐỎ; chèn câu ngoại lệ hai lần ⇒ ĐỎ; ĐỐI CHỨNG: chỉ đổi ngắt dòng/thụt lề của đoạn cũ ⇒ XANH |
| D2 | 6, 7 | `python .claude/dev/packet_loop.py adr-song --root .` rc 0; bảng §20 có đúng 1 dòng mà ô đầu là `ADR-0063` trong dấu nháy ngược, cùng dạng dòng `ADR-0060` sẵn có (vế âm trên base: 0) | xoá dòng §20 ⇒ `adr-song` ĐỎ |
| D3 | 6 | (r5, E11 — thay phép đếm token của r4) trên văn bản ADR đã gộp khoảng trắng toàn tệp: có đúng 1 dòng `Trạng thái: Accepted`; mỗi câu trong sáu câu nguyên văn của mục tiêu 6 xuất hiện đúng 1 lần, khớp NGUYÊN câu kể cả dấu chấm cuối (đếm từng câu riêng, L6c); có `r208c` và `wp1099_nlm_nap_lai`. Vế âm trên base: tệp `docs/adr/0063-*` vắng ⇒ 0 câu | xoá một câu ⇒ ĐỎ; đổi `600` thành `1600` hay `1 lần` thành `2 lần` trong câu ⇒ ĐỎ (nguyên câu không còn khớp); bỏ `không dùng cờ --force` khỏi câu thứ ba ⇒ ĐỎ; ĐỐI CHỨNG: ngắt dòng giữa câu ⇒ XANH |
| H1 | 8 | `changelog.d/wp-1099.md` tồn tại; sau khi gộp khoảng trắng, bắt đầu bằng `WP1099 (CLOUD-SETUP-P3B-NLM-401): ` và có mỗi cụm sau ít nhất 1 lần (đếm riêng): `CLAUDE_CODE_REMOTE`, `nlm-auth-load`, `TL_NLM_NAP_LAI_TAT`, `nlm_nap_lai`. Vế âm trên base: tệp vắng | tệp rỗng ⇒ ĐỎ; bỏ tiền tố `WP1099 (…): ` ⇒ ĐỎ; bỏ một cụm ⇒ ĐỎ |
| F1 | 2, 3 | `python scripts/tl.py --selftest` (Ubuntu, `core.abbrev=7`) in `N/N` với hai số bằng nhau; N = N của base + số ca của fragment mới; dòng `wp1099_nlm_nap_lai` có mặt và ĐẠT; bảng đột biến của fragment: mọi đột biến bị giết đúng lý do (ca đích nhận diện bằng lớp ngoại lệ riêng kèm tên ca — CLAUDE.md, bài học "đột biến bị giết không phải đột biến bị giết đúng lý do") | một đột biến sống ⇒ ĐỎ |
| F2 | — | ca `r213_auth_carve_out_khong_pha_thu_tu` ĐẠT trên head mà KHÔNG sửa `tl_selftest.py` | sửa câu trừ hay xoá chữ `CẤM` ở `QUY_TRINH` ⇒ ĐỎ |
| F3 | 3 | bước CI `bundled-fragment check (topology gói)` (`python .github/checks/bundle_fragment_check.py --json`) `ok` trên head | sửa fragment mà không sinh lại bundle ⇒ ĐỎ (`TEST_ID_SET_MISMATCH`/lệch băm) |
| J1 | 9 | `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` ⇒ `ok=true`, `expected == checked` | sửa một byte `nlm_cli.py` sau tái sinh ⇒ ĐỎ |
| G1 | — | selftest delta so base = 0 ca đỏ mới (đơn vị: ca selftest; nền đo lại trên base lúc cấp lease) | một ca đạt trên base mà đỏ trên head ⇒ ĐỎ |
| G2 | — | `python .claude/dev/packet_loop.py doctrine-scan --root .` rc 0 | — (canh bất biến; xanh sẵn trên nền) |
| K1 | — | `ruff check --select F scripts/nlm_cli.py scripts/test_fragments/wp1099_nlm_nap_lai.py` ⇒ delta so base = 0 | thêm tên chưa định nghĩa ⇒ ĐỎ |
| K2 | — | `git diff --numstat origin/master...HEAD` ⇒ đúng các tệp của `write_set`, ≤ 9 tệp, ≤ 550 dòng thêm | vượt hoặc có tệp lạ ⇒ ĐỎ; DỪNG hỏi chủ kho |
| L1 | — | lượt CI PR (Ubuntu) trên head ứng viên: mọi job bắt buộc theo `ci.yml` lúc nghiệm thu `success`; đọc nhãn job (CLAUDE.md, bài học (c)) | một job bắt buộc đỏ do packet ⇒ ĐỎ |
| M1 | 1 (LIVE, sau land) | phiên Claude Code web trên master sau land; chủ kho duyệt riêng trước khi chạy. (i) sao lưu `~/.notebooklm-mcp-cli`; (ii) thay `profiles/default/cookies.json` bằng một bản đã hết hạn; (iii) một lệnh `tl` đọc đi qua `nlm_cli.source_list` ⇒ stderr có `nlm_nap_lai: ĐÃ NẠP, THỬ LẠI ĐẠT` và lệnh thành công; (iv) làm hỏng jar lần nữa, chạy lại trong vòng 10 phút ⇒ `nlm_nap_lai: BỎ QUA — đã nạp …`, 0 lần nạp; (v) khôi phục bản sao lưu. Biên nhận chỉ ghi rc, trạng thái, thời điểm; không ghi cookie | `chưa đo được` cho tới khi chạy thật. Vế (iii) là phép đo DUY NHẤT xác nhận `nlm_cred.enc` LIVE đủ tươi để hồi sinh jar; không thay bằng phép đo khác. Ai đo: phiên điều phối hoặc executor, sau khi chủ kho duyệt |

Ghi chú L6. D1, D2, D3, H1 có vế dương trên head và vế âm trên base (L6a). D1, D3, H1 đo trên văn bản đã gộp khoảng trắng
toàn tệp (L6b); D1 và D3 so NGUYÊN chuỗi/nguyên câu, không đếm từ khoá (r5). D1 đếm từng tệp; D3, H1, A1, A2, A5, A9 đếm từng
ca/câu/cụm riêng (L6c). Không có lời khai số lượng dạng chữ (L6d). Không có lời khai
"không cổng nào cưỡng chế" (L6e).

Chạy thử trên nền (đo lại 15:2xZ 04-11, `1f0941e9`; r3 đo trên `90c101b8` với số ADR cũ): `rg -c "ADR-0063" docs/PROTOCOL_DA_PHIEN.md` ⇒ 0; `docs/adr/0063-*` vắng; câu
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
- **Cowork, Windows**: không đo (ngoài phạm vi).

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
