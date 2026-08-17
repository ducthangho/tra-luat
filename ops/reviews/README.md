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
| `pr134-ci-lease-gate-codex-verdict.md` | `windows-chua-do-that` | Verdict báo `30/30`, nhưng con số ấy **đo trên Linux** — reviewer từ chối gọi Windows là đạt vì chưa chạy thật. **CẬP NHẬT sau khi verdict được ghi:** lượt Windows THẬT đầu tiên đã chạy (`workflow_dispatch` run `31968805678`, head `3ee62330`) và **xanh** — bước `lease-publish selftest` `success` trên `windows-latest`. Nhưng phần reviewer cảnh báo thì **vẫn chưa chứng minh được**: `t19_symlink_tro_RA_NGOAI_kho_thi_CHAN` bắt `OSError`/`NotImplementedError` rồi `return`, mà harness **vẫn tính ca đó vào số đạt**, nên một lượt Windows xanh có thể chứa một ca CÓ MẶT mà KHÔNG ĐO (đúng bệnh `t24`). Không đọc được đầu ra in ra của bước ấy để xác nhận — `get_job_logs` chỉ trả phần đuôi, và đuôi không chạm tới bước đó. **Xanh trên Windows ⇒ bộ chạy được; KHÔNG ⇒ mọi ca đều đo.** Nợ có sẵn của bộ test, **không** do PR "#134" tạo ra; cách chữa reviewer đề nghị là cho `t19` báo `SKIP` riêng và không tính vào số đạt. |
| `wp55-r2-review-5-codex-verdict.md` | `mutable-master-ref-in-repro-command` | Khối bash tái hiện `merged-tree-doctrine-false-positive` dùng `origin/master`, một ref **DI ĐỘNG**. Master lúc đo là `3d2c52d62696b0c7c190fd891115f543b0f9cb55`. **Thay cả hai chỗ `origin/master` bằng SHA đó**, nếu không bạn đang đo một cây khác. |
| `don-nhanh-base-review-3-claude-verdict.md` | `same-provider-khong-du-land` | Verdict này ghi `assurance: same_provider_approved` — reviewer là **`claude`**, **cùng nhà cung cấp** với người vá. §8 nói mức ấy **một mình không thay** mức assurance bắt buộc cho phạm vi workflow, và #150 sửa `.github/workflows/ci.yml`. **Đừng đọc verdict này — hay verdict `don-nhanh-kien-truc-gh-1` cùng chuỗi — thành điều kiện land.** Muốn land cần cross-review `codex` khi có quota, hoặc human review có audit của chủ kho. Sai lệch §8 do chủ kho chấp nhận trong phiên (lý do: `codex` sắp hết quota), đã khai trong lease. |
| `don-nhanh-kien-truc-gh-1-claude-verdict.md` | `mcp-do-duoc-roi-mat` | Verdict nói reviewer **không tái lập được** phép đo trong lease (`11 PR qua MCP, đủ head và base`). **Người vá đã tự kiểm và reviewer ĐÚNG:** chạy lại lúc `14:56Z` bằng **cùng token** (vân tay `49933df4`, độ dài 93) và **cùng đoạn mã** ⇒ `isError: true`, `403 Resource not accessible by personal access token`. Phép đo gốc chạy `~14:44Z` ⇒ nó **chết trong ~12 phút**, không phải "vài giờ" như verdict ước. Vân tay token **không đổi** ⇒ không phải token xoay vòng mà là trạng thái **uỷ quyền phía server** đổi. **Đừng chạy lại lệnh MCP trong verdict rồi kết luận gì từ kết quả** — đường ấy đã trôi, và chính sự trôi ấy là một phần của kết luận `giu_nguyen`. |
| `don-nhanh-base-review-6-claude-verdict.md` | `same-provider-khong-du-land` | Reviewer là **`claude`**, cùng nhà cung cấp với người vá. §8 nói mức ấy **một mình không thay** mức assurance bắt buộc cho phạm vi workflow, và #150 sửa `.github/workflows/ci.yml`. **Đừng đọc verdict này thành điều kiện land.** Muốn land cần cross-review `codex` khi có quota, hoặc human review có audit của chủ kho. Kèm một chỗ dễ sai: uỷ quyền `ops/uy-quyen-150-same-provider-20260817.yaml` neo `05568de` **đã hết hiệu lực** theo §9 — trỏ lại nó sang SHA mới là agent tự nới uỷ quyền, §2 cấm. |
| `don-nhanh-base-review-6-claude-verdict.md` | `so-dot-bien-neo-o-99e9383-khong-tai-hien-tren-HEAD` | Mọi con số đột biến trong verdict (B1–B4 **sống 21/21**, A1–A4 20/21) neo ở `99e9383e9ff60bb8850f41242beb607808a821e9`. **Bản vá P1 nằm ngay sau trên cùng nhánh**, nên chạy lại trên HEAD nhánh sẽ **KHÔNG** tái hiện: B1–B4 phải **chết** (20/21, đỏ `t21`). Muốn tái hiện đúng verdict thì `git worktree add --detach <đích> 99e9383…` rồi đo ở đó. **Thấy B1 chết trên HEAD không phải bằng chứng verdict sai** — nó là bằng chứng bản vá chạy. |
| `don-nhanh-base-review-6-claude-verdict.md` | `so-eol-checked-398-neo-theo-INDEX-luc-do` | Verdict đối chiếu `eol … checked=398` rồi kết luận "khớp". Số ấy đúng cho cây **trước khi stage** ba tệp `ops/` của đợt bàn giao. `eol_policy.py --all` đọc **INDEX của git**, nên nó đổi theo **thời điểm đo**, không theo mã: đo lại sau khi stage cho **401**, và mỗi tệp thêm vào lại cộng tiếp. **Đừng đọc một con số khác 398 thành hồi quy** — đọc `violations`, và ghi kèm neo (SHA + trạng thái index) cho mọi số cổng. |
| `tao-tag-luu-tru-review-1-codex-verdict.md` | `so-do-thieu-actionlint` | Mọi con số trong verdict (`81/82`, `73/74`, `79/82`, `80/82`) đo ở môi trường **KHÔNG có `actionlint`**, nên đã trừ sẵn đúng một ca — phép `actionlint` fail-close. Ở máy **có** `actionlint` thì cộng 1 vào từng số (`82/82`, `74/74`, `80/82`, `81/82`); chính verdict đã quy đổi sẵn cho hai số đột biến. **Đừng đọc `81/82` thành "có một ca hỏng"** — nó là bằng chứng chốt fail-close CHẠY. Hệ quả thật: `actionlint` trên bản vá này chỉ có **một** nguồn (người vá), reviewer khai `KHÔNG ĐO ĐƯỢC` và từ chối thay bằng PyYAML. |

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
| [`pr134-ci-lease-gate-codex-verdict.md`](pr134-ci-lease-gate-codex-verdict.md) | [`.receipt.yaml`](pr134-ci-lease-gate-codex-verdict.receipt.yaml) | — (không lease) | `approve_with_findings` | `ae755d10` | 7975 |
| [`doctor-github-mcp-review-6-codex-verdict.md`](doctor-github-mcp-review-6-codex-verdict.md) | [`.receipt.yaml`](doctor-github-mcp-review-6-codex-verdict.receipt.yaml) | `doctor-github-mcp-review-6-codex-20260817` | `approve` | `45a06e48` | 2160 |
| [`doctor-github-mcp-review-9-codex-verdict.md`](doctor-github-mcp-review-9-codex-verdict.md) | [`.receipt.yaml`](doctor-github-mcp-review-9-codex-verdict.receipt.yaml) | `doctor-github-mcp-review-9-codex-20260817` | `approve` | `0826629a` | 1156 |
| [`tao-tag-luu-tru-review-1-codex-verdict.md`](tao-tag-luu-tru-review-1-codex-verdict.md) | [`.receipt.yaml`](tao-tag-luu-tru-review-1-codex-verdict.receipt.yaml) | `tao-tag-luu-tru-review-1-codex-20260817` | `approve` | `525c824e` | 2841 |
| [`don-nhanh-base-review-1-codex-verdict.md`](don-nhanh-base-review-1-codex-verdict.md) | [`.receipt.yaml`](don-nhanh-base-review-1-codex-verdict.receipt.yaml) | `don-nhanh-base-review-1-codex-20260817` | `changes_requested` | `5bc635d2` | 3579 |
| [`don-nhanh-base-review-2-codex-verdict.md`](don-nhanh-base-review-2-codex-verdict.md) | [`.receipt.yaml`](don-nhanh-base-review-2-codex-verdict.receipt.yaml) | `don-nhanh-base-review-2-codex-20260817` | `changes_requested` | `1511dd75` | 2545 |
| [`don-nhanh-base-review-3-claude-verdict.md`](don-nhanh-base-review-3-claude-verdict.md) | [`.receipt.yaml`](don-nhanh-base-review-3-claude-verdict.receipt.yaml) | `don-nhanh-base-review-3-claude-20260817` | `changes_requested` | `0ce4d491` | 7829 |
| [`don-nhanh-kien-truc-gh-1-claude-verdict.md`](don-nhanh-kien-truc-gh-1-claude-verdict.md) | [`.receipt.yaml`](don-nhanh-kien-truc-gh-1-claude-verdict.receipt.yaml) | `don-nhanh-kien-truc-gh-1-claude-20260817` | `giu_nguyen` | `bfeedfc4` | 11695 |
| [`don-nhanh-base-review-6-claude-verdict.md`](don-nhanh-base-review-6-claude-verdict.md) | [`.receipt.yaml`](don-nhanh-base-review-6-claude-verdict.receipt.yaml) | `don-nhanh-base-review-6-claude-20260817` | `changes_requested` | `99e9383e` | 13627 |

### Năm hàng `don-nhanh-*` — chuỗi ĐẦU TIÊN của bảng này KHÔNG có hàng `approve` nào

Năm hàng ấy thuộc **PR #150** và tới lúc ghi thì **PR chưa land**. Đọc chúng theo thứ tự,
vì cái đáng học nằm ở **chuỗi**, không ở từng hàng:

| lượt | reviewer | finding | lớp lỗi |
|---|---|---|---|
| 1 | `codex` | `gh` thoát khác 0 mà in JSON hợp lệ ⇒ fail-close mở toang, **xoá thật** | mã thoát bị bỏ qua |
| 2 | `codex` | `2>&1` trộn stderr vào JSON ⇒ thao tác hợp lệ **bị từ chối oan** | hai luồng gộp làm một |
| 3 | `claude` | đếm **số dòng thô** thay vì **nội dung đã tách** vẫn qua bộ test | rỗng-vs-vắng |
| 4 | `claude` | `-ge`→`-eq` và so-sánh-**chuỗi** đều sống 18/18; mặc định `TranPR` không ghim | test không phân biệt số/chuỗi |
| 5 | `claude` | `gh` giả **mù với argv** ⇒ 4 đột biến sống 21/21, một con tái tạo đúng lỗ gốc | đồ giả mô phỏng TRẠNG THÁI, không mô phỏng HỢP ĐỒNG |
| 6 | `claude` | chốt argv `-contains` mù với token **THỪA** ⇒ 4 đột biến mới sống 21/21 | danh-sách-cấm-theo-token |

**Lượt 4 và 5 KHÔNG có tệp ở đây** — chúng chỉ sống trong log chạy dưới `scratchpad/`, tức
NGOÀI kho, đúng lớp nợ mà chuỗi `doctor-github-mcp` đã khai. Nên đừng đọc bảng trên thành
"ba lượt rồi nhảy sang lượt 6": hai lượt ở giữa **có thật, có finding thật**, chỉ là không
tra lại được từ kho. `lease_id` của chúng còn trong `ops/leases/`.

**Lượt 6 đáng đọc kỹ nhất, vì nó là hồi quy của chính bản vá lượt 5.** Lượt 5 bắt `gh` giả
mù argv; bản vá cho nó dựng chốt đòi sáu token bằng `-contains`. Lượt 6 đo ra chốt ấy **đo
sự CÓ MẶT của từng token, không đo CÂU HỎI** — nên thêm `--limit 30` **sau** `--limit 1000`
vẫn 21/21, mà trên `gh` thật cờ-sau-thắng ⇒ limit hiệu lực 30 ⇒ **tái sinh đúng lỗ gốc mà
cả PR #150 sinh ra để vá**. Cùng hình dạng "vá một lỗ mà mở lỗ khác" như lượt 2 với lượt 1.
Nó còn bắt một **lời khai sai trong chú thích** (`t21` khai thêm `--repo` sẽ làm ca đỏ — đo
được là không) đúng lúc bản vá ấy đang sửa một lời khai sai khác ở `t19`.

**Không finding nào là lỗi nghiệp vụ.** Cả ba nằm ở **kênh đọc đầu ra của một tiến trình
con**, và **lượt 2 là hồi quy do chính bản vá lượt 1 đẻ ra** — hình dạng `CLAUDE.md` gọi là
*"vá một lỗ mà mở lỗ khác trong cùng hàm"*.

Ba lần cùng một hình dạng là ngưỡng mà `CLAUDE.md` bảo dừng lại hỏi *"có nên làm việc này
không"* thay vì *"vá thế nào"*. Hàng thứ tư (`kien-truc-gh-1`) là lượt đặt câu hỏi ấy, và nó
trả lời **`giu_nguyen`** — nhưng bằng một đường không ai thiết kế: bằng chứng người vá đưa
vào lease để **ủng hộ** phương án MCP đã chết trong ~12 phút, và chính sự bốc hơi ấy thành
lý do mạnh nhất để **không** thay một fail-close đã cứng qua ba vòng.

**Hai hàng cuối chỉ đạt `same_provider_approved`** — reviewer cùng nhà cung cấp với người vá.
Bảng này không có cột assurance, nên đừng đọc chúng ngang hàng với các hàng `cross_approved`
phía trên; xem hai hàng cảnh báo tương ứng.

Hàng `tao-tag-luu-tru-review-1` là hàng **`approve` ở lượt 1** duy nhất của bảng này, nên
nó dễ bị đọc sai theo hướng ngược lại: không phải "việc dễ", mà là lượt đầu tiên áp
**phạm vi đóng băng** ngay từ đầu — hai tệp, `+36/−4`, lease hỏi đúng bốn câu ĐO ĐƯỢC, và
mọi thứ không phải hồi quy/lỗ an ninh/P1 bị bắt vào `## Nợ khai báo` thay vì `## Findings`.
Đây là cùng cách làm đã kéo chuỗi `doctor-github-mcp` ra khỏi tám lượt `changes_requested`.
Nội dung nó duyệt là bản vá **MỞ một chốt an ninh** (`tao-tag` được tạo `luu-tru/*`), nên
biên nhận ghi riêng từng biên đã đo: `xoa-tag luu-tru/*` **vẫn DỪNG**, `xoa-nhanh` **không
bị nới**, và `luu-tru-gia/` `xluu-tru/` **không khớp oan**. Reviewer cũng **bác một nửa**
lập luận của người vá — về kỹ thuật thì "đặt tên tag khác" vẫn qua được chốt `xoa-nhanh`;
lý do thật để vá là **quy ước không gian tên**, không phải "workflow không chạy được".

Hai hàng `doctor-github-mcp-review-*` là việc **dev-side ngoài packet** — nó sửa
`.claude/dev/launcher.py`, không đụng `write_set` của wp55, và lease ghi `attempts 0/0`.
**Đọc kỹ chỗ này: nó là lượt THỨ SÁU, và năm lượt trước KHÔNG có tệp ở đây.** Cả năm đều
`changes_requested`, và bốn lượt đầu reviewer đều tìm được đột biến SỐNG SÓT ở cùng một lớp
(bộ test đo ĐỒ GIẢ chứ không đo HỢP ĐỒNG) — mỗi lần phải đổi KIẾN TRÚC chốt chứ không phải
thêm điều kiện. Chúng chỉ sống trong log chạy dưới `scratchpad/`, tức NGOÀI kho, nên chuỗi
lập luận dẫn tới `approve` này **không tra lại được đầy đủ từ kho**. Biên nhận khai thẳng
điều đó ở `luot_truoc_khong_duoc_ghi_thanh_tep`, kèm `lease_id`/`reviewed_sha`/`short_id`
của từng lượt để ai muốn thì còn biết đường tìm. Một hàng `approve` đứng một mình ở bảng
này rất dễ đọc thành "duyệt ngay lượt đầu"; nó không phải vậy.

**Hàng `review-9` KHÔNG phải lượt thứ chín của cùng một bản vá.** Lượt 6 `approve`
trên nền `e38b0be`; rồi #143 land và sửa CHÍNH hàm ấy, nên nền thành `c7ad260` và
verdict lượt 6 không còn phủ mã. Lượt 7..9 xét **BẢN HOÀ** — mã khác, nền khác.
Lượt 9 đóng băng phạm vi (không ca mới, không hàm mới) và ra `approve` với
**Findings TRỐNG và Nợ khai báo TRỐNG** — chín lượt trước không lượt nào trống cả hai.

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
trả giá. Nhánh công bố vẫn ghi đủ trong biên nhận ở `published_first`.

**Các nhánh `ops/wp55-r4-*` nay ĐÃ XOÁ** (đo: `git ls-remote --heads origin 'refs/heads/ops/wp55-r4*'`
trả rỗng), và **tag lưu trữ đã tạo TRƯỚC khi xoá** — đúng thứ tự mà bản đầu của trang này còn
phải dặn. Biên nhận nay mang **hai** khoá thay cho một boolean: `truy_xuat_published_qua_tag_tai_lan_do: true`
và `truy_xuat_published_duoc_bao_dam_lau_dai: false` — vì tag **xoá được**, nên "đo được ở lần
đo" khác hẳn "bảo đảm lâu dài", và một cờ `khong_bao_dam: false` đọc máy móc thành cái thứ hai.
Kèm khoá `tag_giu_published` nêu đích danh tag giữ từng commit:

| commit | tag giữ nó |
|---|---|
| `b4e5c5f9` | `luu-tru/wp55-r4-verdict-review-1-ban-dau` |
| `872679c3` | `luu-tru/wp55-r4-verdict-review-1` |
| `c2e7c1f5` | `luu-tru/wp55-r4-verdict-review-2` |
| `6a74f62b` | `luu-tru/wp55-r4-verdict-di-tru` |
| `699ac9af` | `luu-tru/wp55-r4-verdict-viet-lai` |
| `1cfe47f8` | `luu-tru/wp55-r4-verdict-rebase` |

Phép đo dùng để hạ cờ **không** phải là liệt kê ref — liệt kê chỉ chứng minh cái tên còn đó.
Nó là: `git init` một kho **trống**, `fetch` từng tag từ remote, rồi băm lại tệp verdict trong
kho ấy. Kết quả, nói chính xác: **6/6 khớp con băm ghi cho đúng mốc đó**, và **5/6 đồng thời
khớp `verdict_sha256`**. Mốc thứ sáu là `b4e5c5f9` — bản trước khi reviewer tự rút finding,
băm `7dd8e203…` — nó khớp `published_first.sha256_tai_commit` chứ **không** khớp
`verdict_sha256` hiện hành, và đúng ra phải thế. Điều chung cho cả sáu: nhánh đã mất mà nội
dung vẫn tải về được, đúng byte.

**Xoá tag = biến `published_*` thành SHA không tra được.** Đó giờ là ref bền duy nhất giữ chúng.

### Hai tag của 17-08 — và chỗ trang này từng nói một điều không còn đúng

| commit | tag giữ nó | verdict |
|---|---|---|
| `de86c247` | `luu-tru/doctor-github-mcp-verdict-9` | `doctor-github-mcp-review-9` |
| `9d3e3e9e` | `luu-tru/tao-tag-luu-tru-verdict-1` | `tao-tag-luu-tru-review-1` |

Cùng phép đo với sáu tag `wp55-r4` ở trên — `git init` kho **trống**, fetch **đúng một** ref
`refs/tags/…`, băm lại tệp verdict trong kho ấy: **2/2 khớp cả `verdict_sha256` lẫn
`verdict_bytes`** (`0923678b…` 1156 byte · `be342cc4…` 2841 byte). Một kho không có gì
ngoài cái tag vẫn dựng lại được verdict đúng từng byte.

**Chỗ đáng ghi không phải hai cái tag, mà là vì sao suốt một thời gian không tạo được
cái nào.** Chốt `tao-tag` của `ops-don-ref.yml` cấm đúng không gian tên `luu-tru/`, trong
khi chốt `xoa-nhanh` của **cùng tệp ấy** dặn nguyên văn *"Tạo tag TRƯỚC (hành động
tao-tag), rồi mới xoá"*. Không lượt chạy nào thoả được cả hai vế — workflow tự chặn trình
tự do chính nó quy định, và câu "chưa có tag" trong ba biên nhận không phải vì ai quên.
PR #147 gỡ đúng chỗ đó; hai tag trên là hai lượt `tao-tag` **đầu tiên** chạy được trong
`luu-tru/`. Một trong hai neo chính verdict đã duyệt bản vá ấy.

**Biên nhận `review-6` KHÔNG có tag riêng, và điều đó không tương đương.** Commit
`4920113a` bền nhờ **dòng dõi master** (đã đo `git merge-base --is-ancestor` → rc=0), chứ
không nhờ mỏ neo tag. Hai thứ đó hỏng theo hai cách khác nhau: dòng dõi mất nếu master bị
ép lùi — mà proxy egress chặn *xoá* ref lại **vẫn cho** `git push --force`, đã ghi trong
`CLAUDE.md` — còn tag thì `xoa-tag` dưới `luu-tru/` cấm tuyệt đối. `truy_xuat_tag` của
biên nhận ấy để `null`, không để `false`.

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
