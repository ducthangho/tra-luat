# BẢN CHIẾU — thân Issue #119 (wp119 revision 1)

> **Tệp này KHÔNG phải nguồn sự thật.** Nó là văn bản soạn sẵn để dán vào thân #119.
> Nguồn sự thật là `ops/specs/wp119-r1-spec.md`, neo bằng băm. Nếu tệp này và spec lệch
> nhau thì **spec thắng** — và tệp này sai, phải sửa lại theo spec.
>
> Soạn bởi phiên executor wp55 `wp55-r3-exec-4-claude-20260814`. Phiên không đăng được:
> `PATCH /repos/…/issues/119` trả **HTTP 403**, và không workflow nào trong kho ghi được
> THÂN issue (`ops-publish-lease.yml` chỉ `POST …/issues/N/comments`). Cần chủ kho dán.

---

## ⬇ TỪ ĐÂY TRỞ XUỐNG LÀ NỘI DUNG CẦN DÁN VÀO THÂN #119 ⬇

---

**Đây là bản CHIẾU. Nguồn sự thật nằm trong kho, không nằm ở thân Issue này.**

```
spec_path   : ops/specs/wp119-r1-spec.md
spec_branch : ops/successor-packet-session-mutex
spec_hash   : 1740b1c5c0b999c48c24b4aead29a6bc9b97c58eb483d42dd0a03714c9ce0a97
spec_bytes  : 22460
```

Kiểm mỏ neo — chạy được ở mọi nền, không cần mạng, không cần token:

```bash
git fetch origin ops/successor-packet-session-mutex
git show origin/ops/successor-packet-session-mutex:ops/specs/wp119-r1-spec.md | sha256sum
#   ĐÒI 1740b1c5c0b999c48c24b4aead29a6bc9b97c58eb483d42dd0a03714c9ce0a97
```

Lệch một byte thì **dừng và hỏi**, đừng đoán. Mọi lease, verdict và evidence §7 của packet
này phải neo đúng con băm đó.

> **Vì sao thân Issue chỉ là bản chiếu, không phải bản đầy đủ.** wp55 revision 3 đã phải
> đổi cơ sở băm từ "băm thân Issue" sang "băm tệp trong kho" vì hai lý do đo được: thân
> Issue **không đọc được** từ phiên agent (`api.github.com` trả 403), và lớp mã hoá trên
> đường đăng **làm biến dạng ký tự** — thân #55 hiện còn `&#34;` nguyên văn ở đúng những
> chỗ đáng ra là dấu nháy kép. Dán 22 KB tiếng Việt qua đúng đường đã biết là hỏng thì chỉ
> đổi một lỗi đã biết lấy một lỗi chưa đo. Nên bản chiếu này cố ý NGẮN và trỏ về tệp.

## Packet

| | |
|---|---|
| packet | **wp119** · revision 1 · `successor_key: packet-session-mutex` |
| mission | #54 |
| executor | `codex` |
| reviewer | `claude` (§8 — khác provider với executor) |
| environment | local · risk normal · `attempts_limit: 3` |
| **depends_on** | **`[wp55]` — CHẶN CỨNG, xem dưới** |

`write_set` (3 tệp, exact):

```
.claude/dev/packet_loop.py
.claude/dev/packet_loop_test.py
docs/PROTOCOL_DA_PHIEN.md
```

## Mục tiêu

Biến *"một packet, một phiên đang chạy"* từ QUY ƯỚC thành điều **CƯỠNG CHẾ ĐƯỢC**. Hiện
hai phiên cùng mở lượt trên một packet là trạng thái mà máy **không phân biệt được** với
một phiên — và tệ hơn: hai lượt song song chỉ tiêu một đơn vị trần, nên trần attempt bị
bào mòn.

## Vì sao có packet này — va chạm THẬT, không phải giả định

Ngày 2026-08-15, hai phiên cùng chạy wp55, cập nhật cách nhau **14 giây**. Cả hai cùng
nhắm việc ghi ra GitHub. Nếu phiên executor đã đẩy bản nháp lease của nó lên `ops/**` như
dự định ban đầu thì wp55 lúc này có **hai lease reviewer cùng hiệu lực** cho cùng một lượt,
neo cùng một head, hai `lease_id` khác nhau — vì chốt idempotent chỉ chặn đăng lại *cùng
một tệp*, không chặn *hai tệp khác nhau*.

Thứ ngăn được điều đó **không phải cơ chế**, mà là một phiên tự dừng ở ranh giới. Cơ chế
vẫn thủng y nguyên.

## Ba hình dạng của lỗ — ĐÃ ĐO

Probe chạy được: `ops/evidence/probe-packet-session-mutex.py`,
`ops/evidence/probe-packet-session-mutex-race.py` (cùng nhánh spec).

**H1 · đua khi cùng state-dir** — có thật nhưng HIẾM và phụ thuộc tải:

```
N=8  đồng thời, 12 vòng → 12/12: thắng=1                    (KHÔNG lộ lỗ lần nào)
N=32 đồng thời, 15 vòng → 13/15: thắng=1
                            2/15: thắng=2, attempts_used=1   ← LỖ
```

Chữ ký `thắng=2, đếm=1` chỉ khớp một cơ chế: **lost update**. `_load` → kiểm → `_save`
không nguyên tử. Hệ quả nặng không phải "hai lượt song song" mà là **đếm thiếu** ⇒ trần
attempt bị bào mòn.

**H2 · khác container** — không phải đua mà là *vắng mặt hoàn toàn* cơ chế loại trừ. Hai
phiên cùng `running`, mỗi bên tin mình duy nhất. `.claude/.packet_state` không nằm trong
kho nên không có nguồn chung nào để hỏi.

**H3 · lease không có định danh phiên** — khoá chỉ gồm `evidence, expires_utc, granted_by,
lease_id`. Không có gì để hỏi "ai đang giữ", nên không có gì để từ chối.

## Hướng chữa đã cân nhắc (không bắt buộc, xem mục 3.1 của spec)

`git` chính là primitive compare-and-set sẵn có: mọi phiên agent bị 403 ở API nhưng
`git push` luôn chạy, và `--force-with-lease` từ chối khi ref đã dịch.

| lớp | đóng |
|---|---|
| `holder_token` do phiên tự đúc, ghi vào state bền | H3 |
| state bền trên nhánh `ops/state/**` | H2 |
| ghi bằng CAS (`--force-with-lease`) | H1 |
| **số rào (fencing) tăng đơn điệu** | lỗ mà HẠN không đóng được |

Khuyến nghị **không** neo vào `session_id` do nền cung cấp: phiên cloud có `session_01…`,
CLI cục bộ và desktop không có, Actions có thứ khác — neo vào cái nào cũng đóng nền này hở
nền kia rồi phải khai nửa vời.

Số rào đóng đúng cái lỗ mà hạn bỏ sót: holder treo → lease hết hạn → bên khác takeover →
holder cũ tỉnh dậy **ghi muộn**. Hạn không chặn được cú ghi đó.

**Giới hạn, nói thẳng:** cơ chế này định danh **runtime đang giữ khoá**, KHÔNG định danh
con người. Nó chặn va chạm VÔ Ý — đúng thứ đã xảy ra — không chặn một bên cố ý có quyền
ghi kho.

## Acceptance criteria

**12 AC**, đầy đủ trong spec. Bốn cái định hình packet:

- **AC 1** — kế thừa AC 18 của wp55: xuất **DANH SÁCH ĐÓNG** các hình dạng tranh chấp kèm
  phép thử đo được **TRƯỚC** khi sửa mã. Vá một hình dạng mà không có danh sách là KHÔNG ĐẠT.
- **AC 2** — H1 đóng, và ca đua **không được xanh nhờ may**: lặp tới khi quan sát được, hoặc
  điểm dừng tất định. *Ở N=8 lỗ không lộ trong 12 vòng liên tiếp* — một ca chạy một lần rồi
  kết luận sẽ xanh giả, và xanh giả tệ hơn không có ca.
- **AC 6** — số rào: holder treo, hết hạn, bị takeover, tỉnh dậy ghi muộn ⇒ cú ghi phải bị
  TỪ CHỐI. Đột biến bỏ so fence (chỉ giữ kiểm hạn) phải làm ca này ĐỎ.
- **AC 7** — chiều BẮT OAN ngang hàng: phiên nối lại KHÔNG bị chặn; `takeover` chạy được để
  một holder chết không khoá cứng packet. Siết tới mức kẹt cứng là KHÔNG ĐẠT, y như để lọt.

Kèm **AC 12**: `file_count` của `RELEASE_MANIFEST.json` KHÔNG đổi (hiện 179). Đã đo 0/179
tệp thuộc `ops/`, nên `ops/state/**` nằm ngoài gói — chốt này bắt đúng lúc ai đó định đưa
state vào cây làm việc thay vì nhánh riêng.

## ⛔ CHƯA ĐƯỢC LEASE — điều kiện khởi động chưa đủ

| # | việc | trạng thái |
|---|---|---|
| 1 | Mở issue #119 | ✅ xong 2026-08-15 |
| 2 | **wp55 land** | ⛔ **CHẶN CỨNG** |
| 3 | Kiểm ruleset cho `ops/state/**` | ⛔ chưa đo được (cần API) |
| 4 | Cấp lease executor cho `codex` neo `1740b1c5…` | ⛔ chờ #2 |

**Việc 2 là điều kiện VẬT LÝ, không phải thận trọng.** Hai tệp `.claude/dev/packet_loop*.py`
mà packet này phải sửa **chưa tồn tại trên `master`** — chúng do wp55 TẠO RA:

```bash
git show origin/master:.claude/dev/packet_loop.py
# fatal: path '.claude/dev/packet_loop.py' ... not in 'origin/master'
```

wp55 đang ở PR #115, head `e6e4b73`, review lượt 6 đang chạy. Cấp lease cho wp119 trước khi
wp55 land là cấp một lease **không có gì để sửa**.

**Thứ tự đúng:** wp55 land → đo lại trên master mới → cấp lease cho `codex` → mở nhánh
`codex/wp119-r1g1-…`.
