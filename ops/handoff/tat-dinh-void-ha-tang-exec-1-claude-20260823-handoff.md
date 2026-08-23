# HANDOFF — `TAT-DINH-VOID-HA-TANG` (#262), Executor lượt 1–3 (`claude`)

- Provider `claude`; model `opus`; effort `max`; surface Claude Code remote; role Executor.
- Lease `tat-dinh-void-ha-tang-exec-1-claude-20260823`, sửa **hai lần** (neo lại r2 rồi r3, nới ngân
  sách một lần, nới trần vòng review hai lần). Cả ba lần đều có dấu vết trên Issue #262.
- **Kết quả: `blocked`.** Attempt **3/3** cạn, và finding cuối là **lần thứ BA của một hình dạng
  lỗi bị cấm** — `dieu_kien_dung` của r3 §5 và `docs/PROTOCOL_DA_PHIEN.md` §12 đều bảo DỪNG.
- **PR #266 KHÔNG ĐƯỢC MERGE NGUYÊN TRẠNG.** Mã hiện tại vẫn hoàn attempt cho một tệp bằng chứng
  do chính executor viết. Xem §5.
- 4 vòng review, **6 finding, cả 6 đều THẬT** và đều được tái hiện độc lập trước khi vá.

---

## 0. Handoff MÁY ĐỌC ĐƯỢC — `docs/PROTOCOL_DA_PHIEN.md` §7

```yaml
schema_version: 1
packet_id: TAT-DINH-VOID-HA-TANG        # Issue #262
generation: 1
spec_hash: 71559dca8ab65b977d8d0ec0de880e3d0f8cedb7e6f5a78855b34e0c87e81e48   # r3
provider: claude
role: executor
session_id: session_01CX1JhRkNDDuNirBzms5zUr
base_sha: 05de1ab81c235235b971a6fb8d8ae1fb226295d5
head_sha: 2a332f37e7d91c7f9ec33d2702ee2725516c8a8c
status: blocked
summary: >-
  Đóng được hai lỗ thật và lật một tiêu chí nghiệm thu sai của chính packet, nhưng vế
  "run.json làm bằng chứng hạ tầng" KHÔNG đứng vững: ba bản liên tiếp đều tin một trường
  mà bên bị đo đặt được. Attempt cạn ở đúng lúc hình dạng ấy lặp lần thứ ba.
changed_paths:
  - .claude/dev/packet_loop.py
  - .claude/dev/packet_loop_test.py
  - ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md
tests:
  - name: packet_loop_test.py
    status: passed        # 235/235 đạt; nền master 225/225 ⇒ 10 ca mới, 0 hồi quy
    evidence: 'https://github.com/ducthangho/tra-luat/actions/runs/32615731264'
  - name: gate (ubuntu-latest)
    status: passed
    evidence: 'https://github.com/ducthangho/tra-luat/actions/runs/32615731264/job/97136024457'
  - name: gate (windows-latest)
    status: passed
    evidence: 'https://github.com/ducthangho/tra-luat/actions/runs/32615731264/job/97136024283'
  - name: 'đột biến (11 phép thay, xem §4)'
    status: passed        # không đột biến nào sống sót
    evidence: 'ops/handoff/tat-dinh-void-ha-tang-exec-1-claude-20260823-handoff.md#4'
test_selection:
  gate_tier: null         # lease/spec không khai tier — để null thay vì bịa
  selector_policy_sha: null
  tested_sha: 2a332f37e7d91c7f9ec33d2702ee2725516c8a8c
  selected_groups: []
  full_fallback_reason: 'chạy toàn bộ gate, không chọn lọc'
remaining_work:
  - 'M3 vẫn HỞ: bằng chứng từ `run.json` chưa có xác thực NGUỒN GỐC launcher + ràng buộc
     lượt chạy hiện tại. Tệp `{"trang_thai":"hong"}` do executor tự viết vẫn hoàn được attempt.'
  - 'Đường `void` KHÔNG dùng chung phép kiểm nền/tuổi với `begin-attempt`: ảnh doctor 10 ngày
     tuổi, nền `Plan9`, vẫn được nhận ở đường void trong khi begin-attempt từ chối.'
  - 'Bốn chỗ mỏng của r1 chưa cái nào đóng qua 4 vòng: ngưỡng tươi 3600s đo bằng `mtime` ·
     `getattr` nuốt im lặng một lần đổi tên · `--can-cu` chỉ kiểm không rỗng ·
     `quota`/`rate_limit` nhận theo lời khai.'
  - 'N10′ chỉ đo THẬT trên `windows-latest`; trên `ubuntu-latest` nó bỏ qua có in lý do.'
next_role: human
manual_next_action: >-
  Người giữ kho quyết ba việc: (1) KHÔNG merge #266 nguyên trạng — chọn revert phần M3
  hoặc giữ nó như một chốt-chưa-đủ có khai; (2) mở packet kế nhiệm cho xác thực nguồn gốc
  (§5 có gợi ý vá đã được reviewer thử); (3) reroute bằng generation mới — lease này KHÔNG
  được hồi sinh (§12).
copyable_prompt: |
  Bạn là phiên KẾ NHIỆM của packet TAT-DINH-VOID-HA-TANG (#262), kho ducthangho/tra-luat.
  Mission/packet: TAT-DINH-VOID-HA-TANG · revision 3 · generation 1
  spec_hash: 71559dca8ab65b977d8d0ec0de880e3d0f8cedb7e6f5a78855b34e0c87e81e48
  head đã dừng: 2a332f37e7d91c7f9ec33d2702ee2725516c8a8c (PR #266, KHÔNG merge nguyên trạng)

  ĐỌC TRƯỚC: ops/handoff/tat-dinh-void-ha-tang-exec-1-claude-20260823-handoff.md
  rồi ops/specs/TAT-DINH-VOID-HA-TANG-r3.md (kiểm băm trước khi đọc nội dung).

  VAI TRÒ: executor cho packet KẾ NHIỆM — KHÔNG hồi sinh lease cũ (§12), cần Issue + lease mới.

  ĐIỀU PHẢI BIẾT TRƯỚC KHI VIẾT DÒNG NÀO:
  Ba bản liên tiếp (r1/r2/r3) đều tin một trường mà BÊN BỊ ĐO đặt được — xem §3 của handoff.
  Nếu bản vá của bạn lại chọn "tin một trường khác" thì đó là lần thứ TƯ; §12 cấm.
  Thứ còn thiếu là NGUỒN GỐC: chứng minh launcher tạo ra bản ghi, và bản ghi thuộc ĐÚNG
  lượt chạy hiện tại. Không có nó thì mọi trường trong run.json đều là lời khai.

  STOP CONDITIONS: chưa có Issue + lease ⇒ dừng · định tin thêm một trường thay vì lập
  nguồn gốc ⇒ dừng · cần ghi ngoài write set ⇒ dừng.
failure:
  fingerprint: bang-chung-thieu-nguon-goc-lap-ba-lan
  category: content
successors: []            # phiên thi công KHÔNG tự mở packet kế nhiệm
```

---

## 1. Mỏ neo

| vai trò | commit | tree |
|---|---|---|
| `base_sha` = merge-base | `05de1ab81c235235b971a6fb8d8ae1fb226295d5` | — |
| **head đã dừng** | `2a332f37e7d91c7f9ec33d2702ee2725516c8a8c` | `0f12b7b44f6275912cd778977e2819bb69d90020` |

`master` đã đi tới `77d5b766` trong lúc packet chạy. Đo được: **không chạm write set** ⇒ không
xung đột, và ngân sách vẫn đo đúng theo merge-base như `don_vi` của lease khai.

```
git diff --numstat 05de1ab..2a332f3 -- <write_set>
  138  1  .claude/dev/packet_loop.py
  175  0  .claude/dev/packet_loop_test.py
    7  1  ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md
  => 3 tep, +320 -2   (tran 3/320 — DUNG tran)
```

## 2. Ba đặc tả, hai lần sửa lease — vì sao có tới ba bản

| bản | sha256 | vì sao bị thay |
|---|---|---|
| r1 | `9e1d049b…` | **M3 SAI**: đòi nhận `stdout_byte: 0` kèm rc≠0 |
| r2 | `dcfb81bb…` | M3′ vẫn sai: giữ `ma_thoat ∈ {12,13}` |
| **r3** | `71559dca…` | đang hiệu lực — nhưng M3″ **cũng** hở (§3) |

Lease neo lại hai lần và nới trần vòng review hai lần (2→3→4); mọi lần đều có khối `nang_tran`
đúng khuôn `ADR-0043` trên Issue #262 (`5383841852`, `5383944876`).

## 3. HÌNH DẠNG LỖI LẶP BA LẦN — đây là kết quả chính của packet

| bản | tiêu chí được tin | ai đặt được giá trị ấy |
|---|---|---|
| r1 | `stdout_byte: 0` kèm rc≠0 | tiến trình **con** |
| r2 | `ma_thoat ∈ {12,13}` | tiến trình **con** |
| r3 | `trang_thai ∈ {qua_han, hong}` | **executor** viết tệp |

**Ba lần đổi TRƯỜNG được tin; không lần nào lập NGUỒN GỐC.** Mỗi bản vá đúng với ca nó nhắm và
để nguyên cả lớp — đúng mô tả *"vá tiếp lúc nào cũng có vẻ đúng vì lần nào cũng có lỗi thật"*.

Ba phản chứng, chạy được, mỗi cái tái hiện độc lập trước khi vá:

```
r1 ->  {"trang_thai":"xong","ma_thoat":1,"stdout_byte":0}      # sys.exit(1) im lang
r2 ->  launcher THAT, con tu thoat 12  =>  {"trang_thai":"xong","ma_thoat":12}
r3 ->  {"trang_thai":"hong"}                                    # executor tu viet
       CA BA:  void-attempt --reason infrastructure  ->  rc=0,  attempts_used 1 -> 0
```

`launcher.py:50-51` đã cảnh báo sẵn cho ca r2: *"mã thoát của **TIẾN TRÌNH CON** được trả nguyên
vẹn, nên nó **ĐÈ LÊN** mọi mã ở đây"*. **Executor đã đọc đoạn ấy ở đầu phiên** — nó nằm trong 140
dòng hợp đồng mà `CLAUDE.md` bắt đọc trước mọi việc — và vẫn xây bằng chứng lên `ma_thoat`.

**Thứ còn thiếu, nói cho đúng:** không phải "chọn trường tốt hơn" mà là **xác thực NGUỒN GỐC** —
chứng minh launcher tạo ra bản ghi, và bản ghi thuộc ĐÚNG lượt chạy hiện tại. Thiếu nó thì mọi
trường trong `run.json` đều là lời khai của bên bị đo, và đổi trường chỉ dời chỗ hở.

## 4. Lệnh, mã thoát, và đột biến

```
python3 .claude/dev/packet_loop_test.py        rc=0   235/235 đạt   (nền master 225/225)
python3 -m ruff check --select F <2 tệp>       delta so master = 0
packet_loop.py doctrine-scan --root .          rc=0
packet_loop.py adr-song --root .               rc=0   (46 ADR / 46 dòng §20)
packet_loop.py begin-attempt --packet 262      rc=3   "đã dùng hết 3/3 lượt — packet về blocked"
```

**Mười một đột biến, không cái nào sống sót** — 9 trên mã, 2 trên **tài liệu**:

| # | đột biến | ca chết |
|---|---|---|
| 1 | gỡ hẳn chốt môi trường | `mt_thieu_cong_cu` `mt_chup_tren_nen_khac` `mt_anh_hong` (`mt_sach` **sống** — chiều tha, đúng) |
| 2–4 | bỏ `thieu_bat_buoc` · bỏ kiểm nền · gộp `khong_doc_duoc` | mỗi cái đúng một ca |
| 5 | **nhận lý do theo lời khai** (hành vi CŨ) | chỉ `void_ha_tang_khong_bang_chung` |
| 6 | đòi bằng chứng **cả bốn** lý do | `void_quota…` **+ 5 ca CŨ** dùng `quota` |
| 7–9 | bỏ thẩm quyền · không ghi sổ · bỏ `--can-cu` | mỗi cái chỉ `void_duong_thoat` |
| 10–11 | **trên TÀI LIỆU**: bỏ bước chụp ảnh · bỏ cờ `--bang-chung-moi-truong` | mỗi cái chỉ `luong_canonical_chay_that` |

**Và mười một đột biến ấy vẫn XANH trong khi ba đường hở tồn tại.** Lý do đo được: bộ đột biến đo
các chốt executor **BIẾT** mình đã đặt; nó mù với đường executor **TƯỞNG** đã có, và mù với ca
*"cùng một tệp đi hai đường xử khác nhau"*. Đó là giới hạn của phương pháp, không phải của lượt chạy.

## 5. HAI GỢI Ý VÁ CỦA REVIEWER — chưa áp, dành cho packet kế nhiệm

**(a) Xác thực nguồn gốc launcher.** `_doc_so_lauch` phải chứng minh launcher tạo ra bản ghi và bản
ghi thuộc lượt chạy hiện tại. Khoá bằng **một con lỗi nội dung THẬT** tự viết bản ghi giả và phải
nhận `rc=10`, cộng đột biến gỡ phép xác thực nguồn gốc. Rủi ro tương thích reviewer đã nêu: bản ghi
cũ không ký sẽ **hết đủ tư cách**.

**(b) Dùng chung phép kiểm nền/tuổi.** Gom vào một hàm cho **cả hai** người tiêu thụ. Thêm ca ảnh
cũ và ảnh sai nền phải **GIỮ** attempt, cộng đột biến bỏ qua phép xác thực. Tái hiện được: ảnh 10
ngày tuổi nền `Plan9` bị `begin-attempt` từ chối mà đường `void` **nhận**, `attempts_used 1→0`.

## 6. `chua_do_duoc`

- **Không đo được còn bao nhiêu tiêu chí khác của packet cùng bệnh.** Ba cái lộ ra vì có người
  chạy đúng ca của chúng; phần còn lại chưa ai thử phá theo cách ấy.
- **N10′ chỉ đo thật trên Windows** (khối là PowerShell dùng `$env:TEMP`); trên `ubuntu-latest` nó
  bỏ qua **có in lý do**. Ca có mặt ở cả hai nền, chỉ đo ở một.
- **`trang_thai` vẫn là thứ ghi ra đĩa.** Ngay cả (a) cũng chỉ đóng được đường *"con tự chọn mã
  thoát"* nếu nguồn gốc được ký; chưa ai thiết kế phần ký.
- **Ngưỡng tươi 3600s là CHỌN, không phải ĐO.**

## 7. Trạng thái để lại

| | |
|---|---|
| PR #266 | **MỞ**, cổng xanh cả hai nền trên `2a332f3` — **KHÔNG merge nguyên trạng** |
| packet #262 | `blocked` · attempts 3/3 · 4 vòng review · 6 finding |
| lease | **KHÔNG được hồi sinh** (§12); reroute phải là generation mới |
| `ops/specs/` | r2 (`dcfb81bb…`) và r3 (`71559dca…`) chưa land — nằm trên nhánh của PR #266 |
| cây làm việc | sạch, không worktree lạc |
