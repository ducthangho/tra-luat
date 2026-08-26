# Cross-review vòng 6 — packet #318 `DOCTRINE-RANH-GIOI-REVIEWER`

verdict: changes_requested
reviewed_sha: 70311ee3f073d3a905ba59d0851dd2ce9355cd8e
reviewed_tree: 2cef49f4f5d676c5c19ef027e9cdd0a8ec890a80
base_sha: c35ae1c0a1104dbd6e65a321cda3b9f9441a408b
provider: openai_codex
execution_surface: codex_service
transport: machine
executor: claude
independent_from_executor_session: true
review_axes: [spec, standards_security]

## Kết luận

Yêu cầu thay đổi. N1 và N3–N7b đạt; N2 chưa đạt. Phép đo phía phủ định của
Executor là một cải thiện thật: 10/10 hàng dữ liệu trong vùng taxonomy có nhãn,
và 5/5 hàng quan sát có đúng một nhãn. Nhưng phép ấy chỉ đo **nhãn có mặt**, không
đo **nhãn có đúng nghĩa**.

Hai hàng credential nay được gắn nhãn đúng: chính đoạn ngay sau bảng nói rõ
**hai dòng cuối** cùng đo cơ chế proxy bỏ qua credential client và tự chèn
credential ambient. Hàng `codex -s workspace-write` thì khác: hàng chỉ giữ
`rc=0` và hiệu ứng ghi đè; đoạn từng giải thích/xếp hạng hệ tệp đã bị lát cắt
chuyển sang packet #334. Trong reviewed tree không còn mệnh đề nào nói **vì sao**
phép ghi ngoài cây ấy lọt dưới đúng cấu hình đã đo. Vì vậy hàng này chưa đủ điều
kiện của `cơ chế đã xác minh — chiều MỞ`; với evidence còn lại, nó phải là
`chưa xếp được` (hoặc phải được bổ sung điều kiện và cơ chế ngay cạnh quan sát).
Artefact cũng không ghi phiên bản Codex hay số lần lặp của đúng phép đo ấy, nên
chưa đủ để hạ sang `quan sát chưa rõ cơ chế`, hạng vốn đòi tính lặp lại được.

Hệ quả: con số `chiều MỞ ×5` đúng theo phép đếm literal nhưng sai theo taxonomy.
Nếu chỉ phân loại lại trên evidence hiện có, số đúng là `chiều MỞ ×4` và
`chưa xếp được ×2`. Đây là cùng stable finding P1 của vòng trước, không phải một
finding mới cần đổi slug.

## ĐỐI CHIẾU HAI FINDING VÒNG 5

### `nam-hang-khong-tao-phan-hoach` [P1] — **VÁ SINH LỖI MỚI**

Phần thiếu nhãn đã được vá về mặt cú pháp, kể cả hai hàng credential mà vòng 5
chưa nêu. Tuy nhiên bản vá dán cùng nhãn `cơ chế đã xác minh — chiều MỞ` lên cả
ba hàng. Điều này tạo một lỗi phân hạng mới tại
`docs/GOI_AGENT_DA_NEN.md:655`:

> `codex -s workspace-write` ... `rc=0` ... ⇒ `cơ chế đã xác minh — chiều MỞ`

Định nghĩa tại dòng 611 đòi đồng thời “biết **vì sao** nó không chặn” và “đã
đo”. Hàng 655 chỉ cho vế thứ hai. Dòng 659–662 cố ý giới hạn lời giải thích proxy
cho **hai dòng cuối**, nên không thể dùng lời giải thích ấy cho hàng Codex.
Đối chiếu lịch sử cũng cho thấy câu từng gắn cơ chế hệ tệp với `workspace-write`
ở `6d0a183:686–688` đã bị xóa trong lát cắt `6d0a183..770b3af`.

Phép đo tái lập được:

```text
$ nl -ba docs/GOI_AGENT_DA_NEN.md | sed -n '610,622p;651,662p'
611: định nghĩa chiều MỞ đòi biết vì sao + đã đo
655: chỉ có mode, hiệu ứng và rc=0
659–662: cơ chế proxy chỉ thuộc HAI dòng cuối

$ git diff --unified=1 6d0a183e4af6422d85af1d6d3373fcbab2c7e83e..770b3af3399b6794874008dd907f1dfaad6c5dba \
    -- docs/GOI_AGENT_DA_NEN.md | rg -n -C3 -F 'Hệ tệp: chỉ `read-only` bó'
rc=0; đoạn giải thích `workspace-write` mang hạng chiều MỞ xuất hiện ở phía bị xóa
```

Phép tìm hiện vật cho claim chính xác này:

```text
$ git grep -n -E 'ghi tệp \*\*ngoài\*\* cây|workspace-write.*ngoài|ngoài cây bị ghi' \
    70311ee3f073d3a905ba59d0851dd2ce9355cd8e -- docs .claude scripts ops
70311ee3...:docs/GOI_AGENT_DA_NEN.md:655: ...
```

Không có probe/raw evidence tracked thứ hai để tái lập cơ chế hệ tệp; theo chỉ
thị review, tôi không tự soạn payload đường dẫn thay thế.

### `hai-hang-codex-chi-con-mot` [P2] — **ĐÃ VÁ THẬT**

Dòng 638–639 nay dùng số ít, và nói rõ hàng đối chứng thứ hai đã đi cùng phần
mạng sang packet kế nhiệm. Bảng hiện hành có đúng một data-row bắt đầu bằng
`codex`:

```text
$ sed -n '651,657p' docs/GOI_AGENT_DA_NEN.md | rg -c '^\| `codex'
1
$ sed -n '638,639p' docs/GOI_AGENT_DA_NEN.md
Hàng `codex` ... chỉ còn MỘT, vì hàng đối chứng thứ hai đã theo mục mạng ...
```

Không còn lỗi vị trí/số lượng độc lập nào từ hai lượt sửa gần đây. “Bốn tầng”
vẫn là bốn control; bảng có năm hàng quan sát vì `--allowedTools` được tách thành
hai điều kiện đo. “HAI dòng cuối” trỏ đúng hai hàng credential. Sai số `×5` nêu
trên là hệ quả của chính P1 phân hạng, không phải một finding số đếm riêng.

## PHÉP ĐO PHÍA PHỦ ĐỊNH VÀ ĐỘT BIẾN

Phép quét dưới đây duyệt mọi data-row từ taxonomy đến trước mục “Bản in cuối”,
loại hai header/separator, rồi tìm hàng không mang một trong năm nhãn. Baseline:

```python
from pathlib import Path
import re

lines = Path("docs/GOI_AGENT_DA_NEN.md").read_text(encoding="utf-8").splitlines()
labels = re.compile(
    r"cơ chế đã xác minh — chiều (?:ĐÓNG|MỞ)|quan sát chưa rõ cơ chế|"
    r"máy phát hiện|chưa xếp được", re.I)
inside = False
rows = []
for lineno, line in enumerate(lines, 1):
    if line.startswith("#### NĂM HẠNG"):
        inside = True
    if line.startswith("#### Bản in cuối"):
        inside = False
    if inside and line.startswith("|") and not line.startswith(
        ("|---", "| hạng |", "| tầng |")):
        rows.append((lineno, len(labels.findall(line)), line))
missing = [row for row in rows if row[1] == 0]
print(len(rows), len(missing))
raise SystemExit(1 if missing else 0)
```

Kết quả baseline: `10 0`, `rc=0`; riêng vùng quan sát dòng 653–657 là `5/5`
hàng có đúng một nhãn. Đếm label trong vùng vận hành in
`MỞ=5 / chưa xếp=1 / máy phát hiện=1`, khớp phép đếm literal của Executor.

Tôi dựng clone rời tại `/tmp/tra-luat-review6-codex.5NwlZk/cay`, detached đúng
reviewed SHA/tree và ghim `core.abbrev=7`, rồi chạy hai mutant trên bản sao:

| mutant | doctrine-scan | quét phủ định | doc-claims |
|---|---|---|---|
| bỏ nhãn mới khỏi riêng hàng Codex | `rc=0`, vẫn 8 tệp | **`rc=1`, bắt đúng dòng 655, missing=1** | không cần chạy |
| đổi hàng Codex thành `chưa xếp được`, đồng bộ `MỞ ×4 / chưa xếp ×2` | `rc=0`, 8 tệp | `rc=0`, missing=0 | `rc=0`, `ok=True`, 105 tệp, 0 flags, 359 advisories |

Mutant thứ nhất chứng minh phép quét phủ định có răng cho lớp **thiếu nhãn**.
Mutant thứ hai chứng minh cả quét phủ định, doctrine-scan lẫn doc-claims đều
không phân biệt được **nhãn sai nghĩa** với nhãn đúng nghĩa. Sau hai mutant, clone
đã được hoàn nguyên byte-exact: blob working tree và `HEAD:` cùng là
`2545e583b902ef303e044b916859b16d6b71c52d`; `git diff --exit-code` trả `rc=0`.

Phản chứng sẵn có của `packet_loop` cũng đã chạy trên clone:

```text
$ python3 .claude/dev/packet_loop_test.py
rc=0; nền 257/257; 66 đột biến; 78 lớp lách; 35 ca bắt-oan; 0 ngoại lệ AC18; TỔNG: ĐẠT
```

## BẢNG CHẤM N1–N6, N7a, N7b

| tiêu chí | kết quả | lệnh đã chạy, mã thoát và bằng chứng dương |
|---|---|---|
| N1 | **ĐẠT** | `nl -ba docs/GOI_AGENT_DA_NEN.md \| sed -n '592,657p'` (`rc=0`): tiêu đề/câu đầu dòng 633–636 cùng giới hạn **vỏ phiên điều phối** và đối tượng **quyền ghi vào kho**. |
| N2 | **KHÔNG ĐẠT** | Script quét phủ định ở trên cho `10/10` hàng có nhãn, nhưng dòng 655 không cho biết cơ chế/điều kiện đủ để mang nhãn `cơ chế đã xác minh`. Hai mutant ngữ nghĩa đều qua toàn bộ gate hình thức. |
| N3 | **ĐẠT** | `nl -ba ... \| sed -n '564,577p;641,662p'` (`rc=0`): bảng 78/85/45 tự khai không tái lập được; bảng bốn tầng không dùng ba số ấy làm bảo đảm. Hai hàng credential có cơ chế ngay sau bảng. |
| N4 | **ĐẠT** | `nl -ba ... \| sed -n '633,657p'` (`rc=0`): surface, ngày, mode/phép đo và kết quả nằm cạnh từng quan sát. Việc evidence ấy chưa đủ nâng hàng Codex lên hạng “đã xác minh cơ chế” được chấm riêng ở N2, không phải lỗi vị trí. |
| N5 | **ĐẠT** | Sáu `rg -n -F` đều `rc=0`: `bash /tmp/refscan.sh` tại `:553`; giới hạn `stdout.log` tại `:570–572`; `tương quan có neo` tại `:574–577`; ba hàng `78/5/10,8 M`, `85/10/12,8 M`, `45/1/3,7 M` tại `:566–568`. Tập sáu neo ở `770b3af` và `70311ee` có cùng SHA-256 `7d03f9a10456b9702f5e231a610cd2c4afc66970d4e79c3bb6521d5372804f8a`. |
| N6 | **ĐẠT** | `git diff --name-status c35ae1c0a1104dbd6e65a321cda3b9f9441a408b..70311ee3f073d3a905ba59d0851dd2ce9355cd8e` (`rc=0`) in đúng `M docs/GOI_AGENT_DA_NEN.md`; `git diff --check ...` `rc=0`. |
| N7a | **ĐẠT** | `python3 .claude/dev/packet_loop.py doctrine-scan --root . --path docs/GOI_AGENT_DA_NEN.md` → `rc=0`, `đã quét 8 tệp, 0 chỗ chép doctrine`; clone cùng SHA cho kết quả giống hệt. |
| N7b | **ĐẠT** | `git diff --numstat c35ae1c0a1104dbd6e65a321cda3b9f9441a408b -- docs/GOI_AGENT_DA_NEN.md` → `rc=0`, `145  0`; `145 <= 200`, khớp lời khai Executor. |

Đối chiếu cổng nguồn với clone cùng commit: `doc-claims-check --strict` ở cả hai
nơi đều `rc=0`, `ok=True`, `files_scanned=105`, `flags=0`, `advisories=359`,
`layers_skipped=0`. Không có local check nào bị skipped hoặc not-run trong tập
được dùng làm bằng chứng pass ở trên.

## FINDING CÒN MỞ

### `nam-hang-khong-tao-phan-hoach` [P1] — `rc=0` bị nâng thành “đã xác minh cơ chế”

- **Tệp/dòng:** `docs/GOI_AGENT_DA_NEN.md:611`, `:617`, `:620`, `:655`, `:659–662`.
- **Vấn đề:** đơn vị phân loại là claim + điều kiện đo. Hàng Codex chứng minh hiệu ứng mở, nhưng không chứng minh cơ chế; lời giải thích cơ chế sau bảng chỉ phủ hai hàng credential. Gắn nhãn chiều MỞ làm taxonomy tự vi phạm định nghĩa của nó và kéo số `×5` sai theo nghĩa.
- **Phép đo tái lập:** các lệnh `nl/git diff/rg`, script quét phủ định và hai mutant ở trên. Kết quả phân biệt rõ: bỏ nhãn bị bắt, đổi nhãn mà không đổi evidence thì mọi gate vẫn xanh.
- **Gợi ý vá — ở đâu:** sửa cùng lúc hàng 655, số đếm dòng 617 và câu “mọi mệnh đề ... đã truy được cơ chế” dòng 620; đây là ba projection của cùng một phân loại, nên sửa một chỗ sẽ để lại mâu thuẫn.
- **Gợi ý vá — thế nào:** đường rẻ nhất với evidence hiện có là đổi hàng 655 sang đúng một nhãn `chưa xếp được`, đổi số thành `MỞ ×4 / chưa xếp ×2`, và thu câu dòng 620 cho phù hợp. Đường đắt hơn là giữ `chiều MỞ` nhưng phải ghi ngay cạnh hàng target path/workspace root, toàn bộ config writable-roots, Codex version, số lần/A-B và cơ chế giải thích vì sao ghi lọt; không kéo lại mục mạng của #334 chỉ để lấp bằng prose.
- **Ca test khóa:** ngoài quét missing-label hiện có, thêm oracle ngữ nghĩa cho bảng: mutant gắn `cơ chế đã xác minh` vào một hàng chỉ có `rc=0` mà không có cơ chế/điều kiện đầy đủ phải đỏ; mutant phân loại lại phải buộc đồng bộ count và câu tổng kết. Không dùng grep chữ “vì” đơn thuần vì nó có thể xanh giả.
- **Rủi ro bản vá có thể đẻ:** sửa nhãn mà quên count/câu tổng kết sẽ tái tạo đúng lỗi projection của packet; nhét chi tiết sandbox từ #334 trở lại sẽ phá lát cắt; gate máy móc theo từ khóa sẽ nhầm câu lịch sử với claim vận hành.

## CHỖ KHÔNG ĐO ĐƯỢC

1. **GitHub PR head, CI/check remote, Packet projection và trạng thái Issue #334:** `KHÔNG_ĐO_ĐƯỢC` vì mạng sandbox đóng theo chỉ thị và không được `fetch`. Exact local HEAD/tree/base/ancestry đã được đo; trạng thái remote không được suy thành pass.
2. **Ba `stdout.log` nguồn của bảng 78/85/45:** `KHÔNG_ĐO_ĐƯỢC` vì scratchpad không được git theo dõi. Lượt này chỉ chứng minh sáu neo và ba số giữ nguyên byte giữa lát cắt vòng 5 và reviewed head.
3. **Cơ chế thật của phép ghi ngoài cây ở dòng 655:** `KHÔNG_ĐO_ĐƯỢC` từ artefact hiện hành. Kho chỉ giữ câu kết quả, không giữ raw log/probe/config/target path của lượt cũ; chỉ thị cấm tự dựng payload mới. Vì vậy không được đọc `rc=0` thành “đã biết vì sao”.
4. **Nội dung đã được chuyển đầy đủ vào body #334 hay chưa:** `KHÔNG_ĐO_ĐƯỢC` không mạng. Local history chỉ chứng minh đoạn giải thích hệ tệp/mạng bị xóa khỏi #318 tại lát cắt và một phần doctrine còn neo nội-tệp ở dòng 328–345.

## Đếm finding

- P1: **1**
- P2: **0**

Đường dẫn verdict: `ops/reviews/doctrine-ranh-gioi-reviewer-review-6-codex-verdict.md`
