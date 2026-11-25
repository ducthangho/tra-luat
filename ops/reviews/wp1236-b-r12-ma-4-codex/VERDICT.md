# Review mã wp1236 đợt B — lượt 4

**Verdict: changes_requested.** Không còn P0/P1/P2. Còn **B02 — P3 `ngoai_bang_dong`**, cùng lớp `nghiem-thu-khong-co-lap-chot-dich`; chưa có miễn chủ kho neo SHA này. B01 đã được vá trên HEAD nguyên vẹn. Đây là review offline, không phải quyền push/merge/land.

- `reviewed_sha`: `bca55c1cd09c57180d60b05d5ca1813828ae1d10`
- Tree: `14f1571aada834fc22ea32c29076df8834c05bd6`
- Base: `f602325574c62184caf16309631f5f680ca5cee2`
- Spec r12/generation 1: SHA-256 `4589daf1fd666b03a68b7d7dcd5c60903c10e946963fd324c9ee6185ed8e2dc7` đã kiểm.
- Reviewer: `openai_codex / codex_cli / machine/local`, run `48945bd40ef04b6ea739e7a0144645fe`, độc lập Executor Claude. Model/effort phục vụ: `KHONG_DO_DUOC`; assignment yêu cầu high. Không suy identity từ actor GitHub.
- Linux, Python 3.13.18, Ruff 0.15.15. Sandbox thực tế `workspace-write`; reviewer giữ checkout chỉ đọc, mọi ghi/đột biến dưới `work/`. Không gọi mạng.

## Đối chiếu lượt trước và bảng lớp

| Lớp | Biểu hiện và kết quả trên HEAD | Mức mở cao nhất | Cách vá chung / phép đóng |
|---|---|---|---|
| `nghiem-thu-khong-co-lap-chot-dich` | B01: đủ 9 miền, đóng phần free text; B02 cũ: đủ 24 phản chứng inventory; B02 còn: mất phần tử/category vẫn xanh | P3 | Kiểm tập miền nghĩa độc lập; mất category/ô cấu trúc phải đỏ đúng chốt, baseline vẫn xanh; hoặc miễn P3 đúng SHA |

**Nhãn lớp: `VA_MOT_PHAN`.** Xử lý từng finding cũ:

- **B01: `DA_VA_THAT` trong phạm vi finding.** Tái chạy `probe_missing.py` **12/12**, `probe_scope.py` **23/23**. Ledger đo lại khớp từng phần tử: **810 ô B + 8.396 phần tử c36**. Chín miền cũ đều đã có đối chứng qua `main`/L8; xem [bảng miền](scope-domain-review.json). Phần byte không UTF-8 vẫn có trong c35 và probe độc lập.
- **B02: `VA_MOT_PHAN`.** `chon_ca_a` đã chặn mất cả ca: đổi tên/bỏ/nhân đôi lần lượt tám ca trên bản sao, **24/24** cho `rc=3`, đúng dấu `DO:c36:…mỗi ca bắt buộc…`; baseline và c38 nguyên vẹn xanh. Tuy nhiên còn biểu hiện mất phần tử bên trong ca, trình bày dưới.

Tỷ lệ lớp lượt 3→4: **0/1** (`U={slug trên}`, `F=∅`); không lấy việc đóng B01 làm đóng cả lớp. Không có lớp mới. Lớp đã xuất hiện ở các lượt 1–4. Theo checkpoint/handoff được cấp cho lượt này, executor **dừng vá tự động, trả điều phối**, không tự mở lượt 5 hoặc tự mở rộng quyền.

## B01 — kiểm độc lập c37 và oracle

| Vị trí | Ô thực chạy | Đúng ngữ pháp → `bo_sinh_la` | Âm |
|---|---:|---:|---:|
| Vùng tự do header | 160 | 158 | 2 |
| Nhãn job | 162 | 158 | 4 |
| Tên skipped cũ | 163 | 160 | 3 |
| Tên skipped v3 | 163 | 160 | 3 |
| Tổng | **648** | **636** | **12** |

Mỗi vị trí có đủ **128 ASCII + một đại diện từng 29 general category trừ Cs + ngoài BMP**; cộng 16 ô cấu trúc. Reviewer dùng oracle cấu trúc riêng theo literal, luật CR/LF và tìm delimiter theo thứ tự từ đặc tả, không đọc regex sản phẩm để sinh expected. Cả 648 expected khớp và thực chạy qua `main`/L8.

Ô `a] [b` là dương đúng: delimiter sau `ten` không cho phần đuôi khớp trọn, nên tên lazy lùi đến `ten [a]`, nhãn là `b`. Không được đọc câu “nhãn không chứa `]`” như cấm `]` trong toàn vùng đầu vào trước khi regex phân nhóm. Đã đo thêm trên fixture có **bộ sinh và provenance hợp lệ**: tên/nhãn khớp → rc0; giữ tên cũ sai → rc1 với `job_lech`; hai hậu tố đầy đủ lấy điểm khớp sớm nhất; delimiter sớm không khớp thì backtrack. **4/4** đối chứng này đạt.

`bo_sinh_la` thật sự phân biệt parse thành công với parse lỗi: K1 trả lỗi parser trước, chỉ kiểm băm bộ sinh khi có tài liệu đã parse. Không dùng tổng trạng thái `not_measured` làm oracle. “Dương 0/648” trong bảng tổng hợp của executor là **không có dòng L8**, còn c37 cố ý luôn có L8; bảng riêng 636/12 là đúng nghĩa ngữ pháp. Xem [audit c37](c37-audit.json), [ledger từng ô](ledger-o.json), [ledger c36](ledger-c36.jsonl).

## B02 — P3: sàn đếm còn cho phép rơi miền phần tử

**Vị trí:** `ops/land_evidence_nguon_test.py:792,831,842–857`; nguồn helper nhập tại `ops/gate_output_doi_chieu_test.py:1126`. Không đề nghị sửa A ngoài write set.

Trên **bản sao**, đổi điều kiện helper để không xuất đại diện category `Mn` (U+0300). Kết quả:

| Ca A qua c36 | Baseline | Bỏ Mn | Sàn |
|---|---:|---:|---:|
| a124 | 1733 | 1723 | 1700 |
| a125 | 3840 | 3816 | 3800 |
| a126 | 52 | 51 | 50 |
| a129 | 36 | 35 | 30 |
| a131 | 1 | 1 | 1 |
| a132 | 1280 | 1272 | 1250 |
| a133 | 1136 | 1129 | 1100 |
| a134 | 318 | 316 | 300 |
| Tổng | **8396** | **8343** | — |

c36 vẫn **rc0**. c37 còn **644 ô**, mất Mn ở cả bốn vị trí, nhưng vẫn **rc0**: `len(vu_tru)>=150` đạt và biểu thức `4*len(vu_tru)+16` tự co theo cùng bộ sinh. c38 cũng **rc0**, vì tám tên ca vẫn đủ. Đây là mất các phần tử thuộc miền bắt buộc, không chỉ biến động tổng số vô hại.

**Xác nhận toàn suite:** bản sao bỏ Mn vẫn **rc0, CA38/38 · DOT BIEN145/145 · TU KIEM2 · TONG DAT** (292,70s); [log](full-mutant-Mn.log), [receipt](full-mutant-Mn-result.json). Hai tệp B và module A trong phép đo bằng byte HEAD; chỉ helper của test A mang đột biến.

Phản chứng thứ hai: bỏ riêng lời gọi a129 kiểm delimiter sớm không khớp. a129 còn 35≥30, tổng c36=8395; c36/c38 vẫn rc0. Điều này đo giới hạn chốt sàn, **không khẳng định mọi đối chứng backtracking khác đã mất**. Handoff mô tả sàn “~97–98%” quá hẹp: a129 cho phép mất 6/36=16,7%; a134 18/318=5,66%; a126 2/52=3,85%.

Head nguyên vẹn hiện có đủ các ô đã nêu; finding là độ nhạy hồi quy của cơ chế reuse. Hai đột biến sửa test A, không nằm trong manifest module B/kho B rỗng, nên giữ **P3 `ngoai_bang_dong`**, không nâng P2 vì giá trị bị mất thuộc luật 8. [Cặp canonical `ast.unparse`](outside-mutants.json) đã kiểm áp đúng một lần; [số đo bản sao](adapter-audit.json), [log](adapter-audit.log), [644 ô c37 thực đo](mutant-Mn-c37-measured.json).

**Gợi ý đóng:** trong test B, kiểm tập ASCII/category/non-BMP độc lập với helper nhập, cùng các ID/mệnh đề cấu trúc cần bảo toàn qua consumer; thêm phản chứng bỏ một category và một ô cấu trúc. Không chỉ tăng sàn hoặc ghim băm toàn test A: Unicode/định dạng đổi có thể gây đỏ vô can. Giữ 24 đối chứng inventory đã tốt, trần 560 và đúng write set. Nếu không vá, trạng thái là **chờ miễn chủ kho** cho B02/slug trên, neo exact SHA ứng viên; agent không tự ghi nợ hoặc miễn.

## Phép đo và luật 9

| Phép đo reviewer | rc / bằng chứng |
|---|---|
| `python3 -B ops/land_evidence_nguon_test.py` | **0**, CA 38/38; DOT BIEN 145/145; tự kiểm 2; TONG DAT. 493,71s trong lúc có phép đo khác chạy song song |
| `python3 -B ops/land_evidence_nguon.py --root .` | **0**, 149 ĐẠT + 25/28 miễn cutover, 0 vi phạm, 0 không đo được, tổng 174 |
| Ruff F hai tệp, `--no-cache`, head và base | **0 / 0**, delta 0; pin/probe contract riêng **rc0**, 3 mục, không lỗi |
| `python3 -B .claude/dev/ci_dang_ky_test.py` | **0**, 1226/1226 phản chứng đỏ đúng, TỔNG ĐẠT |
| `git diff --numstat f602325 HEAD` | **0**, 2 tệp, +506/−11, đúng write set, dưới 560 |
| `git diff --check f602325 HEAD` | **0**, không lỗi |
| Module so lượt 1 | Cùng blob `1e42090fa05f4dfc84f20d48b840fce5cfaa48ca`; không thay mã L8 |

c24 trong suite đã đo lại `MIEN_TRU_L8`: đúng **56 tên/băm và 93 vi phạm** trên base, không gồm mục L5 có băm khớp; c28 khóa vân tay, c29 khóa tên+byte đã nạp và mất miễn, c31 khóa thứ tự cutover. Không lấy danh sách executor thay việc chạy các ca này.

Luật 9 áp **DELTA + không hồi quy** theo E3 đã cấp:

- Tái sinh manifest **624 head / 550 base**, so byte với hiện vật; kiểm băm công cụ ghim, Python, test, module, inventory, `HOAN_TAT`. Tái sinh `hoi-quy` khớp từng ID/src/SHA. Phân hoạch **76 delta + 548 kế thừa**.
- Reviewer tái chạy **toàn bộ 76 delta: 76 GIET**, baseline 38/38, rc0. Lệnh `chay` in `TAP_CON` vì không chạy toàn manifest; không khai thành `HOAN_TAT` của `do`.
- Bảng so từng ID kế thừa trong hiện vật: **0** GIET-base→không-GIET-head. Tái chạy **6 cặp**: 5 GIET/GIET, 1 SONG/SONG, 0 hồi quy mẫu. **542 cặp còn lại chưa tái chạy.** Không suy toàn miền từ mẫu.
- Hai ID base không áp được là return của `kiem_ho_so`; hai đột biến thay thế dòng408 nằm trong delta, đã GIET bằng c14. Không có delta `TUONG_DUONG` cần chứng minh. 173 SONG + 13 VO_CAN head thuộc mã kế thừa L1–L7, không thành finding đợt B.
- **Full `do` chưa chạy lại**; sử dụng nhánh hiện vật + tái chạy được assignment cho phép. Xem [audit hiện vật](law9/artifact-audit.json), [kết quả delta](law9/delta-kq.jsonl), [548 cặp](law9/inherited-ledger.json), [mẫu base–head](law9/paired-sample.json).

Lần setup mẫu base đầu dùng bản sao thiếu tệp nguồn nên c11 thất bại (`LOI_CHAY`, wrapper rc1); đã giữ [log lỗi setup](law9/paired-sample.log), dựng lại toàn cây bằng `git archive` base, chạy lại baseline **23/23** và sáu cặp. Không coi lỗi setup là lỗi sản phẩm, không tính lượt lỗi là pass.

Lệnh tái lập các audit (chạy từ `repo`, đặt `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR="$PWD/../work/tmp"`): `python3 -B ../work/audit_c37.py`, `python3 -B ../work/adapter_audit.py`, `python3 -B ../work/law9_audit.py`, `python3 -B ../work/path_audit.py`. Các script chỉ ghi dưới `work/`; lệnh và rc chi tiết ở [VERDICT.json](VERDICT.json).

## M3 Windows và giới hạn

**M3: required; Windows local: not_run.** Diff có `subprocess`/`encoding=`/`pathlib`. Miễn Windows CI theo assignment không miễn local. Không dùng kết quả Linux để tuyên bố Windows xanh.

[Đo đường dẫn Linux](path-audit.json): hậu tố dưới TMPDIR dài nhất c36 **77**, c37 **80** ký tự; TEMP dài khoảng 180 ký tự có thể chạm MAX_PATH truyền thống. c36 tạo 8.396 gốc tạm/lượt, c37 thêm 648. c38 từ chối inventory trước vòng dữ liệu nên không nhân thành 24×8.396 cây tạm. Đo Linux cùng tải: c36 **44,47s**, c37 **7,89s**, c38 **0,136s**; Windows cần đo thời gian thật, path Unicode/longpaths và timeout 300s của tiến trình con.

Chưa chạy trong review: Windows local exact base/head; GitHub CI/connector/full_mutant_audit M9; toàn `do`; `scripts/tl.py --selftest` chỉ có evidence executor. Không có test reviewer khai `skipped` thành pass. **CHƯA ĐỦ ĐIỀU KIỆN MERGE:** P3 B02 chưa đóng/miễn, Windows local và các gate hậu push/audit chưa được review này chứng nhận.

HEAD/tree cuối khớp đầu; diff tracked/index, untracked và danh sách tệp ignored đều rỗng; chỉ có thư mục `.codex/` rỗng đã tồn tại từ đầu. Snapshot hai mốc không chứng minh mọi sự kiện trung gian. Schema verdict đã kiểm bằng `kiem_verdict_lop.py --vong 4`; kết quả ở [kiem_verdict.txt](kiem_verdict.txt).

KET_LUAN: changes_requested
