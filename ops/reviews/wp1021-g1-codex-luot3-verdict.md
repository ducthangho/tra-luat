Verdict: request_changes
Reviewed commit: 8d9e3e3b55897575b9e69a13f5d1a4f3ff6c9fde
Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d

Kết luận cuối: **request_changes** vì còn **một finding P3 về chốt hồi quy OSError** (F3 bên dưới). F1/P2 và F2/P3 của lượt 2 đều **ĐÃ VÁ THẬT**. Không tìm thấy lỗi runtime mới trong phần thay đổi qua các phép đo đã chạy. Head đạt toàn suite `97/97 · 149/149 · 2/2`, cổng thật rc=0/tổng 306. Mutant thu hẹp helper mới chỉ còn bắt PermissionError vẫn sống qua toàn suite, dù EIO/ESTALE trên mutant thoát traceback; đây là bằng chứng thiếu chốt, không phải lời khẳng định head đang bắt sai. Chi tiết, lệnh và output được ghi tăng dần dưới đây.

## Phạm vi

Review độc lập packet #1021 r2, lượt 3. Checkout `cay-kho/` chỉ đọc mã nguồn; bản sao đầy đủ cây, fixture và log đặt trong sandbox. Cấu hình `core.abbrev=7` theo chỉ thị. Mọi tiến trình đo dùng `PYTHONDONTWRITEBYTECODE=1`, fixture Git cô lập bằng `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`.

Windows CI/local và Ubuntu CI exact head: chưa có phép đo độc lập; không nhận lời khai executor là kết quả đo. Không cấp quyền merge/land.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Finding lượt 2 | Kết luận | Bằng chứng chạy lại trên head mới |
|---|---|---|
| F1/P2 `loi-do-liet-ke-thu-muc-thoat-traceback` | **ĐÃ VÁ THẬT** | `review_new.py error-child head {kiem,sinh} {stat-os,access}`: 4/4 rc=2/không traceback, có hit. Bản đồ I/O bên dưới kiểm cả guard, helper, `.git`, liệt kê và đọc/băm. |
| F2/P3 `loi-do-thieu-chot-ngoai-le-lap-trinh` | **ĐÃ VÁ THẬT** | `runtime`/`value` ở iterdir truyền ra; `boundary_oracle.py head` rc=0; `new_mutate.py broad`/`broad_literal`: c100 `giet_that`, c18 sạch. Tracer chốt (7) đủ 4 hit/đúng đối tượng. |

Không finding cũ nào bị giữ là VÁ HỜ hoặc CHƯA VÁ. F3 mới ở cuối là thiếu phép phân biệt các lớp con OSError, khác thiếu chốt lỗi lập trình của F2.


## Đợt 1 — neo và tái hiện lượt 2

`evidence/preflight.json`: `git rev-parse HEAD HEAD^{tree} origin/master` rc=0, lần lượt `8d9e3e3b55897575b9e69a13f5d1a4f3ff6c9fde`, `97e0d90fb6dcda86076272c951a44e1ff79ff554`, `757bde561d09738858506aecf5de2f050a5f0d5e`; detached (`symbolic-ref` rc=1/rỗng), không nông (`false`), `.git` là thư mục, status rỗng. SHA-256 SPEC khớp neo.

Script lượt 2 được chép ra gốc sandbox để `ROOT=parent(__file__)` trỏ đúng nơi. `review_new.py` và `boundary_oracle.py` giữ nguyên byte. `new_mutate.py`/`mutate.py` chỉ đổi mốc `if not tm.is_dir()` sang `if not _hoi_trang_thai(tm.is_dir, tm)`; `probe.py` thêm `c100_` vào danh sách ca; `integrity.py` đổi mốc diff lượt trước từ `99c463d`/`DIFF-LUOT2.patch` sang `5efa311`/`DIFF-LUOT3.patch`. Không chỉnh oracle để nhận kết quả mới.

- F1 **ĐÃ VÁ THẬT** ở phép tái hiện cũ: `python3 review_new.py error-child head {kiem,sinh} {stat-os,access}` — cả 4 tiến trình rc=2, có `REVIEW_FAULT_HIT: stat-os`, stderr `KHÔNG ĐO ĐƯỢC: không đọc được trạng thái .../ops/reviews (PermissionError...)`, không traceback. Log `evidence/rerun-head-*.{stdout,stderr,json}`. Lỗi liệt kê muộn (`late`) cũng rc=2 trên hai đường.
- F2 **ĐÃ VÁ THẬT** ở phép tái hiện cũ: `python3 review_new.py error-child head {kiem,sinh} {runtime,value}` — cả 4 tiến trình rc=1, traceback kết thúc bằng đúng `RuntimeError`/`ValueError: review programming fault`; lỗi lập trình không bị đổi thành KhongDoDuoc. `python3 boundary_oracle.py head` rc=0, hai đường `propagated_same_error=true, hit=1, restored=true`.
- `python3 new_mutate.py broad` và `broad_literal`: c98/c99/c89 `qua`, **c100 `giet_that`**: `lỗi lập trình ở iterdir [] bị nuốt/đổi ... được không ngoại lệ`, đối chứng c18 `[true, ""]`. `boundary_oracle.py mut-broad` và `mut-broad_literal` đều rc=1, có hit=1 nhưng bị đổi thành rc=2. Đây là chết đúng chốt c100, không lấy lỗi mất mốc m147 làm tín dụng.

Các lệnh đo dùng tiền tố môi trường đã nêu. Full suite và bản đồ I/O vẫn đang chạy; chưa kết luận cuối.


## Đợt 2 — tiêu chí và bản đồ hệ tệp

`python3 probe.py head behaviors` (log `head-behaviors` và từng `fixture-head-*`): C1a rc=1, `tổng 2`, nêu x đuôi hoa; only-x rc=1, `tổng 1`, không thông báo không có tệp; C1b rc=2, stderr nêu x, không traceback, không có dòng tổng. Base đo lại: C1a `tổng 1`, only-x rc=2/không có tệp, C1b rc=1/bỏ x. Cặp tên chỉ khác hoa thường đếm 2 ở head. Thư mục đuôi hoa tới bước băm và rc=2.

`python3 mutate.py exact --behaviors`: c98/c99 `giet_that`, đối chứng c18 sạch; mutant bỏ x ở C1a/C1b/only-x. `python3 mutate.py isfile --behaviors`: c89 `giet_that` (rc=1 thay rc=2), đối chứng c18 sạch. `python3 mutate.py glob --behaviors`: c98/c99 `giet_that`, đối chứng c18 sạch; c100 `gian_giao` vì không còn gọi iterdir, KHÔNG lấy tín dụng này làm chết mutant. C3 được chứng minh bởi c98.

C6: `python3 measure.py head gate` và `base gate`: rc=0, `253 ĐẠT v2 · 11/11 miễn trừ ... · 42 NỢ ... · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 306`, `TỔNG: ĐẠT`. Lệnh đếm riêng dùng `os.listdir` (log `count-head`, `count-base`) cho `casefold_suffix 306` và `exact_suffix 306`. `python3 ops/bien_nhan_v2.py --root . --sinh-no` trên head/base đều rc=0, `# 42 tệp`.

C9: `git diff --numstat 757bde5..HEAD` chỉ hai tệp: `40 5 ops/bien_nhan_v2.py`, `262 0 ops/bien_nhan_v2_test.py`; `git diff --check` rc=0/rỗng. Ruff `--no-cache --select F` head/base cùng rc=1/cùng F541 tại test:1677, output byte-identical nên delta 0. Doctrine-scan head/base rc=0, `đã quét 10 tệp, 0 chỗ chép doctrine`. `rg -n 'glob\("\*\.receipt\.yaml"\)' ops/bien_nhan_v2.py`: head rc=1/0 dòng; base 2 dòng (1442/1601); mut-glob 1 dòng (116). Dương tính đối chứng là C1a/C1b ở trên, không suy từ vế âm.

### Bản đồ đầy đủ các callsite I/O của mã sản phẩm

Liệt kê độc lập bằng AST (`evidence/fs-call-inventory.json`) và theo các lời gọi từ `main` → `kiem`/`_sinh_no`, gồm bước import nguồn provider và nhánh đọc bằng chứng sau receipt. Bảng dưới đo từng callsite; lệnh cho MỖI ô: `python3 fs_probe.py <head|base> <kiem|sinh> <site>`. Log đầy đủ `evidence/fs-<tree>-<mode>-<site>.{stdout,stderr,json,result.json}` ghi vị trí, hit và khôi phục. `python3 fs_matrix.py` chạy 52 tiến trình độc lập, tất cả có hit dương, khôi phục hàm gốc. Lỗi tiêm là PermissionError thuộc OSError. Không khẳng định đã tiêm mọi syscall bên trong thư viện/importer/Git; đã đo mọi callsite I/O tường minh của tệp sản phẩm trong hai luồng.

| Site và dòng head | Phạm vi / thao tác | Head đo mới | Base đo mới |
|---|---|---|---|
| `provider-resolve` (235) | Không đổi; resolve đường dẫn module trước import nguồn | kiem: rc=1, hit=1, traceback; sinh: rc=1, hit=1, traceback | kiem: rc=1, hit=1, traceback; sinh: rc=1, hit=1, traceback |
| `provider-launcher` (240) | Không đổi; đọc launcher.py | kiem: rc=2, hit=1, không traceback; sinh: rc=0, hit=1, không traceback | kiem: rc=2, hit=1, không traceback; sinh: rc=0, hit=1, không traceback |
| `provider-agents` (244) | Không đổi; đọc AGENTS.md | kiem: rc=2, hit=1, không traceback; sinh: rc=0, hit=1, không traceback | kiem: rc=2, hit=1, không traceback; sinh: rc=0, hit=1, không traceback |
| `provider-protocol` (244) | Không đổi; đọc PROTOCOL_DA_PHIEN.md | kiem: rc=2, hit=1, không traceback; sinh: rc=0, hit=1, không traceback | kiem: rc=2, hit=1, không traceback; sinh: rc=0, hit=1, không traceback |
| `main-resolve` (1581) | Không đổi; resolve --root trước try | kiem: rc=1, hit=1, traceback; sinh: rc=1, hit=1, traceback | kiem: rc=1, hit=1, traceback; sinh: rc=1, hit=1, traceback |
| `guard-isdir` (1471) | Đổi lượt 3; is_dir/stat ops/reviews ở guard kiem | kiem: rc=2, hit=1, không traceback | kiem: rc=1, hit=1, traceback |
| `helper-isdir` (113) | Helper thêm ở packet; bọc lỗi lượt 3; is_dir/stat ops/reviews ở selector (đo riêng cả lần thứ hai trong kiem) | kiem: rc=2, hit=1, không traceback; sinh: rc=2, hit=1, không traceback | Không có callsite này; đối chứng glob ở listing_probe |
| `git-exists` (1472) | Đổi lượt 3; exists/stat .git khi thiếu ops/reviews | kiem: rc=2, hit=1, không traceback | kiem: rc=1, hit=1, traceback |
| `listing` (116) | Đổi glob thành iterdir trong packet; liệt kê thư mục; lỗi ngay và lỗi giữa iterator | kiem: rc=2, hit=1, không traceback; sinh: rc=2, hit=1, không traceback | Không có callsite này; đối chứng glob ở listing_probe |
| `receipt-hash` (677 → 1496/1641) | Không đổi; read_bytes để băm receipt | kiem: rc=2, hit=1, không traceback; sinh: rc=2, hit=1, không traceback | kiem: rc=2, hit=1, không traceback; sinh: rc=2, hit=1, không traceback |
| `receipt-text-kiem` (1497) | Không đổi; read_text receipt ở kiem | kiem: rc=2, hit=1, không traceback | kiem: rc=2, hit=1, không traceback |
| `receipt-text-sinh` (1640) | Không đổi; read_text receipt ở --sinh-no | sinh: rc=2, hit=1, không traceback | sinh: rc=2, hit=1, không traceback |
| `grafts-exists` (1214) | Không đổi; exists/stat .git/info/grafts qua _kho_lanh | kiem: rc=2, hit=42, không traceback | kiem: rc=2, hit=42, không traceback |
| `run-lstat` (1279) | Không đổi; lstat run_json qua _vang | kiem: rc=0, hit=29, không traceback | kiem: rc=0, hit=29, không traceback |
| `run-text` (1434) | Không đổi; read_text run_json | kiem: rc=2, hit=29, không traceback | kiem: rc=2, hit=29, không traceback |
| `verdict-isfile` (1295) | Không đổi; is_file/stat verdict_path | kiem: rc=2, hit=29, không traceback | kiem: rc=2, hit=29, không traceback |
| `verdict-text` (1298) | Không đổi; read_text verdict_path | kiem: rc=2, hit=29, không traceback | kiem: rc=2, hit=29, không traceback |
| `git-run` (843) | Không đổi; subprocess.run trong _git | kiem: rc=2, hit=506, không traceback | kiem: rc=2, hit=506, không traceback |
| `blob-run` (970) | Không đổi; subprocess.run đọc blob Git | kiem: rc=2, hit=253, không traceback | kiem: rc=2, hit=253, không traceback |
| `history-run` (1176) | Không đổi; subprocess.run trong _chay_git | kiem: rc=2, hit=1, không traceback | kiem: rc=2, hit=1, không traceback |

Các thao tác `root / ...`, `p.name`, `.lower()`, `.endswith()`, `Path.parts`, `is_absolute()`, `sorted(ds)` chỉ xử lý đường dẫn/tên trong bộ nhớ; băm SHA-256 không có I/O ngoài `read_bytes` đã đo. Hai caller selector đổi ở 1476/1636; cả hai dùng một helper. `is_file` ở bảng là kiểm verdict sau receipt, KHÔNG phải lọc receipt.

Đối chứng liệt kê cấp OS: `python3 listing_probe.py` trên head/base, hai đường và control/fail, log `listing-*.json`. Head lỗi scandir rc=2 không traceback; base kiem rc=2/không có tệp, base sinh rc=0/`# 0 tệp` (nuốt lỗi). `review_new.py ... late` ở head cho rc=2 sau khi iterator đã yield một mục, không xuất kết quả nợ dở dang.

Hai lỗi resolve thoát traceback là **có sẵn tại base**, các callsite này không được packet sửa. Đọc nguồn provider lỗi khi sinh nợ vẫn rc=0/#42 ở CẢ head/base; không tính finding mới. `_vang.lstat` nuốt EACCES rồi vẫn thử đọc run_json: ở phép tiêm chỉ-lstat, 29 lần đọc thực còn thành công nên rc=0; phép tiêm `run-text` riêng cho rc=2. Không gọi fallback đọc thành công ấy là lỗi đo bị báo sạch. Các nhánh Git/đọc lịch sử bắt lỗi và rc=2 ở cả head/base. Không yêu cầu packet vá các hành vi có sẵn ngoài phần thay đổi.

## Đợt 3 — c100 và đột biến reviewer

`python3 c100_audit.py <1..7> <rig|runtime|value>`: **21/21 tiến trình rc=0**, mỗi lần tiêm dừng ở một trong bảy lần gọi main khi đang thay Path; sau lỗi `Path.is_dir`, `Path.exists`, `Path.iterdir` đều đúng đối tượng gốc; chạy lại c100 `qua`, đối chứng c18 `[true, ""]`. Không đo thấy rò sang ca sau.

Tracer độc lập (`python3 c100_audit.py trace`, log cuối `c100-trace-final`) ghi 7 lần tiêm; bốn lần RuntimeError của chốt (7) đều đúng đối tượng mốc, hit=1, đủ iterdir/is_dir × kiem/sinh. Bản tracer đầu lỗi KeyError vì tưởng closure giữ biến `ten`; log `c100-trace` được giữ và KHÔNG tính là lỗi sản phẩm. Tracer sửa đọc `goc.__name__`; lần đo trung gian gán cờ từ biến vòng lặp cũ làm nhãn .git sai, nên bản cuối lấy argv từ frame main. Chỉ dùng kết quả tracer cuối.

`python3 extra_mutate.py <tên>` (bản sao đủ cây, từng mutant một tiến trình):

| Mutant | Ca c100 | Ý nghĩa |
|---|---|---|
| helper_empty: lỗi trạng thái trả False | giet_that | Không biến lỗi I/O thành vắng |
| helper_pathless: bỏ đường dẫn và chi tiết lỗi | giet_that | Chốt .git còn kiểm thông báo |
| runtime_replaced: ném RuntimeError mới cùng lời | giet_that | Đo đồng nhất đối tượng, không chỉ kiểu/thông điệp |
| injection_noop | gian_giao | dừng do không tiêm trúng, không tính là bắt lỗi sản phẩm |
| injection_runtime_noop | gian_giao | riêng chốt (7) không thể xanh khi không tiêm trúng |
| runtime_same_message: fixture ném đối tượng khác cùng lời | giet_that | Oracle không nhận RuntimeError giả cùng thông điệp |
| narrow_helper: chỉ bắt PermissionError tại helper mới | qua | **SỐNG TOÀN SUITE**, rc=0/97/97 · 149/149 · 2/2; EIO/ESTALE ở guard/helper/.git thoát traceback trên mutant |
| narrow_listing: chỉ bắt PermissionError tại nhánh liệt kê | qua | **SỐNG Ở CÁC CA ĐÍCH** c98/c99/c100/c89; EIO/ESTALE ở scandir thoát traceback trên mutant. Không chạy toàn suite cho mutant này |

Mọi mutant trên có c18 sạch; log `mut-<tên>-cases.stdout` ghi đầy đủ. `python3 errno_probe.py head <mode> <guard|helper|git|listing> <EIO|ESTALE>`: head rc=2 không traceback tại cả sáu tổ hợp đường đi, hit=1; helper trong kiem tiêm vào lần stat THỨ HAI (attempts=2), phân biệt được với guard. Mutant narrow_helper trả rc=1/traceback cho cả bốn tổ hợp trạng thái; narrow_listing trả rc=1/traceback ở hai đường liệt kê. Đây là lỗi bị đưa vào mutant, chưa phải lỗi runtime của head.


## Đợt 4 — toàn suite trên head

`PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 measure.py head suite` đã xong. Tiến trình thật `python3 ops/bien_nhan_v2_test.py` trong `work/head`: **rc=0, 406.32 s**, `97/97 ca đạt · 149/149 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 131/149 đột biến thường khai đối chứng`, `TỔNG: ĐẠT`. Log `evidence/head-suite.{stdout,stderr,json}`; stderr rỗng. Các m148–m153 đều `giet_that` tại c100, m146/m147 vẫn chết ở c99. Không suy pass chỉ từ rc=0.

Phép tiêm ValueError có hai tầng cần phân biệt: tiêm thẳng vào phương thức Path (`errno_probe.py ... value-method`) truyền ra khỏi helper; tiêm sâu hơn vào `os.stat` có thể bị chính `Path.is_dir`/`Path.exists` đổi thành False. Đối chứng `boundary-base-kiem-{guard,git}-value` có cùng hành vi sẵn ở base. Không coi hành vi của pathlib là helper bắt Exception. Log `boundary-head-*` và `boundary-base-*` lưu hai tầng; RuntimeError ở tầng phương thức vẫn truyền nguyên gốc. Điều này không thay kết luận F2 cũ đã vá thật.


## Bảng tiêu chí cuối

| Tiêu chí | Kết quả | Lệnh / output và giới hạn |
|---|---|---|
| Toàn suite head | **ĐẠT** | `python3 measure.py head suite`: rc=0, `97/97 ca đạt · 149/149 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt`, `TỔNG: ĐẠT`; 406.32 s. |
| C1a | **ĐẠT phần đã đo**; Windows **KHÔNG ĐO ĐƯỢC** | `python3 probe.py head behaviors`: C1a rc=1/tổng 2/nêu x; only-x rc=1/tổng 1; mut-exact giết thật c98. |
| C1b | **ĐẠT phần đã đo**; Windows **KHÔNG ĐO ĐƯỢC** | Cùng lệnh: YAML hỏng đuôi hoa rc=2/nêu x/không traceback/không tổng; mut-exact bỏ x và rc=1/tổng 1. |
| C2 | **ĐẠT phần đã đo**; Windows **KHÔNG ĐO ĐƯỢC** | Full suite c89 ĐẠT; `python3 mutate.py isfile --behaviors`: c89 `giet_that`, c18 sạch. |
| C3 | **ĐẠT trên Linux** | `python3 mutate.py glob --behaviors`: c98 `giet_that`, c18 sạch. Không thêm mutant phụ thuộc nền vào bảng thường. |
| C4 | **KHÔNG ĐO ĐƯỢC** | Không có phép đo/log Windows CI độc lập trên exact head; không dùng lời khai executor. |
| C5 | **KHÔNG ĐO ĐƯỢC** | Không có phép đo/log Ubuntu CI độc lập trên exact head; full suite sandbox không được gọi là CI. |
| C6 | **ĐẠT** | `python3 measure.py head gate`: rc=0/tổng 306/TỔNG: ĐẠT; đếm riêng `os.listdir` cho 306; base cũng 306. |
| C7 | **KHÔNG ĐO ĐƯỢC** | Không chạy Windows local. |
| C8 | **KHÔNG ĐẠT** | Còn F3/P3; verdict request_changes trên exact SHA đã neo. |
| C9 | **ĐẠT** | Ruff F delta 0 (cùng F541 đã có ở base); doctrine-scan rc=0/10 tệp/0 chỗ; diff --check rc=0; đúng hai tệp write set; rg glob 0 dòng với đối chứng base 2/mut-glob 1; numstat +40/−5 và +262/−0. |

## Finding còn mở

| ID | Mức | Slug | Phạm vi | Bằng chứng quyết định |
|---|---|---|---|---|
| F3 | P3 | `loi-do-thieu-chot-oserror-ngoai-permissionerror` | c100 mới và c99 nhánh liệt kê của packet | Mutant thu hẹp helper chỉ bắt PermissionError sống toàn suite; oracle độc lập EIO/ESTALE phân biệt head với cả hai mutant thu hẹp. |

- [P3] `loi-do-thieu-chot-oserror-ngoai-permissionerror`: `ops/bien_nhan_v2_test.py:3789` và `:3803` (c100, phép hỏi trạng thái), cùng `:3733` (c99, liệt kê), bảng đột biến `:4656`/`:4669` — `PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 extra_mutate.py narrow_helper --suite` — tiến trình suite trên bản sao mutant **rc=0, 398.14 s**, `97/97 ca đạt · 149/149 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 131/149 đột biến thường khai đối chứng`, `TỔNG: ĐẠT`; nhưng `python3 errno_probe.py mut-narrow_helper sinh helper EIO` **rc=1**, hit=1, `Traceback ... OSError: [Errno 5] review EIO failure`, trong khi cùng lệnh với `head` rc=2, hit=1, `KHÔNG ĐO ĐƯỢC: không đọc được trạng thái ...`, không traceback — mở rộng test bằng OSError không phải PermissionError và thêm mutant thu hẹp catch phải chết đúng chốt.

HÌNH DẠNG: `loi-do`.

**Vì sao đây là thiếu chốt của phần mới:** `_hoi_trang_thai` tại sản phẩm:88–95 hứa và hiện thực đúng hợp đồng OSError. C100 chỉ tiêm PermissionError/EACCES ở cả is_dir và exists, nên không phân biệt bắt toàn OSError với chỉ bắt PermissionError. Mutant reviewer đặt `OSError = PermissionError` cục bộ trong helper trước `return hoi()`; nghĩa bắt lỗi thu hẹp, vẫn giữ nguyên các mốc văn bản m150/m153. Nó không phá rig, không phá import/parity, không bỏ test, và mọi mutant thường vẫn được báo CÓ RĂNG. Đây là chốt hồi quy thiếu răng cho một phần hợp đồng; xếp P3, **không** xếp P2 runtime vì head đang đúng.

**Đủ các đường của cùng lớp:** `errno_probe.py` đo guard kiem, helper trong kiem (stat lần hai), helper trong sinh nợ, `.git` khi thư mục receipt vắng, và scandir trên hai đường. EIO và ESTALE đều rc=2 ở head. `narrow_helper` phá bốn tổ hợp trạng thái; `narrow_listing` (cùng phép thu hẹp trong selector) còn qua c98/c99/c100/c89 và phá hai tổ hợp liệt kê. Mutant listing chưa chạy toàn suite; không suy rằng nó sống toàn suite. Hai mutant cùng một finding, không tách riêng từng biểu hiện để đẩy sang lượt sau.

**Vá ở đâu và thế nào:** thay đổi test `c100` cho các nhánh is_dir/exists và `c99` cho liệt kê, cùng bảng `_dot_bien`. Không cần đổi mã sản phẩm đang đúng. Giữ các ca PermissionError hiện có và thêm tối thiểu `OSError(errno.EIO, ...)`; kiểm hit dương, rc=2, đúng đường dẫn, không traceback trên tất cả đường liên quan. Thêm mutant `except PermissionError` thay `except OSError` ở mỗi helper, đòi chết tại đúng test trong khi c18 còn sạch. Nếu dùng mutant thay catch trực tiếp, cập nhật mốc rig cho đúng; không lấy lỗi mất neo làm tín dụng. Hai phép thu hẹp tương đương giữ neo đã chạy nằm ở `evidence/mut-narrow_helper.patch` và `evidence/mut-narrow_listing.patch`.

**Ca khóa đã chạy ngoài cây:** `python3 io_boundary_oracle.py head` → rc=0/**12/12**; `... mut-narrow_helper` → rc=1/**4/12** (8 phép lỗi trạng thái bị bỏ bắt); `... mut-narrow_listing` → rc=1/**8/12** (4 phép lỗi liệt kê bị bỏ bắt). Script `io_boundary_oracle.py` gọi mỗi phép tiêm bằng tiến trình riêng, đòi hit=1/rc=2/không traceback. Có thể dùng làm đặc tả phản chứng khi bổ sung c99/c100. Lệnh tạo mutant chỉ chạy lần đầu khi đích chưa có; để chạy lại suite trên hiện vật có sẵn: `cd work/mut-narrow_helper && python3 ops/bien_nhan_v2_test.py` với tiền tố môi trường đã nêu.

**Rủi ro khi vá test:** không chọn ENOENT/ENOTDIR làm lỗi bắt buộc rc=2, vì `Path.is_dir` có thể coi đó là vắng thật; không nới catch thành Exception để chữa test. Giữ chốt vắng thật (sinh nợ rc=0/#0), chốt lập trình đúng đối tượng và finally khôi phục monkeypatch. Tầng tiêm phải rõ: lỗi phát từ os.stat có thể được pathlib xử lý trước helper; EIO đã đo truyền qua thực thi Path thật, nên không dựa riêng vào monkeypatch phương thức để giả định điều đó. `ESTALE` là phép bổ sung đã đo, không bắt buộc làm test phụ thuộc nền này nếu bộ Windows thiếu hỗ trợ tương ứng.

## Tính toàn vẹn và giới hạn cuối

`PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 integrity.py` (log `evidence/integrity-run.{stdout,stderr,json}`, dữ liệu chi tiết `evidence/final-integrity.json`) rc=0. Head/tree/base vẫn đúng các neo; `.git` thường, detached, không nông, core.abbrev=7. Status bao gồm tracked/untracked/ignored của `cay-kho` và bản sao head rỗng; diff worktree/index so HEAD rỗng. Hai tệp write set byte-identical với blob HEAD; DIFF.patch và DIFF-LUOT3.patch byte-identical với git diff tương ứng; SPEC SHA-256 đúng neo. Đây là đối chiếu nội dung đầu/cuối, không phải lời khẳng định quan sát toàn bộ lịch sử ghi.

Tất cả tiến trình đo dùng để kết luận đã hoàn tất, không còn phép thử đang chờ. Windows CI/local, Ubuntu CI exact head và lỗi quyền phần cứng/hệ tệp thật: **KHÔNG ĐO ĐƯỢC**; các lỗi I/O trong bảng là phép tiêm có hit kiểm chứng. Không tự dựng nội dung nhạy cảm, không sửa mã nguồn checkout được review, không cấp quyền merge/land.
