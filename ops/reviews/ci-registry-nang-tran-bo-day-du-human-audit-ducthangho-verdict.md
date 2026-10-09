# AUDIT CỦA NGƯỜI — `CI-REGISTRY-NANG-TRAN-BO-DAY-DU` (#705 / PR #707), neo `36190a35`

**BẢN CHIẾU, không phải nguồn có thẩm quyền.** Với verdict của một MÔ HÌNH, kho quy ước tệp có băm là nguồn
và comment là bản chiếu. Lượt `human_audited` thì NGƯỢC lại: §8 neo nó vào danh tính bền trên GitHub, mà một
tệp trong kho không mang được danh tính ấy. **Nguồn là comment `6049196146`**; tệp này để tra ngoại tuyến.

| | |
|---|---|
| nguồn có thẩm quyền | https://github.com/ducthangho/tra-luat/pull/707#issuecomment-6049196146 |
| tác giả | `ducthangho` · `author_association: OWNER` (KHÔNG phân biệt được người với phiên agent dùng token chủ kho, xem #566) |
| `performed_via_github_app` | `null` (các comment phiên agent trên PR #707 — `6048969153`, `6048997602`, `6049769887` — mang `claude`) |
| thời điểm | `2026-10-07T23:52:02Z` (`updated_at` = `2026-10-07T23:52:02Z`, tức comment chưa bị sửa lúc đọc) |

## Phép đo bản ĐÃ ĐẾN

Đọc ngược qua REST `GET /repos/ducthangho/tra-luat/issues/comments/6049196146` (2026-10-08 ~03:32Z, `gh api` —
client GitHub dựng sẵn của Claude Code qua proxy phiên), đo trên BYTE THÔ của trường `body`:

| | giá trị |
|---|---|
| byte | **2497** |
| sha256 | `6753815a6ae2422672afbe1a9eab7a43a136d066f14c9fd27ed167c538943435` |
| xuống dòng | LF × 21, CR × 0; không có LF cuối; NFC |
| dòng đầu | `VERDICT — human_audited · approve` (36 byte) — **KHÔNG có dòng `VERDICT:` nào** (chuỗi `VERDICT:` 0 lần; chữ `VERDICT` 2 lần: dòng đầu và một lần trích băm verdict Codex lượt 2 giữa dòng) |
| `Reviewed commit:` | đúng **1** lần (dòng 2) |
| SHA đầy đủ `36190a35…178dfd82544` | đúng **1** lần |
| `dang_boi: chu_kho_tu_dang` | đúng **1** lần (dòng 3) — LỜI KHAI trong thân, không phải dữ liệu GitHub |
| chuỗi `&#` · dấu backtick | 0 · 0 |

**Mất định dạng Markdown** (giống tiền lệ #681/#701/#703): thân ĐÃ ĐẾN không còn backtick, `**`, tiền tố danh
sách hay dòng trống. Bản nháp của phiên điều phối KHÔNG tìm thấy trong scratchpad lúc ghi sổ, nên phép so nội dung
chữ với bản nháp: KHÔNG ĐO ĐƯỢC. Ai làm lớp bỏ định dạng: KHÔNG ĐO ĐƯỢC. Không sửa bản chiếu cho "đẹp".

**Thứ tự thời gian đáng đọc kèm** (đo từ REST): chữ ký đăng `23:52:02Z`, tức SAU lượt 1 `gate-registry` ĐỎ
(comment `6048969153` lúc `23:32:12Z`) và TRƯỚC khi lượt chạy lại duy nhất xanh (job `113070797698` xong
`00:40:57Z`; comment `6049769887` lúc `00:41:34Z`). Thân chữ ký tự nói "tôi cho chạy lại đúng một lần" — nó ký trên
kết quả A5 của lượt 1 (3612 s), không trên kết quả lượt chạy lại.

---

## Nguyên văn (thân `body` chép từ readback, không sửa một byte)

```text
VERDICT — human_audited · approve
Reviewed commit: 36190a35db647e65d7c6fd4b684d5178dfd82544
dang_boi: chu_kho_tu_dang
assurance_target: human_audited
review_class: sensitive
packet: #705 CI-REGISTRY-NANG-TRAN-BO-DAY-DU revision 3 / generation 3
lease: ci-registry-nang-tran-bo-day-du-r3-g3-claude (cấp quyền #705 comment 6042998795)
spec: ops/specs/CI-REGISTRY-NANG-TRAN-BO-DAY-DU-r3.md @ 36473cd · sha256 ce14c65668f2076795ed20955d263653e927b0aeddea7d5fd6445f41eb563c7d
immutable_acceptance_baseline: 7e5958e440285c8d63d2f710cf97ba20b85f2926
Tôi đã tự đọc spec r3 và toàn bộ diff trên đúng head này. Diff so master chỉ chạm bốn tệp write set, +25/−10:
.claude/dev/ci_dang_ky_test.py
.github/workflows/ci.yml
.github/workflows/ci-dot-bien-du.yml
ops/ci_duong_nhanh_test.py
Tôi không dựa vào bản tóm tắt của executor.
Chấp nhận:
Trần một bộ GIAY_TOI_DA_MOT_BO 4500 → 5400 s; timeout-minutes của gate-registry và dot-bien-du 90 → 105; KHUNG_JOB khớp 105; BAM_GATE_REGISTRY cập nhật; ca p643 nay đo trần thật truyền tới communicate qua _chay_that (M10).
Codex cross-review lượt 2 (gpt-6.1-sol, xhigh) cho approve, 0 P1 / 0 P2 / 0 P3, trên đúng SHA này: #705 comment 6047530796, VERDICT sha256 94a9e9c6f6136a07afe28b40a94348143787296dd885fb7fca367987749d4c52. Hai lớp của lượt 1 (tran-runtime-khong-duoc-ca-kiem-khoa P2, ty-le-cham-khong-khop-so-do P3) đã đóng; P3 đóng bằng erratum trong Spec r3.
A5: ops/nhanh_don_duoc_test.py chế độ đủ chạy 3612 s dưới trần 5400 s (run 37691975887). Lượt đó đỏ vì đột biến tự kiểm r548 bị xếp tín dụng giả do git bảo trì nền đua với bước dọn thư mục tạm của r506, nằm ngoài write set; tôi cho chạy lại đúng một lần.
Giới hạn tôi chấp nhận: 5400 s chưa bảo đảm cho mọi runner (biên ~48% trên 3645 s); giải pháp bền là chia mảnh nhanh_don_duoc_test, để packet kế nhiệm. Phân hạng r548/r506 phụ thuộc thời điểm là nợ có sẵn của ops/nhanh_don_duoc_test.py.
Land: bằng merge commit. Master đã trôi từ 8c98afa tới ab457c6; trôi không chạm bốn tệp write set và git merge-tree sạch (Codex lượt 2 đã đo).
Khai thẳng phạm vi chữ ký này: nó xác nhận "tôi đã đọc và chấp nhận". Nó KHÔNG phải một lượt dò tìm độc lập. Phép đo là của hai lượt Codex và phiên điều phối.
```
