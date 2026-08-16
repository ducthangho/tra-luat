# Viết lại cụm trong `CLAUDE.md` — thay cho bản di trú bị bác · REVIEWER `codex`

Bạn là **reviewer** cross-provider. Tác giả commit là `claude` (§8 đòi khác nền). Vai này
**read-only**: KHÔNG sửa tệp, KHÔNG commit, KHÔNG push, KHÔNG merge/land.
Bạn được phép ghi tệp tạm và ghi ĐÚNG MỘT tệp verdict nêu ở cuối.

## BƯỚC 0 — xác minh. Lệch bất kỳ mục nào ⇒ DỪNG, báo lại, không review.

```bash
git rev-parse HEAD                                                   # ĐÒI c47a439997e0191427d775636ebadbf3be7e1481
git rev-parse HEAD^                                                  # ĐÒI 2531366e1abc6cbca0a6c2765e40e54be38d1fb7
git rev-parse --is-shallow-repository                                # ĐÒI false
git diff --name-only 2531366e1abc6cbca0a6c2765e40e54be38d1fb7 HEAD   # ĐÒI đúng: CLAUDE.md
git diff --shortstat 2531366e1abc6cbca0a6c2765e40e54be38d1fb7 HEAD   # ĐÒI 2 insertions, 2 deletions
```

| | |
|---|---|
| head đang review | `c47a439997e0191427d775636ebadbf3be7e1481` |
| dựng trên master | `2531366e1abc6cbca0a6c2765e40e54be38d1fb7` |
| phạm vi | **một tệp, hai dòng** — `CLAUDE.md` |
| bản bị THAY | `9a5b05cfd8804455dd785b8fe710736773dc78cf` — verdict `do_not_land` |
| verdict bác bản trước | `ops/reviews/wp55-r4-review-di-tru-codex-verdict.md` trên `ops/wp55-r4-verdict-di-tru` |

Diff nhỏ, nhưng đây là commit nhắm thẳng vào **nhánh MẶC ĐỊNH** và là điều kiện tiên quyết
để revision 4 chốt `base_sha`. Tác giả là `claude`; nếu `claude` tự duyệt commit của chính
mình lên master thì đó đúng là thứ protocol sinh ra để chặn. **Bạn là chốt duy nhất.**

## Việc commit này làm

Lượt trước bọc chỗ cần miễn trừ bằng một khối chứng cứ AC 19, và bị bác — finding
`ac19-exemption-wider-than-necessary`: khối miễn 10 dòng để cứu 2 dòng.

Bản này đi **đường bạn đề xuất**: đổi cách gọi trong câu đo thay vì bọc miễn trừ quanh nó.

```
người có / thẩm quyền   →   tên thuộc / danh sách cho phép
```

## Nơi đáng dồn sức

**A. BẢN GHI PHÉP ĐO CÓ CÒN ĐÚNG KHÔNG — câu hỏi quan trọng nhất của lượt này.**

Đây là một dòng trong `CLAUDE.md` **kể lại một phép đo có thật** (`v1.36.68`, PR #104).
Viết lại nó là viết lại một BẢN GHI LỊCH SỬ. Hai cách gọi không đồng nghĩa hoàn toàn:

- `người có thẩm quyền` — một **vai trò**;
- `tên thuộc danh sách cho phép` — một **cơ chế**.

Trong ngữ cảnh đo cổng allowlist, chúng trỏ cùng một thứ được đo. **Phán định: bản ghi sau
khi sửa còn thuật đúng thứ đã đo không, hay đã trượt nghĩa?** Đối chiếu với PR #104 và với
mô tả cổng trong `packet_loop.py` nếu cần. Nếu trượt nghĩa thì đây là finding nặng — sửa
tài liệu cho qua cổng mà làm sai bản ghi là cái giá không được trả.

**B. Cụm thay thế có tự trở thành cụm cấm không?**

`danh sách cho phép` là một khái niệm doctrine của chính kho này. Kiểm xem nó có nằm trong
danh sách cấm hiện hành hoặc có nguy cơ được thêm vào không — nếu có, ta chỉ dời vấn đề.

**C. Có chỗ nào khác cần cùng cách xử lý mà commit bỏ sót không?**

Executor khai đây là chỗ **duy nhất** trên toàn cây đã merge. Kiểm lại con số ấy, ở **cả
hai** hình dạng (ngắt dòng và một dòng), trên **toàn bộ** tệp bị `doctrine-scan` quét.

**D. Đối chứng của chính bạn ở lượt trước — tái lập lại.**

Bạn khai: nối cụm thành một dòng cho `rc=6`, viết lại cho `rc=0`. Executor tái lập được cả
hai. Chạy lại để chắc, và **đọc `rc` trực tiếp từng tiến trình, không qua pipe** — executor
lần đầu đo sai đúng vì lỗi này.

## Gate

```bash
python3 <(git show 1a4525a20aa360476a6f59cb157c21097919c457:.claude/dev/packet_loop.py) \
  doctrine-scan --root .
python3 .githooks/eol_policy.py --all --json
python3 scripts/tl.py doc-claims-check --strict --json
python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --root . --strict --json
python3 scripts/tl.py golden-test
```

Executor khai tất cả `rc=0`, `release-verify` checked=179 failed=0 extra=0, và `CLAUDE.md`
không thuộc manifest. Cũng khai: **0 dòng được miễn trừ** trong tệp — tức bản này không xài
cơ chế khối chứng cứ nào. Kiểm bằng nguyên mẫu:

```bash
git show origin/ops/wp55-r4-spec-draft:ops/specs/wp55-r4-ac19-nguyen-mau.py > /tmp/proto-c47a439.py
```

## Câu hỏi THIẾT KẾ mà bản vá này làm lộ ra — trả lời nếu bạn có căn cứ

Nếu chỗ này là chỗ duy nhất cần miễn trừ, và nó vừa được xử lý mà **không** dùng miễn trừ,
thì **cơ chế khối chứng cứ của AC 19 mới không còn người dùng nào**. Spec revision 4 đứng
trước hai đường:

1. **giữ AC 19 mới** như hợp đồng dự phòng — đổi lại spec mang một cơ chế chưa từng được
   kiểm bằng một ca thật nào;
2. **đơn giản hoá** thành *"không cụm cấm nào được xuất hiện, kể cả ngắt dòng"*, bỏ hẳn
   miễn trừ — mọi phản ví dụ của bốn lượt review tự động đóng, scanner đơn giản hẳn; đổi
   lại mất cửa thoát nếu sau này thật sự cần kể lại một phép đo chứa cụm cấm.

Executor nghiêng về (2) với lý do "cơ chế không có người dùng là cơ chế chưa ai kiểm".
**Bạn thấy sao?** Đây là ý kiến tham khảo cho chủ kho, KHÔNG phải finding — đừng để nó ảnh
hưởng tới verdict về commit.

## Ba chuyện đã trả giá — đừng mất thời gian lại

1. **Sandbox từ chối `rm -rf`.** Dùng thư mục có hậu tố SHA.
2. **Đừng chạy `pip install`** — một lần cài giữa phiên đã làm hỏng `cryptography`.
3. **`release-verify` trong cây làm việc có thể trả `rc=2`** vì tệp nhiệm vụ này nằm ngoài
   manifest. Không phải finding — đo trên `git archive` của đúng head nếu cần số sạch.

## Giao kết quả

Ghi verdict ra ĐÚNG một tệp: `VERDICT_VIET_LAI.md` ở gốc thư mục làm việc.
KHÔNG commit, KHÔNG push.

Định dạng: `approve` | `changes_requested` | `blocked`, mỗi finding có `finding_id`
(slug kebab-case), `severity`, `disposition`, và **bằng chứng CHẠY ĐƯỢC neo SHA bất biến**.
Kèm khối `Evidence §7` dạng YAML với `reviewed_sha`, `base_sha`, danh sách `tests`,
`findings`, và trường `land_recommendation` (`fast_forward` | `merge_commit` | `do_not_land`).

**Nói thẳng chỗ bạn KHÔNG chạy được.** Ranh giới của bản review quan trọng ngang kết luận.
