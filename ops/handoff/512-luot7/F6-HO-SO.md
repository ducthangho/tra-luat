# F6 — bộ đo đột biến cấp TÍN DỤNG GIẢ: nguyên nhân gốc, bản vá, và phần KHÔNG đóng được

**Hiện vật:** `ops/handoff/512-luot7/dotbien512.py` (bản đã vá) · `dotbien512_REGEX_CU.py` (phản chứng,
khác đúng MỘT dòng) · `tukiem-cu.txt` / `tukiem-moi.txt` (đầu ra hai chiều).

**Vì sao đi hồ sơ riêng:** `dotbien512.py` là **bộ đo**, không phải sản phẩm. Nó nằm ngoài write set
exact của lease (`ops/lease_publish_test.py` · `ops/chay_lease_publish_test.sh`), nên vá nó trong PR #512
là chạm đường thứ ba ⇒ điều kiện dừng `S1`. Reviewer vòng 6 nói thẳng: *"Sửa công cụ ngoài write set
bằng hồ sơ riêng; không lén đưa nó vào HINT."*

## Nguyên nhân gốc — đo, không đọc code

Dòng phân hạng cũ:

    vo_can = re.match(r"^[A-Za-z_][A-Za-z0-9_.]*(Error|Exception)\s*:", chi_tiet_do)

`main()` của bộ test in lý do ĐỎ theo HAI đường khác nhau:

| ngoại lệ | `main()` in |
|---|---|
| `AssertionError` (chốt của ca đích, qua `bang()`) | `str(ex)` — **không** tiền tố kiểu |
| mọi ngoại lệ khác | `f"{type(ex).__name__}: {ex}"` — **có** tiền tố kiểu |

Nên "có tiền tố `<Kiểu>Error:`/`<Kiểu>Exception:`" đúng là dấu của một ngoại lệ VÔ CAN. Lỗ: regex đòi
**ít nhất một ký tự** (`[A-Za-z_]` bắt buộc) TRƯỚC `Error|Exception`, nên hai dạng **TRẦN** không khớp:

| chuỗi | regex cũ | hệ quả |
|---|---|---|
| `Exception: CONTROL vo can…` | **KHÔNG khớp** | cấp `GIET THAT` — thể hiện reviewer vòng 6 khai |
| `Error: …` (lớp tên đúng bằng `Error`) | **KHÔNG khớp** | cấp `GIET THAT` — **thể hiện THỨ HAI, vòng 6 không khai** |
| `RuntimeError: …` · `ValueError: …` | khớp | loại đúng |

Hai thể hiện, **một lỗ gốc**: tiền tố bắt buộc. Đây đúng hình dạng *"vá đúng chỗ được chỉ rồi bỏ sót
đường thứ ba"* của `CLAUDE.md` — nên vá theo LỖ, không vá theo danh sách thể hiện reviewer liệt kê.

## Bản vá

Chuyển tiền tố thành **tuỳ chọn**: `^(?:[A-Za-z_][A-Za-z0-9_.]*)?(?:Error|Exception)\s*:`

Hướng sai còn lại là **fail-close**: một thông điệp chốt THẬT vô tình bắt đầu bằng `<Từ>Error:` sẽ bị xếp
`TIN DUNG GIA`, tức **làm catalog ĐỎ** chứ không cấp tín dụng khống.

## Răng — phản chứng HAI CHIỀU, chạy được

Bốn `CONTROL` mà ta **biết trước đáp án**, mỗi cái là một đột biến THẬT đi qua đúng đường catalog dùng
(không phải phép thử regex trên chuỗi bịa). Chạy: `python3 dotbien512.py <gốc-kho> --tu-kiem`.

| bản | kết quả | rc |
|---|---|---|
| `dotbien512_REGEX_CU.py` (khác đúng 1 dòng) | **2/4** — `Exception` TRẦN và `Error` TRẦN cùng ra `GIET THAT` | **1** |
| `dotbien512.py` (đã vá) | **4/4 đúng phân hạng** | **0** |

Ca thứ tư là ca **DƯƠNG** (`CTRL-chet-DUNG-chot-ca-dich`, mutant `M15`), cố ý có mặt: thiếu nó thì một
bản vá "cho mọi thứ là TIN DUNG GIA" cũng qua được ba ca âm — một chốt LUÔN ĐỎ cũng là chốt hỏng.

## KHÔNG ĐÓNG ĐƯỢC — khai thẳng, đây là phần còn nợ

Bộ đo chạy **ngoài tiến trình** và chỉ đọc **CHUỖI** trên stdout. Một dòng trong chính tệp test dạng

    except Exception as e: raise AssertionError(f"... {type(e).__name__}")

vẫn **giả được** tín hiệu "đã chết bằng chốt của ca đích" — đúng bài học `#355`/`#359` của `CLAUDE.md`,
nơi bộ phân hạng bị lừa bởi một dòng viết với ý định TỐT. Bản vá này thu hẹp lỗ, **không đóng** nó.

Đóng hẳn đòi tín hiệu là thứ **mã triển khai không giả được**: một LỚP NGOẠI LỆ RIÊNG có danh tính đi tới
được bộ đo. Kho đã có sẵn `TinHieuChotCa(AssertionError)` (`ops/lease_publish_test.py:4328`) nhưng:
- nó chỉ dùng cho khối `A0`/`t139`, các ca `#504` (`t125`/`t158`/`t160`) khẳng định bằng `bang()` trần;
- và **danh tính lớp chết ở `main()`**: nhánh `except AssertionError` in `str(ex)`, mất tên lớp.

Nên đóng hẳn = sửa `main()` phát một dấu riêng cho `TinHieuChotCa` ⇒ **thay đổi write set**
(`ops/lease_publish_test.py`) giữa lúc dự đoán vòng 7 là vòng chốt. **Đề xuất cho chủ kho, KHÔNG tự làm.**

Trạng thái đúng của F6 sau lượt này: **ĐÃ VÁ THẬT phần đo được, CÒN NỢ phần chống giả mạo tín hiệu** —
không phải "F6 đã đóng".

---

# CẬP NHẬT SAU VÒNG 7 — bản vá trên KHÔNG ĐỦ, và nó hụt đúng chỗ chính nó cảnh báo

Cross-review vòng 7 (`VERDICT.rvwin512-7.md`, sha256 `f3604ab0be75919e5146bd5ccaf6dc738cc73b19d10e8714f6243ecc0d363d4e`)
giữ **F6 = VÁ HỜ, P1**, finding **F6.5**: `raise StopIteration(...)` vẫn được cấp `GIET THAT`.

**Vì sao hụt, nói thẳng:** bản vá vòng 6 chỉ nới regex cho tiền tố thành tuỳ chọn, nhưng **vẫn đoán TÊN
ngoại lệ** qua hậu tố `Error|Exception`. `StopIteration` không mang hậu tố ấy. Đó đúng là bệnh
**"danh sách CẤM không bao giờ đủ"** của `CLAUDE.md` — và tệp này, ở bản trước, **đã trích đúng bài học
"vá theo LỖ, không vá theo danh sách thể hiện" rồi vẫn mắc lại nó**. Thêm `StopIteration` vào danh sách
chỉ để lại `GeneratorExit`, `KeyboardInterrupt`, `SystemExit`, và **mọi lớp tự định nghĩa**.

## Bản vá thứ hai — ĐẢO CHIỀU phép đo

Thôi đoán TÊN; đo **HÌNH DẠNG mà `main()` thật sự in ra**. `main()` có đúng hai nhánh:

```
except AssertionError as ex: hong.append((fn.__name__, str(ex)))                        <- CHỐT ca đích
except Exception       as ex: hong.append((fn.__name__, f"{type(ex).__name__}: {ex}"))  <- VÔ CAN
```

Nên dấu của "vô can" là: chi tiết **bắt đầu bằng một ĐỊNH DANH Python (có thể có chấm) rồi `: `**.
Mọi tên lớp ngoại lệ đều là định danh Python ⇒ phép này phủ **toàn bộ** nhánh thứ hai. **Không còn danh
sách nào để mà thiếu.**

`_DANG_VO_CAN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*: ")`

## Chốt FAIL-CLOSE cho chính giả định ấy

Phép trên **neo vào hợp đồng in của `main()`**. Trước đây bộ đo giả định hợp đồng ấy **âm thầm**; nay nó
**ĐO**: `_kiem_hop_dong_main(NGUON)` đòi cả hai mảnh nguyên văn còn trong nguồn, và **`SystemExit` ngay
lập tức** nếu thiếu — chứ không im lặng phân hạng sai. Một bộ đo tự tắt khi mất giả định của nó là bộ đo
không tồn tại đúng lúc nó cần nhất.

## Răng — ba phép đo, chạy được

| phép đo | kết quả | rc |
|---|---|---|
| bản MỚI, 7 control | **7/7 đúng phân hạng** | **0** |
| `dotbien512_VA_VONG6.py` — **cùng 7 control**, khác đúng **một dòng** phép đo | **5/7**; ĐỎ đúng ở `StopIteration` **và** lớp tự định nghĩa `Bung` | **1** |
| đổi hợp đồng in của `main()` trong cây giả lập | bộ đo **TỰ CHẶN**, in `CHAN: main() không còn in theo hai hình dạng…` | **1** |
| catalogue 16 đột biến, đo lại bằng bộ đo mới | `16/16 giết thật`, **không ca nào đổi phân hạng** | **0** |

Ba control mới cố ý **không mang hậu tố** `Error`/`Exception` — chúng là phản chứng cho **chính cách vá
cũ**: bất kỳ bản vá nào còn đoán TÊN ngoại lệ sẽ ĐỎ ở đó. Reviewer khai một thể hiện (`StopIteration`);
đo lại ra **hai** (thêm lớp tự định nghĩa `Bung`).

**Nói cho đúng về `CTRL-GeneratorExit`:** nó ra `TIN DUNG GIA` qua một **đường KHÁC** — `GeneratorExit`
là `BaseException` nên `except Exception` của `main()` không bắt, không sinh dòng `ĐỎ` nào, và ca rơi vào
nhánh `ĐỎ=[] — không phải ca đích`. Nó **không** chứng minh phép `_DANG_VO_CAN`; giữ lại vì nó chặn một
đường tín dụng khống khác. Đừng đọc `7/7` thành "bảy phép đo cho cùng một chốt".

## Vẫn CÒN NỢ — phạm vi không đổi

Bộ đo chạy **ngoài tiến trình** và đọc **chuỗi**. Một `except Exception as e: raise AssertionError(f"…")`
**trong tệp test** vẫn giả được tín hiệu chốt. Vòng 7 xếp việc ấy là `KHÔNG ĐO ĐƯỢC` (reviewer không tự
soạn mã giả mạo, đúng ràng buộc đã giao). Đóng hẳn đòi `main()` phát dấu riêng cho một lớp tín hiệu ⇒
**thay đổi write set** ⇒ vẫn là **đề xuất cho chủ kho**, không tự làm.

Trạng thái F6 sau lượt này: **ĐÃ VÁ THẬT phần "ngoại lệ vô can" (đo được, phủ toàn nhánh), CÒN NỢ phần
chống giả mạo tín hiệu.** Không viết mạnh hơn.

## F6.6 — đính chính lời khai, không phải sửa mã

Vòng 7 đúng: `EVIDENCE.rvwin512-7.md` nói **cả hai** log ở `do-cua-tac-gia/`, nhưng gói giao cho reviewer
chỉ có **một**. Log `153/155` có thật và **nằm trong kho** tại `ops/handoff/512-luot7/suite-36f68c7-THIEU-shellcheck.log`;
lỗi là ở **khâu đóng gói sandbox**, không phải hiện vật thiếu. Lượt sau: đóng gói ĐỦ, hoặc khai rõ tệp nào
không nằm trong gói.

---

# CHỐT SAU VÒNG 8 — F6 đã DỜI sang packet riêng, và bản mặc định được chọn BẰNG PHÉP ĐO

Chủ kho quyết (#504 comment `5646460376`): **dời F6 sang packet riêng**, `#512` land, F6 thành **nợ có
tên** — `ops/NO_KY_THUAT.md` §23 `BO-DO-DOT-BIEN-SUY-LY-DO-CHET-TU-CHUOI-STDOUT`. Tệp này giữ lại diễn
biến; sổ nợ là nơi có **điều kiện coi là XONG**.

## Bộ control nay có 10 ca, và bản mặc định TỰ BÁO ĐỎ

Thêm ba ca mà bộ 7 ca cũ **thiếu** — hai ca của vòng 8 (`F6.7` tên lớp **Unicode**, `F6.8` **thông điệp
rỗng**) và một **control DƯƠNG thứ hai** lấy nguyên assertion có sẵn trong cây
(`t96_lease_cham_duong_khop_tuyet_doi_khong_phai_chua`, mọi thông điệp của nó mở đầu `t96: `).

Chọn mặc định từ bộ control thiếu chính là lặp lại lỗi *"danh sách bạn giao trở thành TRẦN của họ"* —
lần này tự áp lên mình. Nên ba bản được dựng **trong MỘT lệnh** từ cùng một nền, khác nhau **đúng một
dòng** phép đo, rồi đo trên **cùng 10 control**:

| bản | tệp | đúng | **lọt** (false GREEN) | **hồi quy** (false RED) |
|---|---|---|---|---|
| `v0` tiền tố bắt buộc | `dotbien512_REGEX_CU.py` | `4/10` rc=1 | 6 | 0 |
| `v6` hậu tố tuỳ chọn | `dotbien512_VA_VONG6.py` | `7/10` rc=1 | 3 | 0 |
| **`v8` định danh + `": "`** | **`dotbien512.py` (MẶC ĐỊNH)** | `7/10` rc=1 | **2** | **1** |

## Vì sao `v8` — và vì sao điều đó KHÔNG mâu thuẫn với verdict vòng 8

Vòng 8 xếp bản vá `v8` là **`VÁ SINH LỖI MỚI`**, và **đúng**: nó thêm một khuyết tật mà `v6` không có.
Nhưng đó là câu hỏi *"bản vá có sinh lỗi mới không"*, khác câu hỏi *"trong ba hiện vật đã đo, giữ cái nào
làm mặc định"*. Phép đo trả lời câu thứ hai:

- **`v6` cấp tín dụng giả cho CẢ BA lớp ngoại lệ của chính kho** — `BoQuaNen`, `TinHieuChotCa`, **`Chan`**
  — vì không tên nào mang hậu tố `Error`/`Exception`. `Chan` là lớp `ops/lease_publish.py` ném **khắp
  nơi**. Đo: `v6` bỏ sót **3/3**, `v8` bắt **3/3**.
- Tập lọt của `v6` **không có biên** ("mọi lớp thiếu hậu tố"); hồi quy của `v8` thì **đếm được**:
  **`8` trong `454`** lời gọi `bang()`/`chot()` trùng hình dạng `^<định danh>: `, trải trên **4 ca** —
  `t96` (4 thông điệp), `t133`, `t136`, `t151`.
- **False GREEN nguy hơn false RED**: một `GIET THAT` khống là lời khai an toàn SAI; một `TIN DUNG GIA`
  khống làm catalogue **ĐỎ**, tức ồn ào và có người điều tra.

**Kế hoạch của phiên này dự đoán sẽ lùi về `v6`, và phép đo BÁC dự đoán ấy.** Ghi ra vì một nguyên nhân
sai trong hồ sơ còn tệ hơn không ghi.

## Bộ đo được giao ở trạng thái TỰ BÁO ĐỎ — cố ý

`dotbien512.py --tu-kiem` ⇒ **`7/10`, `rc=1`**. Bộ control **kèm cả ba ca nó xử sai**, nên mỗi lần tự
kiểm là một lần khuyết tật tự khai. Cắt bộ control cho "vừa khít" để có `10/10` là dựng đúng cái cổng
nói dối mà cả packet này sinh ra để chống.

## Catalogue 16 mutant, đo lại bằng bản mặc định + 10 control

`16/16 giết thật, 0 tín dụng giả, 0 sống sót`, rc=0 — và **không ca nào đổi phân hạng** so lần đo trước
(`dotbien-16-tren-36f68c7-bo-do-10ctrl.txt`). Đổi phép đo không làm xê dịch kết luận về 16 mutant ấy.

Nhưng nói cho đúng phạm vi: con số ấy đáng tin **trong phạm vi 10 control đã đo** và **trên đúng 16
mutant ấy**. Nó **không** là lời khai bộ đo miễn nhiễm tín dụng giả — xem §23 mục *Cái MẤT*.
