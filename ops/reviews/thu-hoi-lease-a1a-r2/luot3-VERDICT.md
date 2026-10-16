verdict: changes_requested
reviewed_spec_sha256: fb67bebd45c744ac7d93a85855b6fddb9451a54f3a541e01fa4359108d6217c5
reviewed_sha: 79b8ec7b71b04f7b9bdaffebe930fbb9965cd118
P1: 1   P2: 0   P3: 0
reviewer_provider: openai_codex
model_tu_khai: GPT-6 (Codex); biến thể/effort backend KHÔNG ĐO ĐƯỢC

Review độc lập bản nháp 3, lượt 3/4. Bản ghi sớm đã được tạo trước khi chạy phản chứng và bổ sung trong lượt này. Phạm vi chính là delta nháp 2 → nháp 3. Đây là review đặc tả và hiện vật Q6, không phải nghiệm thu implementation A1a r2.

F8–F10 đã đóng. F11 sửa đúng phần lớn chốt nhưng còn hai đường nhận schema sai, gộp thành **F12, cùng lớp `q6-thieu-kiem-id-ten`**. Các số đo mới, digest, E13 và E14 cục bộ đều khớp. Không mở lại quyết định nguồn Q6/clock hoặc prediction-only của chủ kho; không tăng bộ đếm F1 thành lần 8.

`SPEC.md`, `do_q6.py`, JSON gốc và `cay-kho/` được giữ nguyên. Chỉ ghi đầu ra trong cwd/`scratch/`. HEAD/tree mirror: `79b8ec7b71b04f7b9bdaffebe930fbb9965cd118` / `9ebb77ebae41053e6770b71dba78364d90c8cff8`.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Các lệnh dưới đây chạy từ cwd bằng `python3 -B`. Các harness tự đặt Git global config rỗng trong `scratch/`, bỏ system config và dùng TMPDIR trong cwd. `review_m14.py` là **mô hình hợp đồng mới** gắn vào CLI thật; không nhận mô hình là mã r2 đã ship.

| Finding | Trạng thái | Bằng chứng chạy được và giới hạn |
|---|---|---|
| F8 — `dot-bien-khong-khop-seam-consumer` | **ĐÓNG** | SPEC:181–184,197–201,232 tách rõ seam. `python3 -B scratch/review_m14.py` → `scratch/m14-review.json`: A22iii-unit trả `KHONG_XAC_DINH`; cùng kho, baseline/ứng viên không cờ/có cờ đều rc12, cùng dãy dòng không dự báo và stderr; `helper_called=false`. Mutant làm tròn trạng thái chỉ đổi màu iii-unit, không iii-cli. Không stub scanner hoặc nuốt Chan. |
| F9 — `du-bao-ba-trang-thai-mo-ho` | **ĐÓNG** | SPEC:186–195 chốt ưu tiên lỗi trước tồn tại cặp, định nghĩa mâu thuẫn bằng mapping và kiểm cả L/N. Cùng harness: A22iv-L và A22iv-N đều KXD dù có cặp đối xứng; bỏ kiểm trùng L chỉ giết iv-L, bỏ kiểm trùng N chỉ giết iv-N. A19/A21 là CHE; A20, ID vắng và N không bia mộ là KHONG. YAML không gán được ID trả KXD ở unit. |
| F10 — `thieu-nhanh-nghiem-thu` | **ĐÓNG** | SPEC:229 dùng ba lần chạy, dãy dòng/stderr/rc và baseline A16 bất biến; :236–240 khai tập đích. Harness nạp mã baseline từ OID `24c48e28bacd2c835e6acf7df64c7ee60ae6d424`, ghim map ref/clock cho cả ba lượt. A19 control rc11, `NGƯỜI_GIỮ 1: L`, dãy dòng bằng nhau. Lặp dòng, đảo thứ tự hoặc đổi đầu ra ở cả hai chế độ đều bị bắt. Mutant hỏi mọi ref giết đúng A20+A22(i); mutant đại diện giết đúng A21. |
| F11 — `q6-thieu-kiem-id-ten` | **ĐÓNG-MỘT-PHẦN** | `scratch/self-check.log`: 13/13. `python3 -B scratch/review_q6.py` → `scratch/q6-review.json`: sai tên cả đầu mới, non-map, thiếu/sai kiểu ID, trùng, thư mục con, sai kiểu thay thế đều có chốt; .yml hợp lệ và .yaml.nhap ngoài miền. Bảy mutant đều đúng một ca HONG, không Traceback. Tuy nhiên miền ID đã bị thu hẹp thành phép thử “khác rỗng”, và null bia mộ vượt chốt kiểu; xem F12. Không thể đóng toàn bộ lời khai “script khớp §8.2”. |
| F2 — `mien-lich-su-vuot-quyet-dinh` | **ĐÓNG-MỘT-PHẦN** | Quyết định Q6 tree + (b), mốc và clock vẫn **đóng đúng**: `scratch/scope-review.json` xác nhận dòng quyết định không đổi, mốc là tổ tiên cả HEAD lẫn origin/master. Mutant đọc HEAD chỉ giết ca cây sau; walker độc lập vẫn ra 11 cặp rồi giữ0. Phần hợp đồng kiểm ID/tên của Q6 còn tồn dư F11/F12, nên chưa đóng toàn bộ. Không yêu cầu chủ kho quyết lại nguồn/clock. |

Các finding lượt 1 đã đóng **không bị tái mở**:

- **F1:** dòng quyết định không đổi; M14 vẫn chỉ dự báo. Mô hình giữ holder/rc/dãy dòng baseline, gồm khi đọc cache không đủ dữ liệu.
- **F3:** thứ tự hết hạn → bia mộ không đổi. `new-one-way-live` rc3; `new-one-way-expired` rc0 giữ0; `replaced` chỉ giữ y→z; vòng đối xứng hữu hạn giữ0. Không bỏ trạng thái thứ ba.
- **F4:** A18 giữ nguyên từng byte so nháp2; vẫn có control đầy đủ và yêu cầu đúng Chan12, không nhận TypeError làm bằng chứng.
- **F5:** A4 và A7 giữ nguyên từng byte, không mất nhánh hai khoá hoặc hai đầu cặp.
- **F6:** các số nền vẫn neo B bất biến; E13 không đổi năm tệp liên quan. Số mới §8.2 được đo độc lập ở bảng dưới, không tái dùng đơn vị “92 lease”.
- **F7:** A16 giữ nguyên từng byte, vẫn diff theo `base_sha` bất biến, không theo master động. Master thực tế đã tiến độc lập nhưng các blob nền liên quan bằng nhau.

Đối chiếu tĩnh có assertion chạy được: `python3 -B scratch/check_scope.py` → `scratch/scope-review.json`. Không nhận việc giữ nguyên hợp đồng là đã chạy lại mọi suite của r1/r2.

## Findings

### F12 — P1 — `q6-thieu-kiem-id-ten` — tồn dư F11

**Vị trí:** SPEC:287,296,299–300,303–310; `do_q6.py:64–76,98–106`; luật Q6 cha `cay-kho/ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md:377–380`; miền ID hiện hành `cay-kho/ops/lease_publish.py:125,861–863`.

**1. Miền ID chưa được kiểm.** Bản nháp 3 thay yêu cầu kiểm miền ID bằng “chuỗi khác rỗng”. `LEASE_ID` không phải khái niệm chưa có định nghĩa: cổng khai `^[A-Za-z0-9._-]+$` ở dòng125 và từ chối ngoài miền ở dòng862. Script chỉ kiểm `isinstance`/`strip`, rồi so tên. Một ID ASCII thông thường có dấu cộng, `x+y`, với tên tệp tương ứng, vượt cả hai chốt dù không phải ID hợp lệ của cổng. Đây là thiếu kiểm ID trong Q6; không đề nghị mở rộng schema hay đổi nguồn hằng.

**Đã chạy:** `python3 -B scratch/measure_review.py`, kết quả đầy đủ `scratch/id-domain.json`. Dựng hai kho Git thường độc lập, một lần đầu cũ mang ID ngoài miền, một lần đầu mới; các tệp vẫn đúng tên, cặp hai chiều và đầu mới còn hạn:

```text
ID x+y ở đầu cũ: gate LEASE_ID.fullmatch=False; script rc0, giữ (x+y,y)
ID x+y ở đầu mới: gate LEASE_ID.fullmatch=False; script rc0, giữ (x,x+y)
```

Hai fixture dùng dấu cộng ASCII, không có đường thoát cây, đồng tự Unicode hay payload chuỗi thoát. `dan_xuat` chính script được gọi trực tiếp; kho và OID đều ghi trong JSON.

**2. Có khoá `null` bị coi như vắng khoá.** SPEC:300 và docstring script yêu cầu `da_bi_thay_the` **vắng hoặc là chuỗi khác rỗng**. `d.get(...)` kết hợp `if t is not None` nhập hai trạng thái thành một. YAML `da_bi_thay_the: null`, hoặc khoá không có giá trị, trả None; script không báo vi phạm và phân loại đầu mới là `CON_HIEU_LUC`.

**Đã chạy:** `python3 -B scratch/review_q6.py`, JSON `scratch/q6-review.json`, CLI thật của script trên các kho Git thường. Các fixture null có giờ commit đúng C đang truyền:

| Ca | Thực tế bản nháp3 | Hợp đồng §8.2 |
|---|---|---|
| Sạch, đầu mới không có khoá bia mộ | rc0, giữ x→y | Đúng |
| `null-new`: đầu mới có khoá mang null | **rc0, vi_pham=[], giữ x→y** | rc3 |
| `blank-new`: khoá bia mộ không có giá trị | **rc0, vi_pham=[], giữ x→y** | rc3 |
| `null-unpaired`: thêm z có bia mộ null ngoài cặp | **rc0, vi_pham=[], giữ x→y** | rc3 vì kiểm mọi tệp trong miền trước lọc |
| Chuỗi rỗng/số/danh sách ở cùng trường | rc3 | Đúng; cho thấy null là nhánh bị bỏ sót |

**Vì sao P1:** có đầu vào vi phạm miền/schema bắt buộc vẫn được nhận rc0 và đưa vào tập cặp dùng làm bằng chứng ghim; đồng thời script trực tiếp lệch luật “vắng hoặc chuỗi khác rỗng ⇒ rc3”. Đây là fail-open của validator Q6, không phải lỗi chữ nghĩa. Hai biểu hiện thuộc cùng phần kiểm ID/schema còn thiếu của F11, nên chỉ đếm **một** finding. Không cáo buộc M14 đã được cấp lại quyền xoá holder.

**Ảnh hưởng trên cây thật:** không làm sai các số production đã khai. Bản vá thêm hai chốt vẫn cho JSON **byte-equal**, 11 cặp và hằng rỗng. Không có căn cứ nói digest `8f372ccd…` sai; cũng không lấy việc cây thật tình cờ sạch để chứng minh validator đầy đủ.

**Sửa:** quy định miền ASCII cụ thể của `LEASE_ID`, kiểm cả hai đầu trước dẫn xuất; kiểm sự có mặt của khoá `da_bi_thay_the` độc lập với giá trị, từ chối explicit null. Thêm năm ca âm: ID ngoài miền ở hai đầu, null ở đầu mới/tệp ngoài cặp, khoá không giá trị; giữ đối chứng sạch có khoá vắng. Ghi ma trận đúng tập đích và cập nhật băm script/ngưỡng tự kiểm.

`HINT.patch` chứa hunk cho SPEC và script. Bản sao vá đã chạy **18/18**; bảy mutant cũ vẫn mỗi cái đúng một ca, bỏ miền ID giết đúng hai ca, coi null như vắng giết đúng ba ca; **9/9**, không Traceback. Băm script gợi ý: `7402a0bdb78821cb0fb3b6e9a8a8ba5e2285bb1a615176653ebdcaa506b229cf`. Đây là bản vá gợi ý đã kiểm trong scratch, chưa áp vào tệp được review hoặc mirror.

## Bảng đo lại

Hiện vật chính: `scratch/measure-review.json` (thời điểm `2026-09-26T23:31:07Z`), `scratch/q6-rerun.json`, `scratch/scope-review.json`. Walker độc lập đi **cũ→mới**, khác chiều vòng lặp mới→cũ của script.

| Lời khai | Kết quả đo | Bằng chứng |
|---|---|---|
| SPEC 350 dòng, băm `fb67bebd…` | **350 dòng, 41.550 B**, full băm như header; bằng blob SPEC tại reviewed SHA | measure-review/files, spec_matches_head=true |
| Script băm `f20c0a1a…` | `f20c0a1a45db2f604cac81ec221ab1bcc873041870f8465060a3d8dbea026d46`; 198 dòng, 9.751 B; bằng blob tại HEAD | measure-review/files, script_matches_head=true |
| JSON băm `1fc99cd9…` | `1fc99cd9339fb5f085436e60ef39bac3058a79dbc009161597ecc7bc85efbd61`; 6.128 B; bằng blob tại HEAD | measure-review/files, json_matches_head=true |
| Chạy lại Q6 | rc0, byte-equal JSON cung cấp | `cmp scratch/q6-rerun.json q6-do-2026-09-26.json` rc0 |
| 89 miền lease /89 hợp lệ /3 ngoài miền | **89/89/3**; cả ba ngoài miền có đuôi .yaml.nhap; kiểm độc lập ID/miền/tên trên nguồn thật không thấy lỗi | measure-review/independent_q6; script vá vẫn rc0 |
| 11 hai chiều /3 một chiều /0 KXD | **11/3/0**; (b) giữ **0** | walker độc lập + q6-rerun |
| Digest tập cặp | `8f372ccd2ceab70901868a58d3380acbd89dce25c7127d4d514bc959270fef48` | walker tự tạo sorted tuple4 và JSON compact, cùng băm |
| Hạn muộn nhất | `2026-09-08T10:17:12Z` | độc lập đọc 11 hạn; clock probes script |
| Giờ commit Q6 | `2026-09-10T11:55:37+07:00` = `2026-09-10T04:55:37Z` | git show -s --format=%cI |
| Biên hạn | 10:17:11 giữ1; 10:17:12 giữ0; giờ mốc và năm2099 giữ0; mọi lần rc0/KXD0 | scope-review/clock_probes_script |
| Mốc là tổ tiên | rc0 trên cả reviewed HEAD và origin/master hiện tại | scope-review/ancestry_rc, đọc trực tiếp subprocess returncode |
| E12 tự kiểm | **13/13**, rc0 | self-check.log |
| E12 bảy mutant | **7/7**, mỗi cái một HONG, rc1, không Traceback | q6-review/mutants; từng bản sao và log ở scratch |
| E13 master | `refs/remotes/origin/master=68b552d0f08200ba860ea788517558a4172df384`; commit message merge #653, giờ `2026-09-26T23:11:08Z` | measure-review/master_commit; mirror không có refs/heads/master riêng |
| E13 không chạm write set và hai tệp bổ sung | Diff B→master đúng 6 đường, giao với 5 đường E13 là rỗng; **5/5 blob bằng nhau** | measure-review/e13 |
| Số nền vẫn neo B | lease_publish.py 2047; test 7288; admission workflow178 | measure-review/baseline_lines |
| E14 435 head | **435/435**, hiệu tập tên hai chiều rỗng; OID của bare local và cache cũng bằng nhau | measure-review/e14; endpoint chính cwd/kho.git |
| Hint áp được | patch -p0 rc0 trên bản sao; hai tệp kết quả bằng đúng bản đã kiểm | scratch/patch-validation.json |

Sáu đường master đã đổi: `.claude/dev/ci_dang_ky_test.py`, `.claude/hooks/subagent_ghi_detect_test.py`, `.github/workflows/ci-dot-bien-du.yml`, hai lease `ci-registry-pretooluse-che-do-nhe-r1-g1-claude.yaml`/`ci-registry-thu-hep-vung-r1-g1-claude.yaml`, và `ops/specs/CI-REGISTRY-THU-HEP-VUNG-r1.md`. Không chạm ba đường write set A1a, `.github/workflows/ci.yml`, hoặc spec cha.

Tính ổn định clock trên cây thật không chỉ là lấy mẫu: 11 cặp cố định, mọi hạn ≤ `2026-09-08T10:17:12Z`, thuật toán kiểm hạn trước bia mộ; do đó mọi C hợp lệ ≥ biên này loại cả 11. Không dùng thời gian chạy thay clock ghim.

## Nghiệm thu

**M14:** `scratch/review_m14.py` tạo kho Git thường và bare local, không stub scanner. Nạp baseline từ B bất biến; nạp CLI ứng viên hiện tại rồi thay riêng helper dự báo bằng mô hình phân loại nháp3. Clock được ghim như nhau ở cả hai module; map ref không đổi giữa ba lượt. Tập đích nằm trong biến `declared` trước vòng chạy; assertion đòi bằng tập thực đo. `scratch/m14-review.json` giữ stdout/stderr/rc và cờ quan sát helper.

| Mutant mô hình | Ca đổi màu thực đo |
|---|---|
| Control | Rỗng; mọi ca control đạt |
| CHE thì bỏ holder khỏi dữ liệu scanner | A19, A21 |
| Bỏ toàn bộ dòng trạng thái | A19, A20, A21, A22(i), A22(ii), A22(iv-L), A22(iv-N) |
| Tìm cặp trên mọi ref | **A20, A22(i)** |
| Hỏi đại diện muc['ref'] | **A21** |
| Chỉ hỏi chiều ngược trên mọi ref | **A22(i)** |
| Làm tròn mọi KXD thành KHONG | A22(i), A22(ii), **A22(iii-unit)**, A22(iv-L), A22(iv-N) |
| Ném khi canonical vắng | **A22(ii)** |
| Bỏ kiểm mâu thuẫn L | **A22(iv-L)** |
| Bỏ kiểm mâu thuẫn N | **A22(iv-N)** |
| In lặp dòng không dự báo | A19 và các ca CLI còn tới helper |
| Đảo thứ tự dòng không dự báo | A19 và các ca CLI có dòng để đảo |
| Đổi đầu ra cũ ở cả hai chế độ ứng viên | A19 và tất cả ca CLI, kể cả A22(iii-cli) |

Các tập dùng chung không mâu thuẫn SPEC: A19 không còn khai “chỉ A19” cho mọi mutant; các điều “chỉ” ở mutant đại diện và trùng từng đầu đều khớp. Với mutant mọi ref, seam được ghi rõ là **tập tìm cặp**, còn kiểm schema/mâu thuẫn vẫn trên cây canonical. Không đổi toàn bộ phạm vi kiểm mâu thuẫn sang mọi ref rồi gán collateral cho đặc tả. Mutant không nhận tên ca.

A19 tự kiểm representative của blob bia mộ là `refs/remotes/origin/master`; A21 tự kiểm là `refs/remotes/origin/a-first`. Chốt baseline bắt được thay đổi chung mà phép so hai chế độ ứng viên bỏ lọt. Hai mutant đảo/thay dòng là biến đổi output quan sát của mô hình để kiểm sức phân biệt của tiêu chí; không khai đó là source mutation đã cấy vào production. Mutant in lặp thực sự in từ helper mô hình.

**Q6:** bảy mutant trên bản sao nháp3 cho ma trận:

| Bỏ chốt | Ca HONG duy nhất |
|---|---|
| Tên | sai-ten |
| Từ chối non-mapping | khong-phai-mapping |
| Trùng ID | trung-id |
| Kiểu thay_the_cho | thay-sai-kieu |
| rc3 cho KXD | mot-chieu-moi |
| Cây mốc, đọc HEAD thay | cay-sau-khong-doi-cay-moc |
| Hạn | het-han |

Mutant non-mapping bỏ việc ghi vi phạm nhưng giữ `continue` để mô phỏng **bỏ qua tệp sai**; không dùng AttributeError do gọi `.get` lên list làm tín dụng. Đây là bảy mutant reviewer tự soạn với nội dung lưu trên đĩa; E12 không cung cấp bản nguồn mutant để chứng minh chúng byte-identical với mutant của phiên soạn. Lời khai **có thể tái lập**, nhưng bảy ca không bao phủ F12.

Bản vá gợi ý thêm kiểm miền ID/null, năm ca và hai mutant; `scratch/hint-validation.json` lưu **18/18**, **9/9** cùng tập đích. `scratch/hint-q6.json` vẫn bằng JSON thật. Không thêm đường vào write_set A1a: sửa hiện vật review ở nhánh đặc tả như §3.

**Phần kế thừa:** không thấy delta tái mở A4/A7/A16/A18; không chạy lại toàn suite168, actionlint/shellcheck hoặc nghiệm thu schema v2 chưa tồn tại. A1–A18 ngoài delta giữ trạng thái review trước, không tự đổi thành pass implementation. Review này không cấp lease, không đóng băng, không merge, không cấp ngoại lệ ADR-0044.

## Phản chứng đã chạy

Thiết lập tái lập khi chạy lệnh riêng:

```sh
export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL="$PWD/scratch/empty.gitconfig"
export GIT_OPTIONAL_LOCKS=0
export TMPDIR="$PWD/scratch"
export PYTHONDONTWRITEBYTECODE=1
```

Tệp `scratch/empty.gitconfig` rỗng đã tạo trong lượt review. Các harness bên dưới tự đặt các biến cần thiết.

1. `python3 -B do_q6.py --tu-kiem cay-kho` → `scratch/self-check.log`, 13/13, rc0, stderr rỗng sau khi cô lập cấu hình Git.
2. `python3 -B do_q6.py cay-kho 072181157a27804e69deb35bb792a88c70ac31e3 2026-09-10T04:55:37Z` → `scratch/q6-rerun.json`, rc0; cmp với JSON cung cấp rc0.
3. `python3 -B scratch/review_q6.py` → `scratch/q6-review.json`, `scratch/q6-summary.json`: bảy mutant và 27 fixture Q6. Bao gồm ID/tên/kiểu/miền/trùng, hai chiều/một chiều, chuỗi thay tiếp/vòng, hạn đúng biên và tương đương múi giờ. Ma trận không dùng một lỗi bất kỳ thay cho rc3.
4. `python3 -B scratch/review_m14.py` → `scratch/m14-review.json`, ma trận có assertion toàn bộ tập đích; rc0. Unit/CLI tách riêng, baseline bất biến, preflight thật, bare local.
5. `python3 -B scratch/measure_review.py` → `scratch/measure-review.json` và `scratch/id-domain.json`: walker độc lập, băm/số dòng, E13/E14 và hai ca ID ngoài miền. rc0.
6. `python3 -B scratch/check_scope.py` → `scratch/scope-review.json`: hợp đồng đã đóng không đổi, probe clock trên cây thật và ancestry. rc0.
7. `python3 -B scratch/make_hint.py` → `HINT.patch`, `scratch/hint-validation.json`: kiểm bản vá18/18, chín mutant, production byte-match. rc0.
8. `patch --dry-run -p0 < HINT.patch` rc0. Áp thật vào `scratch/hint-apply/` cũng rc0, kết quả byte-equal các bản sao đã kiểm; `scratch/patch-validation.json`.

**Giới hạn các probe bổ sung:** hai probe hạn sai định dạng/thiếu múi giờ kết thúc rc1 với ValueError/TypeError; không được tính là ca rc3 đạt. Probe danh sách thay thế lặp cho tuple lặp. Những hành vi này đã có trong đường phân loại/vòng lặp của nháp2, không phải regression do delta nháp3; không dùng chúng để tái mở các finding đã đóng hoặc khai thêm kết luận về 11 cặp thật. Log giữ nguyên để không đánh đồng “đã chạy probe” với “đã đạt nghiệm thu”.

**Sự cố môi trường không tính là test pass:** lần tự kiểm đầu kế thừa cấu hình ký Git toàn cục; signer có sẵn tự thử gọi dịch vụ localhost và bị sandbox từ chối, commit rc128, runner Traceback. Không có kết nối thành công hoặc dữ liệu mạng dùng làm chứng cứ. Đã loại lần đó và chạy lại với Git config rỗng trong cwd; mọi fixture/mutant và bare origin dùng sau đó đều cục bộ. Không sửa cấu hình mirror.

**Hướng chỉ MÔ TẢ, không tạo payload:** đường thoát cây; tên đồng tự Unicode; tên/bytes cần chuỗi thoát; helper Git giả; object/cạnh Git giả. Các hướng này cần kiểm miền tên, phân tách output Git và xử lý trạng thái không đo được, nhưng không được nhận là đã thử trong lượt này. Phản chứng đã chạy dùng YAML thông thường, tên ASCII bình thường và object do Git thật tạo.

## KHÔNG ĐO ĐƯỢC

- Không readback GitHub/REST hoặc mạng: không chứng nhận lại Q1 tag, Q3 body/comment, danh tính/quyền người đăng, trạng thái PR #589 hay sự kiện merge trên máy chủ. E13 xác nhận được **nội dung đồ thị Git cục bộ** và thời gian commit, không thay API máy chủ.
- E14 chỉ đối chiếu mirror với **bare local** `kho.git`; không chứng minh cache là OID hiện tại của GitHub, không trao authority cho dự báo.
- M14 r2/schema v2 chưa có implementation để nghiệm thu; mô hình chứng minh tính khả thi và sức phân biệt tiêu chí. Chưa chạy full suite mới, delta actionlint/shellcheck, kích hoạt profile, CI/Windows, C1a1b hoặc đo numstat thi công.
- Không tái tạo snapshot428 ref/holder cũ, không chứng nhận lại kết quả168/168 lịch sử. Số nền ghi timestamp cũ không được đổi thành lời khai tại giờ review.
- Không đo được model variant/effort backend; header tự khai phần biết được, không lấy yêu cầu `gpt-6-astra/high` trong SPEC làm measurement.

`HINT.patch` không rỗng, bao phủ toàn bộ finding P1/P2 của lượt này. Executor cần áp/sửa trên nhánh hiện vật review, chạy lại và xin lượt cuối trên băm mới; verdict này vẫn là **changes_requested** cho đúng bản nháp3 đã đọc.
