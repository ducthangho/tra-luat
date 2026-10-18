# AUDIT CỦA NGƯỜI — `CI-DUONG-NHANH-HO-SO` (#674 / PR #703), neo `46bc11de`

**BẢN CHIẾU, không phải nguồn có thẩm quyền.** Với verdict của một MÔ HÌNH, kho quy ước tệp có băm là nguồn
và comment là bản chiếu. Lượt `human_audited` thì NGƯỢC lại: §8 neo nó vào danh tính bền trên GitHub, mà một
tệp trong kho không mang được danh tính ấy. **Nguồn là comment `5927873457`**; tệp này để tra ngoại tuyến.

| | |
|---|---|
| nguồn có thẩm quyền | https://github.com/ducthangho/tra-luat/issues/674#issuecomment-5927873457 |
| tác giả | `ducthangho` · `author_association: OWNER` (KHÔNG phân biệt được người với phiên agent dùng token chủ kho, xem #566) |
| `performed_via_github_app` | `null` (các comment review lượt 15–18 và lệnh land trên #674 do phiên agent đăng mang `claude`) |
| thời điểm | `2026-10-01T08:41:09Z` (`updated_at` = `2026-10-01T08:41:09Z`, tức comment chưa bị sửa lúc đọc) |

## Phép đo bản ĐÃ ĐẾN

Đọc ngược qua REST `GET /repos/ducthangho/tra-luat/issues/comments/5927873457` (2026-10-01 ~09:58Z), đo trên
BYTE THÔ của trường `body`:

| | giá trị |
|---|---|
| byte | **3554** |
| sha256 | `24a1b8320ad7bbe3c05d991166a5b19b6a707ac2adf02056760b472634704c6d` |
| xuống dòng | LF × 32, CR × 0; không có LF cuối; NFC |
| dòng đầu | `VERDICT — human_audited · approve` (36 byte) — **KHÔNG có dòng `VERDICT:` nào** (chuỗi `VERDICT:` 0 lần; chữ `VERDICT` 2 lần: dòng đầu và một lần trích băm verdict lượt 18 giữa dòng) |
| `Reviewed commit:` | đúng **1** lần (dòng 2) |
| SHA đầy đủ `46bc11de…3895e5fe1` | đúng **1** lần |
| `dang_boi: chu_kho_tu_dang` | đúng **1** lần (dòng 3) — LỜI KHAI trong thân, không phải dữ liệu GitHub |
| chuỗi `&#` · dấu backtick | 0 · 0 |

**Mất định dạng Markdown khi dán** (giống tiền lệ #681/#701). Thân ĐÃ ĐẾN không còn backtick, `**`, tiền tố
danh sách hay dòng trống: chủ kho dán văn bản ĐÃ RENDER của bản nháp. Nội dung chữ giữ nguyên — đo: bỏ backtick,
`**`, tiền tố `#`/`1. `/`- ` và gộp khoảng trắng ở cả hai bên thì thân ĐÃ ĐẾN và bản nháp của phiên điều phối
(`human-audit-674-46bc11d.md` trong scratchpad, 3604 byte, mtime 2026-10-01T08:38:27Z) khớp (3100 = 3100 ký tự,
so bằng `==`). Bản nháp KHÔNG đưa vào kho; ai làm lớp bỏ định dạng: KHÔNG ĐO ĐƯỢC. Không sửa bản chiếu cho "đẹp".

---

## Nguyên văn (thân `body` chép từ readback, không sửa một byte)

```text
VERDICT — human_audited · approve
Reviewed commit: 46bc11de82fab227e29e1bc0e057fcf3895e5fe1
dang_boi: chu_kho_tu_dang
assurance_target: human_audited
review_class: sensitive
packet: #674 CI-DUONG-NHANH-HO-SO revision 2 / generation 4
lease: ci-duong-nhanh-ho-so-r2-g4-claude (nhánh ops/cap-lease-ci-duong-nhanh-ho-so)
spec: ops/specs/CI-DUONG-NHANH-HO-SO-r2.md @ 4105292 · sha256 b6e719c999d5990f987628963c248b1ac53d377dfa5b668ac06adce76981da57
immutable_acceptance_baseline: 1741e0a1ab7ebce4b26912aefadca56ddfcdc691
nhánh: claude/ci-duong-nhanh-ho-so @ 46bc11d (đã đẩy, chưa có PR)
Tôi đã tự đọc spec r2 và toàn bộ diff trên đúng head này. Diff tính từ master 20ec8d5 (đã merge vào nhánh ở 6803012) chạm đúng bốn tệp, +4317/−4:
.github/workflows/ci.yml
ops/ci_duong_nhanh.py
ops/ci_duong_nhanh_test.py
.claude/dev/ci_dang_ky_test.py (một dòng thêm vào DA_NOI)
Tôi không dựa vào bản tóm tắt của executor.
Chấp nhận:
PR chỉ đổi hồ sơ (ops/land, ops/leases, ops/reviews, ops/specs) được xếp duong_nhanh. Ba job bắt buộc vẫn khởi động và báo kết quả, chỉ các bước nặng bị if: cấp bước bỏ qua. Không dùng paths:. Phân loại thất bại thì rơi về day_du (fail-close).
Bước kiem-re thay cho các bước bị bỏ: YAML, git diff --check, lease qua lease_publish, ba ca dữ liệu, mode git (chỉ 100644/100755 hoặc xoá), symlink treo trên toàn cây theo đúng cách t82 chép.
Hai job của #668 (gate-cong-cu, gate-cong-cu-gop) KHÔNG nhận đường nhanh, luôn chạy đủ. Lý do: thêm if: vào bước G5 làm ci_dang_ky_test đỏ (chốt M6), mà sửa registry thì Q4 cấm.
D1/D2 là erratum đã duyệt (issuecomment-5887720007).
Bằng chứng tôi chấp nhận:
Review Opus lượt 18 (advisory_review, cùng họ executor, KHÔNG phải cross_approved): approve, 0 P1 / 0 P2 / 0 P3, trên đúng SHA này. VERDICT sha256 a49c2d9092ccba5676e8953f8853470babbad570e7a1e4785700e7072b3e3fb1 (issuecomment-5927757295).
Các lượt 15–17 ở issuecomment-5924734096, -5925474994, -5926431934. Mọi finding đã đóng; lớp kiem-mode-git-chot-khong-rang đóng theo quyết định S3 của tôi.
Đo tại chỗ trên 46bc11d: ci_duong_nhanh_test CA 104/104, DOT BIEN 383/383; ci_dang_ky_test 23/23 + 1025/1025; tl selftest 1715/1715; ruff F delta 0 (tl.py 12 = nền); doctrine-scan rc=0; adr-song rc=0.
actionlint: một finding SC1003:info ở ops-don-ref.yml:117, có y hệt trên master 20ec8d5 ⇒ delta 0.
Giới hạn tôi chấp nhận:
Nghiệm thu 11 (PR hồ sơ thật trên Actions: tên context khi skipped, thời gian gate rút gọn) CHƯA ĐO ĐƯỢC. Phải đo ở PR land đầu tiên.
Không chạy Windows CI (quyết định của tôi). Junction/core.symlinks=false trên Windows chưa đo.
Symlink treo chỉ với tới được qua bí danh thư mục trỏ RA NGOÀI cây: chưa có ca (H11b sống). PR hồ sơ không tạo được tình huống này.
Symlink lưu trong git trỏ tới thiết bị làm chốt đỏ trong khi copytree chép được: đỏ fail-close, chấp nhận.
Sau land: thêm context gate-cong-cu-gop (ubuntu-latest) vào ruleset (spec #668 §7) nếu chưa thêm.
Phạm vi chữ ký: nó xác nhận "tôi đã đọc và chấp nhận". Nó KHÔNG phải một lượt dò tìm độc lập. Các phép đo là của review Opus lượt 8–18 và phiên điều phối. Đừng đọc chữ ký này thành "đã soi ở mức reviewer".
```
