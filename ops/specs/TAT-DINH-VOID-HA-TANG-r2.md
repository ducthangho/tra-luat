# ĐẶC TẢ PACKET — `TAT-DINH-VOID-HA-TANG`, **revision 2**

```yaml
packet_id: TAT-DINH-VOID-HA-TANG
packet_issue: 262
revision: 2
generation: 1
thay_the: ops/specs/TAT-DINH-VOID-HA-TANG.md   # r1, sha256 9e1d049bc3eb6904adb0ea79d1b9ce6b94182521297be28f93a6360995a95de2
review_class: sensitive
executor: claude
reviewer: codex
assurance_target: cross_approved
base_sha: 05de1ab81c235235b971a6fb8d8ae1fb226295d5
```

> Bản sửa đổi này **không cấp việc**. Lease `tat-dinh-void-ha-tang-exec-1-claude-20260823` neo vào
> băm của **r1**; muốn thi công theo r2 thì lease phải được sửa hoặc cấp lại (§5).

## 0. Delta so `revision 1` — MỘT tiêu chí bị LẬT, và nó là tiêu chí của chính tôi

`r1` viết M3 như sau (nguyên văn, dòng 135):

> *"…mã thoát `12`/`13` của launcher, hoặc `trang_thai` + `ma_thoat` trong `run.json`, **hoặc
> `stdout_byte: 0` kèm rc≠0**"*

**Mệnh đề thứ ba SAI, và nó sai theo đúng cách mà cả packet sinh ra để chặn.** Nó suy từ **HÌNH
DẠNG đầu ra** — *"thoát khác 0 mà không in gì = chết trước khi chạy tới phần việc"* — nhưng hình
dạng ấy **không phân biệt được** lỗi hạ tầng với lỗi nội dung. Đo được trên `b27be0a`:

```
run.json = {"trang_thai":"xong","ma_thoat":1,"stdout_byte":0}      <- `sys.exit(1)` im lang
void-attempt --reason infrastructure   ->  rc=0,  attempts_used 1 -> 0
```

Một lượt hỏng vì **mã sai** được hoàn như lỗi hạ tầng. Tức chính tiêu chí nghiệm thu ấy **mở lại
cửa lách mà M3 tồn tại để đóng**.

**r1 suy từ Ý ĐỊNH, r2 suy từ PHÉP CHẠY** — và hai bên ra hai luật ngược nhau. Đây là cùng hình
dạng lỗi mà `CLAUDE.md` gọi tên: *"allowlist canh TỪ VỰNG, không canh SỰ THẬT"*, chỉ khác là lần
này nạn nhân là **tiêu chí nghiệm thu**, không phải mã.

### Vì sao phải là bản sửa đổi, không phải một quyết định lúc thi công

Cross-review vòng 1 (codex, P1) đòi bỏ mệnh đề ấy — **đúng về an ninh**, tái hiện được. Cross-review
vòng 2 (codex, P1) chỉ ra rằng bỏ nó làm mã **lệch hợp đồng đóng băng** — **cũng đúng**. Hai vòng
không mâu thuẫn nhau: chúng cùng chỉ vào một chỗ, là **M3 của r1 sai**.

Giữ mã theo r1 ⇒ để nguyên một lỗ đã đo được. Sửa mã mà không sửa đặc tả ⇒ *"treating the
implementation-only decision as an implicit spec change"*. Cả hai đều không nhận được. Đường duy
nhất là lật tiêu chí, và lật thì phải qua bản sửa đổi — chính r1 khai luật đó ở đầu tệp.

### Thứ hai cùng lật: packet LÀM HỎNG một luồng đã tài liệu hoá

M1 của r1 làm `begin-attempt` đòi ảnh môi trường. Đo được hệ quả mà r1 **không lường**:

```
ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md:413   begin-attempt --packet <issue> --provider <...>
rg "TL_MOI_TRUONG_JSON"  (ngoai hai tep write set)   ->  KHONG CO
```

Chuỗi lệnh **canonical** của kho gọi `begin-attempt` không kèm ảnh, và **không chỗ nào** trong kho
tạo biến ấy. Nên sau khi land r1, ai làm đúng theo tài liệu ăn `rc=10` ở **mọi** lượt; trước đó
`rc=0`. `r1` khai `ngoai_pham_vi` toàn những thứ nó *không muốn đụng*, nhưng **không hỏi thứ nào
GỌI cái nó sửa** — và đó là chỗ hổng của chính bản đặc tả.

Cùng họ bài học *"guard không nối vào đường chạy tự động thì guard chỉ là tài liệu"*, lật ngược:
**một guard nối vào đường chạy mà không sửa người GỌI thì nó chặn đúng người dùng hợp lệ.**

## 1. `write_set` — 3 đường dẫn (r1 có 2)

```
.claude/dev/packet_loop.py
.claude/dev/packet_loop_test.py
ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md     <- THEM o r2
```

Đường thứ ba là **hệ quả trực tiếp** của M1, không phải việc gộp thêm: land M1 mà để nguyên luồng
canonical là cố ý để lại một lệnh không chạy được. `ADR-0044` cho `sensitive` trần **3 tệp** — đúng
mức, không vượt.

## 2. `ngan_sach_kich_thuoc` — PHẢI ĐƯỢC NGƯỜI GIỮ KHO XÁC NHẬN

| | r1 | r2 đề nghị |
|---|---|---|
| tệp tối đa | 2 | **3** |
| dòng thêm tối đa | 300 | **320** |

Hiện đã dùng **300/300** trên hai tệp đầu, tức **0 dòng dư**. Bản vá M8 (§3) ước **12–18 dòng**.
Con số 320 là **ước lượng, không phải phép đo** — r1 từng khai *"~10–12 dòng"* cho một việc tốn
**25**, nên đừng tin con số này hơn mức nó đáng.

**Lease neo `ngan_sach_kich_thuoc` chứ không phải đặc tả**, nên riêng mục này không tự có hiệu lực:
người giữ kho phải sửa lease hoặc cấp lại. Đặc tả chỉ nêu nhu cầu.

## 3. `muc_tieu` — chỉ ghi cái ĐỔI so với r1

M1 · M2 · M4 · M5 · M6 giữ **nguyên văn r1**.

| # | mục tiêu | tệp |
|---|---|---|
| **M3′** | `void-attempt --reason infrastructure\|permission` đòi bằng chứng máy: mã thoát **`12`/`13`** của launcher, **hoặc** `trang_thai` ∈ {`qua_han`, `hong`} trong `run.json`. **BỎ** mệnh đề *"`stdout_byte: 0` kèm rc≠0"* — nó nhận cả lỗi nội dung. `quota`/`rate_limit` giữ đường cũ | `packet_loop.py` |
| **M8** | Chuỗi lệnh canonical §7.4a phải **chụp ảnh `doctor --json` rồi truyền vào** `begin-attempt`. Ai làm đúng tài liệu phải `rc=0`, không phải `rc=10` | `KE_HOACH_THI_CONG_CLAUDE_CODEX.md` |

## 4. `nghiem_thu` — chỉ ghi cái ĐỔI

| # | nghiệm thu | phép đo làm nó ĐỎ |
|---|---|---|
| **N4c′** | `run.json` `{"trang_thai":"xong","ma_thoat":1,"stdout_byte":0}` ⇒ **`rc=10`**, `attempts_used` **KHÔNG** giảm. Cùng ca, `ma_thoat: 12` ⇒ `rc=0` | đột biến **khôi phục** mệnh đề đã bỏ ⇒ ca ĐỎ, và **chỉ** ca ấy. Đo trên `00ae668`: giết đúng `void_ha_tang_nhan_so_launcher` |
| **N10** | Chuỗi lệnh trong §7.4a chạy được **nguyên văn** trên nền sạch: `rc=0` | chạy đúng khối lệnh đã sửa; bỏ bước chụp ảnh ⇒ `rc=10` ⇒ ĐỎ. **Không** được đo bằng cách đọc tài liệu |

## 5. `dieu_kien_dung` — thêm so với r1

- **Trần vòng review đã CẠN.** Canon `ADR-0043` là **2**; cả hai đã dùng trên PR #266 và
  `assurance_target: cross_approved` **chưa đạt**. Thi công theo r2 cần khối `nang_tran` của người
  có thẩm quyền, **hoặc** người giữ kho chấp nhận land với finding đã ghi nhận.
- **Lease hiện neo băm của r1.** Chưa sửa lease thì `spec_sha256_required` lệch, và mọi lượt thi
  công theo r2 là thi công ngoài lease.

## 6. `chua_do_duoc`

- **Con số 320 chưa có phép đo.** Xem §2.
- **N10 đo được luồng CHẠY, không đo được luồng ĐÚNG.** Nó chứng minh chuỗi lệnh không còn `rc=10`;
  nó không chứng minh chuỗi ấy là thứ người vận hành nên làm.
- **r2 KHÔNG đóng bốn chỗ mỏng r1 đã khai** và cross-review hai vòng cũng không nêu: ngưỡng tươi
  3600s đo bằng `mtime` (sửa được, và con số là chọn chứ không đo) · `getattr` nuốt im lặng một lần
  đổi tên tham số · `--can-cu` chỉ kiểm không rỗng · `quota`/`rate_limit` vẫn nhận theo lời khai nên
  ai muốn lách chỉ cần đổi chữ. Ghi lại để chúng không biến mất khỏi hồ sơ chỉ vì hai vòng review đã
  nói chuyện khác.
- **Không đo được còn tiêu chí nào của r1 sai như M3.** M3 lộ ra vì có người chạy đúng ca của nó.
  Các tiêu chí còn lại chưa ai thử phá theo cách ấy — và bài học của packet này là **chín đột biến
  vẫn xanh trong khi hai đường khai trong đặc tả chưa từng chạy**.
