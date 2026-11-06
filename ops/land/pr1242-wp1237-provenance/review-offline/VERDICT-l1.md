verdict: changes_requested
reviewed_sha: 43258fbe43d2b1508cdb0a00dc1ba436f28968c5

Có **1 finding P2 đã tái hiện độc lập**: kiểm độ dài thô từ chối MAX_TIME hợp lệ có số 0 đứng đầu, trái M2. Lỗi quyền sandbox không được tính thành lỗi sản phẩm hoặc tín dụng giết đột biến. HTTP `t237` là **KHÔNG ĐO ĐƯỢC** trong lượt này.

- Base: `fe84620f897913c7f6c2ce5a0c7316a49655e82f`.
- Reviewed tree: `61bab80ab432dd23715701efe10b0c9da4dc0e32`.
- SHA-256 `SPEC.md`: `b0e12304e0c591db6e2130454ed6a72c1458d4541b1312037935b0ccbb210666`, khớp prompt/lease. Packet wp1237, r1, g1, sensitive; lease khớp base và write_set.
- Reviewer độc lập: provider `openai_codex`, execution_surface `codex_cli`, transport `machine`, theo `runs/979e9205/run.json`. Model/effort phục vụ chưa có trong sổ: **KHÔNG ĐO ĐƯỢC**, không suy từ tài khoản đăng hoặc cấu hình yêu cầu.
- Môi trường: Linux, Python 3.13.18, bash 5.2.21, curl 8.5.0, shellcheck 0.9.0, actionlint 1.7.7, Ruff 0.17.3.
- Chỉ ghi hiện vật ngoài `cay-kho`; không sửa, commit, push, đăng comment hay gọi workflow. Áp dụng `cay-kho/.claude/skills/cross-review/SKILL.md` và protocol §8/§13. Đây là lượt đầu, không có finding lượt trước cần đối chiếu.

## BẢNG ĐỐI CHIẾU SPEC (M1–M5, D1–D6)

| Mục | Khớp/lệch | Bằng chứng và giới hạn |
|---|---|---|
| M1 — retry đủ dài | **KHỚP về mã** | Installer dòng 58–60,136–138: mặc định 8/15/300, đúng đủ `-fsSL`, `--retry`, `--retry-delay`, `--retry-all-errors`, `--retry-max-time`, `--connect-timeout 20`. Tài liệu ở dòng 24–32. Curl thật qua file://: tệp xuất hiện sau 2,5s ⇒ mặc định rc=0 sau 3,035s; retry=2 ⇒ rc=4 sau 2,017s. Chưa đo 504 HTTP. |
| M2 — kiểm núm vặn | **LỆCH: F1** | Regex, mã 13, tên/giá trị trong lỗi và phân biệt unset/rỗng đều có. Nhưng dòng 68 từ chối mọi chuỗi dài >4: `00001`, `00008`, `000300`, `0001800` bị rc13 dù giá trị trong 1..1800. Những ca 0,1801,1e3 và tràn số bị từ chối đúng. |
| M3 — cổng băm | **KHỚP trong phạm vi đo** | Thứ tự MONG dòng 124/127 → tải 136 → THUC/đối chiếu 146–148 → giải nén 197–204 không đổi. Khối băm ghim không đổi. Trace base/HEAD chứng minh AL_GOI không gọi curl. t37 đạt. Gói sai/tệp cắt nửa qua curl thật đều rc9 trước giải nén/chạy. D2/D5 sau HTTP retry chưa đo. |
| M4 — lỗi đọc được | **KHỚP trong phạm vi đo** | Dòng 139 báo `toi da 1+${AL_RETRY} lan thu`, retry/delay/trần. Đã đo lỗi tải file:// thật: rc4, `toi da 1+2 lan thu ... tran 10s`. D3 kiểm `1+2 lan thu` và `30s`; vế HTTP chưa đo. |
| M5 — lần đầu thành công | **KHỚP trong phạm vi đo** | Gói đúng tải bằng curl thật qua file://: base rc0/0,0264s; HEAD rc0/0,0328s. Stdout đúng một dòng thư mục cài, stderr rỗng, không chờ thêm 15s. D6 HTTP/số yêu cầu chưa đo. |

| Vế | Đối chiếu ca mới | Kết quả chạy lại |
|---|---|---|
| D1 | Dòng 14704–14706: 504×3 rồi gói đúng; không đặt AL_RETRY; đòi rc0,n=4. **KHỚP**. | **KHÔNG ĐO ĐƯỢC**: tạo server bị EPERM trước lần chạy installer đầu tiên. |
| D2 | Dòng 14629–14634,14708–14710: Content-Length đủ, ghi nửa thân rồi đóng; sau đó gói đúng; đòi rc0,n=2. **KHỚP**. | KHÔNG ĐO ĐƯỢC. |
| D3 | Dòng 14712–14715: luôn 504, retry2/max30; đòi rc4,n=3, thông điệp có lần thử/trần. **KHỚP**. | KHÔNG ĐO ĐƯỢC. |
| D4 | Dòng 14717–14725: đủ 4 giá trị bắt buộc và thêm rỗng/1e3/tràn; đòi rc13,n=0,tên biến. **KHỚP ca yêu cầu**; không có ca dương có 0 đứng đầu nên sót F1. | KHÔNG ĐO ĐƯỢC trong t237: vế sai núm cũng dựng server trước. Logic từ chối đã đo bổ sung qua AL_GOI; không khai n=0 từ bộ đếm chưa chạy. |
| D5 | Dòng 14727–14732: 504 rồi gói khác băm; rc9,n=2, không marker và không binary giải nén. **KHỚP**, mạnh hơn chỉ xét rc. | KHÔNG ĐO ĐƯỢC; kiểm băm file:// là bổ sung, không thay thế vế HTTP. |
| D6 | Dòng 14734–14737: gói đúng lần đầu, rc0,n=1, stdout đúng một dòng thư mục. **KHỚP**. | KHÔNG ĐO ĐƯỢC; có kiểm bổ sung M5 bằng file://. |

Hình thức ca **KHỚP**: dùng `_bash_cho_cai_actionlint()`, `_goi_actionlint_gia`, `http.server.ThreadingHTTPServer(("127.0.0.1",0),...)`, curl thật; đặt cả NO_PROXY/no_proxy, xóa GITHUB_PATH và các núm ambient. Khóa bảo vệ bộ đếm; kịch bản chọn theo số yêu cầu, hết thì lặp phần tử cuối. Kiểm handler bổ sung bên dưới không thay cho phục vụ HTTP thật.

Các lệnh bắt buộc đã chạy trên `cay-kho`, có `PYTHONDONTWRITEBYTECODE=1`:

| Lệnh | rc / output thật | Đánh giá |
|---|---|---|
| `python3 ops/lease_publish_test.py --chi-ca=t237` — 3 lần có lưu log | Cả 3 rc1; `PermissionError: [Errno 1] Operation not permitted`; `lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0` | **KHÔNG ĐO ĐƯỢC**, không có `1/1 đạt`. |
| `python3 ops/lease_publish_test.py --chi-ca=t35` | rc0; `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` | **ĐẠT** |
| `python3 ops/lease_publish_test.py --chi-ca=t37` | rc0; `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` | **ĐẠT** |
| `python3 ops/lease_publish_test.py --chi-ca=t38` | rc0; `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` | **ĐẠT** |
| `shellcheck ops/cai_actionlint.sh` | base/HEAD rc0, output rỗng | **ĐẠT, delta=0** |
| `bash -n ops/cai_actionlint.sh` | rc0 | **ĐẠT** |
| `python3 -m ruff check --no-cache --select F ops/lease_publish_test.py` | base/HEAD rc1, cùng 9 chẩn đoán F401/F541; phần chẩn đoán giống từng byte | **ĐẠT delta=0**, không phải lint tuyệt đối xanh |
| `actionlint -no-color` | base/HEAD rc1, cùng SC1003 ở workflow `ops-don-ref.yml:117:9`; chẩn đoán giống nhau | **ĐẠT delta=0**; actionlint đo workflows gọi installer, shellcheck đo trực tiếp `.sh` |

Log nguyên văn: `review-evidence/t237-{1,2,3}.log`, `t35.log`, `t37.log`, `t38.log`, `shellcheck-{base,head}.log`, `ruff-{base,head}.log`, `actionlint-{base,head}.log`. Hai SyntaxWarning cũ ở dòng 3640/5783 không phải nguyên nhân t237 đỏ.

**Suite Linux đầy đủ đã kết thúc:** `PYTHONDONTWRITEBYTECODE=1 python3 -B ops/lease_publish_test.py` trên hai bản sao tạm đầy đủ (base được checkout đúng SHA trong bản sao, không đổi nguồn).

| Cây | rc / thời gian | Output cuối |
|---|---|---|
| HEAD 43258fbe43d2b1508cdb0a00dc1ba436f28968c5 | rc1 / 384,976s | `lease_publish: 283/285 đạt; đã chạy=285, bỏ qua=0` |
| Base fe84620f897913c7f6c2ce5a0c7316a49655e82f | rc1 / 388,771s | `lease_publish: 283/284 đạt; đã chạy=284, bỏ qua=0` |

Cả hai cùng đỏ `t223_a1a_q6_ancestor_and_fixed_history`: `rc=128 'fatal: Not a valid commit name 072181157a27804e69deb35bb792a88c70ac31e3'`. Probe trực tiếp `git -C cay-kho cat-file -e '072181157a27804e69deb35bb792a88c70ac31e3^{commit}'` cũng rc128, xác nhận object này không có trong clone được cấp. HEAD thêm t237 đỏ vì PermissionError socket như trên. Không có test cũ nào khác đổi kết quả trong hai lượt. **Không đạt tiêu chí N/N**, không đổi lỗi baseline/capability thành finding của diff. Log đầy đủ: `review-evidence/full-head.log`, `full-base.log`; rc/thời gian: `full-{head,base}-result.txt`.

**Windows:** not_run, không có capability Windows trong lượt này. `tra-luat-win`/KHOA.txt do phiên điều phối chạy theo spec. Không gọi workflow_dispatch.

## BẢNG ĐỘT BIẾN (của executor + của bạn; GIẾT/SỐNG/TÍN DỤNG GIẢ, vế đỏ)

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_checks.py mutations`. Runner executor được chép sang `review-evidence/mutation_runner_executor_local.py`, chỉ đổi REPO thành đường tuyệt đối của `cay-kho`. Mỗi mutant chạy trên bản sao tạm ngoài kho; không sửa runner gốc hoặc nguồn.

Chỉ tính GIẾT khi có assertion cuối `retry của cai_actionlint.sh sai` và đúng vế đỏ. Cả 12 lượt đều rc1 vì **PermissionError trước bang**, không có vế đỏ; **KHÔNG ĐO ĐƯỢC**. Tính GIẾT dựa riêng rc ở đây là **TÍN DỤNG GIẢ**. Runner executor tự trả rc0 dù cả 5 dòng ghi `KHONG/TIN_DUNG_GIA`; rc runner không chứng minh 5/5 giết.

| Nguồn / mutant | Vế đích | Output quan trọng | Phân loại |
|---|---|---|---|
| Executor `retry_ve_2` | D1 | `rc=1 ve_do=[] dung_tin_hieu=False dich=D1` | KHÔNG ĐO ĐƯỢC; nhận GIẾT là tín dụng giả |
| Executor `bo_retry_all_errors` | D2 | `rc=1 ve_do=[] dung_tin_hieu=False dich=D2` | như trên |
| Executor `bo_kiem_regex` | D4 | `rc=1 ve_do=[] dung_tin_hieu=False dich=D4` | như trên |
| Executor `bo_doi_chieu_bam` | D5 | `rc=1 ve_do=[] dung_tin_hieu=False dich=D5` | như trên |
| Executor `doi_bam_sau_giai_nen` | D5 | `rc=1 ve_do=[] dung_tin_hieu=False dich=D5` | như trên |
| Reviewer `bo_khoang_max_time` — bỏ kiểm độ dài và khoảng | D4 | `rc:1,red:[],assertion:false,bash_parse_rc:0` | KHÔNG ĐO ĐƯỢC |
| Reviewer `bo_retry_max_time` | M1/trần thời gian | như trên | KHÔNG ĐO ĐƯỢC |
| Reviewer `doi_13_thanh_4` | D4 | như trên | KHÔNG ĐO ĐƯỢC |
| Reviewer `bo_retry_delay` | M1/khoảng chờ | như trên | KHÔNG ĐO ĐƯỢC |
| Reviewer `loi_4_mat_so_lan_thu` | D3 | như trên | KHÔNG ĐO ĐƯỢC |
| Reviewer `them_stdout` | D6 | như trên | KHÔNG ĐO ĐƯỢC |
| Reviewer `mac_dinh_retry_3` | M1/default8 | như trên | KHÔNG ĐO ĐƯỢC |

**SỐNG đã chứng minh: chưa xác định.** Không coi mutant chưa tới assertion là SỐNG. Chưa xác nhận độc lập được lời khai executor 5/5 GIẾT ở môi trường của họ. Log ở `mutations-executor.log`, `mutations-extra.json`, `mutant-*.log` trong review-evidence.

**Lỗ đo suy từ mã, cần chạy lại khi có HTTP:** D3 chỉ tiêu khoảng 2s trong max30 nên bỏ retry-max-time có thể vẫn qua; không vế nào kiểm nhịp chờ nên bỏ retry-delay có thể vẫn qua; D1 chỉ cần 3 retry nên mặc định 8→3 có thể vẫn qua. Đây là **dự đoán SỐNG, chưa phải kết quả thực nghiệm**; chưa xếp finding. Test nên chạm trần thời gian, đo nhịp retry có dung sai và kiểm đủ mặc định8.

## BẢNG SĂN

Script và log đều nằm ngoài nguồn. Output dưới đây trích trường liên quan từ JSON/log thật; đường dẫn tạm được rút gọn. Các phép file:// dùng curl thật, không giả curl và không được dùng thay cho HTTP t237.

### HƯỚNG 1: số 0 đứng đầu và tương đương thập phân

- Giả thuyết: độ dài chuỗi thay vì giá trị số làm từ chối dữ liệu hợp lệ.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 repro_max_time.py`.
- Output thật:

```text
AL_RETRY_MAX_TIME=1        decimal=1    installer_rc=0  real_curl_rc=0
AL_RETRY_MAX_TIME=0001     decimal=1    installer_rc=0  real_curl_rc=0
AL_RETRY_MAX_TIME=00001    decimal=1    installer_rc=13 real_curl_rc=0
cai_actionlint: `AL_RETRY_MAX_TIME` phai trong 1..1800 giay (duoc '00001')
AL_RETRY_MAX_TIME=8        decimal=8    installer_rc=0  real_curl_rc=0
AL_RETRY_MAX_TIME=00008    decimal=8    installer_rc=13 real_curl_rc=0
AL_RETRY_MAX_TIME=300      decimal=300  installer_rc=0  real_curl_rc=0
AL_RETRY_MAX_TIME=000300   decimal=300  installer_rc=13 real_curl_rc=0
AL_RETRY_MAX_TIME=1800     decimal=1800 installer_rc=0  real_curl_rc=0
AL_RETRY_MAX_TIME=0001800  decimal=1800 installer_rc=13 real_curl_rc=0
```

- `review_checks.py hunts` đo riêng MAX_TIME=08/0099 qua AL_GOI đều rc0; RETRY=08,DELAY=0099 qua tải curl thật cũng rc0.
- Kết luận: **LỖI F1**; không có lỗi bát phân với chuỗi ngắn nhờ `10#`.

### HƯỚNG 2: tràn số và khoảng MAX_TIME

- Giả thuyết: 18446744073709551617 tràn thành 1 rồi qua.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_checks.py hunts`, nhóm `range-overflow`.
- Output thật từ hunts.json: MAX_TIME=0,1801,18446744073709551617,999999999999999999999999999999 ⇒ mỗi cái `rc:13,extracted:false`, thông điệp giữ giá trị. 1e3,` 8`,+8,-1 ⇒ rc13 bởi regex. MAX_TIME=1800 ⇒ rc0.
- Kết luận: **KHÔNG PHẢI LỖI** ở các giá trị này; bảo vệ chống tràn hoạt động và cần giữ khi vá F1.

### HƯỚNG 3: `set -u`, indirect expansion, unset/rỗng

- Giả thuyết: `${!nut}` làm nổ shell hoặc chuỗi rỗng tự đổi thành mặc định.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_checks.py hunts`, nhóm `unset-set-u`, `explicit-empty`.
- Output thật: cả ba núm unset ⇒ `rc:0,stderr:"",stdout_exact:true`; từng núm đặt rỗng ⇒ rc13, stdout rỗng, `phai la so nguyen khong dau (duoc '')` kèm đúng tên biến.
- Kết luận: **KHÔNG PHẢI LỖI**. Biến đều khởi tạo trước vòng indirect; `${VAR-default}` phân biệt unset/rỗng đúng.

### HƯỚNG 4: AL_GOI có bắt đầu tải ngầm không

- Giả thuyết: retry bị bọc rộng làm đường offline gọi curl hoặc đổi stdout.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_checks.py hunts`, nhóm `offline-no-curl-parity`, installer thật chạy bằng bash -x, base lấy từ git show.
- Output thật: base/HEAD đều `rc:0,curl_called:false,downloaded_hash:null,stdout_exact:true,extracted:true`.
- Kết luận: **KHÔNG PHẢI LỖI** với cấu hình hợp lệ đã đo. Từ chối chuỗi MAX_TIME hợp lệ ở đường offline là cùng F1, không đếm thêm finding.

### HƯỚNG 5: stdout/độ trễ lần tải đầu thành công

- Giả thuyết: in thêm hoặc chờ ngay cả khi thành công lần đầu.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_checks.py hunts`, nhóm `first-success-stdout-time`.
- Output thật: base `rc:0,seconds:0.0264,stdout_exact:true,stderr:""`; HEAD `rc:0,seconds:0.0328,stdout_exact:true,stderr:""`; băm gói tải bằng curl thật trùng fixture.
- Kết luận: **KHÔNG PHẢI LỖI** trong phép file://. Không suy ra số yêu cầu HTTP/latency mạng từ phép này.

### HƯỚNG 6: tệp dở/gói sai có lọt cổng băm không

- Giả thuyết: tệp cũ/tải nửa thân bị giải nén/chạy sau retry.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_checks.py hunts`, nhóm `partial-preseed-overwrite`, `bad-hash-no-extract`, `partial-body-hash`.
- Output thật: tạo trước nửa tệp đích rồi tải file:// đúng ⇒ rc0,băm đích đúng. Gói khác băm nhưng binary tự khai đúng bản ⇒ `rc:9,extracted:false`, marker không tồn tại. Nguồn bị cắt nửa ⇒ `rc:9,extracted:false`.
- Kết luận: **KHÔNG PHẢI LỖI** cổng băm/thứ tự đã đo. Khôi phục sau HTTP rc18 là **KHÔNG ĐO ĐƯỢC**; file:// không phát sinh HTTP partial retry.

### HƯỚNG 7: retry-max-time có cắt giữa lần tải đang chạy không

- Giả thuyết: MAX_TIME không phải hạn cứng toàn bộ quá trình tải.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_extra_checks.py`; phép con: `curl -fsSL --retry 8 --retry-all-errors --retry-max-time 1 -o <tmp>/slow-out file://<tmp>/slow-file`. FIFO thật ghi 1024 byte, chờ 2,2s rồi ghi thêm 1024 byte.
- Output thật: `test:retry-max-time-is-not-in-flight-deadline,rc:0,seconds:2.206,bytes:2048,stderr:""`.
- Kết luận: **KHÔNG PHẢI LỖI diff so các cờ M1**. Đây không phải hạn cứng giữa lượt tải. Cụm mô tả "trần TỔNG"/khoảng 300s không bảo đảm wall-clock; connect-timeout cũng không hạn đọc thân. Không áp thêm max-time ngoài spec. Manual cục bộ xác nhận, lưu `curl-manual-retry-max-time.txt`.
- Phép đầu dùng limit-rate trên file thường trả đủ 4096 byte sau 0,009s nên không dùng làm chứng cứ hạn thời gian; phép FIFO mới tạo độ trễ thực.

### HƯỚNG 8: retry thật, trần và thông điệp loi4

- Giả thuyết: cờ thêm vào nhưng retry/trần không có tác dụng hoặc thiếu thông tin log.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_extra_checks.py`; nguồn file:// chưa tồn tại, luồng tạo sau 2,5s; DELAY=1,MAX_TIME=10.
- Output thật: mặc định ⇒ `rc:0,seconds:3.035`, 3 lỗi curl37 trước thành công. RETRY=2 ⇒ `rc:4,seconds:2.017`, `tai ve that bai sau toi da 1+2 lan thu (AL_RETRY=2, cach 1s, tran 10s)`. MAX_TIME=1 ⇒ `rc:4,seconds:1.016`, `toi da 1+8 ... tran 1s`.
- Kết luận: **KHÔNG PHẢI LỖI** ở cơ chế retry lỗi file thực. Không tính đây là D1/D2 hoặc đếm HTTP.

### HƯỚNG 9: chập chờn, proxy và capability loopback

- Giả thuyết: một lần t237 đỏ do proxy/chập chờn hoặc sản phẩm.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_checks.py required` (3 lượt t237), và `python3 -B review_checks.py hunts` (probe socket).
- Output thật: cả 3 `lease_publish: 0/1 đạt`, `PermissionError: [Errno 1] Operation not permitted`; traceback probe tại `_socket.socket.__init__` trước bind, chưa vế D nào chạy.
- Kết luận: **KHÔNG ĐO ĐƯỢC** chập chờn/tính đúng HTTP. Sandbox cấm tạo socket AF_INET, trước curl; test đã đặt cả hai NO_PROXY. Không nhận 3 lần đỏ hạ tầng làm 3 chứng cứ lỗi code.

### HƯỚNG 10: server giữ trạng thái hay trả giả cố định

- Giả thuyết: server luôn trả đúng ở lần hai bất kể lịch sử.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_extra_checks.py`, nhóm `handler-state-supplement-only-no-http`. Thay constructor server bằng bộ giữ lớp handler, gọi do_GET 4 lần với BytesIO; không thay curl/installer hoặc chấm t237 bằng phép này.
- Output thật: kịch bản 504,cat(abcdef),goi(abcdef) ⇒ status 504/200/200/200; counter 1/2/3/4; thân `gateway timeout\n`/`abc`/`abcdef`/`abcdef`; lần cat vẫn khai Content-Length=6.
- Kết luận: **KHÔNG PHẢI LỖI** logic giữ trạng thái đã đo; **KHÔNG ĐO ĐƯỢC** HTTP end-to-end, scheduling và đóng socket thật. Phép bổ sung không nâng D1–D6 thành đạt.

### HƯỚNG 11: curl cũ và Git Bash Windows

- Giả thuyết: curl cũ không nhận retry-all-errors và lỗi trước tải.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_extra_checks.py`, probe các đường curl thông dụng, và `curl --manual`.
- Output thật: /usr/bin/curl,/bin/curl đều `curl 8.5.0 ... x86_64-pc-linux-gnu`; không có /usr/local/bin/curl; manual ghi retry-all-errors được thêm ở 7.71.0.
- Kết luận: **KHÔNG ĐO ĐƯỢC** curl cũ/Windows. Không giả option lỗi để khai đã đo nền đích; chưa có finding độc lập với bằng chứng Windows.

### HƯỚNG 12: miền số của curl nhỏ hơn regex

- Giả thuyết: chuỗi chữ số vẫn có thể bị curl từ chối trước tải.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_checks.py hunts`, nhóm `curl-numeric-capacity`.
- Output thật: RETRY hoặc DELAY=18446744073709551617 ⇒ installer rc4; stderr `curl: option --retry: too large number` hoặc `curl: option --retry-delay: too large number`, rồi thông điệp loi4.
- Kết luận: **KHÔNG PHẢI LỖI đã chứng minh so M2**: spec chỉ quy định regex cho RETRY/DELAY, không quy định khoảng tối đa hai biến này. Không biến khoảng trống spec thành P2 của implementation. MAX_TIME ngoài khoảng vẫn rc13 đúng như Hướng 2.

## KIỂM PHẠM VI VÀ TÍNH TOÀN VẸN

Các lệnh đã chạy:

```text
git -C cay-kho diff --name-status fe84620f HEAD
M ops/cai_actionlint.sh
M ops/lease_publish_test.py

git -C cay-kho diff --numstat fe84620f HEAD
33  3  ops/cai_actionlint.sh
145 0  ops/lease_publish_test.py
```

Đúng **2 tệp, 178 dòng thêm ≤250**. `git diff --check fe84620f HEAD` rc0. Diff workflows rỗng; không đổi hook, wrapper, công cụ khác ngoài write_set.

`review_extra_checks.py` đối chiếu SequenceMatcher/AST, output thật:

```json
{"changes":[{"kind":"insert","old_lines":[14596,14596],"new_lines":[14596,14741]}],"old_definitions_changed":[],"new_definitions":["_MayChuGoiT237","t237_cai_actionlint_retry_song_qua_5xx"]}
```

Phần test chỉ chèn một khối 145 dòng, gồm t237 và helper riêng; mọi định nghĩa cũ giữ nguyên. Không chỉ dựa số dòng xóa=0.

`PYTHONDONTWRITEBYTECODE=1 python3 review_checks.py snapshot-after` đã chạy sau khi hai suite kết thúc. Snapshot đầu/cuối đều **12.248 tệp**, bao gồm tệp tracked/untracked/ignored ngoài metadata `.git`: `added:[]`, `removed:[]`, `changed:[]`. Hai tệp snapshot có cùng SHA-256 `dd21d0068c7518be6b1f92b79e58793690467da16d9916c81893bc41396b3592`. `git status --porcelain=v1 --untracked-files=all --ignored=matching` trước/sau đều rc0, output rỗng. HEAD/tree cuối khớp mốc review. Log ở `source-status-{before,after}.log`, `snapshot-{before,after}.json`, `final-integrity.json`.

Giới hạn: snapshot đầu được ghi sau các kiểm ban đầu và không băm metadata Git; đây là bằng chứng không có delta nội dung quan sát được giữa hai mốc, không chứng minh chưa từng ghi rồi hoàn nguyên trong toàn lịch sử. Các lệnh Python đã tắt bytecode, Ruff no-cache; mọi bản sao thử nghiệm tách khỏi nguồn. Sandbox thực tế workspace-write; quy tắc read-only của vai reviewer được tuân thủ trong các thao tác.

## BẢNG LỚP

| Slug lớp | Finding / biểu hiện | Hạng mở | Nguồn | Cách vá chung / đóng lớp |
|---|---|---|---|---|
| retry-max-time-decimal-equivalence | F1: 00001,00008,00099,000300,0001800 bị từ chối trên đường tải/AL_GOI | P2 | lượt 1, SHA 43258fbe43d2b1508cdb0a00dc1ba436f28968c5 | Chuẩn hóa 0 đứng đầu trước kiểm độ dài/khoảng; kiểm ca dương và âm tràn/ngoài khoảng. |

1 lớp/1 finding. Những cách viết cùng cơ chế không đếm riêng; giới hạn HTTP/Windows và dự đoán mutation không phải finding đã chứng minh.

## FINDINGS

### retry-max-time-decimal-equivalence  [P2]  Từ chối MAX_TIME hợp lệ có nhiều số 0 đứng đầu

**TỆP/DÒNG:** `ops/cai_actionlint.sh:68–70`, hunk mới.

**VẤN ĐỀ:** M2 cho phép `^[0-9]+$` khi giá trị MAX_TIME trong 1..1800, không hạn số 0 đứng đầu. `${#AL_RETRY_MAX_TIME} > 4` xét chuỗi gốc khiến 00001 (1 giây),00008 (8),000300 (300),0001800 (1800) đều loi13 trước cài. 0001 lại được nhận. Cấu hình hợp lệ bị từ chối trên cả đường tải và AL_GOI. Đây không phải lỗi bát phân hoặc đầu vào curl không hỗ trợ.

**ĐÃ THỬ NGHIỆM:** `PYTHONDONTWRITEBYTECODE=1 python3 repro_max_time.py`, gói tar hợp lệ/băm đúng, installer thật và curl thật qua file://. Các cặp 1/00001,8/00008,300/000300,1800/0001800 cho installer rc0/13 trong khi curl thật luôn rc0 cùng cờ/giá trị. Log: `review-evidence/repro-max-time.log`. Hướng 1 ghi output. Không cần socket nên không vướng EPERM t237.

**ĐỘ TIN:** cao. Mỏ neo thuộc hunk mới; đầu vào, mã thoát, stderr và đối chứng curl đều đã chạy. Tác động là sai hợp đồng đầu vào, không có bằng chứng vượt cổng băm hay ảnh hưởng các mặc định chuẩn.

**GỢI Ý VÁ (HINT):** ở khối M2 sau regex, bỏ 0 đứng đầu bằng xử lý chuỗi vào giá trị dùng để kiểm; chuỗi toàn 0 vẫn từ chối. Chỉ kiểm độ dài/khoảng trên dạng thập phân chuẩn hóa rồi mới làm số học; giữ đầu vào gốc cho chẩn đoán. Không chỉ bỏ bảo vệ độ dài vì sẽ tái mở tràn số.

**CA TEST KHÓA:** thêm ca dương cho 1,08,0099,00001,00008,000300,0001800 và hàng chục số 0 trước 1 ⇒ rc0 trên gói đúng; giữ ca âm 0,00000,1801,0001801,18446744073709551617,abc,rỗng ⇒ rc13. Không sửa các ca có sẵn.

**BẢN VÁ CÓ THỂ ĐẺ RA GÌ:** chuẩn hóa chuỗi toàn 0 thành rỗng làm lỗi toán hạng; số học quá sớm tái tạo tràn hoặc bát phân. Cần giữ regex và bảo vệ độ dài sau chuẩn hóa. Reviewer chưa thử bản vá implementation, không xuất patch runtime cho installer sensitive và không sửa nguồn.
