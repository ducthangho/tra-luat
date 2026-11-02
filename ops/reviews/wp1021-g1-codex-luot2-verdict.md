Verdict: request_changes
Reviewed commit: 5efa311fd857f7657a1c687e9ea37693070a37d3
Spec sha256: d5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d

Kết luận: **request_changes**, còn **1 P2 và 1 P3** (2 lớp, 2 biểu hiện mở). Head qua **96/96 ca · 143/143 đột biến thường · 2/2 tự kiểm**, `TỔNG: ĐẠT`. Ba đột biến sống ở lượt trước nay chết đúng chốt c99. Lỗi liệt kê cũ đã được vá ở iterdir, nhưng EACCES ở `is_dir()` vẫn thoát traceback qua đường `--sinh-no`. Đột biến tương đương bắt `Exception` sống qua toàn suite, cho thấy thiếu chốt phân biệt lỗi lập trình. Ngưỡng áp dụng theo packet: không còn P0/P1/P2/P3. Windows và CI trên head này không được đo độc lập; không suy kết quả từ báo cáo executor.

## Neo và phạm vi

`git -C cay-kho rev-parse HEAD HEAD^{tree} origin/master` (rc=0): head như trên; tree `84f05adc6dcaadd38590431d92b2bc5df4206b99`; base `757bde561d09738858506aecf5de2f050a5f0d5e`.
`git -C cay-kho rev-parse --is-shallow-repository` ⇒ `false`; status gồm ignored/untracked ⇒ rỗng; `sha256sum SPEC.md` khớp dòng 3.
Đã đặt `git -C cay-kho config core.abbrev 7` theo chỉ thị. Các bản sao `work/head`, `work/base` có đủ cây và `.git` là thư mục. Lệnh Python đo chạy với `PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null` qua `measure.py` hoặc tiền tố môi trường tương đương.

Các script lượt 1 được chép ra gốc sandbox: `measure.py`, `listing_probe.py` giữ nguyên; `probe.py` thêm c99 vào danh sách ca đích; `mutate.py` đổi mốc neo selector từ biểu thức return sang ds, nosort vẫn che sorted bằng list tại return. Không đổi cơ chế phép thử. Diff adapter nằm trong `evidence/adapter-*.patch`.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn: `VERDICT-LUOT1.md`, reviewed head `99c463d9288798cf7a011e16ce69c36b04520f66` (lượt trước); đối chiếu trên exact head dòng 2 bằng script đã chép kèm.

| Finding P2 lượt 1 | Phân loại | Bằng chứng độc lập trên head mới |
|---|---|---|
| `loi-do-liet-ke-thu-muc-thoat-traceback` | **VÁ HỜ ở cấp lớp; phép tái hiện gốc đã vá thật** | `python3 listing_probe.py`: lỗi scandir ở cả hai đường nay rc=2, không traceback, có marker xác nhận tiêm. Tuy nhiên `python3 review_new.py error-child head sinh access`: EACCES ở stat trước iterdir vẫn rc=1/Traceback tại helper:101. Cùng gốc là thao tác I/O chuẩn bị danh sách nằm ngoài nhánh đổi lỗi đo; xem finding F1. |
| `bo-chon-ung-vien-thieu-rang-hai-duong-goi` | **ĐÃ VÁ THẬT** | `python3 mutate.py sinh_exact --suite`, `nosort --suite`, `noguard --suite`: cả ba rc=1/95 trên 96 ca/TỔNG: ĐỎ. c99 chết đúng chốt sinh nợ, thứ tự, thư mục vắng; c98/c89/c18 đối chứng qua. Thông báo và N/N đầy đủ ở Đợt 1 và Đợt 4. |

Không coi traceback của guard `kiem` ở base là hồi quy mới; F1 khoanh hồi quy vào guard helper mà packet thêm cho `--sinh-no`. Không có finding mới hình dạng `bo-chon-ung-vien`; chốt dừng cũ đã được chủ kho cho làm tiếp theo packet giao lượt này.

## Nhật ký đo

### Đợt 1 — phép tái hiện cũ, C1/C2/C3/C6/C9

`PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 listing_probe.py` giữ nguyên script lượt 1: head `kiem` và `--sinh-no` đều **rc=2**, stderr có `REVIEW_ENUMERATION_FAULT: scandir`, `KHÔNG ĐO ĐƯỢC: không liệt kê được … (PermissionError …)`, không traceback. Đối chứng không tiêm: `kiem` rc=1/tổng 1/sai schema, sinh nợ rc=0/# 1 tệp. Log và rc thật: `evidence/listing-head-{kiem,sinh}-{fail,control}.{json,stdout,stderr}`.

Ba đột biến cũ đã chết đúng chốt c99 trong lượt chạy ca đích (`python3 mutate.py <tên> --suite`; số đo toàn suite bổ sung ở Đợt 4):

| Đột biến | Phân loại của c99 | Thông báo thực đo |
|---|---|---|
| sinh_exact | giet_that | sinh-no: đòi rc=0, khối nợ nêu x.RECEIPT.YAML, # 1 tệp; được rc=0, khối rỗng, # 0 tệp |
| nosort | giet_that | thứ tự: đòi a,m,z khi iterdir trả ngược; được z,m,a |
| noguard | giet_that | vắng/sinh-no: đòi rc=0 # 0 tệp; được rc=2 … FileNotFoundError |

Cả ba: c98 và c89 `qua`, đối chứng c18 `[true, ""]`. Chi tiết nguyên văn: `evidence/mut-*-cases.stdout`; không coi rc của wrapper là bằng chứng giết.

`python3 mutate.py exact --behaviors` ⇒ c98 `giet_that`, C1a tổng 1; `python3 mutate.py isfile` ⇒ c89 `giet_that`, rc=1 thay rc=2; `python3 mutate.py glob` ⇒ c98 `giet_that`, tổng 1. Cả ba có đối chứng c18 sạch. Các đột biến được tạo trên bản sao đầy đủ, mỗi cái tiến trình riêng.

`PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 probe.py head behaviors` dựng các kho git thật độc lập:

| Fixture | rc | tổng | Traceback |
|---|---:|---|---|
| bad-order | 2 | [] | False |
| c1a | 1 | ['2'] | False |
| c1b | 2 | [] | False |
| case-pair | 1 | ['2'] | False |
| directory | 2 | [] | False |
| empty | 2 | [] | False |
| missing | 2 | [] | False |
| only-x | 1 | ['1'] | False |
| order | 1 | ['3'] | False |
| sinh-missing | 0 | [] | False |
| sinh-order | 0 | [] | False |
| sinh-upper | 0 | [] | False |

C1a và chỉ-x đều nêu tên đuôi hoa, không `TỔNG: ĐẠT`; C1b stderr nêu `x.RECEIPT.YAML`. Nội dung từng stdout/stderr và lệnh CLI nằm trong `evidence/fixture-head-*.json`.

`python3 measure.py head gate` và `python3 measure.py base gate` ⇒ cùng rc=0, `253 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 306`, `TỔNG: ĐẠT`. Đếm độc lập bằng `sum(p.name.lower().endswith(".receipt.yaml") for p in Path("work/head/ops/reviews").iterdir())` ⇒ 306; base cũng 306.

`python3 measure.py head doctrine` ⇒ rc=0, `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`.
`python3 measure.py {head,base} ruff` (Ruff 0.15.15, no-cache, --select F, đúng hai tệp) ⇒ cả hai rc=1 và cùng F541 tại `ops/bien_nhan_v2_test.py:1677:19`; delta 0. Không gọi bare lint là sạch.
`git -C cay-kho diff --numstat 757bde561d09738858506aecf5de2f050a5f0d5e..HEAD` ⇒ `26 3 ops/bien_nhan_v2.py`, `148 0 ops/bien_nhan_v2_test.py`; name-only đúng hai tệp write set; diff --check cùng dải ⇒ rc=0/rỗng.
`rg -n 'glob\("\*\.receipt\.yaml"\)' ops/bien_nhan_v2.py` ⇒ head 0 dòng/rc=1; base 2 dòng/rc=0; mut-glob 1 dòng/rc=0 (vế âm có đối chứng dương).

### Đợt 2 — độ nhạy của c99, lỗi giàn giáo và khôi phục toàn cục

`python3 new_mutate.py fault_noop`: vô hiệu điều kiện tiêm bằng `False and …` ⇒ c99 `giet_that`, thông báo `liệt kê hỏng [] … được rc=1`, không xanh giả. `python3 new_mutate.py fault_noop_sinh`: chỉ vô hiệu tiêm ở `--sinh-no` ⇒ c99 `giet_that`, thông báo `liệt kê hỏng ['--sinh-no'] … được rc=0: '# 1 tệp'`. Hai đối chứng c98/c89 qua, c18 sạch.
`python3 new_mutate.py order_noop`: fixture trả xuôi ⇒ c99 `gian_giao`, `fixture: iterdir ngược không có hiệu lực`; không được tính là giết thật. Cùng với mutant nosort chết bằng kết quả helper z,m,a, phép đo thứ tự kiểm cả giàn giáo lẫn đầu ra helper.
`python3 new_mutate.py no_os_catch` ⇒ c99 `giet_that`, `CLI chết bằng PermissionError … đòi mã thoát, không traceback`.
`python3 new_mutate.py catch_empty` ⇒ c99 `giet_that`, rc=2 nhưng chỉ báo `không có tệp`, thiếu `không liệt kê được`. Vậy chỉ rc=2 không đủ đánh lừa chốt (4).

`PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 trace_probe.py` ⇒ c99 `qua`, hai lần PermissionError được tiêm đúng thư mục, modes `[]` và `['--sinh-no']` (`evidence/c99-trace.json`). Bản tracer đầu truy cập sai biến closure `co`, đã được phân loại là lỗi probe và lưu riêng `c99-trace-rig-error.json`; bản chạy đúng đọc mode từ frame c99.
`python3 review_new.py symlink` ⇒ c99 `qua` khi thư mục tạm đi qua symlink (`evidence/symlink-c99.stdout`). Đây chỉ là phép thử symlink trên hệ đang đo, KHÔNG phải bằng chứng Windows.

`python3 review_new.py cleanup <order|kiem|sinh> <runtime|rig>` (6 tiến trình riêng, môi trường chuẩn): cả 6 ghi `restored=true`, `finally_restored=true`, chạy lại c99 sau lỗi đều `['qua', null]`. Fault được tiêm khi Path.iterdir đang là `nguoc` hoặc `hong`, không phải trước khi patch. Với LoiDungCa cả 3 là `gian_giao`; RuntimeError ở order là `tin_dung_gia`, ở hai CLI là `giet_that`. Không quan sát rò Path.iterdir trong 6 nhánh lỗi này.
`python3 probe.py head rig` và `rig-setup` ⇒ c98/c99 đều `gian_giao`; nhánh `except LoiDungCa: raise` mới có hiệu lực. c89 cũ vẫn đổi lỗi rig do main thành `giet_that`; hành vi này ngoài phần sửa lượt 2, không dùng nó để chứng minh mutation mới chết.

### Đợt 3 — mở rộng lỗi I/O và ranh giới bắt ngoại lệ

`python3 review_new.py error-child head <kiem|sinh> late` ⇒ cả hai rc=2/không traceback khi iterator đã yield một mục rồi mới ném PermissionError; stderr có `REVIEW_FAULT_HIT: late` và `không liệt kê được`.
`python3 review_new.py error-child head <kiem|sinh> stat-os` ⇒ cả hai rc=1/Traceback, marker `REVIEW_FAULT_HIT: stat-os`. os.stat của đúng thư mục bị tiêm EACCES; Path.is_dir thật truyền lỗi ra ngoài try. Ở --sinh-no, traceback đi qua `_chon_bien_nhan` dòng 101; ở kiem là guard sẵn có dòng 1459.
`python3 review_new.py error-child <head|base> <kiem|sinh> access` tiêm cùng EACCES vào cả os.stat và scandir/glob của đúng thư mục. Head cả hai rc=1/Traceback; base kiem cũng rc=1/Traceback (lỗi đã có), base sinh rc=0/# 0 tệp, có marker `access-scandir`. Vì vậy hồi quy mới được khoanh ở nhánh `--sinh-no`; lỗi I/O trước iterdir vẫn chưa được chuẩn hoá. Log và mã thoát: `evidence/{head,base}-access-{kiem,sinh}.{json,stdout,stderr}`.

Đo bằng quyền thư mục thật: **KHÔNG ĐO ĐƯỢC**. `python3 actual_permissions.py` không hạ được quyền cho tiến trình con: `os.setgroups([])` trả EPERM ngay cả đối chứng; không có lệnh cổng nào chạy sau chốt đó. Không dùng các rc=1 ấy làm bằng chứng lỗi sản phẩm; finding ở trên chỉ dựa phép tiêm OS có marker trên Path.is_dir thật.

`python3 new_mutate.py broad_literal`: đổi `except OSError` thành `except Exception` ⇒ c98/c99/c89 đều `qua`, c18 sạch. Nếu giữ m147 nguyên văn thì mốc neo mất: `evidence/literal-anchor-check.json` ghi `gian_giao`, không phải oracle giết được lỗi bắt rộng.
`python3 new_mutate.py broad --suite`: đột biến tương đương về nghĩa bằng gán cục bộ `OSError = Exception` trong helper, giữ nguyên mốc neo của m147 để đo hành vi. Ca đích c98/c99/c89 vẫn qua, c18 sạch; toàn suite đã xong: rc=0, 96/96 ca, 143/143 đột biến thường, 2/2 tự kiểm, TỔNG: ĐẠT (463.72 s; xem chốt cuối).
`python3 review_new.py error-child <head|mut-broad> <kiem|sinh> <runtime|value>`: head phát RuntimeError/ValueError ra ngoài (rc=1/traceback); mutant biến chúng thành rc=2/`KHÔNG ĐO ĐƯỢC: không liệt kê được … (RuntimeError/ValueError …)`, không traceback. Tất cả có marker xác nhận lỗi đã tiêm. Đây là khác biệt hành vi thật; head hiện bắt đúng OSError, phần còn thiếu là test phân biệt lỗi lập trình.

### Đợt 4 — toàn suite và xác nhận ba đột biến cũ

| Lệnh (môi trường chuẩn ở đầu tệp) | rc thật của suite | Kết quả nguyên văn rút gọn | Thời gian |
|---|---:|---|---:|
| `python3 measure.py head suite` | 0 | bien_nhan_v2_test: 96/96 ca đạt · 143/143 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 125/143 đột biến thường khai đối chứng; TỔNG: ĐẠT | 483.28 s |
| `python3 mutate.py sinh_exact --suite` | 1 | bien_nhan_v2_test: 95/96 ca đạt · 142/143 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 125/143 đột biến thường khai đối chứng; TỔNG: ĐỎ | 476.41 s |
| `python3 mutate.py nosort --suite` | 1 | bien_nhan_v2_test: 95/96 ca đạt · 143/143 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 125/143 đột biến thường khai đối chứng; TỔNG: ĐỎ | 481.23 s |
| `python3 mutate.py noguard --suite` | 1 | bien_nhan_v2_test: 95/96 ca đạt · 142/143 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 125/143 đột biến thường khai đối chứng; TỔNG: ĐỎ | 481.72 s |

Trong full log, cả ba mutant có dòng `ĐỎ c99_… [giet_that]` với đúng thông báo đã trích ở Đợt 1. `sinh_exact` còn làm m144 mất neo, `noguard` làm m146 mất neo: hai dòng `gian_giao` ấy KHÔNG được dùng làm bằng chứng giết; bằng chứng là c99 tự đỏ khi chạy trên mutant, trước pha đột biến nội bộ. `nosort` giữ 143/143 đột biến nhưng vẫn đỏ vì c99, đúng kỳ vọng.

Phác thảo oracle đã chạy cho ranh giới ngoại lệ: `python3 boundary_oracle.py head` ⇒ rc=0; `python3 boundary_oracle.py mut-broad` và `mut-broad_literal` ⇒ rc=1. Tiêm một RuntimeError sentinel tại đúng thư mục rồi đòi đúng đối tượng ngoại lệ truyền ra ngoài trên cả hai đường; mỗi đường có hit=1 và Path.iterdir được khôi phục. Chi tiết: `evidence/*-boundary-oracle.{json,stdout,stderr}`. Đây là dữ liệu phản chứng trong sandbox, không phải bản vá giao áp tự động.

## Bảng tiêu chí

| Tiêu chí | Kết quả | Lệnh và bằng chứng |
|---|---|---|
| C1a | ĐẠT phần đã đo; Windows KHÔNG ĐO ĐƯỢC | `python3 probe.py head behaviors`: c1a rc=1/tổng 2/có x.RECEIPT.YAML/không ĐẠT; only-x rc=1/tổng 1/không "không có tệp". `mutate.py exact --behaviors`: C1a còn tổng 1, only-x không tổng; c98 giet_that. |
| C1b | ĐẠT phần đã đo; Windows KHÔNG ĐO ĐƯỢC | Cùng lệnh: YAML hỏng đuôi hoa rc=2/stderr nêu x/không traceback/không tổng. Mut-exact bỏ sót x, rc=1, tổng 1. |
| C2 | ĐẠT phần đã đo; Windows KHÔNG ĐO ĐƯỢC | Full suite có c89 ĐẠT; `python3 mutate.py isfile`: c89 giet_that, rc=1 thay rc=2, c98/c99 qua, c18 sạch. |
| C3 | ĐẠT trên Linux | `python3 mutate.py glob`: c98 giet_that/C1a tổng 1; đối chứng c18 sạch. Không cho mutant phụ thuộc nền này vào bảng thường. |
| C4 | KHÔNG ĐO ĐƯỢC | Không có phép đo Windows CI độc lập trên exact head trong lượt này; success trên 99c463d do executor cung cấp không thay bằng chứng 5efa311. |
| C5 | KHÔNG ĐO ĐƯỢC | Không có log Ubuntu CI độc lập trên exact head; full suite tại sandbox không được nhận là CI. |
| C6 | ĐẠT | `python3 measure.py head gate`: rc=0, tổng 306, TỔNG: ĐẠT; đếm riêng 306. Base thật cũng rc=0/tổng 306. `--sinh-no` trên head rc=0/# 42 tệp. |
| C7 | KHÔNG ĐO ĐƯỢC | Không chạy Windows local. |
| C8 | KHÔNG ĐẠT | Còn finding F1 (P2), F2 (P3); verdict request_changes trên exact head đã neo. Không cấp quyền merge/land. |
| C9 | ĐẠT | Ruff --select F delta 0 (cả hai bare lint rc=1/cùng F541); doctrine rc=0/10 tệp/0 chỗ; diff --check rc=0; rg 0 dòng, có đối chứng base 2/mut-glob 1; numstat +26/-3 và +148/-0, đúng hai tệp. |

## Finding

| ID | Mức | Slug lớp nguyên nhân | Nguồn/lý do giữ hoặc thêm | Phép đóng |
|---|---|---|---|---|
| F1 | P2 | `loi-do-liet-ke-thu-muc-thoat-traceback` | Giữ slug lượt 1; biểu hiện cũ ở scandir đã đóng, còn biểu hiện I/O trước liệt kê tại is_dir trên --sinh-no | Tiêm EACCES cả stat và liệt kê: hai đường rc=2/không traceback; vắng thật vẫn đúng hành vi cũ; fixture/c99 mới phải giết mutant bỏ bắt lỗi stat. |
| F2 | P3 | `loi-do-thieu-chot-ngoai-le-lap-trinh` | Mới trong phần test cho nhánh bắt OSError; hiện c99 chỉ tiêm PermissionError | Head qua oracle RuntimeError sentinel; mutant bắt Exception phải bị giết thật bởi ca đích, không phải mất neo m147. |

- [P2] `loi-do-liet-ke-thu-muc-thoat-traceback`: `ops/bien_nhan_v2.py:101` (gọi từ `_sinh_no` dòng 1624), khối try bắt đầu ở dòng 103 — `PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 review_new.py error-child head sinh access` — rc=1, stderr có `REVIEW_FAULT_HIT: stat-os`, `Traceback`, `PermissionError: [Errno 13] review OS stat failure`; base cùng phép tiêm rc=0/# 0 tệp, marker access-scandir — đưa cả bước kiểm tra thư mục vào chính sách bắt **OSError** và đổi thành KhongDoDuoc, không đổi lỗi truy cập thành vắng/rỗng. Giữ hành vi thật sự thiếu thư mục (`kiem` rc=2, sinh nợ rc=0/# 0 tệp), bổ sung ca tiêm lỗi stat ở helper và đối chiếu guard kiem để hai đường cùng chuẩn lỗi I/O. Không bắt Exception để che lỗi lập trình.

HÌNH DẠNG: `loi-do`.

Bằng chứng chỉ rõ điều kiện lỗi: stat của thư mục biên nhận bị từ chối trước khi iterdir chạy, như lỗi quyền tra cứu đường dẫn. Guard mới nằm ngoài try nên lời khẳng định "lỗi I/O khi chọn biên nhận ⇒ rc=2 không traceback" chưa kín. Ở kiem, cùng lỗi đã có trên base và không được kê riêng thành hồi quy. Bản thử quyền thực tế bị chặn ở setup đã nêu ở Đợt 3; không suy rằng phép chmod thật đã được đo thành công.

- [P3] `loi-do-thieu-chot-ngoai-le-lap-trinh`: `ops/bien_nhan_v2_test.py:3731` (c99 chốt lỗi liệt kê), `ops/bien_nhan_v2_test.py:4568` (m147) — `PYTHONDONTWRITEBYTECODE=1 python3 new_mutate.py broad --suite` — **rc=0, 96/96 ca đạt · 143/143 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 125/143 đột biến thường khai đối chứng; TỔNG: ĐẠT**, 463.72 s; trong khi RuntimeError/ValueError ở iterdir bị chuyển thành KhongDoDuoc — thêm chốt tiêm lỗi lập trình ngoài OSError và đòi ngoại lệ nguyên gốc truyền ra trên cả hai đường, cùng mutant nới catch phải chết tại chốt đó. `boundary_oracle.py` đã đo head rc=0, cả hai mutant broad/broad_literal rc=1; có hit=1/đường và khôi phục Path.iterdir.

HÌNH DẠNG: `loi-do`.

Đây là thiếu chốt hồi quy, không khẳng định head hiện bắt Exception. Mutant `broad_literal` đổi trực tiếp tên catch, vượt qua c98/c99/c89 và đối chứng, nhưng phá mốc neo văn bản m147 nên không thể dùng lỗi rig để nhận tín dụng giết. Mutant `broad` đặt tên cục bộ `OSError = Exception` trong chính helper: cùng nghĩa bắt rộng, vẫn giữ mốc neo, và sống qua toàn suite. Vì chốt (4) chỉ đưa PermissionError (thuộc OSError), nó không phân biệt catch hẹp với catch rộng. Ảnh hưởng có giới hạn: mutant vẫn fail-closed rc=2, nhưng che nguyên nhân lỗi lập trình thành lỗi đo; do đó xếp P3, không xếp lỗi runtime P2 cho head đang đúng.

## Chốt bằng chứng và giới hạn

`python3 new_mutate.py broad --suite` đã hoàn tất: log `evidence/mut-broad-suite.stdout`, mã thoát và thời gian `evidence/mut-broad-suite.json`. Không đột biến nào còn đang chờ kết quả để lập verdict này.

`python3 probe.py base behaviors` được chạy lại qua `measure.run` trên đúng base: C1a rc=1/tổng 1/bỏ x; only-x rc=2/không tổng; C1b rc=1/tổng 1/bỏ x. `python3 probe.py base cases` ⇒ c89 qua, c18 sạch. `evidence/base-behaviors.*`, `fixture-base-*.json` và `base-cases.stdout` lưu phép đo mới, không tái dùng số của lượt 1.

`PYTHONDONTWRITEBYTECODE=1 python3 integrity.py` ⇒ rc=0. `evidence/final-integrity.json` ghi lệnh/output: head/tree/base vẫn đúng các neo ở đầu; detached, không nông, core.abbrev=7; status gồm tracked/untracked/ignored rỗng; diff worktree và index so HEAD rc=0/rỗng. Hai tệp write set byte-identical với blob HEAD; DIFF.patch và DIFF-LUOT2.patch byte-identical với git diff tương ứng; SPEC vẫn khớp SHA-256. Bản `work/head` chạy suite cũng sạch và cùng HEAD/tree. Snapshot đầu/cuối chứng minh không có delta nội dung quan sát được; không dùng nó để khẳng định toàn bộ lịch sử mọi lần ghi. Thay đổi cấu hình core.abbrev được thực hiện đúng yêu cầu trước đo.

Các phần **KHÔNG ĐO ĐƯỢC**: Windows CI/local, Ubuntu CI trên exact head, và tái hiện bằng quyền hệ điều hành thật sau hạ quyền (setup EPERM). Không dùng kết quả CI của head cũ hoặc lời khai executor để đánh dấu đạt. Những hướng liên quan nội dung nhạy cảm không được dựng thêm. Không có thay đổi mã nguồn trong checkout được review; các script và mutant là hiện vật thử trong sandbox. Verdict này không cấp quyền merge/land.
