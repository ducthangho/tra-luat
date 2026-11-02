verdict: changes_requested
reviewed_sha: 3519c3d07ae8334d4f09560fc0bce52a56b88507
so_lop: P0 0 / P1 0 / P2 1 / P3 0
so_finding: P0 0 / P1 0 / P2 2 / P3 0
reviewed_tree: d6361690ed59009586c4fb6a9255cadbe273c823
base_sha: 44884446f71c89e25f9a72ac58e4f597db63c1ba
packet: land-81-ha-cap / revision 2 / generation 1 / mission 748
review_class: sensitive
provider: openai_codex
execution_surface: codex_cli
transport: machine
run_id: 73dea3445bfe4d30a7693524c38ffa67
independent_from_executor_session: true
review_axes: [spec, standards_security]

Áp ngưỡng 0 finding P0–P3. Có hai biểu hiện của cùng lớp `bo-sot-assurance-81-trong-van-xuoi`: danh sách thay thế chưa phủ hết lời khai §8.1 trong #870 và #889. Các phép đo nguồn runtime, bảo toàn lịch sử, trần diff và delta cổng đều đạt tiêu chí tương ứng; chúng không đóng được lỗi kiểm kê này.

| Lớp | Finding / biểu hiện | Mức cao nhất | Nguồn | Cách đóng lớp |
|---|---|---|---|---|
| `bo-sot-assurance-81-trong-van-xuoi` | F1: #870; F2: #889 | P2 | Lượt 1, exact SHA ở trên | Liệt kê cả hai đường dẫn còn thiếu, quét lại mọi lời khai ở mọi độ sâu, giữ nguyên tiền tố byte của base. |

**F1 — P2 — Bỏ sót lời khai assurance “đạt” trong văn xuôi của #870.**

- **Tệp:dòng:** `ops/land/pr870-claude-md-bai-hoc-c-land-evidence.yaml:324`, khối mới `ha_cap_assurance_81_20261027.thay_the`. Lời khai bị bỏ sót ở `:212–214`, đường dẫn `$.cap_nhat_20261026.landed_ly_do`.
- **Mô tả:** Chuỗi này nói comment cũ đăng “truoc khi reviewer_assurance_81 dat”. Trong ngữ cảnh bản cập nhật đã khai assurance đạt, đây là lời khai gián tiếp về việc §8.1 đã đạt, dù chữ `dat` viết thường và nằm trong câu về thời điểm duyệt landed. Danh sách mới có sáu đường dẫn, không có đường dẫn này; `thay_the_ghi_chu` chỉ thay thế “Moi duong dan tren”. Đặc tả §2.2 và yêu cầu review (a) đòi liệt kê từng đường dẫn, kể cả văn xuôi. Chỉ hạ trường scalar `reviewer_assurance_81` chưa hoàn tất việc kiểm kê ấy.
- **Tái hiện:** Tại thư mục làm việc, chạy `python3 -B review-evidence/check_supersession.py` → **rc=1**. Output riêng #870: `missing=1 declared=6`, in nguyên giá trị của `$.cap_nhat_20261026.landed_ly_do`. Giá trị và vị trí YAML được đọc từ toàn tệp, không suy từ diff.
- **Đề xuất vá:** Thêm đường dẫn còn thiếu vào chính danh sách `thay_the` mới, ghi rõ phần assurance §8.1 của câu được khối cấp gốc thay thế. Giữ nguyên byte câu lịch sử và các thông tin §10.2.2/landed trong đó. Đây là chỗ ghi phạm vi đính chính theo §2.2; không cần sửa biên nhận hay cổng.
- **Ca khóa lỗi:** Kiểm danh sách với toàn bộ lá YAML và văn xuôi, nhận cả `reviewer_assurance_81 dat` viết thường. Phép kiểm phải đỏ nếu xóa riêng mục vừa bổ sung. Đối chứng: `dinh_chinh_sau_quyet_dinh.dieu_kien_mo_lai` có token `cross_approved` nhưng chỉ nêu điều kiện cần, nên không được coi là lời khẳng định đã đạt.
- **Rủi ro khi vá:** Tìm từ khóa thuần túy có thể lẫn lời phủ định/điều kiện với lời khai đã đạt, hoặc làm ghi chú đính chính phủ cả dữ kiện gate trong chuỗi hỗn hợp. Giới hạn việc thay thế vào phần assurance và tiếp tục kiểm bất biến tiền tố byte.

**F2 — P2 — Bỏ sót cùng lời khai văn xuôi trong #889.**

- **Tệp:dòng:** `ops/land/pr889-claude-md-bai-hoc-c-land-evidence.yaml:350`, khối mới `ha_cap_assurance_81_20261027.thay_the`. Lời khai bị bỏ sót ở `:238–240`, đường dẫn `$.cap_nhat_20261026.landed_ly_do`.
- **Mô tả:** Hồ sơ này cũng giữ câu “truoc khi reviewer_assurance_81 dat” nhưng danh sách sáu đường dẫn không liệt kê nơi chứa câu. Vì vậy chưa đáp ứng yêu cầu liệt kê từng lời khai §8.1 đạt của §2.2. Đây là biểu hiện thứ hai của cùng lớp với F1, được ghi finding riêng theo yêu cầu mỗi đường dẫn bỏ sót là một finding.
- **Tái hiện:** Cùng lệnh `python3 -B review-evidence/check_supersession.py` → **rc=1**; output riêng #889: `missing=1 declared=6`, đường dẫn và giá trị ở dòng 238. Kết quả lưu trong `review-evidence/supersession.json`.
- **Đề xuất vá:** Thêm riêng đường dẫn này vào danh sách `thay_the` của #889 và giới hạn ghi chú thay thế vào lời khai assurance. Giữ nguyên toàn bộ dòng cũ và trạng thái landed. Cần sửa cả hai hồ sơ vì chúng là hai hiện vật độc lập; bổ sung mục cho #870 không thay đổi nội dung #889.
- **Ca khóa lỗi:** Chạy cùng phép kiểm phủ trên #889; xóa riêng mục tương ứng phải làm đỏ dù mục #870 vẫn còn. Giữ đối chứng điều kiện mở lại và kiểm tiền tố byte như F1.
- **Rủi ro khi vá:** Ngoài nguy cơ nhận nhầm câu điều kiện như F1, sao chép giữa hai hồ sơ dễ đưa sai đường dẫn/ID. Kiểm mục mới trên YAML của chính #889 và kiểm không thay đổi các khóa cũ.

## Đã đo

Các script và log nằm trong `review-evidence/`, ngoài `cay-kho/`. `measure.py` dùng `PYTHONDONTWRITEBYTECODE=1` và `GIT_OPTIONAL_LOCKS=0` cho tiến trình con. Khi ghi rc của cổng dưới đây, đó là rc thật của tiến trình cổng, được lưu trong JSON; wrapper lưu log có thể kết thúc rc=0 cả khi cổng trả rc=1/2.

**Tiền kiểm và thước đo đóng băng — đạt.**

- Lệnh đầu tiên sau khi đọc giao việc: `git -C cay-kho rev-parse HEAD` → **rc=0**, đúng `3519c3d07ae8334d4f09560fc0bce52a56b88507`.
- `git show -s --format='%H%n%P%n%T%n%s' HEAD` trong `cay-kho/` → **rc=0**; cha trực tiếp là base `44884446f71c89e25f9a72ac58e4f597db63c1ba`, tree là `d6361690ed59009586c4fb6a9255cadbe273c823`. Checkout được giao ở detached HEAD. `git status --short` rỗng, `core.abbrev=7`.
- `sha256sum ops/specs/land-81-ha-cap-r2-pr870-889-896.md` → **rc=0**, `ba96df801af3caebd015b43611fdaaf64b48bf8dc8491c46310742fabd7d7bed`. Đã đọc §1–§5 và đối chiếu hai khối tiền lệ r1 trong `pr924-wp923-land-evidence.yaml`.
- `python3 -B review-evidence/verify_provenance.py` → **rc=0**: blob đặc tả tại `02bdffa34d6475080a55308b3f45b9006be00712` bằng byte đặc tả đang đọc, cùng SHA-256 đóng băng.

**(a) Nội dung §2 và kiểm kê toàn tệp — hai thiếu sót F1/F2.**

Lệnh `python3 -B review-evidence/measure.py audit` → **rc=0**, `STRUCTURE_AND_RUNS_PASS`. Lệnh `python3 -B review-evidence/check_supersession.py` → **rc=1**, `missing_claim_paths=2; P2 findings=2; classes=1`.

| Hồ sơ | `reviewer_assurance_81` cấp gốc | `review_exact_sha` | `thuc_thi` | Số lá YAML quét toàn tệp | Danh sách thay thế |
|---|---|---|---|---|---|
| #870 | CHUA_DAT | DAT | model measured; effort/sandbox_mode not_measured, đủ lý do | 165 | 6 mục; thiếu F1 |
| #889 | CHUA_DAT | DAT | model measured; effort/sandbox_mode not_measured, đủ lý do | 172 | 6 mục; thiếu F2 |
| #896 | CHUA_DAT | CHUA_DAT | model measured; effort/sandbox_mode not_measured, đủ lý do | 283 | 4 mục; không phát hiện đường dẫn thiếu khác |

Đã duyệt mọi scalar ở mọi độ sâu, đọc ngữ cảnh các ứng viên và quét cả dòng thô/comment bằng biểu thức nhận `cross_approved`, `§8.1` và assurance `DAT/dat/ĐẠT/đạt`. Phân loại nghĩa được thực hiện bằng cách đọc câu; script ghi lại thước đối chiếu sau phân loại, không tự coi mọi lần xuất hiện từ khóa là lời khẳng định đã đạt. Các câu `CHUA DAT`, điều kiện mở lại `(A) cross_approved`, và số đo model đơn thuần không bị tính nhầm. Các đường dẫn đã liệt kê đều tồn tại và phần mô tả trỏ đúng chỗ. Bản kê cùng toàn bộ lá/giá trị/dòng ở `audit.json` và `supersession.json`.

`lich_su` của #870/#889 dẫn đúng `$.cap_nhat_20261026.reviewer_assurance_81`; #896 dẫn đúng `$.pr_ghi_so_duyet_landed_20261027.dieu_kien_da_dat`. Cả ba ghi lỗi connector P1 #934/comment 4372912640 và việc hạ thuộc packet r2. Các khối `ha_cap_assurance_81_20261027` ở cuối tệp. Ghi chú landed dùng đúng ID/PR và nói rút landed là quyết định riêng của chủ kho.

#896 ghi rõ approve trên `fb87110`, khác authorized head `816f439`; comment 6431407190 chấp nhận đơn vị land `816f439 + 3bc4244` là căn cứ landed, không được dùng để nâng `review_exact_sha` lên DAT.

**(b) Đối chiếu trực tiếp run.json, verdict và ID — đạt trong phạm vi đo.**

Lệnh `python3 -B review-evidence/measure.py audit` ở trên mở trực tiếp các tệp sau:

- `ops/reviews/pr870-review-3-codex/run/run.json` và `ops/reviews/pr870-review-3-codex-verdict.md`.
- `ops/reviews/pr889-review-3-codex/run/run.json` và `ops/reviews/pr889-review-3-codex-verdict.md`.
- `ops/reviews/pr896-review-8-codex/run/run.json` và `ops/reviews/pr896-review-8-codex-verdict.md`.

| Hồ sơ | `run_id` đầy đủ / 8 hex đầu | `ma_thoat` | `head` thật | `authorized_head_sha` | Trạng thái model / sự kiện |
|---|---|---|---|---|---|
| #870 | `941251157e4b4a35be82d6daefb390b2` / `94125115` | 0 | `06a50c5feea77c2654f31edd26efeed7eeee62f5` | `06a50c5feea77c2654f31edd26efeed7eeee62f5` | DO_DUOC; 21/21 `gpt-6.1-sol` |
| #889 | `4764bd6fee0645728143c3eb4f1a417b` / `4764bd6f` | 0 | `094e8d17ae4dfcf21dca63702c9262267bdc072c` | `094e8d17ae4dfcf21dca63702c9262267bdc072c` | DO_DUOC; 19/19 `gpt-6.1-sol` |
| #896 | `1d140267c72349cc962d449f8959d52e` / `1d140267` | 0 | `fb87110cfab832406984f893e6a4c79fbb932aef` | `816f43988eb3012726120ad00166a989cc2b9af6` | DO_DUOC; 38/38 `gpt-6.1-sol` |

Số response_id phân biệt lần lượt 21/19/38. Mỗi `lenh` có đúng ba khóa `chuong_trinh`, `so_doi_so`, `van_tay`; chương trình `codex`, `so_doi_so=9`. Đã duyệt đệ quy mọi khóa JSON: không có trường effort hay sandbox trong cả ba biên nhận lịch sử. Cả ba verdict tồn tại, bắt đầu bằng `verdict: approve`, có `reviewed_sha` đầy đủ bằng head của chính run và câu `Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.` Hash verdict lưu trong `audit.json`.

Sáu lời khai `measured` mới (hai mỗi hồ sơ) đều có nguồn phân giải được: run.json và, với `review_exact_sha_nguon`, cả verdict đúng lượt. L1 đòi ít nhất một token nguồn có thật, không đòi mọi từ giống tên tệp trong câu đều phân giải; từ `launcher.py` riêng lẻ không phải nguồn duy nhất của câu nào. Đã đọc nội dung nguồn, không dùng việc L1 xanh để suy nội dung đúng.

Đã GET bốn nguồn GitHub bằng công cụ `github_fetch`, tất cả trả thành công (`isError=false`), và lưu JSON ngoài checkout. `python3 -B review-evidence/verify_provenance.py` → **rc=0**, `PROVENANCE_PASS`:

- [Lease/comment 6445221939 trên #748](https://github.com/ducthangho/tra-luat/issues/748#issuecomment-6445221939): khớp lease ID, r2/g1, ngày 27-10-2026, base, spec_commit và spec_hash. Đây là bản chiếu lease, được dùng đối chiếu các ID trong khối mới.
- [Connector P1/comment 4372912640 trên #934](https://github.com/ducthangho/tra-luat/pull/934#discussion_r4372912640): đúng tác giả connector, mức P1 và lớp lỗi thiếu phép đo effort/sandbox dù đã đo model.
- [Comment 6411410063 trên #951](https://github.com/ducthangho/tra-luat/pull/951#issuecomment-6411410063): đúng tác giả `ducthangho`, duyệt #870/#889 và dẫn §8.1 làm căn cứ. Body hiện tại khớp cả hai readback địa phương.
- [Comment 6431407190 trên #956](https://github.com/ducthangho/tra-luat/pull/956#issuecomment-6431407190): đúng tác giả, chấp nhận `816f439 + 3bc4244` kèm caveat; body khớp readback địa phương. Comment này chấp nhận đơn vị land theo hồ sơ, không bổ sung phép đo runtime hay exact-SHA review. Điều kiện assurance liên quan nằm trong hồ sơ được duyệt.

**(c) Bảo toàn byte/YAML/landed — đạt.**

Lệnh `python3 -B review-evidence/measure.py audit` → **rc=0**. Script lấy byte base bằng `git show BASE:<path>`, kiểm `new.startswith(base)`, nạp cả hai bản bằng SafeLoader từ chối khóa trùng ở mọi mapping, rồi so mọi khóa cũ.

| Hồ sơ | Byte base | Byte head | Base là tiền tố nguyên vẹn | Dòng thêm | Khóa trùng | YAML cũ bằng nhau |
|---|---:|---:|---|---:|---:|---|
| #870 | 19.700 | 22.486 | Có | 38 | 0 | Có |
| #889 | 21.931 | 24.717 | Có | 38 | 0 | Có |
| #896 | 34.530 | 37.469 | Có | 38 | 0 | Có |

Mỗi bản nạp chỉ thêm đúng hai khóa gốc `assurance_81`, `ha_cap_assurance_81_20261027`; không có khóa cũ bị thay. Các `landed` ở mọi độ sâu bằng base: 6 trường ở #870, 6 ở #889, 13 ở #896. `landed_20261026.landed` của #870/#889 và `landed_20261027.landed` của #896 đều giữ `true`; các trường landed lịch sử khác giữ `false`.

**(d) Cổng, so base và đo răng — đạt tiêu chí delta.**

`python3 -B review-evidence/measure.py prepare-base` → **rc=0**: sao chép độc lập cây và `.git` sang `review-evidence/base/`, rồi chạy `git -c core.hooksPath=/dev/null -C review-evidence/base checkout --detach 44884446f71c89e25f9a72ac58e4f597db63c1ba`. Hook bị tắt chỉ trên lệnh checkout bản sao để tránh tác dụng phụ; không đổi cấu hình hoặc quyền của checkout được review. Đã xác minh HEAD bản sao bằng base.

Mỗi cổng được gọi qua `python3 -B review-evidence/measure.py gate <head|base> <land|receipt|doctrine>`. Wrapper chạy đúng lệnh trong bảng với cwd của cây tương ứng, giữ riêng stdout/stderr và rc.

| Lệnh trong cây tương ứng | Cây | rc cổng | Dòng tổng / bằng chứng dương |
|---|---|---:|---|
| `python3 ops/land_evidence_nguon.py --root .` | head thật | 0 | `land_evidence_nguon: 53 ĐẠT · 25/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 78`; `TỔNG: ĐẠT` |
| `python3 ops/bien_nhan_v2.py --root .` | base | 2 | `bien_nhan_v2: 244 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 513 KHÔNG ĐO ĐƯỢC · tổng 297`; `TỔNG: KHÔNG ĐO ĐƯỢC` |
| `python3 ops/bien_nhan_v2.py --root .` | head thật | 2 | Cùng dòng tổng với base: 0 vi phạm, 513 KHÔNG ĐO ĐƯỢC; `TỔNG: KHÔNG ĐO ĐƯỢC` |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | base | 0 | `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine` |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | head thật | 0 | `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine` |

`bien_nhan_v2` không được gọi là pass tuyệt đối: clone thiếu nhiều object lịch sử. Cả stdout lẫn stderr của head và base bằng byte, nên delta vi phạm = 0, delta KHÔNG ĐO ĐƯỢC = 0, không đổi tập lỗi. Tổng câu lịch sử cùng là `nợ L-REVIEW 1 · L-ANCESTRY 6 · L-SURFACE 3 · L-SURFACE chua_do_duoc 0`. Hai luồng output doctrine-scan cũng bằng byte. Log/rc: `review-evidence/{head,base}-{receipt,doctrine}.{json,stdout.txt,stderr.txt}`; cổng nguồn thật: `head-land.*`.

Đo răng: `python3 -B review-evidence/measure.py mutate` → **rc=0** tạo bản sao khác `review-evidence/mutation/`, thay đúng một token nguồn ở `$.assurance_81.thuc_thi.model` của #870: `ops/reviews/pr870-review-3-codex/run/run.json` thành `ops/reviews/review-source-does-not-exist/run.json`. Đã kiểm đường dẫn mới không tồn tại. Đây là một đường dẫn nguồn thiếu bình thường trong cây tạm.

`python3 -B review-evidence/measure.py gate mutation land` chạy `python3 ops/land_evidence_nguon.py --root .` trên bản sao → **rc cổng=1**:

```text
ĐỎ ops/land/pr870-claude-md-bai-hoc-c-land-evidence.yaml: 1 vi phạm
  L1 $.assurance_81.thuc_thi.model: lời khai đo không có token nguồn phân giải được
land_evidence_nguon: 52 ĐẠT · 25/28 miễn trừ (băm khớp) · 1 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 78
TỔNG: ĐỎ
```

Chi tiết token và thông báo đầy đủ ở `mutation-setup.json`, `mutation-land.stdout.txt`, `mutation-land.json`. Đột biến bị cổng bắt đúng lời khai mới, không phải lỗi setup.

**(e) Trần và phạm vi cấm — đạt.**

`git diff --stat BASE HEAD`, `git diff --numstat BASE HEAD` và `git diff --check BASE HEAD` trong `cay-kho/` → **rc=0**. Diff đúng ba tệp được phép, mỗi tệp +38/-0, tổng **+114/-0**, dưới trần 3 tệp/180 dòng thêm. Không có thay đổi ở `ops/land_evidence_nguon.py`, test hoặc `ops/reviews/`. Bất biến byte/YAML ở (c) chứng minh không rút landed hoặc sửa trường cũ.

**Bảo toàn checkout và giới hạn phép đo.**

`python3 -B review-evidence/measure.py snapshot before` và `python3 -B review-evidence/measure.py snapshot after` → **rc=0**. Hai snapshot bằng nhau: HEAD/tree đúng mốc ở đầu verdict; status tracked/untracked/ignored rỗng; diff/index không đổi; **7.358** tệp không đổi. Có 7.353 tệp được băm byte, 5 tên thuộc nhóm nhạy cảm chỉ so metadata, không đọc nội dung. Snapshot kiểm cả tệp ignored; danh sách và hash index lưu trong `snapshot-before.json`/`snapshot-after.json`. Kết quả: `changed_paths=[] whole_snapshot_equal=True`. Phép so hai mốc không chứng minh toàn lịch sử chưa từng có ghi rồi hoàn nguyên.

Định danh provider/surface/transport/run ở đầu verdict đối chiếu với `run/73dea344/run.json`. Biên nhận lượt hiện tại còn `dang_chay` tại thời điểm đọc, chưa có trường model/effort/sandbox đã chốt; không tự suy các giá trị ấy từ tên model trong ba biên nhận lịch sử. Cấu hình quyền công cụ của phiên là `workspace-write`, còn checkout được đối xử read-only và có snapshot không đổi. Launcher trong base có mã ghi `effort_phuc_vu` và `sandbox_trang_thai`; việc chốt biên nhận launcher sau khi tiến trình reviewer kết thúc nằm ngoài phép đo nội dung ba hồ sơ này. Không gọi phần runtime chưa chốt là đã đo đạt.
