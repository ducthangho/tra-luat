---
name: cross-review
description: Review chéo khác provider một PR packet của protocol đa phiên (tra-luat) — hai trục Spec và Standards/Security, không sửa file, xuất verdict approve/changes_requested/blocked có bằng chứng ĐO ĐƯỢC. Dùng khi packet vào trạng thái reviewing.
argument-hint: "[so-issue-packet] [so-PR]"
---

# Adapter `cross-review` — Claude Code

**Đây là ADAPTER, không phải nguồn quy tắc.** Quy tắc ở `docs/PROTOCOL_DA_PHIEN.md` §8 (review phân
tầng) và §13. Lệch nhau thì protocol đúng.

## Điều kiện tiên quyết — kiểm trước, không giả định

**Reviewer PHẢI khác provider với executor.** executor `claude` ⇒ reviewer `codex`; executor `codex`
⇒ reviewer `claude`. Máy trạng thái chặn vi phạm bằng mã thoát 4, nhưng đừng dựa vào nó để phát hiện
muộn — kiểm nhãn `executor:*` của Issue trước.

**Reviewer KHÔNG sửa branch** (§8). `changes_requested` trả việc về executor. Muốn sửa thì đó là lượt
executor, và nó ăn vào trần.

## Hai trục, và trục nào cũng phải ĐO

**Spec** — đối chiếu từng dòng `acceptance_criteria` của revision hiện hành. Lấy body qua GraphQL và
**tái lập `spec_hash`**; lệch ⇒ spec đã trôi, DỪNG. Kiểm `git diff --numstat base..HEAD` khớp đúng
`write_set`, không thừa không thiếu.

**Standards/Security** — đọc code là **chưa đủ**. Ba phép tối thiểu:

1. **Gate tự chạy lại** trên checkout Temp SẠCH, rc trực tiếp từng tiến trình. Không đọc lại số của
   executor.
2. **Phản chứng hai chiều** dưới đúng điều kiện mà bản vá khai là nó chữa: đỏ trước sửa / xanh sau sửa.
3. **Mutation test** — bơm đột biến vào chính chỗ vừa sửa; test **phải ĐỎ**. Test xanh khi bị đột biến
   là test rỗng, và một suite rỗng thì mọi con số phía trên đều vô nghĩa.

Bằng chứng dương: `N/N` hai số BẰNG NHAU, `"ok": true`. **rc=0 không phải bằng chứng** — nó bị lừa được.

## Verdict

`approve` · `changes_requested` · `blocked`. Mỗi finding phải kèm **bằng chứng chạy được** (lệnh + số),
không phải nhận xét. Ghi verdict vào Issue kèm **provider của lượt này**, rồi:

```bash
python .claude/dev/packet_loop.py record-review --packet <n> --provider <claude|codex> \
    --verdict <approve|changes_requested|blocked> [--finding "<mô tả>" ...]
python .claude/dev/packet_loop.py next-comment  --packet <n>     # lấy văn bản, ĐĂNG lên Issue
python .claude/dev/packet_loop.py mark-posted   --packet <n> --url <url>
```

Cùng một finding lặp lần thứ 2 ⇒ máy trạng thái trả mã 3 và chuyển `blocked`. Đó là **cố ý**: cùng một
lỗi lặp lại nghĩa là vòng lặp không sửa nổi nó, đốt thêm lượt chỉ là đốt ngân sách. Báo người.

## `approve` KHÔNG phải merge

`approve` chuyển packet sang `awaiting_merge` và **vòng lặp hết quyền ở đó**. Merge do người làm sau
khi duyệt, bằng **merge commit**, không squash khi packet nhiều commit.
