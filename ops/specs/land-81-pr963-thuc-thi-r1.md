# Đặc tả packet `land-81-pr963` r1 — thêm khối `thuc_thi` có cấu trúc cho hồ sơ `pr963-wp943`

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544

| trường | giá trị |
|---|---|
| packet | `land-81-pr963` (mission #748), revision 1, generation 1 |
| review_class | `sensitive` (hồ sơ land là căn cứ cho `landed`) |
| write set | `ops/land/pr963-wp943-land-evidence.yaml` |
| base | `origin/master` lúc cấp lease (đo khi soạn: `7891c0b`) |
| executor | `anthropic_claude` (Claude Code remote, Linux) |
| reviewer | `openai_codex` qua `launcher.py run`, phiên mới, read-only, neo đúng head |

## 1. Vì sao
Hồ sơ `pr963-wp943` vào master qua #970, sau khi packet `land-evidence-l7` (PR #973) đã soạn xong. Hồ sơ khai `assurance_81.reviewer_assurance_81: DAT`. Phép đo thực thi chỉ có ở văn xuôi trong `ly_do` ("effort xhigh và sandbox đo máy (DO_DUOC)"), không có khối `thuc_thi`. Vì vậy L7 làm cây thật ĐỎ khi #973 merge master (đo trên `a15027a`: 1 vi phạm, `L7 $.assurance_81.thuc_thi`).

**Lời khai trong văn xuôi là ĐÚNG.** Đo trên `ops/land/pr963-wp943-provenance/verdicts/wp943-g1-claude-review-3-codex-run.json`: run `58e19716`, head `fb2bbcb`, `ma_thoat` 0, model 35/35 `gpt-6.1-sol` `DO_DUOC`, `effort_phuc_vu` `[xhigh]` `DO_DUOC`, `sandbox_trang_thai` `DO_DUOC` (`codex-linux-sandbox` cùng `bwrap`). Hồ sơ không khai mạnh hơn phép đo; nó chỉ thiếu cấu trúc.

Không được thêm hồ sơ này vào `MIEN_TRU_L7`, vì đặc tả L7 §2 ghi "KHÔNG thêm tên mới".

## 2. Thay đổi
1. Thêm `assurance_81.thuc_thi` với ba khoá. Mỗi khoá là lời khai `measured` trỏ tới đúng `run.json` trên, ghi giá trị đúng như trong tệp:
   - `model`: số response và tên model;
   - `effort`: giá trị và trạng thái;
   - `sandbox_mode`: trạng thái, kèm tóm tắt cơ chế quan sát được.
2. Mọi khoá và giá trị khác giữ nguyên, kể cả `reviewer_assurance_81: DAT`, `ly_do` và mọi giá trị `landed`.

## 3. Tiêu chí xong
- So YAML đã nạp: chỉ `assurance_81` khác; trong `assurance_81` chỉ thêm khoá `thuc_thi`.
- Mỗi lời khai mới khớp từng giá trị với `run.json` đã dẫn.
- `ops/land_evidence_nguon.py` cho `TỔNG: ĐẠT` với bộ kiểm của master.
- Bộ kiểm L7 (PR #973, head đã merge master) cho `TỔNG: ĐẠT` trên cây sau khi áp thay đổi này, và `pr963` ĐẠT mà không cần miễn trừ.
- Review chéo Codex qua `launcher.py run` trên đúng head, tới khi 0 P0–P3.

## 4. Trần
- Kích thước: ≤ 1 tệp / ≤ 20 dòng thêm.
- Lời gọi Codex: 10 theo dòng khai ADR-0055.

## 5. Ngoài phạm vi
- Không đổi `reviewer_assurance_81`, không đổi `landed`, không sửa hồ sơ nào khác.
- Không sửa L7. Việc các phiên khác ghi hồ sơ mới chưa theo cấu trúc L7 sẽ do L7 chặn sau khi #973 vào master.
