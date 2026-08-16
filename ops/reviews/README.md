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
| [`wp55-r4-review-di-tru-codex-verdict.md`](wp55-r4-review-di-tru-codex-verdict.md) | [`.receipt.yaml`](wp55-r4-review-di-tru-codex-verdict.receipt.yaml) | `wp55-r4-review-di-tru-codex-20260815` | `changes_requested` | `9a5b05cf` | 7797 |
| [`wp55-r4-review-viet-lai-codex-verdict.md`](wp55-r4-review-viet-lai-codex-verdict.md) | [`.receipt.yaml`](wp55-r4-review-viet-lai-codex-verdict.receipt.yaml) | `wp55-r4-review-viet-lai-codex-20260815` | `approve` | `c47a4399` | 8303 |
| [`wp55-r4-review-rebase-codex-verdict.md`](wp55-r4-review-rebase-codex-verdict.md) | [`.receipt.yaml`](wp55-r4-review-rebase-codex-verdict.receipt.yaml) | `wp55-r4-review-rebase-codex-20260816` | `approve` | `c44b2d4c` | 5383 |
| [`wp55-r4-review-1-codex-verdict.md`](wp55-r4-review-1-codex-verdict.md) | [`.receipt.yaml`](wp55-r4-review-1-codex-verdict.receipt.yaml) | `wp55-r4-review-1-codex-20260816` | `do_not_land` | `2432e3f6` | 6578 |
| [`wp55-r4-review-2-codex-verdict.md`](wp55-r4-review-2-codex-verdict.md) | [`.receipt.yaml`](wp55-r4-review-2-codex-verdict.receipt.yaml) | `wp55-r4-review-2-codex-20260816` | `approve` | `817598e2` | 4525 |

Ba hàng đầu của revision 4 (`di-tru`, `viet-lai`, `rebase`) là việc **phụ trợ** — mỗi lượt
review đúng một commit trên master, một tệp `CLAUDE.md` — chứ không phải lượt cross-review
của packet. Hai hàng cuối mới là dòng chính: `do_not_land` trên `2432e3f6`, rồi **`approve`**
trên `817598e2`, và `approve` ấy là căn cứ để #130 land.

**Đường giao của revision 4 khác revision 2, đọc kỹ chỗ này.** Verdict r2 đăng thành PR review
trên #92, nên `evidence_url` của chúng trỏ vào GitHub. Nhánh packet của r4 **không có PR** —
lease khai `target_pull_request: null`, "review neo thẳng vào SHA" — nên năm verdict r4 được
giao bằng **tệp trên nhánh**. Trong phạm vi đã quét (90 comment của #55 + review của #130, ghi
rõ ngày giờ ở khoá `pham_vi_da_kiem_khong_thay_ban_dang` của mỗi biên nhận) **không thấy**
comment hay review nào mang nguyên văn chúng — đọc đúng là "không thấy trong phạm vi đã kiểm",
không phải "không tồn tại".

Biên nhận r4 vì thế mang `evidence_channel: repo_file`, và `evidence_url` neo vào commit
**master** `3223644` chứ không vào nhánh công bố: `ops/HO_SO_wp55-r4.md` khai kế hoạch xoá các
nhánh `ops/**` sau khi land hồ sơ, mà một URL trỏ nhánh sắp xoá chính là lớp lỗi lease #3 đã
trả giá. Nhánh công bố vẫn ghi đủ trong biên nhận ở `published_first` — nhưng kèm cờ
`truy_xuat_published_khong_bao_dam: true`, vì các commit ấy sống trên nhánh sắp bị xoá và git
được phép thu hồi object không còn ref. Thứ bảo đảm là `evidence_url` + `verdict_sha256`; muốn
giữ cả lịch sử công bố thì phải có tag/ref lưu trữ **trước** khi xoá nhánh, và việc đó **chưa
làm**.

Riêng `wp55-r4-review-1` có **hai** mốc, tách thành hai khoá: `published_first` (`b4e5c5f9`,
commit **thêm** tệp, băm `7dd8e203…`) và `published_ban_hien_hanh` (`872679c3`, commit **sửa**
tệp khi reviewer tự rút một finding, băm `fe002e5b…` — bản trùng byte với master).

**Năm biên nhận r4 do một phiên `claude-session` viết SAU, không phải reviewer** — PR #132 land
verdict mà quên biên nhận và quên bảng này, làm `t27` đỏ trên master (`29/30`). Mọi trường
trong chúng là thứ **đo được từ kho** (băm, commit công bố, ngày commit, lease), và mỗi tệp có
khoá `receipt_khong_khai` nói rõ thứ nó **không** khai.

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
