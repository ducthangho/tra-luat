---
name: cross-review
description: Review chéo khác provider một PR packet của protocol đa phiên (tra-luat) trên nền Claude Code — cách đo, cách chạy sandbox, cách ghi verdict. Quy tắc review nằm ở docs/PROTOCOL_DA_PHIEN.md, tệp này chỉ là cú pháp.
argument-hint: "[so-issue-packet] [so-PR]"
---

# Adapter `cross-review` — Claude Code

**ĐỌC `docs/PROTOCOL_DA_PHIEN.md` TRƯỚC.** Mức review, quyền của reviewer, và định nghĩa hoàn tất
nằm ở **§8** và **§13** — kể cả việc verdict phải ghi vào **PR** và reviewer **không sửa branch**.
Tệp này **cố ý KHÔNG chép lại** chúng.

## Cách ĐO — phần thuộc về nền này

Đọc code là **chưa đủ**. Ba phép tối thiểu, và phép thứ ba là phép hay bị bỏ nhất:

1. **Tự chạy lại gate** trên checkout Temp SẠCH, mã thoát trực tiếp từng tiến trình. Không đọc lại
   số của executor.
2. **Phản chứng hai chiều** dưới đúng điều kiện bản vá khai là nó chữa: đỏ trước / xanh sau.
3. **Mutation test.** Bơm đột biến vào chính chỗ vừa sửa; test **phải ĐỎ**. Đột biến nào **sống sót**
   là một lỗ hổng của suite ⇒ đó là finding, kèm số ca đỏ. Test xanh khi bị đột biến là test rỗng,
   và suite rỗng thì mọi con số phía trên đều vô nghĩa.

Bằng chứng dương: `N/N` hai số BẰNG NHAU, `"ok": true`. **`rc=0` không phải bằng chứng.**

## Chạy provider kia — và KHOÁ PHẠM VI

```bash
codex exec -s workspace-write --skip-git-repo-check --cd <sandbox> - < PROMPT.md
```

**Dựng sandbox biệt lập** chứa sẵn `SPEC.md` · `diff.patch` · `numstat.txt` · trích protocol · bản sao
cây sau sửa — rồi cấm reviewer đọc ra ngoài thư mục đó. Đây **không** phải cẩn thận thừa: lượt đầu
chạy với phạm vi mở, agent quét ra ngoài kho, đọc nhầm transcript phiên, 40 phút không ra kết luận.
Sandbox cũng cho reviewer tự do đột biến bản sao mà không chạm kho thật.

## Ghi verdict

Verdict `approve` / `changes_requested` / `blocked` ghi vào **PR** (§13). Mỗi finding kèm **bằng chứng
chạy được** — lệnh + số — không phải nhận xét. Đồng thời ghi transition vào Issue qua máy trạng thái:

```bash
python .claude/dev/packet_loop.py record-review --packet <n> --provider <claude|codex> \
    --verdict <approve|changes_requested|blocked> [--finding "<mô tả>" ...]
python .claude/dev/packet_loop.py next-comment  --packet <n>
python .claude/dev/packet_loop.py mark-posted   --packet <n> --url <url comment THẬT>
```

Vân tay finding bỏ qua hoa/thường, khoảng trắng **và dấu câu** — nên đừng trông chờ diễn đạt lại nhẹ
sẽ thành finding mới. Cùng một lỗi lặp lần thứ 2 ⇒ máy trạng thái dừng và chuyển `blocked`: cùng một
lỗi lặp lại nghĩa là vòng lặp không sửa nổi nó, đốt thêm lượt chỉ là đốt ngân sách.

`approve` chuyển packet sang `awaiting_merge` và **vòng lặp hết quyền ở đó** — merge là việc của người.
