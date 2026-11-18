# WP1319 r2 — Review độc lập, chỉ đọc

```
verdict: approve_scoped
packet: 1319 · revision 2 · generation 1 · review_class: sensitive
spec: ops/specs/wp1319-r2.md  sha256 d1c594aa9034b884e8f521c75ea31ae456a2d0f828e554dd11518706efd2cb9d  (đo lại: KHỚP)
lease: ops/leases/wp1319-r2-g1-operator.yaml  sha256 236a7d8b9fcd454d300f2e3d58dc7535d6e454f804b921eded1820e3988e8fde
bundle: ASUS D:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\wp1319-r2\freeze\wp1319-r2-evidence.zip
        sha256 74f02bd3009861759d764a9a23b539e67d65bc22a1ed75a4be706e05cf313c2f  (certutil: KHỚP lời khai và tệp .sha256)
nguồn mã: recovery-native-acceptance-20261113.zip  sha256 97e9b78f62a3bd73c3a2550309e44e2e25a956367f2d7b3d9cf83de781a3d8dc  (certutil: KHỚP)
P1: 0 · P2: 0 · P3: 7
```

`approve_scoped` có nghĩa là bốn bộ test chạy đúng mã P4, có `rc` và tệp kết quả có băm, và đủ điều kiện để nâng
§11 #10 từ `not_evidenced` lên `partial`. Kết quả này **chỉ** có giá trị trong phạm vi fixture / inert boundary
(xem bảng tác động). Không hàng nào được nâng thành `real_os` cho Proxima/Electron.

## 1. Toàn vẹn

| Kiểm | Kết quả |
|---|---|
| sha256 zip | `74f02bd3…3c2f`, khớp lời khai và `wp1319-r2-evidence.zip.sha256` |
| Số mục trong zip | 33 = `MANIFEST.json` + 32 tệp. MANIFEST liệt kê 32 tệp |
| Từng mục so MANIFEST (size + sha256, băm trong bộ nhớ) | **32/32 khớp**, 0 thiếu, 0 thừa. `MANIFEST.json` trong zip = bản trên đĩa (`362916fc…8834`) |
| `code/`, `parent/` trong zip so `export-manifest.json` của zip P4 | **17/17 tệp `.py` khớp** (bản normal hoặc induced; `induced_sequence_20261113.py` chỉ có ở bản induced). 3 tệp không có trong P4 đều là **đầu ra test**: `result-win32.json` (do `test_recovery.py` ghi), `native-lock-test-result.json` và `own-hostlock-smoke.txt` (do `test_native_lock.py` ghi, `R=Path(__file__).parent`). Không có tệp nào không truy được nguồn |
| Bản làm việc trên đĩa (`W\code`, `W\parent`) lúc review | 18/18 tệp băm bằng đúng mục tương ứng trong zip |
| `r2_driver.py`, `r2_freeze.py` trên đĩa | `40a977a4…76dd`, `5bf91bfa…4c68` = bản `evidence/script-*` trong zip. mtime 08:51:04Z và 08:53:09Z, đều **trước** lúc chạy (08:51:16Z) và lúc đóng băng (08:53:54Z) |
| Thư mục raw `recovery-upload-20261113\` | Không có mục nào sửa ngày 18/11, không có `__pycache__`, không có thư mục con lạ. Chỉ đo được bằng mtime |
| `W` | Không có thư mục con nào ngoài `code evidence freeze parent tools`. Không có `__pycache__`, nên không có rủi ro `.pyc` cũ thay mã nguồn |

## 2. Từng bộ test

Python: `3.13.1 (tags/v3.13.1:0671451 …) [MSC v.1942 64 bit (AMD64)]`, `C:\Python313\python.exe`, `Windows-11-10.0.26300-SP0`
(dòng `start` của `r2-progress.jsonl`), khớp spec §2. Lệnh: `sys.executable -X utf8 <test>`, cwd `W\code`, mỗi tệp một
tiến trình, timeout 900 s. Không có lượt chạy lại (một dòng `start`, mỗi test một dòng `M2/M3`).

| Test | rc | Dấu hiệu dương | stderr | sha256 nguồn | Tệp kết quả (sha256) |
|---|---|---|---|---|---|
| `test_recovery.py` | 0 | dòng cuối stdout `{"passed": true, "cases": 19, "platform": "win32"}` | 0 byte | `f91cd0da732a0d3cf1e8914af2406ba94f98e1d0dd87400554110efb9927ba19` | `result-win32.json` `f616304a…029f` (bản ở `evidence/` và `code/` bằng nhau); stdout `5f1fa822…a1c` |
| `test_native_lock.py` | 0 | `{"passed": true, "cases": 4}` | 0 byte | `6d8e136ec0d8e65332f4de7a1aad8c411106f32b755e1e02b8eb89c6abb9c33a` | `code/native-lock-test-result.json` `51c4fa8e…680c` (4 check); stdout `22dedf45…f928` |
| `test_operator_safety.py` | 0 | `"passed": true`, `"platform": "win32"`, 4 check | 0 byte | `9159f5ebb8ad2e0075b6704f0cfcf3e3b95aa334a53088820340ca87dd607405` | stdout `82953f1a…f019` |
| `test_dependency_pins.py` | 0 | `"passed": true, "known_exact_sdists": 7, "negative_cases": 3` | 0 byte | `1849a4de22fa6f5b0e28572f1f3f18a609d8d3686886b0b14f273454055679ba` | stdout `d9d1d75f…5151` |

Module được test import (băm trong zip = P4): `operator_safety.py` `f5a63054…2308`, `recover_matching_data.py`
`e2625de7…9e6f`, `run_activation.py` `6004fcea…417c`, `prior_run_activation.py` `71ac0c1a…1362`,
`dependency_pins.py` `36bca35a…0e`. `parent/` không được test nào import.

`result-win32.json` đạt đủ tiêu chí M2: `"platform": "win32"`, liệt kê 19 ca (gồm `native locked profile rejects
rename and preserves both data sets` và `native simultaneous owner denied; own lock released after context`), và
`source_sha256` của 5 tệp (`run_activation`, `recover_matching_data`, `operator_safety`, `prior_run_activation`,
`test_recovery`) bằng đúng M1 và P4. Tệp này mới sinh trong lượt: M1 chỉ có 15 tệp `.py`, M4 ghi nó là `new`, raw không có.
Trong mã, `case()` chỉ thêm một dòng khi ca chạy xong không lỗi, và tệp chỉ được ghi sau ca cuối. Nên 19 dòng cùng `rc=0`
nghĩa là cả 19 ca đã chạy và đạt. `"passed": true` được viết cứng, nhưng chỉ tới được khi không ca nào lỗi.

## 3. Phân loại từng ca (đọc mã trong zip)

Từ ngữ: **fixture** = thư mục tạm, dữ liệu tổng hợp, ứng dụng là callback trơ, lỗi tiêm bằng cách thay hàm.
**real_os (nguyên thủy)** = gọi API Windows thật trên tệp tạm hoặc tệp riêng của test, không có Proxima/Electron.

| # | Ca | Lớp | Cơ chế |
|---|---|---|---|
| 1 | success | fixture | copytree/rename thật trên thư mục tạm; restart là callback |
| 2 | busy | fixture | `owned_closed=lambda: False` ⇒ `OWNERSHIP_NOT_VERIFIED_CLOSED`, từ chối trước khi chép. **Không phải "máy bận"** |
| 3 | disk-full | fixture | `disk_usage` thay bằng `free=0` ⇒ `INSUFFICIENT_MATCHING_DATA_RESTORE_RESERVE`. Không có ổ đĩa đầy thật |
| 4 | partial-copy | fixture | `copytree` thay bằng hàm ghi `incomplete` rồi ném `OSError` |
| 5 | promotion-failure | fixture | `rename` thay bằng hàm ném `PermissionError` khi đưa staging lên. Sau lỗi: `profile` vắng, bản hiện tại nằm ở `profile-after-repaired`, staging đúng bản sao lưu |
| 6 | corrupt-backup | fixture | sửa tệp sao lưu ⇒ `BACKUP_MANIFEST_MISMATCH` |
| 7 | corrupt-staging | fixture | `copytree` làm hỏng staging ⇒ `RESTORE_STAGING_MANIFEST_MISMATCH` |
| 8 | existing-destination | fixture | đích đã có ⇒ `RECOVERY_DESTINATION_EXISTS` |
| 9 | ownership-changes | fixture | `owned_closed` đúng lần đầu, sai lần sau ⇒ dừng sau khi chép, trước khi rename |
| 10 | restart-failure | fixture | dữ liệu đã khôi phục, callback restart ném lỗi ⇒ `passed` false, chỉ khôi phục một lần |
| 11–13 | prior-source / new controller failure / success | fixture (AST) | `exec` khối `try` cuối của `prior_run_activation.py`/`run_activation.py` với môi trường trơ (`run` giả, `sha` giả, khóa là tệp tạm mở `r+b`) |
| 14 | intentional interruption | fixture | `KeyboardInterrupt` không bị `except Exception` bắt ⇒ không khôi phục, không restart |
| 15 | wrong profile binding | fixture (AST) | `RECOVERY_PATH_BINDING_MISMATCH` trước mọi lần chạy |
| 16 | dual failure + giữ khóa chủ không rõ | fixture (AST) | lỗi health tiêm + `owned_active_after_cleanup=None` ⇒ lỗi kép, `host_lock_released: false`, tệp khóa tạm còn `owned` |
| 17 | dual failure message chain | fixture | `run_repaired_then_restore` với `owned_closed=False` ⇒ cả hai nguyên nhân, `__cause__` là lỗi gốc |
| 18 | native locked profile | **real_os (nguyên thủy)** | `CreateFileW(GENERIC_READ, FILE_SHARE_READ, OPEN_EXISTING)` trên `profile/state.txt` tạm. Handle không có `FILE_SHARE_DELETE` nên rename thư mục thất bại thật, `winerror ∈ {5, 32}`. Cả ba bộ dữ liệu giữ nguyên. Handle do chính tiến trình test giữ, và `owned_closed` được giả là `True` |
| 19 | native simultaneous owner | **real_os (nguyên thủy)** | `exclusive_host_lock` (`CreateFileW(GENERIC_READ\|WRITE, FILE_SHARE_READ, OPEN_EXISTING, FILE_FLAG_OPEN_REPARSE_POINT)`) trên tệp tạm. Lần mở thứ hai trong cùng tiến trình bị từ chối, tiến trình con mở `r+b` gặp `PermissionError`, nhả xong thì chủ sau lấy được |
| — | `test_native_lock.py` (4 check) | **real_os (nguyên thủy)** | Cùng `exclusive_host_lock`, trên `code\own-hostlock-smoke.txt`. Có `assert COMPUTERNAME=='ASUS-LAPTOP'`. Không đụng `D:\tl-win\KHOA.txt` |
| — | `test_operator_safety.py` (4 check) | fixture + nguyên thủy OS | allowlist biến môi trường (thuần), manifest trên thư mục tạm, symlink thật bị từ chối, `python -O` bị chặn bằng tiến trình con. Tự ghi `"Windows_native_lock_and_activation": "not run here"` |
| — | `test_dependency_pins.py` | tĩnh / trơ | bảng ghim 2 wheel + 7 sdist, 3 ca âm. Không mạng, không build |

`real_application_invocations: 0`. Scope do chính mã ghi: *"actual controller main AST and real owned filesystem, inert
application boundary; not Electron, NSIS, cross-version migration or live ASUS proof"*.

## 4. Tác động lên các hàng

| Hàng | Trước r2 (RAW-1311) | Sau r2 | Còn thiếu |
|---|---|---|---|
| §11 #7 máy bận / khóa trùng | partial: dual-lock `real_os` (smoke 12/11, ngoài zip, KHONG_do_duoc băm); busy→hoãn not_evidenced; khóa trùng của updater not_evidenced | **partial, không đổi mức.** Vế khóa trùng của primitive operator: `real_os (nguyên thủy)` **có raw đóng băng và băm** (`test_native_lock` 4/4, ca 19), mạnh hơn smoke ngoài zip. Vế "bận ⇒ từ chối" ở mức khôi phục dữ liệu: `passed_fixture_scope` (ca 2, 16) | **Bận ⇒ hoãn**: not_evidenced. Không có mã hoãn, chỉ có dừng fail-closed. `assert lock.tell()==0,'HOST_BUSY'` ở `run_activation.py:23` nằm **ngoài** khối `try` mà ca AST chạy, nên chưa từng kích hoạt. Khóa trùng của chính Proxima/electron-updater: not_evidenced. Test không đụng `KHOA.txt` thật |
| §11 #9 khôi phục binary + dữ liệu | partial: dữ liệu `real_os` (7957 tệp); binary yếu (chạy lại thư mục baseline song song) | **partial, không đổi mức.** Thêm vế âm của giao dịch khôi phục dữ liệu ở `passed_fixture_scope` (ca 3–10, 14, 17), ngữ nghĩa khôi phục đúng một lần ở controller AST (ca 11–13, 15, 16), và một ca khóa tệp `real_os (nguyên thủy)` (ca 18) | Khôi phục binary tại chỗ; khôi phục trên profile Proxima thật khi có lỗi (ngoài ca tiêm health của P4); migration giữa phiên bản |
| §11 #10 file khóa / đĩa đầy / rollback thất bại | **not_evidenced** (chỉ có mã test, không có tệp kết quả) | **partial.** File khóa: `real_os (nguyên thủy)` trên dữ liệu tổng hợp (ca 18). Đĩa đầy (kiểm dự trữ): `passed_fixture_scope` (ca 3). Chép dở: `passed_fixture_scope` (ca 4). Đưa staging lên thất bại: `passed_fixture_scope` (ca 5). Rollback thất bại: `passed_fixture_scope` (ca 10, 16, 17) | Ổ đĩa đầy thật; Proxima/Electron thật giữ khóa profile; rollback thất bại trong một lượt kích hoạt native; NSIS |
| §11 #6 vế âm (artifact sai/hỏng) | not_evidenced | **không đổi.** r2 không có ca nào đưa artifact sai vào updater | Như spec §4 |
| §11 #8 promotion fence hai máy | not_evidenced | **không đổi** | Như spec §4 |
| U4 nhánh có bản mới hơn · U8 đăng nhập · NSIS · migration | partial / not_evidenced | **không đổi** | Như spec §4 |

Với F1 của RAW-1311: phần §11 #10 đã có raw chạy native kèm `rc` và tệp kết quả có băm, nên được phép nâng lên
`partial` trong phạm vi fixture. Phần §11 #6 của F1 vẫn đứng nguyên, vì r2 không đo nó.

## 5. Ràng buộc khi ghi MATRIX (điều kiện của approve_scoped)

1. Ca tên `busy` trong `result-win32.json` là "chưa xác minh chủ sở hữu đã đóng" ở tầng khôi phục dữ liệu. Không được
   dùng nó để nâng vế "máy bận thì hoãn" của §11 #7.
2. Ca 18 và 19 cùng `test_native_lock` là `real_os` cho **primitive** khóa/tệp của Windows trên tệp tạm. Không phải
   `real_os` cho Proxima, Electron hay electron-updater. Ca 18 giả `owned_closed=True`, và handle khóa do chính test giữ.
3. "Đĩa đầy" là kiểm dự trữ với `disk_usage` bị thay, không phải ổ đầy thật. Hãy ghi đúng như vậy.

## 6. Phát hiện

**P1: không có.**

**P2: không có.**

**P3:**
- **P3-1 (lệch chữ của spec M4).** M4 nói "chỉ được có thêm tệp `result-*.json` mới". Lượt chạy thêm hai tệp khác,
  `code/native-lock-test-result.json` và `code/own-hostlock-smoke.txt` (0 byte, tức đã nhả sạch). Cả hai do mã đóng băng
  `test_native_lock.py` ghi vào `Path(__file__).parent`. Driver có ghi chúng vào `new` của M4 nhưng không gắn cờ. Không
  có tệp mã nào đổi. Không ảnh hưởng kết luận; spec đã viết hẹp hơn hành vi của mã.
- **P3-2 (kiểm tải + khóa không có trong bundle).** Spec §2 đòi kiểm tải trước khi chạy và ghi lại tiến trình của phiên
  khác (ADR-0057 §4), và đòi khóa `KHOA.txt`. Bundle đóng băng không có bản ghi nào cho hai việc này. `do-luong.csv` chỉ
  có một dòng của phiên lúc `2026-11-18T08:54:52Z`, tức lúc nhả. `KHOA.txt` hiện 0 byte, sửa lúc 08:54:52Z (đã nhả). Việc
  lấy khóa và kiểm tải: **KHONG_do_duoc** từ bundle. Không ảnh hưởng kết luận test, vì các ca chạy trên thư mục tạm và
  tệp riêng của test, trong khoảng 2,7 s. Nếu transcript của operator có các bước này, nên chép vào `ops/acceptance/wp1319/`.
- **P3-3 (transcript M5).** M5 đòi "transcript". Bundle có `r2-progress.jsonl`, đủ stdout/stderr và hai script glue,
  nhưng không có transcript lệnh Desktop Commander, tức lời gọi driver/freeze và đầu ra in ra màn hình của chúng.
- **P3-4 (phạm vi quét secret).** `M5-secret-scan.json` lưu `rc: 0` và `scanner_sha256 = fbf9392b…6083`, bằng đúng hằng
  kỳ vọng. Tệp `tools\pkg_secret_scan.py` trên đĩa cũng băm ra `fbf9392b…6083`, bằng `scripts/pkg_secret_scan.py` trong
  kho. Cách gọi đúng (`argv` dài 2, đích là thư mục). Nhưng bộ quét chỉ chạy trên `evidence/` **trước khi** ba tệp
  `M5-secret-scan.json`, `script-r2_driver.py`, `script-r2_freeze.py` được ghi vào đó, và không quét `code/`, `parent/`.
  Bộ quét không in số tệp đã quét, và không có đối chứng dương, nên `rc=0` một mình không chứng minh có quét. Đã bù
  bằng cách đọc tay: các tệp `.py` trong `code/` và `parent/` bằng byte với P4 đã xuất trước đó, và mọi tệp mới
  (`result-win32.json`, `native-lock-test-result.json`, tệp smoke 0 byte, hai script, M1, M5, progress, stdout) đã đọc,
  không thấy mẫu bí mật.
- **P3-5 (driver M1 chỉ một chiều).** M1 chỉ gắn cờ tệp thừa hoặc lệch băm, không gắn cờ tệp **thiếu** so với
  export-manifest. Thực tế đủ 15/15 (12 normal + `induced_sequence` + 2 parent). M1 và M4 chỉ duyệt tệp ở tầng đầu
  (`glob("*")`) và bỏ qua thư mục con; đo lúc review thì không có thư mục con nào.
- **P3-6 (sổ đo lệch cột).** Dòng `do-luong.csv` của phiên dồn mô tả vào cột `bo_test`, còn `dat`, `tong`, `ca_do`,
  `thoi_luong_s` để trống. Tệp này nằm ngoài bundle, chỉ là chuyện định dạng.
- **P3-7 (quan sát hành vi sản phẩm, không phải lỗi r2).** Sau ca promotion-failure, đường `profile` bị **vắng** (dữ liệu
  hiện tại ở `profile-after-repaired`, bản khôi phục ở `profile-restore-staging`). Sau ca 18 thì staging còn lại. Giao
  dịch là one-shot (`RECOVERY_ALREADY_ATTEMPTED`, `RECOVERY_DESTINATION_EXISTS`), nên hai trạng thái này cần người can
  thiệp, không tự quay lui. Nên ghi vào MATRIX như một giới hạn của thiết kế phục hồi.

## 7. Lệch so với spec và ảnh hưởng

| Lệch | Ảnh hưởng kết luận |
|---|---|
| Spec §2 "đo lại `python --version`": driver ghi `sys.version` của chính trình thông dịch dùng để chạy test | Không. Cùng `sys.executable`, 3.13.1 |
| M4: thêm 2 tệp không phải `result-*.json` (P3-1) | Không |
| Kiểm tải và khóa không có trong bundle (P3-2) | Không, với kết luận test. Là lỗ hồ sơ quy trình |
| Transcript thiếu (P3-3) | Không |
| Quét secret hẹp hơn nội dung zip (P3-4) | Không. Đã bù bằng đọc tay |
| Driver sinh `M1-hashes.json` và tách bước M2/M3 trong cùng vòng lặp | Không. Mỗi test vẫn là một tiến trình riêng, cwd `W\code` |
| Thời điểm: chạy 08:51:16–08:51:18.96Z, đóng băng 08:53:54Z, nhả khóa 08:54:52Z, trong hạn lease (08:21:29–12:21:29Z) | Không |

## 8. Giới hạn của review này

- Chỉ đọc, liệt kê và băm. Không chạy test hay mã sản phẩm, không giải nén ra đĩa. Nội dung zip đọc trong bộ nhớ
  bằng `System.IO.Compression`; băm bằng `certutil` và `[Security.Cryptography.SHA256]`. Không ghi gì lên ASUS.
- Không thể chứng minh "chỉ chạy một lần". Driver tự từ chối nếu `W\code` đã tồn tại, `r2-progress.jsonl` chỉ có một
  dòng `start`, và `test_native_lock.py` đòi tệp smoke chưa tồn tại. Nhưng một lượt trước đó đã bị xóa sạch thì không
  phát hiện được.
- "Raw không bị ghi" chỉ đo bằng mtime.
- Việc mã không đổi sau chạy có hai bằng chứng độc lập: M4 của driver (`changed: []`) và phép so của tôi giữa zip
  (đóng băng 08:53:54Z), bản trên đĩa lúc review và P4. Giai đoạn giữa hai lần băm thì không đo được.
- Không đọc kết luận của operator. Dòng sổ đo ở `do-luong.csv` chỉ được đọc để kiểm việc lấy/nhả khóa; con số trong
  đó không được dùng làm bằng chứng.
- Không kiểm `docs/PROTOCOL_DA_PHIEN.md` hay MATRIX hiện hành. Mức trước r2 lấy từ RAW-1311-VERDICT.

## 9. Model / effort quan sát được

- Model: `claude-opus-5-5` (Opus 5.5). Đây là lời tự khai lấy từ system prompt của phiên reviewer; không có biên nhận
  bên ngoài.
- Effort: **KHONG_do_duoc** (reviewer không thấy tham số effort).
- Context: subagent mới, chỉ đọc, không kế thừa transcript của operator.

---
sha256 bản gốc của reviewer: `7918f55fd875dbd0a1fcbbbbb94d3369388085b20360cc7461313c9934a39d29` (chép nguyên văn).
