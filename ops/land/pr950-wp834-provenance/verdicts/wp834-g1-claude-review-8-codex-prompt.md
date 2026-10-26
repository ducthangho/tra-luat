# Cross-review Codex — packet #834 (`MAY-ADR-0054-a2`) — lượt 8 (lượt CUỐI, 8/8): xác minh head sau merge sửa drift

Bạn là **reviewer độc lập, offline** cho Packet #834, revision 1, generation 1. Executor là Claude (họ `claude`); bạn là Codex
(họ `openai`) ⇒ `assurance_target: cross_approved`, `review_class: sensitive`. Không kế thừa context executor. Không truy cập
mạng, không GitHub, không push. Bạn KHÔNG sửa mã nguồn; mọi phép thử chạy trên **bản sao riêng** dưới `OUT/`.

## Định danh (tự kiểm, đừng tin bảng này)

- `SRC` = thư mục `src/` cạnh tệp này: clone thường (`.git` là thư mục, không nông), detached tại head ứng viên
  **`294f0eb7eaae7b142bd6a3e89a18f512c4b819d0`**. Thứ định danh tệp là **băm/SHA**, không phải tên nhánh.
- Head này = merge của **`8ac10ce47d2587c91637d74d299e3c781025be1e`** (head bạn đã **approve** ở lượt 7, bản chép
  `tham-chieu/VERDICT-luot7.md` sha256 `37f009b88c8f9aca7ae4a09d431f1046f8b7ca09978d2e75e47ce6e57cd68488` — tự băm lại) với `origin/master` **`9372ecd`** (ref
  `refs/remotes/origin/master` trong clone trỏ `9372ecd`). Base lease `ab344da5f07cce673d97056b70b002911c4d5082`.
- `OUT` = thư mục `out/` cạnh tệp này — nơi DUY NHẤT bạn ghi.
- Đặc tả con `SRC/ops/specs/wp834.md` sha256 `c57ef4d86592218729b811efede7909803d75b6d18ca0d0c3e5059848b44a9d2`; phần chung
  `SRC/ops/specs/may-adr-0054-chung.md` sha256 `4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0`.
- Write set: `.claude/dev/packet_loop.py`, `.claude/dev/packet_loop_test.py`, `docs/PROTOCOL_DA_PHIEN.md` (§4). Diff ≤ 450 dòng thêm.

## Vì sao có lượt này

Lời gọi Codex thứ **8/8** (ADR-0052), lượt cuối. Sau khi executor đẩy `8ac10ce` (PR #950), check `thu-hoi` đỏ vì head drift:
`S 9372ecd không phải tổ tiên của H 8ac10ce` (master tiến thêm qua #949, chỉ `ops/land/**`). **Chủ kho quyết định** (Packet Issue
#834, comment `issuecomment-6409611375`, ghi hộ): ngoại lệ một lần — merge `origin/master`, chứng minh write set giống từng byte,
chạy lại suite, gọi Codex 8/8 xác minh trên exact head mới, rồi đẩy lần hai.

## Việc — phạm vi HẸP

1. Băm lại hai đặc tả và verdict lượt 7. Xác nhận: `8ac10ce` và `9372ecd` đều là tổ tiên của head; `ab344da` là tổ tiên head.
2. **Đo** rằng ba tệp write set tại head giống **từng byte** tại `8ac10ce` (`git diff 8ac10ce 294f0eb -- <3 tệp>` rỗng; so blob
   OID). Đo `git diff --numstat 9372ecd 294f0eb` chỉ gồm đúng ba tệp ấy, tổng dòng thêm ≤ 450.
3. Rà phần master mang vào (`git diff 8ac10ce 294f0eb --stat`, tức `356eb26..9372ecd`): có tệp nào mà **mã hoặc test của write set
   đọc hoặc phụ thuộc** không (ví dụ `ops/lease_publish.py`, `ops/bien_nhan_v2.py`, `.claude/dev/launcher.py`, `AGENTS.md`,
   `docs/adr/`, `docs/PROTOCOL_DA_PHIEN.md` trên master — validator canon mà `packet_loop.py` chép từ `origin/master`)? Nếu có,
   đo lại hành vi liên quan: chạy `python -B tham-chieu/chay_ca_va_dot_bien.py src r834_ r834_` trên head (hoặc ít nhất các ca
   `r834_*` và `r812_*`), báo số.
4. Không review lại toàn bộ thiết kế: verdict lượt 7 đã approve nội dung trên `8ac10ce`. Chỉ nêu finding **mới** nếu merge làm đổi
   hành vi hoặc phá nghiệm thu. Luật phân hạng lượt 7 vẫn áp: đột biến độ phủ MỚI do reviewer tự dựng mà mã từ chối đúng ⇒ P3;
   P2 trở lên chỉ khi có hành vi sai thật.

## Dạng verdict — ghi vào `OUT/VERDICT.md`

Dòng 1 `Verdict: approve` hoặc `Verdict: request_changes`; dòng 2 `Reviewed commit: 294f0eb7eaae7b142bd6a3e89a18f512c4b819d0`;
dòng 3 `Spec sha256: <64 hex>; Chung sha256: <64 hex>`. Sau đó: kết quả từng phép đo ở mục Việc (lệnh, rc, output chính), và bảng
finding nếu có (`slug | hạng | biểu hiện | phép đo | hướng vá`). Ngưỡng approve: không còn P0/P1/P2. Nợ P3 lượt 7 giữ nguyên tên.
Verdict chỉ neo commit trên, không cấp quyền push/merge/land.

## Cách chạy

`export PYTHONDONTWRITEBYTECODE=1`. Nếu git toàn cục có `commit.gpgsign=true`, cô lập bằng `GIT_CONFIG_GLOBAL=/dev/null
GIT_CONFIG_SYSTEM=/dev/null`. Suite đầy đủ tốn ~50 phút — executor đang chạy riêng; bạn không bắt buộc chạy lại.
