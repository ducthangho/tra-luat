verdict: changes_requested
reviewed_spec_sha256: 8a0a9a5ab8188f91b132e0c78a482536d3af7ff514b34e4edff4edfe5f791133
reviewed_sha: 43a17e1e30a570b26e50eecbf00dab1ec1875f8d
P1: 0   P2: 0   P3: 1
reviewer_provider: openai_codex
model_tu_khai: GPT-6 (Codex); biến thể/effort backend KHÔNG ĐO ĐƯỢC

Review độc lập lượt **5/10**, bản nháp 5. Đã ghi verdict sớm rồi bổ sung bằng kết quả chạy. Phạm vi: delta nháp 4 → 5 và hệ quả; không phải nghiệm thu implementation A1a r2.

**F13 và F14 đã đóng; các tồn dư F11/F2 đã đóng trong phạm vi review.** Tự kiểm **29/29**, ma trận **18/18 + gốc**, JSON cây thật và cả hai log đều khớp từng byte với hiện vật cung cấp. Còn **một P3**: điều kiện cấp lease dẫn tới hai nhãn lựa chọn đã bị delta xoá. Không tìm thấy P1/P2 mới; không nâng khoảng trống bao phủ thành finding khi không có lời khai bao phủ tương ứng.

Giữ nguyên `SPEC.md`, hai script, các hiện vật đầu vào và `cay-kho/`. HEAD/tree: `43a17e1e30a570b26e50eecbf00dab1ec1875f8d` / `f39bd31d763ed43076d90e1b98853e02b5b2731e`. `HINT.patch` chỉ sửa một dòng SPEC; đã áp thử vào bản sao trong `scratch/` bằng `patch -p0`.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Finding | Trạng thái | Bằng chứng chạy được |
|---|---|---|
| F13 — `q6-thieu-kiem-id-ten` | **ĐÓNG** | `python3 -B scratch/probes5.py`: cùng kho Git thật, OID, clock và helper nguyên văn, CLI nháp4 trả rc1/OverflowError cho cả biên trên/dưới; nháp5 trả rc3, JSON ghi vi phạm, không Traceback. Bốn ca thời điểm hợp lệ sát biên vẫn rc0. `scratch/cli-comparison.json`, `scratch/own-cases.json`. Mutant cung cấp coi tràn như hết hạn giết đúng hai ca mới; mutant riêng bỏ ghi vi phạm rồi bỏ qua tệp cũng giết đúng hai ca, chạy đủ29, không crash. |
| F14 — `loi-khai-co-lap-fixture-sai` | **ĐÓNG** | SPEC:319–322 đã bỏ khẳng định mọi fixture chỉ vi phạm một chốt, nêu rõ các chốt che nhau. `scratch/self-check.log` vẫn ghi hai vi phạm ở mỗi ca ID ngoài miền đầu cặp; `scratch/mutations.log` xác nhận mutant miền ID đơn chỉ đổi ca đứng riêng, mutant ba miền đổi đúng5 ca. Lời văn nay khớp phép đo, không xoá fixture để làm sạch số. |
| F11 — `q6-thieu-kiem-id-ten` (trước **ĐÓNG-MỘT-PHẦN**) | **ĐÓNG** | Phần thiếu ID/tên/schema của F11/F12 tiếp tục được chặn; tồn dư hạn ở F13 đã đóng. 29/29 tự kiểm và 38/38 probe riêng: tên đầu mới, `.yml` hợp lệ, thư mục con, các kiểu hạn/bia mộ/thay thế, lặp sau chuẩn hoá, ID ngoài miền đều đúng hợp đồng được kiểm. Walker độc lập kiểm89 tệp, bốn trường và tên/ID; `scratch/independent-walker.json`. Không suy kết quả này thành chứng minh mọi đầu vào khả dĩ. |
| F2 — `mien-lich-su-vuot-quyet-dinh` (trước **ĐÓNG-MỘT-PHẦN**) | **ĐÓNG** | Nguồn/mốc/clock không đổi: `scratch/measure.json` xác nhận vòng1–3 và §1–7 bằng nhau, mốc là tổ tiên cả HEAD lẫn origin/master, giờ commit đúng C. Mutant đọc HEAD chỉ đổi `cay-sau-khong-doi-cay-moc`. Walker độc lập cho11 cặp, digest đúng, giữ0. Tồn dư hợp đồng dẫn xuất F11/F13 đã đóng; không quyết lại Q6 hay bộ lọc(b). |
| F12 — `q6-thieu-kiem-id-ten` (đã đóng lượt4) | **ĐÓNG**, không tái mở | Ba ca miền ID và ba ca null/khoá không giá trị đều rc3; các mutant miền/null vẫn đúng tập đích. Probe tên đầu mới và `.yml` tiếp tục đúng. |

Các finding đã đóng khác **không bị delta tái mở**:

- **F1:** quyết định prediction-only, bất biến holder/rc và cấm dùng `DU_BAO` cấp lease giữ nguyên. Vòng4 chỉ ghi ngoại lệ ADR-0044 và trần review10, không trả lại quyền xoá holder.
- **F3:** thuật toán ba trạng thái không đổi; các ca một chiều/thay tiếp của suite đúng. Probe riêng `oneway-expired` và `cycle` đều rc0, giữ0; hết hạn được xét trước bia mộ.
- **F4/F5/F7/F8/F9/F10:** §1–7, gồm A4/A7/A16/A18–A22 và §5.1, bằng từng byte bản trước. Blob của cổng, test, workflow và spec cha đều không đổi giữa hai head; OID đầy đủ ở `scratch/measure.json/unchanged_blobs`. Đây là kiểm không hồi quy trong delta, không khai đã chạy lại suite M14/A18.
- **F6:** số nền tại `24c48e28` không bị sửa; các số mới29/29,18/18, băm script và tổng ước422–663 đều đo khớp. Không quay lại đơn vị “92 lease”.

E17 “áp hint lượt4” tái tạo được: `scratch/review5.py` lấy SPEC/script ở head nháp4, áp `luot4-HINT.patch` rc0; băm script kết quả đúng `957b6432e060eb125a7b3957ce79cbf0538ed6757ac7c3b0980453d36af23280`. `scratch/previous-hint.json`. Đây là kiểm kết quả có thể tái tạo, không chứng nhận lịch sử thao tác riêng của phiên soạn.

## Findings

### F15 — P3 — `tham-chieu-lua-chon-da-xoa`

**Vị trí:** `SPEC.md:377` (§8.3), hệ quả trực tiếp của sửa §8.1 tại dòng282–285; quyết định tương ứng ở dòng54.

Điều kiện cấp lease vẫn viết **“chủ kho đã chọn (a) hoặc (b) ở mục 1”**. Bản trước định nghĩa(a) là ngoại lệ ADR-0044 và(b) là tách M5–M9; delta đã xoá cả hai nhãn, thay bằng quyết định **đã chốt ngoại lệ ≤3 tệp, ≤663 dòng thêm; B1–B5 không tách**. Dòng điều kiện còn dẫn tới hai lựa chọn không còn được định nghĩa ở nơi nó trỏ tới.

**Bằng chứng chạy được:**

```sh
python3 -B scratch/review5.py
```

`scratch/measure.json/dangling_reference` ghi và assertion:

| Thuộc tính | Nháp4 | Nháp5 |
|---|---:|---:|
| §8.1 định nghĩa nhãn(a) | true | false |
| §8.1 định nghĩa nhãn(b) | true | false |
| §8.3 vẫn dẫn “(a) hoặc (b) ở mục1” | true | true |

`new_reference_line=377`; trường `new_section8_1` lưu nguyên đoạn đích mới. `delta_matches_git_diff=true` xác nhận đây đúng delta cung cấp/commit, không phải nhầm bản nguồn.

**Phân hạng P3:** quyết định cụ thể đã rõ ở §0 và §8.1, nên đây là tham chiếu chữ nghĩa lỗi thời, không phải quyền để executor chọn lại phương án(b), không phải lỗi thẩm quyền hay số đo. Không yêu cầu chủ kho quyết lại ngoại lệ.

**Sửa:** thay dòng ấy bằng “áp dụng ngoại lệ ADR-0044 đã được chủ kho chốt tại §0 vòng4 và mục1 (≤3 tệp, ≤663 dòng thêm, chỉ cho A1a)”. `HINT.patch` làm đúng một thay đổi này. Dry-run và áp thật trên bản sao đều rc0; kết quả bằng chính xác nội dung dự kiến, băm SPEC sau vá `f7df1cd56136add6a7485426c386ab0b88c8d6b246851517ab1de33afc0f95b5`. Xem `scratch/hint-check.json` và `scratch/build_hint5.py`.

## Bảng đo lại

Nguồn bằng chứng: `scratch/measure.json`, `scratch/independent-walker.json`, các log chạy lại. Walker dùng `git ls-tree -rz`, kiểm schema bằng parser/helper thật đã chỉ định, nhưng tự xây cặp theo chiều **cũ→mới**, trạng thái và digest; không gọi `dan_xuat` để xây tập cặp.

| Lời khai | Thực đo | Giới hạn/bằng chứng |
|---|---|---|
| SPEC395 dòng, băm trong prompt | **395 dòng,48.047 B**, đúng băm header | Bằng blob tại reviewed SHA và bản trong mirror |
| `do_q6.py` | `8d8da92fcac225b7f43d79e49f3baa36e4d971f9486cb0724566b6b16637f8bc` | 237 dòng,12.939 B; đúng SPEC/E17 |
| `mut_q6.py` | `37575113a2bbfac8a0e44770946647d8c7031a1a3660d5fa7975ef84a5a3a07a` | 38 dòng,3.849 B; đúng SPEC/E17 |
| JSON cây thật | `1fc99cd9339fb5f085436e60ef39bac3058a79dbc009161597ecc7bc85efbd61` | 6.128 B; chạy lại rc0, byte-equal |
| Tự kiểm29/29 | **29/29**, rc0 | Log byte-equal, stderr rỗng |
| Ma trận18/18 + gốc | **18/18 + gốc**, `TAT_CA_KHOP` | Log byte-equal; gốc rc0, mỗi mutant rc1,0 Traceback |
| Miền/hợp lệ/ngoài miền | **89/89/3** | Ba tệp `.yaml.nhap` ngoài miền |
| Cặp hai chiều/một chiều | **11/3** | Cặp, blob và thứ tự khớp JSON |
| Digest tuple4 | `8f372ccd2ceab70901868a58d3380acbd89dce25c7127d4d514bc959270fef48` | JSON compact tuple4 sắp thứ tự |
| Vi phạm/KXD/giữ lại | **0/0/0** | 11 đầu mới đều hết hạn |
| Hạn muộn nhất | `2026-09-08T10:17:12Z` | Walker độc lập |
| C = giờ commit mốc | `2026-09-10T11:55:37+07:00` = `2026-09-10T04:55:37Z` | So datetime thực, không chỉ so chuỗi |
| Mốc là tổ tiên | rc0 với HEAD và origin/master | `merge-base --is-ancestor` |
| Tổng ước số dòng | **422–663** | Cộng độc lập cả7 hàng; vẫn là ước, không phải numstat implementation |
| Mirror lúc dựng | **438/438**, tên và OID bằng nhau | Bare cục bộ so cache; đúng `.mirror-info`, không đo máy chủ mạng |
| `origin/master` cục bộ | `68b552d0f08200ba860ea788517558a4172df384` | Không dùng làm nguồn Q6 |
| Probe độc lập | **38/38**,0 ngoại lệ ngoài dự kiến | So rc và tập giữ, kể cả ca rc3 |
| CLI nháp4/5 | Tràn: **rc1→rc3**, cả hai biên | Cùng fixture/OID/clock/helper; đối chứng biên hợp lệ rc0→rc0 |
| Áp HINT lượt5 | dry-run0 / áp0 | Chỉ một dòng SPEC, không sửa script |

438 head là số mirror lượt này; không dùng nó để bác bỏ số lịch sử428 ở nền hoặc437 của lượt4. Header “đã dùng4/10” mô tả trước lời gọi này; review này là lượt5/10.

## Nghiệm thu

**Delta thuật toán:** chỉ thêm bắt `OverflowError` tại `_doc_han`; không biến lỗi thành hết hạn/còn hạn. Phần dựng fixture chỉ đổi tạo thư mục cha để thêm ca thư mục con. Năm ca mới là tràn UTC trên/dưới, hạn bằng C, thư mục con, hạn vắng. Script/mutator hiện tại khớp bản trong reviewed commit; `DIFF.truoc-nay.patch` bằng chính xác Git diff ba tệp giữa hai head.

**Tập đích các mutant mới và mutant có tập mở rộng:**

| Mutant | Tập `HONG` khai trước = thực đo |
|---|---|
| Coi tràn UTC như hết hạn | `han-tran-UTC-tren`, `han-tran-UTC-duoi` |
| Đổi `<=` thành `<` | `han-bang-dung-C` |
| Nhận thư mục con + so basename | `thu-muc-con` |
| Hạn vắng mặc định năm2000 | `han-vang` |
| Bỏ lọc hạn | `het-han`, `han-bang-dung-C` |
| Hạn hỏng coi như hết hạn | `han-sai-dinh-dang`, `han-thieu-mui-gio`, `han-vang` |

Các mutant còn lại giữ đúng tập khai; không có tín dụng do crash. Hai tập mở rộng khớp giải thích E17. Không thể chứng nhận bằng hiện vật cuối rằng chính xác hai lần chạy đầu phiên soạn đã LỆCH, nhưng cơ chế gây lệch mà E17 mô tả tái lập được từ tập ca cuối.

**Tự đột biến bản sao**, nguồn và tập dự đoán lưu trước khi chạy tại `scratch/probes5.py` / `scratch/own-mutation-targets.json`; kết quả ở `scratch/own-mutations.json`:

| Mutant reviewer | Ca HONG trên suite29 | Đối chứng/ý nghĩa |
|---|---|---|
| Bỏ ghi vi phạm tràn UTC, vẫn bỏ qua tệp | Hai ca tràn UTC | Chạy đủ29, rc1, không Traceback; suite bắt bỏ qua lỗi im lặng |
| Bỏ riêng chốt thư mục con | Rỗng,29/29 | Chốt tên vẫn chặn `sub/z`; vì vậy mutant cung cấp cần đồng thời so basename. Không phải minh chứng chốt thư mục tự đứng riêng |
| Từ chối mọi hạn năm1 hoặc9999 | Rỗng,29/29 | Bốn probe biên **hợp lệ** phân biệt: gốc rc0, mutant rc3. Suite chưa có đối chứng dương sát miền ngày |
| Bỏ qua tệp thiếu hạn | `han-vang` | Ca mới bắt lỗi, rc1, đủ29, không crash |

Hai mutant sống được ghi rõ, **không** tính vào18/18 của bên soạn. Mutant thư mục còn bị chốt tên giữ nên chưa đổi kết quả hợp đồng; mutant từ chối năm biên cho thấy một khoảng trống bao phủ, nhưng mã hiện tại xử lý đúng và đặc tả không khai bao phủ mọi mutant. Không có căn cứ nâng chúng thành P1 “tiêu chí không thể đỏ”: probe độc lập đã làm tiêu chí đó đỏ trên bản đột biến.

Tự kiểm cung cấp chỉ assertion tập giữ khi kỳ vọng rc0; ở ca rc3, tập giữ được in nhưng không được assertion. Đây là hành vi cũ không đổi. 38 probe riêng so cả rc lẫn tập giữ, không dùng bản in suite để nhận thêm tín dụng assertion không có.

Ngoại lệ ADR-0044 đã được ghi đúng giới hạn ≤3 tệp, ≤663 dòng thêm, có test, với baseline bất biến; B1–B5 ở lại A1a. F15 chỉ cập nhật tham chiếu điều kiện tới quyết định đó. Review không mở lại prediction-only, cây mốc+(b), ngoại lệ hay trần10.

## Phản chứng đã chạy

Mọi lệnh từ cwd, không mạng. Git đọc mirror/bare cục bộ; kho fixture là kho Git thường trong `scratch/`. Không gọi remote của bare `kho.git`.

```sh
mkdir -p scratch/m
: > scratch/empty.gitconfig
export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL="$PWD/scratch/empty.gitconfig"
export GIT_OPTIONAL_LOCKS=0
export TMPDIR="$PWD/scratch"
export PYTHONDONTWRITEBYTECODE=1

python3 -B do_q6.py --tu-kiem cay-kho > scratch/self-check.log 2> scratch/self-check.err
python3 -B mut_q6.py scratch/m cay-kho do_q6.py > scratch/mutations.log 2> scratch/mutations.err
python3 -B do_q6.py cay-kho 072181157a27804e69deb35bb792a88c70ac31e3 2026-09-10T04:55:37Z > scratch/q6-rerun.json 2> scratch/q6-rerun.err
python3 -B scratch/review5.py
python3 -B scratch/probes5.py > scratch/probes5.log 2> scratch/probes5.err
python3 -B scratch/build_hint5.py
```

Các tiến trình chính trên đều rc0. `review5.py` assertion cả so sánh phạm vi, băm/hiện vật, diff, lời văn F15, walker và tái tạo hint4. `probes5.py` lưu riêng stdout/stderr CLI nháp4/5 cùng nguồn mutant; rc1 của CLI nháp4 là phản chứng dự kiến, không lỗi công cụ bị bỏ qua. `build_hint5.py` sinh hint và kiểm áp trên thư mục mới, không đụng SPEC nguồn.

`HINT.patch` sha256 `816f293e6ce767e4debdf233b81fad1651db2d0ec760ce14fd42c987a643d6de`. Sau kiểm áp, `git status --porcelain --untracked-files=all` của mirror rỗng; SPEC nguồn vẫn bằng blob reviewed SHA.

## KHÔNG ĐO ĐƯỢC

- Không mạng: không xác thực comments/tags, giờ chạy phiên soạn, advertisement máy chủ, trạng thái PR hay việc #579 đã land. Quyết định chủ kho trong prompt là đầu vào được giữ nguyên, không cần xin lại.
- Không chạy suite168, M14/A18 đầy đủ, actionlint/shellcheck, CI hoặc triển khai A1a r2. Kết luận không hồi quy của phần đã đóng dựa trên delta và blob bằng nhau, không thay cho nghiệm thu implementation.
- Chỉ mô tả bằng lời các hướng bị giới hạn: tên đường dẫn khiến Git xuất dạng quote/escape có thể ảnh hưởng lọc hậu tố theo dòng; đường thoát cây, đồng tự Unicode, chuỗi thoát và helper/object Git giả cần thử riêng nếu được cho phép. Không dựng payload hoặc chạy những hướng này, không tính thành finding thực nghiệm mới. Chúng đã được ghi giới hạn ở lượt4; delta không thay bộ đọc tên đường dẫn.
- Kho fixture dùng clock cố định C; không nhận giờ tạo commit fixture bằng C. Trên cây thật đã đối chiếu C với giờ commit mốc. Không suy bộ tự kiểm chứng minh cách chọn clock của mọi caller.
- Không suy89/89 hoặc18/18 thành tính đầy đủ của validator/bộ test; mutant sống và giới hạn assertion đã nêu. Không đo được model/effort backend từ lời yêu cầu reviewer trong SPEC.

Còn một P3 nên chưa `approve`. Bản vá gợi ý đã cụ thể và kiểm áp; không tự áp vào cây nguồn, đóng băng, cấp lease hay merge. Tiếp tục theo trần10 và quy trình human audit đã được chủ kho quyết, không xin lại quyền review.
