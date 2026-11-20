# Review offline MÃ — wp1236 r9 đợt A, lượt 2 — reviewer độc lập (ADR-0060 M12: review trước push)

Bạn là reviewer ĐỘC LẬP, read-only, cho MÃ của một work packet. Kho: ducthangho/tra-luat.

## Quyền
- CHỈ ĐỌC trong `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a-2-codex/repo`: không sửa, không commit, không push. Không gọi GitHub/mạng.
- Được tạo tệp nháp/script đo/bản sao đột biến CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a-2-codex/work/`.
- Hướng thử nào đòi soạn nội dung tấn công thì MÔ TẢ BẰNG LỜI; dựng biến thể bằng cách sửa BẢN SAO fixture thật là được.

## Đầu vào
- Ứng viên: `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a-2-codex/repo`, HEAD `6f7ccf10f2441d0c97b779cfa77ff2839b56fc47` (tree `cfa758558f5d725e4e7016d16745c0d4bf155353`), ba commit trên `origin/master` `0f9aa2a` (lượt 1 review `1719d6e`; hai commit sửa sau đó). Diff: `git diff origin/master...HEAD` (3 tệp, +1093/−0); phần sửa sau lượt 1: `git diff 1719d6e HEAD`.
- Đặc tả đóng băng: `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a-2-codex/SPEC.md`, sha256 `e3efa593c6dbbd15a0850702dfbc927ce51c3f1361642292e2f0b235c1bee6a8` (cũng ở `refs/remotes/origin/claude/spec-1236-r9` @ `176feba`). Kiểm sha256 trước; lệch thì dừng. Phạm vi đợt A = mục *Module mới*, *muc_tieu* 1–3, *nghiem_thu* bảng Đợt A.
- Lease: `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a-2-codex/LEASE.yaml` (write set 3 tệp, trần ≤ 3 tệp / ≤ 1100 dòng thêm).
- Bản tham chiếu đo của phiên soạn đặc tả: `git show refs/remotes/origin/claude/spec-1236-r9:ops/reviews/wp1236-r9-soan/thamchieu.py` (và `do_loi_khai.py`). Đặc tả là chuẩn khi lệch.
- Đọc thêm: `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` §8 · `ops/land_evidence_nguon.py`, `ops/land_evidence_nguon_test.py` (nếp bộ phân hạng đột biến) · `ops/kiem_ho_so_land.py` · `.claude/dev/packet_loop.py` (`CHECK_BAT_BUOC`).

## Việc phải làm (theo thứ tự ưu tiên)
0. **Từng finding lượt 1 CỦA BẠN** (`/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a-2-codex/VERDICT_LUOT1_CUA_BAN.md`): ĐÓNG / CÒN MỞ, kèm phép đo; thử lại chính các probe và mutant của bạn (drop_head, drop_schema, drop_waiver_call, YAML list/hỏng/symlink, vòng alias) trên HEAD mới. Bản sửa không được làm hỏng chốt khác (hồi quy).
1. **Mã có đúng đặc tả không?** Từng hàm/hằng/tên lý do của mục *Module mới* (K1–K8, `loi_khai`, `token`, `tep_danh_gia`, `la_landed`, `kiem_mien` với tên điều kiện cố định, `kiem_ho_so`, CLI và mã thoát). Chỗ nào lệch, nói rõ đặc tả hay mã đúng, kèm phép đo.
2. **Có lời khai dương nào qua `kiem_ho_so` mà không có tệp danh-gia khớp provenance của run land thật** (ngoài giới hạn đã khai ở `chua_do_duoc`/`ngoai_pham_vi`)? Có chặn oan dữ liệu thật không (chạy trên `ops/land/**`: phải ra 47/10/9 và 25/56/39/50)?
3. **Bộ test có răng không:** chạy `python3 -B ops/gate_output_doi_chieu_test.py` (đòi `CA 30/30 · DOT BIEN 58/58 · TU KIEM PHAN HANG: DAT · TONG: DAT`); thử thêm đột biến của riêng bạn trên các chốt (bản sao tạm, `-B`), báo cái nào SỐNG; kiểm mỗi đột biến chết đúng ca đích, không chết vì lỗi vô can. Ca nào phụ thuộc thứ không có trong CI (lịch sử git, symlink, mạng, Python < 3.12 cho `tarfile filter="data"`)?
4. `python3 -m ruff check --select F` trên ba tệp; `python3 -B .claude/dev/ci_dang_ky_test.py`; numstat so trần; `git diff --check`.

## Đầu ra — in ra ĐÚNG khối sau làm phần cuối câu trả lời (Markdown)
```
# VERDICT wp1236 r9 đợt A lượt 2
reviewed_sha: 6f7ccf10f2441d0c97b779cfa77ff2839b56fc47
spec_sha256: <sha256 bạn đo được>
## Finding lượt 1 của tôi
- F0x: ĐÓNG | CÒN MỞ — <một câu>
## Findings mới
- id: G01
  severity: P0|P1|P2|P3
  vi_tri: <tệp:dòng>
  van_de: <một câu>
  bang_chung: <lệnh đã chạy + output rút gọn>
  de_xuat: <sửa thế nào>
## Đã đo lại, khớp
- <liệt kê ngắn>
KET_LUAN: approve | changes_requested
```
Quy tắc: `approve` CHỈ khi không còn P0, P1, P2. P3 không chặn. Mỗi P2 trở lên phải có phép đo. Dòng `KET_LUAN:` là dòng cuối cùng.
Ghi VERDICT tăng dần vào `/tmp/claude-0/-home-user-tra-luat/6c4ac791-21bc-5b0f-932d-b09a8580dddc/scratchpad/review/a-2-codex/work/VERDICT.md` trong lúc làm.
