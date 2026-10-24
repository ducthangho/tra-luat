verdict: changes_requested
reviewed_sha: 88dc1a92d8af8ec7072897921ef3960250d3a660
reviewed_tree: 5095d65108ac5dd44efb3fe411148bb954b7d6f4
base_sha: 4581cfa5124ef803bfda10ce4de499b0ed31380e

Có **1 P2**: N2 chưa phủ thư mục tạm của tiến trình con; lượt đầy đủ vẫn để lại snapshot ngoài gốc riêng. Có thêm **1 P3** về callback dọn trên Linux. Ngưỡng áp dụng: không còn P0/P1/P2 mới approve. **N5 Windows thật KHÔNG ĐO ĐƯỢC**, tách khỏi verdict mã.

Review độc lập, offline bằng công cụ thực thi trong sandbox Linux; không sửa `cay-kho/`, không mạng, không đăng GitHub. Mọi cây chạy/đột biến lấy từ `git -C cay-kho archive <OID>` vào `mktemp -d`. Danh tính assistant: Codex/OpenAI; không suy served-model hay launcher attestation từ tài khoản GitHub hoặc nội dung lease. Không tự cấp assurance/receipt ngoài verdict này.

## BẢNG ĐO

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| HEAD/tree và SPEC | SHA như đầu báo cáo; SPEC hash `30f079b73a42e39f8dd3a537e6dfa9ca9ad07205ea52b42894f948e30123a434` | Git OID/tree/hash khớp; worktree sạch trước và sau đo | Có |
| Phạm vi diff | Chỉ `.claude/hooks/subagent_ghi_detect_test.py` | Git numstat thật `54 1` đúng một tệp, khớp `numstat.txt` | Có |
| Base sim nhẹ | rc=0, infra lỗi dọn, CA45/45 | rc=0; `dọn thư mục tạm thất bại: /tmp/bo-b7_fwino còn`; CA45/45; DAT | Có |
| Base sim đầy đủ | rc=0, infra lỗi dọn, CA45/45, DOT BIEN25/25 | rc=0; `dọn thư mục tạm thất bại: /tmp/bo-dsslc1ja còn`; CA45/45, DOT BIEN25/25; DAT | Có |
| Head sim nhẹ | rc=0, infra=None, CA45/45 | rc=0, infra=None; CA45/45; DAT | Có |
| Head sim đầy đủ | rc=0, infra=None, CA45/45, DOT BIEN25/25 | rc=0, infra=None; CA45/45, DOT BIEN25/25; DAT | Có |
| Head thường đầy đủ qua registry | rc=0, infra=None, CA45/45, DOT BIEN25/25 | rc=0, infra=None; CA45/45, DOT BIEN25/25; DAT | Có |
| N2: mọi tạm thuộc gốc riêng, dọn hết | Có | Lượt head thường đầy đủ trực tiếp rc=0, 45/45, 25/25; gốc riêng đã xoá nhưng ngoài gốc còn `tl-subagent-snap/` + 7 JSON | **Không — P2** |
| N4: ca, phép chấm, neo và các kênh đột biến | Giữ nguyên, đều bị giết | 71 hàm cũ AST không đổi; CA45, mutant25+11+1 không đổi; 11 neo test đều 1, neo settings `[1,1]`; hai kênh bổ sung base/head đều 12 GIET, survivors=[] | Có |
| N6 ruff F | Delta=0 | Ruff0.17.1 base/head đều rc=0, 0 lỗi F; delta=0 | Có |
| Bốn đột biến gỡ bản vá | Mỗi cái làm bộ hoặc registry đỏ | a,b,d đỏ; **c bỏ raise sống**. Tiêm lỗi bền vào c vẫn rc=1 nhờ wrapper kiểm cây còn | Chỉ 3/4 bị giết bởi lượt sim nhẹ |
| N5 Windows thật | Executor đo log job riêng | **KHÔNG ĐO ĐƯỢC** trong Linux offline; không xem log job Windows | Không dùng làm lý do block/approve mã |

Lệnh ma trận: `bash review-evidence/matrix.sh > review-evidence/matrix.log 2>&1`. Một shell dựng **cả base và head**, đặt `PYTHONDONTWRITEBYTECODE=1`, rồi chạy đủ năm vế qua `python3 -I sim/chay.py` (harness capture gọi nguyên script bằng `runpy`). Không thay registry. `rc` ở bảng là mã bộ con; mã harness `sim/chay.py` tự nó luôn 0, không được dùng thay cho `rc`/`loi_ha_tang`.

Ghi chú harness: cả năm dòng `HARNESS_EXIT` đều 0 và kết quả từng suite đã ghi đủ. Sau dòng thứ năm, shell có `unexpected EOF` vì reviewer sửa file script khi shell đang chạy (lệch vị trí đọc); không coi mã thoát shell ngoài là một pass. `bash -n review-evidence/matrix.sh` trên bản script cuối trả 0. Lỗi của harness không thuộc PR; không bỏ nó khỏi raw log và không cần chạy lại các phép đo con đã hoàn tất.

Precondition đã kiểm: archive trần không có `.git`, làm ca t21 chỉ đạt 44/45. Lượt thiết lập sai bị loại, không quy lỗi cho PR. Cây đo chính được `git init`, add/commit **cục bộ** để t21 có Git top-level/HEAD; không thay byte các tệp nguồn. Script tái lập lưu đủ bước. Tiến độ trước khi tổng hợp giữ ở `review-evidence/review-progress.md`.

## ĐỘ TRUNG THỰC CỦA MÔ PHỎNG

**Đã kiểm tệp thật, không chỉ suy từ màu test.** Sau base sim nhẹ qua registry, `/tmp/bo-b7_fwino` còn **266** regular file mode `0444`; tất cả dưới `.git/objects/`. Danh sách đủ: `review-evidence/registry-base-readonly.json`.

Đo lại qua **đúng `_chay_co_lap`** với observer audit bổ sung, vẫn mô phỏng ở cha và con:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -I review-evidence/observe_registry.py
REGISTRY_OBSERVER rc=0 infra='dọn thư mục tạm thất bại: /tmp/bo-4gnrw7ul còn' readonly=266 unmapped=0
SUMMARY ['TONG: CA 45/45 dat · DOT BIEN 25 muc CHE DO NHE — do khi diff cham vung', 'TONG: DAT']
```

`registry-base-readonly-origin.json` liệt kê **từng tệp + mode + kho + ca nguồn**, ánh xạ 266/266 từ audit lúc tạo thư mục, không đoán nguồn từ tên. Một ví dụ:

```text
/tmp/bo-4gnrw7ul/tl329-cay-6wepdamd/.git/objects/27/fc443a425697eb768944791950a4bbadee2551
mode=0444; kho=tl329-cay-6wepdamd; ca=t4b_XOA_tep_da_theo_doi_thi_changed
```

Phân bổ đáng chú ý: t26i tạo 56 object còn sót; t22b có 5 object trong hai kho `tl329-gitcfg-*`; t4d có 7; t18 và t26h mỗi ca 9; t8/t11/t25 mỗi ca 12; các ca `_cay` đơn thông thường 6. t24 còn object trong **kho chính `_cay`**; linked worktree có `.git` là tệp con trỏ, không phải symlink/junction. Nhánh t24 thành công thực tế có gọi `rmtree(wt)`; không quy mọi cây `tl329-wt-*` thành kho chỉ-đọc bị bỏ quên. Bản inventory trực tiếp độc lập cũng cho 266 object, 95 mkdtemp và rc=0 (`direct-base-sim-nhe.json`).

Mô phỏng hỗ trợ giả thuyết cụ thể: Python unlink regular file thiếu bit ghi gây PermissionError; git thực tạo đúng file như thế; helper xoá được chúng. Nó **không chứng minh** lỗi Windows của job cũ chỉ có nguyên nhân đó. Nó không mô hình hoá share flags, reparse points, cwd locking, ACL, hay giới hạn đường dẫn Windows.

| Cơ chế Windows khác | Bộ có tạo điều kiện này không? Mã + phép đo | Bản vá chữa/che thế nào? |
|---|---|---|
| File bị tiến trình con còn sống giữ handle | Các lời gọi suite/hook dùng `subprocess.run`, chờ kết thúc; `_cay` đặt `gc.auto=0`. Các lượt POSIX qua registry đã hoàn tất không báo con cháu còn sống. Không có đường suite dùng Popen để thả nền. Handle còn sống trên Windows: **KHÔNG ĐO ĐƯỢC**. | Chmod không giải phóng handle. Fault injection share violation bền ở unsafe-rmtree: 6 unlink attempts qua 3 lượt, cuối PermissionError, cây còn; không bị báo xanh. Chờ 0,5s có thể giải quyết lỗi nhất thời; không khẳng định giải quyết được handle thật. |
| Thư mục là cwd của tiến trình còn sống | Suite không `os.chdir`; Git/worktree/bash được chạy với cwd riêng bằng run và được chờ. Child hook thừa kế cwd của suite. Probe Linux tạo child giữ cả cwd và open file: child vẫn sống mà cây đã xoá được. Windows: **KHÔNG ĐO ĐƯỢC**. | Chmod không đổi cwd/đóng tiến trình. Probe Linux cho thấy sim readonly không kiểm được cơ chế này. Nếu Windows từ chối dọn bền, wrapper/registry phải đỏ; không có bằng chứng Windows thực. |
| Junction/symlink/reparse point | Không có ca tạo symlink/junction. Trước dọn ở lượt đầy đủ head trực tiếp: 0 symlink; linked worktree `.git` là regular file. Probe POSIX: link trong cây bị xoá, sentinel ngoài cây giữ nguyên. Junction Windows: **KHÔNG ĐO ĐƯỢC**. | Helper uỷ thác traversal cho shutil; chmod không sửa reparse semantics. Không claim kiểm chứng trên Windows. |
| Đường dẫn dài | Lượt đầy đủ trace: đường dài nhất dưới gốc riêng 133 ký tự trong sandbox; nguồn không tạo chuỗi thư mục lồng sâu. Bản vá thêm một cấp `tl329-bo-*`. Độ dài tiền tố TEMP/long-path policy trên runner Windows: **KHÔNG ĐO ĐƯỢC**. | Chmod không rút ngắn đường hoặc bật long paths. Lỗi OSError bền ở helper không được nuốt; Python fd-callback có điểm yếu P3 bên dưới. |

Lệnh các probe giới hạn: `PYTHONDONTWRITEBYTECODE=1 python3 -I review-evidence/windows_limits.py`; output thật ở `windows-limits.log`. `strace` đã thử nhưng ptrace bị sandbox từ chối (`PTRACE_TRACEME: Operation not permitted`); không khai có syscall trace của Git/bash.

## PHỦ GỐC TẠM VÀ N4

AST xác nhận các điểm tạo tạm trực tiếp của suite:

```text
67 mkdtemp (_cay), 147 mkdtemp (_snap), 233 mkdtemp (t6),
547 mkdtemp (probe bash), 622 TemporaryDirectory (fixture bash),
800 mkdtemp (linked worktree), 919 TemporaryDirectory (t25b),
1025 mkdtemp (t22b), 1570 TemporaryDirectory (mutant hooks),
1649 mkdtemp (gốc suite).
```

Không có call site suite trực tiếp tới `mkstemp`, `NamedTemporaryFile` hoặc `gettempdir`. Đường tự ghép từ các gốc trên gồm repo Unicode, file script bash, worktree và mutant hook. **Hook con** có `gettempdir()` ở `subagent_ghi_detect.py:49` và `mkstemp(dir=dich.parent)` ở dòng244; đây là phần cache `tempfile.tempdir` của cha không truyền được.

Lệnh trace head thường đầy đủ: `PYTHONDONTWRITEBYTECODE=1 python3 -I review-evidence/probes.py direct head thuong full`. Không sửa nguồn test; observer bọc mkdtemp/ca để ghi metadata. Output:

```text
rc=0; TONG: CA 45/45 dat · DOT BIEN 25/25 bi giet; TONG: DAT
TEMP_COUNT 2487
ROOTS ['/tmp/wp854-head-thuong-direct-d8awnod9/tl329-bo-2xji4mp8']
ESCAPING_MKDTEMP []
PRE_CLEANUP readonly_count=134, symlinks=[], max_path_chars=133
REMAINING_TOP ['tl-subagent-snap']
```

Thư mục cha sau chạy có bảy tệp ngoài gốc đã dọn: `a6.json`, `a9.json`, `a11.json`, `a11b.json`, `a18.json`, `a23.json`, `a24.json`. Phát hiện này giải thích vì sao chỉ trace mkdtemp trong cha hoặc chỉ đọc `loi_ha_tang=None` là chưa đủ. Git tạo object trong các fixture cwd; bash settings gọi hook với snapshot đã chỉ định. **Escape đo được là child Python của m9**, không có chứng cứ Git/bash tự để lại một thư mục TMP khác. Không có syscall trace để khẳng định bao phủ mọi thao tác native.

N4 đo bằng `probes.py metadata` và `probes.py channels`, có log riêng: mọi hàm cũ/CA/mutant giữ nguyên; mỗi neo nhắm test khớp 1 và settings khớp `[1,1]`. Base/head mỗi bên giết 11 mutant nhắm test và 1 settings, survivors=[]; global tempdir giữ nguyên qua kênh exec. Raw head đầy đủ trực tiếp có **25 GIET sản phẩm + 11 GIET test + 1 GIET settings**, 0 SONG. Không bớt ca/nới assertion để chữa cleanup.

## RĂNG CỦA BẢN VÁ

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -I review-evidence/probes.py teeth`. Mỗi mutant có một archive tạm riêng, precondition Git cục bộ và chỉ thay đúng một neo; đều chạy sim nhẹ bằng script `sim/chay.py` qua capture. Raw output giữ ở `a-no-chmod-raw.log` ... `d-no-tempdir-raw.log`.

| Đột biến | Output thật của bộ/registry | Kết luận |
|---|---|---|
| a. Bỏ `os.chmod` | rc=1; CA45/45; thêm `TONG: DO — don goc tam cua bo that bai: PermissionError...`; registry còn `bo-evzq5yrb` | Bị giết |
| b. Main gọi `chay()` | rc=0, CA45/45, DAT; infra lỗi dọn `bo-7kfo31b_` | Bị registry giết |
| c. Bỏ `raise` cuối | rc=0, CA45/45, DAT; infra=None | **SỐNG** |
| d. Không đặt `tempfile.tempdir` | rc=0, CA45/45, DAT; infra lỗi dọn `bo-_9zy97fc` | Bị registry giết |

(c) sống vì readonly được callback chữa ngay; nhánh OSError cuối không chạy. Thử tiếp lỗi bền với chính mutant c (`windows_limits.py`): `NO_RAISE_MUTANT_WITH_FAILURE rc=1 ... tl329-bo-... con`. Wrapper còn kiểm cây tồn tại, nên bỏ raise riêng lẻ vẫn không biến lỗi dọn bền thành xanh. Không tuyên bố bộ sim nhẹ đã canh nhánh raise; đây là giới hạn phủ, không phải một P2 độc lập.

## BẢNG SĂN

Các hướng sau độc lập với ma trận, inventory, N4 tĩnh và bốn đột biến bắt buộc.

HƯỚNG 1: Global tempfile rò qua mutant chạy bằng exec

- giả thuyết: nạp lại suite trong namespace mutant sẽ đổi/reset gốc tạm dùng chung, làm ca sau thoát gốc.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -I review-evidence/probes.py channels`; kiểm thêm trace full.
- output: base/head `test_survivors=[] settings_survivors=[] killed=12 tempdir_restored=True`; 2487 mkdtemp của full đều dưới gốc riêng.
- kết luận: **KHÔNG PHẢI LỖI** cho kênh exec. Escape của child m9 là P2 riêng, không quy cho exec.

HƯỚNG 2: API onexc/onerror không tương thích Python CI

- giả thuyết: chọn callback theo version làm rmtree TypeError hoặc không chữa readonly trên Python3.12.
- lệnh: `for interpreter in python3.11 python3.12 python3.13; do PYTHONDONTWRITEBYTECODE=1 "$interpreter" -I review-evidence/probes.py hunts; done`.
- output thật: Python3.11.17 chọn `onerror`; 3.12.3/3.13.16 chọn `onexc`; CI cũng ghim `python-version: "3.12"`; cả ba `READONLY_ROOT_REMOVED True`.
- kết luận: **KHÔNG PHẢI LỖI** về chữ ký callback/nhánh version ở đường readonly. Không suy kết quả Linux thành Windows.

HƯỚNG 3: Retry ba lần nuốt lỗi bền hoặc che trạng thái đỏ

- giả thuyết: ba lượt retry có thể trả thành công dù lỗi vẫn tồn tại.
- lệnh: cùng lệnh `hunts` trên ba Python; tiêm PermissionError ở rmtree 1/2/3 lần.
- output: lỗi1 ⇒ calls2/sleeps[0.5]/root absent; lỗi2 ⇒ calls3/sleeps[0.5,0.5]/root absent; lỗi3 ⇒ calls3/PermissionError/root exists. Unsafe callback với share violation bền ⇒ 6 unlink attempts, PermissionError, root exists.
- kết luận: **KHÔNG PHẢI LỖI** về false green. Retry chấp nhận lỗi nhất thời đã hết; không chứng minh chữa được share violation Windows.

HƯỚNG 4: FileNotFoundError của con bị hiểu nhầm thành đã xoá cả gốc

- giả thuyết: catch FileNotFoundError rộng có thể để gốc còn mà wrapper trả 0.
- lệnh: `probes.py hunts` trên ba Python, tiêm ENOENT riêng cho root và child.
- output: `ENOENT root helper=returned root_exists=False`; `ENOENT child helper=returned root_exists=True`; **`ENOENT_WRAPPER rc=1 ... <goc> con`**.
- kết luận: **KHÔNG PHẢI LỖI** ở cổng thoát của suite: tồn tại được kiểm lại. Helper riêng có thể return sớm nhưng call site duy nhất không công bố pass khi cây còn.

HƯỚNG 5: `rc or 1` làm mất mã thoát đã đỏ

- giả thuyết: cleanup lỗi sẽ làm rc khác 0 thành 0 hoặc ghi đè mã lỗi hữu ích.
- lệnh: `probes.py hunts`, fake chay trả lần lượt 0,1,2,7 và tiêm lỗi dọn bền.
- output trên cả ba Python: `0→1, 1→1, 2→2, 7→7`; mỗi lần in rõ `TONG: DO — don goc tam cua bo that bai: PermissionError...`; `tempdir_restored=True`.
- kết luận: **KHÔNG PHẢI LỖI**.

HƯỚNG 6: Ngoại lệ giữa suite bỏ qua finally/khôi phục tempdir

- giả thuyết: khi một ca ném ngoại lệ, global tempdir vẫn trỏ vào cây đã xoá hoặc ngoại lệ bị nuốt.
- lệnh: `probes.py hunts`, fake chay ném RuntimeError.
- output: `SUITE_EXCEPTION injected suite exception tempdir_restored=True` trên ba Python; ngoại lệ truyền ra.
- kết luận: **KHÔNG PHẢI LỖI** cho tình huống đã đo (cleanup thành công). Không claim đã đo mọi tổ hợp exception và lỗi cleanup.

HƯỚNG 7: Callback giả định mọi hàm rmtree báo lỗi đều nhận một đối số

- giả thuyết: native fd-rmtree báo `os.open`/scandir thì callback chmod rồi gọi `ham(duong)` có thể phá chẩn đoán/retry.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -I review-evidence/native_permission.py`; thư mục thật mode0500 chứa một tệp thường, **không monkeypatch** rmtree/unlink.
- output: `NATIVE_PERMISSION_DIRECTORY TypeError: open() missing required argument 'flags' (pos 2) root_exists=True mode=0o200`.
- kết luận: **LỖI — P3**. Gate vẫn đỏ, không làm mất kiểm chứng chính; lỗi chẩn đoán trên điều kiện fixture không tạo ra. Chi tiết bên dưới.

## FINDINGS

### child-temp-env-escapes-suite-root  [P2]  Tiến trình con vẫn tạo snapshot ngoài gốc riêng, N2 chưa đạt

TỆP/DÒNG: `.claude/hooks/subagent_ghi_detect_test.py:1649-1651` (đặt gốc), liên hệ cleanup dòng1654-1657. Nguồn child: product hook dòng47-49 và244; m9 của test dòng1344-1346.

VẤN ĐỀ: Chỉ đặt `tempfile.tempdir` tác động Python cha. Bộ con mới vẫn nhận TMPDIR/TEMP/TMP trỏ tới registry `bo-*`. Trong chế độ đầy đủ, mutant m9 cố ý không đọc `TL_SUBAGENT_SNAP_DIR`, nên hook dùng `tempfile.gettempdir()/tl-subagent-snap`, tạo thư mục và các mkstemp **ngoài `tl329-bo-*`**. Wrapper dọn hết gốc riêng rồi trả 0, trong khi snapshot đó vẫn còn cho registry dọn. Mã hiện tại sửa được readonly của Git nhưng chưa thực hiện N2 “mọi thư mục tạm của bộ nằm dưới một gốc riêng”. Đây là vi phạm acceptance đo được; không khẳng định bảy JSON này tự gây lỗi Windows hay chứa readonly.

ĐÃ THỬ NGHIỆM:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -I review-evidence/probes.py direct head thuong full
rc=0; CA45/45; DOT BIEN25/25; gốc tl329-bo-* đã xoá;
REMAINING_TOP ['tl-subagent-snap'] với 7 JSON nêu trên.

PYTHONDONTWRITEBYTECODE=1 python3 -I review-evidence/child_temp_escape.py
REPAIR_CHILD_ENV False rc=0 own_root_removed=True
  case=True, 'cwd khong phai git -> unknown (mong doi unknown)'
  outside_entries=['tl-subagent-snap','tl-subagent-snap/a6.json']
REPAIR_CHILD_ENV True rc=0 own_root_removed=True
  case=True, cùng phép đo
  outside_entries=[]
```

Bản rút gọn chạy **hook m9 thật trong subprocess** qua t6 bên trong wrapper thật; chỉ thay chay bằng một ca để định vị lỗi. A/B chuyển ba biến env trong harness, không sửa nguồn PR. Chứng cứ: `coverage.log`, `direct-head-thuong-full.json`, `child-temp-escape.log` và script tương ứng.

GỢI Ý VÁ: Trong wrapper của **tệp test thuộc write set**, lưu trạng thái có/vắng của TMPDIR/TEMP/TMP rồi đặt cả ba sang gốc riêng khi chạy suite; finally khôi phục env và tempfile.tempdir, dọn như hiện tại. Xác minh mọi đường gọi child thừa kế env đó. Không cần sửa product, registry, assertion hay bảng mutant.

CA KHOÁ: Chạy m9+t6 trong gốc ngoài rỗng, assert wrapper rc đúng, gốc riêng đã mất, **gốc ngoài rỗng**. Giữ một lượt full head thường trực tiếp và sim qua registry; 45/45, 25+11+1 vẫn phải bị giết. Test này phát hiện đúng lớp lỗi subprocess fallback, không chỉ so chuỗi env.

RỦI RO CỦA CÁCH VÁ: Env là trạng thái toàn cục; phải khôi phục cả biến vốn không tồn tại khi chay ném ngoại lệ, và đồng bộ với tempfile.tempdir. Cần đo lại Windows native/Git Bash sau thay đổi. Không giảm phép đo của m9 để làm hết file ngoài gốc.

ĐỘ TIN: cao (full run và A/B rút gọn độc lập).

### cleanup-callback-assumes-unary  [P3]  PermissionError trên thư mục Linux bị đổi thành TypeError khi retry callback

TỆP/DÒNG: `.claude/hooks/subagent_ghi_detect_test.py:1625-1627`.

VẤN ĐỀ: Callback áp `chmod(..., S_IWRITE)` lên mọi đường rồi gọi mọi `ham` bằng một đối số. Với fd-rmtree Python3.13 trên Linux, lỗi thật khi xoá trong thư mục0500 bị callback làm thư mục thành0200; lượt sau rmtree báo `os.open`, cần đối số flags. TypeError thoát cả retry OSError và thông báo cleanup của wrapper. Bộ vẫn thoát khác 0; điều kiện directory permission này không do fixture hiện tại tạo, nên **P3**, không chặn theo ngưỡng P0/P1/P2.

ĐÃ THỬ NGHIỆM: `PYTHONDONTWRITEBYTECODE=1 python3 -I review-evidence/native_permission.py` ⇒ `TypeError: open() missing required argument 'flags' (pos 2) root_exists=True mode=0o200`. Log `native-permission.log`. Probe lỗi handle tiêm cũng tái hiện ở fd-rmtree; unsafe-rmtree vẫn trả PermissionError (`windows-limits.log`). Không coi đây là kết quả trên Windows.

GỢI Ý VÁ: Giới hạn callback vào thao tác/lỗi readonly có thể retry an toàn; giữ các permission bit cần thiết và truyền lại lỗi gốc cho outer retry khi hàm cần tham số khác, thay vì gọi chung `ham(duong)`. Xử lý hình dạng exception tuple của onerror và object của onexc khi phân loại lỗi. Không mở rộng quyền/xoá ra ngoài cây.

CA KHOÁ: Thư mục0500 chứa file trên nền không có DAC override; đòi lỗi cuối vẫn là OSError có đường dẫn/lý do và suite rc khác0. Giữ ca readonly regular file mode0444 trên Python3.11/3.12/3.13.

RỦI RO CỦA CÁCH VÁ: Không làm mất khả năng gỡ readonly Windows; không nuốt lỗi bền hoặc theo symlink ra ngoài cây. Đây là nợ đề nghị cho executor/chủ kho phân việc, không tự mở rộng packet và không phải điều kiện approve mã trong lượt này.

ĐỘ TIN: cao về TypeError Linux; Windows tương ứng **KHÔNG ĐO ĐƯỢC**.

## PHẦN CHƯA ĐO VÀ CHỐT PHẠM VI

- N5: **KHÔNG ĐO ĐƯỢC**. Executor cần log `gate-registry (windows-latest)` của workflow_dispatch trên exact head sau sửa; Linux sim pass không thay thế log đó.
- Không chạy gate toàn kho/phát hành/LIVE ngoài acceptance của packet; không merge, push hoặc đăng review.
- Xác nhận cuối: `git --no-optional-locks -C cay-kho status --porcelain` rỗng; HEAD/tree vẫn đúng hai OID ở đầu báo cáo. Không sửa checkout review.
