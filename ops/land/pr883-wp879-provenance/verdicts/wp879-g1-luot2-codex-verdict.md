verdict: approve
reviewed_sha: ab2510624e82834159a6ad898185cb2b1d987206
reviewed_tree: 52788390083f5ad889eb63cd28ccd500d06a52e2
base_sha: 747f983ccbcaf29a8e5228d09fd05b5a5ab6e479
post_merge_sha: e63961f27b53e66db8e6600009f97d5706743063

Review độc lập lượt 2, lớp `sensitive`, ngưỡng **không P0/P1/P2 mở**. Không phát hiện P0/P1/P2 mới; P1 lượt 1 và hai lỗ coverage đã đóng bằng phép đo dưới đây. Approval này là verdict mã. **N5 Windows thật: KHÔNG ĐO ĐƯỢC offline**, tách khỏi verdict mã. Không gọi mạng, không đăng GitHub, không sửa `cay-kho/`.

Reviewer là Codex/OpenAI trong sandbox Linux, Python 3.13.16; không suy model/session identity hay assurance receipt từ tài khoản đăng hoặc nhãn của launcher. Đo mã này không xác thực độc lập receipt của launcher và không tạo quyền merge/land/deploy.

Mọi thử nghiệm dùng archive riêng tạo từ `git -C cay-kho archive <OID>` vào thư mục `mktemp`/`tempfile.mkdtemp`, có Git metadata riêng, `core.abbrev=7`, signing commit/tag tắt. `review_evidence/setup.py` dựng hai vế trong một lệnh; từng phép A/B cũng chạy hai vế trong một lệnh, `PYTHONDONTWRITEBYTECODE=1`. Cây và lệnh cụ thể: [paths.json](review_evidence/paths.json), [common.py](review_evidence/common.py). Không áp lại patch vào checkout review.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn: [VERDICT-luot1.md](VERDICT-luot1.md), reviewed SHA `be00ef723eca3fae90932e476d683f233588f2b3`. Cả ba commit sửa được kiểm trên exact head hiện tại; không dùng evidence sandbox lượt 1 làm kết quả lượt này.

| Lớp / biểu hiện lượt 1 | Đo lại trên head | Kết luận |
|---|---|---|
| `stale-fast-lane-workflow-contracts` [P1]: y11/y12/y13 đỏ và hai neo if gom mất | Y11/Y12/Y13 **rc=0/0/0** ở cả nền và head. Hai neo `yml_gop_if_doi_always`, `yml_gop_bo_if` **1→1**; neo mới `yml_gop_if_bo_ubuntu` **1**. Mutate topology/if làm đúng chốt đỏ; full suite không còn ba ca DO riêng head | **ĐÃ VÁ THẬT — ĐÃ ĐÓNG** toàn biểu hiện mã đã nêu |
| `main-case-count-total`: survivor khi truyền `len(CA)` thay `so_ca` vào `dat_windows` | `_chay_1_ca(t54)` → **giet_that**, `TinHieuChotCa.ca_nguon` đúng t54; chỉ `manh_nt_tat_ca_bq` sai, control rc=1 / mutant rc=0 | **ĐÃ VÁ THẬT — ĐÃ ĐÓNG** lỗ coverage |
| `main-mutant-count-constant`: survivor khi truyền `470` thay `len(DOT_BIEN)` vào `dat_windows` | Cùng cơ chế → **giet_that**, tín hiệu đúng t54; chỉ `manh_nt_bang_rong` sai, control rc=1 / mutant rc=0 | **ĐÃ VÁ THẬT — ĐÃ ĐÓNG** lỗ coverage |

Hai survivor lượt 1 được ghi là lỗ coverage, không phải lỗi runtime hiện tại. Lượt này thay **riêng đối số trong return của main**, không sửa `dat_windows`, dòng in hoặc kỳ vọng để tạo kill. Neo/thay nguyên văn, output và ca nguồn lưu trong [t54_mutations.json](review_evidence/t54_mutations.json). Không có finding nào bị đổi slug hay chuyển baseline để xóa lịch sử.

## BẢNG ĐO

Lệnh `python3 review_evidence/<script>.py` chạy từ gốc sandbox; lệnh nội bộ chạy trong archive theo `paths.json`. Raw stdout/stderr giữ trong `.log`, mã thoát/thời gian trong JSON.

| Phép đo | Lệnh / evidence | Output thật | Kết luận |
|---|---|---|---|
| Preflight | `git -C cay-kho rev-parse HEAD HEAD^{tree}`; `sha256sum SPEC.md`; `metadata.py` | SHA/tree như đầu; spec **41c7329bc9c7c944cb081052230d269016e930a584b3b95ca3a6751e615ac81e**, khớp lease; status sạch | Khớp snapshot |
| Hậu merge | `git --git-dir kho.git diff ab25106 e63961f -- <4 tệp write set>` | **rỗng** | Mã đang review bằng mã đã merge trên 4 tệp |
| Phạm vi | `metadata.py` → [metadata_summary.json](review_evidence/metadata_summary.json) | Đúng 4 tệp trong lease; chỉ 2 job G5 đổi; **7 job khác bằng nhau**, khóa workflow ngoài jobs bằng nhau; `diff --check` rc=0 | Không mở phạm vi |
| CA / DOT_BIEN / neo | Cùng script → [metadata.json](review_evidence/metadata.json) | **61→61 CA**, **470→470 mutant**; tên/thứ tự/định nghĩa bằng nhau; **470/470 count neo bằng nhau**: 467 neo ×1, 2 neo ×2, 1 neo ×3 | N3(a) đạt; ba neo đa lần đã có ở nền |
| Không nới ca khác / cơ chế đo | `ast_scope.py` → [ast_scope.json](review_evidence/ast_scope.json) | Chỉ **t54** đổi AST trong 61 CA; **9/9** hàm đo/phân hạng/phân mảnh/phóng/nhận/cấu hình giữ nguyên AST | Không thay cơ chế Linux để lấy parity; t54 được thử mutation riêng |
| Control toàn CA | `radius_pair.py`, worker `BASELINE` gọi `_chay_1_ca` từng CA | Cả hai **61/61 qua**, 0 bỏ qua/kill giả | Không cấp kill từ ca đỏ sẵn |
| Fast-lane đầy đủ | `long_checks.py` → [long_checks.json](review_evidence/long_checks.json) | Base **rc=1, 103/104 CA, 378/383 mutant, 364.46s**; head **rc=1, 103/104, 379/384, 363.96s** | Cùng một lỗi môi trường socket; phân tích bên dưới |
| Ghim workflow | `workflow_mutations.py` → [workflow_mutations.json](review_evidence/workflow_mutations.json) | Control y11/y12/y13 rc=0/0/0; 5 lỗi bắt buộc đều rc=3 ở đúng chốt; thêm always/bỏ if/job-if lạ/step-if lạ cũng đỏ | P1 đóng; giữ exact shape |
| Registration | `paired_checks.py`: `python3 .claude/dev/ci_dang_ky_test.py` | **1056/1056 → 1064/1064** phản chứng đỏ đúng, `TỔNG: ĐẠT`, rc=0/0; 24/24 đăng ký | Đạt; không khai nền 1064 |
| Lease | Cùng lệnh A/B: `python3 ops/lease_publish_test.py --chi-ca=t16` | **9/9, đã chạy=9, bỏ qua=0**, rc=0/0 | Đạt; gồm t161 |
| Actionlint | Cùng lệnh A/B: `actionlint` toàn workflow, bản 1.7.7 | **rc=0/0**, stdout rỗng | Parser sạch; không nhận là scheduler GitHub |
| Ruff thật | Cùng lệnh A/B: `ruff check --no-cache --force-exclude --extend-exclude ci.yml --select F <4 tệp>`; ruff 0.16.9 | **rc=1/1**, cùng **1 F841** biến `ci` tại `ops/cong_cu_test.py:2735`; output bằng nhau | **Delta 0**. Ruff đo 3 Python; YAML dùng actionlint |
| Doctrine | Cùng lệnh A/B: `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | **rc=0/0**, quét 10 tệp, 0 chỗ chép doctrine | Đạt |
| N3(b) | `radius_pair.py` + các batch bổ sung, cùng `radius_worker.py` → [radius_validation.json](review_evidence/radius_validation.json) | **101/101 cặp** hoàn tất; **0** vector lệch, **0** bản ghi sai tiêu chí | Đã phủ đủ 101/470, đúng toàn bộ đích t54 |
| Main thật ép nt trên Linux | `real_nt.py` → [real-nt.log](review_evidence/real-nt.log) | **rc=0, 61/61 CA**, 0 bỏ qua; đúng 61 case slots; main gọi radius/writer **0/0**; không tệp shard; DOT_BIEN cùng object/keys, 470 mục | Đo dây nối thật trên Linux; chưa phải Windows OS |
| Cách ly suite | `parent_isolation.py` → [parent-isolation.log](review_evidence/parent-isolation.log) | t54→t52→t53→t54: **4/4 qua**; object, 470 keys, 8 phân hoạch giữ nguyên sau từng ca | Helper con không rò bảng rỗng sang ca sau |
| Integrity cuối | `integrity.py final` | rc=0, snapshot đầu/cuối bằng nhau; checkout sạch | Snapshot cả file/hash/mode, .git, tracked/untracked/ignored |

### Full fast-lane: lỗi sandbox tách khỏi lỗi mã

Cả hai vế chạy trọn suite, không skip hoặc mock socket để lấy N/N. Cùng duy nhất:

```text
[HONG] t20zo_la_khong_phai_tep_thuong_do: PermissionError: [Errno 1] Operation not permitted
CA: 103/104 dat · 0 do · 1 hong
# base: DOT BIEN: 378/383 bi giet dung ly do
# head: DOT BIEN: 379/384 bi giet dung ly do
TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that)
TONG: DO
```

Lỗi ở `_tao_socket` → `socket.bind`; cùng **5** mutant đích t20zo không đo được: `symlink_treo_khong_theo_bi_danh`, `la_bo_chot_tep_thuong`, `la_cho_phep_fifo`, `la_cho_phep_socket`, `la_khong_theo_symlink`. Không cấp kill cho 5 mục này. Khác biệt head +1 kill đúng ứng với mục mới, không còn ca workflow DO. **Không tuyên bố đã đo 104/104, 383/383 hoặc 384/384** trong sandbox này. Logs: [base](review_evidence/base-ci_duong_nhanh.log), [head](review_evidence/head-ci_duong_nhanh.log). Đây là giới hạn đã thấy ở lượt 1, không phải regression do commit sửa.

## BẢNG ĐỘT BIẾN

`PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/t54_mutations.py` và lượt ghim lại neo hàm đích. Mỗi mutant trên archive riêng, phục hồi nguồn trong finally, Python mới, gọi thật `_chay_1_ca(t54)`. **giet_that** chỉ khi `TinHieuChotCa.ca_nguon == t54_main_chon_DUNG_vong_ban_kinh_theo_che_do`. Control **qua**. Bộ 11 N1 lượt 1 **11/11 giet_that**, thêm 2 survivor nay bị giết và 1 lỗi vị từ mặc định: **14/14 giet_that**, không crash/parse error/LoiDungCa.

| Mutant | Kết quả | Chốt / kịch bản |
| `invert-predicate` | **giet_that** | vị từ chỉ nt mới bỏ vòng đột biến |
| `remove-positive-mutant-table` | **giet_that** | dat_windows đòi bảng khác rỗng |
| `add-bi-giet` | **giet_that** | chuỗi Windows cấm bi giet |
| `remove-nt-main` | **giet_that** | manh_nt |
| `omit-preflight-error` | **giet_that** | manh_nt_tk |
| `harness-host-os` | **giet_that** | manh_nt, nền theo dữ liệu |
| `leak-nt-to-du-gate` | **giet_that** | du_nt / gate_nt |
| `late-nt-after-writer` | **giet_that** | manh_nt, không phóng/ghi |
| `denominator-includes-skipped` | **giet_that** | manh_nt_ca_bq |
| `numerator-total-instead-passed` | **giet_that** | manh_nt_ca_do |
| `remove-positive-case-count` | **giet_that** | dat_windows đòi so_ca > 0 |
| `main-case-count-total` | **giet_that** | manh_nt_tat_ca_bq (mới) |
| `main-mutant-count-constant` | **giet_that** | manh_nt_bang_rong (mới) |
| `default-platform-always-nt` | **giet_that** | manh POSIX phải còn radius |

Hai phép bổ sung kiểm tra lại chỉ sửa đúng hàm `dong_windows`/`nen_bo_qua_dot_bien`, không sửa chuỗi kỳ vọng trong t54. Log thử ban đầu giữ riêng `t54_mutations.initial.json`; bảng trên dùng kết quả ghim đúng neo trong JSON cuối. Thay riêng sentinel khởi tạo `_TEN_NEN = "nt"` cho **qua**, đúng chủ ý vì giàn giáo đặt nền từng kịch bản; khác với lỗi hàm luôn chọn nt khi thiếu đối số, đã bị giết.

### Mutation workflow trên tệp YAML thật

`workflow_mutations.py`: parse YAML, sửa đúng thuộc tính, chạy CLI `--mot-ca` riêng từng y11/y12/y13 trên archive. Control qua cả ba. Bảng ghi rc theo thứ tự y11/y12/y13; **3 là DO bằng TinHieuChotCa**, 0 là không chốt thuộc tính ấy.

| Mutation | y11 / y12 / y13 | Kết luận |
| `control` | 0 / 0 / 0 | control qua |
| `windows-eight-shards` | 0 / 0 / 3 | bị chốt đúng thuộc tính |
| `linux-one-shard` | 0 / 0 / 3 | bị chốt đúng thuộc tính |
| `remove-upload-if` | 0 / 3 / 3 | bị chốt đúng thuộc tính |
| `remove-gather-exclude` | 0 / 0 / 3 | bị chốt đúng thuộc tính |
| `gather-if-only-cancelled` | 3 / 0 / 3 | bị chốt đúng thuộc tính |
| `gather-if-always` | 3 / 0 / 3 | bị chốt đúng thuộc tính |
| `remove-gather-if` | 3 / 0 / 3 | bị chốt đúng thuộc tính |
| `unrelated-job-if` | 3 / 0 / 3 | bị chốt đúng thuộc tính |
| `unrelated-step-if` | 0 / 3 / 3 | bị chốt đúng thuộc tính |

### N3(b): bán kính và phân hạng trên Linux

Tên đích lấy từ **DOT_BIEN nền**, không lọc theo tên mutant: **101/470** đích t54. Worker gọi **`_do_ban_kinh(name)` thật**, không `bo_qua_ca`; rồi `_ket_luan_ban_kinh`. Mỗi bản ghi đủ **61 CA**; so toàn vector trạng thái với nền, không chỉ ca đích. Mọi cặp hoàn tất phải đúng **đích giet_that, 60 ca khác qua, 0 skip/tin_dung_gia, radius 1/61, lỗi 0**. Chi tiết lý do/raw vector giữ ở `review_evidence/radii/*.json`.

Batch bổ sung chỉ phân công công việc hệ điều hành, không dùng agent phụ hay thay logic bộ đo. Kết quả JSON hoàn chỉnh được tái dùng; claim tránh chạy lặp một cặp. Số `COMPLETE` của coordinator không phải số đo: chỉ JSON đã hoàn tất và validator đủ 61 CA mới tính. Không tính các ca thật ép nt hoặc thử mutation ngoài bảng vào coverage A/B này. **Không suy từ 101/470 thành toàn bộ 470**.

| Mutant | Nền: đích · radius · lỗi | Head: đích · radius · lỗi | Vector 61 CA |
| `f6_main_mat_gia_tri` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f6_main_mat_van_tay` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f6_main_bo_tien_kiem` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f6_main_manh_mot_tien_trinh` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f5_main_bo_nhan` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f5_main_bo_ghi` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f5_main_bo_truyen_loi` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f5_main_bo_loi_con` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f5_main_nen_do_van_do` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f2_main_du_bo_ban_kinh` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f2_main_gate_van_do` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f2_main_manh_do_ca_bang` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f7_cau_hinh_nuot` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f7_tk_chi_batch` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f7_tk_chi_alias` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f7_ca_do_nuot` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f7_ca_loi_khac_nuot` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f7_bo_qua_thanh_hong` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f7_con_rc_bo` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f7_ghi_ket_du_loi` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f7_bo_cong` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f7_cong_goc_sai` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f7_bo_phan_hang` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f7_bo_gian_giao` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f7_nen_rong` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f7_bo_song_song` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f7_song_song_nen_rong` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f7_du_nen_rong` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f7_du_nuot_loi` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f7_du_mot_tien_trinh` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f7_ket_bo_tien_kiem` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f7_ket_bo_cong` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f7_ket_bo_loi_db` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f12_ca_lap` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f12_bk_gan_de` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f12_bk_chi_dau` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f12_dem_qua` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f12_dem_bo_qua` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f12_bo_in_bk` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f12_bo_in_ghi` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f15_ghi_bang_mot` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f15_ket_db_bang_mot` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f15_nen_chi_dau` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f15_tk_chi_dau` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f15_ly_cuoi` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f15_so_lieu_loi_0` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f15_so_lieu_cong_dat` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f15_bo_in_do` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f15_bo_in_tk` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f15_bo_in_bq` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f15_bo_thong_bao_giao` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f18_ghi_lon_hon_mot` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f18_ket_db_lon_hon_mot` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f18_manh_n_co_dinh` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f18_bk_dong_dau` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f18_ghi_dong_dau` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f18_bo_in_cong` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f18_bo_in_nen` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f23_bq_chi_in_dau` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f23_bq_dem_bool` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f23_ly_bo_duoi` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f26_bq_ly_ca_dau` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f26_do_ly_ca_dau` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f26_tk_ly_dau` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f26_con_sau_rc0` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f27_entry_drop` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f27_entry_rc` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f27_shard_zero` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f27_fixed_path` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f27_fixed_workers_manh` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f27_fixed_workers_du` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f28_can_cau_hinh` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f28_gate_di_tat` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f28_du_nuot_ma` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f28_nen_ma` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f42_k_mod_8` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f42_n_luy_thua_2` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f42_ra_strip` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f42_ra_lower` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f42_worker_manh_tran_3` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f42_worker_du_tran_3` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f44_nen_k_mod_8` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f44_nen_n_luy_thua_2` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f44_nen_ra_strip` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f44_nen_ra_lower` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f44_nen_ten_n8` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f44_nen_in_k_mod_8` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f44_nen_chi_tien_kiem` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `f27_full_seed` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `w698_e50_bang_2` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `w698_e50_tu_2` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `w698_x50_bang_n_tru_1` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `w698_x47_hong_bang_1` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `w698_x47_tk_bang_1` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `w698_s2_hong_va_khong_bq` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `w698_s2_hong_gt_bq` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `w698_s2_tk_va_khong_bq` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `w698_s3_xor` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `w698_x_main_ra_normpath` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `w698_x3_m3a_ra_nfkc` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |
| `w698_x3_m3b_ra_cf` | giet_that · 1/61 · 0 | giet_that · 1/61 · 0 | BẰNG |

## BẢNG SĂN

Ít nhất ba hướng độc lập nhắm chính commit sửa: (1) trạng thái giàn giáo, (2) nguồn kỳ vọng động, (3) độ chặt của hợp đồng vừa sửa. Tách giả thuyết và kết quả thay vì dùng tổng suite làm bằng chứng thay thế.

| Hướng / giả thuyết | Lệnh | Output thật | Kết luận |
|---|---|---|---|
| Bảng rỗng rò sang các kịch bản sau khi đổi thứ tự | `harness_hunts.py`: normal / blank-first / reverse; quan sát object tại **mọi** lần main vào | Mỗi lượt **521 kịch bản**, **0 lỗi identity**; blank index **47 / 0 / 473**; sau helper đúng object cũ 470. Ca tiếp theo lần lượt `noi-k0-n2`, `cau_hinh_sai`, `manh_nt_tat_ca_bq` đều đọc bảng thật | **KHÔNG PHẢI LỖI** |
| Ngoại lệ trong main bỏ qua phục hồi DOT_BIEN | Cùng script, gây **RuntimeError / KeyboardInterrupt / SystemExit** từ `dat_windows` khi bảng rỗng, bên trong main thật | Blank rc **NEM:RuntimeError / NEM:KeyboardInterrupt / NEM:SystemExit**, mỗi lượt đủ **521**, 0 lỗi identity, ca kế tiếp 470, cuối đúng object cũ | **KHÔNG PHẢI LỖI** trong ba lớp exception và mọi kịch bản đã đo |
| `mong_du`/`mong_manh` vô tình đọc bảng rỗng hoặc hằng 470 | Cùng script, thay bảng thật bằng **469** mục trước khi chạy helper, rồi cho ca bảng rỗng chạy như thường | `mong_du=469`; tổng phân hoạch mỗi n=2..16 **469**, cuối bảng thật cùng object **469**; ca blank vẫn riêng 0. Control gốc mọi tổng **470** | **KHÔNG PHẢI LỖI**; kỳ vọng đọc bảng thật |
| Mở allowlist để dập P1 làm lọt điều kiện ở job/bước khác | `workflow_mutations.py`: thêm job-if vào `gate-ops`, step-if vào bước khác; đổi gom thành always hoặc bỏ if | Job-if lạ **3/0/3**, step-if lạ **0/3/3**, always/bỏ if **3/0/3**; control **0/0/0** | **KHÔNG PHẢI LỖI**; hợp đồng vẫn exact shape |
| Neo mutant mới làm hỏng các transform cũ hoặc trùng tên/mất target | `yaml_transform_inventory.py`, áp mọi hàm biến đổi YAML thật ở hai vế | Base **74/74**, head **75/75** áp được; 383→384 tên, **0 trùng**, **0 target vắng**, CA 104→104. Đây là applicability, kill do suite và phép riêng đo | **KHÔNG PHẢI LỖI** trong inventory này |
| Helper con giữ DOT_BIEN rỗng ở process suite thật | `parent_isolation.py`, t54→t52→t53→t54 trong cùng parent; thêm `real_nt.py` chạy toàn main thật | **4/4 qua**, object/470 keys/8 phân hoạch bằng nhau sau từng ca; main thật **61/61**, không shard/radius/writer | **KHÔNG PHẢI LỖI** trên Linux ép nền nt |
| N5: job-if trước matrix Windows rỗng, upload skipped, thời gian Windows | Cần jobs/check-runs API trên dispatch master e63961f; cấm mạng trong review này | **Không gọi API / không có số phút mới** | **KHÔNG ĐO ĐƯỢC**, tách khỏi verdict mã |

### stale-fast-lane-workflow-contracts  [P1] — ĐÃ ĐÓNG

Ba bảng khung và allowlist if nay ghim đúng topology mới, if gom có `contains(...ubuntu-latest)`, if upload ngoài Windows; hai neo đột biến if gom có đúng một lần. Đóng bằng y11/y12/y13 xanh cả hai vế, các mutation sai hình dạng đỏ đúng, mọi transform áp được, full suite hết ba ca DO riêng head. Socket t20zo vẫn là giới hạn môi trường chung. Không mở finding mới cùng lớp.

### N5 Windows thật — KHÔNG ĐO ĐƯỢC

Theo snapshot, dispatch `runner_set=windows-only` đang chạy trên master `e63961f27b53e66db8e6600009f97d5706743063`; review offline này không xác minh tiến độ/kết luận. Không suy phút Windows từ Linux, timeout hoặc mô hình YAML. Khi đọc được bằng chứng thật cần xác nhận: đúng một `gate-cong-cu (windows-latest, 0)` xanh, đủ CA, không radius; upload skipped/không shard Windows; gom skipped trước matrix rỗng; tổng phút Windows của mọi `gate-cong-cu*` có runner từ started_at/completed_at; required-check hiện hành không còn đòi tên Windows đã bỏ. Không coi N5 là đã đạt hoặc là lỗi mã đã chứng minh.

### Giới hạn và tính toàn vẹn

Sandbox thực tế cho ghi workspace và `/tmp`; checkout review được giữ read-only theo vai trò bằng cách dùng archive riêng. `integrity.py` chụp **hash/mode/link của 4964 tệp kể cả .git**, HEAD/tree, diff/index, status gồm tracked/untracked/ignored. Mốc hash đầu sau các lệnh đọc/preflight, trước các thử nghiệm còn lại; status sạch được ghi ngay từ lúc bắt đầu. So snapshot chỉ chứng minh không có delta quan sát được giữa hai mốc, không chứng minh mọi thời điểm lịch sử đều chưa từng ghi rồi hoàn nguyên. Các archive có Git commit tổng hợp phục vụ fixture, không nhận chúng là commit reviewed SHA.

Không có P0/P1/P2 mở trong phạm vi đã đo. Giữ riêng hai phần chưa đo: full N/N fast-lane do socket sandbox và N5 GitHub Windows. Không đưa lời khai executor hoặc evidence lượt 1 vào số đo lượt này.
