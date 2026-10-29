Verdict: approve
Reviewed commit: 8036ddb47a2e769703cc897798b3ba2182389c49
Spec sha256: e1e709be14e2e7c2a81de39c3acf2666c746e7146116dee669cadee4dad8ed19

Không có finding P0/P1/P2/P3 còn mở trong phạm vi đã đo. P2 lượt trước đã vá thật: cả hai đột biến từng SỐNG nay CHẾT trên toàn suite, đúng chốt c97. Head đạt `94/94`, base đạt `93/93`; cả hai đạt `137/137` đột biến thường và `2/2` ca tự kiểm. Bảng dưới ghi cả các đột biến bổ sung còn SỐNG và giới hạn của chúng. Windows thật và CI PR trên exact head: **KHÔNG ĐO ĐƯỢC** độc lập. Verdict này không cấp quyền merge/land.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn: [VERDICT-LUOT1.md](VERDICT-LUOT1.md), commit `b2e2410a4b9215480aee6771c1ba8a15a6e14160`.

| Lớp finding cũ | Kết quả trên head | Phép kiểm đóng |
|---|---|---|
| P2 `nhanh-tiem-thieu-chot-tu-kiem`, hai biểu hiện vá nhầm module và không gỡ lstat | **ĐÃ VÁ THẬT** | Chạy lại từng đột biến trên toàn suite; c97 bắt đúng đối chứng vô hại và identity; kiểm riêng ba nhánh và hoàn nguyên khi lỗi. |

| Lệnh từ sandbox | Chốt thực sự làm đỏ | Tổng cuối / bằng chứng |
|---|---|---|
| `python3 review_probe.py wrong_module_native --full` | c97: `nhánh tiêm canh-bao trên bản sao vo-hai: đòi QUA, được ĐỎ`; CLI trả rc1, thiếu cảnh báo tiêm, thay vì rc2 | rc1; `93/94 · 137/137 · 2/2`; `TỔNG: ĐỎ`, `FULL_RC 1`. [Log](evidence/wrong_module_native-full.log), [diff](evidence/wrong_module_native.diff). |
| `python3 review_probe.py lstat_no_restore --full` | c97: `nhánh tiêm lstat (vo-hai) KHÔNG gỡ Path.lstat` | rc1; `93/94 · 137/137 · 2/2`; `TỔNG: ĐỎ`, `FULL_RC 1`. [Log](evidence/lstat_no_restore-full.log), [diff](evidence/lstat_no_restore.diff). |

Đột biến thứ nhất thay đúng dòng chọn module trong `_tiem_git` thành `mod = _BNV2_THAT`; đột biến thứ hai chỉ bỏ `Path.lstat = that` trong `finally` của `_tiem_lstat`. Mỗi lượt chỉ có **c97** đỏ; không lấy việc ca khác chết làm bằng chứng. Cờ `Path.lstat=false` cuối lượt đột biến thứ hai là hậu quả cố ý của mutant trong tiến trình riêng; c97 khôi phục trạng thái tại lúc vào, vốn đã bị mutant c91 làm bẩn trước đó. Head nguyên có tất cả cờ hoàn nguyên `true` ở phép đo riêng bên dưới.

## Bảng finding

Không có finding mở để liệt kê theo mẫu `[P0..P3]`. Một lớp / hai biểu hiện của lượt trước đã đóng bằng các phép đo trên. Các trường hợp SỐNG dưới đây được ghi như giới hạn độ phủ, không được che bằng tổng suite xanh.

## Cách tái lập và phạm vi

Các lệnh Python/Git đo fixture dùng:

```sh
export PYTHONDONTWRITEBYTECODE=1
export GIT_CONFIG_GLOBAL=/dev/null
export GIT_CONFIG_SYSTEM=/dev/null
git -C cay-kho config core.abbrev 7
```

Đã dựng `probe-tree/` và `base/` bằng `cp -a cay-kho probe-tree` và `cp -a cay-kho base`, rồi `git -C base checkout --detach e9967f07b95c6458afc63dabf4a5c0494e90eca7`. Cả hai giữ đầy đủ cây, `.claude/dev/launcher.py` và thư mục `.git` độc lập; status khi dựng xong rỗng. [review_probe.py](review_probe.py) thay nguồn test **trong bộ nhớ**, giữ `__file__` trỏ vào bản sao đủ cây; diff của từng biến thể nằm trong `evidence/`. Các phép đột biến không sửa `cay-kho/`.

Với `review_probe.py --full`, mã thoát tiến trình chính là `FULL_RC`. Với các probe nhắm ca, rc0 chỉ nói harness chạy xong; kết quả thực nằm ở `RESULT`, `FAULT`, `FSYNC_C91` hoặc tuple đạt/không đạt. Không gộp hai loại mã này.

| Phép đo / lệnh | Output, mã thoát và bằng chứng |
|---|---|
| `git -C cay-kho rev-parse HEAD HEAD^{tree}`; đối chiếu hash đặc tả và hai diff | HEAD khớp dòng 2; tree `f74b668ad845680d10cb8bad17e2df10c71b6064`; spec khớp dòng 3; `DIFF.patch_matches=true`, `DIFF-LUOT2.patch_matches=true`; clone không nông. [Identity](evidence/identity.json). |
| `(cd cay-kho && python3 ops/bien_nhan_v2_test.py)` | rc0; `94/94 ca đạt · 137/137 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 119/137 đột biến thường khai đối chứng`; `TỔNG: ĐẠT`. [Log](evidence/head-suite.log). |
| `(cd base && python3 ops/bien_nhan_v2_test.py)` | rc0; `93/93 · 137/137 · 2/2 · 119/137`; `TỔNG: ĐẠT`. [Log](evidence/base-suite.log). |
| `git -C cay-kho diff --check e9967f07b95c6458afc63dabf4a5c0494e90eca7 HEAD` | rc0, không output. Lặp trong [scope_check.py](scope_check.py), [log](evidence/scope-check.log). |
| `ruff --version`; `ruff check --no-cache --select F --output-format json .` trên head/base; `python3 scope_check.py` | Ruff `0.16.9`; mỗi lint rc1 với **9160 lỗi nền**, riêng tệp đổi cùng 1 lỗi. So multiset `(path, code, message)`: `new=[]`, `removed=[]`, delta0; script so rc0. [Delta](evidence/ruff-delta.json). Đây là bare lint, không phải kiểm pin Ruff của CI. |
| `(cd cay-kho && python3 .claude/dev/packet_loop.py doctrine-scan --root .)` | rc0; `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`. [Log](evidence/doctrine.log). |
| `(cd cay-kho && python3 ops/bien_nhan_v2.py --root .)` | rc0; `244 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 297`; `TỔNG: ĐẠT`. [Log](evidence/product.log). |
| `python3 scope_check.py` | rc0; diff chỉ `ops/bien_nhan_v2_test.py`; HEAD/tree/spec không đổi; tracked/index/untracked/ignored đều không có delta. SHA256 sản phẩm trên head/base cùng `82a667496adc4ebbe9516f484fc4d9da4e79570ac20006b122a7400d0be539f6`. [Snapshot cuối](evidence/final-scope.json). |

Snapshot sạch chỉ chứng minh không có delta quan sát được ở các mốc đo. `core.abbrev=7` được đặt theo chỉ thị. Công cụ đo: Python `3.13.17`, Git `2.43.0` (`python3 --version`, `git --version`). Số ca tăng đúng một là c97; ba cặp vô hại/đột biến trong c97 không được cộng vào mẫu số 137 hoặc 2 của hai nhóm cũ.

## Nhánh tiêm, lỗi rig và hoàn nguyên

`python3 -u review_probe.py native` ⇒ rc0, c97 `qua`; log ghi sáu lần thay sang module khác. [Trace](evidence/c97-trace.log):

| Nhánh | Bản sao vô hại | Bản sao đột biến |
|---|---|---|
| lstat | rc2; stderr nêu `tiem-lstat`; đạt | m116: rc0, stderr rỗng; không đạt |
| cảnh báo git | rc2; stderr nêu `tiem-canh-bao-1017`; đạt | m114: rc1, L-ANCESTRY thay vì cảnh báo; không đạt |
| git rc3 | rc2; stderr nêu `merge-base` và `rc=3`; đạt | m125: rc1, L-ANCESTRY thay vì trạng thái không đo được; không đạt |

`RESTORE` cho `bnv2`, `CONG`, `Path.lstat`, `_chay_git`, danh sách tạm rỗng và mọi thư mục tạo ra đã xóa đều `true`. c18/c91/c96 chạy tiếp trong cùng tiến trình đều `qua`.

`python3 rig_probe.py` ⇒ rc0 ([log](evidence/rig.log)):

- Lỗi `LoiDungCa` sau dựng bản sao ⇒ `gian_giao`; RuntimeError cùng vị trí ⇒ `tin_dung_gia`.
- Cho rig trả kết quả sai trên đối chứng vô hại ⇒ c97 đỏ ở **đối chứng**, sau đúng một lần thay module. Cho CLI ném RuntimeError ⇒ c97 đỏ ở chốt CLI; không chạy tới chốt nhận kết quả âm của mutant.
- Cả năm tình huống thử (kể cả head nguyên) trả lại module/CONG/lstat/git, xóa thư mục và làm rỗng danh sách tạm; c18 nghiêm sau từng lượt là `(True, '')`.
- Tạo context git trước khi thay module, rồi mới vào context: `old_unchanged=True`, `new_patched=True`, lệnh trúng mẫu rc3. Thân ném lỗi vẫn cho `LATE_BIND_RESTORE True True`.

Vì vậy c97 **có thể đỏ do rig**, nhưng các tình huống đã đo không biến lỗi rig thành một lượt c97 xanh hoặc tín dụng giết m116/m114/m125. Nhãn `giet_that` ở đối chứng/CLI là chốt làm **ca c97 thất bại**, không phải xác nhận mutant sản phẩm có răng.

## Đột biến mới và trường hợp SỐNG

Các lệnh dưới chạy từ sandbox. Bốn lượt `--full` SỐNG đều kết thúc rc0, `94/94 · 137/137 · 2/2`, `TỔNG: ĐẠT`, `FULL_RC 0`.

| Lệnh / thay đổi | Kết quả | Diễn giải / log |
|---|---|---|
| `python3 review_probe.py c97_no_control --full` — bỏ cặp vô hại của c97 | **SỐNG** | Xóa chính đối chứng không làm sản phẩm sạch hỏng; suite không tự khóa việc xóa đối chứng của nó. [Log](evidence/c97_no_control-full.log). |
| `python3 review_probe.py fsync_always_warns --full` — bỏ probe cảnh báo | **SỐNG** | Git tại chỗ thực sự phát cảnh báo, nên nhánh bị bỏ tương đương trong lượt này. Với git im lặng mô phỏng, mutant đỏ đúng `cau_hinh_canh_bao/khong-no`, trong khi head qua và ghi chú. [Full](evidence/fsync_always_warns-full.log), [đối chứng](evidence/fallback.log). |
| `python3 review_probe.py wrong_second_marker --full` — thành phần `<` dùng dấu `a*40` | **SỐNG** | POSIX chọn thành phần dài trước, chưa tới thành phần thứ hai. Khi mô phỏng chọn thành phần `<`, head có marker `b*40` và đạt; mutant rc2 nhưng sai marker, kết quả `False`. [Full](evidence/wrong_second_marker-full.log), [đối chứng](evidence/fallback.log). |
| `python3 review_probe.py no_mkdir --full` — bỏ tạo `ops/reviews` | **SỐNG** | Probe thật dừng ENOENT ở thư mục cha; c91 ghi chú rồi vẫn qua bằng nguồn tiêm. Đây là khả năng mất phủ nguồn thật mà tổng suite không bắt. Head nguyên tạo cha và đo tên dài thật thành công. [Full](evidence/no_mkdir-full.log), [đối chứng](evidence/fallback.log). |
| `python3 review_probe.py c97_wrong_comparison` — đảo `dat == mong_dat` | **CHẾT ở c97** | `lstat`/`vo-hai`: “đòi QUA, được QUA” nhưng phép so bị đảo. [Log](evidence/c97_wrong_comparison-targeted.log). |
| `python3 review_probe.py git_no_restore` — bỏ hoàn nguyên git | **CHẾT ở c97** | `canh-bao (vo-hai) KHÔNG gỡ _chay_git`. [Log](evidence/git_no_restore-targeted.log). |
| `python3 review_probe.py git_no_hit` — không tiêm lệnh nào | **CHẾT ở c97** | Đối chứng `canh-bao` trả rc1 thay vì rc2. [Log](evidence/git_no_hit-targeted.log). |
| `python3 review_probe.py git_all_commands` — tiêm rc3 mọi lệnh | **CHẾT ở c97** | Đối chứng `rc3` nhận lỗi `rev-parse --is-shallow-repository`, thiếu đúng `merge-base`. [Log](evidence/git_all_commands-targeted.log). |

Đo thêm `python3 review_probe.py no_control_wrong_module`: c97 `qua` khi đồng thời xóa đối chứng và vá nhầm module ([log](evidence/no-control-compound.log)). Điều này chứng minh đối chứng mới có vai trò thực tế; head có đối chứng ấy đã bắt lỗi trong lượt full ở trên. Không suy từ các phép đo rằng suite chống được mọi đột biến của chính mã kiểm. Những mutant SỐNG là giới hạn được công khai; chưa có lỗi hành vi tương ứng trên **head nguyên** trong các đối chứng đã chạy, nên không gán thêm finding hiện hành chỉ vì đã xóa một phép kiểm hoặc chưa đi vào nhánh theo nền.

`python3 fallback_probe.py` ⇒ rc0 ([log](evidence/fallback.log)): với head, hai lần lstat độc lập lần lượt thấy tên dài ENOENT và thành phần `<` EINVAL mô phỏng, thư mục cha tồn tại ở cả hai lần, CLI đạt với marker `b*40`. Khi cả hai ENOENT, nguồn thật trả `NOT_CONSTRUCTIBLE`. Git im lặng mô phỏng làm c91 in hai dòng `GHI CHÚ` rồi `qua` bằng nguồn tiêm. `python3 c96_fallback_probe.py` ⇒ rc0, hai ghi chú không bọc được PATH, `RESULT ('qua', None)`, `PROBES 2` ([log](evidence/c96-fallback.log)). Các mô phỏng này không phải phép chạy Windows.

## Byte LF và giới hạn nghiệm thu

`python3 lf_probe.py` ⇒ rc0 ([log](evidence/lf.log)):

| Biến thể | Commit / blob | Kết quả c93 |
|---|---|---|
| LF | `e4a3f5d511d31dfb809024edcde68c4602cd02f1` / `e4a3f5daa164ce057bf3ad4a93b1431146ec5a30` | `qua` |
| Ghi CRLF tường minh | `5cfd3f5e87ecd0877a62d75e22c3cf005d842524` / `70363d663b5f549bdc70e2b0ce3838c2ad43ffd7` | `gian_giao: fixture: commit/blob không chung tiền tố`, khớp cặp trong spec |
| LF + m120 | Cặp LF trên | `giet_that`: rc2, `OID e4a3f5d mơ hồ — 2 commit chung tiền tố` |

- **A1 trên Windows thật: KHÔNG ĐO ĐƯỢC.** Packet cung cấp lời khai run `40853717478`, job `gate-ops (windows-latest)`, bước selftest `94/94 · 137/137 · 2/2`, `TỔNG: ĐẠT` trên `8036ddb`; đây là dữ liệu đầu vào, không phải phép đo độc lập của review này.
- WinError 123/EINVAL với `<`, ENOENT với tên dài, hành vi PATH của Windows và cảnh báo Git for Windows 2.55: **KHÔNG ĐO ĐƯỢC** trực tiếp. Probe mô phỏng chỉ kiểm logic lựa chọn/tiêm.
- **A4 — CI PR xanh trên exact head: KHÔNG ĐO ĐƯỢC** độc lập. Theo dữ liệu packet, bước sau đỏ ở t27 của #1006; không biến lời khai đó thành kết quả toàn job xanh và không sửa phạm vi khác.
- Tổng `94/94` đếm hàm ca, không chứng minh mọi nhánh thật đều chạy: các log mutant/fallback có ghi chú mà tổng vẫn bằng nhau. Approval nội dung ở đây không thay thế nghiệm thu Windows, CI hay quyền merge/land.
