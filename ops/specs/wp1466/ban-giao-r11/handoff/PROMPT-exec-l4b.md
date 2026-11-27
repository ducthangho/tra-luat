# Executor wp1466 (#1466) lượt 4b — viết nốt HANDOFF-l4, Claude Opus 5.5

Bạn tiếp tục công việc của executor lượt 4 (Claude Fable 5.2). Phiên lượt 4 dừng giữa chừng vì API hết credit. **Mã đã xong và đã commit.**
Việc của bạn chỉ có hai: **ĐO nốt phần còn thiếu** và **VIẾT bản handoff**. Viết tiếng Việt.

- Thư mục hiện tại là clone `kho/`, nhánh `claude/wp1466-r11-g3`.
- HEAD phải là `c5d44c93b4aa9326fa087af0bd07cbe918c2adc2`. Nếu không phải thì DỪNG và báo.
- Thẩm quyền:
  - lease `wp1466-r11-g3-claude` (`git fetch origin ops/wp1466-r11-g3-lease`, commit `ca001f8`);
  - đặc tả r11 trên master `6a4f52d`, sha256 `9a41aa6c9d25f3bf884bc293284e3aa2f05613232c7cce8b6b2640c942dbd910`.
- Chủ kho đã quyết (E2, #1466 issuecomment-7209430125): Opus 5.5 viết nốt handoff, KHÔNG sửa mã, KHÔNG commit.

## Đọc trước
- `../PROMPT-exec-l4.md`: chỉ thị gốc của lượt 4. Handoff của bạn phải trả lời đúng mục *Đầu ra* trong tệp đó.
- `../out/HANDOFF-l4.md`: bản ghi sớm của Fable lượt 4.
- `../out/HANDOFF-l2.md`: khuôn handoff đầy đủ của lượt trước. Dùng đúng cấu trúc ấy.
- `.claude/skills/work-packet/SKILL.md` và `docs/PROTOCOL_DA_PHIEN.md` §7. Đọc nguyên văn.
- Log của lượt 4:
  - `../out/log/l4-*.log`;
  - `../out/manh-h4/`: 16 mảnh, có `manh/*.json` và `log/*.log`;
  - `../out/l4/`: có patch và script đo.

## Việc
1. **Chạy job gom cho 16 mảnh**, đúng lệnh mà lượt 1 và lượt 2 đã dùng. Lệnh nằm trong `../out/HANDOFF-l2.md` mục 5, N6 (e), và trong `../out/sc/chay_manh.py`, chế độ `gom`.
   Đòi bằng chứng dương: dòng `GOM: ĐẠT · 16 mảnh · <n> ca bắt buộc` cùng dòng `mọi mảnh khớp phân hoạch`.
2. **Đối chiếu lại tại chỗ** từng con số mà bản ghi sớm khai, bằng cách đọc log, đừng chép lại lời khai.
   Ô nào không có log hoàn tất thì ghi `KHÔNG ĐO ĐƯỢC` kèm lý do, không bỏ trống.
   - numstat so với `6a4f52d`;
   - N1–N12;
   - các vòng đột biến;
   - `doc-claims-check`;
   - selftest;
   - ruff delta.
3. **Bảng lớp.** Phải có đủ các lớp sau:
   - `ca-id-chi-do-mot-gia-tri` (P3): mọi đường vào, ca, đột biến, và kết quả giết của từng đột biến. Lấy từ `../out/log/l4-db-moi.log`.
   - `phep-dem-ban-sao-khong-phu-ca-tep` (P2): đã chuyển sang #1469, nợ `INV-KHOA-BAN-SAO-DINH-CHU`, theo E3. Ghi là chuyển, KHÔNG ghi đã vá.
   - Các lớp cũ.
4. **Khai thẳng trong handoff:**
   - toàn bộ mã của H do Fable 5.2 viết ở lượt 1–4;
   - bạn (Opus 5.5) chỉ đo và viết handoff;
   - lượt 4 dừng vì hết credit.

## Cấm
- KHÔNG sửa tệp nào trong `kho/`.
- KHÔNG commit, push, mở PR hay merge.
- KHÔNG gọi reviewer.
- KHÔNG `workflow_dispatch`.
- KHÔNG đụng secrets.
- KHÔNG chạy lệnh có `--apply`, `source-delete`, `reg-delete` hay `--clear-stale`.
- Tệp tạm đặt trong `../out/`.

## Đầu ra
Ghi đè `../out/HANDOFF-l4.md` bằng bản đầy đủ. Dòng cuối có dạng:
`HEAD=<sha> TEST=<n/n> NUMSTAT=<+a -d> TRAN=<dat|vuot> DOC_CLAIMS=<ok|do> P3=<dong|mo>`.
