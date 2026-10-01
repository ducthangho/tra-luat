# AUDIT CỦA NGƯỜI — `DOT-BIEN-L-BIEN-CONG-KHAI` (#677 / PR #689), neo `0614f7f3`

**BẢN CHIẾU, không phải nguồn có thẩm quyền.** Với verdict của một MÔ HÌNH, kho quy ước tệp có băm là nguồn
và comment là bản chiếu. Lượt `human_audited` thì NGƯỢC lại: §8 neo nó vào danh tính bền trên GitHub, mà một
tệp trong kho không mang được danh tính ấy. **Nguồn là comment `5922154333`**; tệp này để tra ngoại tuyến.

| | |
|---|---|
| nguồn có thẩm quyền | https://github.com/ducthangho/tra-luat/pull/689#issuecomment-5922154333 |
| tác giả | `ducthangho` · `author_association: OWNER` (KHÔNG phân biệt được người với phiên agent dùng token chủ kho, xem #566) |
| `performed_via_github_app` | `null` (4 comment review lượt 4–8 do phiên agent đăng mang `claude`) |
| thời điểm | `2026-10-01T00:22:42Z` (`updated_at` = `2026-10-01T00:22:42Z`, tức comment chưa bị sửa lúc đọc) |

## Phép đo bản ĐÃ ĐẾN

Đọc ngược qua REST `GET /repos/ducthangho/tra-luat/issues/comments/5922154333` (2026-10-01T01:36:23Z và
01:43:21Z, hai lần giống byte), đo trên BYTE THÔ của trường `body`:

| | giá trị |
|---|---|
| byte | **4094** |
| sha256 | `1d1e20d41fd3619662020745c6bf01611636723bd01bad18c61ddd285f1b2f83` |
| xuống dòng | LF × 45, CR × 0; không có LF cuối |
| dòng bắt đầu bằng `VERDICT:` | đúng **1** (chuỗi `VERDICT:` có 2 lần: một lần trích verdict lượt 8 giữa dòng) |
| `Reviewed commit:` | đúng **1** lần |
| SHA đầy đủ `0614f7f3…cbb52d3` | đúng **1** lần |
| chuỗi `&#` | 0 |

**Mất định dạng Markdown khi dán.** Thân ĐÃ ĐẾN không còn `##`, backtick, `**`, số thứ tự danh sách hay dòng
trống: chủ kho dán văn bản ĐÃ RENDER của bản nháp. Nội dung chữ giữ nguyên — đo: bỏ backtick, `**`, tiền tố
`#`/`1. `/`- ` và gộp khoảng trắng ở cả hai bên thì thân ĐÃ ĐẾN và bản nháp phiên điều phối khớp
(3401 = 3401 ký tự, so bằng `==`). Hai dòng neo (`VERDICT: approve`, `Reviewed commit: …`) còn nguyên. Bản nháp
KHÔNG đưa vào kho; ai làm lớp bỏ định dạng: KHÔNG ĐO ĐƯỢC.

---

## Nguyên văn (thân `body` chép từ readback, không sửa một byte)

```text
human_audited — DOT-BIEN-L-BIEN-CONG-KHAI (#677 / PR #689), người audit: @ducthangho
Tôi tự đọc git diff origin/master...0614f7f -- ops/: 1 tệp, ops/lease_publish_test.py, +600/−15. Tôi đọc cả
Issue #677 và spec r8 (ops/specs/dot-bien-l-bien-cong-khai-r8.md, sha256 4dfbfd69…4094).
Bốn chốt tôi soi trực tiếp:
Đột biến L (biên công khai của chốt lease_id ở bước đăng) có ca chết thật. Mutant L gốc làm t195,
t196, t197 đỏ (lượt 8 đo thêm t178), mỗi ca bằng thông điệp chot() của chính nó, không phải ngoại lệ
vô can. Đây là mục tiêu gốc của packet.
F-E — nhật ký gh giả nay được đo "đủ", không chỉ "có mặt". _lech_m4 so NGUYÊN dãy
GET comments → GET issues/55 → GET comments → POST, đúng thứ tự. t202 có hàng tự kiểm cho cả bốn chiều
(cắt, đảo, thiếu, thừa phía trước và phía sau). Nới hàm thành goi[:4] hay goi[-4:] làm t202 đỏ.
F-F — tiền đề của _toa_do_that theo đúng luật sản phẩm. Hạn được phân loại bằng chính _doc_han của
ops/lease_publish.py, nên …z thường và số không đệm 0 không còn lọt. schema_version cùng các trường khác
so bằng repr, nên True/1.0 không còn được coi bằng 1.
t154 không thể giết nhầm. doc_pid đợi tệp PID thành số nguyên trong hạn (vá race int('') của
30-09). Nó từ chối 0, 1, PID của chính tiến trình test, PID cha, trưởng nhóm và phiên; giá trị bị từ chối
không bao giờ tới os.kill.
Bằng chứng máy tôi đối chiếu, không tự chạy lại:
gate (ubuntu-latest) và gate-ops (ubuntu-latest) success trên đúng head này
(run 36792473622, 23:42:42Z → 23:54:07Z). Cả 16 check: 15 success, 1 skipped theo thiết kế; mergeable_state: clean.
Tại chỗ trên 0614f7f: lease_publish: 195/195 đạt; đã chạy=195, bỏ qua=0, kể cả [A]/[B] của t125.
A8: _chay_buoc_dang + t51–t68 giống từng byte với 89fc4fa. ruff F delta 0.
Review Sonnet lượt 8 trên adad5f5: VERDICT: PASS, 0 P1/P2/P3
(pull/689#issuecomment-5921648349, VERDICT sha256 63b0ac0e…5049). Merge master sau đó không đổi byte
ops/lease_publish_test.py (sha256 68169f5c…204a ở cả adad5f5 và 0614f7f).
Những điều tôi chấp nhận TƯỜNG MINH khi ký
Head cuối chưa qua nhà cung cấp thứ hai. Lượt review của lượt vá 7–8 là Sonnet 5.5, cùng họ Claude với
executor Opus 5.5, tức advisory_review. Không lượt codex nào neo head này: các lượt codex đều neo head cũ hơn, và
lượt gọi codex cuối không chạy vì hết quota, không được tính. Chữ ký của tôi THAY cho lượt cross-review ấy,
không cộng vào các lượt advisory.
Trần A7(2) đã chạm đúng 600/600. Mọi thay đổi sau này trên tệp này trong phạm vi packet phải gọn bớt dòng
do PR thêm.
Windows KHÔNG ĐO ĐƯỢC (spec Q6; tôi không cho chạy CI Windows). os.getpgid/os.getsid đã được bọc
getattr, nhưng chưa chạy thật trên Windows.
Bốn P4 để lại làm hồ sơ, không vá:
t198 đỏ oan nếu sản phẩm đổi số lần đọc vô hại. Đây là ngoại lệ có chủ đích của Q13, chỉ áp cho đường M4.
Chốt "trường khác" chỉ có răng khi gỡ cả hai nhân chứng.
Chốt pgid/sid của doc_pid chỉ có răng khi runner có pgid ≠ pid và sid ≠ ppid.
Các P4 còn lại của lượt 5–6.
Một phiên khác đã làm song song trên 211c6405 cục bộ (spec r7, không có lease). Bản đó KHÔNG land; hai
P3 nó tìm ra (F-E, F-F) đã được đo lại và vá trên nhánh này.
#687 (LEASE-PUBLISH-WINDOWS-DO) land SAU #677. #687 phải đăng ký t195–t202 vào sổ bỏ qua của nó khi
merge master.
Ghi để không ai đọc nhầm: đây KHÔNG phải một lần hạ ngưỡng. human_audited là mức hợp lệ sẵn của §8 cho class
sensitive.
VERDICT: approve
Reviewed commit: 0614f7f3781799ebacded4dff67aa9354cbb52d3
```
