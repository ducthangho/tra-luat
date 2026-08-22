# Prompt REVIEWER — `LEASE-DANG-DUNG-MOT-LAN` (#227), lượt **4** — REVIEW DELTA

Lease `lease-dang-review-4-claude-20260822`. **CHỈ ĐỌC.** Không sửa, không commit, không push.

## Neo

- Exact head: **`6eaa3755abd96ef6d8f820daaa6b9d96e2bdd7b5`**
- Nền delta (head lượt trước): **`b32b424165c4a952661cf776bf953d91a7eaf814`**
- Nền packet: `cfaccff9bb373274552042e01edb4bfee81dc0ed`
- Delta lượt 6: **một tệp** `ops/lease_publish_test.py`, **+101/−9**
- Đặc tả **r6** `4ee67d54b5504c0b303dad3bf8470c912ad754e6bcda42e8cb4a2866475ba181`
  trên nền r5 `2c8fb5c6…` · r4 `abe7c292…` · r3 `c65d5dbd…` · r2 `3f310582…`
- Verdict lượt 3 `79f8bb2a48e92f9081cd50ba0d6d24a8f4bd7246d92ab0cc2d500e26ecfe24a0`
- Handoff lượt 4 `dfada285…` · handoff lượt 5 `d53e127f…`

Lấy từ `origin/ops/lease-dang-227`. **KIỂM BĂM; lệch ⇒ DỪNG.**

## Đã đo lại độc lập — đừng tiêu thời gian chứng minh lại

| phép đo | kết quả |
|---|---|
| `numstat cfaccff9..HEAD` | 3 tệp, **+633/−19** (trần 660) |
| suite thường · suite Actions + `gh` **vắng** | **`67/67` rc=0** cả hai |
| `actionlint` | rc=0, 5 tệp |
| **M4** dời `check` qua **sau** POST, giữ nguyên tập vế | **`64/67`**, ĐỎ `t51 t63 t67` — **phép thử quyết định ĐẠT** |
| gỡ guard `mark` · `body` · `$GITHUB_ENV` | mỗi cái **`66/67`**, ĐỎ `t66` (ở head trước **cả ba sống sót `63/63`**) |

## Bối cảnh — đọc kỹ, nó quyết định phạm vi review

Packet này đã qua **sáu** lượt vá. Hình dạng lỗi lặp lại **không nằm ở bản vá** mà ở **đặc tả**:
ba lần liên tiếp đặc tả (do phiên điều phối viết) **liệt kê sai** — hai lần sai **độ phân giải**
(khối vs nhánh), một lần sai **pha thời gian** (đòi khẳng định *"không POST"* cho ba guard nằm
**sau** lời gọi POST). Executor **DỪNG đúng chốt hai lần liên tiếp** thay vì lách.

`r6` là nước đi cuối: **đặc tả THÔI liệt kê vế khẳng định**, chỉ nêu bất biến — *mỗi ca khẳng
định thứ QUAN SÁT ĐƯỢC tại vị trí guard ấy, và KHAI thứ không quan sát được* — còn executor
**dẫn xuất** tập vế từ vị trí, và vị trí thì **dẫn xuất từ YAML**.

**Việc của bạn là kiểm xem nước đi ấy có THẬT hay chỉ dời chỗ ghi cứng.**

## Việc — đo, đừng đọc

### 1. Vị trí có THẬT dẫn xuất không, hay chỉ dời chỗ ghi cứng?

`M4` chết, nhưng đó mới là **một** hướng. Tấn công phép dẫn xuất:
- Nó nhận diện lời gọi POST bằng gì? Chuỗi `gh api`? `ID=$(`? Nếu đổi cách viết lời gọi POST
  (thêm khoảng trắng, đổi tên biến, tách dòng, dùng `$( )` lồng) mà phép dẫn xuất **không** thấy
  POST nữa thì nó rơi vào trạng thái nào — **ĐỎ** hay lặng lẽ coi mọi guard là "trước POST"?
  **Ba trạng thái**: thấy · không thấy · không phân tích được. Hai trạng thái sau **phải ĐỎ**.
- Có **hai** lời gọi giống POST thì sao? Một dòng **chú thích** chứa `gh api` thì sao?
- Dời một guard **sau POST** lên **trước POST** (chiều ngược của `M4`) ⇒ có ĐỎ không?

### 2. Bộ trích guard có bỏ sót hình dạng nào không?

`t64` đối chiếu tập dẫn xuất với sổ đăng ký. Nhưng nó dẫn xuất theo **mẫu** nào? Thử các hình
dạng guard **khác** mà một người sẽ viết thật:
- `set +e` và lệnh trên **cùng một dòng**;
- `cmd || rc=$?` thay cho `set +e … rc=$?`;
- `if ! cmd; then …` (không dùng `rc` chút nào);
- guard nằm trong một **hàm shell** thay vì thân vòng lặp.
Hình dạng nào lọt ⇒ đó là guard **thêm được mà không ai đăng ký** ⇒ finding.

### 3. Vế khẳng định — có ca nào TRỐNG RUỘT không?

Codex khai bảng vị trí. Với **mỗi** guard, hỏi: nếu tôi **giữ nguyên** guard nhưng làm hành vi
của nó **sai** (không phải gỡ hẳn), ca có ĐỎ không? Đặc biệt soi guard `$GITHUB_ENV` — chính
codex khai *"dòng env cuối là trạng thái cộng dồn, không quy thuộc riêng một lease"*. Vế của nó
có còn nói được điều gì không?

### 4. Hồi quy

**9 dòng bị xoá** trong tệp phản chứng. Từng dòng phải có lý do.
`git diff b32b4241..6eaa3755 -- ops/lease_publish_test.py`

### 5. Hình dạng **D lần 4**

D = *đặt câu hỏi kiểm chứng ở sai độ phân giải / sai pha*. Bộ đếm **3**, cả ba do phiên điều
phối. `r6` đăng ký: **D lần 4 ⇒ DỪNG**.

Câu hỏi: **bản vá "dẫn xuất" có tự nó mắc D không?** Nếu tập vế nay dẫn xuất theo **hai** nhóm
(trước/sau POST) mà thực tế cần **ba** hoặc cần chia theo trục khác, thì đó là D lần 4 — **nêu
thẳng**, kể cả khi nó làm packet phải dừng.

## Ngoài phạm vi — ĐỪNG báo

`ngoai_pham_vi` + `chua_do_duoc` của r2–r6, đặc biệt: **cửa sổ "POST xong, `mark` hỏng"** (thuộc
tính của thiết kế, cấm vá) · khe race hai nhánh `ops/**` · nợ nền `chay(env=None)` · nhánh "một
phần" trong `_doc_gh`/`_kiem_loai_so_hieu`/`_kiem_comment_da_co` · `t59` chỉ so `argv[0:2]` ·
chưa có Actions thật / Windows · ruleset ngoài kho.
Thấy một mục `chua_do_duoc` khai **hẹp hơn thực tế** thì ĐÓ mới là finding.

## Verdict

```
KET_LUAN: <cross_approved | can_sua | dung_lai>
reviewed_sha: 6eaa3755abd96ef6d8f820daaa6b9d96e2bdd7b5
```
Từng finding: **P1/P2/P3** · một câu · **lệnh + đầu ra thật** · đề xuất vá.

Cuối: **`da_do_gi`** và **`khong_do_duoc`**. **"Thu hẹp"** khi chỉ thu hẹp; **"đóng"** chỉ khi có
phép đo.

**Ngân sách còn ~27 dòng** (`+633/660`). Nếu bạn kết luận `can_sua`, hãy nói rõ bản vá bạn đề
xuất **có lọt 27 dòng không** — người giữ kho cần con số ấy để quyết.

Nếu `cross_approved`, **nói thẳng cái vẫn còn hở**.

Nguồn sự thật là **tệp có băm trong kho**; prompt này chỉ là bản chiếu.
