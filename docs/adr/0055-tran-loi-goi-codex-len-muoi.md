# ADR-0055 — Trần trục LỜI GỌI Codex nâng lên MƯỜI, và dòng khai vẫn là thứ duy nhất bật nó

- **Trạng thái:** Accepted (2026-10-25, chỉ thị chủ kho `ducthangho`; thi hành bằng packet `wp919`
  revision 1, Issue #919, comment cấp quyền `issuecomment-6393799783` — không phải một phiên tự nâng trần)

Mỗi PR packet được dùng tối đa **mười lời gọi Codex review** — trục LỜI GỌI, bộ đếm
`codex_review_calls_used`. ADR này thay **đúng một con số** của `ADR-0052`: tám thành mười. Mọi phần
khác của `ADR-0052` giữ nguyên hiệu lực: cách đếm một lời gọi, điều kiện cấp mọi lượt sau lượt đầu, mức
dành sẵn **hai** lượt của `ADR-0041`, Review Rescue Checkpoint (`ADR-0037`) khi hết trần, trục VÒNG
(`ADR-0048`) và trục ATTEMPT. Nâng trần mà đồng thời nới cách đếm là nâng hai thứ cùng lúc rồi không biết
cái nào có tác dụng.

## Vì sao, và vì sao con số một mình KHÔNG cứu được ca đã xảy ra

Chỉ thị nguyên văn trong phiên ngày 25-10-2026: *"Tôi duyệt trần 10, ghi vào protocol luôn đi"*; phạm vi
chốt bằng câu hỏi trong cùng phiên: **mười lời gọi mỗi PR, cho mọi packet**. Ca dẫn tới chỉ thị: PR #909
(packet wp748 r25) dùng **năm** lời gọi — hai lượt `launcher.py run` bị executor dừng sau khi đã có output,
hai lượt chạy trọn, một lượt connector khi PR được đánh dấu ready — trong khi đặc tả của nó **không có dòng
khai** nào, nên trần thực tế của nó là **hai**, không phải tám (hồ sơ
`ops/land/pr909-wp748-r25-land-evidence.yaml`, khối `tran_va_vi_pham`). Lần trước cùng lỗi là #892.

Nên ghi thẳng: nâng tám lên mười **không** đổi kết luận của ca ấy. Thứ thiếu ở đó là dòng khai, không phải
con số. Một đặc tả không khai vẫn chịu trần **hai** sau ADR này, y như trước.

## Hiệu lực — luật OID land của `ADR-0052`, token riêng; không hồi tố

Luật OID land **y hệt** mục *"Hiệu lực"* của `ADR-0052` (vì sao không dùng ngày, thời điểm commit hay
`base_sha`: xem ở đó), chỉ thay token và tệp. Mọi phép so dưới đây làm trên **byte gốc** của blob đặc tả mà
`spec_hash` của lease trỏ tới.

**Dòng khai** của ADR này là mọi dòng bắt đầu bằng `tran_loi_goi_codex: ADR-0055@`. Một dòng khai **hợp lệ**
khi nó khớp trọn `^tran_loi_goi_codex: ADR-0055@([0-9a-f]{40})$` và OID `<L>` bắt được thoả cả ba phép đo:

1. `git cat-file -e <L>:docs/adr/0055-tran-loi-goi-codex-len-muoi.md` ⇒ `rc=0`;
2. `git cat-file -e <L>^1:docs/adr/0055-tran-loi-goi-codex-len-muoi.md` ⇒ `rc≠0`;
3. `git rev-list --first-parent origin/master | grep -qx <L>` trên clone **không shallow**, ref vừa fetch.

Dòng khai của `ADR-0052` là mọi dòng bắt đầu bằng `tran_loi_goi_codex: ADR-0052@`; hợp lệ hay không theo
đúng luật của `ADR-0052`.

Trần **mười** áp **khi và chỉ khi** đặc tả có **đúng một** dòng khai `ADR-0055`, dòng ấy hợp lệ, và đặc tả
**không có** dòng khai `ADR-0052` nào. Bảng dưới là hệ quả của câu ấy, không phải luật thứ hai:

| dòng khai `ADR-0055` | dòng khai `ADR-0052` | trần |
|---|---|---:|
| không có | — | theo `ADR-0052`, không đổi (tám hoặc hai) |
| đúng một, hợp lệ | không có | **mười** |
| đúng một, hợp lệ | đúng một, hợp lệ theo `ADR-0052` | **tám** — trần thấp hơn |
| đúng một, hợp lệ | có nhưng không hợp lệ theo `ADR-0052` (trùng, sai mẫu, sai phép đo) | **hai** |
| hai dòng trở lên, hoặc sai mẫu, hoặc một phép đo `rc` sai, hoặc **không đo được** | bất kỳ | **hai** |

Bảng **bảo thủ** theo đúng ba nghĩa sau, và chỉ ba nghĩa ấy:

1. Thêm một dòng khai `ADR-0055` **không hợp lệ** (trùng, sai mẫu, sai phép đo, không đo được) không bao giờ
   làm trần tăng.
2. Đặc tả đã chọn **tám** hoặc **mười**: thêm bất kỳ dòng khai nào, đúng hay sai, của ADR nào, không làm trần
   tăng — nó giữ nguyên hoặc xuống.
3. Đặc tả không có dòng khai `ADR-0055` nào thì kết quả y hệt trước ADR này, kể cả cách `ADR-0052` so khớp
   nguyên văn dòng khai của nó.

Trần **chỉ** đi lên khi người soạn thêm một dòng opt-in **hợp lệ** vào đặc tả đang ở trần thấp hơn: từ hai lên
mười bằng đúng một dòng `ADR-0055`, hoặc từ hai lên tám theo luật của `ADR-0052`. Đó là chủ đích của opt-in,
không phải lỗ. Hàng thứ ba của bảng là luật *"trần chạm trước thắng"* của `ADR-0043` áp cho hai khai báo trên
cùng một trục.

Không hồi tố: ADR này **không** sửa `ADR-0036`, `ADR-0037`, `ADR-0038`, `ADR-0041`, `ADR-0048`,
`ADR-0052` hay đặc tả đóng băng nào. Đặc tả đã đóng băng mà muốn trần mười phải sửa thành revision mới
theo §3.2 — hoặc chủ kho nâng riêng bằng khối `nang_tran` như cũ.

Giới hạn đã biết, chép từ `ADR-0052`: land bằng **fast-forward** đưa chính commit của tác giả lên chuỗi
first-parent nên OID ấy có thể được biết trước; PR của kho không land kiểu ấy, nếu xảy ra thì người cấp
lease kiểm tay.

## Trần LỜI GỌI nay BẰNG trần VÒNG — câu của `ADR-0052` về thứ tự chạm không còn đúng nguyên văn

`ADR-0052` viết: với reviewer Codex, trần tám lời gọi **luôn chạm trước** trần mười vòng của
`ADR-0048`. Với mười lời gọi, hai trần **bằng nhau**. Lý lẽ của `ADR-0052` vẫn đứng — mọi lời gọi đều
tính vào trục LỜI GỌI, còn trục VÒNG chỉ tính verdict có biên nhận hợp lệ, nên số vòng Codex của một PR
không vượt được số lời gọi Codex của nó — chỉ đổi hệ quả: với PR **chỉ có** reviewer Codex, trục LỜI GỌI chạm
**trước hoặc cùng lúc** với trục VÒNG, không bao giờ sau. PR có thêm reviewer khác nền (phiên Claude độc
lập, human) thì trục VÒNG đếm **tổng** số vòng hợp lệ của mọi reviewer, nên nó có thể chạm trước — một vòng
Codex cộng chín vòng khác là mười vòng với một lời gọi. Hai trần bằng số không có nghĩa hai bộ đếm bằng
nhau hay cạn cùng lúc. Đây là luật *"trần chạm trước thắng"* của `ADR-0043`; ghi ra để không ai đọc thành
*"mười lời gọi cộng mười vòng"*.

## Cổng: có bộ đếm, nhưng nó KHÔNG đọc dòng khai — sửa lời khai của `ADR-0052`

`ADR-0052` (đo 17:01Z 16-10-2026) khai `codex_review_calls_used` có **0** dòng trong mã. Lời khai ấy
**đúng lúc ADR-0052 land** (`8ab1007`, 07:45:01Z 17-10-2026: 0 dòng ở `packet_loop.py`) và **đã cũ** từ
16:55:49Z cùng ngày, khi merge `d8b15cb` (PR #779) đưa vào master bộ đếm của packet #775 — commit triển khai
`97291ab` (*"trần vòng review + lời gọi codex cưỡng chế Review Rescue Checkpoint"*, tạo trên nhánh riêng ngày
16-10). Đếm nguyên từ ở `packet_loop.py`: `d8b15cb^1` **0** dòng, `d8b15cb` **8** dòng. Đo lại 25-10-2026 trên
base `9371628`, khớp nguyên từ:

| tên | `ops/lease_publish.py` | `.claude/dev/packet_loop.py` |
|---|---:|---:|
| `codex_review_calls_used` | 0 | 8 dòng |
| `nang_tran` | 0 | 8 dòng |
| `tran_loi_goi_codex` | 0 | 0 |

Cơ chế ấy làm được, và KHÔNG làm được:

- `packet_loop.py init --codex-review-calls-limit N` đặt trần vào state; **mặc định
  `MAC_DINH_TRAN_CODEX = 2`** — đúng luật fail-closed *"không dòng khai ⇒ hai"*, nên ADR này không đòi
  sửa mã.
- `record-codex-call` **chặn TRƯỚC khi vượt** trần trong state; `nang-tran` ghi khối nâng trần (lời khai,
  không phải bằng chứng); `record-rescue --quyet-dinh nang_tran` là cửa ra khỏi checkpoint.
- **Không gì đọc dòng `tran_loi_goi_codex:` của đặc tả** (0 dòng ở cả hai tệp). Đường thường để trần mười
  vào state là người khởi tạo tự truyền `--codex-review-calls-limit 10` sau khi tự áp luật chọn ở mục
  *"Hiệu lực"*; đường kia là `nang-tran --tran-moi 10` trên state đã có, tức một lần nâng trần phải có thẩm
  quyền riêng.
- Bộ đếm chỉ đếm những lời gọi được **ghi** bằng `record-codex-call`; `launcher.py run` tự nó không cưỡng
  chế trần nào. Với PR #909, hồ sơ trong kho chứng minh **năm** lời gọi trên trần **hai**, nhưng **không**
  chứa state hay transcript nào cho biết bộ đếm lời gọi có được dùng hay không — `KHÔNG ĐO ĐƯỢC` từ kho. Lời
  khai của chính executor trong phiên (chưa lưu thành hồ sơ): nó không gọi `record-codex-call` lần nào.

Vì vậy: trước MỖI lời gọi Codex, người gọi đếm số đã dùng và đọc trần trong lease cùng dòng khai của đặc
tả; vượt thì dừng và xin `nang_tran` TRƯỚC khi gọi. Phần ấy vẫn là kỷ luật, không phải cổng.

## Con số chỉ có MỘT chỗ ở

Chỗ ở duy nhất của con số **mười** là **tệp này**. `docs/PROTOCOL_DA_PHIEN.md` §20 thêm một dòng
`ADR-0055` không mang con số, và ô trạng thái dòng `ADR-0052` ghi con số của nó đã bị thay.

## Nợ

- **Không có con trỏ tiến** từ `ADR-0052` tới đây. Thân `docs/PROTOCOL_DA_PHIEN.md` nhắc `ADR-0052` năm lần:
  **bốn** lần làm nơi đặt con số trần (§8 hai lần, §12 hai lần) và **một** lần cho điều kiện cấp lượt sau
  lượt đầu (§8) — điều kiện ấy ADR này giữ nguyên, nên câu ấy vẫn đúng cho mọi packet. Bốn câu về con số vẫn
  đúng cho packet khai `ADR-0052`; với packet khai `ADR-0055` thì đường định tuyến duy nhất là bảng §20. Packet này giới hạn
  ở §20 theo đặc tả, nên không sửa các câu ấy.
- **Không có số đo nào biện hộ con số mười**, cũng như tám trước nó: kho chưa có giá trị bộ đếm cho đủ PR
  để biết một PR thường dùng bao nhiêu lời gọi. Mười là **quyết định của chủ kho**; đừng khai mạnh hơn thế.
- **Dòng khai không được máy đọc** (mục trên). Muốn cổng thật đặt trần từ đặc tả là một packet mã riêng
  đụng `packet_loop.py`.
