verdict: approve
reviewed_sha: 356a27e1378b2162bbc0be2ec06ff08fdacbdead
Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.

P3 lượt 7 **ĐÓNG / ĐÃ VÁ THẬT**. Không có finding còn mở trong các phép đo dưới đây. Toàn suite đạt **98/98 ca · 153/153 đột biến thường CÓ RĂNG · 2/2 tự kiểm**, `TỔNG: ĐẠT`. AST bỏ docstring của cả hai tệp không đổi so c8a493c. Mười hướng săn có lệnh và output được ghi tăng dần ở dưới.

Base: `b29da0bfe3bfb7a7be69136a1c5c40f82c088a93`; reviewed tree: `c1e160cfd5ddf1a053c2e8413e62f5881badd052`; SPEC SHA256: `d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d`. Đo cục bộ được `uname -s` = `Linux`, `python3 -V` = `Python 3.13.17`, Ruff = `0.16.9`. Không suy tên execution surface từ các dữ kiện đó. Không gọi mạng, không push, không sửa cây được review; đột biến chỉ trên bản sao tạm.

**C4, C5, C7 và điều kiện vận hành/budget của C8: KHÔNG ĐO ĐƯỢC.** Approve này là kết luận review nội dung trên exact SHA; không xác nhận đủ điều kiện merge/land. Không tạo `HINT.patch` vì không có finding cần gợi ý vá.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Finding/phạm vi | Lệnh + output quyết định tại HEAD | Kết luận |
|---|---|---|
| P3 `chu-thich-tro-sai-ca-ngoai-le-lap-trinh`, lượt 7 | `python3 evidence/probe.py extra`: c100 sạch `qua`; cùng m153, c99 vẫn `qua`, c100 `giet_that` với `lỗi lập trình ở is_dir [] bị nuốt/đổi... được không ngoại lệ`; c18 sạch. Docstring hiện trỏ c100 chốt 7. | **ĐÓNG / ĐÃ VÁ THẬT** |
| P3 `chu-thich-nang-ca-thuong-thanh-toan-suite`, lượt 6 | `python3 evidence/ast_check.py`: AST bỏ docstring c8a493c/HEAD bằng nhau ở hai tệp; diff lượt 7/8 không chạm chú thích m156/m157 đã sửa ở c8a493c. Hiện tách no_clamp/toàn suite và citation_drop_next/98 ca thường. | Giữ kết luận đóng lượt 7; không khai chạy lại các suite lịch sử. |
| F1/P2 `loi-do-liet-ke-thu-muc-thoat-traceback` | `python3 evidence/probe.py focused`: m147 `giet_that` tại c99, m148–m151 `giet_that` tại c100; đối chứng sạch. | Vẫn đóng trong phạm vi đo. |
| F2/P3 `loi-do-thieu-chot-ngoai-le-lap-trinh` | Cùng lệnh: m152/m153 `giet_that` tại c100 ở iterdir/is_dir; suite và đối chứng sạch. | Vẫn đóng. |
| F3/P3, OSError ngoài PermissionError | Cùng lệnh: m154→c100, m155→c99, `giet_that` với OSError errno=5 (EIO), đối chứng sạch. | Vẫn đóng. |
| P1 `bien-ngoai-cua-so-surface-chua-co-rang` và ảnh hưởng merge `3883b60` | `python3 evidence/references.py`: c88/c101/c98 chạy riêng `qua`; `focused`: m156/m157 chết đúng c88 (ix-trich-dan-sau-hai-dong/ii-b-trich-dan-dong-sau), m142 chết đúng c101. Thân AST c98 trước merge bằng c101 hiện tại sau bỏ docstring/chuẩn hóa tên. | Giữ kết luận hành vi lượt 5–7 trong các chốt đã đo lại. |

Tập lớp còn mở của lượt 7: 1; đóng được: 1; lớp mới còn mở: 0. Không biến các giới hạn CI/local hoặc lỗi thiếu Ruff ban đầu thành finding nguồn. Bằng chứng chi tiết nằm ở hướng 1, 4, 5, 8, 9 bên dưới.

## BẢNG TIÊU CHÍ

| Tiêu chí | Kết quả | Lệnh / output quyết định |
|---|---|---|
| C1a | **ĐẠT tại đây**; Windows KHÔNG ĐO ĐƯỢC | `python3 evidence/probe.py branches`: C1a sạch rc=1 tổng=2, nêu x và không ĐẠT; chỉ-x sạch rc=1 tổng=1, không báo thiếu tệp. m142 `giet_that` ở từng assertion tách riêng. c101 qua cả suite và chạy riêng. |
| C1b | **ĐẠT tại đây**; Windows KHÔNG ĐO ĐƯỢC | Cùng lệnh: sạch rc=2, stderr nêu x.RECEIPT.YAML/YAML hỏng, không Traceback; m142 `giet_that` riêng chốt C1b vì rc=1/không nêu x. Không đòi tổng ở nhánh YAML hỏng. |
| C2 | **ĐẠT tại đây**; Windows KHÔNG ĐO ĐƯỢC | c89 sạch `qua`; m143 lọc is_file bị c89 `giet_that` trong `focused` và suite. |
| C3 | **ĐẠT** | `python3 evidence/probe.py extra`: mutant hoàn nguyên glob bị c101 `giet_that` vì tổng=1; c18 sạch, nguồn sạch c101 qua. `uname -s`=Linux. |
| C4 Windows CI | **KHÔNG ĐO ĐƯỢC** | Không gọi mạng; không đo jobs/labels/runner_id, hai bước selftest và N/N của dispatch 41113949578 trên exact head. Không sử dụng lời khai executor làm bằng chứng. |
| C5 Ubuntu CI | **KHÔNG ĐO ĐƯỢC** | Không đo độc lập run 41113943723 và hai bước selftest trên exact head. Suite cục bộ không chứng minh CI. |
| C6 | **ĐẠT** | Cổng thật rc=0, tổng=306, TỔNG: ĐẠT. Lệnh đếm độc lập `os.listdir/name.lower().endswith`=306, không lọc is_file. |
| C7 Windows local | **KHÔNG ĐO ĐƯỢC** | Không truy cập/đo ASUS-LAPTOP, trạng thái Online, khoá máy dùng chung, lần chạy head/base hay dòng CSV. |
| C8 | **ĐẠT phần nội dung review**; toàn bộ điều kiện merge **KHÔNG ĐO ĐƯỢC** | 0 P0/P1/P2/P3, approve trên exact SHA 40 ký tự. Trần lời gọi/checkpoint thực tế và kết quả Windows local/CI chưa được xác minh; lượt 8 theo chỉ thị hiện hành. |
| C9 | **ĐẠT các phép đo cục bộ** | Ruff F delta=0 (base=1/head=1 F541, không lint sạch tuyệt đối); doctrine rc=0/10 tệp/0 chỗ; diff-check rc=0; rg glob rc=1/0 dòng; C1a/C1b có bằng chứng dương. `git diff --numstat b29da0b HEAD`: sản phẩm +40/−5, test +300/−2, đúng hai tệp write set. Không xác minh nội dung PR qua mạng. |
| Toàn suite | **ĐẠT** | `PYTHONDONTWRITEBYTECODE=1 python3 cay-kho/ops/bien_nhan_v2_test.py`: rc=0, 98/98 · 153/153 · 2/2, TỔNG: ĐẠT. |
| Đột biến chỉ định và tự chọn | **ĐẠT** | `focused`: m142/m147/m153/m156/m157 chạy riêng và `giet_that` đúng ca; tổng 16/16 m142–m157 có đối chứng sạch. `extra`: mutant tự chọn sản phẩm/thứ tự đảo chết tại c99; mutant tự chọn suite/báo cáo thiếu chi tiết chết tại c98 sau đi qua cơ chế _dot_bien_tep; đều có baseline qua và c18 sạch. |
| `--sinh-no` | **ĐẠT** | rc=0, stderr `# 42 tệp`; khối NO_DA_DO lưu tại evidence/sinh-no.out. |

## BẢNG SĂN

Các mục sau giữ diễn tiến phép đo; kết quả cuối của Ruff nằm ở phần cập nhật hướng 7. Lệnh script đo chạy từ thư mục chứa PROMPT.md, các lệnh cổng ghi rõ cwd=cay-kho. Tất cả Python chạy với `PYTHONDONTWRITEBYTECODE=1`; Ruff dùng `--no-cache`. Bản trước khi chốt được giữ ở [VERDICT-progress.md](evidence/VERDICT-progress.md).

### Hướng 1 — neo nguồn và tương đương AST

LỆNH: `git -C cay-kho rev-parse HEAD`, `git -C cay-kho rev-parse HEAD^{tree}`, `git -C cay-kho diff --name-status b29da0b HEAD`, `sha256sum SPEC.md cay-kho/ops/specs/BIEN-NHAN-V2-GLOB-HOA-THUONG-r2.md`, `PYTHONDONTWRITEBYTECODE=1 python3 evidence/ast_check.py`.

OUTPUT THẬT: HEAD `356a27e1378b2162bbc0be2ec06ff08fdacbdead`; tree `c1e160cfd5ddf1a053c2e8413e62f5881badd052`; shallow=`false`; status ban đầu rỗng; write set đúng hai tệp. Hai SPEC cùng băm `d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d`. Script rc=0; AST bỏ docstring giống nhau ở CẢ HAI tệp giữa c8a493c và 356a27e; AST SHA256 sản phẩm `8d2f6e76701e725887d7b2520bba32aff956115715de788f8eb8cdb16086efd0`, test `adab78b4e83e8dc1ec2212a2ba66fdeff37d901a41d4eaea2677e6e92a1816c6`. Diff đầu vào khớp byte `git diff` của đúng hai mốc. Bốn docstring đổi: `_hoi_trang_thai`, `_chon_bien_nhan`, c99, c100. Chi tiết: [ast.json](evidence/ast.json).

Kết luận: **KHÔNG PHẢI LỖI** về lời khai chỉ đổi docstring/chú thích. Chưa kết luận tham chiếu trước phép đo đột biến.

### Hướng 2 — các cổng tĩnh và doctrine

LỆNH (cwd=`cay-kho`): `PYTHONDONTWRITEBYTECODE=1 python3 .claude/dev/packet_loop.py doctrine-scan --root .`; `git diff --check b29da0b HEAD`; `rg -n 'glob\("\*\.receipt\.yaml"\)' ops/bien_nhan_v2.py`.

OUTPUT THẬT: `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`, rc=0; diff-check rc=0/output rỗng; rg rc=1/0 dòng. [Log doctrine](evidence/doctrine.log), [rc](evidence/doctrine.rc), [diff-check rc](evidence/diff-check.rc), [rg rc](evidence/rg-glob.rc).

Kết luận: **KHÔNG PHẢI LỖI** trong phạm vi các cổng này. Ruff delta đang đo riêng.

### Hướng 3 — cổng thật, đếm ứng viên độc lập và sinh nợ

LỆNH (cwd=`cay-kho`): `PYTHONDONTWRITEBYTECODE=1 python3 ops/bien_nhan_v2.py --root .`; `PYTHONDONTWRITEBYTECODE=1 python3 ops/bien_nhan_v2.py --root . --sinh-no`; `python3 -c 'import os; print(sum(n.lower().endswith(".receipt.yaml") for n in os.listdir("ops/reviews")))'`.

OUTPUT THẬT:

```text
bien_nhan_v2: 253 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 306
câu lịch sử: nợ L-REVIEW 1 · L-ANCESTRY 60 · L-SURFACE 0 · L-SURFACE chua_do_duoc 0
TỔNG: ĐẠT
rc=0
```

Sinh nợ: rc=0, stderr=`# 42 tệp`. Đếm riêng bằng os.listdir, không lọc is_file: `306`. [Cổng](evidence/gate.log), [rc](evidence/gate.rc), [sinh nợ stdout](evidence/sinh-no.out), [stderr](evidence/sinh-no.err), [rc](evidence/sinh-no.rc).

Kết luận: **KHÔNG PHẢI LỖI**; C6 đạt tại cây SHA đang review.

### Hướng 4 — từng đột biến được docstring viện dẫn và hồi quy merge master

LỆNH: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/probe.py focused` (từng tên m142–m157 gọi RIÊNG `_dot_bien(chi={tên_đầy_đủ})`; sửa nguồn qua `_dot_bien_tep` trên bản sao tạm; wrapper quan sát `_chay_1` và đối chứng).

OUTPUT THẬT: rc=0, `FOCUSED: 16/16 giet_that, controls clean`. m142→c101; m143→c89; m144/m145/m146/m147/m155→c99; m148/m149/m150/m151/m152/m153/m154→c100; m156/m157→c88. Tất cả `dat=true`, `tt=giet_that`, không tự kiểm, đối chứng c18 sạch khi mutant còn hiệu lực. Không có tín dụng giả/giàn giáo. [Output](evidence/focused.log), [chi tiết ngoại lệ đầy đủ và đối chứng](evidence/focused.json), [rc](evidence/focused.rc).

m153 chết với `lỗi lập trình ở is_dir [] bị nuốt/đổi: đòi RuntimeError mốc đi thẳng ra, được không ngoại lệ` tại c100. m154/m155 chết với `OSError: [Errno 5] I/O error` (EIO). m156 chết ở `ix-trich-dan-sau-hai-dong`; m157 chết ở `ii-b-trich-dan-dong-sau`. Các chốt hiện hành đúng thuộc tính trong docstring. Việc số lượt 1/2/3 gắn với commit lịch sử sẽ được đối chiếu thêm bằng nội dung Git, không coi phép đo hôm nay là lần chạy lịch sử.

Kết luận: **KHÔNG PHẢI LỖI** ở các tham chiếu m144–m155 và các ca đích c88/c89/c99/c100/c101 đã đo.

### Hướng 5 — đột biến tự chọn ở mỗi tệp, hoàn nguyên glob và đối chiếu finding lượt 7

LỆNH: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/probe.py extra`.

OUTPUT THẬT: rc=0, `EXTRA: 4/4 giet_that, controls clean`.

- Tự chọn sản phẩm: `return sorted(ds)` → `return sorted(ds, reverse=True)` qua `_dot_bien_tep`: c99 sạch=`qua`, mutant=`giet_that` tại chốt 2 (đòi thứ tự a,m,z, được z,m,a), c18 sạch.
- C3: thay danh sách iterdir/lower/endswith bằng `list(tm.glob("*.receipt.yaml"))` qua `_dot_bien_tep`: c101 sạch=`qua`, mutant=`giet_that` vì tổng=1, c18 sạch. `uname -s` thực đo=`Linux`.
- Finding lượt 7: nới `_hoi_trang_thai` từ bắt `OSError` sang `Exception` qua `_dot_bien_tep`: c100 sạch=`qua`, mutant=`giet_that` ở chốt 7; cùng mutant c99 vẫn `qua`; c18 sạch. Tham chiếu hiện trỏ c100 đúng chốt. **ĐÓNG / ĐÃ VÁ THẬT**.
- Tự chọn tệp test: trên bản sao byte của suite và nguồn phụ, chỉ đổi đối số `dat` thành `True` khi `do()` gọi hàm định dạng. c98 sạch=`qua`; mutant=`giet_that` với `stdout của do() thiếu ngoại lệ/vị trí ... _c74_gia`, c18 sạch. c98 đi qua đúng `_dot_bien(chi={m81_bo_chot_no_chet})` và `_dot_bien_tep` thật trước khi chốt giết mutant; không phải lỗi import hoặc tín dụng giả. Bản sao tạm đã dọn.

[Output](evidence/extra.log), [mẫu cũ/mới nguyên văn và kết quả](evidence/extra.json), [rc](evidence/extra.rc).

Kết luận: **KHÔNG PHẢI LỖI**; các chốt đã đo có răng ở cả sản phẩm và suite; P3 lượt 7 đã đóng.

### Hướng 6 — ba nhánh nghiệm thu selector có răng độc lập

LỆNH: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/probe.py branches`.

OUTPUT THẬT: rc=0, `BRANCHES: 3/3 baseline qua; 3/3 m142 giet_that at selected existing assertion`. Chạy lại ca c101 sẵn có, giữ riêng từng assertion bằng wrapper `bang` chỉ cho nhánh đang đo phát tín hiệu, không tạo fixture mới: C1a mutant tổng=1; chỉ-x mutant không có tổng/"không có tệp"; C1b mutant rc=1 và không nêu x. Mỗi nhánh trên nguồn sạch `qua`, cùng m142 trên bản sao `giet_that`. Cách này tránh cho chốt C1a chết trước rồi nhận tín dụng thay hai nhánh phía sau. [Output](evidence/branches.log), [chi tiết](evidence/branches.json), [rc](evidence/branches.rc).

Kết luận: **KHÔNG PHẢI LỖI** trong ba nhánh đã đo tại đây; chưa đo Windows.

### Hướng 7 — Ruff delta so base

LỆNH: `python3 -m ruff check --no-cache --select F ops/bien_nhan_v2.py ops/bien_nhan_v2_test.py` (cwd=cay-kho); `PYTHONDONTWRITEBYTECODE=1 python3 evidence/ruff_delta.py`.

OUTPUT THẬT ban đầu: `/usr/bin/python3: No module named ruff`, rc=1. Driver JSON không có dữ liệu lint để phân tích và báo `JSONDecodeError`; đó là lỗi thiếu công cụ, không phải chẩn đoán F. [Output lệnh thật](evidence/ruff-head.log), [rc](evidence/ruff-head.rc), [driver](evidence/ruff-delta.log).

Kết luận hiện tại: **KHÔNG ĐO ĐƯỢC**; đang kiểm tra khả năng có bản Ruff cục bộ, không gọi mạng, không suy delta từ lượt trước.

Cập nhật hướng 7: đã tìm thấy Ruff cục bộ, không cần mạng: `PYTHONPATH=/root/.cache/uv/archive-v0/SOspU4Xc3EXqZccW PYTHONDONTWRITEBYTECODE=1 python3 -m ruff --version` → `ruff 0.16.9`, rc=0. Dùng cùng biến môi trường chạy `python3 evidence/ruff_delta.py`: rc=0, `base_count=1, head_count=1, added=[], removed=[]`. Cùng chẩn đoán F541 ở dòng `dung(lam, f"KHÔNG ĐO ĐƯỢC: không có bề mặt nào của provider KHÁC để mượn thử")`. Lệnh Ruff trực tiếp hai tệp ở HEAD rc=1, 1 F541 có sẵn ở base; **delta=0**, không khai lint sạch tuyệt đối. [Bảng so chuẩn hóa path/code/message/nội dung dòng](evidence/ruff-delta.json), [output](evidence/ruff-delta.log), [Ruff HEAD](evidence/ruff-head.log). Các log thiếu module ban đầu giữ tại `evidence/ruff-*-initial.*`.

Kết luận cuối hướng 7: **KHÔNG PHẢI LỖI** theo tiêu chí delta C9.

### Hướng 8 — tham chiếu lịch sử, ca không đích và đối chiếu t27

LỆNH: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/references.py`.

OUTPUT THẬT: rc=0, `REFERENCES: history matches 1/2/3; rename AST equal; 6/6 current cases qua; c101 survives m144/145/146; t27 suffix mutant killed`.

- Đối chiếu node đột biến được thêm qua Git: `5efa311` (lượt 1) thêm m144–m147; `8d9e3e3` (lượt 2) thêm m148–m153; `e9e0048` (lượt 3) thêm m154/m155. Dữ liệu là blob/commit trong lịch sử cục bộ; không coi đây là phép chạy lịch sử.
- Thân AST c98 của `e9e0048` và c101 của HEAD giống nhau khi bỏ docstring và chuẩn hóa đúng tên hàm. Đúng là đổi số c98→c101 qua merge `3883b60`, tránh nhầm với c98 của #1037.
- Trên HEAD: c88/c89/c98/c99/c100/c101 chạy riêng đều `qua`. Trên từng mutant m144/m145/m146, c101 vẫn `qua` và c18 sạch; đối chiếu hướng 4: chính c99 giết cả ba. Tham chiếu "c101 chỉ đi đường kiem" không nhận tín dụng từ chốt sinh nợ/thứ tự/vắng.
- Dùng nguyên ca `t27_phan_chung_verdict_duoi_HOA_thieu_muc_luc_phai_DO_tren_moi_nen` trên bản sao của lease_publish_test.py: sạch qua; chỉ bỏ `.lower()` trong helper được nhắc tới thì assertion `bộ liệt kê không thấy đủ cả hai cách viết đuôi — nó đang phụ thuộc nền` làm ca đỏ. Đây là phép đo tham chiếu ngoài write set, không sửa tệp nguồn đó.

[Output](evidence/references.log), [lịch sử, AST và kết quả](evidence/references.json), [rc](evidence/references.rc). Có SyntaxWarning escape `\d` của tệp lease_publish_test.py đã có sẵn khi import; không ảnh hưởng assertion, không quy thành finding của packet này.

Kết luận: **KHÔNG PHẢI LỖI** ở các tham chiếu lịch sử 1/2/3, c98/c101 và t27 đã đối chiếu.

Bổ sung hướng 6 — output dương trên nguồn sạch (không chỉ suy từ việc mutant chết): C1a `rc=1 tổng=2`; chỉ-x `rc=1 tổng=1`; C1b `rc=2`, stderr `KHÔNG ĐO ĐƯỢC: x.RECEIPT.YAML: YAML hỏng (ParserError: ...)`, không Traceback. Hai điều kiện nêu x và không "không có tệp" cũng được assertion nguyên gốc đo. Đã lưu riêng `baseline_observation` trong [branches.json](evidence/branches.json).

### Hướng 9 — toàn suite trên nguồn HEAD

LỆNH thực chạy từ thư mục PROMPT: `PYTHONDONTWRITEBYTECODE=1 python3 cay-kho/ops/bien_nhan_v2_test.py` (chính tệp `ops/bien_nhan_v2_test.py` của SHA chỉ định, không phải bản sao hay mã do reviewer soạn).

OUTPUT THẬT cuối log, rc=0:

```text
bien_nhan_v2_test: 98/98 ca đạt · 153/153 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 135/153 đột biến thường khai đối chứng
TỔNG: ĐẠT
```

[Toàn log](evidence/suite.log), [rc](evidence/suite.rc). Hai số bằng nhau ở cả ba phân số nghiệm thu. 135/153 là số đột biến khai đối chứng, không phải tỷ lệ đạt; không nâng thành 153/153 có đối chứng. c88/c89/c98/c99/c100/c101 đều ĐẠT trong suite; m156/m157 vẫn giết đúng c88, m142 nhắm đúng c101. Không có thông báo `Codex home is inside a repository`, không có bỏ qua.

Kết luận: **KHÔNG PHẢI LỖI** trong phạm vi suite trên cây hiện tại.

### Hướng 10 — CI, Windows local và kiểm toàn vẹn cuối

LỆNH cục bộ: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/finalize.py`.

OUTPUT THẬT: `FINAL ASSERTIONS PASS`, rc=0; source_hashes_match_initial_and_HEAD=true, head_still_exact=true, status tracked/untracked/ignored rỗng, diff HEAD và diff cached rỗng. Kiểm trực tiếp source bytes khớp blob HEAD, hash khớp lúc đo AST; HEAD/tree giữ nguyên. [Bảng máy](evidence/final-validation.json), [output](evidence/final-validation.log), [rc](evidence/final-validation.rc).

Kết luận tính toàn vẹn: **KHÔNG PHẢI LỖI** ở các mốc đã đo. Snapshot sạch chỉ chứng minh không có delta quan sát được ở các mốc; không dùng để suy toàn bộ lịch sử ghi.

C4/C5/C7: **KHÔNG ĐO ĐƯỢC**. Không gọi mạng theo ràng buộc; không có phép đo độc lập jobs/labels/runner_id/log trên các CI run được executor khai; không có phép đo máy Windows local. Không coi lời khai success hoặc suite tại đây là bằng chứng CI. Không đo được trần lời gọi thực tế và điều kiện checkpoint/ủy quyền qua GitHub; lượt review này thực hiện theo chỉ thị hiện hành “LƯỢT 8”. Kết luận review nội dung không xác nhận đủ điều kiện merge/land.
