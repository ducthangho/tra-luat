# Cross-review packet wp987 r1 g1 — lượt 1 (reviewer: codex, review_class: sensitive)

Bạn là REVIEWER độc lập. Không sửa `cay-kho/` (chỉ đọc, chạy lệnh đo). Ghi kết luận vào `VERDICT.md`
ở thư mục cha của `cay-kho/` (tức thư mục làm việc hiện tại), ghi SỚM rồi cập nhật dần.

## Đầu vào (cùng thư mục với tệp này)
- `SPEC.md` — đặc tả đóng băng, sha256 9403038447154f1e2e714c40fa8561460a2bac08e8a06708923a5541a5047b15.
- `diff.patch` — diff `20a2e2b..a2e2ebf` (base = master lúc cấp lease; head ứng viên = a2e2ebf812f57254affe9344fd02530efa1a0130).
- `cay-kho/` — clone đầy đủ, checkout detached tại head ứng viên. Có `docs/PROTOCOL_DA_PHIEN.md` và `.claude/dev/launcher.py`.

## Việc
1. Đối chiếu diff với M1, M2 và ràng buộc của SPEC (adapter MỎNG, không chép doctrine protocol, giữ câu lịch sử `r368`,
   ≤ 2 tệp, ≤ 60 dòng thêm).
2. ĐO, đừng đọc: mọi tên trường `run.json` và tên lớp/hằng nhắc trong diff phải có thật trong
   `cay-kho/.claude/dev/launcher.py` và mang đúng ý nghĩa diff gán cho nó (đọc `_BoLocStderr.ghi_so`,
   `_LayMauSandbox.ghi_so`, `_ket_luan_model`, `_ket_luan_effort`, chỗ đặt `RUST_LOG` trong `lenh_run`).
   Mọi lệnh `rg` LUÔN kèm đường dẫn (thiếu đường dẫn thì rg đọc stdin và treo).
3. Kiểm từng khẳng định kỹ thuật trong diff: ví dụ "chỉ `DO_DUOC` mới là đo được", "`sandbox_trang_thai` còn có
   `KHONG_THAY_LENH`", "`sandbox_quan_sat` lấy mẫu `/proc` (chỉ Linux)", "launcher tự đặt `RUST_LOG`", lệnh Python mẫu
   chạy được (chạy nó trên một `run.json` giả bạn tự dựng trong thư mục tạm NGOÀI `cay-kho/`), đoạn PowerShell của
   `.agents` có đúng cú pháp/thuộc tính.
4. Chạy `python .claude/dev/packet_loop.py doctrine-scan --root .` trong `cay-kho/` (N1) và
   `rg -n 'stderr.log' .claude/skills/cross-review/SKILL.md .agents/skills/cross-review/SKILL.md` (N3): còn câu nào
   bảo header `stderr.log` là nguồn đo model/effort không?
5. Săn ≥ 4 hướng ĐỘC LẬP (vd: tên trường sai/thiếu; khẳng định rộng hơn mã; mâu thuẫn với phần khác của cùng adapter;
   lệnh mẫu hỏng trên Windows/PowerShell; trạng thái ngoài `DO_DUOC`/`KHONG_DO_DUOC` bị bỏ sót).

## Dạng VERDICT.md
```
verdict: approve | changes_requested | blocked
reviewed_sha: a2e2ebf812f57254affe9344fd02530efa1a0130

## BẢNG SĂN
HƯỚNG n: <tên>
  giả thuyết : ...
  lệnh       : ...
  output     : <output thật, cắt gọn>
  kết luận   : LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC

## BẢNG ĐO
| khẳng định trong diff | đo được | khớp? |

### <slug-kebab>  [P0|P1|P2|P3]  <tiêu đề>
TỆP/DÒNG / VẤN ĐỀ / ĐÃ THỬ NGHIỆM / ĐỘ TIN
```
`approve` chỉ khi không còn P0/P1/P2. P3 là góp ý không chặn.
