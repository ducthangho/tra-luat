## Findings

### 1. Lời gọi bộ kiểm trong `ops-publish-lease.yml` KHÔNG còn chốt nào bắt nó phải đến từ `$NEO` — P1

Diff đổi lời gọi từ `python3 "$NEO/ops/lease_publish_test.py"` sang `bash "$NEO/ops/chay_lease_publish_test.sh"`. Regex của `t25` chỉ nhận `python3?\s+(\S*lease_publish(?:_test)?\.py)`, nên lời gọi mới **vô hình** với nó. Mã hiện tại vẫn đúng; thứ bị gỡ là cái máy giữ cho nó đúng.

**Bằng chứng đo được — HAI CHIỀU, đột biến chạy trên bản sao tạm.**

Trên `base2` (cây `git archive a09aae62`, tức bản TRƯỚC PR):

```text
BASE_NEN rc=0 :: lease_publish: 38/38 đạt
# đột biến: run: python3 "$NEO/ops/lease_publish_test.py" -> python3 ops/lease_publish_test.py
BASE_M9_bo_NEO rc=1 :: lease_publish: 37/38 đạt ::   ĐỎ  t25_workflow_dang_lease_phai_chay_bo_kiem_NEO_khong_lay_tu_head,
```

Trên `mut1` (bản sao của exact head `e071e0aa`):

```text
# đột biến: run: bash "$NEO/ops/chay_lease_publish_test.sh" -> bash ops/chay_lease_publish_test.sh
M9_wrapper_khong_NEO rc=0 :: lease_publish: 40/40 đạt ::
M9_ACTIONLINT_RC=0
```

Đếm lại chính bằng regex của `t25` trên `ops-publish-lease.yml` ở head:

```text
  207: "$NEO/ops/lease_publish.py
  216: "$NEO/ops/lease_publish.py
  226: "$NEO/ops/lease_publish.py
TONG = 3
```

Ba lời gọi còn lại đều là `lease_publish.py`. Chốt chống-xanh-rỗng `bang(thay >= 3, ...)` vẫn qua, nhưng chú thích của nó ghi *"chờ ít nhất 3 (test, check, body)"* — **`test` không còn trong ba cái đó**. Ngưỡng ấy nay được thoả bởi ba lời gọi khác, nên nó không còn phát hiện được việc lời gọi bộ kiểm biến mất hay tuột `$NEO`.

Không chốt nào khác bù vào: `grep -n "chay_lease_publish_test" ops/lease_publish_test.py` cho đúng 4 dòng — một dòng thông điệp lỗi của `t34`, hai mục trong `GOI_WRAPPER` của `t35` (**chứa sẵn cả dạng KHÔNG `$NEO`**), và đường dẫn wrapper trong `t40`.

**Invariant bị cắt**

Mọi lượt chạy cổng đăng lease phải đến từ bản neo vào nhánh mặc định, không từ head được đẩy — đúng invariant của finding P1 trên PR #104. `ops-publish-lease.yml` bắn theo `push` vào `ops/**`, nên nếu lời gọi tuột `$NEO` thì head được đẩy chạy CHÍNH bản `lease_publish_test.py` và `cai_actionlint.sh` của nó. Chú thích mới ngay trên bước ấy khẳng định *"Vì wrapper cũng đến từ `$NEO`, head được đẩy không thể sửa installer hoặc selftest mà cổng này sẽ chạy"* — câu ấy đúng với tệp hôm nay và **không còn phép đo nào giữ nó đúng ngày mai**. Đây đúng lớp "guard không nối vào đường TỰ ĐỘNG thì guard chỉ là tài liệu", và `t25` tự khai mục đích của nó là chặn *"bản vá bị dọn cho gọn về lại `ops/…`"* — tức chính kịch bản vừa mở lại.

**Gợi ý vá** (trong write set, `ops/lease_publish_test.py`)

Mở `t25` sang cả lời gọi thực thi wrapper, giữ nguyên tính chất "đo ĐỐI SỐ có `$NEO` hay không" chứ không đi phân tích shell:

```python
goi = re.compile(r"(?:^|\s)(?:python3?|bash|sh|exec)\s+(\S*(?:lease_publish(?:_test)?\.py|chay_lease_publish_test\.sh))")
```

và nâng chốt chống-xanh-rỗng lên `>= 4` kèm một chốt riêng *"phải thấy ít nhất một lời gọi wrapper"*, để "gỡ sạch lời gọi bộ kiểm" không lẫn màu với "gọi đúng". Lưu ý dòng `sha256sum ops/… ops/…` ở bước neo CỐ Ý không có `$NEO` (in băm bản head để đối chiếu) — vì vậy phải bó theo **token lệnh dẫn đầu** như trên, đừng bó theo "có nhắc tên tệp". Cần đột biến khoá lại: bỏ `$NEO` khỏi lời gọi wrapper phải làm `t25` ĐỎ 1/1.

---

### 2. Nợ `PLAT-X5-required-status-check` chỉ nằm trong chú thích, trong khi kho có sổ nợ thật — P2

**Bằng chứng đo được**

```text
$ grep -rn "PLAT-X5-required-status-check" . | grep -v "^./.git/"
ops/lease_publish_test.py:1179:    NỢ CÓ TÊN `PLAT-X5-required-status-check`: branch protection phải require status của
ops/chay_lease_publish_test.sh:11:# do thuoc required status check `PLAT-X5-required-status-check`, khong thuoc mot bo
.github/workflows/ci.yml:135:      # NỢ CÓ TÊN `PLAT-X5-required-status-check`: selftest không thể tự chứng minh job
```

Ba chỗ, cả ba là chú thích/docstring. Kho có `ops/NO_KY_THUAT.md` — *"Tệp này là **sổ nợ**"* — với **tiền lệ đúng khuôn**: mục 8 `PLAT-X2 (#195) LAND KÈM NỢ RE-AUDIT`, có "Đo được", "Nợ chính xác là gì", "Điều kiện coi là XONG". Không có mục nào cho `PLAT-X5`; `git log -- ops/NO_KY_THUAT.md` không có commit nào của packet này, và diff `base..head` đúng 5 tệp, không tệp nào là sổ nợ hay handoff (`ops/handoff/` vẫn đúng hai tệp cũ).

Và nợ này nay **gánh tải thật**, không phải trang trí. Đo trên `mut1`, thêm `if: false` vào bước wrapper của `ci.yml`:

```text
F2p_if_false_tren_wrapper      rc=0   lease_publish: 40/40 đạt ::
   actionlint_rc=0
```

Tức phần dư của F2 — cổng **vắng mặt** thay vì đỏ — được ký gửi hoàn toàn cho required status check. Lập luận "F2 nay vô nghĩa" là ĐÚNG (đã đo: không còn đường "test chạy mà thiếu công cụ", xem §Đã đo sạch), nhưng thứ thay thế nó thì chưa được ghi ở chỗ ai đọc.

**Invariant bị cắt**

Packet §4.4: *"Nợ phải KHAI, không được để im … phải thành **một mục nợ có tên**, không phải một khoảng lặng."* Một mục nợ nằm trong chú thích của chính tệp bị nợ thì chỉ người đang sửa tệp ấy đọc được; người đi rà "còn nợ gì chưa trả" mở sổ nợ và thấy trống. Cùng họ "hỏi chỗ tiện tay thay vì hỏi chỗ kết luận được ghi".

**Gợi ý vá**

`ops/NO_KY_THUAT.md` NẰM NGOÀI write set (`effective_write_set` có 5 mục, không có nó). Theo §6 *"Chốt phải nằm ngoài write set ⇒ dừng, xuất handoff, mở packet riêng"*, đường đúng là **xuất handoff** nêu tên nợ + điều kiện XONG (branch protection require status job `gate`), rồi xin người giữ kho mở revision thêm sổ nợ vào write set. Việc này chưa làm.

Kèm một chốt RẺ và nằm TRONG write set, đóng phần vô ý của F2': trong `t34` (hoặc ca mới), đòi bước gọi wrapper ở `ci.yml`/`ops-publish-lease.yml` **không có khoá `if:`** — đây là kiểm KHOÁ CẤU TRÚC của YAML, không phải bộ phân tích shell, nên không rơi vào điều kiện dừng §6; và nó đúng thứ reviewer vòng 3 đã đề nghị (*"Fail-closed khi installer có `if:`"*). Kèm đột biến: thêm `if: false` phải giết 1/1.

---

### 3. Giới hạn `t34` được KHAI HẸP HƠN thứ đo được — bốn dạng gọi THẲNG tệp `.py` vẫn lọt, executor chỉ khai một — P2

Docstring `t34` khai đúng một lỗ: *"GIỚI HẠN BẮT BUỘC KHAI: `python -m ops.lease_publish_test` VẪN lọt"*, và tuyên hợp đồng còn lại là *"workflow gọi THẲNG `lease_publish_test.py` thay vì đi qua wrapper"*.

**Bằng chứng đo được.** Thay đúng dòng `run:` của bước gate trong `ci.yml` (bản sao `mut1`), `rc` đọc trực tiếp:

```text
A_python_m                   rc=0  KHONG-DO   lease_publish: 40/40 đạt
B_python3_u_file             rc=0  KHONG-DO   lease_publish: 40/40 đạt
C_bash_c                     rc=1  DO(t34)    lease_publish: 39/40 đạt
D_shebang                    rc=0  KHONG-DO   lease_publish: 40/40 đạt
E_uv_run                     rc=0  KHONG-DO   lease_publish: 40/40 đạt
F_python_X                   rc=0  KHONG-DO   lease_publish: 40/40 đạt
G_thang_python               rc=1  DO(t34)    lease_publish: 39/40 đạt
H_exec_python                rc=1  DO(t34)    lease_publish: 39/40 đạt
```

Nguyên văn từng biến thể: `B` = `python3 -u ops/lease_publish_test.py`; `D` = `./ops/lease_publish_test.py`; `E` = `uv run ops/lease_publish_test.py`; `F` = `python -X utf8 ops/lease_publish_test.py`. **Cả bốn đều là "lời gọi THẲNG tệp `.py`"** — đúng thứ `t34` tự nhận là canh — và không cái nào được khai. Nguyên nhân là `\S*` trong `_CHAY_BO_TEST` không vượt được khoảng trắng, nên bất kỳ CỜ nào chen giữa `python` và đường dẫn cũng làm phép khớp trượt.

Lời khai `python -m` đã được xác nhận (`A`, rc=0) — thật thà, nhưng KHÔNG ĐỦ.

**Invariant bị cắt**

`CLAUDE.md`: *"PHẠM VI TUYÊN BỐ phải bằng phạm vi ĐO ĐƯỢC."* Người đọc `t34` hôm nay tin rằng lời gọi thẳng tệp `.py` bị chặn và chỉ dạng `-m` là ngoại lệ; đo cho thấy chỉ dạng `python <đường-dẫn>.py` **không cờ** mới bị chặn.

**Gợi ý vá — KHÔNG nối regex** (§6 cấm đúng việc đó). Hai đường, chọn một:

1. **Rẻ:** sửa lời khai cho khớp phép đo — nói rõ `t34` chỉ nhận dạng canonical `python|python3|py <đường-dẫn>.py` và liệt kê 5 dạng đã ĐO là lọt (`-m`, cờ chen giữa, shebang trực tiếp, `uv run`, và mọi runner khác).
2. **Đúng doctrine hơn:** đảo thành **DANH SÁCH CHO PHÉP** như `CLAUDE.md` đòi — mọi *lệnh* trong `run` có nhắc `lease_publish_test` phải khớp ĐÚNG một mục trong tập nhỏ canonical (`bash ops/chay_lease_publish_test.sh`, `bash "$NEO/ops/chay_lease_publish_test.sh"`, `test -s …`, `sha256sum …`), ngoài tập đó là ĐỎ. Cách này giết cả `python -m` (chuỗi `lease_publish_test` vẫn nằm trong `ops.lease_publish_test`) lẫn bốn dạng trên, và chi phí báo-thừa (`run: echo lease_publish_test.py` thành đỏ) đã được vòng 3 đo và **chủ ý chấp nhận** (`MENTION_ONLY_RC=1`).

---

### 4. `GOI_WRAPPER` là danh sách cho phép gác một NGHĨA VỤ — viết khác một dấu là nghĩa vụ biến mất — P3

`t35` đòi bước gọi wrapper phải khai `AL_VER` dạng X.Y.Z, nhưng chỉ với bước có phần lệnh **bằng đúng** một trong hai chuỗi trong `GOI_WRAPPER`; không khớp thì `continue`.

**Bằng chứng đo được** (`mut1`, `ci.yml`):

```text
N1_bo_AL_VER                     rc=1   lease_publish: 39/40 đạt ::   ĐỎ  t35_script_cai_actionlint_phai_TU_CHOI_ban_sai,
N2_bo_AL_VER_va_doi_cach_viet    rc=0   lease_publish: 40/40 đạt ::
```

`N2` = bỏ `env: AL_VER` **và** đổi `bash ops/…` thành `bash ./ops/…`. Cùng một lời gọi, cùng một thiếu sót, khác đúng hai ký tự — và chốt im.

**Invariant bị cắt**

Danh sách CHO PHÉP chỉ đúng khi thứ ngoài danh sách bị **TỪ CHỐI**. Ở đây nó gác một *nghĩa vụ*, nên ra ngoài danh sách = **được miễn**, tức fail-OPEN theo đúng chiều ngược với ý định. Hậu quả không im lặng (installer trả rc=2 lúc chạy thật), nên P3; nhưng đây đúng hình dạng lỗi kho đã trả giá nhiều lượt.

**Gợi ý vá:** nhận diện bước gọi wrapper theo *có nhắc `chay_lease_publish_test.sh` trong một lệnh thực thi*, rồi ĐỎ nếu phần lệnh không nằm trong `GOI_WRAPPER` — đảo nhánh `continue` thành nhánh `loi.append`. Kèm đột biến `bash ./ops/…` phải giết 1/1.

---

### 5. `mkdir -p "$AL_DICH"` hỏng thoát ra rc=1, đụng đúng mã thoát của chính bộ test — P3

Đầu `ops/cai_actionlint.sh` khai *"Ma thoat — RIENG BIET de nguoi goi (va `t35`) khang dinh duoc LY DO tu choi"* rồi liệt kê 2–9. `mkdir -p "$AL_DICH"` không có `|| loi N`, nên nó rơi vào `set -e`.

**Bằng chứng đo được** (`AL_DICH` trỏ một TỆP thường; chạy dưới root nên chốt quyền 555 không đo được, phải dùng cách này):

```text
AL_DICH-la-TEP rc=1 marker=KHONG
mkdir: cannot create directory '…/wtest/la-tep': File exists
```

`rc=1` cũng chính là mã của `lease_publish_test.py` khi có ca đỏ. Người gọi (kể cả `ops-publish-lease.yml`) không phân biệt được "cổng đỏ" với "không tạo nổi thư mục cài".

**Gợi ý vá:** `mkdir -p "$AL_DICH" || loi 4 "khong tao duoc thu muc cai '$AL_DICH'"` (hoặc một mã mới), kèm ca khoá.

---

## Các hướng đã ĐO và SẠCH — nói rõ để im lặng không bị đọc thành chưa thử

**Nền** (`export PATH="$PWD/../bin:$PATH"`, `rc` trực tiếp, không `tail`/`head`):

```text
lease_publish: 40/40 đạt
SUITE_RC=0
ACTIONLINT_RC=0        # actionlint .github/workflows/*.yml — CẢ 5 tệp
PYCOMPILE_RC=0         # python3 -W error::SyntaxWarning, lease_publish_test.py
PYCOMPILE2_RC=0        # …và lease_publish.py
```

`bash ops/chay_lease_publish_test.sh` chạy THẬT end-to-end (tải gói từ mạng, cổng băm qua): `WRAPPER_RC=0`, `40/40`.

**Trục 1 — wrapper có tách rời được không.** Không tách được ở mọi đường tôi dựng nổi; marker của bộ test không bao giờ xuất hiện khi installer hỏng:

```text
AL_DICH-la-TEP   rc=1  marker=KHONG    (mkdir hỏng)
AL_VER-hong      rc=2  marker=KHONG
goi-thieu        rc=4  marker=KHONG
bam-lech         rc=9  marker=KHONG
PATH-co-ban-sai  rc=0  marker=CO       (mồi 0.0.0 đứng trước; which() vẫn trỏ vào AL_DICH)
```

**Trục 2 — `exec` giữ rc.** Đo thẳng bằng bộ test giả tự chọn mã thoát:

```text
rc0 rc=0 · rc1 rc=1 · rc23 rc=23 · rc143 rc=143 · rc255 rc=255   (marker=CO ở cả năm)
```

Đột biến nuốt rc bị giết:

```text
M4b_nuot_rc_bang_||exit0           rc=1  39/40  ĐỎ t40
M4c_pipeline_nuot_rc               rc=1  39/40  ĐỎ t40
```

(Đột biến `; exit 0` của tôi SỐNG SÓT nhưng đó là đột biến hỏng, không phải test yếu: `set -e` thoát ngay tại lệnh thất bại nên `exit 0` không bao giờ chạy tới. Ghi ra vì "đột biến sống sót ≠ mã sai".)

**Trục 3 — mã 10/11.** Cả hai đều đúng ca, và không ca nào rơi vào oan:

```text
goi chi co actionlint.exe (POSIX) -> rc=10  "installer xanh nhung PATH khong co actionlint"
PATH khong co python/python3/py   -> rc=11  "khong tim thay python, python3 hay py"
```

**Trục 4 — ba nhánh python.** Đo CẢ BA bằng cách dựng `PATH` tối giản (`env -i`), không đọc code:

```text
nhanh python   rc=0 marker=CO    (nền mặc định)
nhanh python3  rc=0 marker=CO    (PATH không có `python`)
nhanh py -3    rc=0 marker=CO    (PY_LAUNCHER_DUOC_GOI xuất hiện đúng 1 lần)
không nhánh nào rc=11
```

Không nhánh nào "được đếm ĐẠT mà không đo": wrapper không có đường thoát 0. Lưu ý phạm vi: `t40` trên MỘT host chỉ chạy được nhánh của host đó — hai nhánh kia là **chưa có ca**, không phải ca rỗng.

**Trục 5 — magic bytes.** Ngoài 3 chữ ký ZIP + gzip, mọi thứ khác fail-close có thông điệp phân biệt được:

```text
ok.zip        rc=0
empty.zip     rc=5  giai nen zip that bai
ba-byte       rc=5  khong nhan dien duoc loai goi tu magic bytes '504b03'
zip-cut       rc=5  giai nen zip that bai
rac           rc=5  … '6b686f6e'
rong          rc=5  … ''
plain.tar     rc=5  … '61637469'
plain.tar.bz2 rc=5  … '425a6839'
plain.tar.xz  rc=5  … 'fd377a58'
THIEU_OD      rc=5  KHONG DO DUOC loai goi: thieu `od`
THIEU_SHA     rc=8  KHONG DO DUOC bam: thieu ca `sha256sum` lan `shasum`
```

Không định dạng nào bị từ chối OAN so với artefact chính thức (upstream chỉ phát hành `.tar.gz` và `.zip`).

**Trục 6 — `t40` nhánh POSIX có răng.** Năm đột biến, mỗi cái giết 1/1, đều trên bản sao tạm:

```text
M3_bo_goi_installer     rc=1 39/40  ĐỎ t40
M5_khong_cap_PATH       rc=1 39/40  ĐỎ t40
M8_chay_truoc_cai_sau   rc=1 39/40  ĐỎ t40
M4b / M4c (nuốt rc)     rc=1 39/40  ĐỎ t40
M6_bo_doi_chieu_ban_ghim rc=1 38/40 ĐỎ t35, t40
M1_suffix_thay_magic    rc=1 39/40  ĐỎ t39
KHOI_PHUC_nen           rc=0 40/40
```

Đồ mồi mô phỏng **TRẠNG THÁI** (một `actionlint` 0.0.0 thật nằm trên `PATH` từ đầu), và stub đòi `shutil.which()` phải trỏ vào TRONG `AL_DICH` — không diễn kịch bản theo lượt.

**Ba finding vòng 3 — dựng lại nguyên văn trên head:**

- **F3 đóng.** Cùng byte ZIP dưới ba tên: `zipnodot rc=0` · `archive.ZIP rc=0` · `archive.zip rc=0` (vòng 3: `5 · 5 · 0`).
- **F2 hết đường cũ.** Không còn bước installer riêng để `if: false`; phần dư đã nói ở finding 2.
- **F1** — xem finding 3.

**Hai phản chứng vòng 2 vẫn ĐỎ** (§5):

```text
V2a_installer_job_khac         rc=1  39/40  ĐỎ t34   (actionlint_rc=0)
V2b_installer_sau_selftest     rc=1  39/40  ĐỎ t34
```

**`t34` không mắc bệnh `t24`:** nó neo `HERE.parent/.github/workflows` (đúng gốc kho, không `parent.parent`), và nhánh "không thấy thì thôi" có chốt `bang(not (HERE.parent/".git").exists(), …)`.

**diff.patch trung thực:** `sha256(diff.patch) == sha256(git diff a09aae62 HEAD)` = `9040854e5914b190aea31ae389dbbae67ca7808adee312e41ec8e98c00987d4d`, `diff -u` không một hunk lệch. Write set đúng 5 tệp đã khai, không tệp thứ sáu. `base` là tổ tiên của `head`. Số ca 38 → 40, không tụt.

**Không sinh nợ deploy:** `ops` và `.github` đều nằm trong `_RELEASE_EXCLUDE_DIRS` (`['.claude', '.codex', '.git', '.githooks', '.github', …, 'ops', …]`), và `grep -c "ops/" RELEASE_MANIFEST.json` = `0` — tệp wrapper mới không đụng manifest/golden, nên không tái lập sự cố r238 cho phiên sau.

## Chưa đo được — ghi là GIẢ THUYẾT, không ghi là sạch

- **Nhánh Windows của `t40`** và lượt `workflow_dispatch` trên `windows-latest` (run `32395054494`): sandbox này không có Windows, và tôi không đọc ra ngoài sandbox. Đọc mã thì nhánh ấy **fail-close đúng hướng** (`bang(actionlint_ngoai and …endswith(".exe"), "[Windows] KHÔNG ĐO ĐƯỢC…")` — ĐỎ chứ không `return`), và nó đóng gói lại chính PE vừa được wrapper ngoài cài, tức trạng thái thật. Nhưng đó là ĐỌC, không phải ĐO. Kết luận "cả hai job success" tôi lấy nguyên từ packet, không tự xác minh.
- **Branch protection / required status check** ngoài kho: không kiểm được từ đây.

## Chốt cây — và một lời khai

```text
git -C kho status --short
# rỗng
HEAD=e071e0aae6bdc4d270a42fbc534ad3f05dcba0fa
TREE=cd288cedc82ab1c54efefc7e360ea6db0ffae133
SUITE_CUOI_RC=0   ACTIONLINT_CUOI_RC=0
```

**Khai thẳng:** giữa phiên tôi dựng cây `base` bằng `git --git-dir=<gitdir thật> --work-tree=<bản sao> checkout a09aae62 -- .` — lệnh ấy ghi vào **INDEX của worktree `kho`** (`status` hiện `MM` trên 4 tệp). Không tệp nào trong cây làm việc bị đổi và HEAD không đổi; tôi khôi phục bằng `git -C kho reset -q HEAD -- .` và kiểm lại sạch, rồi dựng lại cây base bằng `git -C kho archive` (thuần đọc) và đo lại từ đầu. Mọi số liệu ở trên đo trên cây base dựng bằng `archive`. Ghi ra vì "chốt sạch cây" chỉ có nghĩa khi cả lần lỡ tay cũng được khai.

VERDICT: changes_requested
Reviewed commit: e071e0aae6bdc4d270a42fbc534ad3f05dcba0fa
