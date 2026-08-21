# Prompt BẤT BIẾN — EXECUTOR `PLAT-X5` (#206), lượt 1 **revision 3**, provider `codex`

> **LƯỢT TRƯỚC BẠN ĐÃ LÀM XONG VÀ CI ĐÃ XANH.** Cross-review (`claude`, khác nền) trả
> `changes_requested` với **năm finding**. Đây là **attempt 3/3 — attempt CUỐI**.
> Người giữ kho đã nới trần đúng MỘT lần và đã **thu hẹp phạm vi**: hai trong năm finding
> **đã bị tách sang packet khác** (#209). Đừng đụng vào chúng.
>
> Điều kiện dừng vẫn nguyên hiệu lực. Lượt r1 bạn dừng vì đặc tả hỏng và bạn **dừng đúng** —
> đừng vì lần này là attempt cuối mà ngại dùng lại nó.

Bạn là NGƯỜI THI CÔNG. Reviewer sẽ là `claude` (khác nền — §8 thoả).

## 0. Bố cục

```
./nhiem_vu.txt              prompt này
./PACKET_ISSUE_206.md       thân Packet Issue — ĐẶC TẢ CÓ THẨM QUYỀN, đã có §REVISION 3
./VERDICT_X5_LUOT_1.md      verdict cross-review lượt 1 — NĂM finding, nguyên văn
./bin/actionlint            actionlint 1.7.7 (NGOÀI cây kho). export PATH="$PWD/../bin:$PATH"
./kho/                      cây làm việc — nhánh `codex/plat-x5-exec-1`, GHI ĐƯỢC
```

Làm việc trong `./kho`. **Commit vào nhánh ấy. ĐỪNG `git push`.** Đừng đụng ra ngoài sandbox.

**Đọc `PACKET_ISSUE_206.md` §REVISION 3 TRƯỚC** — nó là thứ định nghĩa lượt này. Verdict là
**bằng chứng**, không phải danh sách việc: bốn việc phải làm nằm ở §REVISION 3.

## 1. Mỏ neo

| trường | giá trị |
|---|---|
| packet | `#206` — `[WP PLAT-X5]`, revision 3 |
| nhánh | `codex/plat-x5-exec-1` |
| head xuất phát | `e071e0aae6bdc4d270a42fbc534ad3f05dcba0fa` (bản đã được review) |
| base | `a09aae627533f59e6b2e817858a6db50b999d41c` |
| write set | `ops/lease_publish_test.py` · `ops/cai_actionlint.sh` · `ops/chay_lease_publish_test.sh` · `.github/workflows/ci.yml` · `.github/workflows/ops-publish-lease.yml` |

**`ops/NO_KY_THUAT.md` KHÔNG nằm trong write set** và lượt này **không** thêm nó vào.

## 2. BỐN việc — không hơn

### 2.1 P1 — `t25` không còn thấy lời gọi bộ kiểm

Diff lượt trước đổi lời gọi trong `ops-publish-lease.yml` từ `python3 "$NEO/…_test.py"` sang
`bash "$NEO/ops/chay_lease_publish_test.sh"`. Regex của `t25` chỉ nhận
`python3?\s+(\S*lease_publish(?:_test)?\.py)` nên lời gọi mới **VÔ HÌNH** với nó.

**Đo được, hai chiều** (reviewer chạy, bạn nên tái hiện):
- trên cây base (`git archive a09aae62`): đột biến bỏ `$NEO` ⇒ `37/38`, **ĐỎ `t25`**;
- trên head `e071e0aa`: cùng đột biến trên lời gọi wrapper ⇒ `40/40` **ĐẠT**, cổng im.

Mã hôm nay vẫn đúng. Thứ bị gỡ là **cái máy giữ cho nó đúng ngày mai**.

Mở `t25` sang cả lời gọi thực thi wrapper. **Giữ tính chất "đo ĐỐI SỐ có `$NEO` hay không" —
đừng viết bộ phân tích shell.** Nâng chốt chống-xanh-rỗng cho khớp số lời gọi thật, và **sửa
chú thích của nó**: câu *"chờ ít nhất 3 (test, check, body)"* nay **SAI**, `test` không còn nằm
trong ba cái đó, nên ngưỡng ấy đang được thoả bởi ba lời gọi khác.

**Cạm bẫy đã đo:** dòng `sha256sum ops/… ops/…` ở bước neo **CỐ Ý** không có `$NEO` (nó in băm
bản head để đối chiếu). Bó theo *"có nhắc tên tệp"* sẽ báo oan dòng ấy. Bó theo **token lệnh
dẫn đầu** (`python|python3|py|bash|sh|exec`).

### 2.2 P3 — `GOI_WRAPPER` gác một NGHĨA VỤ nên ra ngoài danh sách là ĐƯỢC MIỄN

`t35` đòi bước gọi wrapper khai `AL_VER`, nhưng chỉ với bước có phần lệnh **bằng đúng** một
trong hai chuỗi `GOI_WRAPPER`; không khớp thì `continue`.

**Đo được:** bỏ `AL_VER` ⇒ `39/40` **ĐỎ**. Bỏ `AL_VER` **và** đổi `bash ops/…` thành
`bash ./ops/…` ⇒ `40/40` **IM**. Cùng một thiếu sót, khác đúng hai ký tự.

Danh sách CHO PHÉP chỉ đúng khi thứ ngoài danh sách bị **TỪ CHỐI**. Ở đây nó gác một *nghĩa vụ*
nên ra ngoài danh sách = **được miễn** — **fail-OPEN**, ngược chiều ý định. Đảo nhánh `continue`
thành nhánh báo lỗi: nhận diện bước gọi wrapper theo *có nhắc `chay_lease_publish_test.sh` trong
một lệnh thực thi*, rồi **ĐỎ** nếu phần lệnh không nằm trong `GOI_WRAPPER`.

### 2.3 P3 — `mkdir` hỏng trả `rc=1`, trùng mã thoát của chính bộ test

`ops/cai_actionlint.sh` khai ở đầu tệp rằng các mã thoát là *"RIENG BIET de nguoi goi (va `t35`)
khang dinh duoc LY DO tu choi"*, rồi `mkdir -p "$AL_DICH"` **không** có `|| loi N` nên rơi vào
`set -e` và thoát **`rc=1`** — đúng mã của `lease_publish_test.py` khi có ca đỏ. Người gọi (kể cả
`ops-publish-lease.yml`) không phân biệt được *"cổng đỏ"* với *"không tạo nổi thư mục cài"*.

**Đo được:** `AL_DICH` trỏ một tệp thường ⇒ `rc=1`, marker `KHONG`.

Cho nó một mã thoát **RIÊNG**, khác `1`, có thông điệp phân biệt được. Kèm ca khoá.

### 2.4 P2 — `t34` khai HẸP hơn thứ đo được: **CHỈ SỬA LỜI KHAI**

Docstring `t34` khai đúng **một** lỗ (`python -m`) và tuyên hợp đồng còn lại là *"workflow gọi
THẲNG `lease_publish_test.py` thay vì đi qua wrapper"*. **Đo được — 8 biến thể, `rc` đọc trực tiếp:**

```
A python -m ops.lease_publish_test         rc=0  KHONG-DO
B python3 -u ops/lease_publish_test.py     rc=0  KHONG-DO
C bash -c ...                              rc=1  DO(t34)
D ./ops/lease_publish_test.py              rc=0  KHONG-DO
E uv run ops/lease_publish_test.py         rc=0  KHONG-DO
F python -X utf8 ops/lease_publish_test.py rc=0  KHONG-DO
G python ops/lease_publish_test.py         rc=1  DO(t34)
H exec python ...                          rc=1  DO(t34)
```

`B D E F` **đều là "lời gọi THẲNG tệp `.py`"** — đúng thứ `t34` tự nhận là canh. Nguyên nhân:
`\S*` trong `_CHAY_BO_TEST` không vượt được khoảng trắng nên **bất kỳ cờ nào chen giữa** cũng làm
phép khớp trượt.

**Lượt này CHỈ sửa LỜI KHAI cho khớp phép đo:** nói rõ `t34` chỉ nhận dạng canonical
`python|python3|py <đường-dẫn>.py` **không cờ**, và liệt kê đủ **năm** dạng đã ĐO là lọt.
**KHÔNG nối regex. KHÔNG đảo thành danh sách cho phép** — việc ấy đã sang `#209`, và làm nó ở đây
là lách phạm vi.

`CLAUDE.md`: *"PHẠM VI TUYÊN BỐ phải bằng phạm vi ĐO ĐƯỢC."* Lượt này chọn hạ **tuyên bố** xuống
bằng **phép đo**, không nâng phép đo lên — và **khai thẳng lý do** trong docstring.

## 3. NGOÀI phạm vi — đã sang `#209`, ĐỪNG đụng

- **Finding 2**: nợ `PLAT-X5-required-status-check` vào `ops/NO_KY_THUAT.md`. Tệp ấy **ngoài
  write set**. Bạn có thể **giữ nguyên** ba chú thích đang có; đừng thêm, đừng bớt.
- **Đảo `t34` thành DANH SÁCH CHO PHÉP** — quyết kiến trúc, thuộc `#209`.

Thấy một đường vá đòi chạm hai thứ trên ⇒ **DỪNG**, xuất handoff, đừng lách.

## 4. Tiêu chí hoàn tất

- `python3 ops/lease_publish_test.py` ⇒ `rc=0`, `N/N` **hai số BẰNG NHAU**, **không tụt dưới 40** ca.
- `actionlint .github/workflows/*.yml` ⇒ `rc=0` **cả 5**.
- **Bốn phản chứng MỚI, mỗi cái giết 1/1**, chạy trên **BẢN SAO TẠM**:
  1. bỏ `$NEO` khỏi lời gọi **wrapper** trong `ops-publish-lease.yml` ⇒ `t25` **ĐỎ**
     (bản hiện tại **IM** ở ca này — đó là lý do ca này tồn tại);
  2. **gỡ hẳn** lời gọi bộ kiểm khỏi workflow ⇒ **ĐỎ** (đừng để chốt chống-xanh-rỗng nuốt mất);
  3. `bash ./ops/chay_lease_publish_test.sh` **thiếu** `AL_VER` ⇒ `t35` **ĐỎ**
     (bản hiện tại IM, khác đúng hai ký tự);
  4. `AL_DICH` trỏ một tệp thường ⇒ mã thoát **≠ 1** và ≠ mã bộ test, thông điệp phân biệt được.
- Hai phản chứng vòng 2 vẫn **ĐỎ** (installer ở **job khác**; installer **sau** selftest).
- Docstring `t34` liệt kê đủ **năm** dạng lọt đã đo.

## 5. Nếp của kho này — KHÔNG phải tuỳ chọn

1. **`rc` đọc TRỰC TIẾP từ tiến trình.** `| tail`/`| head` là **nuốt mã thoát**. Và `$( )` **đặt
   lại `$?`** — `printf '… rc=%s' "$(…)" "$?"` in mã của `printf`, đã làm cả một bảng đo báo sai.
   Gán `RC=$?` **ngay dòng sau** lệnh, không đặt lời gọi nào ở giữa.
2. **Đột biến chạy trên BẢN SAO TẠM**, không bao giờ chạm cây thật — `finally` không chạy khi bị
   cắt giữa chừng, và một bản vá NGƯỢC đã từng đi thẳng vào commit theo đường đó.
3. **Đồ giả mô phỏng TRẠNG THÁI, không diễn kịch bản.**
4. **Ca có MẶT khác ca có ĐO.** Harness **không có cơ chế bỏ qua**: `main()` chỉ `qua += 1` khi
   hàm không ném, nên một ca `return` sớm vẫn được đếm là ĐẠT.
5. **Đột biến SỐNG SÓT không luôn nghĩa là test yếu** — có thể đột biến hỏng (ví dụ `; exit 0`
   sau một lệnh thất bại dưới `set -e` không bao giờ chạy tới). Khai ra khi gặp, đừng im.
6. **Chú thích tiếng Việt không dấu trong `.sh`, có dấu trong `.py`.** Ghi **LÝ DO** + **bằng
   chứng đo được**, không chỉ ghi "cái gì".
7. **ĐỪNG viết chuỗi bỏ-qua-CI** (`skip` + `ci` trong ngoặc vuông) vào thông điệp commit, **kể cả
   khi trích dẫn** — GitHub khớp chuỗi trên toàn thông điệp và sẽ tắt gate.
8. Thông điệp commit: nêu **đo được gì**, kèm số. Kết bằng:
   `Co-Authored-By: Codex <noreply@openai.com>`

## 6. Điều kiện dừng — tôn trọng, đừng cố cho xong

- Đường vá đòi `ops/NO_KY_THUAT.md` hoặc đòi đảo `t34` ⇒ **DỪNG** (thuộc `#209`).
- Chốt phải nằm ngoài write set ⇒ DỪNG, xuất handoff.
- Thấy một tiêu chí ở §4 là **sai** ⇒ DỪNG và nói, đừng tự đổi giữa đường.
- Gặp lại **đúng hình dạng** "một dạng cú pháp shell mới làm phép kiểm thua" ở chỗ `t34` ⇒ DỪNG.
  Đó là hình dạng đã lặp bốn lần, và `#209` sinh ra để xử nó bằng kiến trúc khác.

## 7. Trả lời

Báo cáo ngắn ở cuối: **bốn việc** đã làm gì, số đo (`N/N`, `rc`, bảng bốn đột biến mới), và
**cái gì còn hở** — mục cuối **bắt buộc**, đừng để trống.
