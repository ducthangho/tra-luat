Reviewed commit: 98d7d2501f0c35f6a150bdd41eaf610bc1bc92ed

verdict: approve
P1=0 P2=0 P3=0

Reviewer: Codex, provider OpenAI, phiên độc lập với executor Claude; execution surface là coding-agent sandbox, transport là shell/tool trực tiếp. Không tự chứng nhận launcher, receipt hay assurance `human_audited`. Tree: `7ff5d359534bb769771b47880ffb491959efd0f4`. KHO read-only; chỉ ghi thư mục ra và cây tạm `/tmp`. Ngưỡng lượt 7 áp dụng cả P3. Trần ngoại lệ 700 lấy từ chỉ thị trực tiếp của chủ kho trong prompt.

## Findings và đóng finding cũ

Không có finding mới được xác nhận bằng phép đo; không còn P1/P2/P3 mở.

**F07 đã đóng** — `ops/land_evidence_nguon_test.py:146–152,305–306`. c05 hiện dựng riêng hai cặp liền kề `provenance > ops/land` và `ops/land > gốc`, nền cao có số sai còn nền thấp có số đúng. Assertion đòi rc=1 cùng thông báo thiếu chính `'195/195'`. Trên head, c05 xanh; hai mutation chính thức đều bị giết trong 33/33. Kiểm độc lập toàn bộ năm hoán vị sai của ba nền: tất cả **rc=3 + `DO:c05_l2_luot2_positive_phai_co_nguon_chua_nguyen_van:`**, chết ở assertion ưu tiên Q3, không phải traceback/rc=4. Vì thế không chỉ đóng hai hoán vị được nêu đích danh mà cả quan hệ thứ tự ba nền. [Script](evidence/measure.py), [tổng hợp](evidence/measure.log), [log từng hoán vị](evidence/perm1.log), [2](evidence/perm2.log), [3](evidence/perm3.log), [4](evidence/perm4.log), [5](evidence/perm5.log).

F01–F06 của các lượt trước vẫn có các ca hồi quy tương ứng: khóa trùng kể cả null/merge, kiểu YAML ngoài mô hình, mốc ở khóa mapping, glob chỉ khớp thư mục, ngày sai và tổ hợp root/tệp tương đối/tuyệt đối. Các ca và mutation đều xanh đúng phân hạng trong lượt này. Không phát hiện vá lượt 7 mở lại chúng.

## Đã đo

Quy ước: `KHO=/home/user/rv773`; `SP=/tmp/claude-0/-home-user-tra-luat/25822fa2-ac40-52b8-b361-6687f0dd1ccb/scratchpad`. Python chạy với `-B` và `PYTHONDONTWRITEBYTECODE=1`. Các lệnh con, argv, rc và stdout/stderr của phép đo bổ sung được lưu trong script/log liên kết; không chỉ dựa lời khai executor.

- `sha256sum /home/user/rv773-spec-r1.md` ⇒ rc=0, đúng `063ccaa692372d8f431af07fcb86acccef32435e4b69e7a63e3b0a4ee67e02dd`. Đọc spec Q1–Q6, L1–L5, nghiệm thu trước diff. `git -C KHO rev-parse HEAD HEAD^{tree}` ⇒ rc=0, đúng head/tree trên. Đọc AGENTS và tài liệu repo liên quan; đối chiếu verdict lượt 1–6.
- `git -C KHO diff 1022a33 HEAD > evidence/full.patch`; `git -C KHO diff f9045bf HEAD > evidence/last.patch` ⇒ rc=0. Chỉ hai tệp mới trong write set; validator không đổi ở vá lượt 7. [Diff đầy đủ](evidence/full.patch), [vá cuối](evidence/last.patch).
- `PYTHONDONTWRITEBYTECODE=1 python3.13 -B KHO/ops/land_evidence_nguon_test.py` (log chuyển hướng vào `evidence/test-3.13.log`; lượt chạy thực tế cũng đặt PYTHONPATH theo mẫu dưới) ⇒ **CA 14/14, DOT BIEN 33/33 giết đúng lý do, TU KIEM PHAN HANG DAT (2), TONG DAT**. Với `v=3.11,3.12,3.14`: `PYTHONPATH=$SP/yaml-python$v PYTHONDONTWRITEBYTECODE=1 python$v -B KHO/ops/land_evidence_nguon_test.py > evidence/test-$v.log 2>&1` ⇒ cùng kết quả. Bốn tiến trình shell hoàn tất rc=0; `TONG DAT` cũng chỉ được in khi hàm test trả 0. [3.11](evidence/test-3.11.log), [3.12](evidence/test-3.12.log), [3.13](evidence/test-3.13.log), [3.14](evidence/test-3.14.log).
- `PYTHONDONTWRITEBYTECODE=1 python3.13 -B evidence/measure.py > evidence/measure.log 2>&1` ⇒ rc=0. Lệnh con `python3.13 -B KHO/ops/land_evidence_nguon.py --root KHO` ⇒ **rc=0; 0 ĐẠT · 28/28 miễn trừ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 28; TỔNG: ĐẠT**. [Cây thật](evidence/tree.log).
- Trong script trên, `git -C KHO archive <c> ops/land` với `c=c6e2401,1a4c417,d60b9e6` ⇒ mỗi archive rc=0; giải nén vào cây tạm. `python3.13 -B KHO/ops/land_evidence_nguon.py --root <tmp> --tep ops/land/pr765-wp743-land-evidence.yaml` ⇒ cả ba **rc=1**. Lần lượt **2 L1**, có `khong_xung_dot`; **1 L1 + 2 L2 + 1 L3**, 02:58:54Z ≥ 02:58:26Z; **1 L1 tại `$.spec.nguon`**. [c6e2401](evidence/history-c6e2401.log), [1a4c417](evidence/history-1a4c417.log), [d60b9e6](evidence/history-d60b9e6.log).
- Import bản kiểm riêng, đặt `MIEN_TRU_CUTOVER={}` trong bộ nhớ rồi gọi `main(['--root', KHO])` ⇒ **rc=1; 16 ĐẠT, 12 ĐỎ, 82 vi phạm toàn L1, 0 KHÔNG ĐO ĐƯỢC**. [Log](evidence/no-exemption.log). Không sửa dictionary trên đĩa.
- Kiểm ảnh cutover độc lập bằng `git ls-tree -r --name-only c73af7b ops/land` và `git show c73af7b:<path>`: **28 tên**, fingerprint `5311e7557cd75ef2f3b06371c66a4830d4970613c1e98a8fd4af732d7dab2257`, khớp hằng test. c10 không tính kỳ vọng từ dictionary đang kiểm. Mutation đổi tên `plat-x8` thành `plat-x9` ⇒ **rc=3 + đúng DO:c10**; thêm tên có mutation chính thức; c09 đo khớp băm rồi sửa một byte bị kiểm đầy đủ; c11 đòi **m=k=28**. [Đổi tên](evidence/mutation-rename.log).
- Ngoài năm hoán vị Q3, mutation bỏ riêng so nội dung số L2 ⇒ **rc=3 + đúng DO:c05**, chết tại ca nguồn metadata, không vì lỗi vô can. [Log](evidence/mutation-skip-numbers.log). Bộ phân hạng chỉ tính GIET khi rc=3 và đúng marker ca đích; tự kiểm KeyError rc=4 và thay đổi vô hại đều đạt. Mỗi L1–L5 có mutation đúng ca trong bộ 33/33.
- Probe CLI riêng trong `measure.py`: khóa YAML trùng che lời khai ⇒ **rc=2**; `nguon_positive: 123` ⇒ **rc=1 L2**; `positive: 123` có nguồn thật ⇒ **rc=0** (không chứa token số dạng L2); mốc sau merge tại khóa mapping ⇒ **rc=1 L3**; mốc phân số Z sau merge ⇒ **rc=1 L3**; mốc offset có nháy ⇒ **rc=0** (ngoài mẫu Z đóng băng); glob tệp thật, thư mục thật và symlink nguồn nội bộ ⇒ **rc=0**. Từng argv/rc/stdout trong `evidence/probe-*.log`, tổng hợp ở [measure.log](evidence/measure.log). Các ca c02/c03/c08 còn đo glob rỗng/sai loại, token thoát gốc có sẵn, thiếu provenance, YAML hỏng, readback lỗi, kiểu YAML lạ và lỗi đọc nguồn bằng mock.
- `ruff check --no-cache --select F KHO/ops/land_evidence_nguon.py KHO/ops/land_evidence_nguon_test.py` ⇒ **rc=0, All checks passed**, F delta=0 trên hai tệp mới. `git -C KHO diff --check 1022a33 HEAD` ⇒ **rc=0**. `git -C KHO diff --numstat 1022a33 HEAD` ⇒ **312 + 388 = 700 dòng thêm / 2 tệp; trần ngoại lệ 700 theo prompt**.
- `git -C KHO status --porcelain --ignored > evidence/status-before` trước chạy và tương tự `status-after` sau chạy; `cmp evidence/status-before evidence/status-after` ⇒ **rc=0**. Kiểm head/tree cuối vẫn khớp; diff-check cuối sạch. [Head cuối](evidence/head-final).

## Đối chiếu nghiệm thu và lựa chọn đã khai — không tính P3

Các tiêu chí g1 đo được đều đạt: cây thật m=k; tái dựng L1 lượt 1; L2 thiếu nguồn/metadata/đúng số/đổi số; L3 trước-bằng-sau merge và chuyển post; L4 YAML hỏng/provenance vắng; L5 lệch byte/thêm tên; mutation từng luật; ba head thực địa; lint và diff-check. F07 là yêu cầu độ phủ bổ sung ở các lượt trước, nay đã đóng.

Không tìm thấy ca hiện hữu ra ĐẠT sai trong phạm vi phép đo. Không phát hiện ca đích xanh chỉ nhờ một lỗi khác hay mutation rc=4 bị tính giết. Ca ưu tiên Q3 thực sự đổi kết quả nội dung L2, không dùng miễn trừ.

Docstring khai rõ L1 chỉ đo tồn tại, L2 chỉ so token số; không hứa kiểm ngữ nghĩa. So `measured` không phân biệt hoa thường và loại tự trỏ được khai là chặt hơn Q3. Từ chối merge/alias/kiểu YAML ngoài mô hình được khai. Chọn readback đúng PR theo tên hồ sơ được mô tả ngay hàm và được c07 đo bằng readback lân cận có thời gian xung đột; phù hợp cấu trúc thực địa. Offset có nháy ngoài regex Z của spec; phân số Z là hỗ trợ thêm. `positive` kiểu số vẫn phải có nguồn nhưng không tự tạo yêu cầu nội dung khác ngoài hai dạng token đóng băng. Những điểm này không phải finding.

G2 nối CI còn ngoài write set g1; packet tổng thể chưa thể coi xong chỉ từ verdict g1 này. Không tính nợ g2 thành P3.

## KHÔNG ĐO ĐƯỢC

- Không xác minh trực tiếp GitHub issue/lease hoặc ngoại lệ 700; dùng authority trực tiếp trong prompt. Không xác nhận launcher, review receipt, assurance land, required checks bên ngoài hay g2.
- Không soạn đường dẫn thoát cây/mã tấn công mới; chỉ chạy c03 có sẵn. Symlink bổ sung chỉ trỏ nguồn nội bộ. Không suy kết quả cho mọi trạng thái quyền truy cập/filesystem; lỗi đọc được test bằng mock.
- Không chạy toàn bộ CI/repo, không kiểm ngữ nghĩa nguồn (ngoại phạm vi). Probe/mutation bổ sung chạy trên 3.13; bộ test chính chạy đủ 3.11–3.14. Không suy sang mọi OS hoặc phiên bản YAML.
