verdict: approve
reviewed_sha: 2f708690

# CROSS-REVIEW LƯỢT 3 — packet #541 `WP541-PATH-TOI-THIEU-THEO-NEN` **r1 / gen 1**

| | |
|---|---|
| `reviewed_sha` | `2f708690` (nhánh `fix_issue_541`) — head **không trôi** trong lúc review (đo hai lần: `2f70869` ở cả hai) |
| `base_sha` | `d705623162b7` — `merge-base` = `d705623162b7`, đúng base của lease |
| lease | `wp541-path-r1-g1-antigravity`, `spec_hash fc6e814d…1162075` |
| lượt trước | `e60c757aa535` → `changes_requested` (1 lớp P1 · 1 lớp P2) |
| kết luận | **`approve`** — **0 P1 · 0 P2** · **2 P3** |
| assurance | **`advisory_review`** — trần cứng, xem cuối tệp |

## HAI LỚP CỦA LƯỢT 2 — ĐÓNG CẢ HAI, ĐO ĐỘC LẬP

### `P1-2` — bước 3 nhận `.bat`/`.cmd`/`.py` qua `PATHEXT`

**ĐÓNG, và đóng chắc hơn mức lượt 2 đòi.** Bước 3 không còn gọi `shutil.which`:

```python
cand = Path(d) / "git.exe"      # tường minh, không qua PATHEXT
if hop_le(cand):
    return str(cand.resolve())
```

`grep 'shutil.which'` trong thân `_git_windows` ⇒ **1 dòng, là CHÚ THÍCH** (`:77`), không phải mã.

**Phản chứng ĐỘC LẬP đã chạy** (không nhận lời khai của executor, không nhận lời của lượt 2):
thư mục PATH **ngoài cwd** chứa `git.bat`, `git.cmd`, `git.py`, `git` (không phần mở rộng) và một
tệp nhiễu ⇒ **`None`**. Rồi **đối chứng dương**: thêm `git.exe` thật vào **đúng thư mục ấy** ⇒ trả
`…/shim/git.exe`. Ca có thể xanh, nên cái `None` ở trên là phép đo chứ không phải rig chết.

**Điều này mạnh hơn khuyến nghị của lượt 2 ở một chỗ đáng ghi:** lỗ `PATHEXT` chết theo **CẤU TRÚC**,
không theo phiên bản. Lượt 2 đo được `shutil.which` đổi hành vi giữa py3.11 và py3.12/3.13 và CI ghim
3.12 — nay chuyện ấy **không còn liên quan**, vì mã không gọi `shutil.which` nữa. Tôi chạy trên
**3.11.15**, tức bản KHÔNG có lỗ, nên phép đo của tôi một mình **không** phân biệt được "đã vá" với
"nền may mắn" — nhưng phép đọc mã thì phân biệt được, và hai đường cùng chỉ một chỗ.

### `P2-MỚI` — thiếu ca đo `git.bat` ở PATH ngoài cwd

**ĐÓNG.** `t166` nay có **ba cửa**, không phải một:

| cửa | đo gì |
|---|---|
| 1 | `path` = `cwd` chứa `git.bat`/`git.py`/`git.exe` ⇒ kết quả KHÔNG trỏ vào cwd |
| 2 | thư mục PATH **ngoài** cwd chỉ có `git.bat`/`cmd`/`py` ⇒ **từ chối**, và `Chan(12)` |
| 3 | `path` = `path_bat` + `path_exe` ⇒ bỏ qua thư mục shim, nhận `git.exe` |

Cửa 2 là đúng ca mà bàn giao lượt 1 đòi và lượt 2 đo được là **thiếu**.

## ĐỘT BIẾN — NĂM CÁI, VÀ KIỂM CẢ **LÝ DO CHẾT**

Chạy trên **clone tạm rời** (`PYTHONDONTWRITEBYTECODE=1`, khôi phục nguyên bản sau mỗi lượt, đã xác
minh `khoi phuc: OK`) — không đụng cây thật, theo bài học *"đột biến ghi vào tệp THẬT là bom hẹn giờ"*.

| đột biến | ca đích | màu | lý do chết |
|---|---|---|---|
| quay bước giải Windows về hằng số | `t165` | **ĐỎ** | `Chan: KHÔNG_XÁC_ĐỊNH: không thấy git trong PATH tối thiểu ` |
| gỡ phép loại-trừ cwd | `t166` | **ĐỎ** | `N2 cửa 1: kết quả phải là None (loại trừ cwd), nhưng lại nhận: …/fake_cwd/git.exe` |
| gỡ phép loại `%SystemRoot%` | `t167` | **ĐỎ** | `N3a: ứng viên dưới SystemRoot phải bị loại, nhưng nhận: …/Windows/System32/git.exe` |
| bỏ chẩn đoán, rơi thẳng xuống bước 3 | `t167` | **ĐỎ** | `N3b: chẩn đoán phải ghi KHÔNG_ĐO_ĐƯỢC khi ProgramFiles không phân giải, nhận: []` |
| đổi hằng số POSIX | `t168` | **ĐỎ** | `Chan: KHÔNG_XÁC_ĐỊNH: không thấy git trong PATH tối thiểu /khong-ton-tai` |

**Không cái nào là tín dụng giả.** Quét `TypeError|AttributeError|NameError|KeyError|ImportError|
Traceback` trên lý do chết ⇒ **0 khớp**. Ba ca chết bằng assertion nêu đích danh hợp đồng của chính
chúng; hai ca còn lại chết bằng `Chan` từ chính hàm đang thử, với thông điệp nội suy đúng giá trị bị
đột biến — không phải lỗi vô can. Đây là điều `#355`/`#359` dạy phải kiểm, và nó kiểm được.

*Điểm yếu nhỏ, ghi cho đủ:* thông điệp của `t165` và `t168` là `Chan` chung, **không nêu tên ca**.
Chúng phân biệt được nhờ giá trị `path_posix` nội suy, nhưng một người đọc log vội có thể nhầm hai ca
ấy với nhau.

## BẢNG ĐO ĐẦY ĐỦ — KỂ CẢ CÁI KHỚP

| phép đo | kết quả |
|---|---|
| head trôi trong lúc review | **không** (`2f70869` hai lần) |
| `write_set` | **đúng 2** đường, không tệp nào ngoài ✔ |
| `N6` numstat so base thật | **2 tệp, +270 / −4** — dưới trần `sensitive` 3 tệp / 300 dòng ✔ |
| `N5` delta ca đỏ so `d705623` | **0** ✔ — nền và head cùng **3 ca đỏ**, cả ba là `KHÔNG ĐO ĐƯỢC: thiếu actionlint` |
| bộ test đầy đủ ở đây | `158/161 đạt; đã chạy=161, bỏ qua=0` |
| bốn ca đích | `t165` `t166` `t167` `t168` — **QUA cả bốn** ✔ |
| đột biến có răng | **5/5**, và **5/5 giết ĐÚNG LÝ DO** ✔ |
| dấu bỏ-qua-CI nguyên văn trong 3 commit | **0** (`grep -F`; đối chứng dương `fix(#541)` ⇒ 3) ✔ |
| `shutil.which` còn trong `_git_windows` | **0 dòng mã** (1 dòng chú thích) ✔ |

> `158/161` ở đây **khác** `161/161` của lượt 2 vì container này **thiếu `actionlint`**, không phải
> vì bản vá. Ba ca đỏ y hệt trên `origin/master`. Delta là thứ có nghĩa, không phải con số tuyệt đối.

## `P3-1` — dòng `KHÔNG_ĐO_ĐƯỢC` ghi ra `stderr` VÔ ĐIỀU KIỆN và không tắt được

```python
thong_bao_pf = "KHÔNG_ĐO_ĐƯỢC: không thấy git hợp lệ dưới %ProgramFiles%, rơi xuống PATH"
if chan_doan is not None:
    chan_doan.append(thong_bao_pf)
sys.stderr.write(thong_bao_pf + "\n")      # <- không có điều kiện nào
```

Hợp đồng `N3b` được thoả **bằng `chan_doan`**; lần ghi `stderr` là thứ **thêm**, chạy **mọi lần** bước
2 trượt, và **không caller nào tắt được** — kể cả khi đã truyền `chan_doan` để nhận chẩn đoán theo
đường sạch. `_git_exe_toi_thieu` được gọi **3 nơi** (`:1156` `:1218` `:1298`), nên một lượt chạy trên
Windows không có Git dưới `%ProgramFiles%` sẽ bơm ba dòng vào `stderr`.

Đo được: `stderr` là kênh mà **58 dòng** trong `lease_publish_test.py` khẳng định lên (`"Traceback"
not in e`, `"không phải thư mục" in e`, …). Không assertion nào **gãy** vì thêm một dòng — tôi đã
kiểm, chúng đều là phép kiểm chứa/không-chứa. Nên **đây là P3, không phải P2**.

Nhưng đúng kênh ấy là chỗ `t150` đang hỏng vì một tiền tố `stderr` chưa ai giải thích được (packet
#552). Thêm một nguồn ghi vô điều kiện vào đó, trên đúng nền khó chẩn đoán nhất, là làm bẩn tín hiệu.
**Cách chữa rẻ:** chỉ ghi `stderr` khi `chan_doan is None`, hoặc thêm cờ `im_lang=False`.

**Không đo được từ đây:** nhánh này chỉ chạy khi `nen == "windows"`, nên trên `ubuntu-latest` nó
không bao giờ chạy trong bộ test thật. Tôi thấy nó vì gọi `_git_windows` trực tiếp.

## `P3-2` — phép tách PATH đúng nhờ TRÙNG HỢP, và nó là bẫy cho ca test sau

```python
ds_thu_muc = [d for d in path_val.split(";" if ";" in path_val else os.pathsep) if d]
```

Đo thẳng trên Linux (`os.pathsep == ':'`):

```
'C:\Program Files\Git\cmd'          -> ['C', '\Program Files\Git\cmd']     <-- RÁC
'C:\Git\cmd;C:\Windows\System32'    -> ['C:\Git\cmd', 'C:\Windows\System32']  OK
'D:\tools\git\cmd'                  -> ['D', '\tools\git\cmd']             <-- RÁC
```

**Hôm nay nó KHÔNG hỏng**, và tôi nói rõ vì sao để không thổi phồng: trên Windows thật `os.pathsep`
cũng là `;` nên nhánh `else` cho cùng kết quả; còn `t166`/`t167` tiêm đường dẫn tạm **kiểu POSIX**
(không có dấu hai chấm) nên cũng không chạm.

Nó hỏng ở **ca test tương lai**: ai viết `_git_windows(path=r"C:\Git\cmd", …)` trên Linux sẽ nhận
`['C', '\Git\cmd']`, hàm trả `None`, và ca **XANH** trong khi chẳng đo gì — đúng hình dạng *"ca có
MẶT khác ca có ĐO"* mà `t24` đã trả giá. **Cách chữa:** tách bằng `";"` luôn khi ở nhánh Windows
(nền đã biết tại điểm gọi), đừng đoán từ nội dung chuỗi.

## `KHÔNG ĐO ĐƯỢC` — khai, không lấp

1. **Hành vi trên Windows thật.** Mọi phép đo của lượt này chạy trên Linux bằng tham số tiêm. Chúng
   chứng minh **logic giải đường dẫn**, không chứng minh hành vi của `CreateProcessW`, `%PATHEXT%`
   thật, hay `subprocess` với đường dẫn có dấu.
2. **`N7`** (*"Trước = 1, Sau = 0"*) — lượt 1 và 2 đều hỏi hai con số ấy **đếm gì** (luật `L1`); vẫn
   chưa thấy trả lời. Vẫn `KHÔNG ĐO ĐƯỢC`, và lượt này **không** làm tròn nó thành đã có.
3. **`gate (windows-latest)`** — không chạy và sẽ không chạy (`manual_ci_budget: 0`; và từ #548
   `ci.yml` bỏ điều kiện `github.ref == 'refs/heads/master'`). Packet sửa đường Windows mà không được
   chạy Windows để nghiệm thu; đặc tả đã khai và chọn sống chung.
4. **Phiên bản Python của CI so với của tôi.** Tôi chạy 3.11.15; CI ghim 3.12. Với bản vá hiện tại
   khác biệt ấy **không còn liên quan** (không gọi `shutil.which`), nhưng tôi không chạy được 3.12 ở
   đây để đo trực tiếp.

## KHAI XUNG ĐỘT LỢI ÍCH — ĐỌC TRƯỚC KHI DÙNG VERDICT NÀY

Phiên này **soạn đặc tả `r2`** của #541 (`fc6e814d…`) **và soạn chỉ thị thi công** giao cho agy
(`8aa71c43…`). Nghĩa là tôi đang chấm một bản vá làm theo **hai văn bản do chính tôi viết**.

Đó **không** phải self-review theo nghĩa hẹp — tôi không viết dòng mã nào, và không cấp hint patch
nào cho packet này. Nhưng nó có nghĩa: **nếu đặc tả sai ở đâu, lượt này ít có khả năng thấy nhất.**
Cụ thể, tôi không phải người tốt để hỏi *"thứ tự ứng viên ba bước có đúng không"* hay *"có nên bỏ
hẳn bước 3 không"* — đó là lựa chọn của chính tôi ở vòng `soan-spec`.

Hai `P3` ở trên đều nằm **trong** khuôn đặc tả, không thách thức nó. Một reviewer độc lập nên được
hỏi riêng: *đặc tả `r2` có bỏ sót đường vào nào không.*

Kèm theo, như hai lượt trước: phiên này cũng **ghi hộ lease** `wp541-path-r1-g1-antigravity`.

## ASSURANCE — trần cứng

**`advisory_review`**. Lease khai `assurance_target: human_audited`, `reviewer_provider: human`;
phiên này là một phiên `claude`. Verdict `approve` ở đây **KHÔNG** thoả điều kiện land của lease.
Cần một lượt audit của người, độc lập với executor, tự đọc spec và diff, neo vào `2f708690`.

## NGUỒN CÓ THẨM QUYỀN

Tệp này trong kho, có băm. Bản đăng trên GitHub chỉ là **bản chiếu**.
Verdict lượt 1 và lượt 2 giữ nguyên trên đĩa; lượt này **không rút** điều gì của chúng — hai lớp mở
của lượt 2 nay đóng bằng phép đo, không bằng lời khai.
