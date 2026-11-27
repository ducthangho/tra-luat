# Executor wp1466 (#1466), lượt 4: Claude Fable 5.2, effort high

Bạn là EXECUTOR của packet `wp1466`, kho `ducthangho/tra-luat`. Phiên này là phiên MỚI. Hồ sơ các lượt trước nằm ở:
- `../out/HANDOFF.md` (lượt 1)
- `../out/HANDOFF-l2.md` (lượt 2)
- `../out/HANDOFF-l3.md` (lượt 3)
- `../out/sc/`: các script đo đã dựng

Thư mục hiện tại là clone `kho/`. Mọi trao đổi viết tiếng Việt.

## Thẩm quyền
- **Lease** `wp1466-r11-g3-claude`, nhánh `origin/ops/wp1466-r11-g3-lease`, commit `ca001f8`. Đọc bằng lệnh
  `git fetch origin ops/wp1466-r11-g3-lease && git show FETCH_HEAD:ops/leases/wp1466-r11-g3-claude.yaml`.
  - base `6a4f52dde37582df5c6a562e988d9551f45ae150`
  - nhánh làm việc `claude/wp1466-r11-g3`
  - write set: đúng bốn tệp như trước
  - trần ≤ 6 tệp / ≤ 500 dòng thêm, theo khối `nang_tran` trong lease
- **Đặc tả r11** trên master. Kiểm ĐẦU TIÊN: `git show 6a4f52d:ops/specs/wp1466.md | sha256sum` phải ra
  `9a41aa6c9d25f3bf884bc293284e3aa2f05613232c7cce8b6b2640c942dbd910`. Lệch thì DỪNG.
  Đọc các đoạn *Revision 10* và *Revision 11* ở mục 0, mục 8.1, mục 8.3 (có câu giới hạn mới và dòng G8 của bảng G), mục 10 (khối `nang_tran`) và mục 19.
- **Ba quyết định chủ kho** áp vào lượt này:
  - Q3 (E3): thu hẹp lời hứa đếm bản sao, phần còn lại chuyển sang #1469 thành nợ `INV-KHOA-BAN-SAO-DINH-CHU`.
  - E2: nâng trần lên 500.
  - E5: duyệt băm r11.

  Comment duyệt băm r11 là `https://github.com/ducthangho/tra-luat/issues/1466#issuecomment-7206141143`. Phiên điều phối đã đo `created_at` của nó bằng REST: `2026-11-27T00:04:02Z`.
- **Review mã exact-H lượt 1 trên `da4e876`** cho kết quả `blocked`. Có hai lớp:
  - P2 `phep-dem-ban-sao-khong-phu-ca-tep`: nay xử lý bằng cách thu hẹp lời hứa theo r11. Mã của phép (3) KHÔNG đổi.
  - P3 `ca-id-chi-do-mot-gia-tri`: phải ĐÓNG ngay trong lượt này.

  Verdict đầy đủ ở `../out/l4/VERDICT-ma-h-l1.md`. Hãy đọc kỹ các mục F02, và đọc script `reviewer_mutants.py` nếu có trong `../out/l4/`.

## Chỉ thị bắt buộc của chủ kho
Đọc NGUYÊN VĂN các tệp sau, không đọc theo trí nhớ:
- `.claude/skills/work-packet/SKILL.md`
- `docs/PROTOCOL_DA_PHIEN.md`: §7, §8, §8.3, §12
- `docs/adr/0060-dieu-kien-merge-va-moc-ready.md`: M1–M12
- ADR-0062 và ADR-0063
- `CLAUDE.md`
- `SKILL.md`

Quy tắc vá:
- **Vá theo LỚP.** Trước khi vá, liệt kê MỌI đường vào. Đóng cả lớp bằng một thay đổi chung. Mỗi đường vào có một ca khoá và một đột biến riêng.
- **Đóng lớp chỉ khi** mọi biểu hiện đã đóng, không sinh biểu hiện mới, và không còn phần chưa đo.
- **Không tự ghi nợ.** P2 phải vá. P3 chỉ được miễn khi chủ kho có dòng `mien_p3`.
- **Đòi bằng chứng dương** cho mọi phép đo, không tin `rc`.
- **§12:** cùng một lớp lặp từ lần thứ 3 trở lên thì DỪNG và hỏi.

## Việc
1. **Dựng nhánh.** `git fetch origin master`, rồi tạo nhánh `claude/wp1466-r11-g3` từ `origin/master` (`6a4f52d`). Cherry-pick lần lượt ba commit `a85db94`, `d5d96e7`, `da4e876` (đang nằm ở nhánh cục bộ `claude/wp1466-r9-g2`). Kiểm rằng bốn tệp của write set không đổi giữa `695916e` và `6a4f52d`. Ghi kết quả cherry-pick vào handoff.
2. **ADR-0068 phải bằng khối `adr` của r11 từng byte, sau khi điền chỗ trống theo 8.1.**
   - Khối `adr` đổi so với r9 ở đoạn Q3 và có thêm một mục *Nợ* (`INV-KHOA-BAN-SAO-DINH-CHU`).
   - Dòng Trạng thái: ngày `2026-11-27`, `spec_hash` `9a41aa6c9d25f3bf884bc293284e3aa2f05613232c7cce8b6b2640c942dbd910`, `r11`, URL `https://github.com/ducthangho/tra-luat/issues/1466#issuecomment-7206141143`.
   - Các số `{{N1}}`…`{{N6}}`: đo lại bằng đúng lệnh ở mục *Cưỡng chế* của ADR.
3. **Đóng P3 theo dòng G8 của r11.**
   - Thêm ca `doctrine_inv_*` ở cụm G8 cho ID thật (`INV-01`…`INV-28`) và cho các biên `00`, `01`, `09`, `10`, `28`, `98`. Giữ luật hậu tố, và giữ đối chứng tên nợ.
   - Thêm một đột biến thu hẹp miền số của `_INV_ID_TRAN` về đúng `99`. Đột biến này phải bị CÁC CA MỚI giết, và ba đối chứng khác họ phải còn sống.
   - Mọi thứ đăng ký đúng sổ `CASES` và `MUTANTS` theo luật N6, N7, N8 và `so-dang-ky`. Tên mới mang tiền tố `doctrine_inv_`.
   - Cố gọn: tổng numstat so với `6a4f52d` phải ≤ 500 dòng thêm.
4. **Không đụng** protocol, hằng `INV_KHOA_PROTOCOL`, hay mã phép (3). Đặc tả r11 nói mã phép (3) không đổi.
5. **Cách ghi** vào `.claude/dev/*.py` và vào ADR:
   - Chỉ dựng patch ở `../out/l4/` rồi áp bằng `git apply`.
   - KHÔNG dùng `git hash-object -w`, `git update-index --cacheinfo`, `git checkout-index`.
   - Nếu `git apply` bị chặn thì DỪNG và báo.
6. **Đo lại N1–N16** trên H mới, bằng các script ở `../out/sc/`. Trên clone SẠCH riêng ở `../out/ve5/h`, ghim `core.abbrev 7`.
   - Chạy `tl --selftest` trong một clone KHÁC với clone chạy mảnh 0. Lượt 2 đã gặp lỗi carrier vì chạy hai việc chung một clone.
   - Danh sách tối thiểu:
     - N1 với khối `adr` r11
     - N2
     - `doctrine-scan`, `adr-song`
     - `doc-claims-check --strict --json`, đòi `"ok": true` và `flags` rỗng
     - N5
     - N6, N7: tập bắt buộc, cộng ba ca "phần đầu tệp", cộng các ca G8 mới và đột biến "chỉ nhận 99"
     - N8, cả hai chế độ, so blob nền `6a4f52d`
     - `so-dang-ky`
     - ruff F: delta so base bằng 0
     - numstat ≤ 500
     - selftest N/N
     - 16 mảnh + gom
   - Tác vụ nền bị cắt ở 2 giờ: ghi handoff SỚM, cập nhật dần, dồn phần nặng chạy song song.
7. **Commit cục bộ.** Hai dòng cuối của message là:
   `Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>` và
   `Claude-Session: https://claude.ai/code/session_015GtxrcdabvDuhzgezMEE89`.
   KHÔNG viết dấu bỏ qua CI (skip + ci trong ngoặc vuông).

## Cấm
- Không push, không mở PR, không merge, không gọi API ghi.
- Không tự review, không gọi reviewer.
- Không `workflow_dispatch`, không sửa `ci.yml`.
- Không đụng secrets.
- Không chạy lệnh có `--apply`, `source-delete`, `reg-delete`, `--clear-stale`.
- Không ghi ngoài write set. Tệp tạm đặt ở `../out/`.

## Đầu ra
Ghi `../out/HANDOFF-l4.md` theo §7, gồm:
- head SHA và tree
- numstat
- cách dựng nhánh
- bảng N1–N16; ô nào chưa đo thì ghi `KHÔNG ĐO ĐƯỢC` kèm lý do
- ruff delta
- `doc-claims-check`
- bảng lớp, mỗi lớp có đủ đường vào, ca và đột biến
- những gì chưa đo
- câu hỏi cần chủ kho quyết, mỗi câu kèm mã E

Kết thúc bằng một dòng:
`HEAD=<sha> TEST=<n/n> NUMSTAT=<+a -d> TRAN=<dat|vuot> DOC_CLAIMS=<ok|do> P3=<dong|mo>`
