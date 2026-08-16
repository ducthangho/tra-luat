# Verdict cross-review — mục lục

**Đọc trang này TRƯỚC khi chạy lại bất kỳ lệnh nào chép từ một tệp verdict.**

Mỗi `*-verdict.md` trong thư mục này là **nguyên văn của phiên reviewer**, neo `sha256`,
và `t26` trong `ops/lease_publish_test.py` băm lại nó mỗi lượt chạy. **Không sửa** — kể cả
để chữa một chỗ sai đã biết. Một bản ghi sửa được thì không còn là bản ghi.

Hệ quả: chỗ sai vẫn nằm nguyên trong tệp gốc. Đính chính sống ở `*.receipt.yaml` bên cạnh,
dưới khoá `verdict_usage_caveats`. Mà một cảnh báo nằm trong tệp không ai mở thì bằng
không — nên nó được nâng lên đây, và `t27` ĐỎ nếu bảng dưới thiếu bất kỳ mục nào.

## ⚠ Cảnh báo đang có hiệu lực

| tệp verdict | id | phải làm gì khi chạy lại |
|---|---|---|
| `wp55-r2-review-5-codex-verdict.md` | `mutable-master-ref-in-repro-command` | Khối bash tái hiện `merged-tree-doctrine-false-positive` dùng `origin/master`, một ref **DI ĐỘNG**. Master lúc đo là `3d2c52d62696b0c7c190fd891115f543b0f9cb55`. **Thay cả hai chỗ `origin/master` bằng SHA đó**, nếu không bạn đang đo một cây khác. |

## Mục lục

| tệp verdict | biên nhận | lease | kết luận | head đã review | byte |
|---|---|---|---|---|---|
| [`wp55-r2-review-4-codex-verdict.md`](wp55-r2-review-4-codex-verdict.md) | [`.receipt.yaml`](wp55-r2-review-4-codex-verdict.receipt.yaml) | `wp55-r2-review-4-codex-20260814` | `changes_requested` | `cf39109c` | 6294 |
| [`wp55-r2-review-5-codex-verdict.md`](wp55-r2-review-5-codex-verdict.md) | [`.receipt.yaml`](wp55-r2-review-5-codex-verdict.receipt.yaml) | `wp55-r2-review-5-codex-20260814` | `changes_requested` | `546ecf9f` | 4392 |

## Vì sao trang này tồn tại — một finding, không phải ý tưởng hay

Codex nêu trên PR #114: cảnh báo ghi vào biên nhận **không tới được người đọc**, vì người
mở thẳng `verdict_path` để chạy lại lệnh chẳng có gì trỏ họ sang tệp sidecar, và quét cả
kho thì **không có bộ đọc hay mục lục nào** đưa `verdict_usage_caveats` ra. `t26` chỉ kiểm
băm và `evidence_url`. Nói cách khác: bản vá đầu tiên chỉ **dời** vấn đề sang một tệp ít
người mở hơn.

Đúng. Nên chốt nằm ở `t27`, không nằm ở thiện chí: thêm một caveat vào biên nhận mà quên
nâng lên bảng trên thì bộ test ĐỎ.

Giới hạn phải nói thẳng, vì trang này **không** chữa hết: người đọc mở thẳng tệp verdict
bằng đường dẫn tuyệt đối vẫn không đi ngang qua đây. Rào duy nhất còn lại cho họ là dòng
mở đầu của chính mục lục này và thói quen đọc thư mục trước khi đọc tệp. Muốn chặt hơn
thì phải có bộ đọc cưỡng chế — chưa làm, và đừng khai là đã làm.
