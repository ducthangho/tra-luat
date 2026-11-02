```text
verdict: changes_requested
reviewed_sha: 435dd91ac6db79fe681daf213412723d40a82571
dem: P0=0 P1=0 P2=0 P3=1
```

Tree: `a3511739e739019bdc4c6f11b54ecbcfecf9ff18`. Reviewer: `openai_codex / codex_cli / machine`; header công bố `gpt-6.1-sol`, effort `xhigh`.

**Lớp `gan-nang-luc-cho-runner` — S822-04 tái mở, P3.**

Vị trí: `ops/specs/wp822.md:122`, `:172`; đối chiếu A11 tại `:127`.

Hai câu giải thích gọi A11 là đo “toàn suite”, nhưng A11 yêu cầu mọi ca **gọi `kiem-gate`**. Tập này hiện có 106 ca trên tổng 406 ca. Biên nhận thực hiện đủ tập A11 cho một mutant vẫn chưa chứng minh đã chạy toàn suite dưới mutant ấy.

Phép đo ngoài checkout:

```text
python3 -B /tmp/wp822-review-r3-efb32f44/probe_matrix.py
rc=0
base, D1–D6: mỗi bản executed=106, red=0

python3 -B /tmp/wp822-review-r3-efb32f44/probe_scope.py
rc=0
all_cases=406
A11_required_cases=106
outside_A11_required=300
```

`matrix.json` lưu tên và kết quả từng ca thực chạy.

HINT: sửa hai câu tại dòng 122/172 thành “toàn bộ ca gọi `kiem-gate`, theo A11”. Đối chiếu tập tên trong receipt với tập caller đã kiểm kê và ghi riêng tổng `CASES`. Nếu muốn đo cả suite thì sửa chính A11 để yêu cầu tập ấy. Khi sửa, giữ cả hai ca codepage; thu phạm vi xuống riêng `kg_*` sẽ mở lại lỗi độ phủ cũ.

**Đối chiếu lượt trước — ở mức đặc tả**

| Finding | Trạng thái | Bằng chứng |
|---|---|---|
| S822-01 | **ĐÃ ĐÓNG — ĐÃ VÁ THẬT** | M3 tách ba dạng. Bỏ khử trùng giữ rc=0 nhưng số `gate id=1` đổi 1→2. Sáu fixture D đều cho 12→0, không crash. |
| S822-02 | **ĐÃ ĐÓNG — ĐÃ VÁ THẬT** | Bỏ K06 vẫn rc=12 nhưng đổi lý do; `kg_n5_thieu` đỏ. M1/A5 nay cùng bác miễn trừ này. |
| S822-03 | **ĐÃ ĐÓNG — ĐÃ VÁ THẬT** | Prototype chỉ sửa bản sao tệp test: loại tín dụng cho crash F02, nhận fallback `suite=1`; bỏ phép loại crash làm tự kiểm đỏ. M6/A12 khả thi trong write set. |
| S822-04 | **CÒN MỞ, thu hẹp còn P3** | A1 và phạm vi caller của A11 đã sửa đúng; hai lời khai “toàn suite” còn sót. |

Không tìm thấy lỗi mới do hai dòng vá M1/A5 sinh ra.

**Bảng kiểm lời khai số**

Đo lại ngày 18-10-2026 UTC trên exact SHA nêu trên.

| Phép đo | Kết quả |
|---|---|
| Diff base→HEAD | Một tệp mới `ops/specs/wp822.md`, +178/-0 |
| Diff lượt 2→HEAD | Chỉ hai dòng M1/A5 thay đổi |
| Kiểm kê | Đủ 37 ID K; 37−6=31 |
| Nền đã chạy | **100/100**, **104/104**, **106/106** |
| D1/K18 | Neo 1 chỗ; đỏ 0/100, 0/104, 0/106 |
| D2/K35 | Neo 1 chỗ; đỏ 0/100, 0/104, 0/106 |
| D3/K10 | Neo 1 chỗ; đỏ 0/100, 0/104, 0/106 |
| D4/K11 | Neo 1 chỗ; đỏ 0/100, 0/104, 0/106 |
| D5/K12 | Neo 1 chỗ; đỏ 0/100, 0/104, 0/106 |
| D6/K13 | Neo 1 chỗ; đỏ 0/100, 0/104, 0/106 |
| A2, sáu fixture riêng | Cả sáu: nền rc=12 đúng lý do → mutant rc=0 |
| A3, nền | rc=12, `thiếu/sai kiểu trường ['conclusion']` |
| A3, D6 | rc=12, khai 1/có 2 id, `THỪA id` |
| K37: `_VANG`→`None` | Thiếu conclusion: 12→0; null: 0→0; sai kiểu: 12→12 |
| M6/A12 | Prototype xanh; bỏ loại crash ⇒ tự kiểm đỏ |
| `doctrine-scan` / `adr-song` | **passed**, rc=0; 10 tệp/0 chỗ chép; 53 ADR/53 dòng |
| Ruff contract | **passed**, rc=0, `RUFF_CONTRACT 3 []` |
| Bare Ruff | **failed** sẵn: test có 2 F541; `tl.py` có 12 F821; base/head cùng rc=1, delta=0 |

Checkout giữ nguyên HEAD/tree, index và hash của 3.764 tệp tracked. Không có ca skipped trong tập 106 ca đã chạy. Toàn suite 406 ca, vòng 168 mutant, CI/release gate/LIVE **not_run**. GitHub/lease, H1–H3 và authority áp trần 8/450 **chưa đo đủ** trong mirror shallow/offline. `wp788.md` không có, đã bỏ qua theo chỉ thị.

Đã lưu [báo cáo đầy đủ](/tmp/wp822-review-r3-efb32f44/VERDICT.md), [manifest bằng chứng](/tmp/wp822-review-r3-efb32f44/evidence_manifest.json) và bản sao tại [verdict-luot3.md](/tmp/claude-0/-home-user-tra-luat/353bc79e-3dd4-5d53-a13a-54256c3f5d49/scratchpad/rv822-3/verdict-luot3.md).