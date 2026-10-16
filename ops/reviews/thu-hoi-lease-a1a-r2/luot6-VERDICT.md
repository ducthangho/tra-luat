verdict: changes_requested
reviewed_spec_sha256: c314ce69fdc86ae1f31ac9de25523ac00b9d36f2305811c8a9345cdcec138c47
reviewed_sha: 635e9a23a3bc7106adbc7af862cb505277b6312c
P1: 0   P2: 0   P3: 1
reviewer_provider: openai_codex
model_tu_khai: GPT-6 (Codex); biến thể/effort backend KHÔNG ĐO ĐƯỢC

Review độc lập lượt **6/10**, bản nháp 6. Đã ghi VERDICT sơ bộ trước khi chạy rồi cập nhật kết quả. Phạm vi: delta nháp 5 → 6 và hệ quả; không phải nghiệm thu implementation A1a r2.

**F15 đã đóng. Không tìm thấy P1/P2 mới hoặc finding cũ bị delta tái mở.** Tự kiểm **30/30**, ma trận **20/20 khớp + gốc**, ba hiện vật chạy lại bằng từng byte bản cung cấp. Còn **một P3**: lời giải thích vị trí hai hàng mới trong bảng đột biến không khớp bảng. `HINT.patch` sửa một dòng SPEC, đã kiểm áp trên bản sao.

Không sửa `cay-kho/`, SPEC nguồn, script hoặc hiện vật đầu vào. Quyết định prediction-only, Q6 cây mốc + (b), ngoại lệ ADR-0044 ≤3 tệp/≤663 dòng thêm và trần10 giữ nguyên.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Finding | Trạng thái | Bằng chứng chạy được ở lượt này |
|---|---|---|
| F15 — `tham-chieu-lua-chon-da-xoa` (finding duy nhất lượt5) | **ĐÓNG** | `python3 -B scratch/review6.py`: áp `luot5-HINT.patch` vào bản sao `SPEC.truoc.md` rc0; băm kết quả `f7df1cd56136add6a7485426c386ab0b88c8d6b246851517ab1de33afc0f95b5`, đúng lời khai lượt5/E18. Câu điều kiện sau vá có nguyên văn ở SPEC:380; tham chiếu “(a) hoặc (b) ở mục 1” không còn. `scratch/measure.json` lưu câu và băm. |
| F11 — `q6-thieu-kiem-id-ten` (từng ĐÓNG-MỘT-PHẦN; lượt5 đã ĐÓNG) | **ĐÓNG**, không tái mở | So AST: mọi hàm của `do_q6.py` ngoài `tu_kiem` không đổi, gồm validator `dan_xuat`. Suite30/30 giữ các ca ID/tên/schema; walker độc lập kiểm đủ89 tệp thật và bốn trường được đọc. `scratch/measure.json`, `scratch/self-check.log`, `scratch/independent-walker.json`. |
| F2 — `mien-lich-su-vuot-quyet-dinh` (từng ĐÓNG-MỘT-PHẦN; lượt5 đã ĐÓNG) | **ĐÓNG**, không tái mở | §0–7 bằng từng byte bản trước; mốc là tổ tiên HEAD và origin/master, giờ commit bằng C. Walker độc lập ra11 cặp, digest đúng, giữ0. Mutant đọc HEAD vẫn chỉ làm đỏ `cay-sau-khong-doi-cay-moc`. |
| F13 — `q6-thieu-kiem-id-ten` | **ĐÓNG**, không tái mở | Hai ca tràn UTC vẫn rc3; bốn probe thời điểm biên hợp lệ đều rc0. Mutant riêng bỏ ghi vi phạm khi tràn làm đỏ đúng hai ca tràn, đủ30 ca, không Traceback. `scratch/own-probes.json`, `scratch/own-mutations.json`. |
| F14 — `loi-khai-co-lap-fixture-sai` | **ĐÓNG**, không tái mở | SPEC:319–322 vẫn nói rõ các chốt che nhau. Hai hàng mới khai đúng tập `{han-bien-hop-le}` và ∅. Mutant đơn miền ID chỉ đỏ ca đứng riêng; mutant ba miền đỏ đúng5 ca. Không có lời khai mới rằng mọi fixture chỉ vi phạm một chốt. |
| F12 — `q6-thieu-kiem-id-ten` | **ĐÓNG**, không tái mở | Các ca miền ID, null/khoá không giá trị và mutant tương ứng đều tiếp tục đúng trong suite30 và ma trận20. |

Đã rà tất cả nhãn ĐÓNG-MỘT-PHẦN ở verdict1–5: chỉ F2/F11 từng mang trạng thái này; cả hai đã được đóng ở lượt5, không còn tồn dư riêng cần quyết lại.

Các finding đã đóng khác không bị delta tái mở:

- **F1/F3:** quyết định prediction-only và luật ba trạng thái giữ nguyên (§0–7 byte-equal; `dan_xuat` AST-equal). Ca một chiều/thay tiếp/hết hạn vẫn đạt.
- **F4/F5/F7/F8/F9/F10:** §0–7 và blob của cổng, test, workflow, spec cha bằng nhau giữa hai reviewed head. `scratch/measure.json/unchanged_blobs` lưu OID đầy đủ. Đây là bằng chứng không hồi quy do delta, không khai đã chạy lại toàn bộ A18/M14.
- **F6:** không đổi số nền tại `24c48e28`; các số mới30/30 và20/20, băm script và tổng ước422–663 đều đo khớp. F16 bên dưới là tham chiếu vị trí hàng sai, không phải số đo thẩm quyền sai.

## Findings

### F16 — P3 — `tham-chieu-vi-tri-bang-sai`

**Vị trí:** `SPEC.md:356–357`, câu “Bản nháp 6 thêm hai dòng cuối…” ngay dưới bảng §8.2 (các hàng liên quan ở :348–350).

Bảng có20 hàng đột biến. Hai hàng **mới thêm** là hàng18 “từ chối hạn hợp lệ năm 1 / 9999” và hàng19 “gỡ riêng chốt thư mục con”. Hai hàng **cuối bảng** lại là hàng19 và hàng20 “cả ba chốt miền cùng lúc”; hàng20 đã có trong bản nháp5. Vì thế chỉ dẫn “hai dòng cuối” trỏ nhầm một hàng cũ và bỏ sót một hàng mới.

**Bằng chứng chạy được:**

```sh
. scratch/env.sh
python3 -B scratch/review6.py
```

Script trích bảng từ cả hai SPEC và assertion: bảng cũ18 hàng, bảng mới20 hàng; đúng hai hàng mới ở vị trí `[18, 19]`; hàng cuối đã có trong bảng cũ; tập hai hàng mới khác hai hàng cuối. Kết quả nằm ở `scratch/measure.json/table`, gồm nguyên văn nhãn và `claim_line=357`. `DIFF.truoc-nay.patch` cũng được assertion bằng Git diff ba tệp tại đúng hai commit.

**Phân hạng P3:** chỉ sai chỉ dẫn chữ nghĩa. Tên mutant, tập đích, kết quả chạy và số20/20 vẫn đúng; không gây lỗi thuật toán hay thay quyền executor.

**Sửa:** gọi thẳng tên hai hàng mới, thay vì chỉ vị trí “hai dòng cuối”. `HINT.patch` chỉ sửa câu này. Dry-run và áp thật trên bản sao bằng `patch -p0` đều rc0; băm SPEC sau vá `f8c0d3fbc21424b72e9f0924a1a809dc169fc0109ebbd7517be1e008166a996e`. Xem `scratch/build_hint6.py`, `scratch/hint-check.json`.

## Bảng đo lại

| Lời khai / đối tượng | Thực đo | Bằng chứng / giới hạn |
|---|---|---|
| SPEC398 dòng, băm trong prompt | **398 dòng,49.319 B**, băm đúng header | Bằng blob reviewed SHA và bản trong mirror |
| `do_q6.py` | `7fd77bc62756a2b51489e3bbd8f10bc60593d8ca68462df2e3ebd80b85611fd6` | Khớp SPEC và blob commit |
| `mut_q6.py` | `71b1fbb5d74d79728c1ee5aa0bf75be8c51f4df79fe3adc371927c0a2bb5ec81` | Khớp SPEC và blob commit |
| Tự kiểm | **30/30**, rc0 | `scratch/self-check.log`, byte-equal bản cung cấp; stderr rỗng |
| Ma trận đột biến | **20/20 khớp + gốc**, rc0 | `scratch/mutations.log`, byte-equal; 0 Traceback |
| Số mutant làm đỏ suite / sống | **19 / 1** | Mutant bỏ riêng chốt thư mục có tập đích rỗng, rc0 đúng khai; 20/20 là số tập khớp, không phải20 mutant bị giết |
| JSON cây thật | **byte-equal**, rc0 | `scratch/q6-rerun.json`; sha256 `1fc99cd9339fb5f085436e60ef39bac3058a79dbc009161597ecc7bc85efbd61` |
| Miền / hợp lệ / ngoài miền | **89 / 89 / 3** | Walker độc lập; ba tệp ngoài miền có đuôi `.yaml.nhap` |
| Cặp hai chiều / một chiều | **11 / 3** | Cặp, OID và path hai đầu khớp bản in |
| Digest tuple4 | `8f372ccd2ceab70901868a58d3380acbd89dce25c7127d4d514bc959270fef48` | Tự dựng cặp chiều cũ→mới, sort rồi JSON compact |
| Vi phạm / KXD / giữ lại | **0 / 0 / 0** | 11 đầu mới đều hết hạn |
| Hạn muộn nhất | `2026-09-08T10:17:12+00:00` | Walker độc lập |
| C = giờ commit mốc | `2026-09-10T11:55:37+07:00` = `2026-09-10T04:55:37Z` | So datetime; ancestor HEAD và origin/master đều rc0 |
| Tổng ước dòng thêm | **422–663** | Cộng độc lập7 hàng; chưa phải numstat implementation |
| Mirror | **438/438**, tên và OID bằng nhau | So bare cục bộ với cache; không phải quảng bá máy chủ mạng |
| origin/master cục bộ | `eb32b50e40d1b9ee006e057c2f9afc188283af56` | Đúng `.mirror-info`; không dùng làm nguồn Q6 |
| Probe biên riêng | **7/7** | Bốn biên hợp lệ, hai tràn, một hạn=C |
| Áp hint lượt6 | dry-run0 / áp0 | Một dòng SPEC, không sửa script |

Không dùng438 ref của mirror để bác bỏ428 ref lịch sử trong §1. Header “đã dùng5/10” mô tả trước lượt gọi6 này.

## Nghiệm thu

**Delta mã thực thi dẫn xuất bằng0.** So AST của các hàm trong `do_q6.py`: chỉ `tu_kiem` thay đổi. Hai script bằng blob commit; diff ba tệp bằng hiện vật cung cấp. Những thay đổi spec gồm header, băm/số ca, giải thích mutant và điều kiện F15; §0–7 không đổi.

**Hai mutant mới đúng tập đích khai trước:**

| Mutant | Tập HONG thực đo | rc / số ca |
|---|---|---|
| `tu-choi-nam-bien` | `{han-bien-hop-le}` | rc1, đủ30 ca, không crash |
| `bo-rieng-chot-thu-muc-con` | ∅ | rc0,30/30 |

18 mutant cũ giữ nguyên tập đích và khớp log. Hàng rỗng có ý nghĩa cụ thể: khi bỏ riêng chốt thư mục, `sub/z` vẫn khác ID `z`; cho ID chứa `/` thì chốt miền ID chặn. Đột biến ghép nhận thư mục con và so basename tiếp tục làm đỏ `thu-muc-con`. Không coi mutant sống này là lỗi test mà phía soạn đã che giấu.

**Tự đột biến bản sao:** `scratch/probes6.py` ghi tập dự đoán vào `scratch/own-mutation-targets.json` trước khi chạy; nguồn mutant và stdout/stderr lưu trong `scratch/`.

| Mutant reviewer | Trên suite30 | Đối chứng / kết luận |
|---|---|---|
| Từ chối riêng năm1 | Chỉ `han-bien-hop-le` HONG | Sống29/29 trên bản nháp5; ca mới bắt riêng biên dưới |
| Từ chối riêng năm9999 | Chỉ `han-bien-hop-le` HONG | Sống29/29 trên bản nháp5; ca mới bắt riêng biên trên |
| Bỏ qua im lặng các tệp hạn hợp lệ năm1/9999 | Sống30/30 | Hai tệp biên của fixture mới đứng ngoài cặp nên bỏ qua chúng không đổi rc/tập giữ. Probe riêng đưa biên lên đầu mới của cặp: gốc có2 lease hợp lệ, mutant chỉ1; biên trên còn làm mất cặp được giữ |
| Tràn UTC: bỏ ghi vi phạm rồi tiếp tục | Đúng hai ca tràn HONG | Suite bắt việc nuốt lỗi; đủ30 ca, không crash |
| Bỏ riêng chốt thư mục | Sống30/30 | Khớp giải thích chốt tên che chốt thư mục |

Mutant bỏ qua tệp biên cho thấy **giới hạn assertion**, không phải lỗi mã hiện tại: mã gốc nhận đúng cả hai biên. Spec khai ca đối chứng rc0 và mutant từ chối biên, không khai bộ30 ca giết mọi cách làm sai. Vì vậy không nâng khoảng trống này thành P1 “tiêu chí không thể đỏ”; đã có probe làm hành vi sai quan sát được. Không đưa mutant riêng vào số20/20 của phía soạn.

Bảy probe dùng kho Git thường và helper thật nguyên văn: năm1/năm9999 với Z và với offset vẫn trong miền đều rc0; offset gây tràn hai phía đều rc3; hạn=C bị loại. So cả rc lẫn tập giữ, và số lease ở đối chứng mutant. Không dựng helper hoặc object Git giả.

Bộ tự kiểm vẫn chỉ assertion tập giữ ở ca kỳ vọng rc0; ca rc3 chỉ assertion mã thoát. Đây là hành vi cũ, không thay trong delta. Probe riêng có so tập giữ cả ở rc3. Các fixture dùng clock cố định, không chứng minh giờ commit fixture bằng C; cây thật đã được so giờ commit riêng.

## Phản chứng đã chạy

Sau khi đọc prompt snapshot theo yêu cầu đầu vào, mọi đọc/ghi phục vụ review ở trong cwd; không mạng. Git được cô lập bằng `scratch/env.sh`, `GIT_CONFIG_NOSYSTEM=1`, global config rỗng dưới scratch, `GIT_OPTIONAL_LOCKS=0`, TMPDIR dưới cwd. Không fetch, không gọi remote mạng; bare `kho.git` chỉ đọc bằng `for-each-ref`.

```sh
mkdir -p scratch/m
: > scratch/empty.gitconfig
. scratch/env.sh

python3 -B do_q6.py --tu-kiem cay-kho > scratch/self-check.log 2> scratch/self-check.err
python3 -B mut_q6.py scratch/m cay-kho do_q6.py > scratch/mutations.log 2> scratch/mutations.err
python3 -B do_q6.py cay-kho 072181157a27804e69deb35bb792a88c70ac31e3 2026-09-10T04:55:37Z > scratch/q6-rerun.json 2> scratch/q6-rerun.err
python3 -B scratch/review6.py
python3 -B scratch/probes6.py > scratch/probes6.log 2> scratch/probes6.err
python3 -B scratch/build_hint6.py
git -C cay-kho status --porcelain --untracked-files=all
```

Các tiến trình chính đều rc0; các tiến trình mutant có rc1 đúng dự đoán được ghi riêng. `review6.py` hoàn tất `REVIEW6_OK`; `probes6.py` hoàn tất `PROBES6_OK`. Không có lỗi bị bỏ qua để lấy kết luận xanh. Mirror status cuối rỗng.

`HINT.patch` sha256 `5e0e89aabfcffe166b980a8ac72fdd7ef53c53f678edb31c1d9a907c4b5e8503`. Chỉ áp thử dưới `scratch/hint6/`; SPEC nguồn còn nguyên băm reviewed.

## KHÔNG ĐO ĐƯỢC

- Không xác minh nguồn mạng: comments/tags, advertisement máy chủ, PR/merge, thời điểm chạy của phiên soạn. E19 về CI/billing là lời khai chưa kiểm chứng, không dùng để suy hồi quy hay kết quả review.
- Tái tạo được kết quả áp hint5 và bản in, không chứng nhận lịch sử thao tác phiên soạn hoặc các lần chạy đầu từng LỆCH.
- Không chạy suite168, CI, actionlint/shellcheck hoặc toàn bộ nghiệm thu implementation A1a r2; các phần đã đóng ngoài delta chỉ kiểm không hồi quy qua nội dung và OID.
- Các hướng cần tự soạn nội dung nhạy cảm chỉ mô tả bằng lời: đường thoát cây; tên đồng tự Unicode; tên đường dẫn có ký tự khiến Git xuất dạng quote/escape; helper hoặc object Git giả. Không dựng payload, không chạy các hướng ấy, không nhận tín dụng kiểm thử. Bộ đọc đường dẫn không thay trong delta.
- Không suy30/30 hoặc20/20 thành tính đầy đủ của bộ test. Hai mutant reviewer sống và giới hạn assertion đã khai ở trên.
- Không đo được biến thể/effort backend; tên reviewer mà SPEC yêu cầu không phải bằng chứng model thực tế.

Còn một P3 nên verdict là `changes_requested`. Không tự áp hint vào nguồn, đóng băng đặc tả, cấp lease hoặc merge. Giữ quy trình lặp tới sạch trong trần10 và human audit đã được chủ kho quyết.
