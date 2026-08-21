## Findings

### 1. `GOI_WRAPPER_THUC_THI` — chính cơ chế được dựng lên để đóng finding #4 (lượt 1) vẫn còn lỗ, và chú thích bên cạnh KHAI SAI rằng nó kín — P2

`t35` nay đòi mọi bước gọi wrapper phải khớp một trong hai chuỗi canonical trong `GOI_WRAPPER`, nếu không thì ĐỎ. Nhưng bước "gọi wrapper" chỉ được **nhận diện** để đưa vào phép so khớp đó khi khớp `GOI_WRAPPER_THUC_THI` — một regex neo `^` với tập token dẫn đầu hẹp (`bash|sh|exec` rồi trực tiếp `\S*` tới tên tệp). Bất kỳ hình dạng lệnh nào không khớp regex NHẬN DIỆN này thì rơi thẳng vào `goi_wrapper = []` → `continue` (dòng 1434-1435) — tức **được miễn hoàn toàn**, không phải bị từ chối. Đây đúng cấu trúc lỗ mà finding #4 lượt 1 mô tả, chỉ đổi chỗ: trước đây danh sách CHO PHÉP quá hẹp; nay bước NHẬN DIỆN LỜI GỌI quá hẹp, nên allowlist không bao giờ được hỏi tới với các hình dạng này.

**Bằng chứng đo được — trên bản sao tạm `exp7_*` (từ `plat-x5-head`), thiếu `AL_VER` trong cả sáu biến thể, `rc` đọc trực tiếp:**

```text
A_env_prefix_thieu_ALVER       rc=0  40/40  KHONG-DO  (run: env AL_X=1 bash ops/chay_lease_publish_test.sh)
B_bash_c_thieu_ALVER            rc=0  40/40  KHONG-DO  (run: bash -c 'bash ops/chay_lease_publish_test.sh')
C_command_prefix_thieu_ALVER    rc=0  40/40  KHONG-DO  (run: command bash ops/chay_lease_publish_test.sh)
E_github_workspace_co_khoang... rc=0  40/40  KHONG-DO  (run: bash ${{ github.workspace }}/ops/chay_lease_publish_test.sh)
```

Đối chứng — hai dạng regex THỰC SỰ nhận diện được thì bị từ chối đúng như thiết kế:

```text
D_absolute_path_thieu_ALVER               rc=1  ĐỎ t35  "ngoài danh sách canonical" + "thiếu AL_VER"
F_github_workspace_khong_khoang_trang...  rc=1  ĐỎ t35  "ngoài danh sách canonical" + "thiếu AL_VER"
```

Bốn trong sáu biến thể — cả bốn dạng nêu đúng trong nhiệm vụ §3.4 (`env AL_X=1 bash …`, `bash -c '…'`, `command bash …`) cộng một dạng thứ năm tôi tự thêm (`${{ github.workspace }}` có khoảng trắng, cách viết chuẩn phổ biến trong tài liệu GitHub Actions) — **không hề được nhận diện là một lời gọi**, nên nghĩa vụ `AL_VER` biến mất hoàn toàn với chúng. Lý do kỹ thuật: `\S*` không vượt được khoảng trắng, nên bất cứ token nào chen giữa `bash`/`sh`/`exec` và đường dẫn (`-c`, `env X=1`, `command`, hay khoảng trắng bên trong `${{ … }}`) đều làm regex thất bại NGAY TỪ BƯỚC NHẬN DIỆN — khác với dạng đường dẫn tuyệt đối hay `${{github.workspace}}` không khoảng trắng, nơi `\S*` vẫn nối liền được tới tận `chay_lease_publish_test.sh`.

Chú thích ngay trên định nghĩa regex (dòng 1412-1414) khẳng định:

```text
# Nhận diện theo token lệnh dẫn đầu để không báo oan dòng `sha256sum` chỉ in
# băm wrapper. Ngoài hai dạng canonical vẫn là một LỜI GỌI, và vì allowlist
# đang gác nghĩa vụ `AL_VER`, dạng ngoài danh sách phải ĐỎ chứ không được miễn.
```

Câu "**Ngoài hai dạng canonical vẫn là một LỜI GỌI**" là **SAI** theo phép đo trên: bốn/năm dạng không hề được coi là "một lời gọi" — chúng vô hình với `t35`, y hệt cách `sha256sum ops/…` vô hình với `t25`. Đây không phải một giới hạn được khai đúng phạm vi (như `t34` đã sửa ở finding #3 lượt 1); nó là một **khẳng định sai** về chính cái mà finding #4 lượt 1 yêu cầu đóng.

**Vì sao không phải finding vô hại kiểu "sở thích kiến trúc":** đặc tả revision 3, mục "TRONG phạm vi lượt 3, việc 2" viết nguyên văn *"nhận diện bước gọi wrapper theo **có nhắc** `chay_lease_publish_test.sh` **trong một lệnh thực thi**"* — tức đặc tả đòi khớp theo NỘI DUNG lệnh, không đòi neo `^` ở đầu chuỗi. Bản vá thực thi hẹp hơn đúng cái đặc tả đã yêu cầu, và khoảng hở giữa hai bên chính là bốn dạng đo được ở trên.

**Mức độ hậu quả — nói rõ để không phóng đại:** `ops/cai_actionlint.sh` tự nó **vẫn** đòi `AL_VER` khớp `X.Y.Z` (dòng 43-44, `loi 2` nếu thiếu/sai), bất kể `chay_lease_publish_test.sh` được gọi bằng cú pháp nào. Nên hậu quả **không im lặng ở lượt chạy CI thật**: job `gate` vẫn đỏ với rc=2 nếu ai đó vô tình bỏ `AL_VER` dưới một trong bốn dạng trên. Cái mất là **lớp phòng trước** — `t35` chạy độc lập, kể cả ngoài CI (offline, `python3 ops/lease_publish_test.py`) — và cái mất thứ hai, nặng hơn về nguyên tắc: một chú thích trong write set của chính packet này đang khẳng định sai về độ phủ của chốt nó vừa dựng. Theo đúng khung nhiệm vụ mục 3.4: *"lọt-mà-đã-khai là nợ; khai thiếu là finding"* — đây không chỉ khai thiếu, mà khai **ngược**, nên xếp P2 (cùng hạng với finding #3 lượt 1, vốn cũng là một khoảng hở giữa lời khai và phép đo trên cùng một họ cơ chế).

**Invariant bị cắt:** `CLAUDE.md` — *"PHẠM VI TUYÊN BỐ phải bằng phạm vi ĐO ĐƯỢC"* và *"Danh sách CẤM không bao giờ đủ — phải đảo thành danh sách CHO PHÉP … danh sách cho phép chỉ phải liệt kê một tập nhỏ và biết trước."* Ở đây danh sách CHO PHÉP (`GOI_WRAPPER`) đúng là nhỏ và biết trước — nhưng bước NHẬN DIỆN đứng trước nó lại đóng vai một danh sách CẤM ngầm (chỉ có `bash|sh|exec` mới "được xem là lời gọi"), và danh sách cấm kiểu token-dẫn-đầu ấy thua đúng theo doctrine đã trả giá: nó phân biệt CÁCH VIẾT, không phân biệt hành vi thực thi.

**Gợi ý vá (không đòi mở regex phân tích shell, đúng tinh thần "đường RẺ" đã dùng cho finding #3 lượt 1):**

1. **Rẻ nhất — sửa lời khai cho khớp phép đo**, bỏ câu "Ngoài hai dạng canonical vẫn là một LỜI GỌI" (sai), thay bằng liệt kê đúng phạm vi nhận diện (neo `^`, token dẫn đầu duy nhất, không xuyên qua khoảng trắng), và liệt kê các dạng đã đo là lọt — đúng mẫu đã dùng cho `t34`. Không đổi hành vi, đóng đúng phần "khai sai" của finding này; phần "vẫn lọt" thành một nợ có tên (giống nợ `required-status-check`, có thể đi kèm `#209`).
2. **Rẻ và có răng hơn:** đổi `GOI_WRAPPER_THUC_THI.search` từ neo `^…\s+` sang tìm chuỗi con `chay_lease_publish_test.sh` xuất hiện ở BẤT KỲ đâu trong `x.strip()` (đã qua `_dong_lenh`, tức đã lọc chú thích toàn dòng và nối dòng gãy) — đúng cách đặc tả revision 3 mô tả ("có nhắc … trong một lệnh thực thi"). Vì `_dong_lenh` chỉ trả về LỆNH thực thi (không phải văn bản thô), rủi ro báo oan kiểu `sha256sum` của `t25` không lặp lại ở đây trong phạm vi `ci.yml`/`ops-publish-lease.yml` hiện tại (tôi không tìm thấy dòng nào trong hai tệp workflow "nhắc tên wrapper mà không thực thi nó" ngoài `sha256sum`, và `sha256sum` không nằm trong `run:` bị `t35` quét theo `dong_lenh` của MỘT bước là selftest — cần rà lại nếu áp dụng).

---

## Đã đo và sạch — để im lặng không bị đọc thành chưa thử

**Bốn đột biến executor khai đã giết — cả bốn xác nhận CẢ HAI CHIỀU trên bản sao tạm (`archive` thuần đọc, không đụng `kho`):**

```text
1. Bỏ $NEO khỏi lời gọi wrapper (ops-publish-lease.yml):
   head  rc=1  39/40  ĐỎ t25 (regex mới bắt được `bash ops/chay_lease_publish_test.sh` thiếu $NEO)
   prev  rc=0  40/40  IM     (regex cũ của prev không nhận `bash`, không bắt được)

2. Gỡ hẳn lời gọi wrapper (thay `run:` bằng `echo`):
   head  rc=1  39/40  ĐỎ t25 (chốt riêng `thay_wrapper >= 1` bắt được)
   prev  rc=0  40/40  IM     (prev không có chốt "phải thấy lời gọi wrapper")

3. `bash ./ops/chay_lease_publish_test.sh` (thêm `./`) + thiếu `AL_VER` — đúng ca `N2` lượt 1:
   head  rc=1  39/40  ĐỎ t35 ("ngoài danh sách canonical" — GOI_WRAPPER_THUC_THI CÓ nhận diện
                              dạng này vì không có khoảng trắng chen vào `\S*`)
   prev  rc=0  40/40  IM     (allowlist cũ `continue` êm với cách viết khác 2 ký tự)

4. Gỡ chốt mã `mkdir` (bỏ `|| loi 12 …`, về lại `mkdir -p "$AL_DICH"` trần):
   head  rc=1  39/40  ĐỎ t35, thông điệp đúng: "rc=1, output='mkdir: cannot create
                       directory […]: File exists'" — tức bắt đúng cái nó sinh ra để bắt
   prev  (không áp dụng hai chiều: prev vốn đã trần `mkdir`, sub-test rc=12 KHÔNG TỒN TẠI
          trong t35 của prev — baseline 40/40 chính là "IM vì chưa có ca", không phải
          "IM vì chốt yếu")
```

Xác nhận cả bốn — không tin theo lời khai của executor, đo lại độc lập từng cái.

**Chốt mới có báo oan không (mục 3.2 nhiệm vụ):**

```text
full_line_comment           rc=0  40/40  (dòng comment nguyên dòng nhắc tên wrapper — an toàn)
echo_mention                rc=0  40/40  (echo "info: ... chay_lease_publish_test.sh ...")
step_name_mention           rc=0  40/40  (name: kiểm tra chay_lease_publish_test.sh tồn tại)
inline_trailing_sh_comment  rc=1  ĐỎ t25 (`run: echo ok # sh chay_lease_publish_test.sh`)
inline_trailing_bash_comment rc=1 ĐỎ t25 (`run: echo ok # xem bash ops/chay_lease_publish_test.sh`)
```

Ba trong năm là AN TOÀN. Hai dòng cuối là báo oan THẬT của `t25`: một CHÚ THÍCH ĐI SAU một lệnh thật trên cùng dòng `run:` (không phải dòng bắt đầu bằng `#`, nên không bị `dong.lstrip().startswith("#")` lọc) bị đếm là một lời gọi thiếu `$NEO`, vì `goi.findall` quét toàn bộ nội dung dòng chứ không cắt phần sau `#`. Đây là P3 — fail-CLOSED (một ĐỎ giả, không phải một XANH giả), nên không nguy hiểm bằng finding 1, nhưng vẫn là chốt gãy hình dạng nếu ai viết `# xem bash ops/chay_lease_publish_test.sh` làm ghi chú giải thích ngay trên/cạnh bước liên quan — một kiểu comment hoàn toàn tự nhiên. Không nằm trong bốn việc bắt buộc của lượt này (không phải hồi quy do delta này gây ra — hành vi này đã có từ trước, vì đoạn code liên quan không đổi khác gì ngoài việc thêm token `bash|sh|exec`, và bản thân `python3?` gốc cũng đã có cùng lỗ với comment kiểu `# xem python3 ops/lease_publish.py`), nên ghi làm finding phụ, không chặn.

**Trục 3 — ngưỡng `thay >= 4` không tự trở thành cổng xanh rỗng:**

```text
Gỡ wrapper + bù thêm 1 lời gọi lease_publish.py (giữ thay=4 bằng tay):
  rc=1  39/40  ĐỎ t25 — "không thấy lời gọi thực thi `chay_lease_publish_test.sh`"
```

Chốt `thay_wrapper >= 1` bắt được ngay cả khi kẻ tấn công cố giữ tổng `thay` không đổi — đúng vai trò "chốt riêng" mà chú thích trong code tuyên bố.

**Hồi quy:**

- Số ca: `40` (đếm `@ca` = đếm `def t[0-9]` = 40) — không tụt so với nền lượt trước.
- `actionlint` rc=0 cả 5 workflow, đo trên CẢ hai cây (`head` và `prev`) bằng `actionlint 1.7.7` thật (không phải PyYAML).
- `diff.patch` (`a09aae62..2284b465`) và `diff_delta.patch` (`e071e0aae6..2284b465`) khớp byte-for-byte với `git diff` đo trực tiếp trên `kho` (sha256 khớp cả hai).
- Write set delta lượt này đúng **2 tệp**: `ops/cai_actionlint.sh` (+2−1) và `ops/lease_publish_test.py` (+65−20) — không có tệp thứ ba.
- `base` (`a09aae62`) và `head lượt trước` (`e071e0aae6`) đều là tổ tiên của `head` hiện tại (`git merge-base --is-ancestor`, rc=0 cả hai).
- `t34` — chạy lại đúng năm dạng lượt 1 đã đo (`A,B,D,E,F` = lọt; `C,G,H` = ĐỎ) trên `ci.yml` của `head`: kết quả **giống hệt** lượt 1, và `_CHAY_BO_TEST` không đổi một ký tự (xác nhận qua diff: chỉ chú thích quanh nó đổi, biểu thức regex y nguyên).
- `GOI_WRAPPER_THUC_THI` không báo oan với hai dòng `sha256sum` (kiểm bằng cả chạy suite thật lẫn khớp regex trực tiếp ngoài suite).
- `rc=12` không đụng mã nào khác trong `cai_actionlint.sh`/`chay_lease_publish_test.sh` (liệt kê đủ: 2,3,4,5,6,7,8,9,10,11,12 — không trùng); chỉ một lời gọi `mkdir` trong toàn script, có đúng một chốt.
- `git -C kho status --short` RỖNG cả trước lẫn sau toàn bộ phiên review; `HEAD` không đổi (`2284b465…`) — không lặp lại lỗi lượt 1 (checkout vào index của worktree). Mọi đột biến chạy trên `git archive` xuất ra thư mục tạm ngoài `kho`.

## Chưa đo được — ghi là GIẢ THUYẾT, không ghi là sạch

- **CI `workflow_dispatch` 32402136904 (cả hai job `success`)**: có thể kết nối `github.com:443` từ sandbox này, nhưng KHÔNG có `gh`/token trong bộ vật liệu được cấp cho lượt review này để tự truy vấn Actions API. Đúng như nhiệm vụ đã lường trước, tôi khai đây là **lời khai của người khác**, không tự xác minh.
- **Nhánh Windows thật của wrapper/`t40`**: sandbox không có Windows; đọc mã cho thấy nhánh Windows dùng đúng logic chung (không có rẽ nhánh nào bị delta này chạm tới — diff chỉ sửa `ops/lease_publish_test.py` và `ops/cai_actionlint.sh` ở các đoạn không liên quan tới phần chọn hệ điều hành).
- **`V2a`/`V2b` (installer ở job khác / installer sau selftest) — suy luận lại từ mã, KHÔNG dựng lại đúng hai kịch bản gốc.** `t34` quét mọi `job → step` không phân biệt vị trí hay job, và tôi đã xác nhận trực tiếp rằng một lời gọi thẳng `.py` (`G`, `H`) vẫn bị bắt trên `head`; theo cấu trúc mã (`for ten_job, job in (d.get("jobs") or {}).items()`, không có logic phụ thuộc thứ tự job), hai kịch bản cũ vẫn phải đỏ. Nhưng tôi không tự dựng lại chính xác hai tệp YAML nhiều-job của lượt 1 để đo trực tiếp — đây là suy luận có căn cứ từ mã, không phải phép đo độc lập mới.
- **Branch protection / required status check** ngoài kho: không kiểm được từ đây, đúng như đã khai ở lượt 1.

## Chốt cây

```text
git -C kho status --short   # rỗng, cả trước và sau
HEAD = 2284b4657304d0229e95d1f64ebd0c22035d201d   (khớp mỏ neo trong nhiệm vụ)
Không lặp lại sự cố "ghi vào index worktree" của lượt 1 — mọi bản sao mutation dùng
`git -C kho archive <sha> | tar -x` ra thư mục ngoài `kho`, không chạm working tree.
```

## Kết luận

Bốn việc trong phạm vi lượt này (P1 `t25`, P3 `GOI_WRAPPER`→ĐỎ, P3 `mkdir` rc=12, P2 `t34`
lời khai) đều có bằng chứng đo hai chiều, không hồi quy. Nhưng chính cơ chế mới dựng cho
finding #4 (`GOI_WRAPPER_THUC_THI`) còn một khoảng hở đo được — bốn/năm dạng cú pháp hợp lý
(`env X=1 bash …`, `bash -c '…'`, `command bash …`, `${{ github.workspace }}` có khoảng
trắng) vẫn được MIỄN nghĩa vụ `AL_VER` do bước NHẬN DIỆN không bắt được chúng — và chú thích
ngay cạnh đó khẳng định sai rằng đã bắt được ("Ngoài hai dạng canonical vẫn là một LỜI GỌI").
Hậu quả bị giới hạn bởi lớp phòng thủ độc lập trong `cai_actionlint.sh` (vẫn `loi 2` khi
thiếu `AL_VER`, bất kể cú pháp gọi), nên đây không phải một lỗ an ninh im lặng — nhưng nó là
một khẳng định sai trong chính write set của packet này về độ phủ của một chốt vừa được dựng
để đóng một finding P3 trước đó. Theo đúng tiêu chí §5 nhiệm vụ ("mọi thứ còn hở đều đã được
khai tên"), khoảng hở này CHƯA được khai — nó bị khai NGƯỢC — nên chưa đạt bar approve.

Vì `attempts_limit` đã cạn (3/3) ở phía executor, khuyến nghị cụ thể cho người giữ kho: đường
RẺ nhất là chỉ sửa lại đúng ba dòng chú thích (1412-1414) cho khớp phạm vi đo được — không cần
mở lại regex — rồi ghi khoảng hở còn lại thành một mục nợ có tên (cùng nhà với quyết định
"đảo `t34` thành danh sách cho phép" đã chuyển sang `#209`, vì hai thứ cùng một họ: allowlist
gác nghĩa vụ mà bước nhận diện phía trước không phủ hết cú pháp). Đây là một sửa nhỏ, không
đòi thêm attempt vá lớn, nhưng vẫn cần ai đó chạm write set nên tôi không tự làm ở đây (read-only).

VERDICT: changes_requested
Reviewed commit: 2284b4657304d0229e95d1f64ebd0c22035d201d
