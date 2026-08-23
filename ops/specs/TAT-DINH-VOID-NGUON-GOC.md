# ĐẶC TẢ PACKET — `TAT-DINH-VOID-NGUON-GOC`, **revision 1**

```yaml
packet_id: TAT-DINH-VOID-NGUON-GOC
packet_issue: 276
revision: 1
generation: 1
ke_nhiem_cua: TAT-DINH-VOID-HA-TANG   # Issue #262, generation 1 -> blocked
review_class: sensitive
reviewer: codex
assurance_target: cross_approved
```

> **TỆP NÀY ĐÃ ĐÓNG BĂNG. ĐỪNG SỬA.** Lease neo vào `sha256` của nó, nên mỗi lần sửa là
> vô hiệu hoá mọi lease đang neo — im lặng, không cảnh báo. Cần đổi nội dung thì ra
> **revision MỚI** (tệp mới, băm mới), như r1→r2→r3 của `#262` đã làm.
>
> **`executor` và `base_sha` CỐ Ý không có ở đây** — chúng thuộc **LEASE**, không thuộc
> đặc tả. Bản nháp đầu để chúng là `null` kèm chú thích *"điền sau"*, tức mời đúng cái
> sửa vừa cấm ở trên. Cùng hình dạng lỗi với *"câu mô tả VỊ TRÍ phải đúng ở CẢ HAI phía"*:
> một trường trông như chỗ trống thì sẽ có người điền.

## 0. Packet này KHÔNG phải generation 3 của #262

`#262` gen 1 về `blocked` (attempt 3/3, 6 finding). Gen 2 là **Stable Slice** `r4` (PR #274) —
nó **BỎ** M3/M4 và giữ M1/M2/M8. Packet này nhận lại **đúng phần đã bỏ**, với một mục tiêu
KHÁC, Issue riêng và lease riêng. Bốn vòng review của gen 1 **không** kế thừa.

## 1. Vì sao ba bản trước thua — lý do CẤU TRÚC, không phải ba lần sơ ý

| bản | trường được TIN | ai đặt được |
|---|---|---|
| r1 | `stdout_byte: 0` + `rc≠0` | tiến trình **con** |
| r2 | `ma_thoat ∈ {12,13}` | tiến trình **con** |
| r3 | `trang_thai ∈ {qua_han, hong}` | launcher ghi, nhưng **executor ghi được tệp** |

Executor và launcher chạy **cùng principal, cùng hệ tệp**. Thứ gì launcher ghi được thì executor
ghi được ⇒ **không thuộc tính nào của NỘI DUNG tệp phân biệt được hai bên**. "Tìm một trường mà
bên bị đo không đặt được" là bài toán **vô nghiệm**; đổi trường lần thứ tư thua theo đúng cách ấy.

**Đo lại 23-08-2026 bởi phiên kế nhiệm** (ma trận phản chứng × phiên bản mã, có đo `sha256` từng
bản để chứng minh checkout thật sự đổi tệp):

```
                    ma r1(b27be0a)   ma r2(f5c37c0)   ma r3(2a332f3)
phan chung r1        rc=0  HOAN       rc=10 giu        rc=10 giu
phan chung r2        rc=0  HOAN       rc=0  HOAN       rc=10 giu
phan chung r3        rc=10 giu        rc=10 giu        rc=0  HOAN
```

Đường chéo: mỗi phản chứng giết **đúng mã của bản nó**. Bàn giao gen 1 chính xác.

## 2. `muc_tieu` — ĐỔI MỤC TIÊU, không đổi trường

Người giữ kho chốt 23-08-2026. Khai thẳng, và **phải in ra trong chính mã**:

> Cơ chế này chống **VÔ Ý** và chống **PHÁT LẠI**. Nó **KHÔNG** chống giả mạo có chủ đích, và
> **không thể**, chừng nào executor còn cùng principal với launcher.

Tiêu chí nghiệm thu đổi theo:

| | cũ (bất khả thi) | MỚI (kiểm được) |
|---|---|---|
| đòi | "executor không giả mạo được" | "**mọi** lần hoàn attempt hoặc **BUỘC-MÁY** hoặc **CÓ NGƯỜI DUYỆT GHI SỔ**" |

Tính an toàn nằm ở **cuốn sổ**, không ở tệp bằng chứng — r3 §6 đã viết sẵn nửa câu:
*"ai chịu ghi sổ thì không cần giả mạo"*.

| # | mục tiêu | tệp |
|---|---|---|
| **G1** | `begin-attempt` sinh `nonce` (`secrets.token_hex(16)`), ghi vào state kèm **số lượt**, xuất ra cho phía gọi | `packet_loop.py` |
| **G2** | `launcher run` ghi `nonce` **và** `chu_ky` (HMAC-SHA256) vào `run.json` | `launcher.py` |
| **G3** | `void-attempt` đòi: có `nonce` · khớp nonce của **LƯỢT ĐANG MỞ** · **chưa bị đốt** · `chu_ky` hợp lệ ⇒ rồi **ĐỐT** nonce | `packet_loop.py` |
| **G4** | **MỘT** hàm chuẩn hoá + ký, dùng chung cho **cả bên GHI lẫn bên KIỂM** | 1 chỗ, 2 nơi gọi |
| **G5** | Bản ghi cũ (không neo) ⇒ **CẮT CỨNG**, kèm **thông điệp riêng** (§5) | `packet_loop.py` |
| **G6** | Phép kiểm **nền + tuổi** của ảnh `doctor` dùng chung cho **mọi** người tiêu thụ | `packet_loop.py` |

### G2 — vì sao `launcher.py` BẮT BUỘC nằm trong write set

Chỉ **BÊN GHI** mới đặt được neo vào bản ghi. Mọi phương án né (buộc theo đường dẫn, inode,
`mtime`, chủ sở hữu) đều là thứ executor cũng đặt được ⇒ quay lại đúng bài toán vô nghiệm §1.

### Vì sao cần CẢ HAI (nonce và HMAC) — chúng chống hai lớp khác nhau

- **Nonce một mình KHÔNG đủ.** Cách tấn công dễ nhất và đời-thật nhất: lấy một `run.json` **THẬT**
  của chính lượt này (nonce đúng, chưa đốt) rồi sửa `"trang_thai":"xong"` → `"hong"`. Nonce vẫn
  khớp ⇒ vẫn qua. **HMAC** làm bản ghi thành một khối: giữ được neo thì không đổi được phán quyết.
- **HMAC một mình KHÔNG đủ.** Bản ghi cũ, ký hợp lệ, của lượt khác vẫn dùng lại được ⇒ cần **nonce**.

### G6 — không còn là packet riêng, vì r4 đã xoá người tiêu thụ thứ hai

Lỗ "đường `void` không dùng chung phép kiểm nền/tuổi" đo được trên `2a332f3` (`void` nhận ảnh
`Plan9` và ảnh 10 ngày tuổi, `rc=0` hoàn lượt; `begin-attempt` từ chối cả hai, `rc=10`). Trên r4
nó **moot** — `_kiem_bang_chung_ha_tang` đã bị gỡ nên chỉ còn **một** người tiêu thụ. Nhưng packet
này **dựng lại** người tiêu thụ thứ hai, nên phép kiểm dùng chung phải có **ngay từ đầu**, không
để thành nợ. Đó là lý do G6 nằm đây chứ không thành packet riêng.

## 3. `write_set` — 5 đường dẫn, RỘNG HƠN r3 (3) một cách có chủ đích

```
.claude/dev/launcher.py                    # G2: ghi nonce + chu_ky
.claude/dev/launcher_test.py               # phan chung cho ben GHI
.claude/dev/packet_loop.py                 # G1 G3 G5 G6
.claude/dev/packet_loop_test.py            # phan chung cho ben KIEM
ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md      # chuoi lenh canonical §7.4a phai co buoc nonce
```

**Hệ quả vận hành, phải biết TRƯỚC:** đụng `.claude/dev/**` ⇒ bắt buộc đo **Windows**. Gắn nhãn
`windows` **KHÔNG sinh lượt chạy nào** (`ci.yml` khai `pull_request:` không kèm `types:`) ⇒ phải
gọi tay `workflow_dispatch` trên đúng ref.

**Va chạm đã biết:** `#262` gen 2 (PR #274) đang giữ `packet_loop.py` + `packet_loop_test.py`.
Packet này **phải đi SAU** khi #274 land. Không cấp lease chồng lấn.

## 4. `ngan_sach_kich_thuoc`

Đề nghị **5 tệp / 420 dòng thêm**. Căn cứ: r3 dùng 320 cho 3 tệp; packet này thêm 2 tệp
(`launcher*.py`) và một cơ chế có hai đầu. **Vượt ⇒ nén, không nới** — r2 và r3 đều đã nới một lần
và đó là tiền lệ xấu.

## 5. Thông điệp — BA trạng thái, và bản ghi cũ phải nói ĐÚNG chỗ cần sửa

Hiện tại một `run.json` cũ rơi xuống nhánh ảnh `doctor` rồi nhận *"thiếu trường của `doctor --json`"*
— câu ấy **nói sai chỗ cần sửa**. Bắt buộc tách:

| ca | thông điệp riêng |
|---|---|
| bản ghi launcher, **không neo** | "không có neo lượt — dùng `--khong-co-bang-chung` (có ghi sổ)" |
| có nonce, **lệch lượt** | "neo thuộc lượt khác" |
| nonce **đã đốt** | "bản ghi này đã dùng để hoàn một lượt rồi" |
| **chữ ký sai** | "bản ghi đã bị sửa sau khi launcher ghi" |

Cắt cứng an toàn vì cửa `--khong-co-bang-chung` đã tồn tại ⇒ **không tạo ngõ cụt**. Ân hạn bị
loại: nó mở lại đúng lỗ đang vá trong suốt thời gian ân hạn.

## 6. `nghiem_thu` — mỗi ca MỘT đột biến; ca không có đột biến là ca sẽ âm thầm hở

| # | nghiệm thu | đột biến làm nó ĐỎ |
|---|---|---|
| **P1** | **BẤT BIẾN**: mọi lần `attempts_used` giảm đều để lại HOẶC bản ghi buộc-máy HOẶC mục `void_khong_co_bang_chung` có người duyệt | gỡ ghi sổ ở cửa thoát |
| **P2** | **phát lại**: cùng bản ghi hai lần ⇒ lần hai từ chối | bỏ bước **ĐỐT** nonce |
| **P3** | **lật phán quyết**: bản ghi THẬT của đúng lượt, sửa `trang_thai` ⇒ từ chối | bỏ kiểm HMAC |
| **P4** | **chéo lượt**: bản ghi của lượt 1 dùng ở lượt 2 ⇒ từ chối | bỏ kiểm khớp nonce |
| **P5** | bản ghi cũ không neo ⇒ từ chối, **đúng thông điệp** §5 | gộp về thông điệp `doctor` |
| **P6** | **chiều BẮT OAN**: bản ghi thật, ký đúng, đúng lượt ⇒ `rc=0`, hoàn được | siết bừa (từ chối mọi bản ghi) ⇒ **chỉ P6 đỏ**, P2–P4 vẫn xanh |
| **P7** | **cả hai** lý do `infrastructure` **và** `permission` đều được đo, và **một** bản ghi **KHÔNG** chứng minh được cả hai | bỏ phân biệt lý do ở nhánh sổ launcher |
| **P8** | ảnh `doctor` sai nền / quá tuổi bị từ chối ở **cả hai** người tiêu thụ | gỡ phép kiểm dùng chung khỏi **một** đường ⇒ ca của đường ấy đỏ |
| **P9** | mã **in ra** lời khai §2 (không chống giả mạo) | — chốt trung thực, không phải chốt kỹ thuật |

**P6 bắt buộc** — thiếu nó thì "siết tất" cũng xanh, và ta lại đo cái mình đã đặt.

**P7 có nguồn gốc là một phép đo, không phải suy luận.** Trên `2a332f3`: `--reason permission`
**chưa ca nào đi qua** (mọi `--reason` trong suite: `quota`×5, `infrastructure`×4, hai vòng động
`("quota","rate_limit")` và 4 lý do tự chế — **không có** `permission`). Đột biến **gỡ hẳn** nhánh
kiểm `permission` ⇒ suite **vẫn 235/235**. Đối chứng dương (nới lỏng `_doc_so_lauch`) ⇒ **234/235,
rc=1**, nên bộ đột biến có răng. Hệ quả đo được: **một** `run.json` `{"trang_thai":"hong"}` chứng
minh **cả hai** lý do (`infrastructure` rc=0 **và** `permission` rc=0), trong khi ảnh `doctor` thì
phân biệt đúng — vì `_kiem_bang_chung_ha_tang` `return` sớm ở nhánh sổ launcher, không xét lý do.
(Trên r4 lỗ này đã moot vì M3/M4 bị gỡ; P7 tồn tại để nó **không quay lại** khi dựng lại.)

## 7. `dieu_kien_dung`

- **Nếu bản vá lại chọn "tin thêm một TRƯỜNG" thay vì lập NGUỒN GỐC** ⇒ lần thứ **TƯ** của cùng
  hình dạng ⇒ **DỪNG** (`docs/PROTOCOL_DA_PHIEN.md` §12).
- **Không dựng được P3 thành ca ĐỎ** ⇒ HMAC chưa có răng ⇒ **DỪNG**, đừng khai là có.
- **Cần ghi ngoài write set** ⇒ DỪNG, xin revision.
- **Vượt ngân sách** ⇒ nén, không nới.
- Lease của `#262` **không** hồi sinh được; packet này đòi lease **mới**.

## 8. `chua_do_duoc` — khai thẳng

- **Giả mạo cùng-principal vẫn MỞ, CÓ CHỦ ĐÍCH.** Đây là giới hạn của mô hình, không phải nợ.
  Ranh giới tin cậy thật duy nhất trong tầm tay là **CI** (executor không ghi được log GitHub);
  phương án ấy bị loại vì nặng, cần mạng, và cắt mất ca chạy cục bộ. Nếu sau này thấy cần, đó là
  packet KHÁC, không phải bản vá của packet này.
- **HMAC với khoá nằm trong state là INTEGRITY, không phải AUTHENTICITY.** Nó chặn sửa-sau-khi-ghi,
  không chặn ký-lại. Đừng đặt tên hàm/biến gợi ý mạnh hơn thực tế.
- **Ngưỡng tươi vẫn là CHỌN, không phải ĐO**, và vẫn đo bằng `mtime` (sửa được).
- **`getattr` nuốt im lặng một lần đổi tên tham số** — nợ từ r1, chưa cái nào đóng.
- **`quota`/`rate_limit` vẫn nhận theo lời khai** — có chủ đích, chúng không để lại dấu vết máy.
