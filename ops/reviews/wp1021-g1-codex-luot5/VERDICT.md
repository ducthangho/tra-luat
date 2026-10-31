Verdict: request_changes
Reviewed commit: 3883b607c2167758065e408f0fa6eeb580472015
Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d

Kết luận: **request_changes**. Merge giữ đủ thay đổi hai bên; suite head đạt **98/98 · 151/151 · 2/2**, F1/F2/F3 cũ vẫn đóng. Còn **1 lớp P1 ở kiểm thử cửa sổ M4 của c88**: mutant làm sai biên đầu tệp vẫn qua toàn suite; mutant bỏ citation liền sau cũng qua toàn bộ 98 ca thường. Chỉ ghi trong sandbox, không sửa mã nguồn checkout được review. Chi tiết, giới hạn và gợi ý vá có bằng chứng bên dưới.

## Nhật ký đo tăng dần

Quy ước tái hiện: chạy từ gốc sandbox; mọi tiến trình đo dùng `PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null` (wrapper `measure.py` còn đặt UTF-8). `git config core.abbrev 7` được đặt trước phép đo và được giữ trong các bản sao. Log `.json` cạnh `.stdout/.stderr` ghi lệnh, cwd, rc và thời gian thật. Rc=0 của script thu quan sát không tự có nghĩa mutant chết; verdict dùng trạng thái ca và đối chứng cụ thể.

Đợt 1: `evidence/preflight.json` lưu lệnh/rc/output. Reviewed tree: `c25e25dbcfbfd2a8f584199ec2d6e6dfc26c69a6`. Head, cha 1, cha 2 và origin/master đúng assignment; SPEC khớp băm. `git diff --name-only b29da0b..HEAD` đúng hai tệp write set; `git diff --check b29da0b..HEAD` rc=0.

## GIẢI XUNG ĐỘT

`PYTHONDONTWRITEBYTECODE=1 python3 audit_merge.py` rc=0 (`evidence/merge-audit.json`). Ba patch đầu vào khớp byte với các lệnh `git diff` tương ứng. `git merge-file -p <e9e0048> <merge-base> <b29da0b>` trên tệp test phát đúng **một** xung đột; giữ tuần tự cả hai thân, đổi tên định nghĩa/đích m142/docstring c99 ⇒ **byte-identical với HEAD**. Merge-base là `757bde561d09738858506aecf5de2f050a5f0d5e`.

- So cha 1: `ops/bien_nhan_v2.py` không đổi byte. Tệp test nhận ba import contextlib/io/traceback, ca c98 của #1037, các hàm in chi tiết/vị trí ngoại lệ, tham số `chi` và dây in của `_dot_bien`; thêm đúng ba thay tên đã nêu. Ngoài `_chay_1` và `_dot_bien`, mọi hàm cũ còn nguyên sau chuẩn hóa tên.
- So cha 2: nhận đúng thay đổi #1021 của `DIFF.patch`: mã sản phẩm +40/−5, test +281/−0. Mọi hàm #1037 nguyên byte; chỉ `_dot_bien` được bổ sung đăng ký m142–m155. Không mất hàm của bên nào.
- Đếm AST: cha 1 **97 ca / 153 đăng ký**, cha 2 **95 ca / 139 đăng ký**, HEAD **98 ca / 153 đăng ký**. Tên ca, số tiền tố ca và tên đột biến không trùng. 153 gồm 151 thường + 2 tự kiểm (đã đối chiếu bằng output suite bên dưới). Mọi đăng ký của từng cha khớp AST sau đổi tên; chuỗi `c98_chon_bien_nhan_` vắng hoàn toàn ở head.

`python3 run_checks.py` đã chạy riêng `_dot_bien(chi={tên})` cho **m140–m155**, mỗi tên một tiến trình: tất cả rc=0, đúng một hàng, `giet_that`, có đối chứng. m142 trỏ c101; m147/m155 trỏ c99; m154 trỏ c100. Bốn lượt tiêm AttributeError vào đúng ca đích của m142/m147/m154/m155 đều in `KHÔNG RĂNG`, `chi tiết [tin_dung_gia]`, `AttributeError: review_merge_trace_sentinel` và vị trí `focused_merge.py:11 in reviewer_throw`; không nhận tín dụng giết giả. Log `evidence/focused-*.{json,stdout,stderr}`; phép focused không được gọi là toàn suite.

## C88 CỬA SỔ M4 — phép đo hành vi head

`python3 window_probe.py head --gate` (qua `measure.run`, `evidence/window-head.*`) rc=0: **71/71 phép trực tiếp và 71/71 fixture git thật qua cổng đúng kỳ vọng**. Ma trận độc lập đặt provider/citation ở khoảng cách −3…+3, dòng giữa; đầu tệp j=0 và cuối tệp; một/hai/ba dòng; dòng trống, khoảng trắng/tab, nhiều khai báo cùng dòng và gần nhau. Expected được ghi riêng trong script theo hợp đồng ba dòng. Output: `SUMMARY {"total":71,"direct_pass":71,"gate_pass":71,"failed":[]}`. Chưa thấy lỗi hành vi sản phẩm ở head trên tập này. Kết quả đột biến bên dưới cho thấy ma trận head xanh chưa chứng minh c88 đủ răng.

## Tiêu chí đã đo

`python3 run_checks.py` ghi lệnh/rc/output vào `evidence/`:

- C1a/C1b: `probe.py head behaviors` chạy fixture thật; hai tệp hợp lệ YAML sai schema ⇒ rc=1/tổng 2/nêu x; chỉ x ⇒ rc=1/tổng 1; YAML hỏng đuôi hoa ⇒ rc=2/stderr nêu x/không traceback. Log `head-behaviors.*` và `fixture-head-*`.
- C6: head và base chạy `python3 ops/bien_nhan_v2.py --root .` đều rc=0, tổng 306, `TỔNG: ĐẠT`. `receipt-count.stdout` đếm riêng casefold=306/exact=306.
- C9: Ruff F **đỏ sẵn**, head/base cùng F541 ở cùng nội dung dòng; `ruff-delta.json` xác nhận delta=0. Doctrine head/base rc=0: 10 tệp, 0 chỗ chép doctrine. `no-glob` rc=1/0 dòng. Không gọi Ruff sạch.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn lịch sử: `VERDICT-LUOT4.md` trên `e9e0048b48ab610fee1246368b4f134c1ac4ae76`. Kết quả dưới đây đo lại trên head mới, không lấy verdict cũ làm bằng chứng pass.

| Lớp lịch sử | Kết quả trên head mới | Phép đo |
|---|---|---|
| F1/P2 `loi-do-liet-ke-thu-muc-thoat-traceback` | Vẫn đóng trong phạm vi đã đo | `run_old_findings.py`: PermissionError ở trạng thái/liệt kê và iterator yield rồi lỗi trên cả kiem/sinh ⇒ rc=2, không traceback; `mutation_probe.py m147` trên bản sao đầy đủ ⇒ c99 giet_that, c18 sạch. |
| F2/P3 `loi-do-thieu-chot-ngoai-le-lap-trinh` | Vẫn đóng trong phạm vi đã đo | `boundary_oracle.py head` ⇒ cả hai đường truyền đúng đối tượng RuntimeError, hit=1, restored=true; `review_new.py error-child head <kiem\|sinh> <runtime\|value>` ⇒ rc=1/traceback đúng lỗi lập trình; focused m152/m153 chết đúng c100. |
| F3/P3 `loi-do-thieu-chot-oserror-ngoai-permissionerror` | Vẫn đóng trong phạm vi đã đo | `errno_probe.py head <mode> <site> <EIO\|ESTALE>`: 12/12 tiến trình rc=2, hit=1, không traceback, đủ guard/helper/git/listing. `mutation_probe.py m154` ⇒ c100 giet_that vì OSError errno 5; m155 ⇒ c99 giet_that vì errno 5; c18 đều sạch. Tracer c99/c100 xác nhận thực sự ném OSError thuần, không chỉ PermissionError. |

Cả ba lớp F1/F2/F3 có hình dạng `loi-do`; không mở lại bởi merge. Log chi tiết `evidence/errno-*`, `old-*`, `boundary-head.*`, `trace-*`, `mut-m147*`, `mut-m154*`, `mut-m155*`. Các lỗi I/O là lỗi tiêm có hit kiểm chứng.

### C2/C3 và chạy lại đột biến trên bản sao đủ cây

`python3 run_mutants.py` chạy mỗi mutant một tiến trình. `work/mutation` là bản sao đủ cây gồm `.git`; mỗi tiến trình sửa đúng mẫu duy nhất trên bản sao, chạy ca/đối chứng khi mutant còn hiệu lực, băm lại, rồi phục hồi. Patch và kết quả giữ trong `evidence/mut-*.patch` và `mut-*-result.json`.

| Mutant | Ca đích / đối chứng |
|---|---|
| m142 — so đuôi chính xác | c101 **giet_that**; c99 cũng đỏ; c18 sạch |
| m143 — thêm is_file | c89 **giet_that**; c18 sạch; C2 đạt |
| m147 — bỏ bắt lỗi liệt kê | c99 **giet_that**; c18 sạch |
| m154 — chỉ bắt PermissionError ở trạng thái | c100 **giet_that** với EIO; c18 sạch |
| m155 — chỉ bắt PermissionError ở liệt kê | c99 **giet_that** với EIO; c18 sạch |
| glob — hoàn nguyên selector | c101/c99 **giet_that**, c18 sạch; C3 đạt. c100 là `gian_giao` do không gọi iterdir, **không tính** làm tín dụng giết. |

### Toàn suite head đã hoàn tất

`PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 measure.py head suite` chạy lệnh `python3 ops/bien_nhan_v2_test.py` trong bản sao đủ cây `work/head`: **rc=0, 375.16 s**, stderr rỗng (`evidence/head-suite.*`):

```text
bien_nhan_v2_test: 98/98 ca đạt · 151/151 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 133/151 đột biến thường khai đối chứng
TỔNG: ĐẠT
```

So cha 2 chi tiết mã sản phẩm: thêm `_hoi_trang_thai` (chỉ đổi OSError thành KhongDoDuoc) và `_chon_bien_nhan` (iterdir/lower/endswith/sorted, không lọc is_file); kiem dùng helper cho hai câu hỏi trạng thái và selector, thông báo rỗng nêu phép so không phân biệt hoa thường; `_sinh_no` dùng cùng selector. Test thêm import errno, c101/c99/c100 và m142–m155. Đây là toàn bộ delta #1021; `audit_merge.py` đã chứng minh phần #1037 còn nguyên.

### C88 — 40 đột biến reviewer

`python3 run_mutants.py` / `python3 mutation_probe.py <tên>`; bảng máy `evidence/window-mutations-summary.json`. **40/40** mutant có đối chứng c18 sạch và băm nguồn không đổi suốt phép đo. Mỗi mutant chạy tiến trình riêng trên bản sao đủ cây. Không tuyên bố tập hữu hạn này vét cạn mọi biểu thức Python tương đương.

| Nhóm | Số | Kết quả ca c88 / oracle độc lập |
|---|---:|---|
| Cận trái L ∈ {−3,−2,−1,0,+1}, cận phải R ∈ {0,1,2,3,4}, `max(0,j+L):j+R`, trừ cặp đúng (−1,2) | 24 | Tất cả c88 **giet_that**; bao gồm nới/thu hẹp/lệch sang trước/sau và cửa sổ rỗng |
| Lấy mọi dòng trước / mọi dòng sau / toàn tệp / loại dòng trắng / bỏ dòng khai ở EOF | 5 | Tất cả c88 **giet_that** |
| Nới riêng provider hoặc riêng citation sang trước/sau hai dòng | 4 | Tất cả c88 **giet_that**; xác nhận cả bốn phản chứng cũ đã được khóa |
| Bỏ provider trên chính dòng khai; bỏ citation dòng trước | 2 | c88 **giet_that** |
| `no_clamp`: bỏ chặn chỉ số âm ở đầu tệp | 1 | **SỐNG** ở c88/c79/c83; oracle chỉ 66/71 đúng |
| `skip_first`: bỏ qua khai báo j=0 | 1 | **SỐNG** ở c88/c79/c83; oracle chỉ 63/71 đúng |
| `citation_drop_next`: bỏ citation dòng ngay sau | 1 | **SỐNG** ở c88/c79/c83; oracle chỉ 65/71 đúng |
| `citation_drop_self`: bỏ citation cùng dòng | 1 | SỐNG ở c88 nhưng **c79 giet_that**, nên không phải lỗ hổng không được bộ ca bắt |
| `reverse_equivalent`: đảo thứ tự ba dòng trong cửa sổ | 1 | SỐNG; oracle 71/71. Tương đương với hai phép `any`, không phải lỗi |

Tổng: c88 giết 35/40; 5 sống tại c88 gồm 1 tương đương, 1 được c79 bắt, 3 mutant sai hành vi cần kiểm tiếp toàn bộ ca. Kết quả xác nhận cuối: `no_clamp` sống qua toàn suite 98/98 · 151/151 · 2/2; `citation_drop_next` sống qua toàn bộ 98/98 ca thường. Chỉ mutant đầu đã được chạy cả bảng đột biến; không gán kết quả whole-suite đó cho mutant thứ hai.

## Bảng finding — cập nhật sau phép đo ma trận

- [P1] bien-ngoai-cua-so-surface-chua-co-rang: `ops/bien_nhan_v2_test.py:2981` (ma trận c88), `:3001` (prefix che j=0); chốt sản phẩm `ops/bien_nhan_v2.py:1310–1311` — `python3 mutation_probe.py no_clamp` và `python3 mutation_probe.py citation_drop_next` — c88/c79/c83 đều `qua`, c18 sạch, trong khi oracle độc lập lần lượt chỉ 66/71 và 65/71 — bổ sung fixture thật bắt đầu tại dòng 0, citation ở dòng ngay sau và đăng ký đột biến riêng; gợi ý đã đo trong `HINT.patch`.

  HÌNH DẠNG: `bo-chon-ung-vien`.

  **Một lớp, hai biểu hiện còn mở** (biên đầu tệp; citation phía sau). Giữ slug lịch sử để nối P1 lượt 7; không coi số dòng tăng hoặc m140/m141 xanh là đóng mọi biên của lớp này. Đây là thiếu răng kiểm thử; chưa thấy sản phẩm head sai trên 71 fixture độc lập.

  **Biểu hiện A — đầu tệp.** Tất cả nội dung c88 đều được thêm `verdict: approve` và một dòng trống, nên không có khai báo ở j=0. Mutant `no_clamp` chèn `max = lambda lower, value: value` ngay trước dòng cắt cửa sổ, giữ nguyên dòng neo đột biến cũ: ở j=0 nó lấy chỉ số âm, có thể bỏ lời tự khai sai hoặc đọc sai cửa sổ. `skip_first` là phản chứng cùng biểu hiện. Witness `edge-j0-n3-provider-+1`: dòng 0 là khai báo khác run.json, dòng 1 có provider, dòng 2 trung tính; head có L-SURFACE/rc=1, mutant bỏ qua/rc=0. `window_probe.py mutation --gate` trên bản `no_clamp` (`window-no-clamp.*`) xác nhận **67/71** fixture git thật đúng, bốn fixture ra sai mã; oracle trực tiếp **66/71** vì thêm một ca nhiều khai báo vẫn có một vi phạm khác nên rc chưa phân biệt được. Không dùng rc đơn lẻ để che mất một surface.

  **Biểu hiện B — citation phía sau.** c88 chỉ có citation liền trước, hoặc cách hai dòng; c79 có citation cùng dòng. Không ca nào trong ba ca này bắt việc bỏ riêng citation ở dòng kế tiếp. Mutant `citation_drop_next` chỉ đổi tập xét `_RE_TRICH_DAN`, giữ nguyên tập provider. Witness `text-citation-+1`: provider + khai báo sai ở cùng dòng, citation ở dòng ngay sau; head loại khỏi lời tự khai, mutant báo sai L-SURFACE. Ma trận trực tiếp bắt sáu ca sai, còn c88/c79/c83 đều qua.

  **Hướng vá đã thử trong sandbox.** `HINT.patch` bỏ prefix cố định khỏi các fixture c88 (nhờ đó các hàng sẵn có thực sự chạm j=0), thêm hàng citation liền sau, thêm m156/m157 để khóa hai chốt. `python3 hint_probe.py create` rc=0: c88 head qua; m140/m141/m156/m157 đều `giet_that`, có đối chứng. `hint_probe.py <tên>` thử lại 40 mutant: sau hint, 38 mutant sai bị c88 bắt, `citation_drop_self` bị c79 bắt, `reverse_equivalent` vẫn qua. Không yêu cầu mutant tương đương phải chết. Các log `hint-*` lưu bằng chứng; chưa chạy toàn suite cho HINT và chưa áp HINT vào checkout được review. Executor cần tự tái dẫn xuất, chạy toàn suite/CI trên head mới.

  Ghi nhận lỗi của script reviewer: lần đầu `hint_probe.py citation_drop_self` đòi c88 tự giết dù đã biết c79 bắt mutant này; assertion reviewer sai. Giữ log `initial-hint-citation_drop_self.*`, sửa phép kiểm để ghi và đòi c79 `giet_that`, chạy lại rc=0. Không tính lần lỗi oracle đó là lỗi sản phẩm hay tín dụng giết.

### Xác nhận survivor qua toàn suite

`python3 mutation_probe.py no_clamp --suite` (wrapper `confirm-no-clamp.json`) rc=0. Lệnh con `python3 ops/bien_nhan_v2_test.py` trong cây đầy đủ đang mang đột biến: **rc=0**, stderr rỗng, `evidence/mut-no_clamp-suite.*`:

```text
bien_nhan_v2_test: 98/98 ca đạt · 151/151 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 133/151 đột biến thường khai đối chứng
TỔNG: ĐẠT
```

`mut-no_clamp-result.json` xác nhận băm sản phẩm trước/sau suite giữ nguyên; c18 sạch khi mutant đang hiệu lực. Dòng `max = lambda lower, value: value` chỉ thay clipping cận trái; dòng cắt cửa sổ gốc được giữ để m113/m140/m141 vẫn áp đúng mẫu. Vì thế đây là **SỐNG QUA TOÀN SUITE**, không phải rc=0 do bỏ chạy bảng đột biến hoặc lỗi giàn giáo. Witness git thật ở `window-no-clamp.*` đã chứng minh mutant sai hành vi.

**Kết luận riêng P1 lượt 7:** xác nhận `fc73522` đã vá thật bốn phản chứng ngoài cửa sổ ở khoảng cách ±2 (provider và citation); m140/m141 chết đúng c88, kể cả phép reviewer đổi riêng từng bộ lọc. Tuy nhiên **bác kết luận đóng toàn bộ lớp cửa sổ M4**: biên đầu tệp và citation liền sau vẫn chưa được khóa. Một lớp P1 với hai biểu hiện còn mở; nối cùng slug lịch sử. Việc này thuộc phần c88 được chỉ thị bổ sung cho lượt 5, không phải lỗi giải xung đột #1021/#1037.

## Bảng tiêu chí

| Tiêu chí | Kết quả | Lệnh / output quyết định |
|---|---|---|
| Đúng head/spec/phạm vi | ĐẠT | `preflight.json`, `audit_merge.py`: OID 40 ký tự/băm đúng; hai tệp; diff-check rc=0 |
| Giải xung đột | ĐẠT | `audit_merge.py`: 1 conflict; giữ cả hai + 3 đổi tham chiếu ⇒ khớp byte; 98 ca, 151 thường + 2 tự kiểm; không trùng/tên cũ |
| Suite head | ĐẠT | `measure.py head suite`: rc=0, 98/98 · 151/151 · 2/2, TỔNG: ĐẠT |
| #1037 với m142–m155 | ĐẠT | `focused_merge.py <m142…m155> real` đúng một hàng `giet_that`; 4 phép fake ghi đủ chi tiết/vị trí, `tin_dung_gia`, không được nhận CÓ RĂNG |
| C1a | ĐẠT phần đo; Windows KHÔNG ĐO ĐƯỢC | `probe.py head behaviors`: tổng 2/nêu x/rc=1; chỉ x tổng 1/không “không có tệp”; `mutation_probe.py m142` giết c101 |
| C1b | ĐẠT phần đo; Windows KHÔNG ĐO ĐƯỢC | YAML hỏng đuôi hoa rc=2/stderr nêu x/không traceback; mutant exact chết c101 |
| C2 | ĐẠT phần đo; Windows KHÔNG ĐO ĐƯỢC | c89 qua trong suite; `mutation_probe.py m143` c89 giet_that, c18 sạch |
| C3 | ĐẠT phép hoàn nguyên được yêu cầu | `mutation_probe.py glob` c101/c99 giet_that; c18 sạch; không lấy c100 gian_giao làm tín dụng |
| C4 Windows CI | KHÔNG ĐO ĐƯỢC | Không có phép đo độc lập job/runner/log exact head trong lượt này |
| C5 Ubuntu CI | KHÔNG ĐO ĐƯỢC | Suite vừa chạy không chứng minh job CI; không có phép đo độc lập CI exact head |
| C6 | ĐẠT | Head/base gate rc=0, tổng 306/TỔNG: ĐẠT; os.listdir đếm riêng 306 |
| C7 Windows local | KHÔNG ĐO ĐƯỢC | Không chạy Windows local; không suy kết quả từ lời khai executor |
| C8 nội dung review | KHÔNG ĐẠT | 1 lớp P1 còn mở trong phần c88; request_changes |
| C9 | ĐẠT | Ruff F delta 0 (đỏ sẵn F541); doctrine rc=0/10 tệp/0 chỗ; diff-check rc=0; glob 0 dòng; numstat +40/−5 và +281/−0 |
| C88 hành vi head | ĐẠT tập đã đo | `window_probe.py head --gate`: 71/71 trực tiếp và 71/71 git thật |
| C88 răng kiểm thử | KHÔNG ĐẠT | `no_clamp` sai trên witness nhưng vẫn toàn suite xanh; P1 ở trên |

**Tổng finding mở: P0=0, P1=1 lớp (2 biểu hiện), P2=0, P3=0.** Không cấp quyền merge/land.


### Xác nhận biểu hiện citation và toàn vẹn cuối

`python3 mutation_probe.py citation_drop_next --all-cases` (`evidence/confirm-citation-drop-next.*`) **rc=0, 208.20 s**: `ALL_CASES {"total":98,"passed":98,"failed":[]}`. Băm sản phẩm giữ nguyên, c18 sạch. Đây là toàn bộ **ca thường**, không phải lượt toàn suite có 151 đột biến. `python3 witness_citation.py` dựng lại cùng mutant trên bản sao đầy đủ rồi chạy `window_probe.py focus --gate`: phép kiểm oracle rc=1, **65/71 trực tiếp và 65/71 git thật đúng**, sáu fixture phát hiện hành vi sai; mọi lỗi là L-SURFACE, không phải giàn giáo. Log `window-citation-drop-next.*`, bảng `citation-gate-summary.json`.

`python3 validate_review.py` **rc=0**, output `ALL REVIEW ASSERTIONS PASS; 5 trees clean; 20 inherited scripts unchanged`. `evidence/final-validation.json` đối chiếu tự động số đếm suite, ca đích mutant/đối chứng, 12 phép EIO/ESTALE, tracer, C1/C6/C9, 40 mutant, 40 phép hint, bốn đột biến hint chạy riêng từng tiến trình, cùng snapshot cuối:

- `cay-kho`, `work/head`, `work/focus`, `work/mutation` vẫn ở exact head dòng 2/tree `c25e25dbcfbfd2a8f584199ec2d6e6dfc26c69a6`; `work/base` ở `b29da0bfe3bfb7a7be69136a1c5c40f82c088a93`.
- Cả năm cây: tracked/untracked/ignored sạch, diff worktree/index rỗng, không nông, `core.abbrev=7`; hai tệp nguồn khớp từng byte với blob HEAD. Snapshot đầu ghi tracked/untracked; ignored ở đầu lượt không được ghi riêng. Snapshot cuối không chứng minh toàn bộ lịch sử ghi trong lúc chạy; các bản sao phục vụ đột biến đã được phục hồi sau phép đo.
- SPEC giữ đúng SHA-256 dòng 3; 20 script `luot4-probe` được chép ra gốc sandbox giữ nguyên byte. Các script mới và HINT chỉ nằm trong sandbox. `git apply --check HINT.patch` trên bản sao rc=0; không áp lên `cay-kho`.

Các tiến trình đo đã kết thúc. **Verdict cuối: request_changes**, vì một lớp P1 M4 còn mở; phần giải xung đột và F1/F2/F3 không phát hiện hồi quy. Windows CI/local, Ubuntu CI exact head và toàn suite của HINT: **KHÔNG ĐO ĐƯỢC / chưa chạy**, không được suy là pass. Không cấp quyền merge/land.
