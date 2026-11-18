tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# HOAN-LOI-GOI-CODEX r1 — hoàn một lời gọi codex review khi launcher chứng minh CHƯA SINH tiến trình con

- packet_id: HOAN-LOI-GOI-CODEX; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | #804 (chính); #177 đóng kèm khi land (quyết định Q1 của chủ kho, §9) |
| `nguon_cap_viec` | Chủ kho duyệt P4 "#177 + #804" trong đợt vá chỗ sót, phiên điều phối #1206 ngày 18-11-2026. P4 phải chờ #1342 r3 land vì cùng chạm `packet_loop.py`; r3 đã merge ở `aeb5cae`. #804 là nợ `wp775-no-launcher-evidence` (connector P1 trên PR #779). #177 là Packet Issue W0-R1B, mở từ 19-08, chưa ai cấp lease. |
| `review_class` | `sensitive`: cả bốn tệp trong write set nằm dưới `.claude/dev/`. Đối chiếu bằng `lease_publish check` khi cấp lease; lớp chưa đo lại trong lượt soạn này (§8). |
| `base` | `aeb5cae0af01538c88ab2b50c27902dfaf7a7382` (`origin/master` lúc soạn). Lease ghi OID base thật lúc cấp. |

## 0. Hiện trạng (đo 2026-11-18T14:20Z–15:30Z trên `aeb5cae`, Linux, Python 3.13.18, clone riêng trong scratchpad)

Số dòng là số của blob trên base và sẽ trôi. Executor phải đo lại trên exact base của lease trước khi viết.

### 0.1 Ý chính của #177 đã được #775 giải quyết

#177 mục 2: `record-review` không đọc sổ lời gọi, nên bỏ qua `record-review-call` mà vẫn khép đủ vòng review. Trên base,
lỗ đó đã đóng:

- `cmd_record_review` (`.claude/dev/packet_loop.py:1180`) có nhánh `_la_codex(st)` ở dòng 1223–1231. Nhánh này đòi
  `--codex-call` trỏ tới đúng một lời gọi đã `record-codex-call`, cùng head, chưa neo review nào (`da_dung`). Thiếu thì
  `RC_TRACE` (5).
- Review chỉ được ghi khi đã tiêu một lời gọi, nên số vòng không vượt số lời gọi, và số lời gọi bị trần
  (`cmd_record_codex_call` ở dòng 1339–1355; chặn TRƯỚC ở 1349–1350). Trần vòng riêng có ở `_xet_dung` (dòng 3195), dòng
  3203–3205.
- Đo được (lúc soạn, clone ghi được): tám ca `pl_m1_tran_so_duong`, `pl_m2_loi_goi`, `pl_m3_codex`, `pl_m3_neo_loi_goi`,
  `pl_m3_vong`, `void_run_cheo_luot_bi_chan`, `void_run_cu_khong_neo_co_thong_diep_rieng`,
  `void_run_that_dung_luot_duoc_tha` OK. Reviewer lượt 1 (checkout chỉ đọc) tái lập 6/8: hai ca `void_run_*` dừng ở probe
  ghi workspace của launcher (rc 15), tức giới hạn của nền chỉ đọc, không phải hành vi. `case_pl_m3_neo_loi_goi`
  (`packet_loop_test.py:7671`) có vế `_rv(5, "approve", None)`: chính chuỗi phản chứng của #177 §2 ⇒ rc 5.
- #177 §8.4 còn hai câu: "trần vòng cắn trước trần attempt" đã do ADR-0048/0052/0055 quyết định lại. "Lượt void vì quota
  không ăn vòng": `void-attempt` không chạy được sau khi lượt đã có review (dòng 1090–1094), nên không ăn vòng. Nhưng nó
  vẫn ăn **lời gọi codex**, vì không có đường hoàn lời gọi. Đó là #804.

### 0.2 #804: bộ đếm lời gọi chỉ dựa trên lời khai

- `cmd_record_codex_call` (dòng 1339) tăng `codex_review_calls_used` từ `--run-id`/`--head` do người gọi khai, không đọc
  hiện vật launcher. Hai run_id bịa ⇒ cả hai rc 0, `used = 2`; ở trần mặc định 2 (`MAC_DINH_TRAN_CODEX`, dòng 64) lời gọi
  thứ ba rc 3. Reviewer lượt 1 tái lập đúng.
- `void-codex-call` không tồn tại: argparse rc 2.
- Luật đếm: `docs/PROTOCOL_DA_PHIEN.md` §12 (khoảng 1173–1176) và `ADR-0052` dòng 11–15: một lời gọi chỉ tính khi launcher
  có bằng chứng model đã bắt đầu sinh output/token. Mã hiện tính mọi lời gọi đã ghi.

### 0.3 Launcher: cái gì là bằng chứng DƯƠNG, cái gì không

- **Vắng khung KHÔNG phải bằng chứng.** `_ket_luan_model` (dòng 2199–2214) trả chuỗi lý do "không thấy khung" khi bộ lọc
  stderr không nhận diện được khung `response.created/completed`. Reviewer lượt 1 đo được: con đóng stderr sớm rồi in
  output ra stdout, thoát 0 ⇒ bản ghi ký hợp lệ, `trang_thai=xong`, `model_phuc_vu=[]`, đúng chuỗi ấy. Trace chỉ có
  `response.output_text.delta`, hoặc cụt ở `response.crea`, cũng ra đúng chuỗi ấy. Vì vậy packet này **không** hoàn bất
  kỳ lời gọi nào đã sinh tiến trình con (§2).
- **Điểm launcher BIẾT chắc chưa sinh con** (control flow, không suy từ quan sát), trong `lenh_run` sau bước ghi sổ đầu:
  - P1 `_phong(...)` (dòng ~2857) tự ném `OSError`/`ValueError`. Khối `try` hiện bao cả `_BoLocStderr`, `_LayMauSandbox`
    sau `_phong`; reviewer lượt 1 tiêm lỗi vào constructor bộ lọc sau khi con đã in output và nhận cùng bản ghi `hong`,
    `pid=None`, `khong chay duoc lenh: …`. Nên `pid is None` và chuỗi lý do KHÔNG phân biệt được P1 với lỗi sau spawn.
  - P2 `KeyboardInterrupt` khi chụp workspace trước (dòng 2839–2845): `trang_thai="bi_ngat"`, return 130.
  - P3 hạn chót đã qua sau khi chụp (dòng 2846–2852): `trang_thai="hong"`, `Chan(MA_HAN)`.
  - Lỗi probe (dòng 2700–2715) ghi sổ KHÔNG ký, nên không dùng được làm bằng chứng (fail-closed, giữ nguyên).
- Ký: có `--attempt-state` thì mọi `_ghi_so(thu_muc, ban_ghi, khoa_ky)` ký HMAC bằng `hmac_key` của state (bảy điểm ghi,
  dòng 2764, 2798, 2842, 2850, 2873, 2900, 3081). Bản ghi mang `nonce`/`attempt` của neo (dòng 2754), `head` (`kq["head"]`),
  `agent_suy_ra`. HMAC chỉ bảo toàn vẹn **trong cùng principal** (docstring `launcher.py:105`): ai đọc được state đọc được
  khoá. Packet này không đổi ranh giới tin cậy đó (§2, §8).
- Chốt ghép: `launcher.py:2719` đòi `--attempt-state` ⇔ `--void-reason`; `--void-reason` (dòng 6115) chỉ nhận
  `infrastructure`/`permission`. Sau spawn launcher bỏ `void_reason`, ghi `void_reason_requested` (2882–2884).
- Người tiêu thụ hiện có, `_kiem_bang_chung_may` (`packet_loop.py:611`), đòi `void_reason == ly_do` cho mọi bản ghi có
  `trang_thai`/`run_id` (dòng 633–637): bản ghi không có `void_reason` KHÔNG hoàn được attempt.
- Một attempt có MỘT nonce cho mọi lần `launcher run`; nonce chỉ quay khi `begin-attempt`. Vì vậy (nonce, codex_call, head)
  không định danh duy nhất một lần thực thi: hai lần chạy cùng `--codex-call` trong một attempt cho hai bản ghi cùng neo.

### 0.4 Schema 3 (wp1174) không thuộc phạm vi

- `_load` (dòng 654) biết đang trong giao dịch v3 qua `_1174_TRANSACTION` (biến `tx`). Đường thường (`tx is None`) đòi
  `schema_version == 2`; trước đó còn kiểm same-family (rc 4). Lệnh mới không có trong `_1174_MUTATORS` (dòng 4665) chạy
  trên state v3 ⇒ fail-closed (rc 4 hoặc rc 8, tuỳ state).
- **Đường đưa sổ v2 vào v3:** `_1174_adopt_payload` (dòng 4928) đọc nguồn v2, chiếu nguyên sổ sang schema 3 rồi gọi
  `_1174_state` → `_load` với `tx` khác None, trước khi dựng tombstone và trả payload. `status`/`next-comment` đọc v3 qua
  `_reader_state` → `_1174_state`. Nếu nới `_load` chung thì nới luôn phép kiểm projection v3 (reviewer lượt 1, P1).

## 1. `write_set`

```
.claude/dev/packet_loop.py
.claude/dev/packet_loop_test.py
.claude/dev/launcher.py
.claude/dev/launcher_test.py
```

## 2. `ngoai_pham_vi`

- **Không hoàn lời gọi đã sinh tiến trình con**, bất kể stderr/stdout, mã thoát, `model_phuc_vu` hay chuỗi lý do. Lời gọi
  bị rate-limit/từ chối quyền SAU spawn vẫn tính; cửa duy nhất là `nang-tran` như hiện nay. Khi nào transport codex có tín
  hiệu dương buộc vào đúng request ("lỗi trước output"), mở packet riêng. Nợ có tên `wp804-post-spawn-unrefundable`.
- Không đổi `record-codex-call`: vẫn giữ chỗ TRƯỚC lời gọi theo ID tự khai, chặn trước khi vượt trần (ADR-0048). Không đổi
  trần, `nang-tran`, `MAC_DINH_TRAN_*`.
- Không có cửa hoàn do người duyệt (Q2). Không chạm schema 3 / `_1174_*` / `_WP1174_*` / `WP1174_REQUIRED`; không thêm vào
  `_1174_MUTATORS` (Q3).
- Không đổi `void-attempt`, `_kiem_bang_chung_may`, `--void-reason` (vẫn hai giá trị), probe, `_loc_stderr_codex`,
  `_BoLocStderr`. Không thu dọn con khi bộ lọc/sandbox hỏng sau spawn (hành vi base, ngoài phạm vi; packet chỉ bảo đảm ca
  ấy KHÔNG phát chứng nhận).
- Không đổi ranh giới tin cậy: HMAC và tệp claim (M1) chỉ chống sửa nhầm/khác lượt trong cùng principal, không chống một
  principal đọc được state cố ý giả mạo (cùng giới hạn với `void-attempt` hiện nay).
- Không thêm khoá ghi cho state v2. Mọi lệnh v2 hiện ghi trực tiếp qua `_save` theo giả định một writer; lệnh mới kế thừa
  giả định đó, không cổng nào cưỡng chế (§8).
- Không gỡ khả năng bịa run_id để tự đốt ngân sách của chính mình (Q4). Nợ có tên `wp804-unverified-call-reservation` (§7).
- Không viết lại #177 hay văn bản protocol.

## 3. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | `launcher.py run` thêm `--codex-call RUN_ID` (mẫu `RUN_ID_RE` của `packet_loop.py`, khai lại hằng trong launcher, không import ngược). Luật ghép: `--attempt-state` đòi ĐÚNG MỘT trong `--void-reason`/`--codex-call`; một trong hai mà thiếu `--attempt-state` ⇒ `Chan(MA_THAM_SO)`. Có `--codex-call` thì: **(a) claim** — ngay sau `_cap_id` và TRƯỚC lần `_ghi_so` đầu, tạo nguyên tử (`O_CREAT|O_EXCL`) tệp `<thư mục state>/wp<N>.codex-claims/<RUN_ID>.json` chứa `{"codex_call","launcher_run_id": rid,"nonce","attempt"}` (`<N>` đọc từ `packet` của state); tệp đã tồn tại ⇒ `Chan(MA_THAM_SO)`, không ghi bản ghi nào mang trường (c); **(b)** bản ghi mang `codex_call=<RUN_ID>` cạnh `nonce`/`attempt`, không mang `void_reason`; **(c)** đúng ba điểm P1–P3 của §0.3 ghi thêm trường ký `chua_sinh_con` với giá trị lần lượt `"phong"`, `"ngat_chup"`, `"han_chup"`. P1 chỉ khi chính `_phong` ném: gán `p = None` trước `try`, đặt trường khi `p is None` trong `except`; lỗi dựng bộ lọc/sandbox sau khi `_phong` trả về KHÔNG được mang trường. Không điểm nào khác ghi trường này. Mọi đường không có `--codex-call` giữ nguyên byte bản ghi (trừ trường biến động). | `.claude/dev/launcher.py` |
| M2 | `packet_loop.py` thêm `void-codex-call --packet N --run-id ID --bang-chung RUN_JSON` (`cmd_void_codex_call`). Theo thứ tự, mỗi chốt một mã và một lý do in ra: (1) `_la_codex(st)`, sai ⇒ `RC_PROVIDER`; (2) `state == "reviewing"`, `attempt_open`, `attempt_anchor` có và `consumed is False`, sai ⇒ `RC_STATE`; (3) đúng một mục `codex_calls` có `run_id`, sai ⇒ `RC_TRACE`; (4) mục ấy `da_dung is False`; (5) mục ấy chưa `hoan`, sai ⇒ `RC_TRACE`; (6) bằng chứng: đọc bytes, `json.loads` với `_cam_khoa_trung`, là `dict`, các khoá `nonce`,`attempt`,`chu_ky`,`run_id`,`codex_call`,`head`,`agent_suy_ra`,`trang_thai`,`pid` có đúng kiểu; `hmac_key` hợp lệ; `nonce == anchor.nonce` và `attempt == anchor.attempt`; `hmac.compare_digest(chu_ky, ky_ban_ghi_luot(d, key))`; sai ⇒ `RC_MOI_TRUONG`; (7) `codex_call == run_id`, `head == mục.head`, `agent_suy_ra == "codex"`, `"void_reason" not in d`, sai ⇒ `RC_MOI_TRUONG`; (8) chứng nhận (M3), sai ⇒ `RC_MOI_TRUONG`; (9) tệp claim của M1(a) tồn tại, là JSON object có đúng bốn khoá, `codex_call == run_id`, `launcher_run_id == d["run_id"]`, `nonce`/`attempt` khớp neo; sai ⇒ `RC_MOI_TRUONG`. Đạt cả chín: mục nhận `hoan: True`, `codex_review_calls_used -= 1`, nối `history` `{"event": "void_codex_call", "run_id": …, "launcher_run_id": d["run_id"], "chua_sinh_con": d["chua_sinh_con"]}`, `_save` đúng MỘT lần, in số còn dùng, rc 0. Bị từ chối ⇒ KHÔNG gọi `_save`. | `.claude/dev/packet_loop.py` |
| M3 | Chứng nhận là danh sách CHO PHÉP ba bộ, khớp TOÀN BỘ: `(chua_sinh_con, trang_thai) ∈ {("phong","hong"), ("ngat_chup","bi_ngat"), ("han_chup","hong")}` và `pid is None`. Thiếu trường, giá trị khác, hay cặp chéo ⇒ từ chối. `packet_loop.py` không đọc `model_phuc_vu*` hay `ly_do_dung` để quyết định. Tập ba bộ khai MỘT lần trong `launcher.py` (hằng), `packet_loop.py` import cùng `ky_ban_ghi_luot` (dòng 54). | `.claude/dev/packet_loop.py`, `.claude/dev/launcher.py` |
| M4 | Sổ: (a) `_load` vế `loi-goi` nhận dạng bốn khoá `{"run_id","head","da_dung","hoan"}` **chỉ khi `tx is None`**, `hoan is True`, `da_dung is False`; dạng ba khoá cũ vẫn hợp lệ; trong giao dịch v3 (kể cả projection của adopt) mục có khoá `hoan` ⇒ vi phạm `loi-goi`. (b) Vế `dem-goi`: `run_id` duy nhất trên TOÀN sổ (kể cả mục đã hoàn); với `A` = số mục không hoàn, `U` = số mục không hoàn và chưa dùng, `C` = `can_duoi`: `used >= A` và `used >= C + U` (hai bất đẳng thức riêng, mỗi cái một phần tử trong `vi_pham`). (c) `cmd_record_review` từ chối `--codex-call` trỏ mục đã hoàn ⇒ `RC_TRACE`, trước `_xet_dung`. (d) `cmd_record_codex_call` vẫn từ chối mọi `run_id` đã có trong sổ, kể cả mục đã hoàn. | `.claude/dev/packet_loop.py` |
| M5 | Parser `void-codex-call` ba tham số bắt buộc; `--run-id` kiểm `RUN_ID_RE.fullmatch` (không nhận newline cuối) trước khi tra sổ, sai ⇒ `RC_ARG` với lý do riêng. Không thêm vào `_1174_MUTATORS`. | `.claude/dev/packet_loop.py` |
| M6 | Ca `r804_*` trong `packet_loop_test.py` theo §4b. Ca dương và ca âm chính dựng bằng **launcher thật** (`run_json_that` mở rộng với `--codex-call`; P1 bằng lệnh không tồn tại, P3 bằng `--deadline-utc` đã qua kèm `--chup-workspace`, P2 bằng fixture tiêm `KeyboardInterrupt` vào `_chup_an_toan`). Ca đo MỘT vế của predicate ghép dùng helper ký fixture `ky_ban_ghi_luot(d, key_của_state)` trên bản ghi launcher thật đã sửa ĐÚNG một trường — chỉ helper này được dựng chữ ký. | `.claude/dev/packet_loop_test.py` |
| M7 | Ca `r804_l_*` trong `launcher_test.py`: (a) `--codex-call` thiếu `--attempt-state` ⇒ `MA_THAM_SO`; (b) có CẢ `--void-reason` và `--codex-call` ⇒ `MA_THAM_SO`; (c) `--attempt-state` một mình ⇒ `MA_THAM_SO`; (d) `--codex-call "a b"` và `"x\n"` ⇒ `MA_THAM_SO`; (e) P1 thật ⇒ bản ghi ký có `codex_call`, `chua_sinh_con="phong"`, `pid` None, không `void_reason`, tệp claim đúng bốn khoá; (f) lỗi tiêm vào constructor `_BoLocStderr` sau khi `_phong` trả về (con thật đã in) ⇒ bản ghi KHÔNG có `chua_sinh_con`; (g) lượt codex giả thoát 1 không in gì ⇒ không có `chua_sinh_con`; (h) chạy lần hai cùng `--codex-call` trong cùng attempt ⇒ `MA_THAM_SO`, tệp claim giữ nguyên byte, không bản ghi nào mang `chua_sinh_con`; (i) P2, P3 ⇒ đúng giá trị trường; (j) đường `--void-reason` cũ: projection bản ghi (bỏ `run_id`,`short_id`, mốc giờ, `chu_ky`, `pid`) bằng projection của base cùng lệnh, và `void-attempt --bang-chung` trên bản ghi `--codex-call` thật ⇒ từ chối (khoá M3 ở nơi tiêu thụ cũ). | `.claude/dev/launcher_test.py` |
| M8 | Đột biến cho mỗi chốt, cả hai bộ (§4b). Mẫu `(tìm, thay)` lấy nguyên văn mã đã viết, khớp đúng một chỗ; `t117` và kiểm khớp-một-chỗ của `packet_loop_test.py` vẫn xanh. | `.claude/dev/packet_loop_test.py`, `.claude/dev/launcher_test.py` |

## 4. `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | Phản chứng #804 trên H: `record-codex-call` → `launcher run --codex-call` với lệnh không tồn tại (P1) → `void-codex-call` ⇒ rc 0; đọc lại sổ: `used` giảm đúng 1, mục `hoan: True`, đúng một sự kiện `void_codex_call` mang `launcher_run_id` của bản ghi. Đối chứng âm riêng: trên base, `void-codex-call --help` ⇒ argparse rc 2. | Đột biến bỏ `-= 1` ⇒ `r804_hoan_tru_bo_dem` ĐỎ; bỏ `hoan` ⇒ `r804_hoan_danh_dau` ĐỎ; bỏ nối history ⇒ `r804_hoan_ghi_history` ĐỎ (ba ca, ba oracle). |
| N2 | Mỗi đột biến §4b: ca đích ĐỎ tại assertion của chính ca ấy (không traceback, không lỗi fixture); bảng tập-ID-đỏ của từng đột biến được ghi, và các chốt nghi tương đương có giao/hiệu tập khác rỗng. | Gỡ từng chốt ⇒ đúng ca đích ĐỎ. |
| N3 | `packet_loop_test.py` và `launcher_test.py` trên H: tập ID ca H = tập ID base ∪ manifest `r804_*` (so TẬP, không so tổng); mọi ID có trên base mang cùng trạng thái `passed`/`skipped` trên H; các nhóm `pl_m*`, `void_run_*`, `case_void_*`, `wp1174_writer_*`, `wp1174_race_*`, `t117` mỗi nhóm khớp ≥1 ID và tất cả `passed`. | Một ID base `passed` mà H khác; một ID base biến mất; một wildcard nhóm khớp 0. |
| N4 | Bộ đột biến hai tệp trên Linux: tập tên mutant theo nhóm `giet`/`song`/`loi`/`bo_qua`/`khong_do_duoc`; mọi mutant mới `giet`; tập `khong_do_duoc` kế thừa bằng base (liệt kê tên). | Ép một mutant mới thành `bo_qua` ⇒ bộ tổng hợp phải ĐỎ (tự kiểm bộ so tập). |
| N5 | Exact head: `ruff check --no-cache --select F` delta so base = 0 trên bốn tệp (base đo được rc 1, 21 chẩn đoán); `doctrine-scan` rc 0 kèm dòng kết luận dương, `adr-song` rc 0 kèm `66/66` (hoặc số base mới); `git diff --check base..H` sạch; `git diff --numstat base..H` đúng 4 tệp §1, tổng thêm ≤ 450. | Thêm tên chưa định nghĩa ⇒ delta ≠ 0; tệp thứ năm ⇒ 5 tệp; một khoảng trắng cuối dòng ⇒ `diff --check` ĐỎ; numstat 451 ⇒ ĐỎ. `doctrine-scan`/`adr-song` không có phản chứng riêng ở packet này — khai thẳng. |
| N6 | `launcher.py doctor --json` trên H với cùng fixture probe offline như base: rc bằng base, cùng tập khoá top-level và cùng tập probe đã chạy. | rc khác, hoặc thiếu khoá/probe so base. |

### 4b. Đường vào và chốt, mỗi đường một ca và một đột biến

Đường đọc/ghi sổ lời gọi đã liệt kê trên base: `cmd_record_codex_call` (ghi), `cmd_record_review` (đọc + `da_dung`),
`_load` vế `loi-goi`/`dem-goi`/`can_duoi` (bất biến, cả trong giao dịch v3), `_1174_adopt_payload` → `_1174_state` →
`_load` (chiếu v2 sang v3), `_reader_state` (đọc v3), `void-attempt`/`begin-attempt` (đổi neo, không đổi sổ),
`nang-tran`/`record-rescue`/`_xet_dung`/`_vao_rescue` (đổi trần/state), và lệnh mới. Executor phát hiện thêm một đường
đọc/ghi `codex_calls` hay `codex_review_calls_used` ngoài danh sách này ⇒ dừng, đi revision (§6).

| # | đường / chốt | ca đích | đột biến |
|---|---|---|---|
| D1 | reviewer không phải codex | `r804_tu_choi_reviewer_khac` | bỏ chốt (1) |
| D2a | state ≠ reviewing (gồm `blocked` sau khi vượt trần) | `r804_tu_choi_ngoai_reviewing` | bỏ vế state |
| D2b | lượt đã đóng / neo consumed (sau `void-attempt`) | `r804_tu_choi_neo_da_dong` | bỏ vế anchor |
| D3 | run_id không có trong sổ | `r804_tu_choi_goi_khong_co` | đổi tra cứu sang mục đầu |
| D4 | lời gọi đã `da_dung` | `r804_tu_choi_da_dung` | bỏ chốt (4) |
| D5 | hoàn hai lần | `r804_tu_choi_hoan_hai_lan` | bỏ chốt (5) |
| D6a | JSON hỏng / không phải object / trùng khoá / thiếu khoá / sai kiểu | `r804_tu_choi_json_hong` (năm vế, mỗi vế một fixture) | bỏ kiểm kiểu ⇒ traceback thay rc ⇒ ca ĐỎ |
| D6b | nonce của lượt khác, chữ ký HỢP LỆ (ký thật ở lượt 1, dùng ở lượt 2) | `r804_tu_choi_cheo_luot` | bỏ so nonce |
| D6c | chữ ký sai, nonce đúng (sửa một trường không phải neo sau khi ký) | `r804_tu_choi_sua_sau_ky` | `compare_digest` → `True` |
| D6d | `hmac_key` của state đổi sau khi ký, nonce giữ | `r804_tu_choi_doi_khoa` | (cùng chốt D6c; khai tương đương, ghi tập-ID) |
| D7a | `codex_call` ≠ `--run-id` (fixture ký, lệch đúng trường) | `r804_tu_choi_ban_ghi_goi_khac` | bỏ so `codex_call` |
| D7b | `head` ≠ head của mục (launcher thật ở worktree head khác) | `r804_tu_choi_head_khac` | bỏ so head |
| D7c | `agent_suy_ra` ≠ codex (launcher thật, lệnh claude, P1) | `r804_tu_choi_khong_phai_codex` | bỏ so `agent_suy_ra` |
| D7d | có `void_reason` (fixture ký thêm trường vào bản ghi P1 thật) | `r804_tu_choi_co_void_reason` | bỏ chốt `"void_reason" not in d` |
| D8a | bản ghi sau spawn, không trường `chua_sinh_con` (codex giả thoát 1, không khung) | `r804_tu_choi_sau_spawn` | coi thiếu trường là `"phong"` |
| D8b | lỗi sau `_phong` (tiêm vào `_BoLocStderr`) | `r804_tu_choi_loi_sau_phong` | (đột biến ở launcher: bỏ điều kiện `p is None` ⇒ L-f ĐỎ và ca này ĐỎ) |
| D8c | cặp chéo `("phong","bi_ngat")` (fixture ký) | `r804_tu_choi_cap_cheo` | so trường riêng lẻ thay vì cặp |
| D8d | `pid` khác None (fixture ký) | `r804_tu_choi_co_pid` | bỏ vế `pid is None` |
| D8e | giá trị lạ `"phong "` / `"Phong"` (fixture ký) | `r804_tu_choi_gia_tri_la` | so `startswith`/`lower()` |
| D8f | bản ghi trung gian `dang_chay` (lần `_ghi_so` đầu, ký hợp lệ) | `r804_tu_choi_trung_gian` | (khoá bằng M3; khai tương đương với D8a nếu tập-ID trùng) |
| D9a | dương P1 | `r804_hoan_tru_bo_dem`, `r804_hoan_danh_dau`, `r804_hoan_ghi_history` | xem N1 |
| D9b | dương P2 | `r804_hoan_ngat_chup` | bỏ bộ P2 khỏi tập cho phép |
| D9c | dương P3 | `r804_hoan_han_chup` | bỏ bộ P3 khỏi tập cho phép |
| D10a | claim vắng (bản ghi P1 thật, xoá tệp claim) | `r804_tu_choi_claim_vang` | bỏ chốt (9) |
| D10b | claim của lần chạy khác: hai bản ghi cùng codex_call/nonce/head; dùng bản ghi KHÔNG phải của claimant | `r804_tu_choi_claim_lan_khac` | bỏ so `launcher_run_id` |
| D10c | launcher chạy lần hai cùng `--codex-call` | (`r804_l_h` bên launcher) | bỏ `O_EXCL` |
| D11 | `record-review` với lời gọi đã hoàn | `r804_review_tu_choi_goi_da_hoan` | bỏ chốt M4(c) |
| D12 | `record-codex-call` dùng lại run_id đã hoàn | `r804_khong_tai_dung_run_id` | kiểm trùng chỉ xét mục chưa hoàn |
| D13a | `_load` nhận: hoàn một rồi ghi tiếp; hoàn hết; trùng ID giữa hai mục đã hoàn ⇒ TỪ CHỐI | `r804_load_nhan_so_hoan`, `r804_load_trung_id_hoan` | bỏ phần "toàn sổ" của tính duy nhất |
| D13b | `_load` từ chối `hoan: False`, `hoan` kèm `da_dung: True`, khoá thứ năm | `r804_load_dang_muc_sai` | nới M4(a) |
| D13c | witness cận 1: `A=2,C=0,U=0,used=1` ⇒ từ chối | `r804_load_can_a` | bỏ `used >= A` |
| D13d | witness cận 2: `A=1,C=2,U=1,used=2` ⇒ từ chối; `used > A` với cả hai cận đạt và state suy từ v1 ⇒ NHẬN | `r804_load_can_cu` | bỏ `used >= C + U` |
| D14 | bị từ chối ⇒ 0 lần gọi `_save` (đếm bằng monkeypatch) và byte `wp<N>.json` không đổi | gộp trong D1–D10b | gọi `_save` một lần trước chốt (9) |
| D15a | v3: lệnh mới trên state v3 hợp lệ (fixture wp1174) ⇒ từ chối, byte không đổi | `r804_v3_lenh_moi_tu_choi` | nới vế `schema` của `_load` cho `void-codex-call` |
| D15b | adopt hai nguồn v2 tương đương, chỉ một có mục `hoan` ⇒ nguồn có `hoan` bị từ chối trước khi có prepared/target/tombstone; nguồn không `hoan` đi qua cùng cổng | `r804_v3_adopt_tu_choi_hoan` | bỏ điều kiện `tx is None` của M4(a) |
| D16 | `--run-id` sai dạng (gồm newline cuối) | `r804_tu_choi_run_id_sai_dang` | `fullmatch` → `match` không neo cuối |
| D17 | chuỗi tương tác: hoàn → ghi tiếp → review lời gọi còn hiệu lực ⇒ rc 0, bộ đếm đúng; chạm trần → hoàn (đang reviewing) → ghi thêm được một; `nang-tran` → `record-rescue` → hoàn ⇒ bộ đếm/limit đúng | `r804_chuoi_tuong_tac` (ba vế) | bỏ `-= 1` (đã có ở N1; vế này khoá thứ tự, ghi tập-ID) |
| L-a…L-j | launcher M7 (a)–(j) | `r804_l_a` … `r804_l_j` | mỗi chốt ghép tham số một đột biến; bỏ `codex_call` khỏi bản ghi; bỏ `O_EXCL`; bỏ `p is None`; ghi `chua_sinh_con` ở thêm một điểm sau spawn ⇒ L-f/L-g ĐỎ |

Đột biến **nới** bắt buộc: thêm bộ `("sau_spawn","xong")` vào tập cho phép ⇒ ca D8a vẫn ĐỎ (vì thiếu trường) nên phải có
thêm fixture ký mang `chua_sinh_con="sau_spawn"` ⇒ `r804_tu_choi_gia_tri_la` ĐỎ; cho `pid` bất kỳ ⇒ D8d ĐỎ.

## 5. `pham_vi_e`

Không chạm E4, không chạm E5. Packet thêm một cửa hoàn ngân sách có bằng chứng máy; không đổi quyền, không đổi trần.

## 6. `luat_dung`

- Trần lời gọi Codex theo dòng khai `ADR-0055`. Chạm trần ⇒ Review Rescue Checkpoint. Xin tăng là **E2**.
- Dừng triển khai, đi revision đặc tả khi:
  - cần sửa ngoài write set;
  - thấy đường đọc/ghi `codex_calls`/`codex_review_calls_used` ngoài danh sách §4b;
  - mã §0 trên exact base của lease khác hành vi đã đo (đặc biệt: P1–P3 không còn là điểm duy nhất trước spawn; adopt ghi
    gì đó TRƯỚC khi gọi `_1174_state`);
  - `numstat` vượt 450 dòng thêm. Khi đó tách: (A) launcher M1 + M3 hằng + M7 (+ đột biến L); (B) `packet_loop` M2–M6 (+ đột
    biến D). B phụ thuộc hợp đồng của A (trường `chua_sinh_con`, tệp claim, hằng tập cho phép).
- Đặc tả không thuộc Mission, nên chờ chủ kho duyệt băm theo `ADR-0067`: **E2**.

## 7. `hinh_dang_ke_thua`

`khong_ap_dung`: packet thêm cửa hoàn mới, không vá lại một bản vá cũ, dù khép nợ `wp775-no-launcher-evidence`.

Nợ giữ lại, có tên, dẫn lại khi đóng #804/#177:
- `wp804-unverified-call-reservation` (Q4): `record-codex-call` tiếp tục giữ chỗ theo ID tự khai; hai ID bịa ở trần mặc
  định chiếm hết ngân sách. Packet này chỉ đóng đường hoàn không bằng chứng. Đóng hẳn cần đổi ADR-0048.
- `wp804-post-spawn-unrefundable`: lời gọi đã sinh con nhưng chết trước output (429, từ chối quyền) không hoàn được; cần
  tín hiệu dương từ transport codex.

## 8. `chua_do_duoc`

- Kích thước ước tĩnh, chưa vá thử: `launcher.py` ~35 (tham số, claim, ba điểm ghi trường, hằng), `packet_loop.py` ~75
  (lệnh, chín chốt, M4), `launcher_test.py` ~110 (mười ca, đột biến), `packet_loop_test.py` ~220 (helper launcher/ký
  fixture, ~35 ca nhỏ, đột biến); tổng ~440 — SÁT trần. Reviewer lượt 1 ước 385–535. Executor đo `numstat` sau khi viết
  xong phần launcher; vượt 450 ⇒ áp §6 tách.
- `review_class` chưa đo bằng `_tinh_lop_tu_write_set`; suy từ tiền lệ #1313/#1375.
- Không cổng nào cưỡng chế một-writer trên state v2; lệnh mới kế thừa giả định của mọi lệnh v2. Hai `void-codex-call`
  chạy song song đọc cùng ảnh thì ghi sau thắng: mất một cập nhật, không hoàn kép (cả hai trừ từ cùng một giá trị). Không
  dùng điều này làm tiêu chí nghiệm thu.
- Tỉ lệ lời gọi thật hoàn được qua P1–P3 là không biết; dự kiến nhỏ. Phần lớn lỗi quota/quyền xảy ra sau spawn (§2).
- Mốc N/N và tập bỏ qua của hai suite trên base chưa lấy; executor đo trên exact base của lease.
- Fixture v3 hợp lệ cho D15a/D15b: dùng fixture wp1174 có sẵn trong `packet_loop_test.py`; nếu không dựng được adopt từ
  nguồn v2 trong ca thì dừng, đi revision, không hạ D15b thành kiểm vế `schema`.

## 9. Quyết định của chủ kho (2026-11-18, phiên điều phối #1206, qua AskUserQuestion)

- **Q1 — có.** Đóng #177 cùng packet; comment trỏ §0.1 và các ca `pl_m3_neo_loi_goi`, `r804_*`.
- **Q2 — không.** Không thêm cửa hoàn do người duyệt; `nang-tran` là cửa có người duyệt.
- **Q3 — có.** Giữ schema 3 ngoài phạm vi, fail-closed (D15a/D15b khoá).
- **Q4 — có.** Chỉ chặn hướng "hoàn không bằng chứng"; vế "run_id bịa đốt ngân sách" là nợ `wp804-unverified-call-reservation`,
  không đổi ADR-0048 trong packet này.

## 10. Nhật ký thay đổi theo lượt review

- **Lượt 1 → bản này** (Codex, request_changes, 4 P1 + 4 P2 + 1 P3): bỏ dạng (B) "vắng khung" — không còn hoàn lời gọi đã
  sinh con (P1 #1); thay dạng (A) bằng trường ký `chua_sinh_con` chỉ ghi ở ba điểm control-flow P1–P3, P1 chỉ khi chính
  `_phong` ném (P1 #2); thêm tệp claim `O_EXCL` buộc một reservation với đúng một lần thực thi launcher và chốt (9), khai
  ranh giới tin cậy cùng principal (P1 #3); `hoan` chỉ hợp lệ khi `tx is None`, D15b đo adopt (P1 #4); tách đột biến theo
  từng vế với fixture ký lệch một trường, D14 đếm `_save` (P2 #1); thêm D2b, D6a, D17, chuỗi tương tác, giả định một-writer
  khai ở §2/§8 (P2 #2); nợ có tên ở §7, §9 thành biên bản quyết định (P2 #3); D13c/D13d hai witness (P2 D11); N3/N4 so tập,
  N5 phản chứng đủ, N6 `doctor --json` (L1–L7); §8 ước lượng lại ~440 kèm điều kiện tách (P3).
