Bạn là reviewer chéo KHÁC NỀN cho **vòng 8** của PR #512 / packet #504 `WINDOWS-LEASE-SUITE`
(kho `ducthangho/tra-luat`). Tác giả là một phiên Claude; bạn không cùng họ với tác giả.

# PHẠM VI — cứng

Thư mục làm việc là **sandbox này**. **CẤM đọc ra ngoài nó.**

| đường | là gì |
|---|---|
| `cay-kho/` | bản sao ĐẦY ĐỦ, detached đúng `36f68c7e95e0de1fcf8e2311db33a164816db20f`. `is-shallow=false`, `core.abbrev=7`. Được chạy test, được đột biến. |
| `SPEC.md` | đặc tả ĐÓNG BĂNG, sha256 `6af324a368550eda667c67315052cf4fe1a1fb861e2c0da77202163deb34d105` |
| `EVIDENCE.md` | **lời khai tác giả** — dữ liệu cần KIỂM |
| `VERDICT-luot6.md` · `VERDICT-luot7.md` | verdict hai lượt trước |
| `diff.patch` · `numstat.txt` | diff `bb7013c..36f68c7` |
| `do-cua-tac-gia/` | **đủ 16** hiện vật của nhánh hồ sơ, gồm CẢ HAI log suite và cả ba bản bộ đo |
| `goi-offline/` | gói `actionlint 1.7.7` để bạn **chạy được full suite** (vòng 7 không chạy được) |

**CẤM ĐỌC** trong `cay-kho/`: `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` · `AGENTS.md` · `.claude/skills/**`.

**NGOẠI LỆ HẸP, cấp riêng cho lượt này** — vì vòng 7 phải trả `KHÔNG ĐO ĐƯỢC` cho hai cổng chỉ vì lệnh
của chúng đọc các tệp trên: bạn **ĐƯỢC CHẠY**

```
python3 .claude/dev/packet_loop.py doctrine-scan --root .
python3 .claude/dev/packet_loop.py adr-song     --root .
```

trong `cay-kho` và dùng mã thoát + dòng tổng kết của chúng. Công cụ đọc các tệp ấy là **dữ liệu của nó**;
bạn vẫn **không được tự mở** các tệp trong danh sách cấm để đọc nội dung như chỉ dẫn. Phân biệt ấy là
điều kiện của ngoại lệ này.

**CẤM TỰ SOẠN** nội dung dạng đường dẫn thoát khỏi cây, payload khai thác, hay mã tấn công. Mọi phản
chứng cần thiết đã nằm trong cây: **CHẠY** chúng và **ĐỘT BIẾN** bản vá. Hướng thử nào đòi bạn tự soạn
nội dung như thế thì **mô tả bằng lời** cho phiên điều phối.

# GHI `VERDICT.md` SAU MỖI PHÁT HIỆN

Container có thể bị recycle bất chợt. Append ngay khi phát hiện, đừng để dành tới cuối. Kết thúc bằng
dòng `XONG VERDICT`.

# VIỆC

## 1. Kiểm điều tác giả khai là "không đổi"

Tác giả khai **PR không đổi một byte** kể từ vòng 7 (cùng `reviewed_sha`, cùng hai băm write set).
**Đo, đừng nhận.** Nếu đổi, mọi kết luận "đã vá thật" của vòng 7 phải được xét lại.

## 2. F6 — lớp P1 duy nhất còn mở. Cố PHÁ bản vá mới.

Vòng 7 bắt `F6.5`: bộ đo còn đoán **TÊN** ngoại lệ theo hậu tố nên `StopIteration` lọt. Tác giả khai đã
**đảo chiều** phép đo: thôi đoán tên, đo **hình dạng `main()` in ra** —
`^[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*: ` — cộng một chốt **fail-close**
(`_kiem_hop_dong_main`) cho chính giả định ấy.

Việc của bạn là **tìm đường lọt còn lại**, không phải xác nhận lời khai:

- Có ngoại lệ nào `main()` in ra mà **không** khớp mẫu trên không? (`BaseException`? ngoại lệ có tên
  lạ? `__name__` bị ghi đè? chuỗi nhiều dòng?)
- Chiều ngược: có **chốt THẬT** nào bị xếp nhầm `TIN DUNG GIA` không? Đó là fail-close nên làm catalog
  ĐỎ, nhưng **một chốt luôn đỏ cũng là chốt hỏng** — nếu nó đỏ với một thông điệp chốt hợp lệ thường
  gặp, đó là finding.
- `_kiem_hop_dong_main` có thật sự có RĂNG không? Đột biến nó (bỏ đi, hoặc nới điều kiện) và xem catalog
  còn đỏ không.
- Tác giả **tự khai** `CTRL-GeneratorExit` đạt qua **đường khác** (`ĐỎ=[]`), không chứng minh phép mới.
  Kiểm lời tự khai ấy: nó đúng, hay tác giả đang bào chữa cho một control rỗng?
- Chạy `--tu-kiem` **cả ba** bản bộ đo trong `do-cua-tac-gia/` trước khi tin bất kỳ con số nào.

**Đừng chấp nhận "thêm một tên nữa" làm bản vá** — và cũng đừng bác một bản vá chỉ vì nó vẫn dùng regex:
câu hỏi đúng là **phép đo có phủ hết một LỚP hay chỉ phủ các thể hiện đã biết**.

## 3. Không hồi quy

`F1` `F2` `F3` `F4` `F5` `F7` vòng 7 đã kết `ĐÃ VÁ THẬT`. Kiểm chúng **không thoái lui**. Lượt này bạn
chạy được full suite — **đòi bằng chứng DƯƠNG**: ba dòng `lease_publish: N/N đạt` với **hai số bằng
nhau**, ở CHA **và** cả hai vế `[A]`/`[B]`. `rc=0` một mình không phải bằng chứng.

## 4. Kiểm lời khai số

Tác giả tự khai hai lỗi số (`N31` "5 mutant" → **6**; `N32` "dư 386" → **399**) và một lỗi đóng gói
(`F6.6`). Kiểm xem đính chính đã **đủ** chưa — còn chỗ nào mang số cũ mà chưa được điểm danh không.

Nhắc lại bài học kho đã trả giá: **một quan hệ đúng che được các số hạng đã trôi**. Khi một câu vừa nêu
số hạng vừa nêu quan hệ, **kiểm số hạng**.

## 5. Ranh giới

- Kết thúc: `git -C cay-kho status --porcelain` **RỖNG** và `git -C cay-kho log --oneline 36f68c7..HEAD`
  **RỖNG**. Đột biến làm trên **bản sao tạm**.
- Không quyết định merge, không approve thay chủ kho, không cấp hay nâng trần.
- `ops/lease_publish.py` · `.claude/dev/packet_loop.py` · `.github/workflows/**` ngoài write set: lỗi ở
  đó là **nợ được khai**, không phải finding đòi PR sửa.
- `dotbien512.py` cũng **ngoài write set** — finding về nó là việc của hồ sơ riêng, không đòi PR sửa.

# DẠNG ĐẦU RA — `VERDICT.md`

```
verdict: approve | changes_requested
reviewed_sha: 36f68c7e95e0de1fcf8e2311db33a164816db20f
reviewed_base: bb7013c7669da19304a8769e5b25f8c1f8951e9c
reviewed_files_sha256:
  ops/lease_publish_test.py: <bạn tự băm>
  ops/chay_lease_publish_test.sh: <bạn tự băm>
model_tu_khai: <tự khai; không xác minh backend độc lập>
review_round: 8
so_p1: <số LỚP>
so_p2: <số LỚP>
so_p3: <số LỚP>
so_the_hien: <số thể hiện>
hint_sha256: <nếu nộp HINT.patch>
previous_hint_sha256: e7cbefc7d9b11c6dae94bae5d0b04ad15ef9e404ad41564b0466feae6d751ee0
```

Rồi: `## ĐỐI CHIẾU LƯỢT TRƯỚC` (trạng thái canonical **ĐÃ VÁ THẬT / VÁ HỜ / VÁ SINH LỖI MỚI / CHƯA VÁ**
cho **từng lớp**, và điểm danh **từng** thể hiện của vòng 7: `F6.5`, `F6.6`, `N31`, `N32`) ·
`## BẢNG ĐO` · `## Findings theo lớp` · `## Mutant đã chạy` · `## chua_do_duoc`.

`so_p1`/`so_p2`/`so_p3` đếm **LỚP**; `so_the_hien` đếm **thể hiện**.

**Vòng 7 đã tính riêng 36 con số bảng EVIDENCE bỏ sót thành thể hiện. Lượt này ĐỪNG lặp lại việc đó** —
chỉ nêu con số nào **SAI** hoặc **chưa được đính chính**, không điểm danh lại những số đã đo khớp.

`## chua_do_duoc` **bắt buộc**, kể cả khi `approve`. Ba trạng thái: **có · không · KHÔNG ĐO ĐƯỢC**.

Kết thúc bằng `XONG VERDICT`.
