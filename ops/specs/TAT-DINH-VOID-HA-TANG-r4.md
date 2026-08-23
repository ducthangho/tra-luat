# ĐẶC TẢ PACKET — `TAT-DINH-VOID-HA-TANG`, **revision 4** (STABLE SLICE)

```yaml
packet_id: TAT-DINH-VOID-HA-TANG
packet_issue: 262
revision: 4
generation: 2                     # gen 1 da BLOCKED — §12 cam hoi sinh lease cu
thay_the: ops/specs/TAT-DINH-VOID-HA-TANG-r3.md   # r3, sha256 71559dca8ab65b977d8d0ec0de880e3d0f8cedb7e6f5a78855b34e0c87e81e48
review_class: sensitive
executor: claude
reviewer: codex
assurance_target: cross_approved
```

## 0. r4 là một STABLE SLICE — nó BỎ BỚT, không thêm gì

Generation 1 về `blocked`: attempt 3/3 cạn, và finding cuối là **lần thứ ba** của một hình dạng bị
cấm. Toàn bộ hồ sơ ở `ops/handoff/tat-dinh-void-ha-tang-exec-1-claude-20260823-handoff.md`
(`f6059636…`).

Nhưng packet có **hai phần độc lập**, và chỉ một phần hỏng:

| phần | 4 vòng review nói gì | r4 |
|---|---|---|
| **M1 · M2** — `begin-attempt` đòi ảnh `doctor` sạch/tươi/đúng nền | không finding nào bác | **GIỮ** |
| **M8** — luồng canonical chụp ảnh trước khi gọi | không finding nào bác | **GIỮ** |
| **M3 · M4** — `void-attempt` đòi bằng chứng từ `run.json` | ba lần lặp hình dạng, vẫn hở | **BỎ** |

### Vì sao BỎ M3/M4 KHÔNG mở lỗ mới — đo, không suy

```
git show origin/master:.claude/dev/packet_loop.py | sed -n '/def cmd_void_attempt/,/_save/p' \
  | grep -c "bang_chung\|evidence"
=> 0
```

`cmd_void_attempt` trên `master` **hôm nay** chỉ kiểm allowlist của `LY_DO_VOID`; nó **chưa từng**
đòi bằng chứng. Nên bỏ M3/M4 đưa trục ấy về **đúng hiện trạng**, không lùi thêm một bước nào.

Còn M1/M2 là bảo vệ **mới thật**: một lượt chết vì máy thiếu công cụ không còn bị đếm như thất bại
nội dung. **Slice này nghiêm ngặt tốt hơn `master` hôm nay.**

### Vì sao KHÔNG giữ M3 với nhãn "chốt chưa đủ, có khai"

Đó là lựa chọn tệ nhất trong ba. Một cổng hoàn attempt cho một tệp **bất kỳ ai viết** mà lại mang
tên "bằng chứng máy" thì **trông như** bảo vệ — và người vận hành sẽ dựa vào nó. Cùng họ bài học
*"cổng không nói dối, nó VẮNG MẶT"*: một cổng vắng mặt còn đọc được là vắng; một cổng có mặt mà
rỗng thì đọc thành có.

### Năm điều kiện Stable Slice của §12 — đối chiếu từng cái

| điều kiện §12 | slice này |
|---|---|
| hữu ích độc lập | M1/M2 chặn attempt bị đốt oan, không cần M3 |
| đạt acceptance riêng | N1 · N2 · N3 · N7 · N10′ đều thuộc M1/M2/M8 |
| không phụ thuộc phần đang có finding | cả 6 finding đều nằm ở M3/M4 hoặc ở đặc tả của nó |
| không làm yếu security/gate | đo được ở trên: trục void về đúng hiện trạng master |
| có test/evidence dương của chính nó | suite N/N + đột biến giết đúng ca (§3) |

## 1. `write_set` — 3 đường dẫn

```
.claude/dev/packet_loop.py
.claude/dev/packet_loop_test.py
ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md
```

**Hiện vật hồ sơ đi kèm nhưng KHÔNG thuộc write set** (là bản ghi, không phải thi công):
`ops/handoff/tat-dinh-void-ha-tang-exec-1-claude-20260823-handoff.md` · `ops/specs/…-r2.md` ·
`…-r3.md` · chính tệp này. Chúng không tính vào ngân sách dòng, đúng như cách r2/r3 đã được xử.

## 2. `ngan_sach_kich_thuoc`

| | |
|---|---|
| tệp tối đa | **3** |
| dòng thêm tối đa | **220** |

Thấp hơn r3 (320) vì slice **bỏ bớt**. Nếu vượt ⇒ **DỪNG và nén**, không nới: gen 1 đã nới hai lần.

## 3. `muc_tieu` — giữ nguyên văn r3 cho M1/M2/M5/M6/M8; BỎ M3/M4

| # | mục tiêu | tệp |
|---|---|---|
| **M1** | `begin-attempt` đòi ảnh `doctor --json` cho ĐÚNG nền, `thieu_bat_buoc` rỗng. Thiếu/không đọc được ⇒ **từ chối mở lượt** (mã `10`), không mở rồi tính | `packet_loop.py` |
| **M2** | Bằng chứng phải **TƯƠI**: ảnh cũ hơn ngưỡng, hoặc chụp trên `he_dieu_hanh` khác ⇒ từ chối | `packet_loop.py` |
| **M5** | **BA trạng thái**: `co` · `khong` · **`khong_doc_duoc`**; cái thứ ba không gộp vào `khong` | `packet_loop.py` |
| **M6** | Phản chứng cho từng luật + đột biến giết đúng ca của nó | `packet_loop_test.py` |
| **M8** | Chuỗi canonical `§7.4a` chụp ảnh rồi truyền vào `begin-attempt` | `KE_HOACH_…md` |
| ~~M3~~ ~~M4~~ | **BỎ** — chuyển sang packet kế nhiệm (§5) | — |

## 4. `nghiem_thu`

| # | nghiệm thu | phép đo làm nó ĐỎ |
|---|---|---|
| **N1** | `thieu_bat_buoc` khác rỗng ⇒ từ chối, `attempts_used` **không** tăng | đột biến bỏ chốt ⇒ ĐỎ |
| **N2** | ảnh SẠCH ⇒ **mở được** lượt — chiều **BẮT OAN** | giết bằng đột biến **siết thêm**, và nó phải KHÔNG làm N1 đỏ |
| **N3** | ảnh chụp trên nền khác ⇒ từ chối | đột biến bỏ so nền ⇒ ĐỎ |
| **N7** | ảnh hỏng cú pháp ⇒ `khong_doc_duoc`, **không** rơi về `khong` im lặng | đột biến gộp hai trạng thái ⇒ ĐỎ |
| **N10′** | khối `§7.4a` **CHẠY được** (qua `pwsh`); nền không phải `nt` thì **BỎ QUA CÓ IN LÝ DO** | đột biến làm hỏng lệnh **trong tài liệu** ⇒ ĐỎ |
| **N11** | `void-attempt` giữ **đúng hành vi master**: `--reason` trong allowlist ⇒ `rc=0`, không đòi bằng chứng | đột biến thêm lại đòi hỏi bằng chứng ⇒ ĐỎ. **Ca này canh việc BỎ đã sạch** — thiếu nó thì không ai biết M3 còn sót mảnh nào |
| **N12** | delta so master = 0 cho `lease_publish_test.py`; nền master đo **TRONG worktree của chính kho** | chép ra thư mục rỗng ⇒ ĐỎ GIẢ, đã trả giá 4 lần |

## 5. `hinh_dang_ke_thua` — M3/M4 đi đâu

Packet kế nhiệm, **Issue và lease riêng**, không phải generation của packet này. Nội dung đã có sẵn
trong handoff §5: xác thực **nguồn gốc launcher** + ràng buộc lượt chạy hiện tại, khoá bằng một con
lỗi nội dung THẬT tự viết bản ghi giả và phải nhận `rc=10`; cộng gom phép kiểm nền/tuổi cho **cả
hai** người tiêu thụ ảnh `doctor`.

**Cảnh báo cho packet ấy:** ba bản trước đều đổi TRƯỜNG được tin mà không lập NGUỒN GỐC. Chọn "tin
một trường khác" là lần thứ **TƯ** — `docs/PROTOCOL_DA_PHIEN.md` §12 cấm.

## 6. `dieu_kien_dung`

- Vượt **220** dòng hoặc **3** tệp ⇒ DỪNG và nén. Gen 1 đã nới hai lần; gen 2 không nới.
- Thấy mình định **thêm lại** một mảnh của M3/M4 ⇒ DỪNG: slice này định nghĩa bằng thứ nó BỎ.
- Trần vòng review về **2** theo canon `ADR-0043` — gen 2 bắt đầu lại, không kế thừa 4 vòng của gen 1.

## 7. `chua_do_duoc`

- **Bốn chỗ mỏng của r1 vẫn còn**, và r4 **không** đóng cái nào: ngưỡng tươi 3600s đo bằng `mtime`
  (sửa được, con số là CHỌN không phải ĐO) · `getattr` nuốt im lặng một lần đổi tên tham số ·
  `--can-cu` chỉ kiểm không rỗng — **hai cái sau nay VÔ NGHĨA** vì chúng thuộc M4 đã bỏ, giữ trong
  danh sách để packet kế nhiệm không tưởng là đã đóng.
- **N10′ chỉ đo THẬT trên `windows-latest`.** Trên `ubuntu-latest` nó bỏ qua có in lý do. Ca có mặt
  ở cả hai nền, chỉ đo ở một — nói thẳng thay vì để nó xanh im lặng.
- **Không đo được còn tiêu chí nào của M1/M2 cùng bệnh với M3.** M3 lộ ra vì có người chạy đúng ca
  của nó; M1/M2 qua 4 vòng không ai bác, nhưng *"không ai bác"* không phải *"đã đo"*.
