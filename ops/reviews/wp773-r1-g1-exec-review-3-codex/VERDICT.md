Reviewed commit: 5250883f3222a277df7c0eba50f2f9a3e0b45fa1

verdict: changes_requested
P1=0 P2=2 P3=0

Reviewer: Codex, provider OpenAI; trực tiếp chạy shell/tool trong phiên review độc lập với executor Claude. Không suy danh tính model từ GitHub actor, không tự chứng nhận launcher/receipt hay assurance `human_audited`. Review g1, lượt 3, theo chỉ thị chủ kho cho review tới P1=P2=0; không áp trần hai lượt cũ. Tree: `225b3fc0d4eaa29d6877d0094c574ada6be19bed`. KHO giữ read-only.

## Findings

### F01 — P2 — `ops/land_evidence_nguon.py:175`: khoá trùng bên trong nguồn YAML merge vẫn bị ghi đè trước khi kiểm

Nhánh bỏ qua tag merge sửa đúng lỗi sentinel null, nhưng `SafeLoader.construct_mapping` ở dòng 185 gọi `flatten_mapping`: các mapping nằm trực tiếp trong giá trị `<<` được làm phẳng mà không qua constructor kiểm trùng của chúng. Hồ sơ `x: {<<: {a: 'measured — khong nguon', a: ok}}` trả **ĐẠT rc=0**. Thay hai khoá `a` bằng `null` cũng xanh. Lời khai đầu bị mất; vi phạm L1 và cam kết từ chối khoá trùng của L4. Đây là khoá trùng ngay trong một mapping nguồn, không phải override hợp lệ giữa mapping nguồn và mapping nhận merge.

PHÉP ĐO: `PYTHONDONTWRITEBYTECODE=1 python3.13 -B evidence/probes.py > evidence/probes.log` (rc=0), mục `merge_duplicate` và `merge_null_duplicate`: CLI rc=0, 1 ĐẠT, 0 vi phạm. Đối chứng cùng cấu trúc bỏ dòng trùng: lời khai thiếu nguồn ⇒ rc=1 L1; lời khai có `a.json` thật ⇒ rc=0. Provenance có thật, không miễn trừ. `python3.13 -B evidence/extra.py` tái lập đầu vào merge trên 3.11–3.14: cả bốn rc=0. [Probe và đối chứng](evidence/probes.log), [bốn Python](evidence/extra.log).

Chốt bổ sung: `LAND_EVIDENCE_NGUON_MA=/home/user/rv773/ops/land_evidence_nguon.py python3.13 -B evidence/regression.py --mot-ca r01_merge_duplicate` ⇒ **rc=3 + `DO:r01_merge_duplicate:`**, không lỗi vô can. [Kết quả có rc](evidence/regression-results.json).

HINT: kiểm khoá trùng trên từng mapping node nguyên gốc trước khi `flatten_mapping` làm thay đổi chúng, bao gồm mapping trong merge đơn, merge dạng danh sách và merge lồng. Có thể tiền duyệt cây node với tập đã thăm, rồi mới dựng dữ liệu. Phân biệt khoá trùng nội bộ với override giữa các mapping hợp lệ; không chỉ kiểm trên mapping đã flatten vì sẽ từ chối override đúng. Thêm ca chuỗi/null trong nguồn merge và giữ ca merge hợp lệ hiện có. Không chỉ vá hai ví dụ; cần kiểm mọi đường loader làm phẳng mapping.

### F04 — P2 — `ops/land_evidence_nguon.py:194`: ngày YAML không nháy gây ngoại lệ ngay trong loader, ngoài chốt ngày sai

`_thoi_diem` đã xử lý ngày sai trong chuỗi có nháy/readback, nhưng PyYAML tự dựng ngày/timestamp không nháy trước khi tới hàm ấy. `x: 2026-02-30` và `pre_merge_checks: [2026-99-16T02:00:00Z]` ném `ValueError` từ `construct_yaml_timestamp`. Ranh giới parse chỉ bắt `yaml.YAMLError`, nên CLI **rc=1 bằng traceback, stdout rỗng**, thiếu cả hai dòng tổng kết. Đây là KHÔNG ĐO ĐƯỢC theo L4/Q6, không phải ĐỎ có vi phạm.

PHÉP ĐO: cùng `evidence/probes.py` (rc=0), mục `unquoted_bad_date` và `unquoted_bad_date_plain`: CLI rc=1, traceback `ValueError`. `python3.13 -B evidence/extra.py` tái lập ngày 30-02 trên cả 3.11–3.14: cùng rc=1, không tổng kết. [Log](evidence/probes.log).

Chốt bổ sung: `LAND_EVIDENCE_NGUON_MA=/home/user/rv773/ops/land_evidence_nguon.py python3.13 -B evidence/regression.py --mot-ca r04_yaml_date` ⇒ **rc=3 + `DO:r04_yaml_date:`**. Bản sao `/tmp/rv773-r3-date-fixed.py` chỉ đổi `except yaml.YAMLError` thành bắt thêm `ValueError` ở ranh giới parse: cùng chốt ⇒ **rc=0** cho cả hai đầu vào. Đây là đối chứng chẩn đoán, chưa phải patch production được kiểm toàn diện. [Script](evidence/regression.py), [rc và đầu ra](evidence/regression-results.json).

HINT: chuyển lỗi dựng scalar YAML do dữ liệu sai sang `KhongDoDuoc` tại ranh giới parse (hoặc constructor tương ứng), giữ tổng kết Q6. Thêm ca ngày/timestamp không nháy ở cả khoá và giá trị; đột biến bỏ chốt phải chết qua kiểm rc/tổng kết, không qua ngoại lệ vô can. Ca F04 hiện hành chỉ thử chuỗi có nháy và JSON readback nên không đo đường này.

## Đã đo

`KHO=/home/user/rv773`; `SP` là thư mục cha của thư mục ra. Lệnh điều phối, lệnh con, rc và đầu ra được lưu trong [evidence](evidence/). Mọi bản sao/cây dựng ở `/tmp` hoặc thư mục ra; Python dùng `-B`/`PYTHONDONTWRITEBYTECODE=1`.

- `sha256sum /home/user/rv773-spec-r1.md`: rc=0, đúng `063ccaa692372d8f431af07fcb86acccef32435e4b69e7a63e3b0a4ee67e02dd`. Đọc spec L1–L5, Q1–Q6, nghiệm thu, hai verdict trước, AGENTS và chỉ dẫn repo liên quan; đọc hai tệp và diff toàn bộ cùng diff vá lượt 2.
- `git -C KHO rev-parse HEAD HEAD^{tree}`: rc=0, head/tree như trên. `git -C KHO diff --numstat c73af7b 5250883`: rc=0, **2 tệp / 639 dòng thêm; trần ngoại lệ 700 theo chỉ thị chủ kho trong prompt**. Chỉ hai tệp được phép, không sửa workflow/hồ sơ cũ. [Numstat](evidence/stat.log), [diff](evidence/diff.log).
- `PYTHONDONTWRITEBYTECODE=1 python3.13 -B evidence/run_checks.py`: rc=0. Với mỗi `v=3.11,3.12,3.13,3.14`, chạy `PYTHONPATH=$SP/yaml-python$v PYTHONDONTWRITEBYTECODE=1 python$v -B KHO/ops/land_evidence_nguon_test.py`: **tất cả rc=0, CA 13/13, ĐỘT BIẾN 25/25 giết đúng lý do, TỰ KIỂM PHÂN HẠNG ĐẠT (2), TỔNG ĐẠT**. [3.13](evidence/test-3.13.log); các log phiên bản khác cùng thư mục.
- `python3.13 -B KHO/ops/land_evidence_nguon.py --root KHO`: rc=0, **0 ĐẠT · 28/28 miễn trừ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 28**, `TỔNG: ĐẠT`. [Cây thật](evidence/tree.log).
- Với `c=c6e2401,1a4c417,d60b9e6`: `git -C KHO archive <c> ops/land` rc=0; giải nén tar vào `/tmp/rv773-r3-history/<c>` thành công; `python3.13 -B KHO/ops/land_evidence_nguon.py --root <tmp> --tep ops/land/pr765-wp743-land-evidence.yaml` đều rc=1. Lần lượt **2 L1** (gồm `khong_xung_dot`), **1 L1 + 2 L2 + 1 L3** (02:58:54Z ≥ 02:58:26Z), **1 L1 tại `$.spec.nguon`**. [c6e2401](evidence/history-c6e2401.log), [1a4c417](evidence/history-1a4c417.log), [d60b9e6](evidence/history-d60b9e6.log).
- `PYTHONDONTWRITEBYTECODE=1 python3.13 -B evidence/probes.py > evidence/probes.log`: rc=0. Xoá miễn trừ chỉ trong module import riêng ⇒ validator rc=1, **16 ĐẠT, 12 ĐỎ, 82 vi phạm toàn L1, 0 KHÔNG ĐO ĐƯỢC**. `git ls-tree`/`git show c73af7b:<path>` băm từng blob độc lập: 28 tên, vân tay `5311e7557cd75ef2f3b06371c66a4830d4970613c1e98a8fd4af732d7dab2257`, khớp hằng test. Vân tay không tính lại từ dictionary đang bị kiểm. c09 đo lệch byte mất miễn trừ; c11 đòi m=k=28. Mutation đổi `plat-x8` thành `plat-x9` ⇒ rc=3 + đúng `DO:c10...`; mutation thêm tên chính thức cũng bị giết.
- Probe lượt 2: null trùng ở root ⇒ rc=2; ca lồng cũng được c08 đo. `!!set`, `!!omap`, `!!pairs`, `!!binary` ⇒ rc=2 có tổng kết và lý do ngoài mô hình. **F05 đóng theo phương án từ chối được phép; F01 đóng nhánh null trực tiếp, còn nguồn merge như finding trên**. Readback chính PR `merged_at: null` ⇒ rc=2. Chạy riêng ba mutation `F01_null_lam_dau_bo_qua`, `F05_bo_tu_choi_kieu_la`, `L3_readback_null_bo_qua` qua cơ chế test chính thức: cả ba `GIET`, tức rc=3 + đúng `DO:<ca>:`. Chốt null readback thiếu ở lượt 2 nay có răng.
- Các ca chính thức đo lại mapping `pre_merge_checks` cả khoá/value, glob chỉ khớp thư mục, ngày sai có nháy/readback, token thoát gốc c03 có sẵn. Không phát hiện tín dụng giả trong 25 mutation: phân hạng đòi đúng rc=3 và `DO:<ca>:`, rc=4 không được tính giết. Mutation bỏ riêng kiểm nội dung L2 bổ sung ⇒ rc=3 + `DO:c05...`.
- `PYTHONDONTWRITEBYTECODE=1 python3.13 -B evidence/extra.py > evidence/extra.log`: rc=0. Symlink nguồn nội bộ và ưu tiên provenance trước `ops/land` ⇒ rc=0. Mốc phân số sau merge ⇒ rc=1 L3; mốc offset có nháy ⇒ rc=0 (ngoài regex Z của spec); `positive: 123` có nguồn ⇒ rc=0 (không có token số L2). Chỉ readback PR lân cận ⇒ rc=0 có ghi L3 không áp dụng; null readback chính PR ⇒ rc=2.
- **Chốt chưa có ca canh:** bản sao `/tmp/rv773-r3-read_error_green.py` thay duy nhất `raise KhongDoDuoc(f"đọc nguon_positive: {e}")` bằng `return [], []`. Chạy `LAND_EVIDENCE_NGUON_MA=<bản sao> python3.13 -B KHO/ops/land_evidence_nguon_test.py --mot-ca <từng ca>`: **13/13 rc=0**, mutation sống. Đối chứng mock `Path.read_bytes` chỉ ném `OSError` khi đọc nguồn `a.txt`: head rc=2, bản sao rc=0. Đây là khoảng trống coverage nhánh đọc lỗi, chưa phải lỗi hiện hữu trên head hay vi phạm yêu cầu tối thiểu ≥1 mutation mỗi luật. Nên thêm ca lỗi đọc nguồn và mutation này. [Mã phép đo](evidence/extra.py), [log](evidence/extra.log).
- Hai lệnh regression nêu trong findings ⇒ rc=3 đúng chốt, bản đối chứng sửa ranh giới parse ⇒ rc=0. Không tính traceback CLI con thành tín hiệu giết nếu test ngoài chưa kiểm đúng hợp đồng. [Kết quả](evidence/regression-results.json).
- `ruff check --no-cache --select F KHO/ops/land_evidence_nguon.py KHO/ops/land_evidence_nguon_test.py`: rc=0, All checks passed, F delta=0. `git -C KHO diff --check c73af7b 5250883`: rc=0. [ruff](evidence/ruff.log), [diff-check](evidence/diff-check.log).
- `git -C KHO status --porcelain --ignored` trước/sau; `cmp evidence/status-before evidence/status-after`: **rc=0**, không đổi trạng thái KHO. Head cuối phép đo vẫn exact SHA được giao.

## Đối chiếu tuyên bố và nghiệm thu

Các phép nghiệm thu cụ thể về cây thật, L1/L2/L3 dựng lại #771, đổi số nguồn, chuyển post-merge, provenance vắng, miễn trừ, fingerprint, mutation tối thiểu mỗi luật và lịch sử đều tái lập. Hai đường F01/F04 còn làm hỏng L1/L4 và hợp đồng Q6; chưa đạt ngưỡng review P2=0.

Không thấy ca chính thức xanh nhờ lỗi vô can hoặc mutation được đếm giết bằng rc=4. Nhưng kiểm ngày sai hiện chỉ có mặt cho đường chuỗi có nháy/readback; kiểm trùng chưa đi qua mapping nguồn merge. Không được suy bộ test xanh là đã đo hai đường ấy.

Docstring khai rõ không kiểm ngữ nghĩa nguồn, L2 chỉ kiểm token số, tự trỏ không tính nguồn và `measured` không phân biệt hoa thường. Chọn readback theo số PR trong tên có mô tả và c07 đo để tránh readback lân cận; hợp lý trong phạm vi này. Hỗ trợ phần giây thập phân và datetime có múi giờ chặt hơn tập mốc Z tối thiểu của spec; chuỗi offset chưa được đo theo L3 và không tính finding vì spec chỉ định Z. Cam kết từ chối khoá trùng/ngày sai vẫn rộng hơn phép đo như findings. g2 nối CI ngoài lượt này; không coi g1 xanh là packet đã hoàn tất.

## KHÔNG ĐO ĐƯỢC

- Không truy cập GitHub issue/lease/ngoại lệ kích thước/CI từ xa. Review dùng spec đã kiểm băm, exact checkout, lịch sử cục bộ và chỉ thị chủ kho trong prompt về trần 700 cùng review không giới hạn. Không xác nhận g2 đã land hoặc tự cấp assurance/approval cho land.
- Không soạn đường dẫn thoát cây, mã khai thác, alias gây cạn tài nguyên hay symlink thoát gốc. Chỉ chạy c03 sẵn có và symlink nội bộ. Lỗi đọc nguồn được đo bằng mock có kiểm soát; chưa vét mọi dạng lỗi I/O hoặc hệ thống tệp.
- Không xác minh ngữ nghĩa chứng minh câu văn của nguồn (ngoại phạm vi spec); không chạy toàn bộ test repo/CI. Đã chạy các gate chuyên biệt của hai tệp trên bốn Python.
