# AUDIT CỦA NGƯỜI — `LEASE-PUBLISH-WINDOWS-DO` (#687 / PR #701), neo `9d7a523e`

**BẢN CHIẾU, không phải nguồn có thẩm quyền.** Với verdict của một MÔ HÌNH, kho quy ước tệp có băm là nguồn
và comment là bản chiếu. Lượt `human_audited` thì NGƯỢC lại: §8 neo nó vào danh tính bền trên GitHub, mà một
tệp trong kho không mang được danh tính ấy. **Nguồn là comment `5925449076`**; tệp này để tra ngoại tuyến.

| | |
|---|---|
| nguồn có thẩm quyền | https://github.com/ducthangho/tra-luat/pull/701#issuecomment-5925449076 |
| tác giả | `ducthangho` · `author_association: OWNER` (KHÔNG phân biệt được người với phiên agent dùng token chủ kho, xem #566) |
| `performed_via_github_app` | `null` (comment review r1–r3 lượt 2 do phiên agent đăng trên #687 mang `claude`) |
| thời điểm | `2026-10-01T05:38:09Z` (`updated_at` = `2026-10-01T05:38:09Z`, tức comment chưa bị sửa lúc đọc) |

## Phép đo bản ĐÃ ĐẾN

Đọc ngược qua REST `GET /repos/ducthangho/tra-luat/issues/comments/5925449076` (2026-10-01T05:45:32Z, và lần
hai cho biên nhận), đo trên BYTE THÔ của trường `body`:

| | giá trị |
|---|---|
| byte | **4560** |
| sha256 | `557aad4ec068e5ec7b89be636f0e5a02ac16d1b5ce6ce59387dccbdc5e417545` |
| xuống dòng | LF × 48, CR × 0; không có LF cuối; NFC |
| dòng bắt đầu bằng `VERDICT:` | đúng **1** (chuỗi `VERDICT:` có 2 lần: một lần trích verdict review r3 lượt 2 giữa dòng) |
| `Reviewed commit:` | đúng **1** lần |
| SHA đầy đủ `9d7a523e…e1813fc369f9` | đúng **1** lần |
| chuỗi `&#` | 0 |

**Mất định dạng Markdown khi dán.** Thân ĐÃ ĐẾN không còn `##`, backtick, `**`, số thứ tự danh sách hay dòng
trống: chủ kho dán văn bản ĐÃ RENDER của bản nháp. Nội dung chữ giữ nguyên — đo: bỏ backtick, `**`, tiền tố
`#`/`1. `/`- ` và gộp khoảng trắng ở cả hai bên thì thân ĐÃ ĐẾN và bản nháp phiên điều phối khớp
(3861 = 3861 ký tự, so bằng `==`). Hai dòng neo (`VERDICT: approve`, `Reviewed commit: …`) còn nguyên. Bản nháp
KHÔNG đưa vào kho; ai làm lớp bỏ định dạng: KHÔNG ĐO ĐƯỢC.

---

## Nguyên văn (thân `body` chép từ readback, không sửa một byte)

```text
human_audited — LEASE-PUBLISH-WINDOWS-DO (#687 / PR #701), người audit: @ducthangho
Tôi tự đọc git diff origin/master...9d7a523 -- ops/ (7 tệp). Phần mã là ops/lease_publish_test.py, +482/−63 so với
merge-base 20ec8d5. Sáu tệp còn lại là spec r1–r3 và lease g1–g3. Tôi cũng đọc Issue #687 và spec r3
(ops/specs/lease-publish-windows-do-r3.md, sha256 d4d6715d…543e). ops/lease_publish.py không đổi.
Năm chốt tôi soi trực tiếp:
L1 — quyền bỏ ca. main() chỉ chấp nhận BoQuaNen từ ca nằm trong sổ khai tĩnh, và phải đúng cặp
(ops-publish-lease.yml, dang). Ca ngoài sổ, hoặc ca trong sổ nhưng ném sai cặp, thì ĐỎ. Bộ giải runs-on
fail-closed: kiểm strategy/matrix/include/exclude trước mọi nhánh trả sớm, nhãn phải nằm trong danh sách cho
phép tường minh, không khớp theo tiền tố. Ca khoá là t193.
Sổ BỎ QUA đúng 12 ca, đo bằng chạy thật. Gồm 7 ca cũ (t51 t59 t60 t62 t63 t66 t68) và 5 ca của #677
(t195 t196 t197 t198 t200). Tập này lấy ra bằng cách chạy mọi ca với nền mô phỏng nt, không suy từ tên ca.
t199 tự bắt BoQuaNen nên không vào sổ. Sổ không còn mù ca ném gián tiếp qua helper (_ca_ung_vien_gian_tiep).
L2 — phép so A/B. t125 qua verifier transcript trước rồi mới so. Verifier kiểm: đủ ca, mỗi ra một trạng thái,
rc, BỎ QUA ⊆ sổ, và neo đầu dòng. Có thể nhận dòng chẩn đoán xen giữa và CRLF. Ca khoá là t194; t160 dùng
verifier thật.
L4 — seam main() không rò trạng thái. t203 gọi seam chon/nen/so qua nhiều lượt, gồm lượt fixture ném
lỗi và lượt nền khác nền thật. Trạng thái phải nguyên sau mỗi lượt: CA, SO_BO_QUA, os.name, sys.argv,
environ, cwd, sys.path và globals đều phải nguyên.
Merge master sau khi #677 land là union, không mất khúc nào. Các ca t195–t202 của #677 giống từng byte với
master. _chay_buoc_dang và t51–t68 giống từng byte với 89fc4fa. Mutant L của #677 vẫn chết ở
t195/t196/t197.
Bằng chứng máy tôi đối chiếu, không tự chạy lại:
CI: gate (ubuntu-latest) và gate-ops (ubuntu-latest) success trên đúng head này. Run 36816901782,
04:49:22Z → 05:07:53Z, 15 check success và 1 skipped theo thiết kế; thu-hoi success; mergeable_state: clean.
Tại chỗ, hai vế cùng lệnh: nền 20ec8d5 ra 195/195; nhánh ra 198/198, bỏ qua=0, kể cả [A]/[B] của
t125.
S5″ (spec r3 §2, so merge-base 20ec8d5): 482 63 ≤ 600. ruff F delta 0; diff --check rc 0; doctrine-scan
sạch.
Review Sonnet r3 lượt 2 trên 9d7a523: VERDICT: PASS, 0 P1/P2/P3
(issues/687#issuecomment-5924953529, VERDICT sha256 dcccc301…ad32). Trước đó lượt r3 trên f721fb4 có 3 P3
(issues/687#issuecomment-5924715929); cả ba đã đóng bằng HINT áp nguyên văn và được đo bằng đột biến.
Những điều tôi chấp nhận TƯỜNG MINH khi ký
Head cuối chưa qua nhà cung cấp thứ hai. Review là Sonnet 5.5, cùng họ Claude với executor Opus 5.5, tức
advisory_review. Spec r3 §4 thay codex vì codex hết quota tới 03-10. Chữ ký của tôi THAY cho lượt cross-review ấy.
Windows KHÔNG ĐO ĐƯỢC. Spec r3 §5.5 không cho chạy CI Windows. Kỳ vọng trên Windows là 186/186, bỏ qua=12
nhưng chưa đo; mọi nt trong bằng chứng đều là MÔ PHỎNG. Nhánh nt thật của sổ và của t203 chưa từng chạy.
Hai P4 để lại làm hồ sơ, không vá:
_ca_ung_vien_gian_tiep không nhìn mã lồng (def/lambda/class cục bộ). Hiện không ca nào thuộc dạng này;
nếu có thì Windows báo ĐỎ, không xanh giả.
anh() chụp globals bằng id(), nên không thấy sửa tại chỗ (vd ENV_GITHUB). sys.modules/umask không được
chụp; cả hai nằm ngoài phạm vi spec.
Chốt sổ trong suite là bộ lọc ứng viên tĩnh rồi mới chạy thật. Phép quét đủ mọi ca để ra tập 12 ca nằm ngoài
cổng. Ca tương lai thêm vào phải được đăng ký thủ công.
Spec r3 đổi cách đo trần, từ so baseline 89fc4fa sang so merge-base với master, vì #677 đã land +600 dòng trên
cùng tệp. Đo so 89fc4fa thì tổng là 1048 78.
Ghi để không ai đọc nhầm: đây KHÔNG phải một lần hạ ngưỡng. human_audited là mức hợp lệ sẵn của §8 cho class
sensitive.
VERDICT: approve
Reviewed commit: 9d7a523e80e91ef6aca2c7935f3ee1813fc369f9
```
