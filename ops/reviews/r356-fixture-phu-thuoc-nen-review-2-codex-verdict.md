```yaml
verdict: approve
reviewed_sha: 581afd26b2d8d990385fc82f5a4d9f6e916bbd8c
base_sha: 1b3caa11df3e339bcfdb52be903884b5b99b9f77
reviewer: codex
executor: claude
luot: 2
P1: 0
P2: 0
```

## Findings

Không còn finding P1/P2 của lượt 1; không phát hiện finding P1/P2 mới do bản vá lượt 2. `approve` áp dụng cho bản vá fixture trên exact SHA này. Các giới hạn đo Windows, Linux, CI từ xa và lời khai “rủi ro thực tế bằng 0” được phân biệt dưới đây.

Review trực tiếp bằng Codex/OpenAI qua công cụ shell cục bộ, độc lập với executor Claude được khai trong packet. Một sub-agent Codex chỉ đọc hiện vật/log để đối chiếu; không tính nó là một lượt cross-provider khác. Tree đã kiểm: `90fbc03820763d40ddc29c99df1b35f845ee47b2`.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Finding lượt 1 | Phân loại | Bằng chứng tự đo |
|---|---|---|
| P1-01 — sentinel có thể làm marker đúng | **ĐÃ VÁ THẬT** | Mệnh đề mới là `P and not P`; 512 tổ hợp cho `False`, 0 `True`; gỡ lọc giết đúng hàng bằng `TinHieuChotCa`. |
| P2-01 — hash A/B Linux không thuộc exact head | **ĐÃ VÁ THẬT** về lỗi neo băm | Git blob head dài 432225 byte, SHA-256 bắt đầu `966a33ec3d9a4da1`, trùng checkout. Nguyên nhân băm trung gian được tái lập trên Git blob lượt 1. Việc executor đã chạy lại A/B Linux vẫn chưa được reviewer đo độc lập. |

`SPEC.md` còn header SHA lượt 1; SHA lượt 2 được chỉ định tường minh bởi `PROMPT.md` và khớp mirror. Không dùng header cũ làm reviewed SHA.

## Phán định A-G

### A. Marker sai trên mọi giá trị của môi trường marker

**Đạt; đóng P1-01.** Dòng `.claude/dev/launcher_test.py:6453` dùng:

```text
khong_he_ton_tai_r345; sys_platform == "win32" and sys_platform != "win32"
```

Với cùng giá trị chuỗi `s = sys_platform`, hai vế lần lượt là `s == "win32"` và phủ định của nó. Không giá trị chuỗi hợp lệ nào làm cả hai đúng. Những biến khác, kể cả `os_name`, `platform_system`, `python_version`, không xuất hiện trong biểu thức nên không thể đổi kết quả. Đây là lập luận theo cấu tạo; tập mẫu hữu hạn dưới đây là phép kiểm bổ sung, không phải chứng minh bằng liệt kê mọi môi trường.

Đo bằng parser vendored của **pip 24.3.1** trong venv thật, Python **3.13.1**, Windows build **26200**:

| Môi trường truyền vào `evaluate` | Sentinel cũ | Mâu thuẫn mới |
|---|---:|---:|
| Mặc định | False | False |
| `sys_platform=khong_he_co` | True | False |
| `sys_platform=win32` | False | False |
| `sys_platform=linux` | False | False |

Ma trận `8 sys_platform × 4 os_name × 4 platform_system × 4 python_version = 512`: **512 False, 0 True**, child rc=0, stderr rỗng. Đổi riêng từng khóa trong 11 khóa của `default_environment()` cũng đều False. Trong venv đối chứng, `pypdf=3.17.4` và distribution `khong_he_ton_tai_r345` **vắng mặt**, được hỏi trực tiếp bằng `importlib.metadata.distribution`.

### B. Neo băm vào đúng head

**Đạt; đóng P2-01 về hash không khớp.** Tự hash byte thô từ `git show`, không hash chuỗi đã qua chuyển đổi newline:

| Revision | Byte | SHA-256 đầy đủ |
|---|---:|---|
| `1b3caa11df3e339bcfdb52be903884b5b99b9f77` | 429027 | `009f8e6a1cbc640033c48c79bdd400ab214934382d9078bda8f7e8f5627bdc25` |
| `867dd8585770a6d9e63bfe6feb870bca92d2aecb` | 431295 | `b899cb29c0d3295c0213693672fb50473f1ef4033f325773afd66e14656c0ec0` |
| `581afd26b2d8d990385fc82f5a4d9f6e916bbd8c` | 432225 | `966a33ec3d9a4da1a4b2235b92733eddd90e9b9079fbdc6763ba2a69de341574` |

Byte checkout tại head bằng byte Git blob. Thay đúng **3** lần `r355→r354` trong blob **867dd858…** cho `123529a62160ece153771c51ac6cf6958927b5bc23dd1e5b129f2500d65e59b6`: nguyên nhân băm cũ executor khai được tái lập.

Lời khai đổi `r355→r354` ra băm trung gian chỉ tái lập được trên **head lượt 1** vừa được nhắc tại `commit-message.txt:30` / `CHANGELOG.md:81`. Thay trên head lượt 2 có 4 lần và cho `d70f7a085d7918948abeff50972376daa94922b200001d3da801a625de931a3e`, không phải băm trung gian. Không nhập hai revision này làm một.

Hash đúng không tự chứng minh đã thực thi A/B Linux. Các kết quả A/B và lời khai script “thoát 3 nếu lệch” trong `EVIDENCE.md:31-45`: **KHÔNG ĐO ĐƯỢC độc lập** trong lượt review Windows này; bundle không kèm script/log A/B gốc để kiểm đường thoát ấy.

### C. Gỡ lọc marker phải làm đúng hàng đỏ

**Đạt trên Windows.** Đã chạy hàm ca đích thật và hàm ca ba đột biến thật, cả hai trả `None`, không trả chuỗi bỏ qua/KHÔNG ĐO ĐƯỢC.

Đột biến sống duy nhất:

```python
goc = M._r338_than_hook
neo = "            if _r.marker is not None and not _r.marker.evaluate():"
assert goc().count(neo) == 1
M._r338_than_hook = lambda: goc().replace(neo, "            if False:")
M.r345_cac_phep_do_cuc_bo_van_dung()
```

Số đo: `anchor_count=1`; ngoại lệ **đúng lớp `M.TinHieuChotCa`**, thông điệp **đúng nguyên văn**:

```text
phep do cuc bo sai: marker khong khop: duoc 1, mong 0
```

Chạy riêng child với chỉ dòng marker của bảng và cùng mutant: **rc=1**, stderr rỗng, stdout:

```text
[session-start] requirements.txt CHUA THOA: khong_he_ton_tai_r345: VANG MAT (khong co metadata)
```

Do đó lỗi đến từ distribution của hàng cần khóa; không ghi công ngoại lệ vô can. Hook và test trong repository không bị sửa trên đĩa. Trên Linux: **KHÔNG ĐO ĐƯỢC độc lập**; chỉ có lời khai executor.

### D. Chuỗi ca đột biến có khớp hàng bảng không

**Đạt.** Trích literal từ AST của hai hàm: chuỗi tại dòng **6453** và **6530** bằng nhau cả **75 byte UTF-8**, gồm newline cuối; ca đột biến có đúng **1** literal requirements bắt đầu bằng tên sentinel. Bảng có đúng **10** hàng.

Đã chạy riêng cả 10 hàng trong cùng venv thật:

| Hàng | Actual / expected |
|---|---:|
| `ban thoa` | 0 / 0 |
| `lech ban` | 1 / 1 |
| `marker khong khop` | 0 / 0 |
| `marker chua dau thang` | 0 / 0 |
| `chu thich sau khoang trang` | 0 / 0 |
| `URL tran toi host chet` | 0 / 0 |
| `VCS git+http` | 0 / 0 |
| `goi VANG MAT + direct ref` | 1 / 1 |
| `goi CO MAT + direct ref` | 0 / 0 |
| `goi thieu han` | 1 / 1 |

Chín hàng còn lại không thay đổi ở lượt 2. Hàng `os_name == "posix#x"` vẫn có kỳ vọng 0 ở cả nhánh bỏ qua và nhánh kiểm gói `pypdf` đã cài. Nợ về bộ lọc comment được khai riêng, không phải hồi quy của bản vá lượt 2.

### E. Bộ đầy đủ Windows và tự đột biến

Đã chạy trực tiếp file exact head, không thay nội dung suite. Thư mục tạm, cache pip và profile kiểm thử được đặt dưới `C:/tl458c/review-scratch`; bytecode bị tắt. Cấu hình tái lập nằm ở `review-env.ps1`.

| Lượt | Passed | Failed | Skipped / không đo được | Tổng | rc |
|---|---:|---:|---:|---:|---:|
| Full Windows, cấu hình phiên review cô lập | 164 | 1 | 17 skipped | 182 | 1 |
| Full Windows, `CI=true` | 165 | 0 | 17 skipped | 182 | 0 |
| `--dot-bien`, cấu hình phiên review cô lập | 160 | 0 | 11 không đo được | 171 | 0 |

Lượt đầu đầy đủ **thật sự failed**, không được đổi thành pass: `164/165 ca DA CHAY QUA (tong 182, bo qua 17, hong 1)`. Lỗi duy nhất là `t53_doctor_bao_du_khi_du`, child doctor rc=12, `thieu_bat_buoc=["claude"]`; CLI `co=True` nhưng `xac_thuc_ok=False`. Đây không phải lỗi marker.

Đã chạy lại **chính ca t53** từ byte Git của base, lượt 1 và lượt 2 trong cùng rig: cả ba ném `TinHieuChotCa`, cùng doctor rc=12 và cùng `thieu_bat_buoc=["claude"]`. Mỗi vế tự hash file test và kiểm launcher byte-identical với head. Đối chứng này chứng minh lỗi xác thực có sẵn trong rig; không suy ra tổng full base bằng cách chỉ chạy một ca.

Lượt `CI=true` dùng nhánh đã có trong `_bat_buoc` (`launcher.py:2014`), nơi công cụ agent không bắt buộc cho runner kiểm thử; không mock doctor, không bỏ ca t53 và không sửa test. Kết quả hoàn tất: **165/165 ca DA CHAY QUA (tong 182, bo qua 17, hong 0)**, rc=0; số ca khớp lượt 1. Đây là phép chạy local với cấu hình CI, không phải kết quả hosted GitHub Actions.

Tự đột biến kết thúc đúng `DOT BIEN: 160/160 dat (11 khong do duoc tren nen nay)`, khớp lượt 1. Đếm log độc lập đúng 160 dòng OK và 11 dòng KHÔNG ĐO ĐƯỢC.

### F. Phạm vi lời khai

**Lời khai thu hẹp về caller đúng; kết luận “rủi ro thực tế bằng 0” cần hiểu trong phạm vi hẹp, không phải một bảo đảm tuyệt đối đã được đo.** AST thân hook cho đúng một lời gọi `evaluate`, **0 đối số, 0 keyword**; `session-start.sh:369` khớp. Thử đặt biến môi trường tiến trình `sys_platform` và `SYS_PLATFORM` thành sentinel không đổi môi trường marker thật: vẫn `win32`, sentinel cũ vẫn False.

Vì vậy phản chứng lượt 1 truyền dict vào `evaluate({...})` không chứng minh đầu vào đó tới được qua hook. P1-01 của lượt 1 được xác nhận ở yêu cầu **fixture sai theo cấu tạo**, không phải bằng chứng một lỗ khai thác thực tế trong hook.

Tuy nhiên `evaluate()` không đối số không chứng minh `sys.platform` bất biến: phép thử tổng hợp sửa `sys.platform` ngay trong interpreter cho **sentinel cũ/no-args=True**, **marker mới/no-args=False**. Phép thử này đã thêm can thiệp mã Python vào môi trường; nó **không** chứng minh hook cho phép một tác nhân làm việc đó. Bởi vậy không dựng P1/P2 runtime mới từ phép ép này, đồng thời không nhận câu “rủi ro thực tế bằng 0” tại `commit-message.txt:8`, `CHANGELOG.md:68`, `launcher_test.py:6448` làm chứng nhận mọi môi trường. Cách diễn đạt chính xác hơn: “Đường override của phản chứng lượt 1 không được caller hook cung cấp; chưa chứng minh được lỗi reachable trong đường hook thật đã đo.” Đây là lưu ý về phạm vi lời khai, không phải finding chặn bản vá fixture.

Các con số còn lại được phân loại như sau:

| Lời khai | Kết quả kiểm |
|---|---|
| Bốn môi trường marker, ca đích, ba đột biến và gỡ lọc trên Windows | Tự đo lại, khớp; xem A/C/D. |
| `966a33ec…`, `009f8e6a…`, `b899cb29…`, nguồn gốc `123529a6…` | Tự tính, khớp với đúng revision; xem B. |
| `165/165`, `tong 182, bo qua 17`; `160/160` | Đối chiếu theo từng cấu hình ở E; không gán kết quả CI cho lượt cấu hình phiên agent. |
| Linux WSL Python 3.12.3, A/B hai ca lỗi, delta=0 | **KHÔNG ĐO ĐƯỢC độc lập** trong phiên này; lời khai executor. |
| CI lượt 1: Windows 4m11s, Ubuntu 2m41s, gate 21m25s; `181/181`, `170/170`, bỏ qua 1 | **KHÔNG ĐO ĐƯỢC độc lập** từ bộ hiện vật hiện có. `EVIDENCE.md:47-56` gắn rõ với `867dd858…`, không dùng cho `581afd26…`. |
| Các run lịch sử `34023635438`, `34025725347`, `34050306986`, trạng thái success/approve | Không có log/receipt CI gốc được kiểm trong lượt này; **KHÔNG ĐO ĐƯỢC độc lập**. Không dùng số run làm bằng chứng pass. |
| CI tại `581afd26…`, nhãn PR `windows`, tình trạng chạy hiện tại | **KHÔNG ĐO ĐƯỢC độc lập** qua review local này. Reviewer không truy vấn CI; không có nghĩa CI chưa chạy. Câu “ĐANG CHẠY lúc soạn” là snapshot của executor, không phải trạng thái hiện tại đã xác minh. |

Đoạn “Bản vá” ở `CHANGELOG.md:30` còn kể sentinel lượt 1; mục cross-review ngay sau đó ghi nhận phản chứng và thay bằng mâu thuẫn. Không dùng câu lịch sử “sai trên MỌI nền” ấy làm mô tả literal đang chạy. `commit-message.txt` khớp thông điệp Git sau chuẩn hóa newline cuối.

### G. Finding mới do bản vá lượt 2

**Không phát hiện P1/P2 mới trong phần đã đo.** Chuỗi mới parse được, luôn False theo cấu tạo, hai nơi dùng chuỗi đồng nhất, và phản chứng đúng hàng vẫn có răng. Các lỗi/giới hạn môi trường ở E/F được giữ riêng, không đổi tên thành lỗi do patch.

`git diff --check base head`: rc=0. `diff.patch` bằng đúng byte Git diff (10685 byte); numstat khớp: `launcher_test.py +41/-3`, `CHANGELOG.md +92/-0`. `doc-claims-check --strict`: rc=0, `ok=true`, 106 tệp, `claims_flagged=366`, **0 flags**. Cổng tài liệu này không chứng minh các lời khai Linux/CI ngoài bundle.

Kiểm lại sau mọi phép đo: mirror **sạch**, HEAD vẫn `581afd26b2d8d990385fc82f5a4d9f6e916bbd8c`, tree vẫn `90fbc03820763d40ddc29c99df1b35f845ee47b2`; tệp test checkout vẫn bằng Git blob. Không có commit, push hay sửa nguồn trong mirror.

## Lệnh tái lập và hiện vật đo

Chạy trong `C:/tl458c/cay-kho`. Các script dưới đây đã thực thi; chỉ viết scratch ngoài mirror, trong `C:/tl458c`:

```powershell
. C:\tl458c\review-env.ps1
python -B -u C:\tl458c\probe-review.py
python -B -u C:\tl458c\probe-regression.py
python -B C:\tl458c\run-suite.py full
python -B C:\tl458c\run-suite.py full-ci
python -B C:\tl458c\run-suite.py mutation
git diff --check 1b3caa11df3e339bcfdb52be903884b5b99b9f77 581afd26b2d8d990385fc82f5a4d9f6e916bbd8c
python -B scripts/tl.py doc-claims-check --strict
```

`run-suite.py full-ci` đặt `CI=true` chỉ cho tiến trình kiểm thử của lượt đó. Hai mode full đều gọi nguyên `.claude/dev/launcher_test.py --nhat-ky ...`; mode mutation gọi nguyên file với `--dot-bien`. Không dựng chuỗi đường dẫn thoát cây cho phản chứng mới.

Log/số đo: [probes.json](review-scratch/probes.json), [regression.json](review-scratch/regression.json), [full.log](review-scratch/full.log), [full.result.json](review-scratch/full.result.json), [full-ci.log](review-scratch/full-ci.log), [full-ci.result.json](review-scratch/full-ci.result.json), [mutation.log](review-scratch/mutation.log), [mutation.result.json](review-scratch/mutation.result.json), [doc-claims.json](review-scratch/doc-claims.json). Nhật ký full có từng lượt vào/ra để kiểm số ca thực chạy.

## Sai lệch thủ tục của phiên review

Trước khi đọc được giới hạn thư mục trong `PROMPT.md`, reviewer đã tra nhanh mục lục memory bên ngoài `C:/tl458c` theo chỉ dẫn preflight của môi trường. Đây là một lần đọc ngoài phạm vi đã được thông báo ngay; không dùng kết quả đó làm bằng chứng cho A-G. Sau khi nhận giới hạn, các lệnh đọc hiện vật, script và output review được giới hạn trong thư mục được giao. Sai lệch này không được giấu dưới kết quả test xanh.
