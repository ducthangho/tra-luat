verdict: approve
reviewed_sha: 93abdf2aeb9c

# CROSS-REVIEW LƯỢT 2 — packet #548 `CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND` r1/g1

| | |
|---|---|
| `reviewed_sha` | `93abdf2aeb9c` (PR #550) |
| `base_sha` | `a612c70cbc56` — **base trôi đã giải**, agy merge master ở `f4906f6` |
| `numstat` so base mới | **4 tệp, +226 / −24** |
| lượt trước | `d1258fef203d` — lượt 1, `changes_requested`, 2 × P2 + 1 × P3 |
| kết luận | **`approve`** — cả ba đóng, có phép đo; **1 × P3 MỚI**, không chặn |
| assurance | **`advisory_review`** |

## TRƯỚC HẾT — TÔI SỬA MỘT SỐ LIỆU SAI CỦA CHÍNH VERDICT LƯỢT 1

Verdict lượt 1 (`ops/reviews/ci-windows-review-1-claude-verdict.md`,
`sha256 606287b285c88e99a7fc7c8c136a72a593687597f234c2162b55692483dee989`) khai:

> `actionlint` (có `shellcheck 0.9.0`) — **rc=0** ở CẢ HAI vế …

**Sai.** Tôi chạy `actionlint 2>&1 | tail -5; echo "rc=$?"` — `$?` ở đó là mã thoát của **`tail`**, không
phải của `actionlint`. Đúng cái bẫy mà chính tôi vừa dặn agy tránh trong bản bàn giao ở #548
(*"Đọc `rc` TRỰC TIẾP, đừng qua pipe"*), và bẫy ấy đã có tên trong `CLAUDE.md`.

Đo lại, `rc` đọc trực tiếp, bốn vế:

| vế | `rc` | số finding |
|---|---|---|
| nền `f27a28ffa3cc` | **1** | 1 (`ops-don-ref.yml SC1003:info`) |
| `d1258fef203d` (lượt 1) | **1** | 1 |
| `93abdf2aeb9c` (lượt này) | **1** | 1 |
| `origin/master` `a612c70cbc56` | **1** | 1 |

**Kết luận của lượt 1 KHÔNG đổi: `delta = 0`.** Chỉ con số `rc` là sai, và nó khớp đúng nền mà
`CLAUDE.md` đã ghi (*"đo lại 23-08-2026: `rc=1`, một finding `SC1003:info` … Delta so `origin/master`
vẫn = 0 — đỏ sẵn, không phải hồi quy"*).

Verdict lượt 1 **giữ nguyên trên đĩa** làm hồ sơ; đính chính sống ở đây, đúng quy ước bản-sửa-trong-
verdict-MỚI-có-back-link.

## KHAI VÒNG TRÒN — LƯỢT NÀY CÓ, VÀ Ở ĐÂU

Khác lượt 1 (không có vòng tròn nào), lượt này **có**, phải khai cho chật:

- `P2-a`: tôi đề xuất *"2–4 dòng trong ADR ghi trạng thái đo được"*. agy làm đúng thế
  ⇒ phán quyết về **hình dạng** bản vá **không** có giá trị độc lập.
- `P2-b`: tôi liệt kê ba đường (a)/(b)/(c); agy chọn **(b)+(c)** — tức chọn **trong** danh sách tôi đưa
  ⇒ cùng giới hạn.
- `P3`: tôi đề xuất *"bỏ hai dòng, hoặc biến thành đột biến thật"*; agy chọn bỏ ⇒ cùng giới hạn.

**Thứ CÓ giá trị độc lập**, và nó là phần nặng nhất của lượt này:

- **Phép đo mệnh đề `deploy-package.*`** — agy tự đo và tự sửa một sai sót trong ADR của chính họ;
  tôi đo **lại độc lập** trên cây và xác nhận từng vế (bảng dưới). Tôi không nhận lời khai.
- **Phép đo răng sau khi gỡ tautology** — đột biến bơm vào **hàm thật**, không đọc mã.
- **P3 mới** — tôi tìm ra nó bằng phép đo `rc`, không ai chỉ.

---

## `P2-a` — ĐÓNG

ADR-0049 nay ghi, nguyên văn từ cây:

> **Cổng Windows đang đỏ biến mất khỏi CI không phải vì được chữa:** Tại thời điểm land (commit
> `a612c70`, run `35232106589`, job `105238582317`), lane `gate (windows-latest)` trên `master` đang đỏ
> sẵn 15 ca ở bước 18 `lease-publish selftest` (`133/148 đạt`, do `shutil.which("git",
> path="/usr/bin:/bin")` hardcode tại `ops/lease_publish.py:1106`, nợ WP541). … ADR-0049 **KHÔNG** chữa
> nợ WP541.

Đủ ba thứ tôi đòi: **neo tra được** (commit · run · job), **con số** (`133/148`, 15 ca), **nguyên nhân
có địa chỉ** (`ops/lease_publish.py:1106`), cộng câu phủ định tường minh. Người đọc master xanh trở lại
sau khi #548 land nay **không** đọc được thành "WP541 đã chữa".

agy **không** chạm `ops/lease_publish.py` — đúng, nó ngoài write set. Đo: `git diff --numstat
a612c70..93abdf2 -- ops/lease_publish.py` ⇒ **rỗng**.

## `P2-b` — ĐÓNG, và phần mạnh nhất là agy tự bác một lời khai của chính mình

agy chọn **(b)+(c)**, **không** chọn (a). Đo: `git diff a612c70..93abdf2 -- .github/workflows/ci.yml`
cho ra **đúng diff của lượt 1**, không thêm `types:` nào. Tức agy **không tự ý đổi hành vi CI** khi tôi
đã dặn phải dừng hỏi chủ kho — tuân thủ ranh giới thẩm quyền.

### Phép đo (c): 8 cổng của `deploy-package.*` — tôi đo LẠI, không nhận lời khai

| mệnh đề trong ADR sau vá | phép đo của tôi | phán |
|---|---|---|
| 8 cổng là `selftest` `gen_inst` `workflow` `golden` `docclaims` `determinism` `relcheck` `relverify` | `scripts/deploy-package.sh:113-120` liệt kê **đúng tám tên ấy**, và dòng `123` lặp lại đúng thứ tự | **KHỚP** |
| **không** bao gồm `lease_publish_test` | `grep -c 'lease_publish_test'` ⇒ **0** ở **cả** `deploy-package.sh` **lẫn** `deploy-package.ps1` | **KHỚP** |
| dòng 234 của `.ps1` chặn thật | `Bad 'GATE ĐỎ — DỪNG, không build/không đẩy (golden diff = BUG của thay đổi, R6)'; exit 1` | **KHỚP** |
| `ci.yml` dùng `pull_request` mặc định, không khai `types:` | đọc khối `on:` — `pull_request:` **không** có `types:` | **KHỚP** |

**Đáng ghi công riêng:** bản ADR ở lượt 1 khai 8 cổng là `--selftest, doc-claims-check, doctrine-scan,
adr-song, workflow-audit, golden-test, determinism-audit, release-verify`. Đo ra thì **`doctrine-scan`
và `adr-song` KHÔNG nằm trong bộ ấy**; thật ra là `gen_inst` và `relcheck`. agy tự phát hiện và tự sửa
khi đi đo theo đường (c). Đó là **đúng thứ mà đường (c) sinh ra để mua**: một lời khai trong ADR bị
thay bằng một phép đo, và phép đo lật lại lời khai.

### Độ phủ

ADR nay khai thẳng độ phủ Windows tự động cho `ops/**`, `scripts/**`, `.github/**` về **0 trên thực
tế** dưới `manual_ci_budget: 0`, nêu cơ chế (nhãn không bắn vì thiếu `types:`), nêu **ai chịu rủi ro**
(*"Người điều phối và người phát hành"*), và nêu **WP541 là bằng chứng sống**. Đủ điều kiện `P2-b`.

## `P3` (lượt 1) — ĐÓNG, và răng còn nguyên

`grep -c 'chot_bi_go\|evaluator_doan_bua'` ⇒ **0**. agy còn sửa **cả docstring**: `t161` thôi khai
*"Đột biến: gỡ chốt…"*, `t162` phân biệt rõ *"Đột biến A3"* (thật) với *"Chốt fail-close A4"* (một câu
khẳng định, không phải đột biến). **Vá đúng chỗ hỏng — lời khai — chứ không vá quanh nó.**

Phản chứng bắt buộc: gỡ hai dòng ấy có làm mất răng không? Bơm fail-open vào **hàm thật** trên head mới:

| đột biến bơm vào hàm thật | ca | rc | câu đã giết |
|---|---|---|---|
| `_kiem_tra_nguon_duy_nhat_os_ci` luôn trả `[]` | `t161` **ĐỎ** | 1 | `"chốt không bắt được job lén khai os: []"` |
| `_danh_gia_bieu_thuc_chuan_bi` trả `["ubuntu-latest"]` thay vì `raise` | `t162` **ĐỎ** | 1 | `"PR nhãn windows phải chạy hai nền, nhận được: ['ubuntu-latest']"` |

Nền không đột biến: cả hai `1/1 đạt`, `rc=0`. **Giết y hệt lượt 1** ⇒ gỡ tautology **không mất gì**,
đúng như lượt 1 dự đoán.

---

## `P3-MỚI` — TIÊU CHÍ `A6` NHƯ ĐANG VIẾT **KHÔNG THỂ ĐẠT**

Thân PR #550 khai:

> **A6** (`actionlint`) — `rc=0`, 0 finding — **PASS** — Chạy trên cả 6 workflow, delta = 0

Đo lại (bảng ở đầu verdict này): `rc=1`, **1** finding, trên **cả bốn** vế kể cả nền và master. Nên:

1. Lời khai `rc=0, 0 finding` **sai**;
2. Phần *"delta = 0"* **đúng**;
3. Và nặng hơn cả hai: **`A6` phát biểu như thế thì KHÔNG BAO GIỜ đạt được** trên kho này chừng nào
   `ops-don-ref.yml` còn finding `SC1003:info` đỏ sẵn. Ai sau này cưỡng chế `A6` theo đúng chữ sẽ chặn
   packet vĩnh viễn vì một lỗi **không phải của packet**.

**Vì sao KHÔNG chặn `approve`:** đây là lỗi **phát biểu tiêu chí**, không phải lỗi mã, và cổng thực tế
(`delta = 0`) đã đạt. Sửa được bằng một dòng: phát biểu `A6` theo **DELTA so nền**, không theo `rc`
tuyệt đối — đúng doctrine ngưỡng của kho (*"tiêu chí là DELTA so master = 0, KHÔNG phải 0 tuyệt đối"*).

**Và tôi mắc ĐÚNG lỗi ấy ở lượt 1.** Cùng một nguyên nhân (`rc` qua pipe), cùng một ngày, hai bên độc
lập. Nêu ra đây vì một lỗi mà cả executor lẫn reviewer cùng mắc là dấu hiệu công cụ chứ không phải
người: cần một cách gọi `actionlint` chuẩn trong kho thay vì mỗi nơi tự gõ. Nợ: **`RC-QUA-PIPE-KHONG-
CO-CHOT`**.

---

## BẢNG ĐO ĐẦY ĐỦ — KỂ CẢ CÁI KHỚP

| phép đo | kết quả |
|---|---|
| base trôi | **đã giải** — `f4906f6` merge `a612c70`; merge sạch, không xung đột |
| `write_set` | **đúng 4 đường** |
| tệp trong `khong_duoc_cham` bị chạm | **0** (quét cả 11 đường) |
| `ops/lease_publish.py` | **không chạm** — đúng, ngoài write set |
| `docs/PROTOCOL_DA_PHIEN.md` | **+1 / −0**, vẫn đúng một hàng §20.A |
| `numstat` | **4 tệp, +226 / −24** ⇒ trần ngoại lệ 4 tệp / ≤300 → **đạt, dư 74 dòng** |
| `A1` `grep -c 'os: ${{ fromJSON'` | **1** |
| `adr-song` | **rc=0** |
| `doctrine-scan` | **rc=0** |
| `doc-claims-check --strict` | **rc=0** |
| `git diff --check` | **rc=0** |
| `actionlint` (có `shellcheck 0.9.0`) | **rc=1, 1 finding** trên cả bốn vế ⇒ **delta = 0** |
| `t161` · `t162` | `1/1 đạt`, `rc=0` mỗi ca |
| hai đột biến fail-open vào hàm thật | **bị giết** cả hai |

## `KHÔNG ĐO ĐƯỢC` — khai, không lấp

1. **Hành vi thật của ma trận trên CI.** `t162` đo một **evaluator viết tay**, không đo GitHub chạy
   thật. Đúng dưới `manual_ci_budget: 0`, nhưng evaluator hiểu khác GitHub thì bảng bốn ca vẫn xanh
   trong khi CI làm việc khác. Cùng họ *"YAML parse được KHÁC GitHub NHẬN"*. Phép đo duy nhất đóng
   được lớp này là **chính lượt CI sau khi merge** — nên lượt ấy phải được đọc, đừng bỏ qua.
2. **`gate` trên head `93abdf2`** — chưa đo lúc viết verdict này.

## NGUỒN CÓ THẨM QUYỀN

Tệp này trong kho, có băm. Bản đăng trên GitHub chỉ là **bản chiếu**.
Verdict lượt 1 (`606287b2…`) giữ nguyên; đính chính `actionlint rc` sống ở mục đầu tệp này.
