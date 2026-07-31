# PROMPT BÀN GIAO sau lượt 26 — 31-07-2026

Q-A / Q-B(nhánh 45-2019) / Q-C của `PROMPT_TIEP_NLM_2026-07-31b.md` **ĐÃ THI HÀNH XONG**.
**KHÔNG chạy lại** — mỗi mục đều có readback keyed + đối soát vật lý làm bằng chứng.

★★ **ĐỌC KÈM: hai sổ, một đợt việc.** Cùng đợt duyệt này có **HAI phiên chạy song song** trên notebook
45739ff7 — `rasoat/KETQUA_US_NLM_QUEUE_2026-07-31.md` §8-§11 (commit `5c12dd6`) và
`rasoat/KETQUA_NLM_QA_QB_QC_2026-07-31.md` (phiên này). Phân định quyền tác giả chính xác nằm ở **§4.4**
sổ sau. Tóm tắt: Q-A + Q-C + rename/add canonical do phiên sau làm; **gỡ raw `04e51f9c` + register do
phiên `5c12dd6` làm trước 59 giây**, phiên sau chạy trùng (idempotent, không hư hại).
★ Cổng dedup-live của `nlm-add` đã tự chặn va chạm `add` — nhưng `nlm-source-remove --force` và
`register` **KHÔNG có cổng nào**. Trước lô ghi NLM/registry: `git fetch origin master` + kiểm xem có
phiên khác đang mở cùng đợt không. Chốt này CHƯA được cưỡng chế ở đâu cả.

Trạng thái chốt: `nlm-audit-physical` **rc=0 `clean:true`** (pointer_dead=0 · dup_physical=0 ·
pointer_mismatch=0 · unregistered_physical=0) · `nlm-reconcile --all-notebooks` **desync_real=0/0/0** ·
`coverage_gap=0` trên 45739ff7.

## Slot LIVE sau lượt 26 (dùng cột này, KHÔNG dùng registry)

| notebook | LIVE | trống |
|---|---|---|
| 743ed200 (nền) | 299/300 | 1 |
| 45739ff7 (VBQPPL-2) | 292/300 | 8 |
| 2d8c2fef (ILO/điều ước) | 22/300 | 278 |
| 80742228 | 108/300 | 192 |

## Còn lại — CHỜ DUYỆT

**R-1. `CU_ILO-128` trùng CHÉO notebook** (tồn sẵn, lộ ra sau khi gỡ dup Công đoàn).
sid `c4f16911-f255-4876-9735-ad7c3fa40964` nằm vật lý trên **45739ff7** nhưng registry chỉ biết bản
`a8e7b4e8-b790-490e-b623-e33af70a7a39` trên **743ed200** (row `1All5aL5HNRwXSYSsibTLGrZb234xx5gDBjpcUuoKibE`,
corpus=true). Trước khi quyết: `nlm-content <cả hai sid> --no-fallback` + so sha256 (nếp §2 sổ lượt 26).
- (a) gỡ `c4f16911…` khỏi 45739ff7 nếu nội dung trùng — 743ed200 giữ bản registry biết;
- (b) hoặc đăng ký nó thành dòng riêng nếu nội dung KHÁC.
★ `nlm-audit-physical` **không bắt** ca này (dedup trong-notebook) — phải đọc `nlm-reconcile <nb>`.

**R-2. `removed_family_still_live = 7`** trên 45739ff7 — chưa điều tra lần nào. Cần liệt kê rồi phân loại
trước khi đề xuất.

**R-3. Row Công đoàn `1MogfQLK-pZgJ7Wt_O2HJF5WGtODCBvLnS6GjEo4k9KI` SAI so với vật lý** — sổ ghi
`on_nlm=False` + `nlm_status=removed_by_user`, nhưng sid `1e9d957b` **SỐNG thật** trên 45739ff7
(`nlm-list` + `nlm-content` rc=0). Dòng này corpus=true ⇒ nhiều khả năng bị đếm oan vào
`CORPUS_TRUE_NOT_ON_NLM` (53 → có thể 52).
★ `nlm-audit-physical` **không bắt** vì `pointer_mismatch` chỉ soi dòng tự nhận `on_nlm=true`; sai theo
chiều "sổ nói đã gỡ mà vật lý CÒN" thì lọt lưới — cùng họ lỗi với ca 176-khuyết ở lượt 25.
Sửa = `register --drive-id 1MogfQLK… --nlm-status pushed` sau khi verify vật lý. Chưa duyệt nên chưa ghi.

**R-4. `raw_on_nlm` còn 3 nguồn** (duyệt lượt 26 chỉ phủ nhánh 45-2019 — nhánh đó XONG):
```
1PWj5iUJb1pcd5Q1TItAeDhuZvqrdgdK2     TL_ILO_2026_AI_tao_sinh_va_viec_lam_VN        9c0611ad…
19_6Mp_8e1NQerD5ed42A5TRlO7W14VWt     VBT_PL_BC_BHXH_HaNoi_khao_sat_6-2026.pdf      c0d3c268…
1h0kl-G4-8l7r_rvOMSlVlXu3su1IwSvU     VBT_BC_BHXH_HaNoi_thuc_hien_CS_BHXH_2025.pdf  52f8ac58…
```
★ 2 nguồn PDF cần phiên **CÓ MCP notebooklm** — hai container gần nhất (lượt 25, 26) đều KHÔNG có.
Phác đồ: convert GDoc → re-push → gỡ raw + reg_clear mapping.

**R-5. `CORPUS_TRUE_NOT_ON_NLM` = 53** — nợ CẤU TRÚC do trần 300/notebook. 9 slot dôi không đủ; muốn về 0
phải mở shard mới. Trừ R-3 ra trước khi đếm lại (có thể là 52).

## Nếp bắt buộc (đã trả giá — lượt 25 + 26)

- `nlm-content` **luôn kèm `--no-fallback`** khi đo nguồn sống/chết (mặc định fallback CORPUS gây dương giả).
- `reg-query --live --json`: **tách stdout khỏi stderr** rồi parse; `2>&1` cho `count=None` GIẢ.
- Cổng dedup-live theo **TÊN VẬT LÝ trên NLM**, không theo tên registry — hai bên có thể LỆCH (ca 45-2019).
  Gỡ va chạm bằng **đổi tên cho khớp sổ**, KHÔNG dùng `--skip-live-check`.
- `nlm-source-remove` fail-closed `POINTER_STILL_ATTACHED` là ĐÚNG — dùng `--force` (vật lý trước, sổ sau),
  rồi `register --nlm-status removed_by_user`.
- `register` có thể trả `verified:false` + `FIELDS_DROPPED_ON_WRITE` mà **field đích vẫn vào** ⇒ đọc
  readback keyed rồi mới kết luận, đừng chạy lại mù.
- **`nlm-audit-physical` ≠ `nlm-reconcile`** — cái đầu dedup trong-notebook, cái sau bắt trùng chéo-notebook.
  `clean:true` KHÔNG đồng nghĩa sạch toàn cục. Đọc cả hai.
- Gỡ nguồn trùng: đo `nlm-content --no-fallback` + **so sha256** hai bản trước khi gỡ.
- `slot-audit` LIVE là chân lý; notebook gợi ý trong prompt có thể đã FULL.

## Ngoài phạm vi (giữ nguyên)

Note dup↔bản chuẩn (cần đường đọc cột note GAS) · lô 3b 43 tên thiếu chủ đề (chạy lệnh quét năm r276
trước) · r vá auditor/doc-text · sheet-dup `1Qja1Lwp…` Kế toán (**CẤM `reg-delete`**) · 43 row_kind
overflow · quarantine hẳn bản khuyết 176 `1auEnrsy…` · BC thẩm tra mẫu P9.
Deploy: **nợ 0** (Drive = v1.36.16). Lượt 26 KHÔNG đụng code/deploy.

## Việc sổ sách còn thiếu

Memory topic `rasoat-hoso-orchestration-plan` **chưa cập nhật cho lượt 26** — container lượt 26 không có
công cụ memory. Phiên có memory hãy chép §5-§7 sổ `KETQUA_NLM_QA_QB_QC_2026-07-31.md` vào ĐẦU topic.
