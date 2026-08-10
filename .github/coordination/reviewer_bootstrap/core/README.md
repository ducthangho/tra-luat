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
