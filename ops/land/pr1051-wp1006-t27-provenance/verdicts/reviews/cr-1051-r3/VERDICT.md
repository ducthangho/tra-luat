verdict: changes_requested
reviewed_sha: cceb0b356136bf445d07ea2bb653cc1fa97f7e8a
so_lop: P0 0 / P1 0 / P2 1 / P3 0

Review độc lập PR #1051, lượt 3. P2 lượt 2 về lời chữa cho tên có khoảng trắng **đã đóng ở đường đổi tên**. Còn một lớp sai danh tính ở đường đọc mục lục/cảnh báo: ô ghi tên khác vẫn thoả cho tên trên đĩa. Đây là phần còn sót trong phạm vi được giao kiểm, đã có ở base; không gọi là hồi quy mới của lượt 3.

Base: `b29da0bfe3bfb7a7be69136a1c5c40f82c088a93`. Head tree: `eecc1dcf780b42268501f774ca613772ffd77791`. Diff toàn PR và diff từ `82a5ef5` đều chỉ có `ops/lease_publish_test.py`.

## Finding F1 — P2 — `wp1006-case-insensitive-listing-case-sensitive-consumer` (danh tính token mục lục)

**Tệp:dòng:** `ops/lease_publish_test.py:1668`–`:1670`, tích hợp với bước bỏ backtick ở `:1605`, consumer ở `:1803` và `:1860`; ca khoá mới ở `:2033` chỉ gọi bộ trích trực tiếp.

**Mô tả.** Chốt đọc nguyên code span có tác dụng khi gọi riêng `_ten_tep`, nhưng không giữ được qua đường đọc bảng thật. `_bang` chạy `` .strip("`") `` trên ô trước khi giao cho `_ten_tep`. Vì vậy ô chỉ ghi `` `two x-verdict.receipt.yaml` `` trở thành `two x-verdict.receipt.yaml`; bộ trích lấy `x-verdict.receipt.yaml`. Tệp trên đĩa mang tên hợp lệ này nên qua `_doi_ten_hop_le`; t27 xanh dù hàng chỉ nêu một tên khác. Cùng đường đó, ô cảnh báo `` `two x-verdict.md` `` thoả cho caveat của `x-verdict.md`.

Nhánh ngoài span còn thiếu biên **sau** token: `x-verdict.receipt.yaml.bak` hoặc `x-verdict.receipt.yaml/child` cũng bị trích thành `x-verdict.receipt.yaml`. Tương tự với tên verdict trong bảng cảnh báo. Đây đều là nhận nhầm danh tính, cùng một finding; không đếm riêng mỗi cách viết.

**Tái hiện đã chạy.** `PYTHONDONTWRITEBYTECODE=1 python3 review_extra.py`, driver rc=0. Script dựng kho Git fixture đầy đủ riêng cho head và base, receipt v2 đủ trường, băm đúng và mỏ neo Git thật. Mã suite được chép nguyên byte từ từng revision; CLI v2 dùng nguyên mã head, không mock Git hay sửa validator. URL/identity trong fixture là dữ liệu thử, không phải chứng cứ reviewer bên ngoài.

Tệp thật: `x-verdict.md` và `x-verdict.receipt.yaml`. Receipt có caveat `C1`; ngoài ô đang thử, mọi hàng đều đúng. Kết quả dưới đây giống nhau ở **head và base**:

| Ô thay thế | t26 CLI | t27 CLI thực đo | v2 CLI | Kết quả đúng cần có ở t27 |
|---|---:|---:|---:|---|
| Tên đúng trong cả hai bảng | 0 | 0 | 0 | Xanh |
| Biên nhận: `` `two x-verdict.receipt.yaml` `` | 0 | **0** | 0 | Đỏ vì thiếu đúng tên biên nhận |
| Biên nhận: `x-verdict.receipt.yaml.bak` | 0 | **0** | 0 | Đỏ vì thiếu đúng tên biên nhận |
| Biên nhận: `x-verdict.receipt.yaml/child` | 0 | **0** | 0 | Đỏ vì khác đường/tên |
| Verdict trong bảng cảnh báo: `` `two x-verdict.md` `` | 0 | **0** | 0 | Đỏ vì caveat không ở hàng đúng verdict |
| Verdict trong bảng cảnh báo: `x-verdict.md.bak` hoặc `x-verdict.md/child` | 0 | **0** | 0 | Đỏ vì khác danh tính |
| Biên nhận: `other.receipt.yaml` | 0 | **1** | 0 | Đỏ, đối chứng âm đạt |
| Verdict trong bảng cảnh báo: `other-verdict.md` | 0 | **1** | 0 | Đỏ, đối chứng âm đạt |

v2 xác nhận **1/1 receipt đạt**, không có trạng thái chưa đo, trong từng ca của bảng này. Bộ đọc v2 đọc đúng tệp thật; lỗi nằm ở việc t27 dùng tên khác trong mục lục để thoả cho tệp ấy. Không diễn giải đây là bypass schema v2.

Chênh lệch pipeline đo trực tiếp:

```text
_ten_tep("`two x-verdict.receipt.yaml`")             == set()
_bang(...)[0]["biên nhận"]                          == "two x-verdict.receipt.yaml"
_ten_tep(_bang(...)[0]["biên nhận"])                 == {"x-verdict.receipt.yaml"}
CLI t27                                            == rc 0, 1/1 đạt
```

Bằng chứng: [script phản chứng](review_extra.py), [kết quả từng revision](review-evidence/repro-results.json), [README tái hiện](review-evidence/repro-head-wrong-receipt-span.md), [log t27](review-evidence/repro-head-wrong-receipt-span-t27.stdout), [log v2](review-evidence/repro-head-wrong-receipt-span-v2.stdout). Các ca link, dấu phẩy, ngoặc, token sai tiền tố và đường con được đo thêm tại [row-results.json](review-evidence/row-results.json).

**Đề xuất.** Giữ nguyên ranh giới code span của ô dữ liệu khi đi qua `_bang`, rồi mới trích tên; chuẩn hoá header và id cảnh báo riêng ở consumer tương ứng. Bổ sung biên kết thúc token cho nhánh ngoài span để không lấy tiền tố của `.yaml.bak` hoặc `.yaml/child`. So nguyên tên, giữ hoa/thường và dấu Unicode của tiền tố.

**Ca khoá.** Dùng fixture đủ băm/URL; đưa các ô sai trong bảng trên qua **CLI t27 hoặc `_kiem_muc_luc`**, với đối chứng tên đúng xanh và tên khác đỏ. Làm cho mutant bỏ giữ span ở parser bảng và mutant bỏ biên sau token đều bị bắt. Chỉ assert `_ten_tep` trực tiếp như dòng 2033 không khoá được tích hợp này.

**Rủi ro khi vá.** `_bang` cũng cung cấp header và ô `id`: giữ backtick toàn cục mà không điều chỉnh hai chỗ đó có thể báo thiếu cột/caveat đang đúng. Phải giữ các hàng thật, link Markdown, tên sau dấu phẩy/ngoặc và quy tắc bỏ comment/rào mã; không dùng lowercase toàn tên hoặc substring để chữa.

## Đối chiếu lượt 2 và biên tên

[review_probes.py](review_probes.py) lặp receipt v2 hợp lệ với **cùng byte YAML** qua ba tên; hàng mục lục luôn cập nhật đúng tên. [rename-results.json](review-evidence/rename-results.json):

| Tên receipt alias | t26 | t27 | v2 CLI | Bộ đọc packet |
|---|---:|---:|---|---|
| `two words.RECEIPT.YAML` | 1 | 1 | rc=0, chỉ đếm 1 receipt nền | Chỉ thấy nền |
| `two words.receipt.yaml` | 1 | 1 | rc=0, **2/2 đạt v2** | Thấy cả alias |
| `two-words.receipt.yaml` | **0** | **0** | rc=0, **2/2 đạt v2** | Thấy cả alias |

Thông báo đầu nêu **cả** lỗi đuôi và tên trong cùng một lỗi; chỉ đổi đuôi còn đỏ đúng chốt tên. Đổi cả tiền tố và đuôi theo lời chữa làm **cả t26/t27 xanh**, v2 đọc cùng byte receipt. Biểu hiện P2 lượt 2 đã vá thật; không giữ nó làm finding.

Các phép đo biên khác: [boundary-results.json](review-evidence/boundary-results.json), [verdict-boundaries.json](review-evidence/verdict-boundaries.json), [suffixes.json](review-evidence/suffixes.json).

- Duyệt đủ **2.048** biến thể hoa/thường ASCII của `.receipt.yaml`: chốt chỉ nhận đúng đuôi thường. Không thấy đường tên HOA được t26/t27 nhận mà v2/packet bỏ qua.
- `-dash`, `.hidden`, `..dots`, Unicode NFC tiếng Việt, CJK và `İıſK` với đuôi thường đều qua chốt, t26/t27 và v2; reader packet nhận đúng nguyên tên. Đo thêm verdict + sidecar tương ứng cho tên bắt đầu `-`/`.`, CJK và `-VERDICT.MD`: t26/t27/v2 CLI đều rc=0, v2 đếm đủ 7/7.
- Hai danh tính `e-verdict.md` và `é-verdict.md` cùng tồn tại và qua cả ba CLI; bỏ riêng hàng của tên có dấu làm t27 đỏ. Không gộp tên chỉ khác dấu.
- Unicode NFD chứa combining mark, khoảng trắng, `+`, `;`, `:` bị chốt tên từ chối rõ ràng; v2/packet vẫn đọc được nếu đuôi thường. Đây là tập nhận **hẹp hơn có chủ ý** của chính sách đổi tên mới, không phải tệp được cổng tên nhận rồi vô hình ở reader. Không normalize/gộp âm thầm hai tên.
- `.receipt.yml` không thuộc tập liệt kê của cả t26/t27/v2/packet/c38/c42; alias đuôi đó bị tất cả bỏ qua. Gọi riêng chốt tên với nó thì bị từ chối đuôi. Không gọi rc=0 của reader là đã validate alias `.yml`.
- Token `nested/x-verdict.receipt.yaml` không được nhận thay basename: CLI t27 rc=1. Trường hợp đường có hậu tố `/child` lại bị cắt tiền tố, đã đưa vào F1; `/` không phải ký tự hợp lệ trong basename trên POSIX.
- Đã chạy **hàm c38 và c42 thật** với tập receipt biên nói trên trong thư mục thử: cả hai hoàn tất không lỗi; các glob của chúng chỉ thấy đuôi `.receipt.yaml` thường. [c38-c42-results.json](review-evidence/c38-c42-results.json). Không khai đã chạy toàn suite v2.

Trên `ops/reviews/README.md` thật, so tập token head/base của **mọi ô tên** ở cả hai bảng cho delta **0**: parser trả 750 hàng bảng cảnh báo; 321 hàng dưới mục lục, trong đó 306 hàng có cột tên verdict/receipt (612 ô tên). Trên đĩa có 306 receipt và 284 verdict thuộc tập liệt kê. [real-tables.json](review-evidence/real-tables.json). Các ca đúng tên trong code span, link Markdown, sau dấu phẩy và trong ngoặc đều CLI t27 rc=0. Kết quả này chứng minh không làm hỏng các hàng đã đo; không phủ định F1 trên ô sai tên.

## Răng của ca mới

Chạy mỗi mutant riêng, chỉ sửa một chốt trong bản sao tạm ngoài nguồn, chọn đúng ca mới qua `main` thật. [review_mutations.py](review_mutations.py), [mutation-results.json](review-evidence/mutation-results.json), [trace control](review-evidence/trace-control.json).

| Mutant | rc | Điểm bị bắt |
|---|---:|---|
| Control nguyên byte | **0**, 1/1 | Chạy hết ca; 7 lần helper t26, 9 lần helper t27 |
| Bỏ chốt đuôi | **1** | Bước 1, helper t26 nhận alias HOA |
| Bỏ chốt tên | **1** | Bước 2, thông báo tên vừa có khoảng trắng vừa HOA thiếu lỗi tiền tố |
| Bỏ lời gọi chốt receipt ở t27 | **1** | Bước 1, helper t27 nhận alias HOA |
| Bỏ lời gọi chốt verdict ở t27 | **1** | Bước 3, lỗi mục lục thay vì lỗi tên verdict |
| Bỏ lời gọi chốt ở helper t26 | **1** | Bước 1, helper t26 nhận alias HOA |
| Sidecar không phân biệt hoa/thường | **1** | Bước 5, nhận nhầm `c-verdict.receipt.yaml` cho `c-VERDICT.md` |
| Bỏ IGNORECASE ngoài span | **1** | Assert hàng tên trần HOA, dòng 2036 |
| Bỏ biên trước token | **1** | Assert `plus+name...`, dòng 2033 |
| Bỏ đọc nguyên span | **1** | Assert span chứa khoảng trắng, dòng 2033 |

Không có mutant sống trong chín chốt được yêu cầu. Tuy nhiên, hai assert parser cuối chỉ chứng minh helper trực tiếp; F1 cho thấy code span đã mất ở upstream của ô thật. Đo bổ sung bỏ delegation ở **entry point** t26 còn xanh qua riêng ca mới (rc=0, 1/1), vì ca gọi helper trực tiếp. Đây là giới hạn coverage wiring, không tính thành finding hành vi độc lập của head.

## Đã đo

Các lệnh con có argv/cwd/rc/thời lượng và stdout/stderr riêng trong `review-evidence/`; wrapper tại [review_runner.py](review_runner.py). Mọi suite, fixture và mutant nằm ngoài `cay-kho/`, với `PYTHONDONTWRITEBYTECODE=1`, `GIT_OPTIONAL_LOCKS=0`; Ruff không ghi cache.

| Lệnh / phạm vi | rc | Kết quả |
|---|---:|---|
| `python3 ops/lease_publish_test.py`, bản sao head | **1** | **267/269**, chạy 269, bỏ qua 0; **565.686 s** |
| Cùng lệnh, bản sao base | **1** | **266/268**, chạy 268, bỏ qua 0; **566.615 s** |
| `ruff check --no-cache --select F --output-format json ops/lease_publish_test.py`, head/base | 1/1 | Delta chuẩn hoá **0** |
| `PYTHONDONTWRITEBYTECODE=1 python3 review_probes.py` | 0 | Đổi tên hai chiều, cả hai bảng thật, biên tên, reader packet, c38/c42 và Ruff |
| `PYTHONDONTWRITEBYTECODE=1 python3 review_extra.py` | 0 | Phản chứng F1 qua CLI ở cả head/base; 2.048 suffix; verdict/sidecar và cặp khác dấu |
| `PYTHONDONTWRITEBYTECODE=1 python3 review_mutations.py` | 0 | Control rc=0; cả chín mutant bắt buộc rc=1; mutant wiring bổ sung rc=0 |
| `git diff --check b29da0b HEAD` | 0 | Không lỗi whitespace |
| `git status --porcelain=v1 --untracked-files=all`, nguồn | 0 | Output rỗng |

Hai suite giữ trạng thái **failed**, không gọi là pass toàn bộ. Hai ca đỏ giống hệt nhau là `t137_M9_workflow_admission_hop_dong_tinh_va_actionlint_shellcheck` và `t159_t137_can_do_DU_ket_qua_va_dung_nhan_than_timeout`, đều vì thiếu ShellCheck. Phần phép đo ShellCheck là **not_measured** do môi trường. Delta: thêm đúng một ca mới đạt, không đổi kết quả ca chung, không thêm ca thất bại/bỏ qua. Đã tách log A/B lồng trong t125 khỏi 269/268 cặp vào/ra cấp ngoài; mã suite ở hai bản sao sau chạy còn nguyên byte đúng revision. [full-comparison.json](review-evidence/full-comparison.json), [head stdout](review-evidence/full-head.stdout), [base stdout](review-evidence/full-base.stdout).

Ruff: mỗi revision có **7 F401 + 2 F541**, rc=1; so code/message đã loại vị trí dịch dòng cho **delta 0**. [ruff-comparison.json](review-evidence/ruff-comparison.json).

CLI v2 trên bản sao cây thật trả **rc=2**, `not_measured`: kho được cấp thực tế có `--is-shallow-repository=true`, trái mô tả đủ lịch sử trong prompt. Không gỡ marker shallow hay sửa object store để làm xanh. Các chứng cứ v2 dương/âm ở trên dùng Git fixture đầy đủ riêng, không thay cho chứng nhận toàn kho thật đạt v2. [history.stdout](review-evidence/history.stdout), [v2-real-head.stderr](review-evidence/v2-real-head.stderr).

## Tính toàn vẹn và giới hạn

Snapshot đầu/cuối gồm **8.502 entry tệp/symlink**, bao gồm nội dung các tệp trong `.git`; so đường dẫn, loại, mode tệp, băm nội dung và đích symlink cho **delta 0**. Đây là không có thay đổi quan sát được trong phạm vi snapshot, không phải chứng nhận cưỡng chế read-only của OS hoặc chưa từng ghi rồi hoàn nguyên. [source-before.json](review-evidence/source-before.json), [source-after.json](review-evidence/source-after.json), [source-delta.json](review-evidence/source-delta.json).

Môi trường Linux, Python 3.13.17, PyYAML 6.0.3, Ruff 0.16.9; có actionlint, thiếu ShellCheck. Windows thật và CI GitHub: `not_measured`. Công cụ `environment_status` không có trong tập tool của phiên; không thực hiện tác vụ mạng.

Reviewer: Codex, phiên API độc lập; provider `openai_codex`, execution surface `codex_service`, transport `machine` theo môi trường công cụ và ánh xạ của kho. Model ID/effort thực phục vụ không có runtime attestation trong bằng chứng này: `KHONG_DO_DUOC`. Không push, không gọi API ghi GitHub; verdict này không tự tạo approval/state hoặc quyền land.
