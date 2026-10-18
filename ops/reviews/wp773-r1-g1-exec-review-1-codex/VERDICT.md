Reviewed commit: 8ff40b14c241c506bdcafbed414fe6edf9544c28

verdict: changes_requested
P1=0 P2=4 P3=0

Reviewer: Codex, provider OpenAI; thực thi bằng shell/tool trong phiên review hiện tại, độc lập với executor Claude. Không suy danh tính model từ GitHub actor. Review g1, lượt 1; không approve/merge/publish. Tree: `74428a09ff2c69d05e2b207dee2b4b1f688471e9`.

## Findings

### F01 — P2 — `ops/land_evidence_nguon.py:171`: khoá YAML trùng làm mất lời khai trước khi kiểm L1/L2/L3

`yaml.safe_load` âm thầm giữ giá trị cuối của khoá trùng. Hồ sơ có `x: 'measured — khong nguon'` rồi `x: ok` được báo ĐẠT, rc=0. Như vậy một chuỗi lời khai có mặt trong hồ sơ không được đo; kết quả xanh phụ thuộc hành vi ghi đè của parser. Cùng cơ chế có thể xoá một mapping `positive` hoặc phần `pre_merge_checks` trước khi duyệt. Cổng cần từ chối YAML mơ hồ thay vì coi việc parse thành công là đủ.

PHÉP ĐO: `python3.13 -B /tmp/rv773-review/probes.py` (script rc=0), mục `duplicate_key`: validator rc=0, `1 ĐẠT`, `0 vi phạm`, `TỔNG: ĐẠT`. Provenance tồn tại nên không bị lỗi thiếu thư mục che phép đo. Script và kết quả: [probes.py](evidence/probes.py), [probes.log](evidence/probes.log).

HINT: dùng SafeLoader có kiểm khoá mapping trùng (quy định rõ xử lý YAML merge), chuyển lỗi sang `KhongDoDuoc`; thêm ca phải rc=2 và ca đột biến bỏ chốt này.

### F02 — P2 — `ops/land_evidence_nguon.py:221`: bỏ mốc ở khoá của `pre_merge_checks` dạng mapping

Nhánh dict lấy `list(pmc.values())`, loại bỏ toàn bộ khoá trước khi `duyet` có cơ hội kiểm chúng. Với readback `merged_at=2026-10-16T02:58:26Z`, `pre_merge_checks: {'2026-10-16T02:59:00Z': ok}` trả ĐẠT rc=0. Đặt chính mapping đó trong một phần tử list lại ĐỎ L3 rc=1. Đây là bỏ sót theo hình dạng đầu vào, trong khi bộ kiểm chủ động hỗ trợ mapping và duyệt cả khoá chuỗi ở nơi khác.

PHÉP ĐO: `python3.13 -B /tmp/rv773-review/probes.py`, mục `pmc_dict_key`: rc=0. `python3.13 -B /tmp/rv773-review/extra.py`, hai mục `DICT_CONTROL`: mapping nằm trong list và timestamp nằm trong value đều rc=1 L3. Cả hai script rc=0; [extra.log](evidence/extra.log).

Đo răng: trên bản sao `/tmp/rv773-review/dict_walk.py`, đổi duy nhất `list(pmc.values()) if isinstance(pmc, dict)` thành `[] if isinstance(pmc, dict)`. Chạy test gốc với `LAND_EVIDENCE_NGUON_MA` trỏ bản sao và `--mot-ca` cho từng ca: **12/12 rc=0**, kể cả `c06_l3_luot2_moc_sau_merged_at`. Đột biến bỏ hoàn toàn kiểm mapping vẫn sống. Lệnh con và vòng chạy nằm trong `extra.py`; không phải lỗi vô can rc=4.

HINT: duyệt toàn bộ cấu trúc `pmc` với đường dẫn phù hợp, hoặc từ chối dạng mapping bằng trạng thái rõ ràng nếu muốn chỉ nhận list; thêm ca khoá/value và mutation tương ứng.

### F03 — P2 — `ops/land_evidence_nguon.py:113`: glob coi thư mục mang đuôi tệp là nguồn tệp

Nhánh thường đòi `is_file()` cho token không kết thúc bằng `/`, nhưng nhánh glob chỉ đòi `exists()`. Dựng provenance chỉ có thư mục rỗng `folder.json`, lời khai `measured — *.json` vẫn ĐẠT rc=0 dù không khớp tệp nào. Vi phạm Q3: glob phải khớp ít nhất một tệp; cũng trái mô tả phân loại token trong docstring.

PHÉP ĐO: `python3.13 -B /tmp/rv773-review/probes.py`, mục `glob_directory`: validator rc=0, `1 ĐẠT`, `0 vi phạm`. Bản sao sửa `and x.exists()]` thành `and x.is_file()]`, chạy `LAND_EVIDENCE_NGUON_MA=/tmp/rv773-review/glob_file.py python3.13 -B /home/user/rv773/ops/land_evidence_nguon_test.py --mot-ca c02_l1_glob_va_thu_muc`: rc=0. Ca hiện tại chỉ đo glob tệp và thư mục literal, không đo glob khớp sai loại.

HINT: lọc glob theo loại token (tệp, hoặc thư mục khi kết thúc `/`) và giữ kiểm nằm trong gốc; thêm ca thư mục mang đuôi `.json`.

### F04 — P2 — `ops/land_evidence_nguon.py:137` (gọi tại 162, 226): ngày sai gây traceback, phá hợp đồng ba trạng thái

Regex chỉ kiểm hình thức; `datetime.fromisoformat` có thể ném `ValueError`, không được chuyển thành `KhongDoDuoc`. `pre_merge_checks: ['2026-99-16T02:59:00Z']` với readback hợp lệ làm CLI thoát rc=1 bằng traceback `ValueError: month must be in 1..12`, không có hai dòng tổng kết bắt buộc. Đây là lỗi đo đầu vào, không phải kết quả ĐỎ có vi phạm; Q6/L4 yêu cầu rc=2 và tổng kết KHÔNG ĐO ĐƯỢC. Đường đọc `merged_at` cũng dùng cùng hàm không bắt lỗi dù docstring hứa sai dạng sẽ thành `KhongDoDuoc`.

PHÉP ĐO: `python3.13 -B /tmp/rv773-review/extra.py`, mục `INVALID_DATE_CLI`: subprocess CLI rc=1, stdout rỗng, stderr traceback; script điều phối rc=0. `probes.py` cũng ghi `bad_date EXCEPTION ValueError`. Không đếm ngoại lệ này là giết đột biến đúng lý do.

HINT: bắt lỗi chuyển đổi ngày và trả `KhongDoDuoc` tại ranh giới đo; thêm ca ngày sai trong hồ sơ và readback, kiểm rc=2 cùng hai dòng cuối, mutation bỏ chốt phải chết bằng `DO:<ca>:`.

## Đã đo

Các lệnh dưới đây chỉ đọc KHO; cây dựng và bản sao mã đều ở `/tmp`. Log/script được chép vào [evidence](evidence/). `KHO=/home/user/rv773`; `SP=/tmp/claude-0/-home-user-tra-luat/25822fa2-ac40-52b8-b361-6687f0dd1ccb/scratchpad`.

- `sha256sum /home/user/rv773-spec-r1.md`: rc=0, đúng `063ccaa692372d8f431af07fcb86acccef32435e4b69e7a63e3b0a4ee67e02dd`. Đã đọc L1–L5, Q1–Q6 và bảng nghiệm thu; đọc hai tệp mã có số dòng và chỉ thị repo.
- `git -C KHO rev-parse HEAD HEAD^{tree}`: rc=0, exact head/tree như đầu verdict. `git -C KHO diff --stat c73af7b 8ff40b1` và `--numstat`: rc=0, **2 tệp / 597 dòng thêm; trần ngoại lệ 600**. Q1/Q5 đúng phạm vi diff, không sửa workflow/hồ sơ cũ.
- Với từng `v=3.11,3.12,3.13,3.14`: `PYTHONPATH=$SP/yaml-python$v PYTHONDONTWRITEBYTECODE=1 python$v -B KHO/ops/land_evidence_nguon_test.py`: tất cả rc=0, `CA: 12/12 dat`, `DOT BIEN: 15/15 bi giet dung ly do`, `TU KIEM PHAN HANG: DAT (2 dot bien)`, `TONG: DAT`. [Các log](evidence/test-3.13.log). Đã đọc bộ phân hạng: rc=3 phải có `DO:<ca>:`, rc=4 không được tính giết; không tìm thấy đột biến chính thức nào được tính giết do lỗi vô can.
- `python3.13 -B KHO/ops/land_evidence_nguon.py --root KHO`: rc=0, `0 ĐẠT · 28/28 miễn trừ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 28`, `TỔNG: ĐẠT`; [tree.log](evidence/tree.log).
- Với từng `c=c6e2401,1a4c417,d60b9e6`: `mkdir -p /tmp/rv773-review/$c`; `git -C KHO archive $c ops/land | tar -x -C /tmp/rv773-review/$c` thành công; `python3.13 -B KHO/ops/land_evidence_nguon.py --root /tmp/rv773-review/$c --tep ops/land/pr765-wp743-land-evidence.yaml`: cả ba rc=1. Lần lượt **2 L1** (gồm `khong_xung_dot` lượt 1), **L1 + 2 L2 + L3** (02:58:54Z >= 02:58:26Z), **1 L1 tại `$.spec.nguon`**. Chi tiết trong ba `history-*.log`.
- `python3.13 -B /tmp/rv773-review/extra.py`: rc=0. Bản module import riêng được xoá `MIEN_TRU_CUTOVER` trong bộ nhớ: validator rc=1, **16 ĐẠT, 12 ĐỎ, 82 vi phạm toàn L1, 0 KHÔNG ĐO ĐƯỢC**; [no-exempt.log](evidence/no-exempt.log). Không sửa mã KHO.
- Cũng trong `extra.py`: `git ls-tree` rồi `git show c73af7b:<path>` băm độc lập từng blob: 28 tên, digest của danh sách đã sắp `5311e7557cd75ef2f3b06371c66a4830d4970613c1e98a8fd4af732d7dab2257`, khớp hằng kỳ vọng test. Vân tay test thật sự độc lập với dictionary lúc chạy. `c11` đo m=k=28; `c09` đo đổi byte mất miễn trừ. Mutation đổi tên `plat-x8` thành `plat-x9` trên bản sao: `--mot-ca c10_l5_danh_sach_dong_bang` rc=3 kèm đúng `DO:c10...`; mutation thêm tên chính thức cũng bị giết.
- `python3.13 -B /tmp/rv773-review/probes.py`: rc=0. Ngoài F01–F04: mốc có phần thập phân sau merge rc=1; timestamp offset có nháy rc=0, không nháy rc=1 (PyYAML datetime). Đây là bất đối xứng được ghi nhận, **không tính finding** vì spec L3 chỉ định token kết thúc Z. Giá trị `positive: 123` có nguồn tồn tại rc=0; số không mang token `N/M`/`hong N` nên không vi phạm L2 đã đóng băng. Scalar số ở nơi khác rc=0 đúng L1 chỉ áp dụng chuỗi. Khoá YAML list không hợp lệ rc=2. Symlink nội bộ tới tệp nguồn nội bộ rc=0, đúng phép phân giải; ca c03 hiện hữu đã chạy trên cả bốn Python.
- Mutation bổ sung bỏ kiểm nội dung L2 (`if not any(...)` thành `if False:`), qua `LAND_EVIDENCE_NGUON_MA` + `--mot-ca c05...`: **rc=3 + đúng `DO:c05...`**, giết thật. Mutation bỏ mapping sống như F02; mutation đổi loại glob qua c02 như F03. Không tính một mutation sửa lỗi thành yêu cầu phải giết.
- `ruff check --no-cache --select F KHO/ops/land_evidence_nguon.py KHO/ops/land_evidence_nguon_test.py`: rc=0, `All checks passed!`; hai tệp mới nên F delta=0. `git -C KHO diff --check c73af7b 8ff40b1`: rc=0.
- `git -C KHO status --porcelain --ignored` lưu trước/sau; `cmp /tmp/rv773-review/status-before /tmp/rv773-review/status-after`: rc=0. Không thay đổi trạng thái KHO.

## Đối chiếu phạm vi và nghiệm thu

Các ca dựng lại L1/L2/L3, phép chuyển sang post-merge, đổi số nguồn, YAML lỗi, thiếu provenance, mất miễn trừ, danh sách đóng băng, mutation tối thiểu từng luật, thực địa và cây thật đều đạt các phép đo executor khai. Chúng chưa chứng minh kín các nhánh đầu vào: ba đường xanh sai F01–F03 và xử lý lỗi F04 còn mở. Bộ test không có ca mapping `pre_merge_checks`; mutation độc lập xác nhận nhánh đó không được canh. Không thấy ca hiện hữu xanh chỉ nhờ một lỗi không liên quan trong các đường đã chạy.

Docstring khai rõ giới hạn không kiểm ngữ nghĩa nguồn, L2 chỉ kiểm token số, chưa nối CI; không coi xanh hiện tại là packet đã hoàn thành g2. So `measured` không phân biệt hoa thường được khai rõ và chặt hơn spec. Chọn readback theo số PR trong tên được khai tại docstring hàm và có c07 đo việc bỏ readback lân cận: hợp lý để tránh lấy mốc PR khác. Tự trỏ hồ sơ bị loại có comment tại dòng 186 và ca c01 đo, nhưng là lựa chọn chặt hơn L1 nguyên văn; nên đưa lựa chọn này lên phần mô tả luật khi sửa. Không nâng thành finding riêng vì không tạo ĐẠT sai.

## KHÔNG ĐO ĐƯỢC

- Không kiểm trực tiếp GitHub issue/lease/CI từ xa; review dựa exact commit, spec đã kiểm băm và lịch sử cục bộ. Không xác nhận việc cấp ngoại lệ 600 trong comment hay g2 đã land. Chúng không được suy từ test xanh.
- Không tự soạn token thoát cây, payload khai thác hoặc symlink thoát gốc theo giới hạn của yêu cầu. Chỉ chạy nguyên ca c03 có sẵn; chỉ bổ sung symlink nội bộ. Không tuyên bố đã vét hết các trường hợp symlink/đọc lỗi/quyền truy cập.
- Không xác minh ngữ nghĩa chứng minh câu văn của các tệp nguồn, theo ngoại phạm vi spec. Không chạy toàn bộ test của repo vì write set chỉ gồm validator độc lập và bộ test riêng.
