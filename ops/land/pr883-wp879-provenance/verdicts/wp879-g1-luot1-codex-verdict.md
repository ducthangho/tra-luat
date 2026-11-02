verdict: changes_requested
reviewed_sha: be00ef723eca3fae90932e476d683f233588f2b3
reviewed_tree: 764ed835e3b556d4f8354161918ca151da643be4
base_sha: 747f983ccbcaf29a8e5228d09fd05b5a5ab6e479

Review độc lập, lớp `sensitive`, ngưỡng không P0/P1/P2 mở. **Một P1: các hợp đồng workflow trong `ci_duong_nhanh_test.py` chưa cập nhật, làm CI Linux đỏ.** N5 GitHub thật tách khỏi verdict mã và **KHÔNG ĐO ĐƯỢC** offline.

Mọi thay đổi thử nghiệm nằm trong archive tạm (`mktemp`/`tempfile.mkdtemp` + `git -C cay-kho archive <OID>`); không sửa checkout được review, không đăng GitHub. Bản nền/head có Git metadata riêng và `core.abbrev=7`. Python 3.13, Linux. Bản sao và lệnh đo lưu ở [review_evidence](review_evidence/). Không suy model/receipt được phục vụ từ nhãn reviewer; xác nhận identity/assurance của launcher nằm ngoài phép đo mã này.

## BẢNG ĐO

Các script `review_evidence/*.py` chạy từ gốc sandbox; lệnh nội bộ `python3 ops/...`, actionlint và ruff chạy với cwd là archive trong `paths.json`. `setup.py` dựng cả hai archive trong một lời gọi; mỗi phép A/B chạy **cả hai vế trong một lời gọi**, `PYTHONDONTWRITEBYTECODE=1`. Log đầy đủ giữ nguyên.

| Mục | Lệnh / evidence | Output thật | Kết luận |
|---|---|---|---|
| Preflight | `git -C cay-kho rev-parse HEAD HEAD^{tree}`; `sha256sum SPEC.md`; `git -C cay-kho status --short` | SHA/tree như đầu báo cáo; spec `41c7329bc9c7c944cb081052230d269016e930a584b3b95ca3a6751e615ac81e`; status rỗng | Khớp snapshot/lease |
| Integrity cuối lượt | `python3 review_evidence/final_integrity.py` | **rc=0**, errors=[]; HEAD/tree/spec vẫn đúng; worktree cay-kho sạch; base là tổ tiên head; cả hai archive không đổi tracked file, core.abbrev=7 | Giữ nguyên checkout được review |
| Phạm vi | `PYTHONDONTWRITEBYTECODE=1 python3 -W ignore review_evidence/metadata.py` → `scope.json` | 3 tệp đổi, đều thuộc write set; 9 job, chỉ `gate-cong-cu`, `gate-cong-cu-gop` đổi; **7 job khác bằng nhau**; khóa workflow `on/name/concurrency` bằng nhau | Đúng phạm vi; `ops/ci_duong_nhanh_test.py` được phép cập nhật nhưng bị bỏ sót |
| CA / mutation / anchors N3(a) | Cùng lệnh metadata → `metadata_summary.json`, `metadata.json` | **61→61 CA**, **470→470 mutant**; danh sách, thứ tự, định nghĩa bằng nhau; **470/470 count neo không đổi** (467 count=1, 2 count=2, 1 count=3) | Không bớt ca hoặc mutant; 3 neo không duy nhất đã có từ nền |
| CA nền chưa đột biến | `python3 review_evidence/baseline_cas.py`, gọi thật toàn CA qua `_chay_1_ca` ở cả hai vế trong một lệnh | **61/61 qua, rc=0/0**, không bỏ ca | Positive control: không cấp kill cho ca đỏ sẵn |
| Registration | `python3 review_evidence/paired_checks.py` (retry registration) | Base **1056/1056**, head **1064/1064**, `rc=0/0`; đăng ký **24/24** | Đạt; 8 wp879-* đều ĐỎ đúng |
| Lease t16 | Cùng script A/B ban đầu: `python3 ops/lease_publish_test.py --chi-ca=t16` | **9/9, đã chạy=9, bỏ qua=0**, `rc=0/0`, gồm t161 khóa nguồn os | Đạt |
| Actionlint | Cùng script A/B: `actionlint` (toàn workflow) | `rc=0/0`, stdout rỗng | Không thêm finding; chỉ xác minh parser, không coi là runner |
| Ruff | `ruff check --select F .claude/dev/ci_dang_ky_test.py ops/cong_cu_test.py`, hai vế | Cùng **1 F841** biến `ci` không dùng trong `ops/cong_cu_test.py`, line 2735, `rc=1/1` | **Delta 0** |
| Doctrine | `python3 .claude/dev/packet_loop.py doctrine-scan --root .`, hai vế | `rc=0/0`; sạch, 10 tệp, 0 chỗ chép doctrine | Đạt |
| Diff whitespace | `git -C cay-kho diff --check <base> <head>` | `rc=0`, stdout rỗng | Đạt |
| Hợp đồng workflow độc lập | `python3 review_evidence/stale_contracts.py` | Base y11/y12/y13 **rc=0/0/0**; head **rc=3/3/3**, `DO:<đúng tên ca>` | **LỖI P1**, không phải lỗi sandbox |
| Bán kính N3(b) | `python3 review_evidence/radius_retry.py` (cache các cặp đã đo xong trước đó) cùng cơ chế `_do_ban_kinh` → `radii/*.json` | **101/101 cặp** xong; **0** cặp đổi status/phán quyết | Đã so tất cả mutant đích t54 |
| Bộ đường nhanh đầy đủ | `python3 review_evidence/long_checks.py` → `{base,head}-ci_duong_nhanh.log` | base: rc=1, 1372.23s, CA 103/104, mutant 378/383 ; head: rc=1, 1370.24s, CA 100/104, mutant 347/383 | Lỗi socket chung t20zo tách riêng; 3 ca đỏ chỉ head là regression |

Lần registration đầu gặp `commit.gpgsign=true` kế thừa từ môi trường; fixture `git commit` gọi code-sign rồi thất bại vì dịch vụ ký bị sandbox chặn. Đã giữ raw log và thử lại bằng **override môi trường chỉ cho lệnh test** `GIT_CONFIG_COUNT=2`, key 0 `core.abbrev=7`, key 1 `commit.gpgsign=false`; không sửa global Git hay cây review. Kết quả lease/actionlint/ruff/doctrine nằm trong `paired_checks.raw.json`, registration retry trong `paired_checks.json`.

### Main thật trên Linux ép nhánh Windows (N1/N2)

`real_main_probe.py` gọi **main thật, đủ CA thật**, chỉ quan sát bằng audit/profile hooks. `real_main_pair.py` chạy Windows/posix; sau khi phát hiện signing ảnh hưởng fixture, đã chạy lại nhánh Windows với signing tắt (`real-nt-clean.*`). Lệnh cốt lõi:

```python
g = runpy.run_path("ops/cong_cu_test.py", run_name="x")
g["main"].__globals__["_TEN_NEN"] = "nt"
sys.exit(g["main"]())
```

Env: `CONG_CU_TEST_MANH=0/8 CONG_CU_TEST_MANH_RA=<tệp chưa tồn tại> PYTHONDONTWRITEBYTECODE=1`. Đã đo biểu thức `g is g["main"].__globals__` trả `False`; gán `g["_TEN_NEN"]` **không** đổi globals của main. Không dùng lỗi gán dict để tự tạo phép đo Windows giả.

| Nền ép | rc / ca / dòng kết | Tệp / child từ main |
|---|---|---|
| nt | **rc=0**, `cong_cu_test: 61/61 đạt; tổng=61, bỏ qua=0, tiền kiểm bỏ qua=0`; ``TỔNG: CA 61/61 đạt · ĐỘT BIẾN 470 mục KHÔNG ĐO TRÊN WINDOWS — đo trên ubuntu-latest (`gate-cong-cu` 8 mảnh + `gate-cong-cu-gop`)`` | Tệp tồn tại: **False**; 61 case slots; **0** call vào phóng radius/ghi shard; 474 Popen đều ở tiền kiểm/CA, line {8879: 3, 8880: 1, 8887: 470} |
| posix | **rc=0**; `cong_cu_test: 61/61 đạt; tổng=61, bỏ qua=0, tiền kiểm bỏ qua=0`; `BÁN KÍNH ĐỘT BIẾN — MẢNH 0/8 (59/470 đột biến; 4 tiến trình):`; `MẢNH 0/8: 59/59 đột biến bán kính 1 · ghi /tmp/claude-0/-home-user-tra-luat/d9c6c3bb-1347-5927-91fd-7aefba3ba0a1/scratchpad/rv879.P3pPdl/review_evidence/real-posix.shard` | Tệp tồn tại: **True**; **4 worker radius** tại line 8922, `_phong_con` và `_ket_thuc_manh` mỗi hàm được main gọi 1 lần |

Đối chứng posix sạch: **rc=0, 61/61 CA, 59/59 mutant radius 1/61**, tệp **678783 bytes**, thời gian Linux có contention **1722.71s**; nt sạch **89.8s**, không suy ra phút Windows thật từ các số Linux này. Không có dòng TỔNG ở đường POSIX mảnh cũ; dòng kết hợp đồng là `MẢNH 0/8: 59/59 ...`. 59 phép đo head-only này không được cộng vào coverage A/B N3. Lần nt đầu vẫn `rc=0`, **60/60** (tổng 61, 1 bỏ qua t47 do fixture Git không tạo được INDEX xung đột); không tệp, không radius. Lần sạch **61/61** xác nhận ca bỏ qua đó do signing môi trường. Không gọi tất cả subprocess của CA là radius của main: CA tự kiểm có con riêng.

Đối chiếu tiền lệ #456 (`.claude/hooks/pretooluse_guard_test.py:785`): cùng `so_ca > 0 and do == 0 and so_dot_bien > 0`. Ca bỏ qua rời mẫu số; ca đỏ và tiền kiểm bỏ qua đều tính lỗi; zero-ca và bảng mutant rỗng không đạt. Dòng Windows nói rõ nơi đo Linux, không có `bi giet`. Nhánh nằm riêng trong `che_do == "manh"`; 518 khóa giàn giáo chung giữ nguyên, `du_nt==du`, `gate_nt==gate`.

### Ngữ nghĩa Actions và giới hạn offline

| Giả định | Phép đo / evidence | Kết luận và hệ quả nếu sai |
|---|---|---|
| (a) exclude không khớp ở lượt chỉ Ubuntu vô hại | `metadata.py` mô hình tích Descartes trên YAML đã parse: Ubuntu **8 mảnh+1 gom**, Windows **1+0**, hai nền **9+1**. Không tìm được snapshot tài liệu máy chủ/runner có thể chạy offline | **KHÔNG ĐO ĐƯỢC trên Actions**. Mô hình cho đúng tổ hợp; nếu server coi exclude không khớp là lỗi, lượt chỉ Ubuntu sẽ fail mở matrix. N5 windows-only không chứng minh vế này: cần nhìn thêm lượt Ubuntu-only, 8 check mảnh và gom đều được tạo, không có Windows |
| (b) job-if trước mở matrix Windows-only rỗng | Mô hình thấy matrix gom **0 tổ hợp**, điều kiện contains Ubuntu **False**; actionlint rc=0 nhưng không thực thi scheduler | **KHÔNG ĐO ĐƯỢC** thứ tự server offline. Nếu matrix được mở trước if, workflow sẽ fail “matrix rỗng”. N5 phải thấy gom `skipped` (không lỗi strategy/validation, không runner/artifact Windows), Windows shard 0 vẫn chạy |
| (c) runner.os trong step-if | `actions_history.json`: readback jobs run **39313480770**, head **3818bd4a9685e1782afdd7e8a593482f74b663ff**; Git show workflow tại đúng SHA: bước ci-phamvi có đúng `runner.os != 'Windows'`; API lưu **skipped Windows / success Ubuntu**. Parser cũng chấp nhận expression mới | **ĐÃ ĐO lịch sử offline**, hỗ trợ ngữ nghĩa step-if; upload mới trên head **KHÔNG ĐO ĐƯỢC**. Nếu sai, upload Windows tìm shard không có rồi đỏ. N5 nhìn upload `skipped`; Ubuntu upload vẫn chạy |
| (d) tên check và required checks | Cùng jobs snapshot có tên thật **`gate-cong-cu (windows-latest, 0)`**. `ruleset_history.json`: ruleset 20856202 cập nhật **30-09-2026** chỉ có các context Ubuntu: gate, gate-ops, gate-packet-loop, gate-cong-cu-gop (gom bị lặp trong snapshot) | Đã đọc evidence lịch sử, **KHÔNG ĐO ĐƯỢC ruleset hiện tại/tên check head**. Nếu ruleset nay đòi Windows 1..7/gom, PR sẽ mắc required check vắng: phải dừng và hỏi chủ kho theo N2. N5 xem tên Windows còn lại; readback ruleset hiện tại trước land |

## BẢNG ĐỘT BIẾN

`python3 review_evidence/t54_mutations.py`: một archive riêng khỏi cây review, phục hồi nguồn trước mỗi mutation và chạy Python mới từng lượt; gọi `runpy.run_path(...)["_chay_1_ca"](t54)`. `giet_that` chỉ được cấp khi **TinHieuChotCa mang đúng ca_nguon t54**, không phải parse error, KeyError hay `LoiDungCa`. Control `qua`.

| Mutant (mỗi lượt riêng) | Loại thật | Chốt / ý nghĩa |
|---|---|---|
| Đảo vị từ nền (`invert-predicate`) | **giet_that** | vị từ nền: chỉ 'nt' mới bỏ vòng đột biến |
| Bỏ `so_dot_bien > 0` (`remove-positive-mutant-table`) | **giet_that** | dat_windows phải đòi SỐ DƯƠNG hai vế (ca > 0, đỏ = 0, bảng đột biến khác RỖNG #319) |
| Thêm `bi giet` vào dòng Windows (`add-bi-giet`) | **giet_that** | dòng Windows phải khai đột biến đo Ở ĐÂU và KHÔNG mang chữ giết: 'TỔNG: CA 60/61 đạt · ĐỘT BIẾN 470 mục bi giet KHÔNG ĐO TRÊN WINDOWS — đo trên u |
| Bỏ nhánh nt trong main (`remove-nt-main`) | **giet_that** | `main` nối SAI (kịch bản: thấy [rc, nhật ký, stdout]): {'manh_nt': "[0, ['tk:batch_behavior_test', 'tk:python_alias_behavior_test', 'ca:t1_thieu_ |
| Bỏ tiền kiểm khỏi đối số do (`omit-preflight-error`) | **giet_that** | `main` nối SAI (kịch bản: thấy [rc, nhật ký, stdout]): {'manh_nt_tk': "[0, ['tk:batch_behavior_test', 'tk:python_alias_behavior_test', 'ca:t1_thi |
| Giàn giáo đọc os.name (`harness-host-os`) | **giet_that** | `main` nối SAI (kịch bản: thấy [rc, nhật ký, stdout]): {'manh_nt': "[0, ['tk:batch_behavior_test', 'tk:python_alias_behavior_test', 'ca:t1_thieu_ |
| Cho nhánh nt lan du/gate (`leak-nt-to-du-gate`) | **giet_that** | `main` nối SAI (kịch bản: thấy [rc, nhật ký, stdout]): {'du_nt': "[0, ['tk:batch_behavior_test', 'tk:python_alias_behavior_test', 'ca:t1_thieu_ba |
| Đặt nt sau ghi tệp (`late-nt-after-writer`) | **giet_that** | `main` nối SAI (kịch bản: thấy [rc, nhật ký, stdout]): {'manh_nt': "[0, ['tk:batch_behavior_test', 'tk:python_alias_behavior_test', 'ca:t1_thieu_ |
| Mẫu số giữ ca bỏ qua (`denominator-includes-skipped`) | **giet_that** | `main` nối SAI (kịch bản: thấy [rc, nhật ký, stdout]): {'manh_nt_ca_bq': "[0, ['tk:batch_behavior_test', 'tk:python_alias_behavior_test', 'ca:t1_ |
| Tử số dùng len(CA) (`numerator-total-instead-passed`) | **giet_that** | `main` nối SAI (kịch bản: thấy [rc, nhật ký, stdout]): {'manh_nt_ca_do': "[1, ['tk:batch_behavior_test', 'tk:python_alias_behavior_test', 'ca:t1_ |
| Bỏ so_ca > 0 (`remove-positive-case-count`) | **giet_that** | dat_windows phải đòi SỐ DƯƠNG hai vế (ca > 0, đỏ = 0, bảng đột biến khác RỖNG #319) |
| `main-case-count-total` (săn thêm) | **qua** | SỐNG: chưa có tình huống tất cả ca Windows bỏ qua |
| `main-mutant-count-constant` (săn thêm) | **qua** | SỐNG: chưa làm rỗng bảng DOT_BIEN tại main |
| `default-platform-always-nt` (săn thêm) | **giet_that** | Default luôn nt làm các kịch bản posix sai |

11 mutant đầu (7 bắt buộc + 4 tự nghĩ) **11/11 giết thật**; thử thêm 3 mutant khác: 1 giết thật, **2 sống**. Hai survivor là **lỗ coverage dây nối zero-case/zero-table**, không phải lỗi code hiện tại: head đang truyền đúng `so_ca`, `len(DOT_BIEN)`. Phép đo tổng hợp `survivor_boundaries.py` chứng minh mức hại: toàn ca bỏ qua **control rc=1 / mutant rc=0**; bảng rỗng **control rc=1 / mutant rc=0**. Cần thêm kịch bản zero tại main nếu muốn khóa hai lỗi này; các fixture tổng hợp này tách khỏi phép đo main thật ở trên.

`python3 review_evidence/workflow_mutations.py`: sửa **tệp YAML thật** trên archive, chạy nguyên `ci_dang_ky_test.py` từng lượt. Control rc=0; cả 5 mutant **rc=1**, đúng chốt G5:

| Mutation workflow | Output chốt thực |
|---|---|
| Windows về 8 mảnh | `gate-cong-cu: matrix phải đúng ... + exclude ...` |
| Linux về 1 mảnh | Cùng chốt matrix, thấy exclude Ubuntu 1..7 sai |
| Bỏ if upload | `gate-cong-cu: sau bước G5 phải đúng MỘT bước tải lên ...` |
| Bỏ exclude gom | `gate-cong-cu-gop: matrix phải đúng os + exclude ...` |
| If gom về !cancelled() | `gate-cong-cu-gop: needs/if phải đúng ...` |

### N3(b): phân hạng và bán kính từng mutant đích t54

Control chưa mutate `baseline_cas.py` đã cho **61/61 qua ở cả hai vế**, rc=0/0. Các tên đích được lấy từ **DOT_BIEN nền**, không suy từ tên mutant: **101/470**. `radius_worker.py` gọi **_do_ban_kinh(name)** thật (toàn CA, không bo_qua_ca), rồi `_ket_luan_ban_kinh`. Mỗi process có module riêng và tắt bytecode; tất cả dùng đúng cơ chế dựng cây mutate của bộ. Các lượt chạy quá nhiều worker đã được hủy (`rc=130`) trước khi đủ kết quả và tiếp tục bằng `python3 review_evidence/radius_retry.py` với 4 worker, tái dùng chỉ kết quả JSON hoàn chỉnh. Không tính lượt hủy là pass/kill. Đối chứng posix ban đầu bị dừng để dựng lại với signing tắt như phép đo nt sạch. Batch chỉ chia công việc, không giả kết quả. Raw JSON giữ **status từng CA**, lỗi và toàn bộ dòng kết luận, không chỉ status đích.

Đã hoàn tất **101/101 cặp**; **0** cặp khác toàn vector status/phán quyết. Không suy rộng ra phần chưa đo trong 470. `python3 review_evidence/validate_radii.py` **rc=0**: đủ **202/202** bản ghi, mỗi bản có **61/61** tên ca; đúng đích `giet_that`, **60 ca khác đều qua**, không skip/tín dụng giả/collateral; verdict lỗi=0. So toàn vector giữa hai vế: **101/101 bằng nhau**, radius **1/61** từng mutant. Coverage A/B là **101/470**, không suy thành toàn 470. Ký hiệu G = `giet_that`, Q = `qua`, TDG = `tin_dung_gia`, BQ = `bo_qua`.

| Mutant | Nền: đích / radius / lỗi | Head: đích / radius / lỗi | So vector mọi CA |
|---|---|---|---|
| `f6_main_mat_gia_tri` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f6_main_mat_van_tay` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f6_main_bo_tien_kiem` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f6_main_manh_mot_tien_trinh` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f5_main_bo_nhan` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f5_main_bo_ghi` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f5_main_bo_truyen_loi` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f5_main_bo_loi_con` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f5_main_nen_do_van_do` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f2_main_du_bo_ban_kinh` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f2_main_gate_van_do` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f2_main_manh_do_ca_bang` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f7_cau_hinh_nuot` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f7_tk_chi_batch` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f7_tk_chi_alias` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f7_ca_do_nuot` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f7_ca_loi_khac_nuot` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f7_bo_qua_thanh_hong` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f7_con_rc_bo` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f7_ghi_ket_du_loi` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f7_bo_cong` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f7_cong_goc_sai` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f7_bo_phan_hang` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f7_bo_gian_giao` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f7_nen_rong` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f7_bo_song_song` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f7_song_song_nen_rong` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f7_du_nen_rong` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f7_du_nuot_loi` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f7_du_mot_tien_trinh` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f7_ket_bo_tien_kiem` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f7_ket_bo_cong` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f7_ket_bo_loi_db` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f12_ca_lap` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f12_bk_gan_de` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f12_bk_chi_dau` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f12_dem_qua` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f12_dem_bo_qua` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f12_bo_in_bk` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f12_bo_in_ghi` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f15_ghi_bang_mot` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f15_ket_db_bang_mot` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f15_nen_chi_dau` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f15_tk_chi_dau` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f15_ly_cuoi` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f15_so_lieu_loi_0` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f15_so_lieu_cong_dat` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f15_bo_in_do` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f15_bo_in_tk` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f15_bo_in_bq` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f15_bo_thong_bao_giao` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f18_ghi_lon_hon_mot` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f18_ket_db_lon_hon_mot` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f18_manh_n_co_dinh` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f18_bk_dong_dau` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f18_ghi_dong_dau` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f18_bo_in_cong` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f18_bo_in_nen` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f23_bq_chi_in_dau` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f23_bq_dem_bool` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f23_ly_bo_duoi` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f26_bq_ly_ca_dau` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f26_do_ly_ca_dau` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f26_tk_ly_dau` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f26_con_sau_rc0` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f27_entry_drop` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f27_entry_rc` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f27_shard_zero` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f27_fixed_path` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f27_fixed_workers_manh` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f27_fixed_workers_du` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f28_can_cau_hinh` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f28_gate_di_tat` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f28_du_nuot_ma` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f28_nen_ma` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f42_k_mod_8` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f42_n_luy_thua_2` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f42_ra_strip` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f42_ra_lower` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f42_worker_manh_tran_3` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f42_worker_du_tran_3` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f44_nen_k_mod_8` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f44_nen_n_luy_thua_2` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f44_nen_ra_strip` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f44_nen_ra_lower` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f44_nen_ten_n8` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f44_nen_in_k_mod_8` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f44_nen_chi_tien_kiem` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `f27_full_seed` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `w698_e50_bang_2` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `w698_e50_tu_2` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `w698_x50_bang_n_tru_1` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `w698_x47_hong_bang_1` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `w698_x47_tk_bang_1` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `w698_s2_hong_va_khong_bq` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `w698_s2_hong_gt_bq` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `w698_s2_tk_va_khong_bq` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `w698_s3_xor` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `w698_x_main_ra_normpath` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `w698_x3_m3a_ra_nfkc` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |
| `w698_x3_m3b_ra_cf` | giet_that / 1/61 / 0 | giet_that / 1/61 / 0 | BẰNG |

## BẢNG SĂN

| Hướng độc lập / giả thuyết | Lệnh | Output thật | Kết luận |
|---|---|---|---|
| Sentinel ban đầu Windows làm các kịch bản cũ đi nhánh nt | `python3 review_evidence/hunts.py`: archive đổi riêng `_TEN_NEN = "nt"`, gọi t54; so output helper base/head | `INIT nt`, `RESULT ["qua", null]`; **518 khóa chung BẰNG**, chỉ 6 kịch bản nt + bảng windows thêm | **KHÔNG PHẢI LỖI** ở phần chọn nền. Windows OS thật vẫn **KHÔNG ĐO ĐƯỢC**; N5 cần t54 xanh trong đủ CA |
| Job gate/du bị nhánh mới làm bỏ radius/selfchecks | Cùng `hunts.py`, so nguyên rc/log/stdout của helper main | `gate_nt_equals_gate=True`, `du_nt_equals_du=True`; gate/du cũ cũng bằng base | **KHÔNG PHẢI LỖI** trong dây nối đã đo; không gọi đây là đo Windows thật |
| Mutant khác vô tình ghi _TEN_NEN | Quét toàn 470 anchor/replacement trong `metadata.json`; count mọi neo base/head | `sentinel_mutation_hits=[]`, **0/470** cặp chứa `_TEN_NEN`; không neo nào đổi count | **KHÔNG PHẢI LỖI** trong phép quét này; full radius 470 chưa đo |
| Ubuntu-only lọt job Windows | `python3 review_evidence/all_jobs_model.py` + `metadata.py`: parse workflow, thay OS input Ubuntu, liệt kê tích/exclude; so mọi job khác | **8 mảnh Ubuntu + 1 gom Ubuntu**; mô hình **tất cả 9 job** (`all_jobs_ubuntu_model.json`) cho **23 job Ubuntu, 0 Windows** ở cả nền/head, toàn danh sách bằng nhau; 7 job khác không đổi | **KHÔNG PHẢI LỖI** mô hình; scheduler thật **KHÔNG ĐO ĐƯỢC** |
| Bộ ghim độc lập vẫn nhớ topology cũ | `stale_contracts.py`, sau khi full suite phát hiện | Base **0/0/0**, head **3/3/3**; chốt named y11/y12/y13 | **LỖI P1**, finding bên dưới |
| Main hiện tại chấp nhận zero-case / zero-table? | `t54_extra_mutations.py`; `survivor_boundaries.py` | Hai mutant `qua`; mỗi biên control **1**, mutant **0** | **KHÔNG PHẢI LỖI runtime hiện tại**: control từ chối cả hai biên; đồng thời phát hiện lỗ coverage của t54 (hai mutant sống) |

### stale-fast-lane-workflow-contracts  [P1]  Hình dạng mới làm gate-ops Linux đỏ vì các bảng ghim độc lập chưa cập nhật

**TỆP/DÒNG:** `.github/workflows/ci.yml:523` (exclude mảnh), `:575` (if upload), `:591` (if gom); các bảng/chốt bị bỏ sót trong `ops/ci_duong_nhanh_test.py:2258`, `:2289`, `:2348`, `:2421`.

**VẤN ĐỀ:** PR cập nhật `ci_dang_ky_test.py` nhưng chưa cập nhật `IF_BUOC_CHUAN`, `KHUNG_JOB`, `KHUNG_BUOC`, `JOB_CO_IF_CHO_PHEP` trong bộ độc lập. `y11` từ chối điều kiện gom mới; `y12` từ chối điều kiện upload; `y13` từ chối strategy rồi sẽ gặp cả snapshot bước. CI gọi nguyên bộ này trực tiếp tại `.github/workflows/ci.yml:698` trong `gate-ops` khi `runner.os == 'Linux'`, đồng thời registry còn đăng ký nó (`.claude/dev/ci_dang_ky_test.py:78`). Vì vậy sửa Windows hợp lý vẫn làm cổng Linux thất bại. Spec write set mục 4 **đã cho phép** sửa đúng các bảng này khi đỏ do hình dạng G5.

**ĐÃ THỬ NGHIỆM:** `python3 review_evidence/stale_contracts.py` chạy hai vế trong một lệnh, bytecode tắt, core.abbrev=7, signing tắt riêng cho fixture:

```text
base y11 rc=0; y12 rc=0; y13 rc=0
head y11 rc=3 DO:y11... if cap job lech ... contains(...ubuntu-latest)
head y12 rc=3 DO:y12... actions/upload-artifact@v4 runner.os != Windows
head y13 rc=3 DO:y13... gate-cong-cu ... khac [strategy]
```

Đo toàn lớp (`all_workflow_mutator_anchors.py`): áp thuần **74/74** hàm biến đổi YAML được trên nền, **72/74** trên head; chỉ hai hàm dưới lỗi neo 0. Đây là đo khả năng áp transform, không nhận là đo kill. Đo AST độc lập (`stale_mutation_anchors.json`): cả `yml_gop_if_doi_always` và `yml_gop_bo_if` có **anchor count 1 ở nền → 0 ở head**, nên bộ mutant cũng cần cập nhật neo. Ba dòng DO của y11/y12/y13 ở trên là **TinHieuChotCa** đúng ca (`--mot-ca` trả 3), khác với lỗi hạ tầng neo 0 vừa đo. Full suite cũng tách cùng lỗi socket bị sandbox cấm ở t20zo (có ở cả hai vế, 5 mutant không đo được) khỏi **3 ca DO chỉ head**. Kết quả đầy đủ: nền **103/104 CA, 378/383 mutant**, head **100/104 CA, 347/383 mutant**; thêm **31 mutant** không đo được trên head vì y11/y12/y13 đã đỏ ở nền của chính lượt mutation. Evidence: `stale_contracts.json`, `stale_contracts.out`, `{base,head}-ci_duong_nhanh.log`.

**ĐỘ TIN:** cao. **Hướng vá:** trong `ops/ci_duong_nhanh_test.py`, cập nhật bằng đúng 2 topology mới, if gom, if upload và snapshot bước artifact; sửa 2 neo mutant `yml_gop_if_doi_always`/`yml_gop_bo_if` ở dòng 3259–3260 còn ghim if cũ (nếu không, bộ mutation sẽ lỗi neo). Giữ nguyên contract của 7 job khác. **Ca khóa:** y11/y12/y13 phải xanh; các mutation Windows 8 mảnh/Linux 1 mảnh/bỏ if/bỏ exclude phải tiếp tục đỏ đúng; chạy lại toàn `ci_duong_nhanh_test.py`. **Rủi ro khi vá:** mở rộng allowlist hoặc bỏ so snapshot sẽ làm lọt lỗi routing/skip; cập nhật exact shape thay vì nới assertion.

### N5 và việc cần nhìn ở dispatch thật — KHÔNG ĐO ĐƯỢC

N5 **chưa chạy và không thể chạy offline**; không ước lượng phút, không coi parser/mock là GitHub. Sau khi sửa P1, dispatch `ci.yml` **đúng head cuối** với `runner_set=windows-only`, rồi đọc jobs/check-runs API:

1. Chỉ **một** `gate-cong-cu (windows-latest, 0)` có runner, conclusion **success**; không có mảnh Windows 1..7.
2. Đủ CA thật, gồm t54, dòng Windows khai “KHÔNG ĐO” và Linux; không phóng radius, upload **skipped**, không artifact shard Windows.
3. `gate-cong-cu-gop` **skipped trước khi mở matrix rỗng**, không lỗi strategy, không runner/gom Windows đòi 0..7.
4. Lấy `started_at/completed_at` của **mọi job gate-cong-cu*** có runner Windows, tính tổng phút thật, đối chiếu mốc 570–650; không lấy timeout hay ước lượng làm số đo.
5. Readback ruleset hiện hành để xác minh required check chỉ có các tên Ubuntu; nếu tên Windows bị bỏ vẫn required thì dừng hỏi chủ kho theo N2. Tách lượt Ubuntu-only để xác nhận exclude không khớp vô hại và **8 mảnh + gom** đều xanh.

Approval mã đang bị chặn bởi P1 đã đo, độc lập với N5. Không coi verdict này là quyền merge/land/deploy.
