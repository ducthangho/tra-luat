verdict: changes_requested
reviewed_spec_sha256: b8856466da6638054f1f379c6118176177efd0b3dbbdaad2c37b2210345f0190
reviewed_sha: 33e19c4121d32aeb4497c28214d7d3ffa20c9c08
P1: 1   P2: 0   P3: 1
reviewer_provider: openai_codex
model_tu_khai: GPT-6 (Codex); tên biến thể/effort backend KHÔNG ĐO ĐƯỢC

Review độc lập bản nháp 4, lượt **4/4 — CUỐI**. Bản ghi sớm được tạo trước các phép thử và bổ sung thành bản này. Phạm vi là delta nháp 3 → nháp 4 và hệ quả Q6, không phải nghiệm thu implementation A1a r2.

**24/24, 14/14, 89/89, digest và bản in cây thật đều đúng.** F12 đã sửa đúng hai lỗi ID/null. Còn một nhánh lỗi hạn mới được đưa vào thuật toán nhưng chưa quy về rc3 (F13), và một lời khai chữ nghĩa về tính cô lập fixture không đúng (F14). Không cáo buộc số liệu cây thật sai hoặc phát hiện quyền xoá holder mới. Không mở lại quyết định nguồn/clock Q6 hay prediction-only của chủ kho.

Giữ nguyên `SPEC.md`, `do_q6.py`, `mut_q6.py`, JSON cung cấp và `cay-kho/`. HEAD/tree đo được: `33e19c4121d32aeb4497c28214d7d3ffa20c9c08` / `fbffeaf828a2e0730d5b37835b533af2db83adb3`. Bản vá chỉ nằm trong `HINT.patch` và bản sao `scratch/hint/`.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Finding | Trạng thái | Bằng chứng chạy được |
|---|---|---|
| F12 — `q6-thieu-kiem-id-ten` | **ĐÓNG** | `python3 -B do_q6.py --tu-kiem cay-kho`: ID ngoài miền đứng riêng/cũ/mới đều rc3; ba ca bia mộ null/khoá không giá trị đều rc3; ca sạch vắng khoá vẫn rc0 giữ x→y. `scratch/self-check.log`. Chạy lại mutant miền ID, null và ghép ba miền cho đúng tập khai, không Traceback. |
| F11 — `q6-thieu-kiem-id-ten` | **ĐÓNG-MỘT-PHẦN** | Phần ID/tên và các tồn dư F12 đã đóng: non-map, thiếu/sai kiểu ID, tên sai, trùng ID, schema thay thế đều bị chặn. Probe riêng `name-new` rc3, `valid-yml` rc0, `subdir` rc3 trong `scratch/own-cases.json`; 89 tệp thật qua kiểm độc lập. Tuy nhiên lời khai validator khớp toàn bộ §8.2 vẫn còn nhánh hạn không trả rc3, F13. Giữ lớp cũ cho thiếu sót kiểm schema Q6; không đếm lại F12. |
| F2 — `mien-lich-su-vuot-quyet-dinh` | **ĐÓNG-MỘT-PHẦN** | Phần quyết định nguồn/mốc/clock tiếp tục **đóng đúng**: mục 0–7 byte-equal nháp3; mốc là tổ tiên HEAD và origin/master, cả hai rc0; giờ commit đúng C; mutant đọc HEAD giết đúng ca cây sau. Walker độc lập và script cùng cho 11 cặp rồi giữ0. Phần hợp đồng dẫn xuất đầy đủ còn F13, không phải lỗi chọn nguồn và không cần chủ kho quyết lại E8. |

Không có finding đã ĐÓNG nào bị delta tái mở:

- **F1:** quy tắc prediction-only, bất biến holder/rc, cấm dùng dự báo cấp lease và bộ đếm lần7 không đổi.
- **F3:** thử lại `mot-chieu-moi` rc3; `da-bi-thay-tiep` chỉ giữ y→z; probe riêng `oneway-expired` rc0 giữ0 và `cycle` rc0 giữ0. Hết hạn vẫn được xét trước bia mộ.
- **F4/F5/F7:** A18, A4/A7 và A16 giữ nguyên từng byte; không nới seam, bỏ nhánh hoặc đổi baseline thành ref động.
- **F6:** các số nền không đổi; số delta đo lại ở bảng dưới đúng. Không tái dùng đơn vị “92 lease”.
- **F8/F9/F10:** toàn bộ §5.1 và A19–A22 giữ nguyên từng byte so nháp3; mã cổng, test, workflow và spec cha cũng có blob OID bằng nhau giữa hai head. Không có thay đổi quay lại seam CLI/unit sai, hai trạng thái, hoặc so đầu ra thiếu baseline.

Phép đối chiếu tĩnh có assertion chạy được ở `python3 -B scratch/review4.py` → `scratch/measure.json` (`scope.before_section8_equal`, `scope.after_section8_2_equal` đều true). `scratch/unchanged-blobs.json` ghi OID bốn tệp; có thể đo lại bằng `git -C cay-kho rev-parse 79b8ec7b:<path> 33e19c41:<path>`. Đây là kiểm **không hồi quy trong delta**; không nhận là chạy lại các suite M14/A18 của lượt trước.

E15 về áp hint lượt3 cũng tái lập: `python3 -B scratch/final_checks.py` áp `HINT.luot3.patch` bằng `patch -p0` lên bản sao SPEC/script nháp3, rc0; băm script kết quả đúng `7402a0bdb78821cb0fb3b6e9a8a8ba5e2285bb1a615176653ebdcaa506b229cf`. Điều này xác nhận hunk và kết quả trung gian tái tạo được, không chứng minh lịch sử thao tác riêng của phiên soạn.

## Findings

### F13 — P1 — `q6-thieu-kiem-id-ten` — nhánh kiểm hạn mới còn lọt ngoại lệ

**Vị trí:** SPEC:287,296–303; `do_q6.py:91–95`; `cay-kho/ops/lease_publish.py:228–242`; EVIDENCE E15 gạch đầu dòng2. Dùng lại lớp của F11/F12 vì đây tiếp tục là thiếu nhánh kiểm schema trong cùng validator Q6, dù trường lần này là hạn.

§8.2 quy định hạn không đọc được bằng `_doc_han` ⇒ rc3; E15 còn nói rõ “hỏng ⇒ rc3, không Traceback”. Script chỉ bắt `lp.Chan`. `_doc_han` chuyển datetime có múi giờ sang UTC bằng `astimezone`; phép đổi này có thể ném **OverflowError** khi UTC nằm ngoài miền năm biểu diễn. Ngoại lệ ấy thoát khỏi `dan_xuat` và CLI.

**Phản chứng ASCII thông thường, kho Git thật:** x→y hai chiều, ID/tên/schema đều hợp lệ; chỉ thay hạn được quote của y. Gọi CLI thật, nạp bản sao nguyên văn `ops/lease_publish.py` cung cấp, không stub helper.

| Hạn của y | Bản nháp4 | Hợp đồng | Bản vá gợi ý |
|---|---|---|---|
| `9999-12-31T23:59:59-01:00` | rc1, stdout rỗng, `OverflowError: date value out of range` | rc3, có vi phạm hạn | rc3, JSON có vi phạm, stderr rỗng |
| `0001-01-01T00:00:00+01:00` | rc1, stdout rỗng, cùng ngoại lệ | rc3, có vi phạm hạn | rc3, JSON có vi phạm, stderr rỗng |

**Chạy lại:** `python3 -B scratch/additional_proofs.py` → `scratch/additional-proofs.json`; stdout/stderr riêng ở `scratch/cli-{upper,lower}-{original,hint}.{out,err}`. `scratch/review4.py` cũng gọi trực tiếp `dan_xuat` và lưu hai ngoại lệ trong `scratch/own-cases.json`. Cả hai hướng biên có đối chứng bản vá trên cùng kho/OID/clock.

**Vì sao P1 theo thang đề bài:** thuật toán được chỉ định không thực hiện nhánh bắt buộc “không đọc được ⇒ rc3”; lời khai E15 về xử lý lỗi không đúng ở một trường mới của delta. Đây là mâu thuẫn hành vi với hợp đồng dẫn xuất, **không phải** fail-open: thực tế rc1 vẫn là lỗi, không tạo tuple được chấp nhận. Không có bằng chứng hằng trên cây thật sai hay quyền production bị mở. Phân hạng không dựa vào phóng đại hậu quả đó.

**Sửa:** bắt riêng `OverflowError` ở seam gọi `_doc_han`, ghi vi phạm và tiếp tục kiểm cây để kết quả cuối rc3. Không làm tròn thành hết hạn/còn hạn và không sửa cổng production ngoài write set review. Thêm ca biên trên/dưới; mutant coi lỗi tràn như hết hạn phải giết đúng hai ca này, không nhận crash làm tín dụng. Cập nhật băm/ngưỡng/bản in của bản vá.

`HINT.patch` thực hiện sửa ấy. Bản sao vá đạt **26/26**, ma trận **15/15 + gốc sạch**, JSON thật byte-equal; băm script vá `957b6432e060eb125a7b3957ce79cbf0538ed6757ac7c3b0980453d36af23280`. Đây là kết quả reviewer trên bản vá, không thay số lịch sử 24/24 và 14/14 của bản nháp4.

### F14 — P3 — `loi-khai-co-lap-fixture-sai`

**Vị trí:** SPEC:312–313 (“Mỗi fixture chỉ vi phạm đúng một chốt”), đối chiếu :334; `do_q6.py:175–176,186–187`.

Lời khẳng định tuyệt đối này không khớp fixture/bản in. Chẳng hạn `id-ngoai-mien-cu` ghi **hai** vi phạm: miền ID ở x+y và miền tham chiếu ở y. `id-ngoai-mien-moi` cũng ghi hai. Chính bảng :334 đã giải thích hai chốt che nhau và cần mutant ghép. Ngoài ra `id-sai-kieu` còn thiếu hạn; bỏ riêng chốt ID vẫn bị tên/hạn chặn. Không phải mọi fixture đã được biến thành chỉ có một điều kiện sai.

**Bằng chứng chạy được:** `python3 -B do_q6.py --tu-kiem cay-kho` → `scratch/self-check.log`, hai dòng nêu trên chứa hai phần tử `vi_pham`; `python3 -B mut_q6.py scratch/m cay-kho do_q6.py` xác nhận bỏ riêng miền ID chỉ đổi `id-ngoai-mien-don`, trong khi mutant ba miền đổi cả hai ca đầu cặp.

**Vì sao chỉ P3:** 24/24 và tập đích 14/14 đều đúng; bảng ngay sau đã khai đúng cơ chế che. Đây là phát biểu chữ nghĩa quá rộng, không thêm quyền hoặc làm sai con số đo.

**Sửa:** bỏ câu tuyệt đối; nói tính phân biệt được chứng minh bằng **tập đích từng mutant**, ghi ngoại lệ fixture nhiều chốt. `HINT.patch` có hunk sửa câu này, không xoá các ca đầu cặp hữu ích.

## Bảng đo lại

Hiện vật: `scratch/measure.json`, `scratch/final-checks.json`, `scratch/q6-rerun.json`. Walker độc lập dùng `git ls-tree -rz`, đi chiều **cũ→mới**, tự xây tuple4 và băm; vẫn dùng parser/schema helper của cổng như đặc tả yêu cầu, không gọi `dan_xuat` để xây tập cặp.

| Lời khai | Thực đo | Bằng chứng/giới hạn |
|---|---|---|
| SPEC 379 dòng, sha256 `b8856466…` | 379 dòng, 44.759 B; đúng full băm header | Bằng blob SPEC tại reviewed SHA |
| Script `040bfd0d…` | `040bfd0df9273f810a7fd0f1b4a29b135addde847f621e795c50806f1fd4df9f` | 228 dòng, 12.183 B; bằng blob HEAD |
| Mutator `d74c282f…` | `d74c282fc62238e83d391cc91a8e087da653c3715a55077fa83ec401a7ee3912` | 34 dòng, 3.007 B |
| JSON `1fc99cd9…` | `1fc99cd9339fb5f085436e60ef39bac3058a79dbc009161597ecc7bc85efbd61` | 6.128 B; chạy lại byte-equal |
| Tự kiểm 24/24 | **24/24**, không stderr | Bản in byte-equal log cung cấp |
| Ma trận 14/14 + gốc | **14/14 + gốc**, `TAT_CA_KHOP`, không stderr | Bản in byte-equal log cung cấp; mỗi mutant rc1, gốc rc0 |
| 89 miền /89 hợp lệ /3 ngoài miền | **89/89/3** | Kiểm độc lập cả bốn trường và ID/tên; 3 tệp `.yaml.nhap` |
| 11 cặp hai chiều /3 một chiều | **11/3** | Walker độc lập và JSON script khớp |
| Digest tập cặp | `8f372ccd2ceab70901868a58d3380acbd89dce25c7127d4d514bc959270fef48` | JSON compact tuple4 sắp thứ tự |
| 0 vi phạm /0 KXD /giữ0 | **0/0/0** | Mọi đầu mới hết hạn tại C |
| Hạn muộn nhất | `2026-09-08T10:17:12Z` | Walker đọc 11 hạn |
| C = giờ commit mốc | `2026-09-10T11:55:37+07:00` = `2026-09-10T04:55:37Z` | `git show -s --format=%cI` |
| Mốc là tổ tiên | rc0 trên cả HEAD và origin/master | Returncode trực tiếp |
| E16 437 head | **437/437**, tên và OID đều bằng nhau | Bare `kho.git` cục bộ so cache; không chứng nhận máy chủ mạng |
| E16 master | `68b552d0f08200ba860ea788517558a4172df384` | Đúng lời khai, không dùng làm nguồn Q6 |
| HINT lượt3 | Áp rc0, băm `7402a0bd…` đúng | Bản sao nháp3 trong scratch |
| HINT lượt4 | `patch -p0` rc0; cả ba tệp byte-equal bản đã kiểm | `scratch/additional-proofs.json/patch` |
| Hint tự kiểm /mutant /JSON | **26/26**, **15/15 + gốc**, JSON byte-equal | `scratch/hint-self-check.log`, `scratch/hint-mutations.log`, `scratch/hint-q6.json` |

Header “đã dùng 3/4” là số trước lời gọi này, phù hợp lịch sử ba verdict; review này tiêu thụ lượt **4/4**, không cấp lượt thứ5. Các băm lịch sử và bản nháp3 khớp hiện vật. Không coi dòng yêu cầu `gpt-6-astra/high` là phép đo model/effort backend.

## Nghiệm thu

**Rà E15 theo trường và nhánh:**

| Trường/điều kiện | Quan sát |
|---|---|
| `lease_id` | Kiểm kiểu và fullmatch, rồi so tên; không ép str. Các ca F12 đỏ đúng. Tên đầu mới và đuôi `.yml` đã probe riêng. |
| `thay_the_cho` | Dùng `_danh_sach_thay_the_cho`, sau đó kiểm miền và lặp trên kết quả chuẩn hoá. Null/chuỗi rỗng/danh sách rỗng là [] theo helper đã được chỉ định; không tự áp luật null của bia mộ sang trường này. Số/bool/map, phần tử sai kiểu/rỗng, lặp sau strip bị chặn. |
| `da_bi_thay_the` | Kiểm có khoá độc lập với giá trị; null/bool/số/list/map/chuỗi rỗng và khoảng trắng đều rc3; chuỗi ngoài miền rc3. Khoá vắng vẫn hợp lệ. |
| `lease_expires_at_utc` | Sai kiểu, rỗng, định dạng sai, thiếu múi giờ bị chặn; cùng thời điểm biểu diễn bằng +07:00 vẫn hết hạn tại biên. Còn nhánh đổi sang UTC tràn miền, F13. |
| Dẫn xuất/trạng thái | Hai chiều bắt buộc, một chiều được kiểm kê, hết hạn trước bia mộ, đã thay tiếp không giữ cặp trước, vòng hữu hạn. Không đưa cặp sau mốc vào hằng. |

`python3 -B scratch/review4.py` tạo **35 probe**, kết quả từng ca trong `scratch/own-cases.json`; đây không được khai là “35/35 pass”: hai probe tràn UTC ném ngoại lệ. Dùng kho Git thường, tệp YAML ASCII thông thường và helper thật.

**Ma trận cung cấp:** mọi tập đích đúng như SPEC:321–334 và `mut_q6.py`, gồm 5 ca của mutant ghép ba miền. Hai ca ID ở đầu cặp không phân biệt được việc bỏ **riêng** chốt miền ID, vì chốt miền tham chiếu đầu kia vẫn chặn. Log 14/14 thật, không phải tín dụng từ crash. Bộ tự kiểm chỉ so tập giữ khi kỳ vọng rc0 (`do_q6.py:204`); ở ca rc3, tập `giu_mong` không được assertion. Không dùng các giá trị đó làm bằng chứng độc lập về tập giữ trong ca lỗi.

**Đột biến riêng**, nguồn và tập dự đoán lưu trước chạy trong `scratch/own_mutations.py`; tất cả chạy hết suite, không Traceback:

| Mutant reviewer | Ca HONG trên 24 ca hiện có | Kiểm phân biệt bổ sung |
|---|---|---|
| Bỏ ghi vi phạm ID nhưng vẫn bỏ qua tệp sai | `thieu-id`, `id-sai-kieu`, `id-ngoai-mien-don` | Chứng minh ca thiếu/sai kiểu ID có tác dụng bắt bỏ qua im lặng, dù chưa có mutant này trong 14 dòng cung cấp |
| Bỏ ghi vi phạm YAML nhưng vẫn bỏ qua tệp sai | `yaml-hong` | Không dùng crash làm tín dụng |
| Đổi hạn `<=` thành `<` | Rỗng; vẫn 24/24 | Ca riêng hạn đúng C: gốc giữ0, mutant giữ x→y |
| Nhận thư mục con, so tên bằng basename | Rỗng; vẫn 24/24 | Ca riêng nested/z.yaml: gốc rc3, mutant rc0 |
| Hạn vắng mặc định thành năm2000 | Rỗng; vẫn 24/24 | Ca riêng z chỉ có ID: gốc rc3, mutant rc0 |

Ba mutant sống cho thấy **14/14 không phải bao phủ mọi nhánh**: thiếu ca biên bằng, thư mục con, và hạn vắng độc lập. Chốt tên cũng chỉ có fixture âm đầu cũ trong suite; reviewer đã thử đầu mới. Không nâng riêng các khoảng trống bao phủ này thành finding P1 “tiêu chí không thể đỏ”: các tiêu chí có thể đỏ trên ca độc lập, và đặc tả không khai đã giết mọi mutant khả dĩ. `scratch/additional-proofs.json/surviving_mutants` lưu đối chứng gốc/mutant; `scratch/own-mutations.json` lưu tập thực đo.

Với bản vá F13, mutant **coi tràn UTC như hết hạn** giết đúng hai ca mới; 14 mutant cũ giữ nguyên tập đích. Không ghép tên ca vào mã thuật toán để ép kết quả. Bản vá không thay bất kỳ số nào trên cây thật.

## Phản chứng đã chạy

Mọi lệnh từ cwd. Thiết lập Git và tệp tạm:

```sh
mkdir -p scratch/m
: > scratch/empty.gitconfig
export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL="$PWD/scratch/empty.gitconfig"
export GIT_OPTIONAL_LOCKS=0
export TMPDIR="$PWD/scratch"
export PYTHONDONTWRITEBYTECODE=1
```

Các lệnh chính tái lập:

```sh
python3 -B do_q6.py --tu-kiem cay-kho
python3 -B mut_q6.py scratch/m cay-kho do_q6.py
python3 -B do_q6.py cay-kho 072181157a27804e69deb35bb792a88c70ac31e3 2026-09-10T04:55:37Z
python3 -B scratch/review4.py
python3 -B scratch/own_mutations.py
python3 -B scratch/build_hint.py
python3 -B scratch/hint/do_q6.py --tu-kiem cay-kho
mkdir -p scratch/hint/m
python3 -B scratch/hint/mut_q6.py scratch/hint/m cay-kho scratch/hint/do_q6.py
python3 -B scratch/hint/do_q6.py cay-kho 072181157a27804e69deb35bb792a88c70ac31e3 2026-09-10T04:55:37Z
python3 -B scratch/additional_proofs.py
```

`build_hint.py` tạo lại bản sao vá và unified diff. `additional_proofs.py` kiểm CLI gốc/vá trên cùng kho và áp patch lên bản sao sạch; áp bằng `patch -p0`, cả ba tệp kết quả đúng bản đã kiểm. `scratch/final_checks.py` kiểm hint lượt3, so bản in/log và trạng thái mirror; lần chạy ghi nhận `git status --porcelain --untracked-files=all` rỗng. Script kiểm hint lượt3 dùng thư mục scratch mới cho lần áp; khi tái chạy cần thư mục `scratch/previous-hint/` không chứa các tệp phụ do một lần áp lỗi trước đó.

## KHÔNG ĐO ĐƯỢC

- Không mạng: E16 chỉ đo bare cục bộ và cache; không xác thực lời khai advertisement máy chủ lúc 23:47:11Z, thời điểm chạy bản soạn, GitHub comments/tags hoặc trạng thái PR online.
- Không chạy lại suite168, M14/A18 đầy đủ, actionlint/shellcheck; không có implementation r2 mới để nghiệm thu. Kế thừa kết luận trước chỉ ở phần delta và blob không đổi, đã nói rõ.
- Hướng cần nội dung nhạy cảm chỉ xét bằng lời: tên đường dẫn khiến Git xuất dạng quote/escape có thể làm phép lọc hậu tố trên output dạng dòng bỏ sót blob; đường thoát cây, đồng tự Unicode, helper/object Git giả cần phép thử riêng được phép. Không tạo payload, không chạy các hướng ấy và không tính chúng vào findings có bằng chứng thực nghiệm.
- Clock trên cây thật được đối chiếu giờ commit. Kho phản chứng dùng clock kiểm thử cố định; không nhận thời gian tạo commit fixture bằng clock đó, và không nhận bộ 24 ca chứng minh nguồn clock của mọi caller.
- Không suy kết quả 89/89 sạch thành validator đầy đủ; không suy 14/14 thành bao phủ toàn bộ nhánh. Không đo hoặc khai danh tính model/effort từ trường reviewer trong SPEC.

Đây là lượt cuối và còn P1/P3: **phiên soạn dừng, đưa chủ kho quyết theo yêu cầu**. Không đề nghị gọi review thứ5; không tự đóng băng, cấp lease, merge hoặc áp HINT vào mirror. HINT là phương án sửa đã kiểm để chủ kho xem xét.
