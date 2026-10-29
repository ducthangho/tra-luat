Verdict: request_changes
Reviewed commit: b2e2410a4b9215480aee6771c1ba8a15a6e14160
Spec sha256: e1e709be14e2e7c2a81de39c3acf2666c746e7146116dee669cadee4dad8ed19

Có **1 finding P2**: bộ kiểm chưa khóa riêng độ đúng của nhánh tiêm theo M4. Hai đột biến trong phần test mới vẫn qua toàn suite. Hành vi hiện tại của nhánh tiêm đạt các phép đo độc lập; finding là lỗ hổng kiểm hồi quy, không phải kết luận đã thấy lỗi chạy Windows. Áp ngưỡng không còn P0/P1/P2/P3 nên chưa approve. Không cấp quyền merge/land.

**Finding**

- [P2] nhanh-tiem-thieu-chot-tu-kiem: `ops/bien_nhan_v2_test.py:3114`, `:3483`, `:4212`, `:4249` — Tái hiện: `python3 review_probe.py wrong_module_native --full` và `python3 review_probe.py lstat_no_restore --full` với môi trường bên dưới — Cả hai đều in `93/93 ca đạt · 137/137 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt`, `TỔNG: ĐẠT`, `FULL_RC 0`. Đột biến thứ nhất chỉ đổi `mod = bnv2` thành `mod = _BNV2_THAT`; đột biến thứ hai bỏ hoàn nguyên `Path.lstat`, kết thúc với `RESTORE Path.lstat= False`. M4 yêu cầu bổ sung phép đột biến ép nhánh tiêm trên POSIX, nhưng m116/m125 hiện chết trước ở nguồn thật nên không bảo vệ được phần này. Hướng vá: bổ sung kiểm riêng nhánh tiêm ngay trong tệp test, có đối chứng dương trên module đã thay nhưng giữ nguyên hành vi, rồi áp m116/m125; kiểm callback thực sự được gọi và khôi phục identity cả khi thân ca ném lỗi. Không sửa sản phẩm.

Bằng chứng chi tiết cho finding:

| Lệnh từ sandbox | Output quan trọng | Ý nghĩa / log |
|---|---|---|
| `python3 review_probe.py native_m116` | `giet_that run_json_ten_qua_dai/khong-no ... rc=0` | m116 chết trước nguồn tiêm; [log](evidence/native_m116.log). |
| `python3 review_probe.py native_m125` | `giet_that merge-base/path ... rc=1` | m125 chết trước biến thể `tiem`; [log](evidence/native_m125.log). |
| `python3 review_probe.py wrong_module_native --full` | `93/93`, `137/137`, `TỔNG: ĐẠT`, `FULL_RC 0` | Đột biến vá nhầm module **SỐNG**; [diff đúng một dòng](evidence/wrong-module.diff), [log toàn suite](evidence/wrong_module_native-full.log). |
| `python3 review_probe.py swapped_control` | `BEHAVIOR_IDENTICAL_MODULE_SWAP True`; c96 `qua`; c18 `(True, '')` | Thay module bằng `_dot_bien_tep` chỉ sửa docstring, ép đường tiêm, mã test hiện tại vẫn đúng; [log](evidence/swapped_control.log). |
| `python3 review_probe.py wrong_module_swapped_control` | Cùng phép thay module vô hại; c96 `giet_that merge-base/tiem ... rc=1`; c18 `(True, '')` | Lỗi ở chính rig tiêm: git thật chạy, thiếu `rc=3`. Đối chứng này phân biệt được việc vá nhầm module mà suite thường bỏ lọt; [log](evidence/wrong_module_swapped_control.log). |
| `python3 review_probe.py lstat_no_restore --full` | `93/93`, `137/137`, `FULL_RC 0`, `RESTORE Path.lstat= False` | Đột biến không gỡ vá **SỐNG** ngay cả khi đã tắt nguồn thật; [log](evidence/lstat_no_restore-full.log). |

Ca khóa sau vá phải bắt được cả hai đột biến trên. Giữ các phép đo thật của POSIX và đối chứng sản phẩm sạch; không dùng việc một ca đỏ bất kỳ làm bằng chứng. Cần phân biệt lỗi giàn giáo tiêm với lỗi sản phẩm: nếu đối chứng trên module giữ nguyên hành vi đã đỏ thì không được ghi tín dụng giết m116/m125. Việc bổ sung ca phải cập nhật số đếm thực, và mọi vá toàn cục phải nằm trong `try/finally` để tránh làm hỏng ca sau.

**Cách tái lập và phạm vi**

Các lệnh Python/Git đo fixture dùng:

```sh
export PYTHONDONTWRITEBYTECODE=1
export GIT_CONFIG_GLOBAL=/dev/null
export GIT_CONFIG_SYSTEM=/dev/null
git -C cay-kho config core.abbrev 7
```

`base/` được giải bằng `git -C cay-kho archive e9967f07b95c6458afc63dabf4a5c0494e90eca7 | tar -x -C base`. `probe-tree/` được giải bằng `git archive HEAD`. Cả hai có đầy đủ cây, gồm `.claude/dev/launcher.py`; trước lượt toàn suite hợp lệ, bổ sung bản sao `.git` độc lập, ghim `core.abbrev=7`, và đưa HEAD/index của base về base bằng `git reset --mixed`. Nội dung archive không bị thay. `git status --short` của hai cây khi dựng xong rỗng.

[review_probe.py](review_probe.py) biến đổi nguồn test trong bộ nhớ, lưu bản nguồn từng biến thể vào `evidence/<mode>.test.py`, và giữ `__file__` trỏ vào cây đầy đủ. Đột biến sản phẩm dùng `_dot_bien_tep` cùng chốt parity/nguồn phụ có sẵn. Không dùng bản sao chỉ có `ops/`. Với lệnh nhắm ca, rc=0 của harness chỉ là phép đo hoàn thành; kết quả thực nằm ở `RESULT` và thông báo. Với `--full`, đọc thêm `FULL_RC`. Quy ước từng biến thể: [evidence/README.txt](evidence/README.txt).

**Gate và đối chiếu base**

| Phép đo / lệnh | Kết quả độc lập |
|---|---|
| `(cd cay-kho && python3 ops/bien_nhan_v2_test.py)` | rc=0; `93/93 ca đạt · 137/137 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 119/137 đột biến thường khai đối chứng`; `TỔNG: ĐẠT`. [Log](evidence/head-selftest.log). |
| `(cd base && python3 ops/bien_nhan_v2_test.py)` sau khi bổ sung lịch sử | rc=0, cùng toàn bộ số đếm trên, `TỔNG: ĐẠT`. [Log](evidence/base-with-history-selftest.log). |
| Lượt base archive ban đầu, chưa có `.git`, cùng lệnh | rc=1, `89/93`, `136/137`, `TỔNG: ĐỎ`. c1/c40/c14/c76 và m49 hỏng vì thiếu kho thật. Đây là lỗi giàn giáo đã khắc phục, không phải hồi quy. [Log](evidence/base-selftest.log). |
| `python3 review_probe.py forced --full` | Tắt nguồn tên dài thật và coi probe PATH thất bại, sản phẩm nguyên: `93/93`, `137/137`, `TỔNG: ĐẠT`, `FULL_RC 0`; hai identity đều được trả lại. [Log](evidence/forced-full.log). |
| `git -C cay-kho diff --check e9967f07b95c6458afc63dabf4a5c0494e90eca7 HEAD` | rc=0, không output. |
| `ruff --version`; `ruff check --no-cache --select F --output-format json .` trên từng cây; `python3 ruff_delta.py` | Ruff `0.16.9`; lint cả hai rc=1 vì **9160 lỗi nền**; riêng tệp đổi cùng 1 lỗi. So `(path, code, message)` với số lần xuất hiện: `new=[]`, `removed=[]`, delta=0, script so rc=0. Đây là bare lint, không phải kiểm pin Ruff của CI. [Kết quả](evidence/ruff-delta.log). |
| `(cd cay-kho && python3 .claude/dev/packet_loop.py doctrine-scan --root .)` | rc=0; `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`. [Log](evidence/doctrine.log). |
| `(cd cay-kho && python3 ops/bien_nhan_v2.py --root .)` | rc=0; `244 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 297`; `TỔNG: ĐẠT`. [Log](evidence/product.log). |
| `sh evidence/scope-check.sh`; đối chiếu `DIFF.patch` với diff thực | rc=0; HEAD và base khớp đầu vào; tree head `2aef829dd380df544c4216fb0aea1429d1069673`; clone không nông; chỉ `ops/bien_nhan_v2_test.py` đổi. Diff khớp byte. Status cuối, kể cả ignored/untracked, rỗng. [Log](evidence/scope-check.log), [identity](evidence/identity.json). |
| `sha256sum cay-kho/ops/bien_nhan_v2.py base/ops/bien_nhan_v2.py` | Cùng `82a667496adc4ebbe9516f484fc4d9da4e79570ac20006b122a7400d0be539f6`; sản phẩm không đổi. |

Các phép đột biến và hiện vật review nằm ngoài `cay-kho/`. Snapshot/status sạch chỉ chứng minh không có delta quan sát được; thay đổi cấu hình `core.abbrev=7` được thực hiện đúng chỉ thị.

**Gốc CRLF: đã tái hiện đúng hai SHA**

| Lệnh | Commit SHA | Blob SHA | Kết quả c93 |
|---|---|---|---|
| `python3 review_probe.py lf` | `e4a3f5d511d31dfb809024edcde68c4602cd02f1` | `e4a3f5daa164ce057bf3ad4a93b1431146ec5a30` | `qua`; chung tiền tố `e4a3f5d`. [Log](evidence/lf.log). |
| `python3 review_probe.py crlf` | `5cfd3f5e87ecd0877a62d75e22c3cf005d842524` | `70363d663b5f549bdc70e2b0ce3838c2ad43ffd7` | `gian_giao fixture: commit/blob không chung tiền tố`, khớp chính xác cặp trong packet. [Log](evidence/crlf.log). |

Biến thể CRLF ghi byte `a\r\n`, `x\r\n`, `m\r\n` và blob CRLF; không dựa vào phép chuyển newline của hệ điều hành. Đây là bằng chứng cho gốc lỗi (1), không phải phép chạy Windows.

**Răng của nhánh tiêm và các đột biến bổ sung**

| Lệnh | Ca, nhánh, thông báo thực |
|---|---|
| `python3 review_probe.py forced` | c91/c93/c96 đều `qua`; c91 ghi hai nhánh tên dài không dựng được, c96 ghi hai nhánh PATH không bọc được. [Log](evidence/forced.log). |
| `python3 review_probe.py forced_m116` | c91 `giet_that run_json_lstat_loi_tiem/khong-no ... đòi rc=2 ... được rc=0: ''`; c18 `(True, '')`. Đúng lỗi coi OSError là vắng, không chết vì launcher/fixture. [Log](evidence/forced_m116.log). |
| `python3 review_probe.py forced_m125` | c96 `giet_that merge-base/tiem ... đòi rc=2 ... rc=3, được rc=1`, lỗi L-ANCESTRY thay cho trạng thái không đo được; c18 `(True, '')`. [Log](evidence/forced_m125.log). |
| `python3 review_probe.py native_m120` | c93 `giet_that ... được rc=2 ... OID e4a3f5d mơ hồ — 2 commit chung tiền tố`; c18 `(True, '')`. [Log](evidence/native_m120.log). |
| `python3 review_probe.py lstat_no_hit` | Bỏ khớp lstat: c91 **CHẾT**, đúng `run_json_lstat_loi_tiem/khong-no`, rc=0 thay vì 2. [Log](evidence/lstat_no_hit.log). |
| `python3 review_probe.py git_no_hit` | Không tiêm lệnh git: c96 **CHẾT**, đúng `merge-base/tiem`, rc=1 thay vì 2. [Log](evidence/git_no_hit.log). |
| `python3 review_probe.py git_all` | Tiêm mọi lệnh: c96 **CHẾT**, `merge-base/tiem` nhận lỗi của `git rev-parse --is-shallow-repository rc=3`; thiếu đúng tên `merge-base`. Đây là chốt chọn đúng lệnh đang đo. [Log](evidence/git_all.log). |
| `python3 review_probe.py unwrappable`; `python3 review_probe.py probe_always_true` | Đặt script tên không được PATH tìm thấy: đối chứng c96 `qua` bằng tiêm. Khi bỏ chốt probe: c96 **CHẾT** ở `merge-base/path`, rc=1 thay vì 2. [Đối chứng](evidence/unwrappable.log), [đột biến](evidence/probe_always_true.log). |

Hai đột biến **SỐNG toàn suite** là `wrong_module_native` và `lstat_no_restore`, đã nêu trong finding. Không tính ngoại lệ vô can là tín dụng giết mutant.

**Xanh rỗng, khôi phục và cách đọc số đếm**

`python3 branch_probe.py` rc=0: c91/c96 `qua`; trace ghi hai lần callback lstat đến từ `_vang`, hai lệnh git khớp mẫu đến từ `_git_do`, cùng **10 lệnh không khớp đi git thật**. Đổi `_vang` sang `p.stat()` và chỉ giữ nguồn tiêm làm c91 `giet_that ... run_json_lstat_loi_tiem/khong-no ... rc=0`. Không thấy xanh rỗng ở các phép đo cô lập của mã hiện tại. [Log](evidence/branch.log), [trace](evidence/branch-events.json).

`python3 cleanup_probe.py` rc=0: ném `Sentinel` ngay trong thân CLI của nhánh tiêm; kiểm cả c91/c96 trên module gốc và module đã thay. Cả bốn lượt `hits=1`, `lstat_restored=True`, `git_restored=True`, `original_module_intact=True`; context lstat trực tiếp cũng được khôi phục khi ném lỗi. Nhãn `tin_dung_gia` ở log này là do ngoại lệ reviewer chủ động ném, không phải mutant sản phẩm bị giết. Mã hiện tại khôi phục đúng; suite chưa bắt được việc gỡ khôi phục như finding đã chứng minh. [Log](evidence/cleanup.log).

`python3 review_probe.py forced --full` vẫn cho `93/93` trong khi log có `GHI CHÚ c91 run_json_ten_qua_dai/{khong-no,co-no}` và `GHI CHÚ c96 {merge-base,is-shallow-repository}/path`. Dòng ghi chú đủ xác định nhánh thật không đo được khi đọc toàn log; **93/93 chỉ đếm hàm ca, không đếm nhánh thật/tiêm**. Không được dùng riêng dòng tổng để nói đã đo đủ mọi nhánh hay đã chạy Windows. Nên bổ sung số nhánh thật/tiêm/không đo vào báo cáo để tránh người đọc bỏ mất giới hạn; đây không phải finding độc lập về một hành vi sai đã đo.

**Giới hạn nghiệm thu**

- A1 trên Windows thật: **KHÔNG ĐO ĐƯỢC**. Không có kết quả Windows trên exact head trong bằng chứng đã đo. Những phép ép nhánh ở đây chỉ kiểm logic thay thế.
- Việc Windows trả ENOENT cho tên dài và không chạy script git không đuôi: **KHÔNG ĐO ĐƯỢC trực tiếp**; không suy từ kết quả Linux. Đã đo phản ứng khi hai khả năng ấy không dùng được.
- A4, check run CI PR xanh trên exact head: **KHÔNG ĐO ĐƯỢC**; chưa có phép đọc check-run độc lập trong review này. Run lỗi được nêu trong packet không thay thế bằng chứng CI của head ứng viên.
- Không dùng hai giới hạn trên làm finding lỗi mã. Quyết định `request_changes` dựa trên finding P2 có phản chứng chạy được ở trên.
