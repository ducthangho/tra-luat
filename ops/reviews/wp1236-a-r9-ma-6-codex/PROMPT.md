# Review offline MÃ — wp1236 r9 đợt A, lượt 6 — reviewer độc lập, theo PROTOCOL §8.3 (ADR-0060 M12: review trước push)

Bạn là reviewer ĐỘC LẬP, read-only, cho MÃ của một work packet `sensitive`. Kho: ducthangho/tra-luat.

## Vì sao có lượt này
Năm lượt trước (bạn chạy, file `VERDICT_LUOT1..5_CUA_BAN.md` trong thư mục này) KHÔNG theo §8.3: không có slug lớp, không bảng lớp, dùng ĐÓNG/CÒN MỞ thay cho bốn nhãn. Chủ kho bác dùng chúng để vá hay approve. Một lớp — chốt/nhánh không có ca và đột biến bảo vệ — xuất hiện ở cả 5 lượt; executor đã xét lại cách làm (sổ uỷ quyền #1236 issuecomment-7046799415): quét đột biến AST HỆ THỐNG thay vì vá theo từng finding. Lượt này phải (1) dựng lịch sử lớp cho lượt 1–5, (2) kiểm độc lập bản vá cả lớp, (3) review toàn bộ diff theo đặc tả.

## Quyền
- CHỈ ĐỌC trong `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a-6-codex/repo`: không sửa, không commit, không push. Không gọi GitHub/mạng.
- Được tạo tệp nháp/script đo/bản sao đột biến CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a-6-codex/work/` (và chạy các script trong `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a-6-codex/quet/`, ghi output vào `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a-6-codex/work/`).
- Hướng thử nào đòi soạn nội dung tấn công thì MÔ TẢ BẰNG LỜI; dựng biến thể bằng cách sửa BẢN SAO fixture thật là được.

## Đầu vào
- Ứng viên: `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a-6-codex/repo`, HEAD `c2d606b` (`git rev-parse HEAD` phải bắt đầu bằng c2d606b; tree `9b78e9e0b1e1d445e19747e65ab4f65ea4016511`). Base `0f9aa2a`. Diff đầy đủ: `git diff 0f9aa2a...HEAD` (3 tệp). Phần mới sau lượt 5: `git diff 89fb99b HEAD` (89fb99b = sửa K01/K02 lượt 5, chưa ai review) và `git diff 028f8b3 HEAD` (028f8b3 = SHA lượt 5).
- Đặc tả đóng băng: `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a-6-codex/SPEC.md`, sha256 `e3efa593c6dbbd15a0850702dfbc927ce51c3f1361642292e2f0b235c1bee6a8` (cũng ở `refs/remotes/origin/claude/spec-1236-r9` @ `176feba`). Kiểm sha256 trước; lệch thì dừng. Phạm vi đợt A = mục *Module mới*, *muc_tieu* 1–3, *nghiem_thu* bảng Đợt A.
- Lease: `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a-6-codex/LEASE.yaml` (write set 3 tệp; trần ≤ 3 tệp / ≤ 1400 dòng thêm, nang_tran lần 3).
- Bộ quét đột biến của executor (NGOÀI kho vì trần kích thước): `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a-6-codex/quet/sinh.py` (sinh), `chay_ca.py` (chạy mọi ca trong một tiến trình, dừng ở ca đầu tiên ném `TinHieuChotCa`; thay `yaml.safe_load` bằng C loader + nhớ đệm CHỈ để tăng tốc), `chay.py` (song song 4 luồng). Kết quả executor: `kq_89fb99b.jsonl` (381 đột biến, 51 sống) và `kq_moi.jsonl` + `mutants_c2d606b.jsonl` (368, 7 sống trước m124; executor khai còn 6 sống, cả 6 chỉ chết vì lỗi vô can). Đây là LỜI KHAI của executor — đo lại, đừng tin; và soi chính bộ quét (toán tử nào nó KHÔNG sinh, nó có thể cấp tín dụng giả ở đâu, bản patch yaml có đổi ngữ nghĩa không).
- Đọc thêm: `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` §8, §8.3, §12 · `ops/land_evidence_nguon.py` · `ops/kiem_ho_so_land.py` · `.claude/dev/packet_loop.py` (`CHECK_BAT_BUOC`). Bản tham chiếu của phiên soạn đặc tả: `git show refs/remotes/origin/claude/spec-1236-r9:ops/reviews/wp1236-r9-soan/thamchieu.py`.

## Việc phải làm
0. **Lịch sử lớp lượt 1–5 (§8.3).** Đọc năm verdict cũ, gán MỖI finding cũ (F01…, G01…, H01…, J01…, K01…) đúng một `class_slug` (chữ thường, số, gạch nối, theo NGUYÊN NHÂN, ổn định). Gộp finding cùng cơ chế vào một lớp. Với từng lớp, gắn một nhãn trên HEAD hiện tại: `DA_VA_THAT` · `VA_MOT_PHAN` · `CHUA_VA` · `KHONG_DO_DUOC`, kèm phép đo (chạy lại probe/mutant cũ của bạn). `DA_VA_THAT` CHỈ khi mọi biểu hiện trong phạm vi đã đóng, không còn biểu hiện cùng cơ chế do bản vá sinh ra, và không còn phần phải đo. Thiếu quan sát hay cắt acceptance không tính là vá.
1. **Quét lớp trước khi báo.** Với mỗi lớp (cũ hay mới) bạn tìm thấy, quét MỌI biểu hiện cùng lớp trên HEAD trước khi ghi finding; không báo lỗi lẻ. Riêng lớp "chốt thiếu ca/đột biến": tự dựng thước kiểm của bạn (toán tử đột biến bộ quét của executor không có — vd đổi hằng chuỗi lý do, đổi regex, đổi thứ tự kiểm, đổi `is`/`==`, xoá `return` sớm, đổi tập `TOKEN`/`PHI_LOI_KHAI`/`CHECK_BAT_BUOC_TEN`/`BO_SINH`), chạy trên bản sao tạm với `-B`, báo cái nào SỐNG.
2. **Mã có đúng đặc tả không?** Từng hàm/hằng/tên lý do của mục *Module mới* (K1–K8, `loi_khai`, `token`, `tep_danh_gia`, `la_landed`, `kiem_mien` với tên điều kiện cố định, `kiem_ho_so`, CLI và mã thoát). Bốn chỗ rút gọn mã ở c2d606b (bỏ lọc `thu[:]`, gộp vế ket_luan_lech, bỏ `is_dir` trước glob readback, bỏ `or ""` trước `str(body)`) có thật sự tương đương không?
3. **Lời khai dương sai hay chặn oan:** có lời khai dương nào qua `kiem_ho_so` mà không có tệp danh-gia khớp provenance của run land thật (ngoài `chua_do_duoc`/`ngoai_pham_vi`)? Trên `ops/land/**` tại base phải ra 47/10/9 và 25/56/39/50.
4. **Bộ test có răng:** `python3 -B ops/gate_output_doi_chieu_test.py` phải in `CA: 36/36 dat` · `DOT BIEN: 124/124 bi giet dung ly do` · `TU KIEM PHAN HANG: DAT` · `TONG: DAT`. Mỗi đột biến chết đúng ca đích, không vì lỗi vô can? Ca nào phụ thuộc thứ không có trong CI?
5. `python3 -m ruff check --select F` trên ba tệp; `python3 -B .claude/dev/ci_dang_ky_test.py`; `git diff --numstat 0f9aa2a...HEAD` so trần 1400; `git diff --check 0f9aa2a HEAD`.

## Mức nghiêm trọng — §8 nguyên văn, KHÔNG dùng thước của prompt lượt 4–5
Review class `sensitive`: approve chỉ khi 0 P0/P1/P2 mở; **mỗi P3 phải đóng** (bạn xác nhận đã đóng có bằng chứng, hoặc chủ kho miễn neo exact SHA). P3 KHÔNG tự động "không chặn"; liệt kê đủ. Mỗi P2 trở lên phải có phép đo.

## Đầu ra — HAI tệp
1. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a-6-codex/work/VERDICT.json` — JSON, đúng khoá dưới đây; ghi tăng dần trong lúc làm. Kiểm bằng `python3 /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a-6-codex/kiem_verdict_lop.py /tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a-6-codex/work/VERDICT.json --vong 6` (phải in `HOP_LE`; lưu output vào `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a-6-codex/work/kiem_verdict.txt`).
```json
{
  "reviewed_sha": "<40 hex>", "spec_sha256": "<đo được>", "vong": 6,
  "findings": [{"id": "L01", "class_slug": "<slug>", "severity": "P0|P1|P2|P3", "vi_tri": "<tệp:dòng>",
                "van_de": "<một câu>", "bang_chung": "<lệnh + output rút gọn>", "de_xuat": "<cách vá CHUNG cho lớp>"}],
  "class_table": [{"slug": "<slug>", "finding_ids": ["L01"], "manifestations": ["<biểu hiện>"], "highest_open_severity": "P2|null",
                   "nguon": "<lượt/SHA>", "common_fix": "<cách vá chung>", "closing_check": "<phép kiểm đóng lớp>",
                   "ly_do_va_rieng": "<chỉ khi phải vá từng biểu hiện>"}],
  "prior_class_status": [{"slug": "<slug>", "finding_cu": ["F01", "..."], "status": "DA_VA_THAT|VA_MOT_PHAN|CHUA_VA|KHONG_DO_DUOC",
                          "evidence": "<phép đo trên HEAD>", "chua_do_duoc": "<phần chưa đo, nếu có>"}],
  "bang_noi_slug": [{"slug": "<slug>", "finding_cu": ["..."], "ly_do_gop": "<cùng cơ chế gì>"}],
  "da_do_khop": ["<liệt kê ngắn>"],
  "verdict": "approve|changes_requested"
}
```
`class_table` có ĐÚNG một dòng cho mỗi slug của `findings` (lớp còn mở) và có thể thêm dòng cho lớp cũ đã đóng (`highest_open_severity: null`). `prior_class_status` phủ MỌI lớp của lượt 1–5.
2. `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a-6-codex/work/VERDICT.md` — tóm tắt người đọc, dòng cuối đúng dạng `KET_LUAN: approve | changes_requested`.
