# Đặc tả packet — `CLOUD-SETUP-P3B-NLM-401` (revision 2 — errata)

- `packet_id`: **CLOUD-SETUP-P3B-NLM-401** · `packet_issue`: **#1099** (Issue cha #1008; tách từ #1089 theo vòng 1 Q1 của đặc tả
  P3) · `revision`: **2 (errata)** · trạng thái: r1 **ĐÓNG BĂNG** 01-11-2026 ~02:30Z (`ops/specs/cloud-setup-p3b-nlm-401-r1.md`,
  blob `ef74edbe`, sha256 `15fe242a…`; chưa cấp lease, chưa thi hành). r2 là **errata** của r1, soạn 02-11-2026 bởi phiên
  `session_015GtxrcPNaayykBErdfcNUB` theo chỉ thị chủ kho "Kiểm tra và cập nhật thay đổi"; chỉ sửa dữ kiện đã trôi (mục
  `errata_r2` cuối tệp), KHÔNG đổi phạm vi, mục tiêu hay tiêu chí. Băm `sha256` của r2 ghi trên Issue #1099 và PR #1101, không
  ghi trong tệp. Lease phải neo **r2**, không neo r1. Sửa nội dung từ đây ⇒ revision 3.
- `nguon_cap_viec`: chỉ thị chủ kho "soạn tiếp spec P3b NLM 401" (01-11 ~01:57Z) trong phiên nói trên; phạm vi gốc ở dòng P3 của
  bảng chuỗi #1008 ("NLM tải lại jar khi gặp 401"). Chốt trong phiên soạn: vòng 1 Q1–Q8 và vòng 2 Q9–Q17, chủ kho trả lời cả hai
  vòng "Đồng ý tất cả khuyến nghị". Không có dòng kế hoạch nào trong `ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md`.
- `review_class`: **sensitive** — ghi đè jar cookie NLM (`~/.notebooklm-mcp-cli`) và đổi doctrine (`RASOAT_HOSO_LOOP.md` §4b,
  ADR mới, bảng §20 của protocol) (protocol §8).
- Base dự kiến: `origin/master` lúc cấp lease (đo lại 01:0xZ 02-11: `c7174bfe`, merge PR #1130). Mọi phép đo kích thước/delta đo so
  merge-base (`git diff origin/master...HEAD`).
- **Điều kiện cấp lease (vòng 2 Q15, đo lại cho r2):** bất biến là *không lease nào còn hiệu lực giữ một đường dẫn của
  `write_set`*. Đo 01:0xZ 02-11 bằng `ops/lease_publish.py ai-dang-giu` sau khi fetch đủ ref: `RELEASE_MANIFEST.json` và
  `scripts/tl_test_fragments_bundled.py` ⇒ `NGƯỜI_GIỮ 1: wp1134-r2-g1-claude` (`CHANGELOG-D-NGOAI-GOI`, hạn
  `2026-11-02T23:53:00Z`); `docs/PROTOCOL_DA_PHIEN.md` ⇒ `NGƯỜI_GIỮ 1: wp825-r1-g1-claude` (hạn `2026-11-03T00:46:00Z`); sáu
  đường dẫn còn lại ⇒ `NGƯỜI_GIỮ 0`. Lease P3 `wp1089-…-r2-g1` nay `ĐÃ_BỊ_THAY_THẾ`. Chỉ cấp khi cả 9 đường dẫn ra
  `NGƯỜI_GIỮ 0`; đo lại ngay trước khi cấp (L5). **Thêm cho r2:** đo lại trên MỌI ref `refs/remotes/origin/*` rằng không tệp
  nào khác mang tiền tố `docs/adr/0062-` (đo 01:0xZ 02-11: 0); bị chiếm ⇒ DỪNG, ra r3 đổi số — không tự chọn số khác.
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
`references/RASOAT_HOSO_LOOP.md:119` và `references/QUY_TRINH_RA_SOAT_3_TANG.md:49`) vì bundle có thể **cũ hơn** hoặc **cũng
chết**, khiến vòng nạp-thử-lại quay vô ích. Packet này đảo quyết định ấy **có điều kiện, chỉ ở phiên cloud**: chỉ nạp khi canary
LIVE xác nhận jar hiện tại CHẾT, chỉ từ `nlm_cred.enc` qua lệnh có sẵn `tl nlm-auth-load` (giữ chốt chống hạ cấp), tối đa một lần
mỗi tiến trình và một lần mỗi 10 phút, và chỉ tự chạy lại lệnh ĐỌC.

## `write_set`

Đúng 9 đường dẫn (vòng 2 Q9). Không ký tự đại diện.

1. `scripts/nlm_cli.py` — cơ chế tự nạp lại trong `_run`
2. `scripts/test_fragments/wp1099_nlm_nap_lai.py` — **mới**: ca + đột biến
3. `scripts/tl_test_fragments_bundled.py` — sinh lại từ `scripts/test_fragments/` (CI PR chạy `bundled-fragment check`)
4. `references/RASOAT_HOSO_LOOP.md` — một câu ngoại lệ ở §4b
5. `references/QUY_TRINH_RA_SOAT_3_TANG.md` — cùng câu ngoại lệ ở dòng "Sửa xác thực" (dòng 49, đo 02:2xZ 01-11)
6. `docs/adr/0062-nlm-tu-nap-lai-co-dieu-kien-phien-cloud.md` — **mới**
7. `docs/PROTOCOL_DA_PHIEN.md` — đúng 1 dòng `ADR-0062` trong bảng §20 (cổng `adr-song`)
8. `changelog.d/wp-1099.md` — **mới**
9. `RELEASE_MANIFEST.json` — tái sinh vì (1), (3), (4), (5) nằm trong gói (manifest đo 01:0xZ 02-11 trên `c7174bfe`: 198 tệp, có cả bốn)

Không tệp nào khác. Cần sửa một tệp ngoài danh sách ⇒ DỪNG, hỏi chủ kho (L2). Cụ thể **KHÔNG** sửa `scripts/tl_selftest.py`
(ca `r213_auth_carve_out_khong_pha_thu_tu`, `tl_selftest.py:24827` trên `c7174bfe`, phải xanh NGUYÊN TRẠNG), `scripts/tl_gws.py`,
`scripts/tl_core/**` (kể cả `_AUTH_FIX_FALLBACK` ở `nlm_ops.py:296`), `SKILL.md`, golden, CHANGELOG, VERSION. Hằng
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
- **Import `tl_gws` vào `nlm_cli`** (vòng 1 Q5, vòng 2 Q11): `_nlm_auth_alive` (`tl_gws.py:308`) tự gọi `nlm_cli` ⇒ đệ quy.
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
   - **Xác nhận** (Q4, Q11): tiến trình con `[sys.executable, <thư mục chứa nlm_cli.py>/tl.py, "nlm-auth-status"]`, môi trường
     kế thừa cộng `TL_NLM_NAP_LAI_TAT=1`, stdin `DEVNULL`, timeout **60 s**. Đọc stdout làm JSON; chỉ `alive is False` (đúng kiểu
     `bool`) mới đi tiếp. `alive` là `True` ⇒ `BỎ QUA — canary sống, lỗi không do auth`; `None`, thiếu khoá, JSON hỏng, quá hạn,
     `OSError` ⇒ `KHÔNG ĐO ĐƯỢC — canary <lý do>`. Hai nhánh này không nạp.
   - **Nạp** (Q5, Q16): ghi tệp dấu `{ "ts": <epoch giây>, "ket_qua": "dang_nap" }` (0600, nguyên tử) **trước**, rồi tiến trình
     con `[sys.executable, <…>/tl.py, "nlm-auth-load"]` (không `--force`), cùng môi trường/timeout như trên. rc ≠ 0 và đầu ra chứa
     `TỪ CHỐI HẠ CẤP` ⇒ `TỪ CHỐI HẠ CẤP`; rc ≠ 0 khác ⇒ `KHÔNG ĐO ĐƯỢC — nlm-auth-load rc=<N>`. Không chuyển tiếp đầu ra của con.
   - **Kiểm lại**: rc 0 ⇒ chạy canary lần hai như trên. `alive is True` ⇒ nạp thành công; khác ⇒ `BUNDLE CŨNG CHẾT — laptop
     WP710 cần đăng nhập lại` (khi `alive is False`) hoặc `KHÔNG ĐO ĐƯỢC — canary sau nạp <lý do>`. Cập nhật `ket_qua` trong dấu.
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
   **giả** (hai lệnh `nlm-auth-status`, `nlm-auth-load`) và `nlm` **giả** trên `TL_NLM_BIN`; ba đồ giả dùng chung một tệp trạng
   thái `{jar: song|chet, bundle: song|chet|cu_hon}` — `nlm-auth-load` giả chỉ đổi `jar` thành `song` khi `bundle == "song"`, in
   `TỪ CHỐI HẠ CẤP` và rc 2 khi `cu_hon` — và ghi nhật ký mọi lời gọi (argv + giá trị `TL_NLM_NAP_LAI_TAT`). Đột biến chạy
   trên bản sao tạm của `nlm_cli.py`, không ghi tệp thật.
3. → `scripts/tl_test_fragments_bundled.py`: sinh lại bằng `tl_core.test_fragments.generate_bundled_module_bytes`.
4. → `references/RASOAT_HOSO_LOOP.md`: sau câu "CẤM tự `nlm-auth-load` …" ở §4b, thêm đúng một câu: *"Ngoại lệ duy nhất:
   cơ chế tự nạp có điều kiện bên trong `nlm_cli` ở phiên cloud (`ADR-0062`) — agent vẫn không tự gõ lệnh nạp."* Mọi chữ cũ giữ.
5. → `references/QUY_TRINH_RA_SOAT_3_TANG.md`: cùng câu ấy, nguyên văn, ở cuối gạch đầu dòng "Sửa xác thực". Mọi chữ cũ giữ.
6. → `docs/adr/0062-nlm-tu-nap-lai-co-dieu-kien-phien-cloud.md`: `Trạng thái: Accepted`; nêu nó **thay r208c ở đúng điểm "tự nạp
   khi hết hạn", chỉ cho phiên cloud**; tiền đề đã đổi (WP710 30 phút + canary trước stage của wp726; chốt chống hạ cấp còn);
   năm điều kiện (canary chết · chỉ `nlm_cred.enc` không `--force` · 1 lần/tiến trình + 10 phút · chỉ thử lại lệnh đọc · nạp xong
   vẫn chết ⇒ §4b); mục Cưỡng chế trỏ fragment `wp1099_nlm_nap_lai`.
7. → `docs/PROTOCOL_DA_PHIEN.md`: đúng 1 dòng mới trong bảng §20 cho `ADR-0062`, cột cổng = `wp1099_nlm_nap_lai (selftest
   fragment)`.
8. → `changelog.d/wp-1099.md`: mục tóm tắt theo khuôn các tệp `changelog.d/wp-*.md` sẵn có.
9. → `RELEASE_MANIFEST.json`: tái sinh sau mục 1, 3, 4, 5 (CLAUDE.md, Quy ước deploy mục 5).

## `nghiem_thu`

Mỗi tiêu chí kèm đột biến làm nó đổi màu (L3). Mọi ca A chạy `nlm_cli` bản THẬT đã chép vào cây tạm (import theo đường dẫn,
`HOME` tạm, `CLAUDE_CODE_REMOTE=true` trừ khi ca nói khác); đếm lời gọi bằng nhật ký của đồ giả.

| # | mục tiêu | tiêu chí | phép đo làm ĐỎ (đột biến) |
|---|---|---|---|
| A1 | 1 | `CLAUDE_CODE_REMOTE` vắng · `false` · có `TL_NLM_NAP_LAI_TAT=1` (ba ca riêng), `nlm` giả rc 1 + `Authentication expired` ⇒ `_run` trả đúng `(rc, out, err)` như bản base trên cùng đồ giả (so tuple), 0 lời gọi `tl.py`, stderr tiến trình không có `nlm_nap_lai:` | bỏ cổng `CLAUDE_CODE_REMOTE` ⇒ ĐỎ; bỏ cổng `TL_NLM_NAP_LAI_TAT` ⇒ ĐỎ |
| A2 | 1 | rc 1 không chứa chuỗi auth · rc 124 · rc 127 (ba ca) ⇒ 0 lời gọi `tl.py` | coi rc 124 là ứng viên ⇒ ĐỎ |
| A3 | 1 | jar chết, bundle sống, argv `source list NB -j` ⇒ nhật ký đúng thứ tự `nlm` → `tl nlm-auth-status` → `tl nlm-auth-load` → `tl nlm-auth-status` → `nlm`; `_run` trả rc 0 của lần chạy lại; stderr có đúng 1 dòng `nlm_nap_lai: ĐÃ NẠP, THỬ LẠI ĐẠT — …`; `source_list` trả dict có `nap_lai.trang_thai == "ĐÃ NẠP, THỬ LẠI ĐẠT"` | bỏ bước chạy lại ⇒ ĐỎ |
| A4 | 1 | mọi lời gọi `tl.py` trong nhật ký mang `TL_NLM_NAP_LAI_TAT=1`; `tl.py` giả của ca này gọi ngược `nlm_cli._run` với lỗi auth ⇒ tổng lời gọi `nlm-auth-load` = **1** (không đệ quy) | không đặt biến cho con ⇒ ĐỎ (đếm > 1 hoặc quá hạn) |
| A5 | 1 | canary trả `alive: true` · `alive: null` · JSON hỏng · con ngủ quá hạn (hạn đặt nhỏ qua tham số test) (bốn ca) ⇒ 0 lời gọi `nlm-auth-load`; trạng thái lần lượt `BỎ QUA — canary sống…`, `KHÔNG ĐO ĐƯỢC — canary …` ×3 | dùng `not alive` thay `alive is False` ⇒ ĐỎ ở ca `null` |
| A6 | 1 | bundle `chet` ⇒ 1 lời gọi `nlm-auth-load`, 0 lần chạy lại `nlm`, trạng thái `BUNDLE CŨNG CHẾT — …`, `_run` trả kết quả lần ĐẦU | chạy lại bất kể canary sau nạp ⇒ ĐỎ |
| A7 | 1 | bundle `cu_hon` ⇒ trạng thái `TỪ CHỐI HẠ CẤP`; argv của `nlm-auth-load` trong nhật ký không chứa `--force` (ở mọi ca A) | thêm `--force` ⇒ ĐỎ |
| A8 | 1 | argv `source add NB --url x` (lệnh ghi), jar chết, bundle sống ⇒ nạp 1 lần, `nlm` được gọi đúng **1** lần, trạng thái `ĐÃ NẠP, KHÔNG THỬ LẠI (lệnh ghi)`; argv `notebook query NB q -j` ⇒ có chạy lại | đổi danh sách cho phép thành danh sách cấm `(source,add)` ⇒ ĐỎ ở ca bổ sung `source sync` (phải KHÔNG thử lại) |
| A9 | 1 | hai lời gọi `_run` liên tiếp cùng tiến trình, jar vẫn chết sau lần nạp ⇒ lời gọi thứ hai: 0 lời gọi `tl.py`, `BỎ QUA — đã nạp …`; tiến trình MỚI với dấu `ts = now − 300` ⇒ `BỎ QUA`; dấu `ts = now − 700` ⇒ nạp; dấu `ts = now + 3600` ⇒ nạp; dấu là `[1]` ⇒ nạp (năm ca riêng) | đổi 600 thành 60 ⇒ ĐỎ ở ca −300; bỏ chốt đồng hồ lệch ⇒ ĐỎ ở ca +3600 |
| A10 | 1 | dấu được ghi TRƯỚC lời gọi `nlm-auth-load`: `tl.py` giả đọc tệp dấu lúc nhận `nlm-auth-load` và ghi vào nhật ký `dau_co=1`; quyền tệp 0600 (POSIX) | ghi dấu sau khi nạp ⇒ ĐỎ |
| A11 | 1 | mọi ca A: stderr tiến trình có ≤ 1 dòng `nlm_nap_lai:`; stdout và chuỗi `err` trả về không chứa `nlm_nap_lai:`; không chứa sentinel cookie mà `tl.py` giả in ra | chuyển tiếp đầu ra của con ⇒ ĐỎ |
| A12 | 1 | `AUTH_FIX_HINT`, `AUTH_FIX_HINT_SHORT`, `_AUTH_FIX_ORDER`, `_AUTH_FIX_RASOAT_CARVE` của head bằng base (so từng hằng, giá trị đọc từ `git show <base>:scripts/nlm_cli.py`) | sửa câu trừ ⇒ ĐỎ |
| D1 | 4, 5 | trên văn bản §4b của `RASOAT_HOSO_LOOP.md` và gạch "Sửa xác thực" của `QUY_TRINH_RA_SOAT_3_TANG.md`, đã gộp khoảng trắng theo đoạn (L6b): câu ngoại lệ ở mục tiêu 4 xuất hiện đúng 1 lần ở MỖI tệp (đếm riêng — L6c); vế âm trên base: 0 lần mỗi tệp; chuỗi `CẤM tự` và `nlm-auth-load` vẫn có ở mỗi tệp | xoá câu ở một tệp ⇒ ĐỎ |
| D2 | 6, 7 | `python .claude/dev/packet_loop.py adr-song --root .` rc 0; bảng §20 có đúng 1 dòng mà ô đầu là `ADR-0062` trong dấu nháy ngược, cùng dạng dòng `ADR-0060` sẵn có (vế âm trên base: 0) | xoá dòng §20 ⇒ `adr-song` ĐỎ |
| D3 | 6 | trên văn bản ADR đã gộp khoảng trắng theo đoạn: có `Trạng thái: Accepted`, `r208c`, `CLAUDE_CODE_REMOTE`, `nlm_cred.enc`, `--force`, `600`, `wp1099_nlm_nap_lai` (đếm từng cụm riêng) | xoá một cụm ⇒ ĐỎ |
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

Ghi chú L6. D1, D2 có vế dương trên head và vế âm trên base (L6a). D1, D3 đo trên văn bản đã gộp khoảng trắng theo đoạn (L6b).
D1 đếm từng tệp; D3, A1, A2, A5, A9 đếm từng ca/cụm riêng (L6c). Không có lời khai số lượng dạng chữ (L6d). Không có lời khai
"không cổng nào cưỡng chế" (L6e).

Chạy thử trên nền (02:2xZ 01-11, `90c101b8`): `rg -c "ADR-0062" docs/PROTOCOL_DA_PHIEN.md` ⇒ 0; `docs/adr/0062-*` vắng; câu
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
- **`nlm-auth-status` trong cây phát hành ra `alive` ba trạng thái**: đo trong mã (`nlm_ops.py:1398` khởi tạo `alive: None`),
  chưa đo trên phiên cloud LIVE.
- **Hai tiến trình cùng nạp trong cùng một giây**: tệp dấu không có khoá; cả hai có thể cùng qua bước "Giới hạn" và nạp hai lần.
  Hậu quả: hai lần ghi đè jar bằng cùng một bản. Chấp nhận ở r1.
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
