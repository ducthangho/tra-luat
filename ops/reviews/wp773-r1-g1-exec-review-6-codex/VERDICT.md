Reviewed commit: f9045bff735937e7f00ea009f6811ce8b5494ffc

verdict: changes_requested
P1=0 P2=0 P3=1

Reviewer: Codex (OpenAI), phiên độc lập với executor Claude; chạy shell/tool trực tiếp trong sandbox, KHO read-only. Tree: `e44bfe4bd12de7a904ef9837f29e929c95efbffb`. Không tự chứng nhận launcher, receipt hoặc assurance `human_audited`. Áp ngưỡng lượt 6: cả P1, P2 và P3 phải bằng 0. Trần 700 lấy từ chỉ thị trực tiếp trong prompt.

## Finding

### F07 — P3 — `ops/land_evidence_nguon_test.py:146`: ca mới chỉ khóa provenance trước gốc, chưa khóa vị trí `ops/land/` trong thứ tự Q3

Vá lượt này có răng: đảo toàn bộ `(prov, goc / THU_MUC, goc)` thành `(goc, goc / THU_MUC, prov)` nay bị c05 giết bằng **rc=3 + `DO:c05_l2_luot2_positive_phai_co_nguon_chua_nguyen_van:`**, đúng assertion Q3 vừa thêm. Nhưng quan hệ ba nền chưa được canh đủ. Hai mutation độc lập tại `ops/land_evidence_nguon.py:108` vẫn sống:

1. `(goc / THU_MUC, prov, goc)` — đặt `ops/land/` trước provenance.
2. `(prov, goc, goc / THU_MUC)` — đặt gốc trước `ops/land/`.

**PHÉP ĐO:** `PYTHONDONTWRITEBYTECODE=1 python3.13 -B evidence/measure.py > evidence/measure.log 2>&1` ⇒ script rc=0. Script chép mã sang `/tmp/rv773-r6-{middle-first,root-before-middle}.py`, rồi gọi từng ca thật bằng `LAND_EVIDENCE_NGUON_MA=<bản sao> python3.13 -B /home/user/rv773/ops/land_evidence_nguon_test.py --mot-ca <ca>`. **Cả hai mutation đều qua 14/14 ca, mỗi ca rc=0**; không phải rc=4 hoặc chết vô can. [Lệnh và script](evidence/measure.py), [kết quả](evidence/measure.log).

Đối chứng nội dung, cùng hồ sơ `positive: '1/1'`, `nguon_positive: r.txt`, provenance tồn tại:

| Ca | provenance/r.txt | ops/land/r.txt | gốc/r.txt | Head | Mutation tương ứng |
|---|---|---|---|---|---|
| provenance phải trước ops/land | `2/2` | `1/1` | `1/1` | rc=1, L2 thiếu `1/1` | middle-first: rc=0, ĐẠT sai |
| ops/land phải trước gốc | không có | `2/2` | `1/1` | rc=1, L2 thiếu `1/1` | root-before-middle: rc=0, ĐẠT sai |

Bằng chứng dương của hai bản sao: [middle-first](evidence/middle-first-prov-vs-land.log), [root-before-middle](evidence/root-before-middle-land-vs-root.log). Chạy lại `PYTHONDONTWRITEBYTECODE=1 python3.13 -B evidence/priority-head.py > evidence/priority-head.log` ⇒ script rc=0, hai head đều rc=1 với đúng **một L2 thiếu `1/1`**, không có lỗi khác. [Đối chứng head](evidence/priority-head.log). Head đúng; đây là **một thiếu sót độ phủ hồi quy Q3**, không phải fail-open hiện hữu trên head và không nâng thành P2. F07 lượt 5 đã được sửa cho mutation được nêu đích danh, nhưng chưa đóng đầy đủ quan hệ ưu tiên nguồn mà finding đó bảo vệ.

**HINT patch:** dựng bảng hai cặp ưu tiên liền kề `provenance > ops/land` và `ops/land > gốc`, có tệp trùng tên với số trái nhau; đo ĐỎ khi nền ưu tiên có số sai và ĐẠT khi nền ưu tiên có số đúng. Thêm hai mutation hoán đổi trên, yêu cầu đúng ca rc=3 + `DO:<ca>:`. Có thể gom ca thành bảng và rút gọn mã để giữ trần 700; không cần sửa validator vốn đang phân giải đúng. Owner đề nghị: executor/bảo trì test #773.

## Đã đo

Quy ước: `KHO=/home/user/rv773`; `SP=/tmp/claude-0/-home-user-tra-luat/25822fa2-ac40-52b8-b361-6687f0dd1ccb/scratchpad`. Tất cả Python dùng `-B`/`PYTHONDONTWRITEBYTECODE=1`; bản sao/cây dựng nằm trong `/tmp`. Script evidence ghi chính xác argv, fixture và cách tạo mutation; log giữ stdout/stderr và rc con.

- `sha256sum /home/user/rv773-spec-r1.md` ⇒ rc=0, đúng `063ccaa692372d8f431af07fcb86acccef32435e4b69e7a63e3b0a4ee67e02dd`. Đọc spec trước mã: Q1–Q6, L1–L5, bảng nghiệm thu; đọc hai tệp, diff toàn bộ và vá cuối, AGENTS cùng tài liệu repo liên quan và verdict lượt 5. `git -C KHO rev-parse HEAD HEAD^{tree}` ⇒ rc=0, đúng head/tree ghi trên.
- `git -C KHO diff 1022a33 f9045bf > evidence/diff.patch` và `git -C KHO diff 32b441b f9045bf > evidence/last-patch.diff` ⇒ rc=0. So master chỉ hai tệp mới, 699 dòng; vá cuối chỉ thêm fixture Q3 và mutation. [Diff](evidence/diff.patch), [vá cuối](evidence/last-patch.diff).
- `PYTHONDONTWRITEBYTECODE=1 python3.13 -B KHO/ops/land_evidence_nguon_test.py > evidence/test-3.13.log 2>&1` ⇒ rc=0, **CA 14/14; DOT BIEN 32/32 giết đúng lý do; TU KIEM PHAN HANG DAT (2); TONG DAT**. [Log](evidence/test-3.13.log).
- Với `v=3.11,3.12,3.14`: `PYTHONPATH=$SP/yaml-python$v PYTHONDONTWRITEBYTECODE=1 python$v -B KHO/ops/land_evidence_nguon_test.py > evidence/test-$v.log 2>&1`. **Cả ba rc=0**, cùng **CA 14/14; DOT BIEN 32/32 giết đúng lý do; TU KIEM PHAN HANG DAT (2); TONG DAT**. [3.11](evidence/test-3.11.log), [3.12](evidence/test-3.12.log), [3.14](evidence/test-3.14.log).
- `PYTHONDONTWRITEBYTECODE=1 python3.13 -B evidence/measure.py > evidence/measure.log 2>&1` ⇒ rc=0. Lệnh con `python3.13 -B KHO/ops/land_evidence_nguon.py --root KHO` ⇒ **rc=0: 0 ĐẠT · 28/28 miễn trừ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 28; TỔNG ĐẠT**. [Cây thật](evidence/tree.log).
- Trong script trên, với `c=c6e2401,1a4c417,d60b9e6`: `git -C KHO archive <c> ops/land` ⇒ mỗi lệnh rc=0; giải nén bằng tarfile vào `/tmp/rv773-r6-history/<c>`. `python3.13 -B KHO/ops/land_evidence_nguon.py --root <tmp> --tep ops/land/pr765-wp743-land-evidence.yaml` ⇒ mỗi lệnh **rc=1**. Lần lượt **2 L1**, có `khong_xung_dot`; **1 L1 + 2 L2 + 1 L3**, 02:58:54Z ≥ 02:58:26Z; **1 L1 tại `$.spec.nguon`**. [c6e2401](evidence/history-c6e2401.log), [1a4c417](evidence/history-1a4c417.log), [d60b9e6](evidence/history-d60b9e6.log).
- Import module riêng, đặt `MIEN_TRU_CUTOVER={}` trong bộ nhớ rồi gọi `main` trên cây thật ⇒ **rc=1: 16 ĐẠT, 12 ĐỎ, 82 vi phạm toàn L1, 0 KHÔNG ĐO ĐƯỢC**. Không sửa dictionary trên đĩa. [Log](evidence/no-exemption.log). Script đọc độc lập blob base qua `git ls-tree -r --name-only c73af7b ops/land` và `git show c73af7b:<path>` ⇒ **28 tên**, fingerprint `5311e7557cd75ef2f3b06371c66a4830d4970613c1e98a8fd4af732d7dab2257`, khớp hằng test. Hằng test không tính từ dictionary đang kiểm.
- Cũng trong `measure.py`: mutation đảo thứ tự toàn bộ Q3 bị giết đúng c05 như trên. Mutation đổi tên `plat-x8` thành `plat-x9` ⇒ **rc=3 + `DO:c10_l5_danh_sach_dong_bang:`**. Mutation thêm tên chính thức nằm trong 32/32. c09 đo khớp băm rồi sửa một byte mất miễn trừ; c11 đòi rc=0 và **m=k=28**.
- Probe bổ sung trong `measure.py`: glob tệp thật và thư mục thật ⇒ rc=0; symlink nguồn nội bộ ⇒ rc=0; khóa YAML trùng che lời khai ⇒ **rc=2**, có dòng tổng kết KHÔNG ĐO ĐƯỢC; `nguon_positive` dạng số ⇒ **rc=1 L2**; `positive: 123` cùng nguồn thật ⇒ rc=0 vì không có token số dạng L2; mapping `pre_merge_checks` có mốc ở khóa ⇒ **rc=1 L3**; mốc phân số Z sau merge ⇒ **rc=1 L3**; chuỗi timestamp offset có nháy ⇒ rc=0 (ngoài regex Z đóng băng). Từng log `evidence/probe-*.log` và tổng hợp trong [measure.log](evidence/measure.log).
- `PYTHONDONTWRITEBYTECODE=1 python3.13 -B evidence/extra.py > evidence/extra.log 2>&1` ⇒ script rc=0. Mutation bỏ riêng phép so nội dung số L2 ⇒ **rc=3 + đúng `DO:c05...:`**, chết ở ca readback chỉ metadata. [Script](evidence/extra.py), [log](evidence/extra.log).
- `ruff check --no-cache --select F KHO/ops/land_evidence_nguon.py KHO/ops/land_evidence_nguon_test.py` ⇒ **rc=0**, All checks passed; hai tệp mới nên F delta=0. `git -C KHO diff --check 1022a33 f9045bf` ⇒ **rc=0**. `git -C KHO diff --numstat 1022a33 f9045bf` ⇒ **312 + 387 = 699 dòng thêm / 2 tệp; trần ngoại lệ 700 theo prompt**. Đúng write set g1, không sửa workflow/hồ sơ cũ.

- `git -C KHO status --porcelain --ignored > status-before` và lệnh tương tự vào `status-after`; `cmp status-before status-after` ⇒ **rc=0**, KHO không đổi. Đo lại `git -C KHO rev-parse HEAD` ở cuối vẫn đúng exact head; diff-check cuối rc=0.

## Đối chiếu nghiệm thu và phạm vi (không tính finding)

Các điều kiện nghiệm thu tối thiểu g1 đã đo đều đạt: cây thật m=k, L1 không nguồn, L2 thiếu nguồn/metadata/đúng số/đổi số, L3 trước-bằng-sau merge/chuyển post-merge, YAML hỏng và provenance vắng, lệch băm, thêm/đổi tên danh sách, mutation mỗi L1–L5, thực địa lịch sử, lint và diff-check. F07 là khoảng trống test được đo thêm, không phải tuyên bố sai rằng nghiệm thu tối thiểu yêu cầu đủ mọi hoán vị.

Không phát hiện fail-open hiện hữu trên head trong các ca đã chạy. Bộ phân hạng chỉ đếm rc=3 cùng `DO:<ca>:`; rc=4 không được tính giết. Tự kiểm KeyError vô can và thay đổi vô hại đều đạt. Ca Q3 mới thực sự chạy nhánh L2, không xanh do miễn trừ hoặc một lỗi khác.

Docstring khai giới hạn L1 chỉ kiểm tồn tại và L2 chỉ so token số, không hứa xác minh ngữ nghĩa. So `measured` không phân biệt hoa thường, loại tự trỏ, từ chối merge/alias/kiểu YAML ngoài mô hình đều được khai và được bộ test đo. Chọn readback theo PR trong tên hồ sơ được khai tại hàm và c07 đo việc không dùng PR lân cận; phù hợp cấu trúc hồ sơ thực địa. Offset có nháy nằm ngoài mẫu Z trong spec; phân số Z được hỗ trợ thêm. Đây không phải P3. G2 nối CI còn ngoài phạm vi g1, không dùng làm finding lượt này.

## KHÔNG ĐO ĐƯỢC

- Không xác minh issue/lease/ngoại lệ 700 qua GitHub; dùng authority trực tiếp trong prompt. Không xác nhận g2 land, CI bên ngoài, launcher, receipt hoặc assurance land.
- Không soạn token thoát cây, mã khai thác hoặc symlink thoát gốc mới; chạy c03 có sẵn nguyên trạng. Symlink bổ sung chỉ trỏ tệp trong cùng provenance. Không suy kết quả cho mọi trạng thái filesystem/quyền truy cập; lỗi đọc nguồn được bộ test đo bằng mock.
- Không chạy toàn bộ test repo hay CI, không kiểm ngữ nghĩa nguồn (ngoại phạm vi). Probe riêng và mutation bổ sung chạy trên 3.13; không suy sang mọi OS/parser/recursion limit.
