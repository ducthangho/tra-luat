# Reviewer bootstrap core — RA-01 (wp77)

Lõi controller **không đặc quyền** cho Mission #76. Packet này KHÔNG giữ credential, KHÔNG gọi
model, KHÔNG chạm GitHub thật, KHÔNG dựng sandbox và KHÔNG dựng gateway — sandbox/oracle thuộc
RA-02, credential gateway thuộc RA-03.

Nằm trong `.github/**` nên **ngoài gói phát hành** (`_RELEASE_EXCLUDE_DIRS`): không ăn trần 200
tệp, không kéo `RELEASE_MANIFEST.json` vào write set.

## Chạy

```
python3 controller.py schema     # schema operation máy đọc được
python3 controller.py coverage   # phạm vi phủ của tripwire - CẢ phần KHÔNG phủ
python3 controller.py call --op read_issue --params '{"repo":"ducthangho/tra-luat","issue_number":77}'
python3 controller.py produce --out RUNDIR --run-id r1
python3 controller.py verify --root RUNDIR
python3 controller.py selftest   # đòi N/N với hai số BẰNG NHAU
```

rc quy ước: `0` ok · `2` bị TỪ CHỐI (op lạ, tham số sai, payload mang credential) · `3` verify đỏ ·
`64` sai cách dùng.

## Thành phần

| tệp | bất biến nó giữ |
|---|---|
| `operations.py` | tập operation ĐÓNG + schema tham số; từ chối ĐÍCH DANH; quét bề mặt credential trong payload |
| `fake_github.py` | store giả toàn bộ trong tiến trình; mô phỏng 403/404/409/rate-limit; dispatch qua bảng tường minh |
| `ledger.py` | idempotence theo `reconcile_key`, bền qua ranh giới tiến trình, không mang timestamp |
| `artifacts.py` | manifest + locator BỀN ràng buộc trong `run_root` + SHA-256 từng file + sidecar |
| `guards.py` | tripwire env/subprocess/mạng, mỗi cái khai `COVERAGE` gồm cả `not_covered` |
| `selftest.py` | phản chứng chạy được cho từng acceptance, và đối chứng dương cho từng tripwire |

## Generation 2 — năm finding của audit g1 đã đóng bằng test hồi quy

Audit g1 ([verdict](https://github.com/ducthangho/tra-luat/pull/78#issuecomment-5236513526)) không
dừng ở việc đọc code: nó **chạy được** năm thủ thuật vượt rào. Mỗi thủ thuật nay là một test mang
đúng ID finding trong tên, và test đó ĐỎ nếu lỗ hổng quay lại.

| finding | lỗ hổng g1 | đóng bằng | test hồi quy |
|---|---|---|---|
| `wp77-g1-spec-01` | `OPERATIONS` là dict công khai khả biến + dispatch `getattr(self, "_op_" + name)` ⇒ đăng ký op lúc chạy và **gọi được** | proxy chỉ đọc tới tận lá · frozenset chụp lúc import gắn vào tham số mặc định · phát hiện lệch bảng · bảng dispatch tường minh có kiểm chẵn lẻ lúc import | `ra01_regression_spec01_*` (4) |
| `wp77-g1-spec-02` | `subprocess.run(..., env=None)` cho child kế thừa `GH_TOKEN` mà `sensitive_reads()` vẫn rỗng | `EnvGuard` vá `subprocess.Popen`: **ghi nhận** phơi nhiễm và **scrub** biến nhạy cảm khỏi env của child · `EnvGuard(inject=)` bỏ hẳn kiểu đọc-trước-khi-cài-guard | `ra01_regression_spec02_*` (4) |
| `wp77-g1-sec-01` | locator `../escaped.txt` ghi file NGOÀI `run_root`, `verify()` vẫn `ok=true` | `safe_locator()` chặn tuyệt đối/`..`/`.`/`\`/symlink + kiểm containment; áp dụng ở CẢ lúc ghi lẫn lúc kiểm; `verify()` chỉ hash **tệp thường** (`lstat`) | `ra01_regression_sec01_*` (4) |
| `wp77-g1-sec-02` | `socket.socket` cache trước guard vẫn tạo được socket; scanner mù `importlib`/`subprocess` | vá `__init__` của chính lớp socket · scanner bắt import động, `subprocess` với argv[0] hằng, `os.system/popen` · **claim bị thu hẹp**: `COVERAGE.not_covered` khai bằng máy, ranh giới thật là netns | `ra01_regression_sec02_*` (4) |
| `wp77-g1-sec-03` | `payload={"token": ...}` được persist nguyên vào ledger | chọn đường **(b)** — ràng buộc payload: quét đệ quy khoá + hình dạng giá trị, **từ chối** đích danh (không scrub) | `ra01_regression_sec03_*` (4) |
| `wp77-g1-dup-01` | seed fake-store chép đôi ở `controller.py` và `selftest.py` | một nguồn duy nhất `fake_github.seeded_store()` | `ra01_seed_fixture_has_exactly_one_definition` |

## Vòng audit thứ hai — sáu finding độc lập trên head `dc0dbf42`

Vòng một sửa đúng chỗ nhưng chưa đủ sâu. Sáu lỗ tiếp theo, mỗi cái có test `ra01_regression_a2_*`
và **counter-mutant đã chạy** chứng minh test biết ĐỎ.

| # | lỗ hổng | vì sao nó tồn tại | đóng bằng |
|---|---|---|---|
| 1 | manifest reseal `entries: [], required_categories: []` vẫn `ok=true` | `verify()` hỏi CHÍNH tài liệu đang bị kiểm xem nó có nghĩa vụ gì | nghĩa vụ lấy từ hằng `REQUIRED_CATEGORIES` của module; validate schema; đòi `verified_files > 0` |
| 2 | `carrier.txt:payload` (NTFS ADS), `NUL`, `CON` lọt | chỉ nghĩ tới `..` và đường tuyệt đối, quên ngữ nghĩa riêng của Windows | chặn `:`, tên thiết bị DOS (kể cả có đuôi/chấm/space cuối), ký tự điều khiển; `fstat` sau `os.open` |
| 3 | test ZERO-credential **false-green** | guard vừa phát hiện vừa scrub ⇒ child không bao giờ có marker để mà đọc | recorder cài **trong child** trước khi import controller, marker vẫn hiện diện; thêm `scrub_child_env=False` tách phát hiện khỏi scrub |
| 4 | scanner lọt `import subprocess as sp` | so tên gọi theo chữ, không canonical hoá | bảng alias cho cả `import X as Y` lẫn `from X import f as g` |
| 5 | chặn nhầm `session_id`, `authorization_url`, `token_budget`, `author`, `cookie_policy` | regex substring không neo | quyết theo **từ cuối** của khoá; ràng buộc được công bố trong `schema()` |
| 6 | `post_verdict` nhận `reviewed_sha` bất kỳ | khai `type: string` là chưa đủ | format `git_oid` — đúng 40 hex thường; viết tắt cũng bị từ chối |

Kèm một lỗi tương thích P2: `os.environ.copy()` ném `AttributeError` khi recorder đang thay chỗ —
`MutableMapping` không cấp `.copy()`, mà thư viện con hay gọi đúng thứ đó trước khi tạo subprocess.
Nay `.copy()` hoạt động và **được ghi nhận như một lần đọc** nếu có biến nhạy cảm.

Về `52/53` trên Windows: nguyên nhân là **fixture**, không phải bất biến — `os.symlink` đòi quyền
riêng. Test đó nay báo `[SKIP]` có nêu lý do (không phải `[FAIL]`, cũng không phải im lặng thành
`passed`), và bất biến no-follow vẫn được kiểm ở mọi nền bằng
`ra01_regression_sec01_verify_refuses_non_regular_file_portable` dùng thư mục thay cho symlink.

## Vòng audit thứ ba — năm finding spec trên head `c4784728`

Suite `68/68` mà spec vẫn FAIL. Bài học của vòng này: **sửa một hướng của bộ lọc thì mở hướng kia**.

| # | lỗ hổng | vì sao | đóng bằng |
|---|---|---|---|
| 1 | `authorization_header`, `client_secret_value` LỌT; `requested_tokens`, `remaining_tokens` bị CHẶN NHẦM | quyết theo mỗi TỪ CUỐI — hỏng cả hai hướng cùng lúc | quyết theo TOÀN BỘ tập từ với ba vai: **danh từ bí mật** · **đơn vị đo** (biến `token` thành số) · **vật chứa** (`header`/`value`/`blob` — giữ giá trị thật, thắng mọi thứ). Thêm value-shape `Bearer`/`Basic` |
| 2 | `reviewed_sha` nhận `40hex + "\n"` và persist nguyên newline | `$` trong Python khớp cả **trước** newline cuối chuỗi, cộng `.match()` | `\Z` + `fullmatch`. Cùng lỗi ở `_SHA256_HEX` của manifest entry |
| 3 | `builtins.__import__('requests')` và `runner = sp.run; runner([...])` cho `offenders=[]` | canonical hoá alias chỉ phủ import, không phủ gán biến; hai tên cho cùng một hàm | strip tiền tố `builtins.`, theo dõi **một tầng alias qua biến** (hội tụ 3 lượt). Phần còn lại khai trong `STATIC_SCANNER_COVERAGE.not_covered` và in ra qua `controller.py coverage` |
| 4 | `manifest.json`/`manifest.sha256` mở thẳng, không no-follow; năm category cùng trỏ MỘT locator vẫn `ok=true` | containment áp cho entry mà không áp cho tài liệu mô tả chúng; đếm entry ≠ đếm object rời nhau | `_read_regular` (islink + `fstat` regular) cho chính manifest/sidecar; `_open_regular_for_write` lúc ghi; **từ chối locator trùng** ở cả `add()` lẫn `verify()` |
| 5 | `os.environ \| {}` ném `TypeError` dưới guard; `os.environb` ngoài tầm recorder | `MutableMapping` không cấp `__or__`; POSIX có mapping thứ hai vào cùng environment | `__or__`/`__ror__`/`__ior__`; bọc luôn `os.environb`, ghi vào **cùng một sổ** |

## Điều lõi này KHÔNG hứa

Ba tuyên bố bị **thu hẹp có chủ đích** so với g1, và mỗi cái có test đòi phần "không phủ" phải
khác rỗng — để không ai lặng lẽ nâng claim trở lại:

- `NetworkGuard` là **tripwire, không phải sandbox**. Nó không phủ `_socket` mức C, tiến trình con,
  binary tự ra mạng, `ctypes`/syscall thô. Ranh giới thật của "không có lối ra mạng" là
  **network namespace** (`unshare -n`).
- Bộ quét tĩnh không thấy import dựng động từ biến, argv dựng động, `eval`/`exec`.
- `EnvGuard` canh **environment**, không canh credential nằm trong tệp trên đĩa, và không phủ
  `os.execve`/`posix_spawn` gọi thẳng.

Một tripwire khai đúng giới hạn của mình vẫn dùng được. Một tripwire tuyên bố phủ mọi thứ thì
không — đó là bài học đã trả giá ở #54 khi output tự khai `168/168 dat` trong lúc chạy trần.
