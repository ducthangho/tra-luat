# Review offline MÃ — wp1236 đợt B theo đặc tả r12 — lượt 1 — reviewer độc lập, theo PROTOCOL §8.3 và ADR-0060 (M2, M12: review trước push)

Bạn là reviewer ĐỘC LẬP, read-only, cho MÃ của work packet `sensitive` wp1236 **đợt B** (luật L8 trong `ops/land_evidence_nguon.py`). Kho: ducthangho/tra-luat. Đây là lời gọi Codex **1/4** của đợt B (trần chủ kho, #1236 issuecomment-7129998930). Effort: high (chủ kho chỉ định).

## Bối cảnh
- Đợt A (module `ops/gate_output_doi_chieu.py` + test) đã land trên master (`9d61d4e`, PR #1502). Đợt B NỐI module ấy vào cổng `ops/land_evidence_nguon.py` thành luật **L8** + hằng `MIEN_TRU_L8`, theo đặc tả r12 (`SPEC.md`, sha256 `4589daf1fd666b03a68b7d7dcd5c60903c10e946963fd324c9ee6185ed8e2dc7`): mục *Luật mới ở hai cổng* (dòng L8), đoạn `MIEN_TRU_L8`, *Hệ quả cho hồ sơ mới*, bảng *Đợt B* (B1–B8), *Ma trận chốt–ca–đột biến* (luật 1–9), *kich_thuoc*, *Kiểm chứng theo nền*, *luat_dung*.
- **Quyết định chủ kho áp cho luật 9 ở đợt B/C** (E3, #1236 issuecomment-7130670276) — ĐÂY là định nghĩa miền bắt buộc, thay cho chữ "(A) = manifest trên module ở head" khi module có mã cũ:
  1. Miền **DELTA + không hồi quy**: miền bắt buộc = đột biến của manifest head KHÔNG phải bản kế thừa của manifest base (tách bằng `quet_dot_bien.py hoi-quy <manifest base> <base.py> <head.py>` + so sha256). Mọi đột biến delta phải `GIET` (chết vì `TinHieuChotCa` của đúng ca) hoặc `TUONG_DUONG` có chứng minh. Phần kế thừa: bảng so từng ID base↔head, đòi **0** ID `GIET` ở base mà `SONG` ở head. Đột biến sống sẵn của mã cũ (L1–L7) là NỢ, KHÔNG phải finding của đợt B. Phần còn lại của luật 9 (thứ tự xét, P3 `ngoai_bang_dong` cho đột biến bạn tự dựng ngoài manifest) áp cho miền delta. Kho (B) của đợt B rỗng.
  2. Cho phép test đợt B nhận bí danh biến `GATE_OUTPUT_DOI_CHIEU_MA` (một dòng, có chú thích) để lệnh `do` nguyên văn đo được.
- Executor: Claude Fable 5.2 high, phiên `session_015Gtxraj8uybNKhrrYZSKtB`. Lease `LEASE.yaml` (write set: `ops/land_evidence_nguon.py`, `ops/land_evidence_nguon_test.py`; trần ≤ 6 tệp / ≤ 450 dòng thêm theo ADR-0053).

## Quyền
- CHỈ ĐỌC trong `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/b1-1-codex/repo`. Không sửa, không commit, không push. Không gọi GitHub/mạng.
- Tệp nháp, bản sao để đột biến, thư mục đo: CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/b1-1-codex/work/`. Đột biến luôn chạy trên BẢN SAO, không trên `repo`. Hướng thử nào đòi soạn nội dung tấn công thì MÔ TẢ BẰNG LỜI.

## Đầu vào
- Ứng viên: `repo` ở HEAD `f4e93b366d7014e3efd464b2018e8ec7a4f8576c` (tree `ef68fdd1…`), cha = base lease `f602325574c62184caf16309631f5f680ca5cee2`. Diff: `git diff f602325 HEAD`.
- `SPEC.md` (kiểm sha256), `LEASE.yaml`.
- Bằng chứng executor `bang_chung/` — LỜI KHAI, ĐO LẠI những gì quyết định kết luận:
  - `handoff.yaml` (có mục `lua_chon_can_reviewer_biet`: nạp module bằng `importlib.util` + `exec(compile)` không qua `.pyc`; nạp module đứng TRƯỚC xét miễn trừ; `SystemExit` từ module thành KHÔNG ĐO ĐƯỢC; ca L1–L7 cũ chạy với module đối chiếu câm, ca B dùng module thật; cổng trên cây thật chậm ~2 s → ~7 s).
  - `gates/`: bộ test đợt B `CA 33/33 · DOT BIEN 140/140 · TU KIEM DAT · TONG DAT`; `land_evidence_nguon --root .` rc 0 (174 hồ sơ); thử ghép master `5259239` rc 0 (175); selftest 1786/1786; ruff F delta 0; `git diff --check` 0; `ci_dang_ky_test` 1226/1226; `kiem_ho_so_land` đỏ sẵn delta 0; numstat 2 tệp +342.
  - `luat9/`: `do` base `f602325` 550 = 335 GIET/187 SONG/28 VO_CAN; head 624 = 438/173/13; tách 548 kế thừa + 76 delta, 76/76 GIET; kế thừa 0 hồi quy (`so-base-head-f4e93b3.md`, `ke-thua-base-len-head.chi-muc.jsonl`, `so_base_head.py`).
  - `do-l8/`: phép đo tập ĐỎ L8 trên base (`do_l8.py`, `do_l8_base.json`) — 56 mục `MIEN_TRU_L8`, khai trùng tên + byte danh sách đặc tả.
- Đọc thêm: `repo/CLAUDE.md` · `repo/SKILL.md` (WM-01…06, deterministic gates) · `repo/docs/PROTOCOL_DA_PHIEN.md` §8, §8.3, §12 · `repo/docs/adr/0060-dieu-kien-merge-va-moc-ready.md` (M2, M3) · module đợt A `repo/ops/gate_output_doi_chieu.py` và khuôn test `repo/ops/gate_output_doi_chieu_test.py`.

## Việc phải làm
1. **Mã khớp đặc tả L8**: chạy SAU chốt `MIEN_TRU_CUTOVER`; hồ sơ không thuộc `MIEN_TRU_L8` (khớp băm) ⇒ mỗi vi phạm của `kiem_ho_so(du_lieu đã nạp, thư mục provenance)` thành một dòng `L8 <đường dẫn>: <lý do>`; module nạp từ `<gốc của --root>/ops/gate_output_doi_chieu.py`; không nạp được ⇒ KHÔNG ĐO ĐƯỢC rc 2, KHÔNG BAO GIỜ ĐẠT; docstring LUẬT có câu về văn xuôi ngoài khoá `gateoutput`. Xét các lựa chọn executor tự khai (thứ tự nạp module trước miễn trừ; `SystemExit`; `exec(compile)`) có trái đặc tả hay mở đường lọt không.
2. **`MIEN_TRU_L8`**: đo LẠI tập ĐỎ trên base `f602325` (dùng mã của bạn hoặc `do-l8/`), so với hằng: đủ 56, đúng băm byte, KHÔNG chứa hồ sơ được `MIEN_TRU_CUTOVER` miễn với băm khớp; bản kỳ vọng chép riêng trong test (B5).
3. **Ca B1–B8** có mặt và ĐO đúng điều đặc tả nói (không phải "có mặt" — "có đo", bài học CLAUDE.md), mỗi đột biến mB1–mB8 làm đúng ca đích đỏ bằng `TinHieuChotCa`.
4. **Luật 9 theo quyết định chủ kho**: chạy lại `do` nguyên văn trên head (và base nếu cần) bằng bộ quét ghim `repo/ops/reviews/wp1236-r10-soan/quet_dot_bien.py` (sha256 phải là `1b3e4a9e0a4608b9fd6c62e1de99bf509cfd8cb96bedb4d956bac681fc1b9c0c`); kiểm cách tách delta/kế thừa; từng `TUONG_DUONG` của delta có chứng minh đúng; bảng kế thừa 0 hồi quy. Bẫy: lệnh dài có thể bị cắt — ghi kết quả từng phần.
5. **Quét độc lập theo LỚP** (§8.3, ADR-0060 M2): khái quát mỗi biểu hiện thành lớp nguyên nhân, quét MỌI biểu hiện cùng lớp trên ứng viên trước khi báo; KHÔNG báo từng lỗi lẻ. Đột biến bạn tự dựng ngoài manifest ⇒ P3 `ngoai_bang_dong` (ghim cặp). Lỗi HÀNH VI (khác đặc tả) là finding theo mức thật.
6. **M3 (ADR-0060)**: phân loại Windows cho diff THẬT của đợt B theo bước của M3 (dòng thêm có `subprocess`/`encoding=`/`pathlib`/`os.*`…) — ghi kết luận `required`/`not_required`/`unknown` kèm dòng căn cứ. Chủ kho đã miễn Windows CI; Windows local (nếu required) do điều phối chạy.
7. Tự chạy: `python3 -B ops/land_evidence_nguon_test.py`; `python3 -B ops/land_evidence_nguon.py --root .`; `python3 -m ruff check --select F ops/land_evidence_nguon.py ops/land_evidence_nguon_test.py` (so base); `python3 -B .claude/dev/ci_dang_ky_test.py`; numstat `git diff --numstat f602325 HEAD` so trần 450; `git diff --check f602325 HEAD`.

## Mức nghiêm trọng — §8 nguyên văn
`sensitive`: approve chỉ khi 0 P0/P1/P2 mở; **mỗi P3 phải đóng** (bạn xác nhận có bằng chứng, hoặc chủ kho miễn neo exact SHA). Mỗi P2+ phải có phép đo. P3 chờ miễn: ghi `chờ miễn chủ kho`; verdict `approve` chỉ khi điều kiện duy nhất còn lại là lời miễn ấy.

## Đầu ra — HAI tệp
1. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/b1-1-codex/work/VERDICT.json` ghi tăng dần; kiểm `python3 /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/b1-1-codex/kiem_verdict_lop.py /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/b1-1-codex/work/VERDICT.json --vong 1` (phải HOP_LE; lưu stdout vào `work/kiem_verdict.txt`). Khoá: `reviewed_sha`, `spec_sha256`, `vong`: 1, `dot`: "B", `findings` [`id` B01…, `class_slug`, `severity`, `vi_tri`, `van_de`, `bang_chung`, `de_xuat`], `class_table` [`slug`, `manifestations`, `highest_open_severity`, `common_fix`, `closing_check`], `m3_windows` {`ket_luan`, `can_cu`}, `luat9` {`delta`, `ke_thua_hoi_quy`, `tuong_duong_da_kiem`}, `da_do_khop`, `verdict`.
2. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/b1-1-codex/work/VERDICT.md` — tóm tắt cho executor (bảng lớp, từng finding kèm phép đo tái lập); dòng cuối `KET_LUAN: approve | changes_requested`.
