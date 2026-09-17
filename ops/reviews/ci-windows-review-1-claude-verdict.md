verdict: changes_requested
reviewed_sha: d1258fef203d

# CROSS-REVIEW LƯỢT 1 — packet #548 `CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND` r1/g1

| | |
|---|---|
| `reviewed_sha` | `d1258fef203d` (PR #550) |
| `base_sha` khai trong lease | `f27a28ffa3cc` · `numstat` **4 tệp, +235 / −24** |
| kết luận | **`changes_requested`** — **2 × P2**, **1 × P3** |
| assurance | **`advisory_review`** |

## KHAI VÒNG TRÒN — LƯỢT NÀY KHÔNG CÓ

Tôi **không** cấp HINT patch nào cho packet này, không đề xuất hình dạng bản vá nào trước khi agy
thi công, và không đọc mã của packet trước lượt này. Nên khác #546, phán quyết lượt này có **giá trị
độc lập đầy đủ**. Ghi ra vì lease #546 đã bắt phải khai độ lệch ấy, và im lặng thì không phân biệt
được "không có vòng tròn" với "quên khai".

## VIỆC THỦ TỤC TRƯỚC ĐÃ — BASE ĐÃ TRÔI

PR #550 neo `base f27a28ffa3cc`; `origin/master` nay là **`a612c70cbc56`** (merge packet #546).

```
git merge-base --is-ancestor origin/master origin/agy/ci-windows-r1-g1   ⇒ SAI
```

Theo `.claude/skills/cross-review/SKILL.md` (luật `M8`): head đổi vì **base trôi** ⇒ **merge base
TRƯỚC**, rồi mở vòng trên head **sau** merge. Trôi này **không đụng write set** của #548 — #546 chỉ
chạm `.claude/dev/launcher.py`, `.claude/dev/launcher_test.py`, `.claude/hooks/session-start.sh` —
nên merge sẽ sạch. Nhưng verdict cuối phải neo head **sau** merge, và **executor** là người merge, không
phải reviewer.

---

## `P2-a` — PACKET LÀM BIẾN MẤT ĐÚNG CÁI CỔNG ĐANG ĐỎ, VÀ HỒ SƠ KHÔNG GHI ĐIỀU ĐÓ

**Đo được.** `gate (windows-latest)` trên `origin/master` `a612c70cbc56`: **FAILURE**
([job `105238582317`](https://github.com/ducthangho/tra-luat/actions/runs/35232106589/job/105238582317)),
đúng một bước đỏ — bước 18 `lease-publish selftest`. Log:

```
lease_publish: 133/148 đạt; đã chạy=148, bỏ qua=7
```

15 ca đỏ, gần như ca nào cũng một câu: `` KHÔNG_XÁC_ĐỊNH: không thấy `git` trong PATH tối thiểu
/usr/bin:/bin `` — nguồn `ops/lease_publish.py:1106`, tức nợ **WP541**.

**Packet này gỡ `github.ref == 'refs/heads/master'` khỏi điều kiện ma trận.** Sau khi land, push
master cho `["ubuntu-latest"]`, nên `gate (windows-latest)` **thôi chạy**. Cái đỏ trên **biến mất khỏi
CI — không phải vì được chữa, mà vì cổng không còn tồn tại ở đó**.

`ADR-0049` **có** khai phần mất mát (*"~22 bước test mất soi Windows tự động trên mỗi lần land"*),
và đó là khai **độ phủ**. Nó được viết **trước** khi lane ấy đỏ. Không dòng nào nói rằng tại thời
điểm land, lane bị gỡ **đang mang một lỗi thật, 15 ca, có tên**.

Hệ quả cụ thể: người đọc master xanh trở lại ngay sau khi #548 land sẽ kết luận WP541 đã chữa.
Đúng bài học đã trả giá của kho — *"cổng không nói dối, nó VẮNG MẶT; trên giao diện 'xanh' với
'không chạy' nhìn giống hệt nhau."*

**Đây KHÔNG phải phản đối quyết định.** Việc đổi tiêu chuẩn gate là chủ kho duyệt. Thứ thiếu là
**hồ sơ**.

**Vá đề xuất — 2–4 dòng trong `docs/adr/0049-*.md`** (đã trong write set): ghi trạng thái đo được tại
thời điểm land — `gate (windows-latest)` FAILURE trên `a612c70cbc56`, `lease_publish 133/148`, nguyên
nhân `ops/lease_publish.py:1106`, nợ WP541 — và nói thẳng rằng ADR này **không** chữa nó.

---

## `P2-b` — ĐƯỜNG NHÃN `windows` TRỞ THÀNH GÁNH CHỊU LỰC, MÀ ĐƯỜNG ẤY VỐN KHÔNG BẮN

Sau packet, điều kiện hai nền còn **đúng hai** cửa:

```yaml
(github.event_name == 'workflow_dispatch'
 || contains(github.event.pull_request.labels.*.name, 'windows'))
```

Cả hai đều có vấn đề đã biết trong kho, và packet làm chúng **gánh chịu lực** thay vì phụ trợ:

1. **Nhãn `windows` KHÔNG tự sinh lượt chạy.** `ci.yml` khai `pull_request:` mà **không** khai
   `types:`, nên mặc định chỉ bắn `opened`/`synchronize`/`reopened` — **`labeled` không nằm trong
   đó**. `CLAUDE.md` đã ghi nguyên văn bẫy này. Gắn nhãn xong vẫn đúng một check Ubuntu; ma trận chỉ
   đọc nhãn ở lượt bắn **kế tiếp**.
2. **`workflow_dispatch` bị CẤM.** `manual_ci_budget: 0` trong chính lease #548, và
   `prohibited_actions` liệt kê `workflow_dispatch` · `manual full CI` · `Windows CI`.

**Trước packet**, hai bẫy ấy vô hại: push master vẫn cho Windows, nên mọi thứ land đều được soi ít
nhất một lần. **Sau packet**, Windows tự động chỉ còn `launcher-windows.yml`, mà nó phủ
`.claude/dev/**`. Với `ops/**`, `scripts/**`, `.github/**` thì độ phủ Windows về **0 trên thực tế**
dưới đúng chính sách chi CI hiện hành.

**WP541 là bằng chứng sống**: một lỗi Windows-only nằm trong `ops/`, và sau packet này **không cổng
nào còn bắt được nó**.

`ADR-0049` khai rằng cổng hai nền trước phát hành do **8 cổng tại chỗ của `deploy-package.*`** bảo
đảm. Tôi **KHÔNG ĐO ĐƯỢC** mệnh đề ấy từ phiên này và không nhận nó: `deploy-package.ps1` là script
**chạy tay**, nên nó thuộc đúng lớp *"workflow chỉ chạy khi có người bấm là workflow KHÔNG có ai
canh"*. Cần đo: 8 cổng ấy có bao gồm `lease_publish_test` trên Windows không? Nếu không thì nó
**không** thay thế được thứ vừa bị gỡ, và ADR đang khai mạnh hơn phép đo.

**Vá đề xuất — ba đường, agy/chủ kho chọn:**
- **(a)** khai `types: [opened, synchronize, reopened, labeled]` cho `pull_request` ⇒ nhãn thành đường
  dùng được thật. Nhưng `.github/workflows/ci.yml` đã trong write set nên làm được **trong** packet này;
- **(b)** giữ nguyên cơ chế, nhưng `ADR-0049` phải khai thẳng rằng độ phủ Windows cho `ops/`,
  `scripts/`, `.github/` về **0** dưới `manual_ci_budget: 0`, và nêu ai chịu rủi ro;
- **(c)** đo mệnh đề `deploy-package.*` và ghi kết quả vào ADR thay vì khẳng định.

Tôi **không** chỉ định đường nào — (a) đổi hành vi CI nên có thể vượt ý định của spec đã đóng băng.

---

## `P3` — HAI "ĐỘT BIẾN" LÀ TAUTOLOGY, KHÔNG THỂ ĐỎ

`t161`:

```python
def chot_bi_go(wf):
    return []
bang(chot_bi_go(wf_gia_len) == [], "đột biến gỡ chốt phải làm ca lén chuyển sang đạt")
```

`t162`:

```python
def evaluator_doan_bua(expr, ctx):
    try: return _danh_gia_bieu_thuc_chuan_bi(expr, ctx)
    except ValueError: return ["ubuntu-latest"]
bang(ket_doan == ["ubuntu-latest"], "đột biến đoán bừa phải trả về mảng thay vì lỗi")
```

Cả hai khẳng định một hàm cục bộ trả đúng thứ nó vừa được viết để trả. **Không đầu vào nào làm chúng
đỏ.** Chúng cũng **không** đột biến hàm thật.

**Đo, không khẳng định.** Tôi bơm đột biến fail-open vào **hàm THẬT** — đúng hướng mà hai dòng trên
khai là đang canh — và xem ca nào đỏ, đỏ vì câu nào:

| đột biến bơm vào hàm thật | ca | rc | câu khẳng định đã giết nó |
|---|---|---|---|
| `_kiem_tra_nguon_duy_nhat_os_ci` luôn trả `[]` | `t161` **ĐỎ** | 1 | `"chốt không bắt được job lén khai os: []"` |
| `_danh_gia_bieu_thuc_chuan_bi` trả `["ubuntu-latest"]` thay vì `raise` | `t162` **ĐỎ** | 1 | `"PR nhãn windows phải chạy hai nền, nhận được: ['ubuntu-latest']"` |

Nền không đột biến: cả hai ca `1/1 đạt`, `rc=0`.

**Nên nói cho đúng mức, và tôi cố ý KHÔNG thổi lên P2:** hai ca **có răng thật**; chốt bảo vệ đến từ
**câu khẳng định hàng xóm**. Hai dòng "đột biến" đóng góp **0**. Đây là lỗi **LỜI KHAI** — thân PR
khai `A2` và `A4` được chống lưng bằng *"mutant check"*, mà phần mutant ấy không đo gì — chứ không
phải lỗ hổng. Rủi ro thật: ai đó sau này gỡ câu khẳng định hàng xóm vì tưởng đột biến đã phủ.

**Vá đề xuất:** hoặc bỏ hai dòng ấy và nói thẳng rằng chốt nằm ở câu khẳng định hàng xóm, hoặc biến
chúng thành đột biến THẬT (vá hàm thật trên bản sao rồi chạy lại ca đích, như bảng trên).

`A3` thì **KHÁC**: `expr_dot_bien_ref` dựng lại biểu thức cũ và ca cũng khẳng định trên biểu thức
**THẬT** đọc từ `ci.yml`, nên thêm lại `github.ref == 'refs/heads/master'` vào `ci.yml` sẽ làm
`r_push` thành hai nền và ca ĐỎ. **Đó là đột biến có răng**, ghi nhận đúng công.

---

## BẢNG ĐO — KỂ CẢ CÁI KHỚP

| phép đo | kết quả |
|---|---|
| `write_set` | **đúng 4 đường** như lease khai |
| tệp trong `khong_duoc_cham` bị chạm | **0** — quét cả 11 đường |
| `docs/PROTOCOL_DA_PHIEN.md` | **+1 / −0**, và đúng là **một hàng bảng §20.A** cho `ADR-0049` |
| `numstat` | **4 tệp, +235 / −24** ⇒ trong ngoại lệ đã cấp (4 tệp / ≤300 dòng) |
| `A1` `grep -c 'os: ${{ fromJSON'` | **1** |
| `adr-song` | **rc=0** |
| `doctrine-scan` | **rc=0** |
| `git diff --check` | **rc=0** |
| `actionlint` (có `shellcheck 0.9.0`) | **rc=0** ở CẢ HAI vế, cùng một finding `ops-don-ref.yml:117 SC1003:info` ⇒ **delta = 0** |
| `t161` · `t162` trên nền | `1/1 đạt` mỗi ca, `rc=0` |
| bộ chốt nguồn-duy-nhất | đo **THAM QUYỀN** (`"needs.chuan-bi.outputs.os" not in …`), **không** đo chính tả ⇒ `fromJSON`/`fromJson` đều qua |
| `gate (ubuntu)` trên PR #550 | chưa đo lượt này — head sẽ đổi sau merge base |

**Tôi rút một nghi ngờ của chính mình.** Lúc đầu tôi ngờ `A1` và bộ chốt đo **CHÍNH TẢ** thay vì
**THẨM QUYỀN** (bệnh *"distinguishes spelling, not authority"*). Đọc mã thì bộ chốt đo thẩm quyền —
nghi ngờ ấy **sai**, tôi rút. Còn lại một điểm nhỏ **không** nâng thành finding: `A1` là `grep` theo
chữ `fromJSON`, nó ra **1** chỉ vì ba consumer viết `fromJson` chữ thường; ai chuẩn hoá cách viết sẽ
làm `A1` **đỏ giả**. Bộ chốt `t161` mới là thứ có giá trị, `A1` chỉ là bản chiếu của nó.

---

## `KHÔNG ĐO ĐƯỢC` — khai, không lấp

1. **Hành vi thật của ma trận trên CI.** `t162` đo một **evaluator viết tay** mô phỏng biểu thức
   Actions, không đo GitHub chạy thật. Đó là lựa chọn đúng dưới `manual_ci_budget: 0`, nhưng phải khai:
   nếu evaluator hiểu biểu thức khác GitHub thì cả bảng bốn ca vẫn xanh trong khi CI làm việc khác.
   Bài học cùng họ đã có: *"YAML parse được KHÁC GitHub NHẬN"*.
2. **Mệnh đề 8 cổng của `deploy-package.*`** — xem `P2-b`.
3. **Head sau merge base** — chưa tồn tại lúc viết verdict này.

## NGUỒN CÓ THẨM QUYỀN

Tệp này trong kho, có băm. Bản đăng trên GitHub chỉ là **bản chiếu**.
