verdict: approve
reviewed_spec_sha256: 9bc0fe282fbebc02791f47a30e4ff187b1182a2e5e357ee2e66c04d4f7dac7cd
reviewed_sha: 7fc28680dd79fd5088555cd393bda380581e4aac
P1: 0   P2: 0   P3: 0
reviewer_provider: openai_codex
model_tu_khai: GPT-6 (Codex); biến thể/effort backend KHÔNG ĐO ĐƯỢC

Review độc lập lượt **7/10**, bản nháp 7. Đã ghi VERDICT sơ bộ trước khi chạy và cập nhật bằng kết quả thực đo. Phạm vi: delta nháp 6 → 7 và hệ quả; không phải nghiệm thu implementation A1a r2.

**F16 ĐÓNG. Không tìm thấy P1/P2/P3 còn lại hoặc finding đã đóng bị delta tái mở.** Tự kiểm **31/31**, ma trận **21/21 khớp + gốc**; cả ba bản in chạy lại giống từng byte hiện vật cung cấp. `HINT.patch` rỗng.

Giữ nguyên `cay-kho/`, SPEC, script và các hiện vật đầu vào. Giữ các quyết định prediction-only, Q6 cây mốc + (b), ngoại lệ ADR-0044 ≤3 tệp/≤663 dòng thêm và trần10. `approve` này cho phép chuyển sang human audit đã được chủ kho quyết; không thay thế human audit, đóng băng, cấp lease hay merge.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Finding | Trạng thái | Bằng chứng chạy được trong lượt này |
|---|---|---|
| **F16 — `tham-chieu-vi-tri-bang-sai`**, finding duy nhất lượt6 | **ĐÓNG** | `python3 -B scratch/review7.py`: áp `luot6-HINT.patch` vào bản sao `SPEC.truoc.md` bằng `patch -p0`, rc0; băm kết quả `f8c0d3fbc21424b72e9f0924a1a809dc169fc0109ebbd7517be1e008166a996e`, đúng lượt6/E20. SPEC:358 nay gọi đích danh hai hàng, không còn “hai dòng cuối”. Bảng mới có21 hàng; hai hàng được gọi tên hiện ở vị trí18 và20, đều tồn tại đúng một lần. `scratch/measure.json`, `scratch/coverage-delta.json`. |
| **F2 — `mien-lich-su-vuot-quyet-dinh`**, từng ĐÓNG-MỘT-PHẦN, đã đóng lượt5 | **ĐÓNG**, không tái mở | §0–7 bằng từng byte bản trước; mốc là tổ tiên HEAD và origin/master, giờ commit bằng C. Walker độc lập dựng11 cặp, digest đúng, giữ0. Mutant đọc HEAD vẫn chỉ làm đỏ `cay-sau-khong-doi-cay-moc`. `scratch/review7.py`, `scratch/independent-walker.json`, `scratch/mutations.log`. |
| **F11 — `q6-thieu-kiem-id-ten`**, từng ĐÓNG-MỘT-PHẦN, đã đóng lượt5 | **ĐÓNG**, không tái mở | AST mọi hàm ngoài `tu_kiem` của `do_q6.py` không đổi, gồm toàn bộ `dan_xuat`. Suite31 giữ các ca kiểm ID/tên/schema; walker kiểm89 tệp thật và bốn trường được đọc. Probe CLI riêng kiểm biên hợp lệ/tràn ở helper thật. `scratch/measure.json`, `scratch/self-check.log`, `scratch/own-probes.json`. |
| F12/F13 — `q6-thieu-kiem-id-ten` | **ĐÓNG**, không tái mở | Các ca miền ID/null/khoá không giá trị vẫn rc3; hai ca tràn UTC vẫn rc3, không crash. Probe CLI riêng tái đo hai ca tràn và bốn biên hợp lệ; mutant từng năm bị đúng ca mới bắt. `scratch/self-check.log`, `scratch/mutations.log`, `scratch/own-mutations.json`, `scratch/own-probes.json`. |
| F14 — `loi-khai-co-lap-fixture-sai` | **ĐÓNG**, không tái mở | SPEC:320–322 vẫn khai chốt che nhau. Mutant đơn miền ID chỉ đỏ ca đứng riêng; mutant ba miền đỏ đúng5 ca. Bỏ riêng chốt thư mục vẫn có tập đích rỗng được khai rõ. Ma trận thực đo khớp lời văn; không có lời khai mới rằng mọi fixture chỉ vi phạm một chốt. |
| F15 — `tham-chieu-lua-chon-da-xoa` | **ĐÓNG**, không tái mở | Toàn bộ §8.3 trở đi bằng từng byte bản trước; điều kiện cấp lease tiếp tục dẫn tới ngoại lệ đã quyết, không quay lại lựa chọn “(a) hoặc (b) ở mục 1”. Assertion trong `scratch/review7.py`. |

Đã rà nhãn ĐÓNG-MỘT-PHẦN trong cả sáu verdict trước: chỉ F2/F11 từng mang trạng thái này; cả hai đã đóng ở lượt5, không có tồn dư khác cần quyết lại.

Các finding đã đóng khác không bị delta tái mở:

- **F1/F3:** quyết định prediction-only và luật ba trạng thái giữ nguyên (§0–7 byte-equal; `dan_xuat` AST-equal). Ca một chiều, thay tiếp, hết hạn vẫn đạt.
- **F4/F5/F7/F8/F9/F10:** §0–7 và blob cổng, test, workflow, spec cha không đổi giữa hai reviewed head. OID đầy đủ ở `scratch/measure.json/unchanged_blobs`. Đây là kiểm không hồi quy do delta, không nhận là chạy lại toàn bộ A18/M14.
- **F6:** số nền tại `24c48e28` không bị sửa. Các số mới31/31,21/21, băm hai script và tổng ước422–663 đều đo khớp.

## Findings

**Không có P1/P2/P3.** F16 đã sửa đúng. Lời văn mới về vị trí hạn biên, số lease hợp lệ và tập đích mutant khớp mã và bản in.

Giới hạn bao phủ tìm được bằng mutant riêng được ghi ở phần Nghiệm thu; không có lỗi mã gốc hoặc lời khai bao phủ tương ứng bị bác bỏ, nên không nâng giới hạn ấy thành finding.

## Bảng đo lại

| Lời khai / đối tượng | Thực đo | Bằng chứng / giới hạn |
|---|---|---|
| SPEC và reviewed SHA | **400 dòng, 50.574 B**, băm đúng header | Bằng blob reviewed SHA và bản trong mirror; `scratch/measure.json` |
| `do_q6.py` | `36d8f1667aaa72a1bf00dfb7d1ded4331cb65efab5a0376bb3506528fd6d89d0` | Khớp SPEC và blob commit |
| `mut_q6.py` | `272dc1e82a32331348f59c182803c7cada373f98fbbdd6d4f91ce40d6641e794` | Khớp SPEC và blob commit |
| Tự kiểm | **31/31**, rc0 | `scratch/self-check.log`, byte-equal bản cung cấp; stderr rỗng |
| Ma trận đột biến | **21/21 khớp + gốc**, rc0 | `scratch/mutations.log`, byte-equal; không Traceback |
| Mutant phía soạn làm đỏ suite / sống | **20 / 1** | Mutant bỏ riêng chốt thư mục có tập đích ∅, rc0 đúng khai; 21/21 là số tập khớp, không phải21 mutant bị giết |
| JSON cây thật | **byte-equal**, rc0 | `scratch/q6-rerun.json`, sha256 `1fc99cd9339fb5f085436e60ef39bac3058a79dbc009161597ecc7bc85efbd61` |
| Miền / hợp lệ / ngoài miền | **89 / 89 / 3** | Walker độc lập; ba tệp ngoài miền là `.yaml.nhap` |
| Cặp hai chiều / một chiều | **11 / 3** | Cặp, path và OID hai đầu khớp bản in |
| Digest tuple4 | `8f372ccd2ceab70901868a58d3380acbd89dce25c7127d4d514bc959270fef48` | Tự dựng cặp theo chiều cũ→mới, sort rồi JSON compact |
| Vi phạm / KXD / giữ lại | **0 / 0 / 0** | 11 đầu mới đều hết hạn tại C |
| Hạn muộn nhất | `2026-09-08T10:17:12+00:00` | `scratch/independent-walker.json` |
| C = giờ commit mốc | `2026-09-10T11:55:37+07:00` = `2026-09-10T04:55:37Z` | Ancestor HEAD và origin/master đều rc0 |
| Tổng ước dòng thêm | **422–663** | Cộng độc lập7 hàng; không phải numstat implementation |
| Mirror | **438/438**, tên và OID bằng nhau | So cache với bare cục bộ; không phải quảng bá máy chủ mạng |
| origin/master cục bộ | `eb32b50e40d1b9ee006e057c2f9afc188283af56` | Khớp `.mirror-info`; không dùng làm nguồn Q6 |
| Probe CLI riêng | **10/10** | `scratch/own-probes.json`; cả rc, số lease và tập giữ đúng; giờ commit fixture bằng C |
| Tự đột biến | **8 biến thể nháp7 + 1 đối chứng nháp6**, đúng tập dự đoán | `scratch/own-mutations.json`; không crash, đủ31/30 ca tương ứng |

Không dùng438 ref của mirror để bác bỏ428 ref lịch sử ở §1. Header “đã dùng6/10” mô tả trước lượt gọi7 này.

## Nghiệm thu

**Delta mã dẫn xuất bằng0.** Mọi hàm trong `do_q6.py` ngoài `tu_kiem` giữ nguyên AST. `DIFF.truoc-nay.patch` bằng Git diff ba tệp tại đúng hai commit. Trong bộ ca thường:28 ca chung không đổi AST, bỏ một ca `han-bien-hop-le`, thêm hai ca biên trên/dưới; cộng ca cây sau riêng thành31. `scratch/coverage-delta.json` lưu các assertion.

Hai ca mới đặt hạn ở đầu mới `y`, đúng quan hệ hai chiều `x→y`. Ca năm9999 đòi rc0, giữ `(x,y)`; ca năm1 đòi rc0, giữ rỗng. Cả hai đòi `lease_hop_le == 2` ở `do_q6.py:209–221`. Phần tử thứ4 tùy chọn không làm đổi cách xét28 ca chung.

**Tập đích mới/đổi khớp lời khai:**

| Mutant phía soạn | Tập HONG thực đo | rc |
|---|---|---:|
| `tu-choi-nam-bien` | `{han-bien-tren-hop-le, han-bien-duoi-hop-le}` | 1 |
| `bo-qua-im-lang-tep-han-bien` | `{han-bien-tren-hop-le, han-bien-duoi-hop-le}` | 1 |
| `bo-loc-han` | `{het-han, han-bang-dung-C, han-bien-duoi-hop-le}` | 1 |
| `bo-rieng-chot-thu-muc-con` | ∅ | 0 |

Các hàng còn lại cũng khớp đầy đủ ma trận khai trước. E20 về kết quả cuối tái tạo được; không chứng nhận lịch sử lần đo đầu LỆCH của phiên soạn.

**Tự đột biến bản sao:** `scratch/probes7.py` ghi dự đoán vào `scratch/own-mutation-targets.json` trước khi chạy; mã từng mutant, stdout và stderr lưu ở `scratch/own-mutants/`.

| Mutant reviewer | Thực đo trên suite31 | Ý nghĩa |
|---|---|---|
| Bỏ qua riêng năm1 / riêng năm9999 | Chỉ ca biên dưới / biên trên HONG | Hai ca tách biệt bắt được từng biên |
| Từ chối riêng năm1 / riêng năm9999 | Chỉ ca biên dưới / biên trên HONG | Không bị một biên che biên kia |
| Bỏ qua cả hai năm | Đúng hai ca biên HONG | Cùng mutant sống30/30 trên nháp6; delta đã đóng khoảng trống chỉ ra lượt6 |
| Bỏ qua hai năm **và** bỏ phép kiểm số lease | Chỉ ca biên trên HONG | Ở biên dưới, tập giữ vẫn rỗng; assertion mới về số lease là chốt phân biệt việc bỏ tệp |
| Chỉ bỏ phép kiểm số lease | Sống31/31 | Mã gốc vẫn trả đúng số; phải ghép với hành vi sai mới quan sát được đóng góp của assertion |
| Chỉ bỏ tệp hạn biên khi nó ở đầu cũ có bia mộ, không khai thay thế | Sống31/31 | Hai ca mới đặt hạn ở đầu mới; chưa phủ biến thể chỉ làm sai đầu cũ |

**Giới hạn được đo, không phải finding:** mutant cuối làm mất cặp trong ba probe riêng `old-upper`, `old-lower`, `both-extremes`: mã gốc rc0,2 lease hợp lệ, giữ `(x,y)`; mutant rc0,1 lease hợp lệ, giữ rỗng. Mã gốc xử lý đúng cả đầu cũ lẫn đầu mới. Spec khai rõ hai ca mới ở **đầu mới** và một mutant bỏ tệp biên không phân biệt vị trí; các lời khai này đều đúng. Không có cam kết rằng31 ca giết mọi mutant theo vị trí, cũng không có hồi quy mã dẫn xuất. Không cộng mutant riêng vào số21/21 và không yêu cầu kéo dài vòng review chỉ để đạt bao phủ vô hạn.

Mười probe gọi CLI thật trên kho Git thường, dùng bản sao nguyên văn helper `ops/lease_publish.py`: bốn hạn biên hợp lệ (Z/offset), hai tràn UTC, hạn=C, hai biên ở đầu cũ, và hai đầu cùng sát biên. Assertion so rc, số lease và tập giữ; hai ca tràn còn đòi không crash. Clock commit fixture được ghim đúng C và kiểm lại.

Walker độc lập dùng `git ls-tree -rz`, `yaml.safe_load` và helper chuẩn hoá được hợp đồng chỉ định; tự kiểm schema và dựng cặp theo chiều cũ→mới, không gọi `dan_xuat` để dựng cặp/digest. Tính độc lập không bao gồm viết lại parser YAML hoặc helper thời gian.

## Phản chứng đã chạy

Sau lần đọc prompt snapshot do người dùng chỉ định, mọi đọc/ghi phục vụ review ở trong cwd; không dùng mạng. Git cô lập bằng `scratch/env.sh`: `GIT_CONFIG_NOSYSTEM=1`, global config rỗng dưới scratch, `GIT_OPTIONAL_LOCKS=0`, TMPDIR dưới cwd; Python không ghi bytecode. Không fetch hoặc gọi remote mạng. Bare `kho.git` chỉ đọc bằng `for-each-ref`. Kho fixture và mọi bản đột biến nằm dưới scratch.

Các lệnh tái chạy từ cwd:

```sh
mkdir -p scratch/tmp scratch/m
. scratch/env.sh
python3 -B do_q6.py --tu-kiem cay-kho > scratch/self-check.log 2> scratch/self-check.err
python3 -B mut_q6.py scratch/m cay-kho do_q6.py > scratch/mutations.log 2> scratch/mutations.err
python3 -B do_q6.py cay-kho 072181157a27804e69deb35bb792a88c70ac31e3 2026-09-10T04:55:37Z > scratch/q6-rerun.json 2> scratch/q6-rerun.err
python3 -B scratch/review7.py
python3 -B scratch/probes7.py
git -C cay-kho status --porcelain --untracked-files=all
```

Các tiến trình chính đều rc0; `review7.py` in `REVIEW7_OK`, `probes7.py` in `PROBES7_OK`. Các tiến trình mutant có rc0/1 đúng tập đích đã lưu, không dùng crash lấy tín dụng. `review7.py` chỉ được chạy lại sau khi thêm assertion kiểm delta fixture/bảng; không thay nguồn rồi lặp tới xanh.

`HINT.patch` **0 B**, sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Không có finding cần hunk vá. Hint lượt6 chỉ được áp vào bản sao `scratch/hint6/SPEC.md`; không áp vào nguồn.

## KHÔNG ĐO ĐƯỢC

- Không xác minh nguồn mạng: comments/tags, advertisement máy chủ, PR/merge hoặc thời điểm chạy phía soạn. E21 về CI/billing chưa kiểm chứng và không dùng làm bằng chứng review.
- Tái tạo được kết quả áp hint6 và ba bản in; không chứng nhận lịch sử thao tác, thời điểm hoặc lần ma trận LỆCH được E20 kể lại.
- Không chạy suite168, CI, actionlint/shellcheck hoặc toàn bộ nghiệm thu implementation A1a r2. Phần đã đóng ngoài delta được kiểm không hồi quy qua nội dung và OID.
- Các hướng cần tự soạn nội dung nhạy cảm chỉ mô tả bằng lời: đường thoát cây; tên đồng tự Unicode; đường dẫn khiến Git xuất dạng quote/escape; helper hoặc object Git giả. Không dựng payload hoặc chạy các hướng ấy; không nhận tín dụng kiểm thử. Bộ đọc đường dẫn không đổi trong delta.
- Suite31 vẫn chỉ so tập giữ ở ca kỳ vọng rc0; ca rc3 chỉ so mã thoát, trừ các probe riêng đã mô tả. Assertion số lease hiện áp cho hai ca biên mới. Không suy31/31 hay21/21 thành tính đầy đủ của bộ test; mutant sống và giới hạn đã ghi ở trên.
- Không đo được biến thể/effort backend. Tên model reviewer được SPEC yêu cầu không phải bằng chứng model thực tế.
