# Verdict lượt 5 — BẢN CHÉP TỪ COMMENT, KHÔNG PHẢI BẢN GỐC

**ĐỌC MỤC NÀY TRƯỚC KHI DÙNG TỆP NÀY LÀM BẰNG CHỨNG.**

Tên tệp có hậu tố `POSTED-COPY` là cố ý. Đây **không** phải tệp mà verdict lượt 5 viện dẫn.

| | |
|---|---|
| tệp verdict KHAI trong header review | `ops/reviews/wp55-r2-review-5-codex-verdict.md` |
| băm KHAI | `d1d04452d0ab…` · 4392 byte · *byte-identical với stdout của phiên reviewer* |
| tệp đó có trong kho không | **KHÔNG** — đã quét mọi ref remote (`git for-each-ref refs/remotes/origin`) |
| tệp này là gì | bản chép phần verdict từ review đã đăng trên PR #92 |
| nguồn chép | https://github.com/ducthangho/tra-luat/pull/92#pullrequestreview-4939956924 |
| băm của tệp này | tự đo bằng `sha256sum`, **KHÁC** `d1d04452d0ab…` — xem dưới |
| có thay được bản gốc không | **KHÔNG** |

## Vì sao băm chắc chắn KHÔNG khớp, và đó là thông tin chứ không phải sự cố

Ba lý do độc lập, mỗi lý do đủ một mình:

1. **Bản đăng đã qua ít nhất một lớp mã hoá.** Đọc lại review qua API cho thấy các dòng
   nối lệnh trong khối bash mang **hai** dấu chéo ngược (`\\`) ở chỗ shell chỉ cần **một**.
   Đó là dấu vết của một lớp thoát chuỗi trên đường đăng — cùng lớp đã đổi `"` thành
   `&#34;` trong thân #55, và cùng lớp verdict lượt 4 đã ghi nhận.
2. **Bản đăng có thêm phần không thuộc verdict**: khối trích dẫn mở đầu của người đăng hộ,
   và chân trang attribution. Bản gốc 4392 byte gần như chắc chắn không chứa chúng.
3. **Tệp này do một phiên khác chép lại**, không phải xuất từ `stdout` của phiên reviewer.

Nên đừng dùng tệp này để chứng minh xuất xứ. Dùng nó để **đọc được nội dung verdict mà
không cần vào GitHub**, và để có một mỏ neo git cho tới khi bản gốc được đẩy lên.

## Việc còn phải làm

Phiên reviewer soạn verdict — hoặc người đăng hộ đang giữ `stdout` của nó — cần đẩy tệp
gốc lên một nhánh `ops/**` với đúng tên `wp55-r2-review-5-codex-verdict.md`. Khi ấy băm
`d1d04452d0ab…` mới giải được, và tệp này nên bị xoá cùng lúc để khỏi còn hai bản.

---
---

# PR #92 review — verdict lượt 5 (phần chép nguyên trạng)

Verdict: `changes_requested` cho PR #92, neo chính xác tại `546ecf9fd4dfe889d0cd3ee77b9589d8bed0465f`.

## Findings

### `merged-tree-doctrine-false-positive` — P1 / blocking

`doctrine-scan` sạch trên branch nhưng đỏ trên cây sau merge với `origin/master=3d2c52d62696b0c7c190fd891115f543b0f9cb55`.

Lệnh tái hiện:

```bash
merged_tmp=$(mktemp -d /tmp/wp55-merged.XXXXXX)
git archive origin/master | tar -x -C "$merged_tmp"
git diff --binary \
  fbe5ab9e1ece3b45c065879bfd59dee2554db3e2..546ecf9fd4dfe889d0cd3ee77b9589d8bed0465f |
  git -C "$merged_tmp" apply
python "$merged_tmp/.claude/dev/packet_loop.py" doctrine-scan --root "$merged_tmp"
```

Kết quả:

```text
/tmp/wp55-merged.../CLAUDE.md:82: [bang-vai-tro-muc-2] chép doctrine: 'người có thẩm quyền'
1 chỗ chép doctrine trong adapter...
rc=6
```

Trong khi:

```bash
git merge-tree \
  fbe5ab9e1ece3b45c065879bfd59dee2554db3e2 \
  origin/master \
  546ecf9fd4dfe889d0cd3ee77b9589d8bed0465f
```

trả `rc=0`, không có conflict marker. Đây là lỗi tương thích tích hợp, không phải merge conflict.

### `partial-lease-authority-bypass` — P1 / blocking

`record-lease` chỉ tạo lease sau khi kiểm `lease_id`, `granted_by`, `evidence` và `expires_utc`. Nhưng `begin-attempt` chỉ đòi `lease` truthy và `expires_utc`, nên chấp nhận state không thể được tạo hợp lệ qua `record-lease`.

Fixture:

```json
{
  "state": "leased",
  "lease": {
    "expires_utc": "2099-01-01T00:00:00Z"
  }
}
```

Lệnh:

```bash
python .claude/dev/packet_loop.py \
  --state-dir <fixture-dir> \
  begin-attempt --packet 55 --provider claude
```

Kết quả:

```text
bắt đầu lượt 1/3 — state running
rc=0
```

Như vậy khẳng định tại dòng 507 rằng `lease` "hợp lệ" và chỉ đạt được qua `record-lease` không được mã cưỡng chế. Một state cũ/hỏng chỉ cần giữ `expires_utc` tương lai là đi vòng qua kiểm tra thẩm quyền.

Các kiểu sai khác:

```text
lease thiếu/null/dict rỗng          rc=8
lease là chuỗi                      rc=1, Traceback
expires_utc là số                   rc=1, Traceback
expires_utc sai/thiếu timezone      rc=2
```

Hai traceback cũng cho thấy nhánh malformed chưa fail-closed có kiểm soát.

---
---

# Ghi chú của phiên chép — đã ĐO LẠI, không chép suông

Cả hai finding đều **tái lập được độc lập** trên `546ecf9`:

- `merged-tree-doctrine-false-positive`: rc=6 trên cây đã merge, rc=0 trên nhánh một mình.
  Truy thêm tới nguyên nhân gốc mà verdict chưa nêu — `CLAUDE.md` của master **ngắt dòng
  ngay giữa cụm**: dòng 82 kết thúc bằng `người có`, dòng 83 bắt đầu bằng `thẩm quyền`.
  `_chuan_hoa` chuẩn hoá cả tệp nên nối hai dòng rồi khớp. Câu đó đang kể lại một kết quả
  đo, không chép doctrine.
- `partial-lease-authority-bypass`: `lease = {expires_utc: 2099-01-01T00:00:00Z}` cho rc=0
  và mở được lượt.

Một P1 thứ ba **không** nằm trong verdict này, do `chatgpt-codex-connector[bot]` nêu lúc
2026-08-14T17:27:49Z trên cùng head: `_chuan_hoa` dùng **NFC**, mà NFC theo định nghĩa
không gộp ký tự tương thích, nên `merged：` (hai chấm toàn rộng U+FF1A) cho rc=0. Cũng đã
tái lập.

Cả ba đi vào Packet Spec revision 3: `ops/specs/wp55-r3-spec.md`
(sha256 `e321f811724fae97b19d523a3e5159bc13b425cd15fc6c753c7439fe28cae22d`).
