# Cross-review wp943 r1 g1 — lượt 1/2 (lớp sensitive)

Bạn là REVIEWER độc lập (họ openai) cho packet `wp943` của kho `ducthangho/tra-luat`. Executor là Claude.
Bạn KHÔNG sửa cây `cay-kho/`. Bạn CHỈ ghi vào `VERDICT.md` ở thư mục hiện tại (cwd), và có thể dựng
bản sao tạm bằng `mktemp -d` nếu cần thử đột biến.

## Hiện vật trong cwd
- `SPEC.md` — đặc tả đóng băng (sha256 `22729e93eec0e1c4677a5d6529b81f9f0c46c47f3f605017b7abb337b5e1e270`; hãy băm lại).
- `LEASE.yaml` — lease `wp943-r1-g1-claude`.
- `diff.patch`, `numstat.txt` — diff `3e973a03b151e37cd402e0a723816eeaa8247193..eb5e5bf119358babf831d2aec0ee27c7e5896c1f`.
- `cay-kho/` — clone đầy đủ, checkout detached ở `reviewed_sha = eb5e5bf119358babf831d2aec0ee27c7e5896c1f`
  (base `3e973a0` có trong lịch sử). Không có mạng; đừng fetch.
- `selftest.log` (executor chạy `python scripts/tl.py --selftest` trên eb5e5bf), `dcc-base.json` / `dcc-head.json`
  (`doc-claims-check --strict --json` ở base và head).
- `ISSUE835-comment-6407154789.txt` — bản đọc qua API của comment mà diff trích dẫn (đọc ngược về: html entity
  có thể là tạo tác của công cụ đọc, đừng ghi thành finding).

## Việc
1. Ghi `VERDICT.md` NGAY khi bắt đầu (dòng `verdict: dang_review`, `reviewed_sha: eb5e5bf…`), rồi cập nhật dần sau
   mỗi hướng — lượt có thể bị ngắt giữa chừng.
2. Đối chiếu diff với SPEC mục M1/M2 từng ý: Trạng thái, Hiệu lực (giữ câu đo lịch sử 19-10/25-10), luật áp dụng
   (chỉ lease SAU mốc khai 360; lease trước giữ số, kể cả lease của chính wp943 khai 30), §20 dòng ADR-0056, §4 giữ
   nguyên, không đụng phần §4 của #834 (cửa `accept`), không đổi số 360, không đổi mục *Những gì KHÔNG đổi* /
   *Vì sao sáu giờ* / *Không hồi tố*, không bịa SHA/giờ cho mốc kích hoạt.
3. Tự CHẠY lại trong `cay-kho/` (đặt `git config core.abbrev 7` đã có sẵn; `export PYTHONDONTWRITEBYTECODE=1`):
   - `python .claude/dev/packet_loop.py adr-song --root .` (đòi rc 0)
   - `python .claude/dev/packet_loop.py doctrine-scan --root .` (đòi rc 0)
   - `git diff --check 3e973a0 HEAD` (đòi rc 0)
   - `rg -n "CHƯA KÍCH HOẠT VẬN HÀNH|chưa kích hoạt vận hành" docs/adr/0056-* docs/PROTOCOL_DA_PHIEN.md` (N3)
   - `python scripts/tl.py doc-claims-check --strict --json` ở HEAD và ở base (dùng `git worktree` KHÔNG được —
     dùng `mktemp -d` + `git clone` cục bộ rồi checkout `3e973a0`), so delta.
   - Nếu đủ thời gian: `python scripts/tl.py --selftest`, đọc dòng `== tl selftest N/N ==`.
4. Kiểm tính ĐÚNG của từng lời khai trong văn bản mới: trích dẫn #835 có khớp nguyên văn comment không; câu
   "lease `wp943-r1-g1-claude` … vẫn khai 30" có khớp `LEASE.yaml` không; còn câu nào trong ADR-0056 hoặc protocol
   (ngoài hunk) trở nên SAI/mâu thuẫn sau khi kích hoạt (vd mục *Không hồi tố*, §4 dòng 271 và ~283, các dòng §20
   khác như ADR-0017 nhắc ADR-0056) — nếu có, đó là finding (kể cả khi đặc tả bảo giữ nguyên thì nêu rõ).
5. Kiểm trần: ≤ 2 tệp, ≤ 80 dòng thêm, chỉ write set.

## Bảng SĂN — ≥ 6 hướng ĐỘC LẬP, mỗi hướng có LỆNH + OUTPUT THẬT
Dạng:
```
HƯỚNG <n>: <tên>
  giả thuyết : <nếu ... thì ... sai>
  lệnh       : <lệnh đã chạy>
  output     : <output thật, cắt gọn>
  kết luận   : LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC
```
Các việc bắt buộc ở mục 3 KHÔNG được tính là hướng săn. Hướng nào cần soạn nội dung đặc biệt thì mô tả bằng lời.

## Dạng VERDICT.md
```
verdict: approve | changes_requested | blocked
reviewed_sha: eb5e5bf119358babf831d2aec0ee27c7e5896c1f
## BẢNG ĐO   (khẳng định | PR khai | đo được | khớp?)
## BẢNG SĂN
### <slug>  [P0|P1|P2|P3]  <tiêu đề>   (mỗi finding: TỆP/DÒNG, VẤN ĐỀ, ĐÃ THỬ NGHIỆM, ĐỘ TIN)
```
`approve` chỉ khi không còn P0/P1/P2. P3 = gợi ý không chặn. Kết thúc bằng dòng `# XONG`.
