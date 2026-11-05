verdict: changes_requested
reviewed_sha: 4f9774aecfb14340fcbe59e89d5781d9603457b7
so_lop: P0 0 / P1 0 / P2 1 / P3 0

Review độc lập PR #1051, lượt 1. **Hai biểu hiện gốc trong t27 đã được vá thật**, nhưng còn một consumer cùng lớp: receipt HOA được t26/t27 chấp nhận ở head lại bị cổng lược đồ v2 bỏ qua trên Linux. Có phản chứng chạy thật với cùng byte YAML, chỉ đổi hoa/thường của đuôi và tên tương ứng trong README. Một lớp, một finding F1; các điểm liệt kê bên dưới không được đếm thành nhiều finding.

## Phạm vi và mỏ neo

- HEAD đầu và cuối: `4f9774aecfb14340fcbe59e89d5781d9603457b7`.
- Parent trực tiếp/base: `b29da0bfe3bfb7a7be69136a1c5c40f82c088a93`.
- Tree head: `06f0a8d75f13f4a800b99189c3807505519f68ea`.
- Diff đúng một tệp: `ops/lease_publish_test.py`, 90 dòng thêm / 4 dòng bỏ.
- `tham-chieu/wp1006.md` có SHA-256 `6c21bd26b64aa5a57925875789a8d9f9f3132a00ae53416b1ac4d0ad703e3eef`, khớp chỉ thị.
- Review Class: `sensitive` do phạm vi `ops/**`. Áp ngưỡng riêng của chỉ thị lượt này: approve chỉ khi không còn finding P0–P3.

Chỉ thị trong [prompt.snapshot](run/b9caf4b4/prompt.snapshot) cấp quyền review; đặc tả wp1006 được đọc như nguồn yêu cầu lịch sử, không dùng lease cũ làm quyền ghi. Checkout `cay-kho/` được đối xử chỉ đọc. Mọi clone, fixture, mutant và output nằm ngoài checkout đó.

## Finding F1 — P2 — `wp1006-case-insensitive-listing-case-sensitive-consumer`

**Vị trí:** `ops/lease_publish_test.py:1663` mở acceptance của tên receipt HOA; consumer chưa đồng bộ ở `ops/bien_nhan_v2.py:1442`. Các đường cùng cơ chế: `ops/bien_nhan_v2_test.py:1705`, `:1908`; `ops/bien_nhan_v2.py:1601`; `.claude/dev/packet_loop.py:2121`.

**Mô tả và tác động.** Sau bản vá, một alias `review-alias.RECEIPT.YAML` có `verdict_path`, băm và URL đúng được t26/t27 chấp nhận. Cổng v2 vẫn dùng `sorted(tm.glob("*.receipt.yaml"))`, nên trên Linux nó không đọc alias này. Biên nhận thiếu identity, receipt ID, anchor và thậm chí khai `schema_version: 999` vẫn đi qua cả ba phép kiểm. Với cùng byte và đuôi thường, cổng v2 trả rc=1 và nêu đúng các lỗi đó. Ở base, tên HOA vẫn bị t27 chặn; head vừa mở đường vượt qua chốt cuối đang thấy nó. Vì thế đây là hệ quả quan sát được của acceptance mới, dù các glob bỏ sót đã có sẵn.

**Tái hiện đã chạy** bằng [review_schema_probe.py](review_schema_probe.py), rc=0 của harness xác nhận từng kết quả dưới đây, không có nghĩa receipt lỗi đã được validate:

1. Clone head riêng tại `review-evidence/schema-case`, giữ đủ refs và `core.abbrev=7`. Cổng v2 ban đầu đạt: **253 v2 + 11 legacy + 42 nợ = 306**, không vi phạm, không KHÔNG ĐO ĐƯỢC.
2. Thêm `review-alias.receipt.yaml` trỏ `ops/reviews/wp929-g1-codex-luot1-VERDICT.md`, SHA-256 tính từ byte verdict, `evidence_url: https://example.test/review`, và `schema_version: 999`. Thêm tên vào đúng cột `biên nhận` của bảng Mục lục. URL này là dữ liệu fixture để đáp ứng chốt https của t26, không được khai là chứng cứ thật.
3. Chạy CLI t26, t27 và validator; đổi tên alias sang `.RECEIPT.YAML`, thay đúng tên trong README, chạy lại cùng ba CLI. Không đổi byte alias.

| Cùng một biên nhận lỗi | t26 CLI | t27 CLI | `python3 ops/bien_nhan_v2.py --root .` |
|---|---|---|---|
| `review-alias.receipt.yaml` | rc=0, 1/1 | rc=0, 3/3 | **rc=1**, `schema_version=999, đòi 2`, cùng các trường v2 bị thiếu |
| `review-alias.RECEIPT.YAML` | rc=0, 1/1 | rc=0, 3/3 | **rc=0, TỔNG: ĐẠT**, vẫn tổng **306**, không đếm alias thứ 307 |
| Cùng cây HOA, dùng checker t27 base | — | **rc=1, 0/1**, báo tên alias thiếu ở cột `biên nhận` dù có hàng | — |

Các argv, rc và output nằm trong [schema-results.json](review-evidence/schema-results.json); bản ghi tổng thể của harness ở [schema-probe.json](review-evidence/schema-probe.json), transcript rc ở [schema-probe.stdout](review-evidence/schema-probe.stdout). JSON chi tiết được dựng lại từ các log CLI bền và transcript rc sau khi phát hiện tên JSON tổng hợp trùng với tên output của wrapper; không suy rc từ riêng màu thông báo.

**Các biểu hiện bổ sung đã đo.** [review_other_readers.py](review_other_readers.py), rc=0:

- `c38` và `c42` thật đều đạt trên cây có alias HOA, nhưng trace `Path.glob` xác nhận mỗi ca chỉ lấy 306 receipt thường, không đọc alias trên đĩa. Không coi hai ca xanh này là bằng chứng bao phủ tập tên vừa được mở rộng.
- `_doc_bien_nhan` của packet loop đọc 1 receipt đuôi thường, rồi 0 sau khi chỉ đổi sang đuôi HOA; byte giữ nguyên. Đây là phép đo helper đọc, không phải phép chứng minh đã vượt review budget hay thay đổi state điều phối.
- CLI `--sinh-no` ghi 1 mục với đuôi thường; đuôi HOA trả rc=0, danh sách rỗng, `# 0 tệp`.

Chi tiết tại [other-reader-results.json](review-evidence/other-reader-results.json). Không tính các biểu hiện này thành finding riêng.

**Đề xuất — vá ở đâu và thế nào.** Đồng bộ bộ liệt kê ở validator v2, hai ca quét receipt thật, đường sinh nợ và reader packet loop với namespace đã được t26/t27 chấp nhận: con trực tiếp là tệp, so riêng suffix không phân biệt hoa thường, giữ nguyên tên và danh tính. Có thể đưa helper vào module dùng chung phù hợp; tránh để mã sản phẩm import module test. Giữ chốt sidecar mơ hồ và so đường dẫn đầy đủ của t27. Việc mở write set cần đi theo authority của packet; reviewer không sửa cây executor.

**Ca khóa.** Cùng fixture đầy đủ: receipt v2 hợp lệ đuôi thường/HOA phải được validator đếm và nhận; bỏ trường v2 hoặc khai schema sai phải đỏ ở cả hai tên. Kiểm c38/c42 thực sự nhận tập tệp HOA, sinh nợ không bỏ sót, reader packet loop đọc cùng tập. Đột biến từng reader quay về glob phân biệt hoa thường phải chết ở đúng phép đo đó; tổng suite xanh không thay các đối chứng này.

**Rủi ro của cách vá.** Không lowercase/casefold toàn tên rồi gộp entry hoặc dùng khóa đã đổi case để khớp allowlist/nợ lịch sử. Trên POSIX, tên khác case là hai danh tính; helper mới phải giữ cả hai, còn sidecar có nhiều ứng viên phải tiếp tục đỏ mơ hồ. Không đổi byte verdict lịch sử hay tự thêm receipt HOA lỗi vào baseline nợ để làm xanh.

## Đối chiếu finding gốc và từng đường xử lý tên

Nguồn: F1 P2 của [kiểm toán sau merge #1007](tham-chieu/kiem-toan-1007-VERDICT.md), SHA `76b65936e9e83ad2711e20a158e552449b4c6d86`. Hai biểu hiện được nêu đích danh đã vá thật. Ở cấp lớp liên consumer, phân loại **VÁ SINH LỖI MỚI**: mở acceptance tại t27 làm lộ đường qua cổng v2 ở F1; không tuyên bố glob v2 vừa được sửa thành sai trong PR này.

Phạm vi quét: tệp test đang hoạt động được lấy từ `git ls-files`, dò chuỗi `ops/reviews`, `receipt.yaml` và phép dựng đường dẫn `reviews`, rồi đọc call site và các reader được chúng gọi. Không tính các bản chụp code/log lịch sử dưới `ops/reviews/`, `ops/land/`, `ops/evidence/`, `rasoat/` thành các test đang chạy. Danh sách tệp và phép gọi tĩnh tại [static-inventory.json](review-evidence/static-inventory.json). Phép dò tĩnh là bản đồ để đọc và dựng phản chứng, không tự chứng minh hành vi của call site.

| Đường / vị trí ở head | Kết luận riêng và bằng chứng |
|---|---|
| `_doi_thu_muc_reviews`, `lease_publish_test.py:1548` | Dựng cứng tên thư mục `reviews`, đúng vị trí quy định; không phân loại đuôi hay gộp tên receipt. |
| `_bang:1607`, `_cot_duy_nhat:1629` | `lower()` chỉ chuẩn hóa tiêu đề cột. Không đổi tên tệp trong ô. |
| `_liet_ke_theo_duoi:1646–1648` | `lower()` dùng làm predicate suffix; trả Path gốc, sắp bằng tên nguyên. Hai verdict `Case-VERDICT.MD`/`case-VERDICT.MD` cùng tồn tại và cùng được giữ. Không có casefold/dedup tên. |
| `_ten_tep:1663`; `co_o_cot:1773` | Nhận `.MD`, `.YML`, `.RECEIPT.YAML` và mixed case; token giữ nguyên. Alias HOA đủ hàng xanh ở head, cùng input đỏ ở base; bỏ hàng đỏ đúng tên/cột. Hai token chỉ khác case vẫn là hai token. |
| `_bien_nhan_cua:1749`; caller `:1787–1794` | So prefix bằng stem nguyên, chỉ hạ case suffix. Sidecar mixed case được tìm; đổi riêng case stem bị từ chối. Ba mutant xác nhận từng chốt còn răng. |
| Verdict trong mục lục `:1783` và receipt trong mục lục `:1808` | So danh tính nguyên qua helper chung, không hardcode suffix ở consumer. Có đối chứng đầy đủ/thiếu hàng receipt HOA. |
| `verdict_path`, `:1800–1805` | So đường dẫn đầy đủ bằng `PurePosixPath`, không chỉ basename và không đổi case. Đổi sang `ops/reviews/archive/Case-VERDICT.MD` bị bắt. |
| `ten_verdict = Path(...).name`, `:1812–1815` | Lấy basename không đổi case, không kiểm đuôi bằng regex riêng. Tên `.MD` từ receipt mixed case đi qua đúng cột; kiểm đường dẫn đầy đủ vẫn ở nhánh trước cho sidecar. |
| Caveat trong bảng cảnh báo `:1826–1828` | Dùng cùng `_ten_tep`, nên verdict `.MD` với ID cùng hàng xanh; bỏ ID hoặc chỉ đổi case tên verdict trong hàng cảnh báo đều đỏ đúng caveat. ID được so nguyên, đúng hợp đồng. |
| t26 `:1678–1699` | Dùng cùng listing, đọc nguyên `verdict_path`, kiểm tệp, băm và https. Receipt HOA băm đúng xanh, đổi riêng băm đỏ `LỆCH BĂM`; t26 không có trách nhiệm thay cổng lược đồ v2. |
| Fixture builders `:1856`, `:1860`, `:1929–1939` | Các tên `.receipt.yaml` dựng cứng tại đây là đầu vào do fixture chủ động tạo, không phải consumer khám phá tệp. Fixture mới còn tạo tên HOA/mixed case qua probe riêng. |
| Các `_ten_tep` call site còn lại | Ngoài hai consumer `:1773`, `:1827`, chỉ còn assertion trực tiếp trong ca mới `:1942`. Không tìm thấy consumer regex phân biệt hoa thường thứ ba trong chính module này. |
| Các glob/endswith khác trong module | Glob `.yml`/`.yaml` ở `:2389`, `:2611` và phép kiểm đuôi `:12925` phục vụ workflow; `receipt.json` ở `:6420` là artifact M4. Chúng không đọc receipt/verdict của `ops/reviews`. |
| `bien_nhan_v2_test.py:620`, c12 | `endswith(".receipt.yaml")` phân biệt hoa thường nhưng chỉ lọc **snapshot cutover cố định** `2f84531`. Tự đọc Git: đúng 11 receipt, mọi suffix đều thường. Không bỏ thành viên nào của snapshot ấy; không phải đường F1. [historical-cutover.json](review-evidence/historical-cutover.json). |
| `bien_nhan_v2_test.py:1705`, c38 | Glob receipt thật còn phân biệt hoa thường; đã đo ca xanh nhưng bỏ alias HOA. Thuộc F1. |
| `bien_nhan_v2_test.py:1908`, c42 | Cùng vấn đề khi lấy tập receipt để so hai mirror builder; đã đo bỏ alias HOA. Thuộc F1. |
| `.claude/dev/packet_loop_test.py:4320–4334` và các fixture receipt | Tên thường được dựng có chủ ý trong fixture; reader thực được kiểm là `_doc_bien_nhan` ở `packet_loop.py:2121`. Reader ấy bỏ HOA, đã đo 1/0, ghi cùng lớp F1. |
| `chon_reviewer_test`, `ci_dang_ky_test`, `ci_duong_nhanh_test` | `ops/reviews` là dữ liệu kiểm phân loại/định tuyến đường dẫn; không có bộ trích đuôi receipt hoặc verdict để sót ở đây. `_ten_tep` trong `ci_dang_ky_test` là helper nhận diện tên chương trình, không phải helper t27. |
| `idiom_py_test`, `cong_cu_test`, `tl_selftest` | Tham chiếu vùng lịch sử, chính sách quét code hoặc dữ liệu kiểm inventory; không phải consumer tên receipt/verdict. |
| `kiem_nhan_hint_test.py:22` | Đọc `ops/reviews/**/*HINT.patch`, hợp đồng riêng của patch-as-hint; không dùng glob này để chứng nhận receipt/verdict. |
| Validator v2 `:1442`, sinh nợ `:1601`, packet loop `:2121` | Còn dùng glob suffix thường trên tập động. Validator có phản chứng CLI trước/sau rõ ràng; hai đường phụ có probe riêng. Thuộc F1. |

Các đối chứng đơn vị và danh sách token nằm trong [probe-results.json](review-evidence/probe-results.json), sinh bởi [review_probes.py](review_probes.py).

## Răng của ca mới và nhánh `phan_biet`

Đã chạy CLI thật trên bốn bản sao riêng chỉ chứa module test cần thiết dưới `review-evidence/mutations/`. Mỗi mutant thay đúng một chốt, không cộng dồn thay đổi. Selector là tên đầy đủ `t27_phan_chung_bien_nhan_duoi_HOA_co_hang_phai_XANH_va_sidecar_HOA_tim_duoc`; argv nguyên văn trong JSON.

| Bản | rc / số ca | Kết quả đúng bước |
|---|---|---|
| Control | 0 / 1/1 | Đạt cả trình tự. |
| Bỏ `re.IGNORECASE` chỉ ở `_ten_tep` | 1 / 0/1 | Bước 1: alias HOA đủ hàng lại bị báo thiếu ở cột `biên nhận`. |
| Dựng cứng sidecar thường và lookup `is_file()` | 1 / 0/1 | Bước 3: `b-VERDICT.md: KHÔNG có biên nhận`. |
| Bỏ riêng chốt `len(ung_vien) == 1` | 1 / 0/1 | Bước 4: `hai sidecar chỉ khác hoa thường ở đuôi mà vẫn XANH — tự chọn một`. |

Log: [control](review-evidence/mutation-control.stdout), [bỏ IGNORECASE](review-evidence/mutation-no-ignorecase.stdout), [sidecar dựng cứng](review-evidence/mutation-hardcoded-sidecar.stdout), [bỏ mơ hồ](review-evidence/mutation-no-ambiguity-check.stdout).

Trace trực tiếp ca mới ghi nhận `phan_biet=True`, ba tên đã được vật chất hóa đúng thứ tự so sánh:

```text
b-VERDICT.RECEIPT.YAML
b-VERDICT.md
b-VERDICT.receipt.yaml
```

Trace đi qua dòng 1971–1976, tức đã chạy bước 4 và bắt assertion mơ hồ. Điều kiện hiện tại không luôn-false trên Linux; mutant bỏ guard thật sự bị giết. Nhánh `False` vẫn có thể bỏ bước 4 trên filesystem không phân biệt hoa thường, hoặc khi `write_text` ném `OSError` do khối except hiện tại; một dòng 1/1 đơn lẻ không chứng minh đã đo bước đó. Trong lượt Linux này, trace và mutant loại trừ việc bỏ bước 4. Không cấp tín dụng đo mơ hồ trên Windows từ kết quả Linux hay từ lời khai executor.

## Đã đo

Lệnh chạy qua [review_run.py](review_run.py) ghi riêng stdout, stderr, argv, cwd, rc và thời lượng. Các lệnh Python dùng `PYTHONDONTWRITEBYTECODE=1`; fixture/clone dùng cấu hình Git toàn cục và hệ thống rỗng. Clone head/base có index/ref riêng, alternate object chỉ đọc từ nguồn, snapshot refs được giữ trong [source-refs.txt](review-evidence/source-refs.txt). `core.abbrev=7` chỉ cấu hình ở clone.

| Lệnh/phạm vi | rc | Kết quả |
|---|---:|---|
| `git -C cay-kho rev-parse HEAD`, đầu/cuối | 0 / 0 | Đúng reviewed SHA đầy đủ. |
| `sha256sum tham-chieu/wp1006.md` | 0 | Khớp hash đóng băng nêu trên. |
| `python3 ops/lease_publish_test.py --chi-ca=t27_`, head / base | 0 / 0 | **3/3 / 2/2**, bỏ qua 0. |
| `python3 review_probes.py` | 0 | Dương/âm alias, caveat, đường dẫn, stem, tên khác case, băm; control và ba mutant đạt kết quả mong đợi. |
| `python3 review_schema_probe.py` | 0 | Tái hiện F1 bằng CLI; validator rc **1 → 0** khi chỉ đổi suffix thường → HOA, t26/t27 head đều xanh. |
| `python3 review_other_readers.py` | 0 | c38/c42 không đọc alias; reader packet loop 1/0; `--sinh-no` 1/0. Không khai đã chạy toàn suite `bien_nhan_v2_test.py`. |
| `python3 ops/bien_nhan_v2.py --root .`, clone head trước khi thêm alias | 0 | **253 v2 / tổng 306**, 0 vi phạm, 0 KHÔNG ĐO ĐƯỢC. |
| `ruff check --no-cache --select F --output-format json ops/lease_publish_test.py`, head / base | 1 / 1 | Mỗi bên **7 F401 + 2 F541**, cùng code/message, **delta F = 0**. Bare lint không xanh tuyệt đối. |
| `git -C cay-kho diff --check b29da0b 4f9774a` | 0 | Không lỗi whitespace. |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .`, clone head | 0 | Quét 10 tệp, 0 chỗ chép doctrine. |
| `python3 ops/lease_publish_test.py`, clone head | **1** | **267/269**, chạy 269, bỏ qua 0; **499.189 giây**. |
| Cùng lệnh, clone base | **1** | **266/268**, chạy 268, bỏ qua 0; **502.090 giây**. |
| `python3 review_finalize.py` | 0 | 8.468 tệp tracked trùng băm đầu/cuối; HEAD/tree/index/refs và status không đổi; nhật ký cấp ngoài đủ từng cặp vào/ra; Ruff delta 0. |

Nhật ký toàn suite: [head stdout](review-evidence/full-head.stdout), [head rc/thời lượng](review-evidence/full-head.json), [base stdout](review-evidence/full-base.stdout), [base rc/thời lượng](review-evidence/full-base.json). Phân tích từng ca tại [final-integrity.json](review-evidence/final-integrity.json).

Hai ca đỏ **giống hệt** ở cả hai phía:

- `t137_M9_workflow_admission_hop_dong_tinh_va_actionlint_shellcheck`: thiếu `shellcheck`.
- `t159_t137_can_do_DU_ket_qua_va_dung_nhan_than_timeout`: chưa tới consumer ShellCheck vì cùng thiếu công cụ.

Hai lệnh toàn suite được ghi **failed**, hai phép đo ShellCheck **not_measured** vì môi trường; không đổ chúng cho PR và không đổi nhãn thành pass. Delta là đúng một ca mới đạt, không thêm ca thất bại hoặc bỏ qua. Đã đếm **269/268 cặp vào/ra cấp ngoài**, không cộng các lượt A/B lồng bên trong; t125 cấp ngoài đạt ở cả hai phía.

## Giới hạn và tính toàn vẹn

Môi trường đã đo: Linux, Python 3.13.17, PyYAML 6.0.3, Ruff 0.16.9; có actionlint, thiếu ShellCheck. Windows thật và CI GitHub của exact head: **not_measured** trong lượt này. Không suy xác nhận từ lời khai `tra-luat-win` của executor. Chưa đạt điều kiện N/N toàn suite vì hai phép đo thiếu công cụ; đây tách biệt với phản chứng F1 đã đo được.

Reviewer: OpenAI Codex, phiên API độc lập, shell/tools qua transport `machine`, bề mặt `codex_service` theo ánh xạ của kho. Model ID/effort thực phục vụ không có runtime attestation trong chứng cứ của lượt review, ghi **KHONG_DO_DUOC**; không tự khai là `codex exec`. Executor là Claude theo phân công, không có phép đo model thực phục vụ của executor trong lượt này. Verdict đánh giá mã ở exact SHA, không tự tạo state approval hay quyền land.

Snapshot đầu/cuối bao gồm nội dung tracked, untracked và ignored, HEAD/tree/index; refs cũng khớp. Checkout nguồn sạch, 8.468 tệp trùng băm. Đây là chứng cứ không có delta quan sát được giữa hai mốc, không phải chứng nhận OS đã cưỡng chế read-only hoặc chứng minh chưa từng ghi rồi hoàn nguyên. Không push, không gọi API ghi GitHub, không merge, deploy hay gọi LIVE.
