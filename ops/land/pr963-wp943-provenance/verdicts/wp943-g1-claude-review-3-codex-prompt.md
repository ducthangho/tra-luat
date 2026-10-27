# Cross-review wp943 r1 g1 — lượt 3/3, lời gọi Codex CUỐI (lớp sensitive, xác minh merge)

Bạn là REVIEWER độc lập (họ openai) cho packet `wp943` của kho `ducthangho/tra-luat`; executor là Claude.
KHÔNG sửa `cay-kho/`. CHỈ ghi `VERDICT.md` ở cwd (bản sao tạm thì dùng `mktemp -d`). Không có mạng.

## Bối cảnh
- Lượt 2 đã `approve` nội dung trên head `eb5e5bf119358babf831d2aec0ee27c7e5896c1f` (base lease `3e973a0`): xem
  `LUOT2_VERDICT_eb5e5bf.md`. Đó là DỮ LIỆU của lượt trước, không phải kết luận của bạn.
- Cổng `thu-hoi` đòi master là tổ tiên của head, nên chủ kho cấp thêm đúng một lượt Codex (`NANG_TRAN_943-6434092559.txt`)
  để executor MERGE `origin/master` (`a268bcc0e956f010eb4e06633676aafe1f386c37`) vào nhánh.
- Head cần review: `reviewed_sha = fb2bbcbf5ba456756df28701f97eb2ce67cd574c` (merge commit; cha 1 = `eb5e5bf`, cha 2 = `a268bcc`).
  `cay-kho/` checkout detached ở đó.

## Phạm vi lượt này (đúng như chỉ thị nâng trần)
1. Ghi `VERDICT.md` NGAY khi bắt đầu (`verdict: dang_review`, `reviewed_sha: fb2bbcb…`), cập nhật dần. Có dòng `verdict:`
   cuối cùng ngay khi đủ căn cứ; việc chạy selftest (dài) để SAU CÙNG.
2. Xác minh merge commit đúng hình dạng: đúng hai cha như trên; `git merge-base --is-ancestor a268bcc HEAD` rc 0.
3. Xác minh write set GIỐNG TỪNG BYTE với `eb5e5bf`: blob của `docs/adr/0056-lease-no-progress-six-hours.md` và
   `docs/PROTOCOL_DA_PHIEN.md` ở HEAD bằng blob ở `eb5e5bf`.
4. Xác minh phần merge mang vào KHÔNG đưa finding mới cho packet:
   - `git log --oneline 3e973a0..a268bcc -- <2 tệp write set>` phải rỗng (master không chạm write set);
   - `git diff a268bcc HEAD --stat` chỉ còn đúng 2 tệp write set, +12/−5 (diff PR thật sau merge);
   - merge không có xung đột hay sửa tay: `git diff-tree --cc HEAD` (combined diff của merge) phải rỗng, hoặc giải
     thích nếu không;
   - không có tệp nào khác trong cây HEAD khác `a268bcc` ngoài 2 tệp ấy.
5. Chạy lại trong `cay-kho/` (`export PYTHONDONTWRITEBYTECODE=1`, `core.abbrev` đã là 7):
   `python .claude/dev/packet_loop.py adr-song --root .`, `python .claude/dev/packet_loop.py doctrine-scan --root .`,
   `git diff --check a268bcc HEAD`, `rg -n "CHƯA KÍCH HOẠT VẬN HÀNH|chưa kích hoạt vận hành" docs/adr/0056-* docs/PROTOCOL_DA_PHIEN.md`,
   `python scripts/tl.py doc-claims-check --strict --json` ở HEAD, so với `dcc-master.json` (executor đo trên `a268bcc`).
6. Kiểm lại: sau merge, các câu ADR-0056/§20 có còn đúng khi đặt cạnh nội dung MỚI từ master không (vd master có thêm
   ADR hay dòng §20 nào mâu thuẫn; `adr-song` đếm khớp 1–1).
7. Cuối cùng (nếu đủ giờ): `python scripts/tl.py --selftest`, đọc `== tl selftest N/N ==`. Executor có `selftest.log`
   trên chính `fb2bbcb`. Nếu ca đỏ vì môi trường sandbox (vd ký commit Git trong kho tạm), tái hiện trên `a268bcc` và
   ghi là giới hạn hạ tầng, không phải finding.

## Bảng SĂN — ≥ 3 hướng ĐỘC LẬP về rủi ro của MERGE (không lặp 13 hướng của lượt 1–2), mỗi hướng có LỆNH + OUTPUT THẬT
```
HƯỚNG <n>: <tên>
  giả thuyết : <nếu ... thì ... sai>
  lệnh       : <lệnh đã chạy>
  output     : <output thật, cắt gọn>
  kết luận   : LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC
```

## Dạng VERDICT.md
```
verdict: approve | changes_requested | blocked
reviewed_sha: fb2bbcbf5ba456756df28701f97eb2ce67cd574c
## BẢNG ĐO   (khẳng định | executor khai | đo được | khớp?)
## BẢNG SĂN
### <slug>  [P0|P1|P2|P3]  <tiêu đề>   (TỆP/DÒNG, VẤN ĐỀ, ĐÃ THỬ NGHIỆM, ĐỘ TIN)
```
`approve` chỉ khi không còn P0/P1/P2. Kết thúc bằng dòng `# XONG`.
