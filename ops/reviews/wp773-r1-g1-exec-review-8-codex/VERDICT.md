Reviewed commit: 93ef97e8b03dd1b2e344cdfe4afc660edd899ac8

verdict: changes_requested
P1=0 P2=0 P3=1

Reviewer: Codex (GPT-6), provider OpenAI, execution surface coding-agent sandbox, transport shell/tool trực tiếp; độc lập với executor Claude. Không tự xác nhận launcher/receipt hay assurance `human_audited`. Tree: `021dde3d0180fdb8bb95b3bb5cd397d8bbc5ce30`. KHO được giữ read-only. Trần 750 lấy từ chỉ thị trực tiếp trong prompt lượt 8.

## Finding

**F01 — P3 — `ops/land_evidence_nguon_test.py:166` — các ca offset chỉ đo nhận dạng, chưa canh phép quy đổi múi giờ.**

Các offset hiện có đều bằng 0 (`+00:00`, `+0000`, `-00:00`). Vì vậy một hồi quy bỏ độ lệch khi dựng datetime vẫn qua c06 và toàn bộ 14 ca. Đây là thiếu chốt hồi quy cho chính lớp lỗi L3 mà bản vá connector đang đóng; không phải lỗi thực thi của head hiện tại, và không nâng thành P2.

PHÉP ĐO: `PYTHONDONTWRITEBYTECODE=1 python3.13 -B evidence/measure.py` ⇒ rc=0. Script chép validator vào thư mục tạm, thay đúng một neo tại `ops/land_evidence_nguon.py:150`:

```python
# gốc
return t if t.tzinfo else t.replace(tzinfo=datetime.timezone.utc)
# đột biến
return t.replace(tzinfo=datetime.timezone.utc)
```

Với `LAND_EVIDENCE_NGUON_MA=<bản đột biến>`, chạy `python3.13 -B KHO/ops/land_evidence_nguon_test.py --mot-ca <ca>` cho từng tên trong `CA`: **cả 14 ca rc=0**, kể cả c06; không có traceback hay rc=4. Với cùng readback `merged_at=2026-10-16T02:58:26Z`:

| Mốc pre_merge_checks | Head hiện tại | Bản đột biến |
|---|---|---|
| `2026-10-16T02:00:00-01:00` (=03:00Z, sau merge) | rc=1, L3 | **rc=0, ĐẠT sai** |
| `2026-10-16T03:00:00+01:00` (=02:00Z, trước merge) | rc=0 | **rc=1, ĐỎ sai** |

HINT patch: thêm hai assertion độc lập trên vào c06 và thêm mutation bỏ quy đổi offset. Tôi đã đo trên **bản test tạm**: c06 mở rộng xanh với head (**rc=0**), đỏ với mutation (**rc=3 + `DO:c06_l3_luot2_moc_sau_merged_at:`**, lý do `offset am sau merge: mong rc=1, được 0`). Không sửa test trong KHO. Có thể dùng thêm dạng `±HHMM` khác 0 nếu muốn canh cả hai cách viết.

Bằng chứng: [script tái chạy](evidence/measure.py), [tổng hợp](evidence/measure.log), [c06 hiện hữu sống sót](evidence/tz-mutation-c06_l3_luot2_moc_sau_merged_at.log), [ĐẠT sai trên mutant](evidence/tz-mutant-probe-negative.log), [ca bổ sung xanh trên head](evidence/extended-c06-original.log), [giết đúng chốt](evidence/extended-c06-mutant.log). Đây là một finding về độ phủ, không đếm riêng từng biến thể thời gian thành nhiều P3.

## Đã đo

Quy ước: `KHO=/home/user/rv773`; `SP=/tmp/claude-0/-home-user-tra-luat/25822fa2-ac40-52b8-b361-6687f0dd1ccb/scratchpad`. Mọi Python dùng `-B`, `PYTHONDONTWRITEBYTECODE=1`; chỉ ghi thư mục ra và `/tmp`. Script liên kết chứa lệnh con/đầu vào; log từng phép đo lưu rc và stdout/stderr.

- `sha256sum /home/user/rv773-spec-r1.md` ⇒ rc=0, khớp `063ccaa692372d8f431af07fcb86acccef32435e4b69e7a63e3b0a4ee67e02dd`. Đọc spec Q1–Q6, L1–L5 và nghiệm thu trước diff. `git -C KHO rev-parse HEAD HEAD^{tree}` ⇒ rc=0, head/tree như trên. Đọc AGENTS và tài liệu protocol/CLAUDE/provider liên quan; đối chiếu verdict cũ, đặc biệt lượt 7 và lỗi connector nêu trong prompt.
- `git -C KHO diff 1022a33 93ef97e` và `git -C KHO diff 98d7d25 93ef97e` ⇒ rc=0; đọc toàn bộ hai tệp và vá connector. [Diff đầy đủ](evidence/full.patch). `git -C KHO diff --numstat 1022a33 93ef97e` ⇒ rc=0: **2 tệp / 718 dòng thêm; trần ngoại lệ 750 theo prompt**, đúng write set g1.
- `python3.13 -B KHO/ops/land_evidence_nguon_test.py` ⇒ rc=0: **CA 14/14; DOT BIEN 36/36 bi giet dung ly do; TU KIEM PHAN HANG DAT (2); TONG DAT**. Với `v=3.11,3.12,3.14`: `PYTHONPATH=$SP/yaml-python$v PYTHONDONTWRITEBYTECODE=1 python$v -B KHO/ops/land_evidence_nguon_test.py` ⇒ cả ba rc=0, cùng kết quả. Các tiến trình đã chờ hoàn tất. [3.11](evidence/test-3.11.log), [3.12](evidence/test-3.12.log), [3.13](evidence/test-3.13.log), [3.14](evidence/test-3.14.log).
- `python3.13 -B KHO/ops/land_evidence_nguon.py --root KHO` ⇒ **rc=0; 0 ĐẠT · 28/28 miễn trừ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 28; TỔNG: ĐẠT**. [Log cây thật](evidence/tree.log).
- `python3.13 -B evidence/measure.py` ⇒ rc=0 (đã chạy lại sau khi bổ sung phép đo). Dùng `git -C KHO archive <c> ops/land` ⇒ rc=0, giải nén vào thư mục tạm, rồi `python3.13 -B KHO/ops/land_evidence_nguon.py --root <tmp> --tep ops/land/pr765-wp743-land-evidence.yaml`: `c6e2401` ⇒ **rc=1, 2 L1**, gồm `khong_xung_dot`; `1a4c417` ⇒ **rc=1, 1 L1 + 2 L2 + 1 L3**, mốc 02:58:54Z sau 02:58:26Z; `d60b9e6` ⇒ **rc=1, 1 L1 tại `$.spec.nguon`**. [Lượt 1](evidence/history-c6e2401.log), [lượt 2](evidence/history-1a4c417.log), [lượt 3](evidence/history-d60b9e6.log).
- Bỏ `MIEN_TRU_CUTOVER` trong module import riêng ở bộ nhớ, gọi `main(['--root', KHO])` ⇒ **rc=1, 16 ĐẠT, 12 ĐỎ, 82 vi phạm toàn L1, 0 KHÔNG ĐO ĐƯỢC**. [Log](evidence/no-exempt.log).
- Ảnh cutover đo độc lập bằng `git ls-tree -r --name-only c73af7b ops/land` và `git show c73af7b:<path>` ⇒ 28 tên, fingerprint `5311e7557cd75ef2f3b06371c66a4830d4970613c1e98a8fd4af732d7dab2257`, khớp dictionary và hằng test. c10 dùng vân tay kỳ vọng cố định, không tự tính kỳ vọng từ dictionary đang kiểm. Mutation đổi tên `plat-x8` thành `plat-x9` ⇒ **rc=3 + đúng DO:c10**. Thêm tên có mutation chính thức; c09 đo khớp băm rồi đổi byte; c11 đòi m=k=28. [Đổi tên](evidence/rename-mutation.log).
- Ca c01 thực sự đo L2 tự trỏ: `positive` chứa đúng token nằm trong chính hồ sơ, không có lời khai `measured` để L1 che lỗi ⇒ head ĐỎ L2. Các mutation bỏ chặn tự trỏ và thư mục chứa hồ sơ bị giết trong 36/36. Probe riêng symlink nội bộ tới nguồn thật ⇒ **rc=0**; symlink tới chính hồ sơ ⇒ **rc=1 L2**. [Nguồn thật](evidence/symlink-source.log), [alias chính hồ sơ](evidence/symlink-self.log).
- Probe CLI riêng: khóa YAML trùng ⇒ **rc=2**; `nguon_positive: 123` ⇒ **rc=1 L2**; `positive: 123` có nguồn tồn tại ⇒ **rc=0** (không chứa hai dạng token L2); thời gian sau merge ở khóa mapping ⇒ **rc=1 L3**; mốc phân số `.001Z` sau merge ⇒ **rc=1 L3**. Offset khác 0 trên head cho kết quả đúng ở cả hai chiều như bảng F01. c02/c03/c08 còn đo glob có/rỗng/sai loại, token thoát cây có sẵn, YAML sai, thiếu provenance, lỗi đọc nguồn, readback lỗi, kiểu YAML ngoài mô hình, alias/merge. [Tổng hợp probe](evidence/measure.log).
- Đọc cơ chế `chay_ca`/`phan_hang`: chỉ `TinHieuChotCa` sinh rc=3 và marker đúng ca mới được tính giết; lỗi vô can rc=4 không được tính. Bộ tự kiểm KeyError và thay đổi vô hại đều đạt. Không thấy mutation chính thức nào nhận tín dụng từ lỗi vô can; mỗi L1–L5 có mutation bị giết đúng ca. Ngoại lệ về độ phủ bổ sung là F01, không phủ nhận kết quả 36/36 hiện hữu.
- `ruff check --no-cache --select F KHO/ops/land_evidence_nguon.py KHO/ops/land_evidence_nguon_test.py` ⇒ **rc=0, All checks passed**, F delta=0. `git -C KHO diff 1022a33 93ef97e --check` ⇒ **rc=0**.
- `git -C KHO status --porcelain --ignored` lưu trước/sau; `cmp evidence/status-before evidence/status-after` ⇒ **rc=0**, cả hai rỗng. Không ghi vào KHO.

## Lựa chọn đã khai, nghiệm thu và ngoài phạm vi — không tính P3

Hai lỗi thực thi connector được đóng trên các ca đã đo: `_la_nguon` chặn chính hồ sơ cho cả L1 và L2, gồm alias symlink; L3 nhận và so offset, kể cả độ lệch khác 0. Không tái hiện P1/P2 ở head hiện tại.

`measured — ./` với provenance rỗng có tồn tại ⇒ **rc=0** ([log](evidence/directory-dot.log)). Nó phân giải về provenance trước, thư mục này không chứa hồ sơ. Q3 cho phép token thư mục và L1 không kiểm ngữ nghĩa; vì vậy đây không phải fail-open trái spec. Ví dụ `./` trong docstring phải được hiểu có điều kiện “thư mục chứa hồ sơ”, không phải cam kết cấm token đó ở mọi nền. Không yêu cầu siết thư mục rỗng ngoài spec.

So `measured` không phân biệt hoa thường, loại tự trỏ, từ chối YAML merge/alias/kiểu ngoài mô hình đều được khai. Chọn readback đúng PR theo tên hồ sơ có giải thích trong hàm và c07 canh readback lân cận; không tính là lỗi. L1 chỉ đo tồn tại; L2 chỉ so token số; docstring khai đúng giới hạn ngữ nghĩa. `positive` kiểu số vẫn phải có nguồn, không tự sinh yêu cầu nội dung ngoài dạng token đóng băng.

Các tiêu chí nghiệm thu g1 đã chạy đều đạt: cây thật m=k; tái dựng L1/L2/L3; ba trạng thái L4; cutover L5; mutation từng luật; ba head thực địa; lint/diff-check. F01 là khoảng trống hồi quy của bản vá múi giờ mới, được đo bằng mutation bổ sung. Theo ngưỡng lượt này P3 cũng phải bằng 0 nên chưa approve.

G2 nối CI chưa nằm trong write set g1; packet tổng thể còn nợ g2. Không tính nợ g2 thành P3.

## KHÔNG ĐO ĐƯỢC

- Không xác minh GitHub issue/lease/ngoại lệ qua mạng; dùng spec đã kiểm băm, exact Git OID và authority trực tiếp trong prompt. Không xác nhận launcher, receipt, assurance land hoặc required checks bên ngoài.
- Không soạn đường dẫn thoát cây hay mã tấn công mới; chỉ dùng token thoát cây có sẵn ở c03. Symlink bổ sung chỉ trỏ bên trong cây tạm. Không suy kết quả cho mọi filesystem/quyền truy cập; lỗi đọc đã có mock trong c08.
- Không chạy toàn bộ CI/repo hoặc kiểm ngữ nghĩa của nội dung nguồn. Probe/mutation bổ sung chạy trên 3.13; test chính chạy đủ 3.11–3.14. Không suy sang mọi OS/PyYAML.
- Skill runtime cloud đã được đọc, nhưng không có tool `environment_status` trong danh sách công cụ; không dùng mạng, credentials hay Docker trong review này.
