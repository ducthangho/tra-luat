tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# HOAN-LOI-GOI-CODEX r1 — hoàn một lời gọi codex review khi launcher chứng minh model chưa sinh output

- packet_id: HOAN-LOI-GOI-CODEX; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | #804 (chính); #177 (đóng kèm nếu chủ kho chấp nhận kết luận ở §0.1, xem Q1) |
| `nguon_cap_viec` | Chủ kho duyệt P4 "#177 + #804" trong đợt vá chỗ sót, phiên điều phối #1206 ngày 18-11-2026. P4 phải chờ #1342 r3 land vì cùng chạm `packet_loop.py`; r3 đã merge ở `aeb5cae`. #804 là nợ `wp775-no-launcher-evidence` (connector P1 trên PR #779). #177 là Packet Issue W0-R1B, mở từ 19-08, chưa ai cấp lease. |
| `review_class` | `sensitive`: cả bốn tệp trong write set nằm dưới `.claude/dev/`. Đối chiếu bằng `lease_publish check` khi cấp lease; lớp không đo lại trong lượt soạn này (§8). |
| `base` | `aeb5cae0af01538c88ab2b50c27902dfaf7a7382` (`origin/master` lúc soạn, đo 2026-11-18T14:4xZ). Lease ghi OID base thật lúc cấp. |

## 0. Hiện trạng (đo 2026-11-18T14:20Z–14:49Z trên `aeb5cae`, Linux, Python 3.13.18, clone riêng trong scratchpad)

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
- Đo được: tám ca `pl_m1_tran_so_duong`, `pl_m2_loi_goi`, `pl_m3_codex`, `pl_m3_neo_loi_goi`, `pl_m3_vong`,
  `void_run_cheo_luot_bi_chan`, `void_run_cu_khong_neo_co_thong_diep_rieng`, `void_run_that_dung_luot_duoc_tha` chạy qua
  `chay_suite(CANONICAL, tmp, names)` trên base, cả tám OK. `case_pl_m3_neo_loi_goi` (`packet_loop_test.py:7671`) có vế
  `_rv(5, "approve", None)`, tức chính chuỗi phản chứng của #177 §2: review codex không kèm lời gọi ⇒ rc 5.
- #177 §8.4 có hai câu hỏi còn ý nghĩa: "trần vòng cắn trước trần attempt" và "lượt void vì quota không ăn vòng". Câu
  thứ nhất đã do ADR-0048/0052/0055 quyết định lại; canon hiện tại là vòng 10, lời gọi 10, không còn là 2. Câu thứ hai:
  `void-attempt` không chạy được sau khi lượt đã có review (dòng 1090–1094), nên lượt void không ăn vòng. Nhưng nó vẫn ăn
  **lời gọi codex**, vì không có đường hoàn lời gọi. Đó chính là #804, và là phần packet này làm.

### 0.2 #804: bộ đếm lời gọi chỉ dựa trên lời khai

- `cmd_record_codex_call` (dòng 1339) tăng `codex_review_calls_used` từ `--run-id` và `--head` do người gọi khai. Nó không
  đọc hiện vật nào của launcher.
- Phản chứng chạy được trên base (test harness `_reviewing`, trần 50): hai `record-codex-call` với run_id bịa
  `bia-khong-co-launcher` và `bia-2` ⇒ cả hai rc 0, `codex_review_calls_used = 2`, hai mục `da_dung: False`. Với trần mặc
  định `MAC_DINH_TRAN_CODEX = 2` (dòng 64), hai lời gọi bịa là đủ cạn ngân sách.
- Không có đường hoàn: `void-codex-call` không tồn tại. Gọi thử ⇒ argparse rc 2, danh sách lệnh không có nó.
- Luật đếm: `docs/PROTOCOL_DA_PHIEN.md` §12 (khoảng dòng 1173–1176 trên base) và `ADR-0052` dòng 11–15 nói rằng một lời
  gọi chỉ tính khi launcher có bằng chứng model đã bắt đầu sinh output/token. Lỗi preflight, permission denial hay
  rate-limit trước khi có output thì không tính. Mã hiện tính MỌI lời gọi đã ghi, kể cả loại đáng ra không tính.

### 0.3 Launcher đã đo được "model chưa bắt đầu"

- Lượt codex (`_la_codex(qd)`, `launcher.py:2063`, theo `agent_suy_ra`) chạy qua `_BoLocStderr` (dòng 2227). Bộ này đọc
  stderr tới EOF và ghi `model_phuc_vu` (danh sách khung `response.created`/`response.completed`),
  `model_phuc_vu_trang_thai`, `model_phuc_vu_ly_do` (dòng 2258–2274).
- `_ket_luan_model` (dòng 2199–2214) trả lý do chính xác
  `"khong thay khung response.created/response.completed nao mang model trong stderr cua con; KHONG suy tu -m hay cau hinh"`
  CHỈ khi bộ lọc không hỏng, ống đã đóng, không mất khung và không có dòng không rõ loại. Vì vậy lý do này cùng với
  `model_phuc_vu == []` là chứng nhận đọc trọn stderr mà không thấy khung nào: máy chủ chưa tạo response.
- Ký: khi có `--attempt-state`, mọi lần `_ghi_so(thu_muc, ban_ghi, khoa_ky)` ký HMAC bằng `hmac_key` của state. Có bảy
  lời gọi, dòng 2764, 2798, 2842, 2850, 2873, 2900, 3081; lần cuối (3081) ghi sau `bo_loc.ghi_so` (2942) và sau khi băm
  log, nên bản cuối mang chữ ký trên các trường model. Bản ghi mang `nonce`/`attempt` của neo lượt (dòng 2754), cùng `head`
  của workspace (`kq["head"]`, dòng 1835) và `agent_suy_ra` (dòng 2686).
- Chốt cản: `launcher.py:2719` đòi `--attempt-state` và `--void-reason` đi cùng nhau, và `--void-reason` (dòng 6115) chỉ
  nhận `infrastructure`/`permission`. Muốn có bản ghi ký cho một lượt codex review, người gọi phải khai một lý do void dù
  lượt ấy chưa hỏng. Sau spawn, launcher bỏ `void_reason` và ghi `void_reason_requested` (dòng 2882–2884).
- Người tiêu thụ hiện có, `_kiem_bang_chung_may` (`packet_loop.py:611`), đòi `void_reason == ly_do` cho mọi bản ghi có
  `trang_thai`/`run_id` (dòng 633–637). Vì vậy một bản ghi không có `void_reason` KHÔNG hoàn được attempt. Packet này dựa
  vào điều đó, và khoá nó bằng ca (M7).
- Fixture có sẵn: `run_json_that` (`packet_loop_test.py:191`) chạy launcher thật với `--attempt-state`; `_r25_codex_gia`
  (`launcher_test.py:6700`) là codex giả in khung `response.created` ra stderr.

### 0.4 Schema 3 (wp1174) không thuộc phạm vi

- `_1174_MUTATORS` (dòng 4665) liệt kê các lệnh ghi của đường giao dịch v3. Lệnh không có trong danh sách sẽ đi đường
  thường (`main`, dòng 7055–7060), mà `_load` khi không có giao dịch lại đòi `schema_version == 2` (vế `schema`, dòng 681).
  Vì vậy một lệnh mới chạy trên state v3 sẽ fail-closed `RC_STATE`.
- Đường v3 còn khoá bộ đếm đơn điệu (dòng 5414–5416: `codex_review_calls_used` không giảm) và sổ lời gọi chỉ được nối thêm
  (5422–5424). Hoàn lời gọi trên v3 là thay đổi chính sách của wp1174, không làm ở đây (Q3).

## 1. `write_set`

```
.claude/dev/packet_loop.py
.claude/dev/packet_loop_test.py
.claude/dev/launcher.py
.claude/dev/launcher_test.py
```

## 2. `ngoai_pham_vi`

- Không đổi `record-codex-call`: vẫn giữ chỗ TRƯỚC lời gọi, vẫn chặn trước khi vượt trần (ADR-0048). Không đổi cách tính
  trần, không đổi `nang-tran`, không đổi `MAC_DINH_TRAN_*`.
- Không hoàn lời gọi đã có output, kể cả timeout hay output sai schema (ADR-0052 tính các lời gọi đó).
- Không có cửa hoàn do người duyệt (kiểu `--khong-co-bang-chung` của `void-attempt`). Lời gọi không có bản ghi ký thì đi
  `nang-tran` như hiện nay (Q2).
- Không chạm schema 3 / `_1174_*` / `_WP1174_*` / `WP1174_REQUIRED`. Không thêm lệnh mới vào `_1174_MUTATORS`.
- Không đổi `void-attempt`, `_kiem_bang_chung_may`, `--void-reason` (vẫn hai giá trị), luồng probe của launcher, hay bộ lọc
  stderr `_loc_stderr_codex`.
- Không gỡ khả năng bịa run_id để tự đốt ngân sách của chính mình: việc đó chỉ làm hỏng phía người bịa, theo hướng
  fail-closed. Packet này chặn hướng ngược lại: không được hoàn mà không có bằng chứng (Q4).
- Không viết lại #177 hay văn bản protocol. Đóng #177 là việc của phiên điều phối khi land.

## 3. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | `launcher.py run` thêm `--codex-call RUN_ID`, mẫu bằng `RUN_ID_RE` của `packet_loop.py`; khai lại hằng trong launcher, không import ngược. Luật ghép đổi từ "`--attempt-state` ⇔ `--void-reason`" thành: `--attempt-state` đòi ĐÚNG MỘT trong `--void-reason` hoặc `--codex-call`; `--void-reason` hay `--codex-call` mà thiếu `--attempt-state` ⇒ `Chan(MA_THAM_SO)`. Có `--codex-call` thì bản ghi mang thêm `codex_call=<RUN_ID>` cạnh `nonce`/`attempt` ở bước ghi sổ đầu (dòng 2754), không mang `void_reason`, và được ký như mọi bản ghi có neo. Mọi đường còn lại giữ nguyên byte. | `.claude/dev/launcher.py` |
| M2 | `packet_loop.py` thêm lệnh `void-codex-call --packet N --run-id ID --bang-chung RUN_JSON` (`cmd_void_codex_call`). Theo thứ tự, mỗi chốt trả mã riêng và in lý do: (1) `_la_codex(st)`, sai ⇒ `RC_PROVIDER`; (2) `state == "reviewing"` và `attempt_open`, sai ⇒ `RC_STATE`; (3) có mục `codex_calls` đúng `run_id`, sai ⇒ `RC_TRACE`; (4) mục ấy `da_dung is False`, sai ⇒ `RC_TRACE`; (5) mục ấy chưa hoàn, sai ⇒ `RC_TRACE`; (6) bản ghi: đọc JSON, `hmac_key` hợp lệ, có `nonce`/`chu_ky`, `nonce == attempt_anchor["nonce"]`, chữ ký khớp `ky_ban_ghi_luot` (so bằng `hmac.compare_digest`), sai ⇒ `RC_MOI_TRUONG`; (7) `codex_call == run_id`, `head == mục.head`, `agent_suy_ra == "codex"`, `"void_reason" not in d`, sai ⇒ `RC_MOI_TRUONG`; (8) chứng nhận "chưa có output" ở M3, sai ⇒ `RC_MOI_TRUONG`. Đạt cả tám thì: mục nhận `hoan: True`, `codex_review_calls_used -= 1`, nối `history` một sự kiện `{"event": "void_codex_call", "run_id": …, "launcher_run_id": d["run_id"]}`, `_save`, in số còn dùng, rc 0. Mọi chốt chạy TRƯỚC `_save`; bị từ chối thì state giữ nguyên từng byte. | `.claude/dev/packet_loop.py` |
| M3 | Chứng nhận "chưa có output" là danh sách CHO PHÉP hai dạng, không dạng nào khác: (A) **trước spawn**: `trang_thai == "hong"`, `pid is None`, `ly_do_dung` bắt đầu bằng `"khong chay duoc lenh: "`; (B) **sau spawn, đã kết thúc**: `trang_thai` thuộc `{"xong", "qua_han", "bi_ngat", "hong"}`, `model_phuc_vu == []`, `model_phuc_vu_trang_thai == "KHONG_DO_DUOC"`, và `model_phuc_vu_ly_do` BẰNG từng ký tự chuỗi không-khung của `_ket_luan_model`. Chuỗi này lấy từ MỘT hằng mới trong `launcher.py`, được `_ket_luan_model` dùng và `packet_loop.py` import cùng `ky_ban_ghi_luot` (dòng 54); không chép tay hai nơi. Mọi trạng thái khác (`dang_chay`, `da_dung`, `ghi_workspace`, `khong_do_duoc_workspace`, thiếu trường) ⇒ từ chối. | `.claude/dev/packet_loop.py`, `.claude/dev/launcher.py` |
| M4 | Sổ và người đọc sổ: (a) `_load` vế `loi-goi` nhận thêm dạng `{"run_id","head","da_dung","hoan"}` chỉ khi `hoan is True` và `da_dung is False`; dạng ba khoá cũ vẫn hợp lệ, mọi dạng khác vẫn hỏng. (b) Vế `dem-goi` tính trên lời gọi CÒN HIỆU LỰC: `run_id` duy nhất trên TOÀN sổ (kể cả mục đã hoàn); `số mục không hoàn <= used >= can_duoi + số mục không hoàn và chưa dùng`. (c) `cmd_record_review` từ chối `--codex-call` trỏ tới mục đã hoàn ⇒ `RC_TRACE`, trước `_xet_dung`. (d) `cmd_record_codex_call` vẫn từ chối mọi `run_id` đã có trong sổ, kể cả mục đã hoàn (giữ nguyên dòng 1347). | `.claude/dev/packet_loop.py` |
| M5 | Parser: `sub.add_parser("void-codex-call", …)` với ba tham số bắt buộc. `--run-id` kiểm `RUN_ID_RE` trước khi tra sổ. Không thêm vào `_1174_MUTATORS`. | `.claude/dev/packet_loop.py` |
| M6 | Ca mới trong `packet_loop_test.py`, tiền tố `r804_`. Mỗi ca dựng bản ghi bằng **launcher thật** (mở rộng `run_json_that` hoặc helper mới gọi `launcher.py run --attempt-state … --codex-call …`), không tự dựng JSON đã ký, trừ ca giả mạo chữ ký. Bảng §4b. | `.claude/dev/packet_loop_test.py` |
| M7 | Ca mới trong `launcher_test.py`, tiền tố `r804_`: (a) `--codex-call` không kèm `--attempt-state` ⇒ `MA_THAM_SO`; (b) `--attempt-state` kèm CẢ `--void-reason` và `--codex-call` ⇒ `MA_THAM_SO`; (c) `--attempt-state` một mình ⇒ `MA_THAM_SO` (giữ hành vi base); (d) `--codex-call "a b"` ⇒ `MA_THAM_SO`; (e) codex giả KHÔNG in khung, thoát 1 ⇒ `run.json` có `codex_call`, `nonce`, `chu_ky` khớp, không có `void_reason`, `model_phuc_vu == []`, `model_phuc_vu_ly_do` bằng hằng M3; (f) codex giả in một khung `response.created` ⇒ `model_phuc_vu` có đúng một mục; (g) đường `--void-reason` cũ vẫn cho bản ghi y như base (so tập khoá với một lượt base cùng lệnh). | `.claude/dev/launcher_test.py` |
| M8 | Đột biến mới cho mỗi chốt, cả hai bộ (bảng §4b). Mẫu `(tìm, thay)` lấy nguyên văn mã đã viết, mỗi mẫu khớp đúng một chỗ; `t117` của `launcher_test.py` và kiểm khớp-một-chỗ tương ứng của `packet_loop_test.py` vẫn xanh. | `.claude/dev/packet_loop_test.py`, `.claude/dev/launcher_test.py` |

## 4. `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | Phản chứng #804 trên H: chuỗi `record-codex-call` (lời gọi thật) → launcher codex giả không khung → `void-codex-call` ⇒ rc 0, `used` giảm đúng 1, mục `hoan: True`. Cùng chuỗi trên base ⇒ argparse rc 2 (lệnh không tồn tại). | Đột biến bỏ bước trừ bộ đếm ⇒ ca `r804_hoan_tru_dung_mot` ĐỎ. |
| N2 | Mọi ca §4b ĐẠT trên H; mỗi đột biến §4b giết ĐÚNG ca đích, ghi `giet` (không phải lỗi/bỏ qua), và không giết ca của chốt khác. | Bảng §4b: gỡ từng chốt ⇒ đúng ca đích ĐỎ. |
| N3 | Không hồi quy: `packet_loop_test.py` trên H ra N/N hai số BẰNG NHAU; tập ca BỎ QUA bằng base; số ca nền tăng đúng bằng số ca `r804_` thêm. `launcher_test.py` trên H ra N/N, tập bỏ qua bằng base. Riêng các ca `pl_m*`, `void_run_*`, `case_void_*`, `wp1174_writer_*`, `wp1174_race_*`, `t117` ĐẠT. | Bất kỳ ca nào đạt trên base mà ĐỎ trên H. |
| N4 | Bộ đột biến hai tệp trên Linux: dòng tổng kết hai số bằng nhau. Các mục "KHÔNG ĐO ĐƯỢC trên nền này" đúng bằng tập kế thừa của base (đếm và liệt kê tên). | Số "không đo được" khác base mà không giải thích được bằng thay đổi của base. |
| N5 | Trên exact head: `ruff check --select F` delta so base = 0 trên bốn tệp; `doctrine-scan`, `adr-song` rc 0 kèm dòng kết luận dương; `git diff --check base..H` sạch; `git diff --numstat base..H` đúng 4 tệp của §1, tổng dòng thêm ≤ 450 (`ADR-0053`). | Thêm một tên chưa định nghĩa ⇒ ruff delta ≠ 0. Thêm tệp thứ năm ⇒ numstat 5 tệp. `doctrine-scan`/`adr-song`: packet này không có phản chứng riêng, khai thẳng. |
| N6 | `python .claude/dev/launcher.py doctor` trên H chạy trọn, rc bằng base. | rc khác base. |

### 4b. Đường vào và chốt, mỗi đường một ca và một đột biến

Liệt kê HẾT các đường đọc/ghi sổ lời gọi trước khi viết, không vá theo danh sách reviewer chỉ (bài học CLAUDE.md "vá
đúng chỗ được chỉ rồi bỏ sót đường thứ ba"). Đường đã liệt kê trên base: `cmd_record_codex_call` (ghi), `cmd_record_review`
(đọc + đánh dấu `da_dung`), `_load` vế `loi-goi`/`dem-goi`/`can_duoi` (bất biến), đường v3 (dòng 5018, 5422–5424,
5444, 5504–5507; ngoài phạm vi, khoá bằng D13), và lệnh mới. Phát hiện thêm một đường đọc `codex_calls` ngoài danh sách
này ⇒ dừng, đi revision (§6).

| # | đường / chốt | ca đích (tên gợi ý) | đột biến (gỡ chốt) |
|---|---|---|---|
| D1 | reviewer không phải codex | `r804_tu_choi_reviewer_khac` | bỏ chốt (1) |
| D2 | state ≠ reviewing hoặc lượt đóng | `r804_tu_choi_ngoai_reviewing` | bỏ chốt (2) |
| D3 | run_id không có trong sổ | `r804_tu_choi_goi_khong_co` | bỏ chốt (3), đổi `next(..., None)` sang mục đầu |
| D4 | lời gọi đã neo review (`da_dung`) | `r804_tu_choi_da_dung` | bỏ chốt (4) |
| D5 | hoàn hai lần cùng một lời gọi | `r804_tu_choi_hoan_hai_lan` | bỏ chốt (5) |
| D6a | chữ ký sai (sửa một trường sau khi ký) | `r804_tu_choi_sua_sau_ky` | thay `compare_digest` bằng `True` |
| D6b | nonce của lượt khác (bản ghi lượt 1 dùng ở lượt 2) | `r804_tu_choi_cheo_luot` | bỏ so nonce |
| D6c | bản ghi không có neo (`nonce`/`chu_ky` vắng) | `r804_tu_choi_khong_neo` | bỏ chốt có mặt |
| D7a | `codex_call` của bản ghi ≠ `--run-id` (bản ghi của lời gọi khác) | `r804_tu_choi_ban_ghi_goi_khac` | bỏ so `codex_call` |
| D7b | `head` ≠ head của mục | `r804_tu_choi_head_khac` | bỏ so head |
| D7c | `agent_suy_ra` ≠ codex (lượt claude có ký) | `r804_tu_choi_khong_phai_codex` | bỏ so `agent_suy_ra` |
| D7d | bản ghi void-attempt (có `void_reason`) dùng làm bằng chứng hoàn lời gọi | `r804_tu_choi_ban_ghi_void` | bỏ chốt `"void_reason" not in d` |
| D8a | có khung model (`model_phuc_vu` khác rỗng) | `r804_tu_choi_co_output` | bỏ vế `model_phuc_vu == []` |
| D8b | lý do khác chuỗi không-khung (ví dụ stderr còn mở / mất khung) | `r804_tu_choi_ly_do_khac` | nới so bằng thành "chứa"/`startswith` |
| D8c | `trang_thai == "dang_chay"` (launcher bị giết giữa chừng) | `r804_tu_choi_dang_chay` | thêm `dang_chay` vào tập (B) |
| D8d | dạng (A) trước spawn: được hoàn | `r804_hoan_truoc_spawn` | bỏ nhánh (A) ⇒ ca dương ĐỎ |
| D8e | dạng (B) sau spawn không khung: được hoàn | `r804_hoan_tru_dung_mot` | bỏ `-= 1` ⇒ ĐỎ; bỏ `hoan: True` ⇒ ĐỎ (hai đột biến) |
| D9 | `record-review` với lời gọi đã hoàn | `r804_review_tu_choi_goi_da_hoan` | bỏ chốt M4(c) |
| D10 | `record-codex-call` dùng lại run_id đã hoàn | `r804_khong_tai_dung_run_id` | đổi kiểm trùng thành chỉ xét mục chưa hoàn |
| D11 | `_load` nhận sổ có mục hoàn hợp lệ; từ chối `hoan: False`, `hoan` kèm `da_dung: True`, khoá thứ năm, và `used` bị sửa tay lệch số mục còn hiệu lực | `r804_load_bat_bien_so_hoan` | bỏ từng vế M4(a)/(b) (mỗi vế một đột biến) |
| D12 | bị từ chối thì state giữ nguyên byte | gộp trong D1–D8c: mỗi ca so byte `wp55.json` trước/sau | gọi `_save` trước chốt (8) |
| D13 | state schema 3 ⇒ fail-closed, không đổi byte | `r804_v3_fail_closed` | (không có chốt mới; khoá hành vi base. Đột biến đối chứng: thêm `void-codex-call` vào `_1174_MUTATORS` ⇒ ca phải ĐỎ hoặc báo rõ nó không còn đo đường thường) |
| D14 | `--run-id` sai dạng | `r804_tu_choi_run_id_sai_dang` | bỏ kiểm `RUN_ID_RE` |
| L1–L7 | launcher M7 (a)–(g) | `r804_l_*` trong `launcher_test.py` | mỗi chốt ghép tham số một đột biến; bỏ `codex_call` khỏi bản ghi; dùng chuỗi lý do chép tay thay hằng (đột biến đổi một ký tự hằng ⇒ D8b/M7(e) ĐỎ) |

Đột biến **nới** bắt buộc (khẳng định ca đo đúng danh sách cho phép): cho tập (B) nhận mọi `trang_thai` khác
`dang_chay` ⇒ phải có ca ĐỎ (dùng `ghi_workspace`); cho lý do so bằng `startswith("khong thay khung")` ⇒ D8b ĐỎ.

## 5. `pham_vi_e`

Không chạm E4, không chạm E5. Packet thêm một cửa hoàn ngân sách có bằng chứng máy; không đổi quyền, không đổi trần.

## 6. `luat_dung`

- Trần lời gọi Codex theo dòng khai `ADR-0055`. Chạm trần ⇒ Review Rescue Checkpoint. Xin tăng là **E2**.
- Dừng triển khai, đi revision đặc tả khi:
  - cần sửa ngoài write set;
  - thấy một đường đọc/ghi `codex_calls` hoặc `codex_review_calls_used` trên đường thường ngoài danh sách §4b;
  - mã của §0 trên exact base của lease khác hành vi đã đo;
  - `numstat` vượt 450 dòng thêm. Khi đó tách: (A) launcher M1 + M7; (B) `packet_loop` M2–M6. B phụ thuộc A.
- Đặc tả không thuộc Mission, nên chờ chủ kho duyệt băm theo `ADR-0067`: **E2**.

## 7. `hinh_dang_ke_thua`

`khong_ap_dung`: packet thêm cửa hoàn mới. Nó không vá lại một bản vá cũ, dù khép nợ `wp775-no-launcher-evidence`.

## 8. `chua_do_duoc`

- Kích thước ước tĩnh, chưa vá thử: `packet_loop.py` khoảng 55 dòng thêm, `packet_loop_test.py` khoảng 180, `launcher.py`
  khoảng 15, `launcher_test.py` khoảng 70; tổng khoảng 320. Đo lại bằng numstat trước khi công bố.
- `review_class` chưa đo bằng `_tinh_lop_tu_write_set`; suy từ tiền lệ #1313/#1375 (`.claude/dev/*` ⇒ `sensitive`).
- Codex CLI thật, khi bị rate-limit 429 hay từ chối quyền, có in khung `response.created` trước lỗi không: CHƯA ĐO. Nếu có
  thì lời gọi ấy không hoàn được qua dạng (B), và đúng là không được hoàn (máy chủ đã tạo response). Tỉ lệ ca thật hoàn
  được là không biết.
- Head của workspace reviewer có bằng head PR không: tuỳ cách gọi. Đặc tả đòi `head` bản ghi bằng `head` của mục; gọi
  codex từ một worktree khác head thì không hoàn được, theo hướng fail-closed.
- Chưa chạy toàn bộ `packet_loop_test.py`/`launcher_test.py` trên base để lấy số N/N và tập bỏ qua làm mốc. Executor đo
  trên exact base của lease.
- Đường v3 có thật sự bị ca D13 đo hay không (cần một state v3 hợp lệ do fixture wp1174 dựng): chưa đo; nếu fixture đắt,
  ca D13 có thể chỉ khoá vế `schema` của `_load`, và phải khai rõ phạm vi ấy.

## 9. Câu hỏi cho chủ kho (trước khi duyệt băm)

- **Q1.** Đóng #177 cùng packet này? Theo §0.1, ý chính đã do #775 làm và có ca chạy được. Phần còn lại ("lượt void vì
  quota không ăn ngân sách") chính là #804. *Khuyến nghị: có*, đóng với comment trỏ §0.1 và các ca `pl_m3_neo_loi_goi`,
  `r804_*`.
- **Q2.** Có cần cửa hoàn do người duyệt (`--khong-co-bang-chung --ai-cho-phep ducthangho --can-cu URL`) cho lời gọi chết
  ở probe (launcher không ký) hay chạy không qua launcher? *Khuyến nghị: không*, vì `nang-tran` đã là cửa có người duyệt và
  có ghi sổ; thêm cửa thứ hai là hai cơ chế cho một việc.
- **Q3.** Giữ schema 3 ngoài phạm vi (bộ đếm v3 đơn điệu theo thiết kế wp1174)? *Khuyến nghị: có*; hoàn trên v3 là một
  packet riêng của lane wp1174, nếu cần.
- **Q4.** Câu thứ hai của #804, "run_id bịa có thể làm cạn ngân sách": chỉ đóng hướng "hoàn không bằng chứng", không bắt
  `record-codex-call` đọc hiện vật launcher (vì nó giữ chỗ TRƯỚC lời gọi)? *Khuyến nghị: có*. Bịa run_id chỉ đốt ngân sách
  của chính người bịa (fail-closed), và lời gọi bịa vẫn không neo được review nào nếu không có review thật. Muốn đóng hẳn
  thì phải đổi `record-codex-call` sang ghi SAU lời gọi, đụng ADR-0048; đó là quyết định lớn hơn packet này.

**Trả lời của chủ kho (2026-11-18, phiên điều phối #1206, qua AskUserQuestion):** Q1 có — đóng #177 cùng packet;
Q2 không — không thêm cửa hoàn do người duyệt; Q3 có — giữ schema 3 ngoài phạm vi, fail-closed; Q4 có — chỉ chặn hướng
"hoàn không bằng chứng", vế "run_id bịa đốt ngân sách" ghi thành nợ có tên, không đổi ADR-0048 trong packet này.
