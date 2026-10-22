Reviewed commit: bf5993aaf81a2af72dc533c0d640485f8e47f2ec

verdict: changes_requested
P1=0 P2=2 P3=0

Reviewer: Codex, provider OpenAI, phiên review độc lập với executor Claude; trực tiếp chạy shell/tool trong sandbox. Không suy model/transport từ GitHub actor, không tự chứng nhận launcher hay assurance `human_audited`. Review g1, lượt 2; tree `59aa346916ac16c8b0c5b30b126b30f8109f2d97`. KHO được giữ read-only. Spec có sha256 đúng `063ccaa692372d8f431af07fcb86acccef32435e4b69e7a63e3b0a4ee67e02dd`.

## Findings

### F01 — P2 — `ops/land_evidence_nguon.py:174`: vá khoá trùng còn bỏ lọt khoá YAML null

F01 lượt 1 chưa đóng hết. Dùng `None` đồng thời làm dấu bỏ qua khoá merge và giá trị thật của khoá YAML null khiến điều kiện `khoa is not None` bỏ qua mọi lần kiểm trùng của khoá null. Hồ sơ có hai dòng `null: 'measured — khong nguon'` và `null: ok` vẫn ĐẠT rc=0; lời khai thứ nhất biến mất trước L1. Provenance tồn tại, không có miễn trừ, nên phép đo không bị lỗi khác che.

PHÉP ĐO: `PYTHONDONTWRITEBYTECODE=1 python3.13 -B evidence/probes.py > evidence/probes.log` (rc=0), mục `duplicate_null`: CLI rc=0, `1 ĐẠT`, `0 vi phạm`, `TỔNG: ĐẠT`. Đối chứng khoá `x` trùng: rc=2 đúng bản vá. Script chạy CLI thật qua subprocess và ghi cả stdout/stderr; xem [probes.py](evidence/probes.py), [probes.log](evidence/probes.log).

HINT: trong `map_khong_trung`, bỏ qua riêng node có tag merge trước khi dựng/kiểm khoá; đừng dùng giá trị `None` của khoá làm sentinel. Giữ kiểm lỗi khoá không băm được qua parser. Thêm ca null trùng ở root và mapping lồng nhau, đòi rc=2; giữ ca merge hợp lệ rc=0 để tránh vá làm hỏng override YAML hợp lệ. Rủi ro cần canh: sentinel lẫn giá trị khoá thật và false positive ở `<<`.

Đối chứng đã chạy ở `/tmp`: thay điều kiện bằng kiểm tag merge riêng làm chính đầu vào này chuyển rc=0 → rc=2 (`khoá trùng None`), còn cả 13 ca hiện hành vẫn xanh. `LAND_EVIDENCE_NGUON_MA=/tmp/rv773-null-fixed.py python3.13 -B evidence/regression.py --mot-ca r01_null_key` rc=0; trỏ lại mã head rc=3, có `DO:r01_null_key:`. Đây là chốt có răng trên bản sao, không phải traceback. [extra.log](evidence/extra.log), [regression.log](evidence/regression.log).

### F05 — P2 — `ops/land_evidence_nguon.py:124`: chuỗi YAML trong set/ordered map không được L1 đo

Q3/L1 áp dụng mọi chuỗi YAML ở bất kỳ độ sâu, không giới hạn hồ sơ ở dict/list. SafeLoader chấp nhận `!!set` thành Python set và `!!omap` thành list các tuple; `duyet` chỉ đi xuống dict/list. Hai hồ sơ hợp lệ `x: !!set {'measured — khong nguon': null}` và `x: !!omap [{a: 'measured — khong nguon'}]` đều trả ĐẠT rc=0, dù có chuỗi lời khai thiếu nguồn. Vì không phát hiện lời khai, cùng nhánh còn bỏ qua điều kiện cần provenance. Docstring hứa mọi chuỗi/mọi độ sâu rộng hơn phép đo thật.

PHÉP ĐO: cùng lệnh `evidence/probes.py`, các mục `set_string`, `omap_string`: cả hai CLI rc=0, `1 ĐẠT`, `0 vi phạm`, tổng ĐẠT. Provenance được dựng sẵn để cô lập L1. Đối chứng chỉ bổ sung tuple/set vào nhánh duyệt trên bản sao `/tmp/rv773-walker-fixed.py`: cả hai chuyển rc=1, đúng L1, cả 13 ca hiện hành vẫn xanh. `LAND_EVIDENCE_NGUON_MA=/tmp/rv773-walker-fixed.py python3.13 -B evidence/regression.py --mot-ca r02_collections` rc=0; trỏ lại mã head rc=3 và `DO:r02_collections:`. Chi tiết trong [extra.py](evidence/extra.py), [extra.log](evidence/extra.log), [regression.py](evidence/regression.py), [regression.log](evidence/regression.log).

HINT: hoặc duyệt đầy đủ các kiểu tập hợp SafeLoader tạo, hoặc từ chối rõ kiểu ngoài mô hình hỗ trợ bằng `KhongDoDuoc` trước khi kết luận ĐẠT. Nếu chọn từ chối thì test đòi rc=2 thay cho rc=1. Thêm ca từng kiểu được parser chấp nhận; mutation bỏ nhánh hỗ trợ/từ chối phải bị chốt giết. Rủi ro: ordered map có cặp khoá/giá trị trong tuple; không được chỉ kiểm giá trị rồi lại bỏ sót khoá. Bản đối chứng ở đây chỉ chứng minh đường bỏ sót L1, không phải bản vá production đã kiểm đủ L2/L3.

## Đã đo

`KHO=/home/user/rv773`; `SP` là thư mục cha của thư mục ra. Các lệnh điều phối được lưu tại [run_checks.py](evidence/run_checks.py), [probes.py](evidence/probes.py), [extra.py](evidence/extra.py). Mọi cây dựng và bản sao mã ở `/tmp`; không ghi vào KHO. Log từng lệnh có command, rc và đầu ra.

- `sha256sum /home/user/rv773-spec-r1.md`: rc=0, khớp băm đã nêu. Đọc spec L1–L5, Q1–Q6 và bảng nghiệm thu; đọc AGENTS và hướng dẫn repo liên quan; đọc hai tệp mới và diff lượt 1 → lượt 2.
- `git -C KHO rev-parse HEAD HEAD^{tree}`: rc=0, đúng head/tree đầu verdict. `git -C KHO diff --stat c73af7b bf5993a`, `--numstat`: rc=0, **2 tệp / 624 dòng thêm; trần ngoại lệ 600**. Vượt trần đã được executor báo theo prompt, không tính finding. Write set chỉ hai tệp; không chạm workflow hay hồ sơ cũ (Q1/Q5).
- Với mỗi `v=3.11,3.12,3.13,3.14`: `PYTHONPATH=$SP/yaml-python$v PYTHONDONTWRITEBYTECODE=1 python$v -B KHO/ops/land_evidence_nguon_test.py`: cả bốn rc=0; **CA 13/13, ĐỘT BIẾN 22/22, TỰ KIỂM PHÂN HẠNG ĐẠT (2), TỔNG ĐẠT**. [Log 3.13](evidence/test-3.13.log); ba log còn lại cùng thư mục evidence.
- `python3.13 -B KHO/ops/land_evidence_nguon.py --root KHO`: rc=0, **0 ĐẠT · 28/28 miễn trừ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 28**, `TỔNG: ĐẠT`; [tree.log](evidence/tree.log).
- Với từng `c=c6e2401,1a4c417,d60b9e6`: `git -C KHO archive <c> ops/land` và `tar -x -C <tmp>` đều rc=0; chạy `python3.13 -B KHO/ops/land_evidence_nguon.py --root <tmp> --tep ops/land/pr765-wp743-land-evidence.yaml` đều rc=1. Kết quả lần lượt **2 L1** (có `khong_xung_dot`), **1 L1 + 2 L2 + 1 L3** (02:58:54Z ≥ 02:58:26Z), **1 L1 tại `$.spec.nguon`**. [c6e2401](evidence/history-c6e2401.log), [1a4c417](evidence/history-1a4c417.log), [d60b9e6](evidence/history-d60b9e6.log).
- `PYTHONDONTWRITEBYTECODE=1 python3.13 -B evidence/probes.py > evidence/probes.log`: rc=0. Xoá `MIEN_TRU_CUTOVER` chỉ trong module đã import riêng: validator rc=1, **16 ĐẠT, 12 ĐỎ, 82 vi phạm toàn L1, 0 KHÔNG ĐO ĐƯỢC**. Dùng `git ls-tree -r --name-only c73af7b ops/land` rồi `git show c73af7b:<path>` (đều thành công) băm độc lập từng blob: 28 tên, vân tay `5311e7557cd75ef2f3b06371c66a4830d4970613c1e98a8fd4af732d7dab2257`, khớp hằng test. Vân tay không tính lại từ dictionary được kiểm nên độc lập. Mutation đổi tên `plat-x8` thành `plat-x9`, chạy `--mot-ca c10_l5_danh_sach_dong_bang`: rc=3 + đúng `DO:c10...`. Mutation thêm tên chính thức cũng bị giết; c09 đo byte lệch mất miễn trừ; c11 thật sự đòi m=k=28.
- `PYTHONDONTWRITEBYTECODE=1 python3.13 -B evidence/extra.py > evidence/extra.log`: rc=0. Chạy riêng lại các mutation `F01_bo_chot_khoa_trung`, `F01_chan_ca_khoa_merge`, `F02_bo_khoa_mapping`, `F02_khoa_khong_chuoi`, `F03_glob_chi_can_ton_tai`, `F04_ngay_sai_traceback`, `L5_doc_tep_lan_hai`: đều **GIẾT đúng chốt**, bộ phân hạng đòi rc=3 và đúng `DO:<ca>:`. F04 có subprocess CLI chết rc=1 như lỗi cũ, nhưng test bao ngoài bắt bằng chốt kiểm rc=2 và kết thúc, trả rc=3 đúng chủ đích; không đếm ngoại lệ vô can rc=4 là giết.
- Probe vá lượt 1: duplicate khoá chuỗi rc=2; `pre_merge_checks` mapping có mốc ở khoá rc=1 L3; glob chỉ khớp thư mục `.json` rc=1 L1; ngày sai rc=2, đủ dòng tổng kết, không traceback. Ca ngày sai ở readback cũng được c08 chạy qua CLI thật. **F02, F03, F04 lượt 1 đóng; F01 còn nhánh null như trên**. c13 và mutation đọc lần hai chứng minh luật đo cùng byte đã băm; main đọc hồ sơ một lần.
- Probe mở rộng: khoá không băm được rc=2; anchor/alias mapping thường chứa lời khai thiếu nguồn rc=1 L1; merge `<<` với override hợp lệ và nguồn thật rc=0. Symlink nội bộ tới nguồn nội bộ rc=0. `positive: 123` cùng nguồn tồn tại rc=0 (không mang token số L2); `nguon_positive: [123]` rc=1 L2. Timestamp phân số sau merge rc=1 L3; timestamp có offset đặt trong nháy rc=0, ngoài regex Z của spec nên không tính finding.
- Readback PR tương ứng vắng rc=0 **có ghi L3 không áp dụng**; chỉ có readback lân cận cũng vậy; readback tương ứng có `merged_at: null` rc=2. Bỏ chốt null trên bản sao `/tmp/rv773-l3_null_skip.py`, chạy bằng `LAND_EVIDENCE_NGUON_MA=<bản sao> python3.13 -B KHO/ops/land_evidence_nguon_test.py --mot-ca <từng ca>`: **13/13 rc=0**. Đây là chốt hiện chưa được test canh, không phải fail-open đang có ở head. Mutation bỏ kiểm nội dung L2 riêng bị c05 giết rc=3 + `DO:c05...`.
- Phép đối chứng cho hai finding và chốt regression: lệnh và rc lưu nguyên tại [regression.log](evidence/regression.log). Các sửa đối chứng nằm ngoài KHO; không coi việc thêm hỗ trợ rồi test vẫn xanh là “mutation có lỗi sống”; bằng chứng thiếu coverage là dữ liệu sai trên head vẫn qua, trong khi chốt bổ sung chuyển xanh/đỏ đúng nguyên nhân.
- `ruff check --no-cache --select F KHO/ops/land_evidence_nguon.py KHO/ops/land_evidence_nguon_test.py`: rc=0, `All checks passed!`, F delta=0 vì cả hai tệp mới. `git -C KHO diff --check c73af7b bf5993a`: rc=0. [ruff.log](evidence/ruff.log), [diff-check.log](evidence/diff-check.log).
- `git -C KHO status --porcelain --ignored` trước/sau; `cmp /tmp/rv773-status-before /tmp/rv773-status-after`: rc=0. Bản ghi [trước](evidence/status-before), [sau](evidence/status-after) giống nhau.

## Phạm vi tuyên bố và nghiệm thu

Các phép nghiệm thu cụ thể executor khai đều tái lập được: cây thật m=k, dựng L1/L2/L3, chuyển post-merge, đổi số nguồn, YAML lỗi, thiếu provenance, băm lệch, danh sách đóng băng, mutation mỗi luật và ba head lịch sử. Tuy nhiên Q3/L1 và cam kết từ chối mọi khoá trùng chưa kín (F01/F05), nên chưa đạt điều kiện review P2=0. Không thấy ca chính thức nào bị đếm giết do lỗi vô can; các ca đã có không bao phủ hai đầu vào finding. Chốt null readback cũng chưa có mutation đích canh trong bộ chính thức.

Docstring khai đúng giới hạn không kiểm ngữ nghĩa lời khai; L2 chỉ so token số; g2 chưa nối CI nên không coi packet đã hoàn thành. So `measured` không phân biệt hoa thường, bỏ nguồn tự trỏ, và chọn readback theo số PR trong tên đều được khai (hai lựa chọn đầu ngay docstring đầu, lựa chọn readback tại hàm). Đây là lựa chọn chặt hơn/thu hẹp mốc nhằm tránh PR lân cận, có test và hợp lý trong phạm vi này. Cam kết “mọi chuỗi/mọi độ sâu” và “khoá trùng” còn rộng hơn phép đo như hai finding.

## KHÔNG ĐO ĐƯỢC

- Không kiểm GitHub issue/lease/ngoại lệ kích thước/CI từ xa; không xác nhận g2 đã land. Review dựa spec kiểm băm, exact checkout và lịch sử có sẵn. Không tự chứng nhận bề mặt chạy là `codex_cli` qua launcher hay model identity từ receipt bên ngoài.
- Không soạn token thoát cây, payload khai thác, cấu trúc alias nhằm gây cạn tài nguyên hoặc symlink thoát gốc. Chỉ chạy ca c03 có sẵn và thêm symlink nội bộ. Không tuyên bố đã vét hết đường đọc lỗi/quyền truy cập/symlink.
- Không kiểm ngữ nghĩa chứng minh câu văn của nguồn, theo ngoại phạm vi spec. Không chạy toàn bộ test repo hay CI; đã chạy test/gate chuyên biệt của hai tệp.
- Trần review hai vòng theo hướng dẫn repo đã tới lượt 2; verdict này không cấp quyền mở vòng 3. Việc xử lý checkpoint thuộc chủ kho.
