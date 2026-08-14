# wp55 r3g4 · PHỤ LỤC 2 — master đã dịch, AC 20 ĐO LẠI; va chạm hai phiên đã tự giải

Ghi bởi phiên executor `wp55-r3-exec-4-claude-20260814`, 2026-08-15 ~03:0x giờ VN.
Head bản vá **KHÔNG đổi**: `e6e4b73dc940fcd04e9030e353e0e5fe7f3f0af8`.

## 1 · AC 20 đo lại — master đã dịch sau lần đo đầu

`origin/master` đi từ `3d2c52d62696b0c7c190fd891115f543b0f9cb55` →
`2531366e1abc6cbca0a6c2765e40e54be38d1fb7` (merge PR #114: đưa verdict lượt 5 vào kho).

AC 20 đòi đo trên cây ĐÃ MERGE với master **lúc đo**, nên phép đo cũ hết hiệu lực và đã
được chạy lại nguyên văn:

```bash
m=$(mktemp -d)
git archive origin/master | tar -x -C "$m"          # master = 2531366
git diff --binary fbe5ab9e..e6e4b73 | git -C "$m" apply
python3 "$m/.claude/dev/packet_loop.py" doctrine-scan --root "$m"
GIT_DIR="$PWD/.git" python3 "$m/.claude/dev/packet_loop_test.py"
```

| phép đo | master `3d2c52d` (lần đầu) | master `2531366` (đo lại) |
|---|---|---|
| `doctrine-scan` cây đã merge | rc=0, sạch, 4 tệp | **rc=0, sạch, 4 tệp** |
| suite trên cây đã merge | 109/109, TỔNG ĐẠT | **109/109, TỔNG ĐẠT** |

Master không đụng `CLAUDE.md` hay `.claude/**` trong khoảng này (`git diff --name-only
3d2c52d 2531366` không có đường dẫn nào thuộc hai nhóm đó), nên kết quả không đổi là điều
CHỜ ĐỢI — nhưng vẫn phải đo, vì "không đụng" là suy luận còn "rc=0" là bằng chứng.

## 2 · Va chạm hai phiên: đã tự giải, phần của tôi bị bỏ

Phiên `session_019Dbx4q` ("bàn giao: mở PR + đăng verdict") đã hoàn tất cả ba việc trong
lúc phiên này còn đang soạn:

| việc | kết quả | bằng chứng |
|---|---|---|
| mở PR | **PR #115**, head `e6e4b73` | `git ls-remote origin 'refs/pull/*/head'` → `refs/pull/115/head` = `e6e4b73…` |
| cấp lease review | `wp55-r3-review-6-codex-20260814` | neo `reviewed_sha_required: e6e4b73…`, `target_pull_request: 115` |
| đăng lease lên #55 | **đã đăng** | `posted_comment_id: 5297322412` (workflow ghi ngược) |

Lease lượt 6 dùng cách đánh số TIẾP TỤC (lượt 3→4→5→6), khác cách phiên này định dùng
(đếm lại từ 1 cho revision 3). **Cách của phiên kia đang sống, cách của phiên này bị bỏ.**

Bản nháp của phiên này — `ops/leases/wp55-r3-review-1-codex-20260815.yaml` và
`ops/prompts/wp55-r3-review-1-codex-20260815.md` trên nhánh
`claude/wp55-r3-review-1-lease-draft` — **CHƯA từng được đẩy lên `ops/**`, chưa từng kích
hoạt workflow, chưa từng được đăng**. Nó là lease TRÙNG và phải bị bỏ, không phải bị dùng.

Đây đúng là hậu quả mà `wp55-VA-CHAM-hai-phien.md` dự báo: *"chốt idempotent chỉ chặn đăng
lại CÙNG MỘT TỆP, nó không chặn HAI TỆP KHÁC NHAU cho cùng một lượt"*. Nếu phiên này đã
push bản nháp lên `ops/**` thì lúc này wp55 có HAI lease reviewer cùng hiệu lực cho cùng
một lượt, neo cùng một head, với hai `lease_id` khác nhau. Thứ ngăn được điều đó không phải
cơ chế — mà là phiên này tự dừng ở ranh giới "soạn xong, không đăng". **Cơ chế vẫn thủng
y nguyên**; successor `packet-session-mutex` vẫn cần.

## 3 · Đã kiểm hộ lease lượt 6 — mỏ neo prompt LÀNH

Kho từng mất hai ngày vì lease #3 khai `prompt_sha256_required` mà không có tệp ứng với
con băm. Đã kiểm lease lượt 6 để không lặp lại:

```text
prompt_path            ops/prompts/wp55-r3-review-6-codex-20260814.md   → tồn tại (rc=0)
sha256 tệp thật        e5719fc6e942ec3da9cf7dac66a35c05c3ae2ad86ffca17cb53b6d351e37050c
lease khai             e5719fc6e942ec3da9cf7dac66a35c05c3ae2ad86ffca17cb53b6d351e37050c   ✓ KHỚP
```

Reviewer lượt 6 qua được cổng `--expected-prompt-sha256`. Không có gì chặn.

## 4 · Rác cần dọn (executor KHÔNG xoá nhánh — việc của chủ kho)

| nhánh | vì sao là rác | trỏ vào |
|---|---|---|
| `ops/wp55-r3-review-1` | tạo do một lệnh push nhầm: `git push origin HEAD:refs/heads/ops/…` chạy khi `git checkout` phía trước đã THẤT BẠI, nên nó đẩy HEAD cục bộ chứ không phải nhánh nháp | `fd5d7c7 "thu chot ruleset"` |
| `claude/wp55-r3-review-1-lease-draft` | lease nháp nay đã thừa vì lượt 6 đang sống | `a039b1b` |

**Đã kiểm: lần push nhầm KHÔNG đăng gì.** Nhánh `ops/wp55-r3-review-1` không chứa tệp
lease r3 nào (`ops/leases/` trên đó chỉ có `wp55-r2-review-3` và `wp55-r2-review-4`), và cả
hai tệp cũ ấy đều đã mang `posted_comment_id` (`5290319622`, `5290987281`) nên chốt
idempotent của `lease_publish.py` (`RC_DA_DANG`) bỏ qua chúng. Không có comment thừa nào
lên #55 từ lần push đó.
