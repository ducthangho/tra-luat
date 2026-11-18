tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# HOAN-LOI-GOI-CODEX r1 — hoàn một lời gọi codex review khi launcher dừng TRƯỚC khi gọi `_phong`

- packet_id: HOAN-LOI-GOI-CODEX; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | #804 (chính); #177 đóng kèm khi land (quyết định Q1 của chủ kho, §9) |
| `nguon_cap_viec` | Chủ kho duyệt P4 "#177 + #804" trong đợt vá chỗ sót, phiên điều phối #1206 ngày 18-11-2026. P4 phải chờ #1342 r3 land vì cùng chạm `packet_loop.py`; r3 đã merge ở `aeb5cae`. #804 là nợ `wp775-no-launcher-evidence` (connector P1 trên PR #779). #177 là Packet Issue W0-R1B, mở từ 19-08, chưa ai cấp lease. |
| `review_class` | `sensitive`. Reviewer lượt 2 đo `_tinh_lop_tu_write_set` trên bốn tệp §1 ⇒ `sensitive`. Đối chiếu lại bằng `lease_publish check` khi cấp lease. |
| `base` | `aeb5cae0af01538c88ab2b50c27902dfaf7a7382` (`origin/master` lúc soạn). Lease ghi OID base thật lúc cấp. |

## 0. Hiện trạng (đo 2026-11-18 trên `aeb5cae`, Linux, Python 3.13.18; lượt soạn và hai lượt review)

Số dòng là số của blob trên base và sẽ trôi. Executor đo lại trên exact base của lease trước khi viết.

### 0.1 Ý chính của #177 đã được #775 giải quyết

- `cmd_record_review` (`.claude/dev/packet_loop.py:1180`), nhánh `_la_codex(st)` dòng 1223–1231, đòi `--codex-call` trỏ
  đúng một lời gọi đã `record-codex-call`, cùng head, chưa `da_dung`; thiếu ⇒ `RC_TRACE` (5). Review chỉ ghi khi đã tiêu
  một lời gọi; số lời gọi bị trần (`cmd_record_codex_call` 1339–1355, chặn trước ở 1349–1350); trần vòng ở `_xet_dung`
  (3195, 3203–3205).
- `case_pl_m3_neo_loi_goi` (`packet_loop_test.py:7671`) có vế `_rv(5, "approve", None)`: chuỗi phản chứng của #177 §2 ⇒ rc
  5. Tám ca `pl_m1_tran_so_duong`, `pl_m2_loi_goi`, `pl_m3_codex`, `pl_m3_neo_loi_goi`, `pl_m3_vong`,
  `void_run_cheo_luot_bi_chan`, `void_run_cu_khong_neo_co_thong_diep_rieng`, `void_run_that_dung_luot_duoc_tha` OK trong
  clone ghi được; reviewer lượt 1 (chỉ đọc) tái lập 6/8, hai ca `void_run_*` dừng ở probe ghi workspace (rc 15) — giới hạn
  nền chỉ đọc.
- #177 §8.4: "trần vòng cắn trước trần attempt" đã do ADR-0048/0052/0055 quyết định lại. "Lượt void vì quota không ăn
  vòng": `void-attempt` không chạy sau khi lượt có review (1090–1094) nên không ăn vòng, nhưng vẫn ăn **lời gọi codex**.
  Đó là #804.

### 0.2 #804: bộ đếm lời gọi chỉ dựa trên lời khai

- `cmd_record_codex_call` tăng `codex_review_calls_used` từ `--run-id`/`--head` tự khai. Hai ID bịa ⇒ rc 0, `used = 2`;
  ở trần mặc định 2 (`MAC_DINH_TRAN_CODEX`, dòng 64) lời gọi thứ ba rc 3. `void-codex-call --help` ⇒ argparse rc 2.
- Luật đếm (`docs/PROTOCOL_DA_PHIEN.md` §12 ~1173–1176, `ADR-0052` 11–15): lời gọi chỉ tính khi launcher có bằng chứng model
  đã bắt đầu sinh output/token. Mã hiện tính mọi lời gọi đã ghi.

### 0.3 Launcher: chỉ có bằng chứng DƯƠNG cho "chưa sinh con" ở điểm dừng trước `_phong`

- **Vắng khung không phải bằng chứng** (lượt 1 đo: con đóng stderr rồi in stdout, thoát 0 ⇒ bản ký `xong`,
  `model_phuc_vu=[]`, đúng chuỗi lý do không-khung; trace chỉ `response.output_text.delta` hay cụt cũng vậy).
- **`_phong` cũng không cho bằng chứng** (lượt 2 đo): `_phong` là wrapper trực tiếp của `Popen`. Trên POSIX, đóng pipe và
  đọc errpipe xảy ra SAU `_fork_exec`; lỗi exec (ENOENT) được báo từ tiến trình đã fork; `Popen` thật cho con chạy, thoát
  37, rồi bước dọn pipe ném `OSError` trong khi biến `p` của caller vẫn `None`. Trên Windows `Popen` đóng handle sau
  `CreateProcess` (chỉ đọc stdlib, chưa chạy). Nên mọi ngoại lệ từ `_phong` trở đi KHÔNG chứng minh được gì.
- **Điểm dừng trước `_phong` trong `lenh_run`, sau bước ghi sổ ký đầu (dòng ~2764):**
  - P2 `KeyboardInterrupt` khi chụp workspace trước (`_chup_an_toan`, dòng 2839–2845): `trang_thai="bi_ngat"`,
    `ly_do_dung="bi ngat trong luc chup workspace truoc; chua sinh con"`, return 130. Ca base `r1252_ngat_khi_chup`
    (`launcher_test.py:14093`) đạt.
  - P3 hạn chót hết TRONG lúc chụp (dòng 2846–2852): `trang_thai="hong"`, `Chan(MA_HAN)`. Ca base `r1252_han_sau_khi_chup`
    (`launcher_test.py:14132`) đạt. Hạn đã qua lúc gọi bị `chot_han` (dòng 1815) chặn TRƯỚC `_cap_id` ⇒ không có sổ ký.
  - Các điểm dừng khác trước `_phong` (prompt đổi sau băm, probe) hoặc không ký sổ (probe, dòng 2700–2715) hoặc không thuộc
    miền được hoàn. Probe `--version` tự sinh tiến trình; đối tượng chứng nhận là LỆNH REVIEW CHÍNH, không phải probe.
- Ký: có `--attempt-state` thì mọi `_ghi_so(thu_muc, ban_ghi, khoa_ky)` ký HMAC bằng `hmac_key` của state. Bản ghi mang
  `nonce`/`attempt` của neo (dòng 2754), `head` (`kq["head"]`), `agent_suy_ra`. HMAC chỉ bảo toàn vẹn **trong cùng
  principal** (docstring `launcher.py:105`).
- Chốt ghép: `launcher.py:2719` đòi `--attempt-state` ⇔ `--void-reason`; `--void-reason` (6115) chỉ nhận
  `infrastructure`/`permission`. Người tiêu thụ hiện có `_kiem_bang_chung_may` (`packet_loop.py:611`) đòi
  `void_reason == ly_do` cho mọi bản ghi có `trang_thai`/`run_id` (633–637).
- Một attempt có MỘT nonce cho mọi lần `launcher run`; nonce chỉ quay khi `begin-attempt`. (nonce, codex_call, head) không
  định danh duy nhất một lần thực thi.

### 0.4 Schema 3 (wp1174) và các đường đọc sổ

- `_load` (654) biết giao dịch v3 qua `_1174_TRANSACTION` (`tx`); đường thường (`tx is None`) đòi `schema_version == 2`,
  trước đó kiểm same-family (rc 4). Source-scoped v2 cũng có `tx` (`source=True`), có khoá riêng (`_1174_source_command`,
  6343).
- `_1174_state` (4803) đặt `tx` TRƯỚC khi gọi `_load`; mọi đường v3 đi qua đó: `_1174_adopt_payload` (4928, chiếu nguồn v2
  sang v3), `_reader_state` (1407, `status`/`next-comment`), khởi tạo `init`/`_1174_initial`, `_1174_diagnostic`, kiểm
  append-only (5414–5424), validation/review v3, `_1315_pending_recovery`. Lượt 2 đo trên base: adopt nguồn có mục mang khoá
  `hoan` bị từ chối ở full-state validation rc 8, nguồn giữ nguyên, không có target/witness; nguồn đối chứng qua
  (`completed_no_dispatch`), dùng `_adopt_fixture1174` (`packet_loop_test.py:11592`).

## 1. `write_set`

```
.claude/dev/packet_loop.py
.claude/dev/packet_loop_test.py
.claude/dev/launcher.py
.claude/dev/launcher_test.py
```

## 2. `ngoai_pham_vi`

- **Không hoàn lời gọi khi launcher đã gọi `_phong`**, bất kể kết quả (`_phong` ném, con thoát lỗi, stderr/stdout,
  `model_phuc_vu`). Lời gọi bị rate-limit/từ chối quyền sau đó vẫn tính; cửa duy nhất là `nang-tran`. Nợ có tên
  `wp804-post-spawn-unrefundable` (§7).
- Không đổi `record-codex-call` (giữ chỗ TRƯỚC lời gọi theo ID tự khai, ADR-0048), trần, `nang-tran`, `MAC_DINH_TRAN_*`.
- Không có cửa hoàn do người duyệt (Q2). Không chạm schema 3 / `_1174_*` / `_WP1174_*` / `WP1174_REQUIRED`; không thêm vào
  `_1174_MUTATORS` (Q3).
- Không đổi `void-attempt`, `_kiem_bang_chung_may`, `--void-reason` (vẫn hai giá trị), probe, `_loc_stderr_codex`,
  `_BoLocStderr`, `_phong`, hay việc thu dọn con khi bộ lọc/sandbox hỏng.
- Không đổi ranh giới tin cậy: HMAC và tệp claim (M1) chống sửa nhầm và khác lượt trong cùng principal; một principal ghi
  được thư mục state có thể dựng claim/ký lại — ngoài phạm vi, cùng giới hạn với `void-attempt` hiện nay.
- Không thêm khoá ghi cho state v2 legacy (`tx is None`); lệnh mới kế thừa giả định một-writer của mọi lệnh v2 legacy
  (§8). Source-scoped v2 có khoá và ngoài phạm vi.
- Không gỡ khả năng bịa run_id để tự đốt ngân sách (Q4; nợ `wp804-unverified-call-reservation`).
- Không viết lại #177 hay văn bản protocol.

## 3. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | `launcher.py run` thêm `--codex-call RUN_ID` (mẫu `RUN_ID_RE` của `packet_loop.py`, khai lại trong launcher, kiểm bằng `fullmatch`). Luật ghép: `--attempt-state` đòi ĐÚNG MỘT trong `--void-reason`/`--codex-call`; một trong hai mà thiếu `--attempt-state` ⇒ `Chan(MA_THAM_SO)`. Có `--codex-call`: **(a) kiểm reservation** khi đọc state (cạnh chỗ đọc neo, dòng ~2722): state có đúng một mục `codex_calls` với `run_id == RUN_ID`, `da_dung is False`, không có khoá `hoan`, `head == kq["head"]`; sai ⇒ `Chan(MA_THAM_SO)`. **(b) claim** — sau `_cap_id`, TRƯỚC `_ghi_so` đầu và trước `_phong`: thư mục `<thư mục chứa state>/<tên tệp state>.codex-claims/` tạo với quyền `0700` (POSIX), tệp `<sha256 hex của RUN_ID nguyên văn UTF-8>.json` tạo nguyên tử `O_CREAT\|O_EXCL\|O_WRONLY`, quyền `0600`, nội dung `{"codex_call": RUN_ID, "launcher_run_id": rid, "nonce", "attempt"}`, `fsync` rồi đóng. Tệp đã tồn tại, hay bất kỳ lỗi tạo/ghi/đóng ⇒ `Chan(MA_THAM_SO)`, không `_phong`, không bản ghi nào mang trường (d). Claim đã tồn tại (kể cả ghi dở, kể cả từ attempt trước) giữ chỗ vĩnh viễn cho ID ấy. **(c)** bản ghi mang `codex_call=RUN_ID` cạnh `nonce`/`attempt`, không mang `void_reason`. **(d)** đúng hai điểm P2, P3 của §0.3 ghi thêm trường ký `chua_sinh_con` = `"ngat_chup"` (P2) hoặc `"han_chup"` (P3); không điểm nào khác ghi trường này. Mọi đường không có `--codex-call` giữ nguyên byte bản ghi (trừ trường biến động). | `.claude/dev/launcher.py` |
| M2 | `launcher.py` khai hằng `CHUNG_NHAN_CHUA_SINH_CON = frozenset({("ngat_chup","bi_ngat"), ("han_chup","hong")})` và hàm `ten_tep_claim(run_id) -> str` (sha256 hex + `.json`); M1(b) dùng hàm này. | `.claude/dev/launcher.py` |
| M3 | `packet_loop.py` thêm `void-codex-call --packet N --run-id ID --bang-chung RUN_JSON` (`cmd_void_codex_call`), import `CHUNG_NHAN_CHUA_SINH_CON`, `ten_tep_claim` cùng `ky_ban_ghi_luot` (dòng 54). Theo thứ tự, mỗi chốt một mã và một lý do riêng in ra: (1) `_la_codex(st)`, sai ⇒ `RC_PROVIDER`; (2a) `state == "reviewing"`, sai ⇒ `RC_STATE`; (2b) `attempt_open is True`, `attempt_anchor` có và `consumed is False`, sai ⇒ `RC_STATE`; (3) đúng một mục `codex_calls` có `run_id`, sai ⇒ `RC_TRACE` "không có lời gọi"; (4) mục `da_dung is False`, sai ⇒ `RC_TRACE`; (5) mục không có `hoan`, sai ⇒ `RC_TRACE`; (6a) đọc bytes, `json.loads(object_pairs_hook=_cam_khoa_trung)`, là `dict`, sai ⇒ `RC_MOI_TRUONG` "bằng chứng không đọc được"; (6b) các khoá `nonce`,`attempt`,`chu_ky`,`run_id`,`codex_call`,`head`,`agent_suy_ra`,`trang_thai`,`pid` có mặt, đúng kiểu (`str`/`int`/`None` theo launcher), sai ⇒ `RC_MOI_TRUONG`; (6c) `nonce == anchor.nonce`; (6d) `attempt == anchor.attempt`; (6e) `hmac.compare_digest(chu_ky, ky_ban_ghi_luot(d, st["hmac_key"]))` (khoá hỏng ⇒ cùng lý do); (7a) `codex_call == run_id`; (7b) `head == mục.head`; (7c) `agent_suy_ra == "codex"`; (7d) `"void_reason" not in d`; (8) `(d.get("chua_sinh_con"), d["trang_thai"]) in CHUNG_NHAN_CHUA_SINH_CON` và `d["pid"] is None`; (9) tệp `ten_tep_claim(run_id)` trong thư mục claim của state: tồn tại, JSON object đúng bốn khoá, `codex_call == run_id`, `launcher_run_id == d["run_id"]`, `nonce`/`attempt` khớp neo. (6c)–(9) sai ⇒ `RC_MOI_TRUONG`, mỗi vế một lý do. Đạt cả: mục nhận `hoan: True`, `codex_review_calls_used -= 1`, nối `history` `{"event": "void_codex_call", "run_id", "launcher_run_id": d["run_id"], "chua_sinh_con": d["chua_sinh_con"]}`, `_save` đúng MỘT lần, rc 0. Từ chối ⇒ 0 lần `_save`. | `.claude/dev/packet_loop.py` |
| M4 | Sổ: (a) `_load` vế `loi-goi` nhận dạng bốn khoá `{"run_id","head","da_dung","hoan"}` **chỉ khi `tx is None`**, `hoan is True`, `da_dung is False`; dạng ba khoá cũ vẫn hợp lệ; khi `tx` khác None (v3, adopt, source-scoped) mục có khoá `hoan` ⇒ vi phạm `loi-goi`. (b) `dem-goi`: `run_id` duy nhất trên TOÀN sổ (kể cả mục đã hoàn); với `A` = số mục không hoàn, `U` = số mục không hoàn và chưa dùng, `C` = `can_duoi`: `used >= A` và `used >= C + U`, hai phần tử riêng trong `vi_pham`. (c) `cmd_record_review` từ chối `--codex-call` trỏ mục đã hoàn ⇒ `RC_TRACE`, trước `_xet_dung`. (d) `cmd_record_codex_call` vẫn từ chối mọi `run_id` đã có trong sổ, kể cả mục đã hoàn. | `.claude/dev/packet_loop.py` |
| M5 | Parser `void-codex-call` ba tham số bắt buộc; `--run-id` kiểm `RUN_ID_RE.fullmatch` (không nhận newline cuối) trước khi tra sổ, sai ⇒ `RC_ARG` lý do riêng. Không thêm vào `_1174_MUTATORS`. | `.claude/dev/packet_loop.py` |
| M6 | Ca `r804_*` trong `packet_loop_test.py` theo §4b. Ca dương và ca âm chính dựng bằng **launcher thật** (P2 theo fixture `r1252_ngat_khi_chup`, P3 theo `r1252_han_sau_khi_chup`, probe offline đạt). Ca đo MỘT vế dùng helper ký fixture `ky_ban_ghi_luot(d, key)` trên bản ghi launcher thật đã sửa ĐÚNG một trường — chỉ helper này được dựng chữ ký. Đột biến D của §4b. | `.claude/dev/packet_loop_test.py` |
| M7 | Ca `r804_l_*` trong `launcher_test.py`: (a) `--codex-call` thiếu `--attempt-state` ⇒ `MA_THAM_SO`; (b) CẢ `--void-reason` và `--codex-call` ⇒ `MA_THAM_SO`; (c) `--attempt-state` một mình ⇒ `MA_THAM_SO`; (d) `--codex-call "a b"`, `"x\n"` ⇒ `MA_THAM_SO`; (e) reservation vắng / đã dùng / đã hoàn / head khác / state sai packet ⇒ `MA_THAM_SO`, không thư mục claim mới, không `_phong` (đếm bằng monkeypatch); (f) P2 thật ⇒ bản ký `codex_call`, `chua_sinh_con="ngat_chup"`, `trang_thai="bi_ngat"`, `pid` None, không `void_reason`, claim đúng bốn khoá, tên = sha256, quyền `0600`/`0700` (POSIX); (g) P3 thật ⇒ `"han_chup"`/`"hong"`; (h) `_phong` thật ném (tiêm lỗi ở bước dọn pipe sau khi con đã chạy, và lệnh không tồn tại với probe đạt) ⇒ KHÔNG có `chua_sinh_con`; (i) lượt codex giả thoát 1 ⇒ không `chua_sinh_con`; (j) chạy lần hai cùng `--codex-call` ⇒ `MA_THAM_SO`, claim giữ nguyên byte, không bản ghi mang `chua_sinh_con`; hai launcher tranh cùng ID (luồng song song) ⇒ đúng một claim; (k) lỗi I/O khi tạo claim (thư mục chỉ đọc, hoặc tiêm `OSError` vào `os.open`) ⇒ `MA_THAM_SO`, không `_phong`; (l) đường `--void-reason` cũ: projection bản ghi (bỏ `run_id`,`short_id`, mốc giờ, `chu_ky`, `pid`) bằng projection base cùng lệnh; `void-attempt --bang-chung` trên bản ghi `--codex-call` thật ⇒ từ chối. Đột biến L của §4b. | `.claude/dev/launcher_test.py` |
| M8 | Mẫu đột biến `(tìm, thay)` lấy nguyên văn mã đã viết, khớp đúng một chỗ; `t117_moi_mau_dot_bien_phai_khop_DUNG_MOT_cho` và kiểm khớp-một-chỗ của `packet_loop_test.py` vẫn xanh. | `.claude/dev/launcher_test.py`, `.claude/dev/packet_loop_test.py` |

## 4. `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | Phản chứng #804 trên H: `record-codex-call` → `launcher run --codex-call` dừng ở P3 (launcher thật) → `void-codex-call` ⇒ rc 0; đọc lại sổ: `used` giảm đúng 1, mục `hoan: True`, đúng một sự kiện `void_codex_call` mang `launcher_run_id` của bản ghi; đếm `_save` = 1. Lặp với P2. Đối chứng âm riêng: base `void-codex-call --help` ⇒ argparse rc 2. | Bỏ `-= 1` ⇒ `r804_hoan_tru_bo_dem` ĐỎ; bỏ `hoan` ⇒ `r804_hoan_danh_dau` ĐỎ; bỏ nối history ⇒ `r804_hoan_ghi_history` ĐỎ. |
| N2 | Mỗi đột biến §4b: ca đích ĐỎ tại assertion của chính ca ấy với rc và lý do mong đợi (không traceback, không lỗi fixture). Ghi bảng tập-ID-đỏ cho từng đột biến (cả D lẫn L); hai chốt khác nhau có tập-ID-đỏ khác nhau, trừ cặp đã khai tương đương ở §4b. | Gỡ từng chốt ⇒ đúng ca đích ĐỎ với đúng lý do. |
| N3 | Ghim tập ID ca base theo OS. `packet_loop_test.py` và `launcher_test.py` trên H: tập ID H = tập ID base ∪ manifest `r804_*`; mọi ID base giữ cùng trạng thái `passed`/`skipped`; các nhóm `pl_m*`, `void_*`, `void_run_*`, `wp1174_writer_*`, `wp1174_race_*` (packet_loop) và đúng ID `t117_moi_mau_dot_bien_phai_khop_DUNG_MOT_cho`, `r1252_ngat_khi_chup`, `r1252_han_sau_khi_chup` (launcher) mỗi nhóm khớp ≥1 ID trên base và tất cả `passed` trên H. | Một ID base `passed` mà H khác; một ID base biến mất; một nhóm khớp 0 trên H. |
| N4 | Bộ đột biến hai tệp trên Linux: tập tên mutant theo nhóm `giet`/`song`/`loi`/`bo_qua`/`khong_do_duoc`; mọi mutant mới `giet`; tập `khong_do_duoc` kế thừa bằng base (liệt kê tên). | Ép một mutant mới thành `bo_qua` ⇒ bộ tổng hợp phải ĐỎ. |
| N5 | Exact head: `ruff check --no-cache --select F` delta so base = 0 trên bốn tệp (base: rc 1, 21 chẩn đoán); `doctrine-scan` rc 0 kèm dòng kết luận dương; `adr-song` rc 0 kèm số khớp bằng số ADR của base (lượt 2 đo 66/66); `git diff --check base..H` sạch; `git diff --numstat base..H` đúng 4 tệp §1, tổng thêm ≤ 450. | Tên chưa định nghĩa ⇒ delta ≠ 0; tệp thứ năm ⇒ 5 tệp; khoảng trắng cuối dòng ⇒ `diff --check` ĐỎ; numstat 451 ⇒ ĐỎ. `doctrine-scan`/`adr-song` không có phản chứng riêng ở packet này — khai thẳng. |
| N6 | `launcher.py doctor --json` trên H với cùng fixture probe offline như base: rc bằng base, cùng tập khoá top-level, cùng tập probe đã chạy. | rc khác, hoặc thiếu khoá/probe so base. |

### 4b. Đường vào và chốt, mỗi đường một ca và một đột biến

Đường đọc/ghi sổ lời gọi trên base, đã liệt kê: ghi `cmd_record_codex_call`; đọc + `da_dung` `cmd_record_review`; bất biến
`_load` (`loi-goi`, `dem-goi`, `can_duoi`, cả khi `tx` khác None); đổi neo `void-attempt`/`begin-attempt`; đổi trần/state
`nang-tran`/`record-rescue`/`_xet_dung`/`_vao_rescue`; các đường v3 của §0.4 (`_1174_state`, `_1174_adopt_payload`,
`_reader_state`, `init`/`_1174_initial`, `_1174_diagnostic`, append-only 5414–5424, validation/review v3,
`_1315_pending_recovery`) — **giữ nguyên**, chỉ bị ảnh hưởng qua M4(a) và bị khoá bởi D15; và hai đường mới (launcher M1,
lệnh M3). Executor thấy thêm một đường đọc/ghi `codex_calls`/`codex_review_calls_used` ngoài danh sách này ⇒ dừng,
revision (§6).

| # | đường / chốt | ca đích | đột biến |
|---|---|---|---|
| D1 | reviewer không phải codex | `r804_tu_choi_reviewer_khac` | bỏ (1) |
| D2a | state ≠ reviewing (`blocked` sau vượt trần; `running` sau `void-attempt`) | `r804_tu_choi_ngoai_reviewing` | bỏ (2a) |
| D2b | `reviewing` nhưng neo consumed / `attempt_open` False / neo vắng (fixture sửa đúng một trường state, `_load` vẫn nhận) | `r804_tu_choi_neo_dong` (ba vế) | bỏ (2b) |
| D3 | ID vắng trong sổ, kèm bằng chứng + claim hợp lệ cho ID ấy và một mục mồi cùng head | `r804_tu_choi_goi_khong_co` (assert lý do "không có lời gọi") | tra sang mục đầu |
| D4 | mục `da_dung` | `r804_tu_choi_da_dung` | bỏ (4) |
| D5 | hoàn hai lần | `r804_tu_choi_hoan_hai_lan` | bỏ (5) |
| D6a | JSON hỏng / mảng / trùng khoá | `r804_tu_choi_json_hong` (ba vế) | bỏ `_cam_khoa_trung` ⇒ vế trùng khoá ĐỎ; bỏ kiểm `dict` ⇒ vế mảng ĐỎ |
| D6b | thiếu khoá / sai kiểu (fixture ký) | `r804_tu_choi_khoa_kieu` | bỏ (6b) |
| D6c | nonce lượt khác, chữ ký HỢP LỆ (ký thật lượt 1, dùng lượt 2) | `r804_tu_choi_cheo_luot` | bỏ (6c) |
| D6d | `attempt` khác, nonce đúng (fixture ký) | `r804_tu_choi_attempt_khac` | bỏ (6d) |
| D6e | chữ ký sai (sửa một trường không phải neo sau khi ký); `hmac_key` state đổi sau khi ký | `r804_tu_choi_chu_ky` (hai vế) | `compare_digest` → `True` (hai vế dùng chung mutant: khai tương đương, cả hai assert lý do chữ ký) |
| D7a | `codex_call` ≠ `--run-id` (fixture ký) | `r804_tu_choi_ban_ghi_goi_khac` | bỏ (7a) |
| D7b | `head` ≠ head của mục (launcher thật ở worktree head khác; reservation ghi head đó trước, rồi so với mục khác — fixture ký nếu M1(a) chặn) | `r804_tu_choi_head_khac` | bỏ (7b) |
| D7c | `agent_suy_ra` ≠ codex (fixture ký) | `r804_tu_choi_khong_phai_codex` | bỏ (7c) |
| D7d | có `void_reason` (fixture ký) | `r804_tu_choi_co_void_reason` | bỏ (7d) |
| D8a | bản ký `bi_ngat`/`pid=None` THIẾU `chua_sinh_con` (fixture xoá đúng trường) | `r804_tu_choi_thieu_chung_nhan` | coi thiếu trường là `"ngat_chup"` |
| D8b | cặp chéo `("ngat_chup","hong")` (fixture ký) | `r804_tu_choi_cap_cheo` | so trường riêng lẻ thay cặp |
| D8c | `pid` khác None (fixture ký) | `r804_tu_choi_co_pid` | bỏ vế `pid is None` |
| D8d | giá trị lạ `"ngat_chup "`, `"Ngat_chup"`, `"phong"` (fixture ký) | `r804_tu_choi_gia_tri_la` | so `strip()`/`lower()`; thêm `("phong","hong")` vào tập (đột biến NỚI) |
| D8e | bản ghi trung gian `dang_chay` (lần `_ghi_so` đầu, ký thật) | `r804_tu_choi_trung_gian` | thêm `dang_chay` vào tập |
| D8f | bản ghi sau `_phong` (M7 h, i: ký thật, không trường) | `r804_tu_choi_sau_phong` | (đột biến launcher L-h: ghi trường ở nhánh `_phong` ném) |
| D9a | dương P3 | `r804_hoan_tru_bo_dem`, `r804_hoan_danh_dau`, `r804_hoan_ghi_history` | xem N1 |
| D9b | dương P2 | `r804_hoan_ngat_chup` | bỏ bộ P2 khỏi tập |
| D9c | dương P3 riêng tập | `r804_hoan_han_chup` | bỏ bộ P3 khỏi tập |
| D10a | claim vắng (bản ghi thật, xoá tệp claim) | `r804_tu_choi_claim_vang` | bỏ (9) có mặt |
| D10b | claim của lần chạy khác (claim tay mang `launcher_run_id` khác, bốn khoá đúng) | `r804_tu_choi_claim_lan_khac` | bỏ so `launcher_run_id` |
| D10c | claim sai khoá / thừa khoá / nonce khác | `r804_tu_choi_claim_hong` (ba vế) | bỏ kiểm khoá; bỏ so nonce claim |
| D11 | `record-review` với lời gọi đã hoàn, mọi tiền điều kiện khác của `record-review` đạt | `r804_review_tu_choi_goi_da_hoan` | bỏ M4(c) |
| D12 | `record-codex-call` dùng lại run_id đã hoàn | `r804_khong_tai_dung_run_id` | kiểm trùng chỉ xét mục chưa hoàn |
| D13a | `_load` nhận: hoàn một rồi ghi tiếp; hoàn hết; từ chối trùng ID giữa hai mục đã hoàn | `r804_load_nhan_so_hoan`, `r804_load_trung_id_hoan` | tính duy nhất chỉ trên mục chưa hoàn |
| D13b | `_load` từ chối `hoan: False`, `hoan` kèm `da_dung: True`, khoá thứ năm | `r804_load_dang_muc_sai` | nới M4(a) |
| D13c | witness `A=2,C=0,U=0,used=1` ⇒ từ chối | `r804_load_can_a` | bỏ `used >= A` |
| D13d | witness `A=1,C=2,U=1,used=2` ⇒ từ chối; `used > A`, hai cận đạt, state suy từ v1 ⇒ NHẬN | `r804_load_can_cu` | bỏ `used >= C + U` |
| D14 | đếm `_save`: 0 ở mọi ca D1–D10c, 1 ở D9a | gộp | gọi `_save` một lần trước (9) ⇒ D10a ĐỎ; gọi hai lần ở nhánh thành công ⇒ D9a ĐỎ |
| D15a | v3: lệnh mới trên state v3 hợp lệ (fixture wp1174) ⇒ từ chối với lỗi vế `schema` (hoặc same-family rc 4, ghi rõ cái nào), byte không đổi | `r804_v3_lenh_moi_tu_choi` | nới vế `schema` cho `void-codex-call` |
| D15b | adopt hai nguồn v2 tương đương qua `_adopt_fixture1174`, chỉ một có mục `hoan` hợp lệ ⇒ nguồn `hoan` bị từ chối ở full-state validation trước prepared/target/tombstone, nguồn đối chứng `completed_no_dispatch` | `r804_v3_adopt_tu_choi_hoan` | bỏ điều kiện `tx is None` của M4(a) |
| D16 | `--run-id` sai dạng (gồm newline cuối) | `r804_tu_choi_run_id_sai_dang` | `fullmatch` → `match` |
| D17 | chuỗi: hoàn → ghi tiếp → review lời gọi còn hiệu lực ⇒ rc 0, bộ đếm đúng; chạm trần (reviewing) → hoàn → ghi thêm được một; sổ chạm trần có reservation + claim + attempt mở: `nang-tran` → `record-rescue` (state `running`) → hoàn ⇒ `RC_STATE`; `transition reviewing` đúng head, neo còn hiệu lực → hoàn ⇒ rc 0, `used` giảm 1, limit mới giữ | `r804_chuoi_tuong_tac` (ba vế) | (khoá thứ tự; tập-ID đỏ của bỏ `-= 1` và bỏ (2a) phải chứa ca này) |
| L-a…L-l | launcher M7 (a)–(l) | `r804_l_a` … `r804_l_l` | mỗi chốt ghép tham số một đột biến; bỏ kiểm reservation (từng vế); bỏ `O_EXCL`; tên claim = ID thô; bỏ `fsync`/quyền (POSIX); ghi `chua_sinh_con` ở nhánh `_phong` ném ⇒ L-h ĐỎ; ghi ở nhánh thường sau spawn ⇒ L-i ĐỎ; bỏ `codex_call` khỏi bản ghi ⇒ L-f ĐỎ |

## 5. `pham_vi_e`

Không chạm E4, không chạm E5. Packet thêm một cửa hoàn ngân sách có bằng chứng máy; không đổi quyền, không đổi trần.

## 6. `luat_dung`

- Trần lời gọi Codex theo dòng khai `ADR-0055`. Chạm trần ⇒ Review Rescue Checkpoint. Xin tăng là **E2**.
- Dừng triển khai, đi revision đặc tả khi:
  - cần sửa ngoài write set;
  - thấy đường đọc/ghi `codex_calls`/`codex_review_calls_used` ngoài danh sách §4b;
  - mã §0 trên exact base khác hành vi đã đo, đặc biệt: P2/P3 không còn nằm trước `_phong`, hoặc một đường được phép cấp
    chứng nhận có thể gọi `_phong` trước khi ký; adopt ghi gì đó TRƯỚC khi gọi `_1174_state`;
  - không dựng được D15b bằng fixture sẵn có (không hạ D15b thành kiểm vế `schema`);
  - `numstat` vượt 450 dòng thêm. Khi đó tách: (A) launcher M1 + M2 + M7 (+ L); (B) `packet_loop` M3–M6 (+ D). B phụ thuộc
    hợp đồng của A (trường `chua_sinh_con`, `CHUNG_NHAN_CHUA_SINH_CON`, `ten_tep_claim`, nội dung claim).
- Đặc tả không thuộc Mission, nên chờ chủ kho duyệt băm theo `ADR-0067`: **E2**.

## 7. `hinh_dang_ke_thua`

`khong_ap_dung`: packet thêm cửa hoàn mới, không vá lại một bản vá cũ, dù khép nợ `wp775-no-launcher-evidence`.

Nợ giữ lại, có tên, dẫn lại khi đóng #804/#177:
- `wp804-unverified-call-reservation` (Q4): `record-codex-call` tiếp tục giữ chỗ theo ID tự khai; hai ID bịa ở trần mặc
  định chiếm hết ngân sách. Đóng hẳn cần đổi ADR-0048.
- `wp804-post-spawn-unrefundable`: mọi lời gọi đã qua `_phong` không hoàn được, kể cả khi chết trước output (429, từ chối
  quyền, `_phong` ném sau fork). Cần tín hiệu dương từ transport codex buộc vào đúng request.

## 8. `chua_do_duoc`

- Kích thước ước tĩnh, chưa vá thử: `launcher.py` ~45 (tham số, kiểm reservation, claim, hai điểm ghi trường, hằng, hàm
  tên), `packet_loop.py` ~75, `launcher_test.py` ~120, `packet_loop_test.py` ~210 (dùng chung helper ký fixture, ca nhiều vế
  theo bảng); tổng ~450 — CHẠM trần. Lượt 2 đánh giá biên 10 dòng khó giữ. Executor đo `numstat` ngay sau khi xong phần
  launcher (A); nếu A + ước lượng B > 450 thì áp §6 tách TRƯỚC khi viết B.
- Giá trị thực dụng thấp: chỉ hai điểm dừng (ngắt khi chụp, hạn hết trong lúc chụp) được hoàn; phần lớn lỗi quota/quyền
  xảy ra sau `_phong` và vẫn không hoàn được (§2, §7). Packet chủ yếu dựng hạ tầng (claim, chứng nhận ký, lệnh hoàn, bất
  biến sổ) cho packet sau khi có tín hiệu dương.
- Không cổng nào cưỡng chế một-writer trên state v2 legacy (`tx is None`); hai `void-codex-call` song song đọc cùng ảnh thì
  ghi sau thắng: mất một cập nhật, không hoàn kép. Không dùng làm tiêu chí nghiệm thu.
- Windows: `O_EXCL` trên NTFS cục bộ, quyền `0600`/`0700` không áp dụng (ca quyền chỉ chạy POSIX, khai `bo_qua` có tên);
  hành vi `_phong`/`CreateProcess` chỉ đọc stdlib, chưa chạy. Không đo native Windows trong packet này.
- Mốc N/N và tập bỏ qua của hai suite trên base chưa ghim; executor ghim trên exact base của lease.

## 9. Quyết định của chủ kho (2026-11-18, phiên điều phối #1206, qua AskUserQuestion)

- **Q1 — có.** Đóng #177 cùng packet; comment trỏ §0.1 và các ca `pl_m3_neo_loi_goi`, `r804_*`.
- **Q2 — không.** Không thêm cửa hoàn do người duyệt; `nang-tran` là cửa có người duyệt.
- **Q3 — có.** Giữ schema 3 ngoài phạm vi, fail-closed (D15a/D15b khoá).
- **Q4 — có.** Chỉ chặn hướng "hoàn không bằng chứng"; vế "run_id bịa đốt ngân sách" là nợ
  `wp804-unverified-call-reservation`, không đổi ADR-0048 trong packet này.

## 10. Nhật ký thay đổi theo lượt review

- **Lượt 1 → bản 2** (Codex, request_changes, 4 P1 + 4 P2 + 1 P3): bỏ dạng "vắng khung"; thay dạng (A) bằng trường ký
  `chua_sinh_con` ở ba điểm control-flow; thêm tệp claim `O_EXCL` và chốt (9); `hoan` chỉ khi `tx is None`; tách đột biến
  theo vế; thêm D2b, D6a, D17; nợ có tên ở §7; hai witness D13; N3/N4 so tập; N5 phản chứng; N6 `doctor --json`; §8 ~440.
- **Lượt 2 → bản 3** (Codex, request_changes, 1 P1 + 5 P2 + 1 P3): bỏ P1 `("phong","hong")` — `_phong` ném có thể sau
  fork; chỉ còn P2/P3 trước `_phong`, N1 dùng P3 (P1); launcher kiểm reservation (đúng packet, ID, chưa dùng/hoàn, head)
  TRƯỚC claim, tên claim = sha256 của ID, quyền `0700`/`0600`, `fsync`, mọi lỗi I/O ⇒ `MA_THAM_SO` không `_phong`, ca
  tranh đồng thời/I/O/sai packet (P2 claim); P3 dùng fixture hạn hết TRONG lúc chụp, ca `_phong` ném là đối chứng không
  ký, đối tượng chứng nhận là lệnh chính (P2 điểm dừng); tách (2a)/(2b), D3 kèm bằng chứng + claim và assert lý do, D6 tách
  parser/kiểu/nonce/attempt/chữ ký, D8a fixture thiếu trường, D8e `dang_chay` riêng, D11 qua đủ tiền điều kiện, D15a assert
  vế lỗi, D14 đếm `_save` ở ca thành công (P2 ma trận); D17 thêm bước `transition reviewing` sau rescue (P2 D17); N3 dùng ID
  thật `void_*`, `t117_moi_mau_…`, ghim theo OS (P2 N3); §4b liệt kê đủ đường v3 đánh dấu giữ nguyên, một-writer chỉ cho v2
  legacy (P3); M2 tách hằng/hàm sang launcher, M8 theo tệp (L2); §8 ước ~450, tách sớm khi đo A.
