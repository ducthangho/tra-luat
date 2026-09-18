# CHỈ THỊ EXECUTOR — packet #541 `WP541-PATH-TOI-THIEU-THEO-NEN` **revision 2 / generation 2**

Gửi: `agy` (antigravity) · Nền: Windows, local · Vai: **executor**
Soạn: phiên điều phối claude, `2026-09-18T16:00Z`

> **Đây là CHỈ THỊ, không phải đặc tả và không phải lease.** Đặc tả là `spec r3`; lease là
> `wp541-path-r2-g2-antigravity`. Nếu tệp này mâu thuẫn với hai thứ kia thì **hai thứ kia
> thắng** — và hãy báo lại chỗ mâu thuẫn, đừng tự hoà giải.

---

## 0. TỰ XÁC MINH TRƯỚC — đừng tin bảng số trong tệp này

Kho này đã trả giá vì điều phối đưa bảng giá trị cho executor thay vì đưa đường tự kiểm.
Chạy đúng các lệnh dưới đây rồi **đọc từ chính tệp**, không đọc từ tôi:

```bash
git fetch origin '+refs/heads/*:refs/remotes/origin/*'
git config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*'   # nếu clone bị siết

# LEASE — nguồn có thẩm quyền
git show origin/ops/cap-lease-541-g2:ops/leases/wp541-path-r2-g2-antigravity.yaml

# SPEC r3 — đặc tả đóng băng
git show origin/claude/spec-541-r3-20260918:ops/specs/wp541-path-toi-thieu-theo-nen-r3.md

# BĂM spec phải khớp spec_hash trong lease
git cat-file blob origin/claude/spec-541-r3-20260918:ops/specs/wp541-path-toi-thieu-theo-nen-r3.md | sha256sum
# mong: 3920f23f9635e46899dac4157a8d1e7eb49a3dee64996ca9fe0644e87b1a379d
```

Băm không khớp ⇒ **DỪNG**, báo lại. Đừng đoán, đừng lấy băm của tệp lease làm `spec_hash`.

---

## 1. CẢNH BÁO ĐẦU TIÊN: lease KHÔNG có comment công bố trên #541

Nếu preflight của bạn đi tìm một comment công bố lease trên Issue #541 thì **sẽ không thấy**, và
đó **không** phải lý do để từ chối. Sự thật đã đo:

- Lease **đã cấp** — đẩy lên `ops/cap-lease-541-g2` lúc `2026-09-18T15:54Z`. Trong kho này **hành
  vi cấp là lần `git push` lên `ops/**`**, comment chỉ là **bản chiếu**.
- Workflow `ops — đăng lease bằng git` chạy lượt `35365260980` và **ĐỎ ở bước `tự kiểm cổng
  trước khi tin nó`**, nên bước `đăng` bị `skipped`. Fail-close đúng thiết kế.
- Nguyên nhân đỏ là **`t125`**, một ca **chập chờn** — không phải lease sai, không phải mã bạn sẽ
  sửa. Chi tiết ở §7.

**Nguồn có thẩm quyền là TỆP LEASE CÓ BĂM trong kho**, không phải comment. Lease thật:

```
ops/leases/wp541-path-r2-g2-antigravity.yaml  @ origin/ops/cap-lease-541-g2
blob 35510a342989ed3fef8e865c9adc5e2f46937923
```

---

## 2. Vì sao có generation 2 — và bản vá g1 của bạn KHÔNG bị vứt

`2f70869a` **đạt** nghiệm thu thật của r2: `N1`–`N4` (`t165`–`t168`) QUA cả bốn trên **Windows
thật** của chủ kho (18-09, quyền Administrator, `rc=0`), và đột biến N7 giết `t165` **đúng lý do**.
Giải đường dẫn thật trả `C:\Program Files\Git\cmd\git.exe`; shim `.bat/.cmd/.py` bị từ chối; đối
chứng dương (thêm `git.exe`) tìm ra. 15 ca từng đỏ trên CI nay **11 xanh**.

g2 tồn tại vì **review tìm thêm bốn hướng r2 không nói tới**, cộng một chỉ thị mở rộng của chủ kho.
`docs/PROTOCOL_DA_PHIEN.md:300`: *"Mở rộng phạm vi hay đổi closure là revision mới, generation mới
và cấp lại lease."*

**Không phải bạn làm sai đặc tả.** r2 `:192-199` **im lặng về đuôi tệp** — nó chỉ đòi loại `cwd` và
`%SystemRoot%` ở "mọi bước". Ràng buộc `git.exe` sinh ra từ review lượt 1–2 và bạn đã áp nó cho
bước 3, đúng phạm vi bạn được giao.

---

## 3. NHÁNH — đọc kỹ, có một điều CẤM

- Làm tiếp trên **`fix_issue_541`**, head hiện tại `2f70869a0537843e9cae78618ee7ae8c261d972d`.
  PR **#554** giữ nguyên. Lease g2 khai đúng tên nhánh này (g1 khai tên khác và lệch ấy đã thành
  một finding — không lặp lại).
- `origin/master` đã đi **5 commit** kể từ base `d705623`; nay là `eb15657dae7a`.
  **Hoà bằng `git merge origin/master`. CẤM `git rebase`.**
  Lý do đo được: `2f70869a` là `reviewed_sha` của **bốn** lượt review; rebase làm cả bốn verdict
  trỏ vào SHA không tra được.
- `base_sha` giữ nguyên `d705623162b75b7340ee7cca54ac2d2abbddbb6f` — mọi phép đo kích thước
  (§6) đo **so với SHA này**.

---

## 4. ĐIỀU KIỆN BẮT ĐẦU — một đường bị chặn, phải ĐO chứ đừng xem đồng hồ

- `ops/lease_publish.py` → **rảnh**, bắt tay ngay (M3–M6).
- `ops/lease_publish_test.py` → còn bị `ci-windows-r2-g2-antigravity` (#548) giữ. Đo `16:00Z`:
  `NGƯỜI_GIỮ 2`. Lease ấy khai hết hạn `17:00:00Z`.

**Không được suy từ mốc 17:00Z.** `"hết hạn"` ≠ `"đã nhả"`: lease gia hạn được, và phải đọc cả
`da_bi_thay_the`. Đo trước MỖI lần chạm:

```bash
python ops/lease_publish.py ai-dang-giu ops/lease_publish_test.py; echo "rc=$?"
```

Chỉ chạm khi `rc=0` / `NGƯỜI_GIỮ 0`. Đọc `rc` **trực tiếp**, đừng qua pipe — `| tail` làm `rc`
thành của `tail`.

Nếu `ai-dang-giu` trả `rc=12`, đó là **fail-close đúng**, không phải hỏng. Hai nguyên nhân đã gặp
hôm nay, cả hai có cách chữa: nhánh `master` cục bộ tụt sau (`git branch -f master origin/master`),
và bộ đệm ref thiếu nhánh máy chủ (fetch lại). Chốt hai nguồn chạy TRƯỚC khi tin bất kỳ kết quả quét
nào:

```bash
git ls-remote --heads origin | sed 's#.*refs/heads/##' | sort > /tmp/mc
git for-each-ref --format='%(refname:lstrip=3)' refs/remotes/origin | grep -v '^HEAD$' | sort > /tmp/cb
comm -23 /tmp/mc /tmp/cb    # PHẢI RỖNG
```

---

## 5. VIỆC — sáu mục tiêu. Chi tiết và lý lẽ ở spec r3 §muc_tieu

Write set **KHÔNG đổi**: `ops/lease_publish.py` · `ops/lease_publish_test.py`.

| | việc | tệp |
|---|---|---|
| **M3** | Bước 1 (`CONG_CU_GIT`) chỉ nhận `git.exe`. Sửa cả docstring — câu *"chỉ chấp nhận git.exe, không qua PATHEXT"* hiện đọc như bất biến của **cả hàm** trong khi nó đúng cho **một trong ba** bước. | `lease_publish.py` |
| **M4** | Bóc nháy kép + khoảng trắng mỗi mục PATH: `d = d.strip().strip('"')`. Mục rỗng sau khi bóc thì bỏ qua. | `lease_publish.py` |
| **M5** | Tách PATH theo `os.pathsep` của **nền đang chạy**, không đoán dấu phân cách từ NỘI DUNG chuỗi. Ca cần tiêm PATH kiểu Windows trên Linux thì truyền dấu phân cách **tường minh** qua tham số. | `lease_publish.py` |
| **M6** | Chỉ ghi `sys.stderr` khi `chan_doan is None`. **KHÔNG được bỏ hẳn chẩn đoán** — đây là đổi KÊNH, không phải bịt miệng. | `lease_publish.py` |
| **M7** | Hằng đường dẫn sentinel trong fixture `t136` phải **tuyệt đối trên CẢ HAI nền** (dựng từ thư mục sandbox, ví dụ `str(Path(s) / "khong-co-git")`). Giữ nguyên ý định ca: `rc == 12` **và** lý do chứa `"không khớp executable"`. | `lease_publish_test.py` |
| **M8** | **5 ca mới** cho M3–M7, chạy được trên `ubuntu-latest` bằng tham số tiêm, **mỗi ca một đột biến riêng**. | `lease_publish_test.py` |

### Phép đo đã tái hiện độc lập cho M3–M5 (chạy được, dùng làm phản chứng)

```
=== CA DOI CHUNG (chạy TRƯỚC, biết trước đáp án) ===
  git.exe ngoai cwd  -> NHAN   OK
  git.exe TRONG cwd  -> None   OK

  CONG_CU_GIT=git.exe                      -> NHAN
  CONG_CU_GIT=git.bat                      -> NHAN     <- M3
  CONG_CU_GIT=git.cmd                      -> NHAN     <- M3
  CONG_CU_GIT=git.py                       -> NHAN     <- M3
  CONG_CU_GIT=khong-phai-git-chut-nao.txt  -> NHAN     <- M3

  PATH=khong nhay   -> NHAN
  PATH=co nhay kep  -> None (TU CHOI)                  <- M4

  os.pathsep=':', mot muc chua ';' trong TEN -> None   <- M5
```

Script tái hiện: `ops/reviews/wp541-kiem-lai-luot4.py` @ `origin/claude/review-541-luot3-20260918`.

### M7 — vì sao nó tồn tại, đọc kẻo sửa sai chỗ

`t136` tiêm `git_path="/khong/co/git"` và đòi `rc == 12` **KÈM lý do** `"không khớp executable"`.
Hằng ấy chỉ-POSIX:

```
POSIX    is_absolute("/khong/co/git") = True
WINDOWS  is_absolute("/khong/co/git") = False
```

Nên trên Windows `kiem_mien_ho_so` bắn TRƯỚC với lý do khác: **`rc` đúng, lý do sai**. Sửa **hằng
trong fixture**, KHÔNG nới `kiem_mien_ho_so` — phép kiểm ấy đang đúng.

---

## 6. NGHIỆM THU — spec r3 §nghiem_thu là nguồn. Tóm ở đây để khỏi đọc sót

| # | phải đúng | đột biến làm nó ĐỎ |
|---|---|---|
| **N8** | `CONG_CU_GIT` trỏ `.bat`/`.cmd`/`.py`/`.txt` ⇒ `None`; trỏ `git.exe` hợp lệ ngoài `cwd`/`%SystemRoot%` ⇒ trả đúng đường ấy | gỡ phép kiểm tên ở bước 1 |
| **N9** | Mục PATH bọc nháy kép ⇒ **NHẬN**; mục rỗng/toàn khoảng trắng ⇒ bỏ qua, không ném | bỏ `.strip().strip('"')` |
| **N10** | PATH posix có một mục mang `;` trong TÊN, mục kia có `git.exe` ⇒ **tìm ra** | quay lại `split(";" if ";" in path_val else os.pathsep)` |
| **N11** | Truyền `chan_doan=ds` ⇒ `ds` có thông báo **và** stderr **0 byte**; KHÔNG truyền ⇒ stderr **vẫn có** | **hai** đột biến: (a) trả `stderr.write` về vô điều kiện; (b) bỏ hẳn lệnh ghi |
| **N12** | Mọi hằng sentinel trong fixture schema hồ sơ adapter tuyệt đối trên **cả hai** nền: `PurePosixPath(s).is_absolute() and PureWindowsPath(s).is_absolute()` | trả hằng về `"/khong/co/git"` ⇒ ĐỎ **trên ubuntu** |
| **N5'** | *(chỉ báo)* bộ test trên `ubuntu-latest`: **0** ca đỏ | đỏ ⇒ hồi quy do g2 |
| **N6'** | `git diff --numstat` so `d705623`: **≤ 2 tệp và ≤ 400 dòng thêm** | vượt ⇒ **DỪNG** |

**Mỗi ca phải có ĐỐI CHỨNG DƯƠNG.** Ca chỉ đo chiều "phải từ chối" thì `return None` vô điều kiện
cũng qua được — kho đã trả giá (`t24`: suite báo 24/24 trong khi ca ấy không đo gì).

**Năm ca phải phân biệt được bằng ĐẦU VÀO.** Không phân biệt được thì chúng là **bộ tương đương** —
khai thẳng, đừng giả vờ có năm chốt.

### Ngân sách dòng — đo TRƯỚC khi mở review, đừng đo sau

```bash
git diff --numstat d705623162b75b7340ee7cca54ac2d2abbddbb6f HEAD
```

g1 đã dùng **+270**. Trần **400**. Còn **~130 dòng** cho cả sáu mục tiêu. Dự toán của spec là ~410 —
**cố ý sát trần**, để bạn phải đo thật. Vượt 400 ⇒ **DỪNG và handoff, KHÔNG tự nới**.

Trần 400 (không phải 300) là ngoại lệ **đã khai trong spec r3 §KÍCH THƯỚC** theo đúng cửa ADR-0044
tự mở. Đừng xin lại, cũng đừng tự nâng tiếp.

---

## 7. `t125` — ĐỌC TRƯỚC KHI HOẢNG

`t125_AB_toan_suite_KHONG_doi_verdict_theo_ambient_actor` chạy **toàn bộ suite hai lượt** (có/không
`GITHUB_ACTOR`) rồi so. Nó **chập chờn** và đã chặn hai phép đo khác nhau trong một ngày:

- Windows của chủ kho, 18-09: ĐỎ, ca lệch `t156`.
- CI lượt đăng lease g2, `15:54Z`: ĐỎ, ca lệch `t139` — `S8-bo-deadline: kỳ vọng GIET, thực SONG
  (seam: KhoObject._con_thoi_gian)`, tức một đột biến **hạn chót**, phụ thuộc thời gian/tải.

Phép đo tách nguyên nhân: lượt `ops/cap-lease-541-g2` (`15:54:30Z`) **ĐỎ** còn lượt
`ops/cap-lease-541` (`15:55:04Z`) **XANH** — cách nhau **34 giây**, `lease_publish.py` và
`lease_publish_test.py` **giống từng byte** trên hai nhánh (blob `8a58066385` và `06701deb6e`).

**Ba điều cho bạn:**

1. `t125` **NGOÀI PHẠM VI** r3. Đừng sửa nó. Đừng "ổn định hoá" nó. Đừng nới nó.
2. Thấy `t125` đỏ ⇒ **KHÔNG** đọc thành hồi quy của mình. Đo lại; nếu `t139`/`t156` chỉ đỏ ở một
   trong hai nhánh A/B thì đó là chập chờn.
3. Nhưng **đừng dùng "chắc là flake" làm lá chắn.** Nếu một ca đỏ **lặp lại ổn định** qua nhiều
   lượt, hoặc đỏ với lý do khác hẳn hai lý do trên, thì đó là chuyện khác — báo lại kèm log.

---

## 8. CẤM — nguyên văn từ lease g2

- `self_review` · `self_approve` · `merge` · `land` · `deploy` · `LIVE` · `ruleset mutation` ·
  `admin bypass` · `secret disclosure`
- `workflow_dispatch` · `manual full CI` · **Windows CI** (`manual_ci_budget: 0`)
- **CHẠM `ops/lease_publish_test.py` trước khi `ai-dang-giu` cho đường ấy trả `rc=0`**
- **REBASE nhánh `fix_issue_541`**
- **VÁ `t150`** — thuộc #552, lease riêng đã cấp 18-09
- **VÁ `t131` / `t132` / `t35`–`t40` / `t125`** — ngoài phạm vi r3, xem spec §ngoai_pham_vi
- Đặt `_git_windows` vào `ops/cong_cu.py` — Issue #541 khai write set `only` hai tệp
- Thay phép giải cố định bằng PATH thừa kế **không giới hạn** (nguyên văn Issue #541)
- **Bỏ hẳn chẩn đoán N3b khi làm M6** — M6 đòi **chuyển kênh**, không phải bịt miệng
- Nới write set quá hai đường
- Vượt 2 tệp hoặc 400 dòng thêm
- Viết dấu bỏ-qua-CI nguyên văn trong thông điệp commit, **kể cả khi trích dẫn**
- Đọc `rc` qua pipe

Kèm hai kỷ luật kỹ thuật của kho:
- **Đột biến chạy trên BẢN SAO TẠM**, không bao giờ trên tệp thật. Lượt chạy bị cắt giữa chừng thì
  `finally` không chạy và tệp ở lại trạng thái méo — đã có một bản vá NGƯỢC đi thẳng vào commit
  theo đường này.
- **`core.abbrev = 7`** khi chạy gate.

---

## 9. DỪNG — năm điều kiện, mỗi cái nói rõ phải báo gì

1. `--numstat` vượt **2 tệp** hoặc **400 dòng thêm** ⇒ DỪNG, handoff, kèm số đo. Không tự nới.
2. Năm ca của M8 **không phân biệt được bằng đầu vào** ⇒ khai là bộ tương đương, báo lại, đừng tự quyết.
3. Một ca của M8 **không dùng được tham số tiêm** để chạy trên `ubuntu-latest` ⇒ DỪNG và báo. Đó là
   con đường **duy nhất** còn lại: #548 đã gỡ Windows khỏi cổng master (ADR-0049), và
   `manual_ci_budget: 0`.
4. Cần chạm `ops/cong_cu.py`, workflow, hay bất kỳ đường nào ngoài write set ⇒ DỪNG, xin revision.
5. **Một hình dạng lỗi lặp lần thứ BA** ⇒ DỪNG, hỏi *"có nên làm việc này không"*, đừng hỏi
   *"vá thế nào"*.

---

## 10. BÁO CÁO — cái tôi cần nhận lại

Không cần văn hoa. Cần đo được:

1. `git diff --numstat d705623… HEAD` — nguyên văn đầu ra.
2. Với mỗi N8–N12: ca tên gì, **chạy ra sao**, và **đột biến nào** làm nó đỏ — kèm đầu ra thật của
   lượt chạy đột biến, không phải lời hứa trong docstring.
3. Bộ test đầy đủ trên `ubuntu-latest`: dòng tổng kết nguyên văn `lease_publish: N/M đạt; …`.
4. Chỗ nào **không đo được** thì ghi thẳng `KHÔNG ĐO ĐƯỢC` kèm lý do. **Đừng làm tròn, đừng suy.**
   Một câu khai rộng hơn phép đo là thứ kho này phạt nặng nhất.
5. SHA ứng viên cuối cùng để reviewer neo `reviewed_sha`.

---

## 11. ĐÍNH CHÍNH MỘT CON SỐ TRONG SPEC r3 VÀ TRONG LEASE — đọc, và tin tệp này ở đúng chỗ này

Spec r3 (`:30`) và lease g2 (`ke_hoach_rebase`) đều ghi *"`origin/master` đã đi **13 commit** kể từ
`d705623`"*. **Sai.** Đo lại `16:05Z 18-09`:

```
d705623..origin/master =  5 commit     <- ĐÚNG
a612c70..origin/master = 13 commit     <- con số 13 thuộc mốc NÀY
```

`a612c70` là base của **spec r2**, không phải base của lease. Tôi lấy số đo đúng của một mốc rồi
gán cho mốc khác — đúng lớp lỗi *"một quan hệ đúng trông giống các số hạng đúng"* mà `CLAUDE.md`
chép sẵn.

**Phạm vi thiệt hại: không có.** Con số ấy nằm trong một câu GIẢI THÍCH vì sao phải `merge` thay vì
`rebase`; lý lẽ ấy là `2f70869a` là `reviewed_sha` của bốn lượt review, và nó đúng dù 5 hay 13.
Không tiêu chí nghiệm thu nào, không chỉ thị nào đổi theo con số này.

**Spec r3 và lease g2 CHƯA sửa, có chủ đích.** Sửa spec làm đổi `spec_hash`, kéo theo phải cấp lại
lease — cái giá ấy lớn hơn một con số mô tả. Chủ kho quyết có cần r4 hay không. Tới lúc đó, **tệp
này là bản đúng cho riêng con số ấy**; mọi thứ khác thì spec và lease vẫn thắng.

---

## 11. Hai chỗ trống tôi khai thẳng, không giấu

- `granted_on_instruction` của lease trỏ vào **Issue #541**, không vào một comment chỉ thị — chủ kho
  chưa đăng comment nào. Cổng **không** cưỡng chế trường này. Nếu preflight của bạn đòi một chỉ thị
  neo được, đây là chỗ nó thiếu; báo lại chứ đừng tự lấp.
- `assurance_target: human_audited` nhưng **chưa có người audit thật**. Bốn lượt review của g1 đều
  là phiên claude, trần cứng của chúng là `advisory_review`. Verdict cuối cùng của g2 cần **người**.
