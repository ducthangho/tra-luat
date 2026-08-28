verdict: changes_requested
reviewed_sha: f31cdbf3db83c94c087edb990b4df365fab1268d
P1: 0
P2: 3
finding_moi: 3

Ghi chú ngay: **0 P1** — không có finding nào trong lượt này chặn land. Ba P2 dưới đây, theo luật
land của kho ("changes_requested mà chỉ còn P2 thì land được nếu mọi P2 thành nợ CÓ TÊN"), đủ điều
kiện land NẾU người giữ kho chốt chúng thành nợ có tên (hoặc executor vá luôn, rẻ — xem từng mục).
Không có finding nào bị hạ từ P1 xuống P2 để land — cả ba được đánh giá P2 từ đầu, có lý lẽ riêng.

Cây review: clone độc lập tại `/home/user/rv360`, detach đúng `f31cdbf3db83c94c087edb990b4df365fab1268d`,
`core.autocrlf=false core.eol=lf core.abbrev=7` đúng như lease yêu cầu (đã đo, không đổi). `git status
--porcelain` rỗng khi kết thúc; không `add`/`commit`/`push` nào được chạy trong cây thật — mọi đột biến
phản chứng chạy trên **bản sao NGOÀI cây** (`/tmp/.../scratchpad/mcp360/rang{1,2,3,4}` và `.../rang1`).

## ĐỐI CHIẾU LƯỢT TRƯỚC

Đây là lượt review đầu tiên của packet #360 (lượt 1 của cross-review trên PR #365) — không có lượt
trước để đối chiếu. Nhưng packet này TỰ NÓ là remediation của #319 r6; đối chiếu với r6 nằm trong mục
"Trục 1 — item 5" và "PHẢN CHỨNG BẮT BUỘC #5" bên dưới.

## BẢNG ĐO

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| `CA` | 41/41 đạt · 0 đỏ · ĐẠT | `CA         : 41/41 đạt · 0 đỏ · ĐẠT` | khớp |
| `ĐỘT BIẾN` | 51/51 tập giết · ĐẠT | `ĐỘT BIẾN   : đã đo 51/51 tập giết · ĐẠT` | khớp |
| `D8(a)(b)(c)` | ĐẠT cả ba | ĐẠT cả ba | khớp |
| `TỔNG` | ĐẠT | `TỔNG: ĐẠT` | khớp |
| `rc` | 0 | `$?` = 0 (đo bằng `run > out; echo RC=$?`, không qua `tail`) | khớp |
| `D9` hai số hạng | 230 + 670 = 900 | `wc -l .claude/dev/mcp_gh.py .claude/dev/mcp_gh_test.py` → `230` + `670` = `900` | khớp — cả hai SỐ HẠNG đo riêng, không chỉ đo tổng |
| biên D9 | 0 | 230+670=900, trần `<= 900` → đúng biên 0 | khớp |
| mẫu đột biến duy nhất | ngụ ý (ĐỘT BIẾN ĐẠT ⇒ D12 không báo lỗi) | quét tay `src.count(old)` cho cả 51 mẫu → **0 mẫu không duy nhất** | khớp |
| `D10-main` được khôi phục | có dựng cảnh + cờ `da_chay` | đọc mã: đúng, có `class Canh`, gọi `chay_cli` thật, đòi `da_chay == [True]` | khớp |
| chốt fail-close `count != 1` | có | đọc mã dòng 621-623: đúng `if src.count(old) != 1` | khớp |
| lời khai spec "D11 thu hẹp còn một dòng" | ĐÃ SỬA thành câu yếu hơn | đọc `ops/specs/mcp-gh-cuu-ho.md` diff — câu mới khớp NGUYÊN VĂN gợi ý của chính r6 | khớp, không quá mạnh |

## Trục 1 — SPEC

### item 1 — chốt fail-close `count != 1`
**ĐẠT, có răng.** Đọc mã (`chay_dot_bien`, dòng 621): `if src.count(old) != 1: errors.append(f"{name}:
KHÔNG_ĐO_ĐƯỢC (mẫu xuất hiện {src.count(old)} lần)"); continue`. Đây là fail-close thật: không có
đường nào bỏ qua kiểm tra để "đi tiếp im lặng" — đường ĐI TIẾP duy nhất là khi `count == 1`.
Răng đo bằng phản chứng: đổi `!= 1` → `< 1` trên bản sao ngoài cây (`rang4/`), chạy
`python3 mcp_gh_test.py`: `CA 40/41 đạt · 1 đỏ · ĐỎ`, `ĐỎ D12-duy-nhat: AssertionError`, `TỔNG: ĐỎ`,
`rc=1`. Đỏ đúng như kỳ vọng.

### item 2 — "HAI dòng hậu tố", có phải chỉ hai không?

**Không phải hai — có BỐN dòng/biểu thức sinh hậu tố ĐẠT/ĐỎ trong tệp thật (không tính bảng
`MUTATIONS`, đó là DỮ LIỆU):**

| # | dòng | hàm | được canh bằng gì |
|---|---:|---|---|
| 1 | 448 | `dong_dot_bien` (dòng ĐỘT BIẾN) | MUTATIONS entry mới `d11_hau_to_dot_bien_xanh` |
| 2 | 464 | `dong_d8` (ba dòng D8(a)/(b)/(c)) | **KHÔNG có** — xem finding `dong-d8-thieu-canh-rieng` |
| 3 | 657 | `chay_cli` (dòng CA) | MUTATIONS entry mới `d11_hau_to_ca_xanh` |
| 4 | 664 | `chay_cli` (dòng TỔNG) | assertion trực tiếp có SẴN từ trước (dòng 507: `assert f"TỔNG: {'ĐỎ' if do else 'ĐẠT'}" in report`, không phải thêm ở lượt này) |

Vậy: bản vá lượt này ĐÚNG là thêm hai canh mới (#1 và #3) — khớp với khẳng định "hai đột biến canh
hậu tố". Nhưng "hai" đó là **hai canh MỚI**, không phải "tổng cộng có hai dòng cần canh". Dòng #4 đã
an toàn từ trước (không phải việc của lượt này). Dòng #2 (`dong_d8`) là dòng THỨ BA thật sự thiếu,
và cả executor lẫn phiên điều phối đều bỏ sót nó — xem finding bên dưới. Bằng chứng chạy được ở mục
PHẢN CHỨNG #3 (mở rộng) và trong finding.

### item 3 — `D10-main`
**ĐẠT, có răng.** Đọc mã: hàm nay dựng `class Canh: CASES = (("c", lambda: da_chay.append(True)),)`,
gọi `chay_cli(Canh, (), lambda: ({}, []))` thật (không phải gọi thẳng `ma_thoat`), đòi `== 1` VÀ đòi
`da_chay == [True]` — đúng cả hai điều kiện mà đặc tả r4 yêu cầu (mã thoát khác 0 VÀ cờ đã đặt).
Răng đo bằng phản chứng: trên bản sao ngoài cây (`rang1/`), xoá lệnh gọi `fn()` thật trong
`chay_cac_ca` (mô phỏng "main không chạy ca"), gọi trực tiếp `d10_main_khong_chay_ca_phai_do()` →
`AssertionError` — bắt được.

### item 4 — lời khai spec "D11 thu hẹp bề mặt xuống một dòng duy nhất"
**Đã sửa ĐÚNG và KHÔNG quá mạnh.** Câu mới: *"`D11` không xoá được bề mặt, nhưng nó làm mọi đường
làm giả trừ dòng ngoài cùng nhất đều phải để lại vết trong báo cáo."* Đối chiếu với finding
`dong-d8-thieu-canh-rieng` ở trên: forcing `dong_d8` luôn "ĐẠT" **vẫn để lại vết** trong báo cáo hiện
tại (dòng `ĐỎ D11-gate: AssertionError` + `TỔNG: ĐỎ`, xem PHẢN CHỨNG #3 mở rộng) — nên câu spec MỚI
**không bị chính finding của tôi phản bác**; nó chỉ hứa "để lại vết", không hứa "có canh riêng dạng
MUTATIONS", và lời hứa "để lại vết" vẫn đúng cho dòng #2. Đây là lý do tôi xếp finding đó P2 chứ
không P1 — nó không vi phạm lời hứa hiện hành của spec, chỉ là một khoảng hở rộng hơn giữa "có vết"
và "có canh chủ động, không phụ thuộc trùng hợp kịch bản test khác".

## Trục 2 — STANDARDS: D9 900/900 biên 0 đạt được bằng cách nào

**Đây là đánh vào phép đo một phần, không toàn phần — và đáng ghi thành nợ, không chặn land.**

Đo được: bản vá xoá **8 chỗ** hai-dòng-trắng-giữa-hàm-mức-module (giữa `d6_hop_dong_cli_0_2_3` /
`d7_cong_xanh...` / `dong_dot_bien` / `d7b_nen_do...` / `loi_d8` / `dong_d8` / `bang_giao_pham_vi` /
`d8_quy_trach_nhiem...`), làm 11 hàm mức module không còn dòng trắng trước `def` — trong đó **8 là
MỚI do lượt này** (3 còn lại — dòng 175/240/364 — vốn đã không có dòng trắng từ trước, vì đứng ngay
sau một dòng chú thích tiêu đề nhóm `# A —`/`# B —`/`# C/D —`, khác bản chất). Cộng thêm hai dòng
ghép lệnh bằng `;` (`class Canh: CASES = (...)`, `out = sys.stdout = io.StringIO(); assert ...`).
Toàn bộ 670 dòng còn lại của tệp vẫn giữ quy ước 2-dòng-trắng PEP8 giữa hàm mức module (48/59 hàm) —
tự bản vá tạo ra một quy ước KHÔNG NHẤT QUÁN trong CHÍNH tệp nó sửa.

**Lý lẽ của tôi:** đây LÀ đánh vào phép đo, không phải "viết ngắn lại" hợp lệ theo §12 — nội dung
logic không giảm (không hàm nào bị gộp/xoá, không đơn giản hoá thật), chỉ có MẬT ĐỘ DÒNG bị nén để
đi qua đúng ngưỡng `<= 900`. Bằng chứng của chính sự nén này: 8/8 chỗ nén đều nằm sát các hàm MỚI/SỬA
trong đúng diff này (không phải rải đều toàn tệp) — tức nén được thực hiện CÓ MỤC ĐÍCH đưa số dòng
về khớp ngân sách, không phải một đợt dọn dẹp phong cách độc lập.

Hệ quả thực tế đáng nói với người giữ kho: biên **0** tuyệt đối nghĩa là **BẤT KỲ** dòng thêm nào kế
tiếp (kể cả một `assert` một dòng) sẽ đỏ D9 ngay, và đường "chữa" rẻ nhất luôn sẵn có sẽ lại là nén
thêm khoảng trắng — tạo một vòng xoáy làm tệp ngày càng khó đọc mà con số 900 vẫn báo "trong ngân
sách". Đây đúng là lỗ hổng "một bất biến còn đúng không chứng minh các số hạng còn đúng" ở dạng khác:
`230 + 670 <= 900` đúng, nhưng KHÔNG chứng minh 900 dòng đó vẫn giữ nguyên MẬT ĐỘ THÔNG TIN mà D9
được sinh ra để giới hạn.

**Không xếp P1** vì D9 tự nó vẫn ĐẠT theo đúng định nghĩa đo được của nó (đếm dòng vật lý — đó là
những gì `sum(1 for _ in path.open())` làm, không hơn không kém); tôi không có căn cứ để nói bản vá
làm SAI phép đo D9 — nó chỉ khai thác đúng cách D9 được ĐỊNH NGHĨA. Xếp P2: nợ có tên, khuyến nghị
người giữ kho quyết định một trong hai — (a) chấp nhận biên 0 và cấm nén khoảng trắng thêm trong quy
ước tương lai, hoặc (b) đo lại xem có nên đổi D9 sang đếm theo cách khác (vd. bỏ dòng trắng khỏi cả
hai phía trước khi đếm, hoặc đặt trần thấp hơn 900 để chừa biên thật).

## Trục 3 — `d12_mau_dot_bien_phai_duy_nhat` thiếu `try`/`finally`

**P2 — có cơ chế rò rỉ trạng thái toàn cục thật, nhưng KHÔNG có đường khai thác được trong cách nó
đang được gọi hôm nay. Phán quyết của tôi, kèm phản chứng hai chiều.**

Mã (dòng 528-532):
```python
def d12_mau_dot_bien_phai_duy_nhat():
    global MUTATIONS
    cu, MUTATIONS = MUTATIONS, (("trung", "test", "def ", "x", "D12-duy-nhat"),)
    _, errors = chay_dot_bien(); MUTATIONS = cu
    assert errors and errors[0].startswith("trung: KHÔNG_ĐO_ĐƯỢC (mẫu xuất hiện ")
```

**(a) Cơ chế rò rỉ là THẬT, đo được.** Phản chứng độc lập (không đụng cây thật, chạy trong module nạp
riêng): gọi một hàm mô phỏng ném `RuntimeError` đúng vị trí `chay_dot_bien()`, không có `finally` →
`MUTATIONS` ở lại `len == 1` (thay vì 51) VĨNH VIỄN cho phần còn lại của tiến trình. Đúng hình dạng
"bom hẹn giờ" mà `CLAUDE.md` đã cảnh báo, dù ở đây là BỘ NHỚ chứ không phải ĐĨA.

**(b) Nhưng: `chay_dot_bien()` với ĐÚNG mẫu `("trung", "test", "def ", "x", ...)` mà `d12` dùng thì
KHÔNG THỂ ném ra ngoài trong đường thực thi hiện tại.** Lý do, đọc mã `chay_dot_bien` (dòng 619-646):
mẫu `"def "` xuất hiện rất nhiều lần trong `mcp_gh_test.py` (nhiều `def` hàm) nên
`src.count("def ") != 1` LUÔN đúng → nhánh fail-close bắt trước, `continue` ngay, KHÔNG BAO GIỜ chạm
tới khối `with tempfile.TemporaryDirectory()...try/except Exception` — tức không bao giờ chạm tới
phần mã có khả năng ném lỗi hệ thống thật (đĩa/IO) mà KHÔNG bị `except Exception` nội bộ của chính
`chay_dot_bien()` nuốt mất trước khi lộ ra ngoài. Đã đọc toàn bộ thân hàm để xác nhận: MỌI exception
trong nhánh xử lý mutation thật đều bị bọc bởi `except Exception as e: errors.append(...)` NGAY BÊN
TRONG `chay_dot_bien()` — đường raise-ra-ngoài duy nhất còn lại là lỗi hệ thống ở
`tempfile.TemporaryDirectory().__enter__`/`__exit__` (nằm ngoài `try` nội bộ), và đường đó không thể
chạm tới vì mẫu của `d12` không bao giờ vượt qua chốt duy-nhất để đi tới đó.

**(c) Ngay cả khi giả định GIẢ ĐỊNH TỆ NHẤT (một lỗi hệ thống thật ném ra từ `chay_dot_bien()`), hệ
quả quan sát được vẫn KHÔNG sai:** `D12-duy-nhat` là **CASE CUỐI CÙNG** trong `CASES` (xác nhận bằng
`grep`, dòng 545). Một exception ném ra từ thân `d12_...` bị bắt bởi `except Exception` của
`chay_cac_ca` (bọc quanh MỌI case), biến thành một case ĐỎ hợp lệ — và vì `chay_cli` chỉ gọi
`run_mutants()` (bản `chay_dot_bien` THẬT, dùng `MUTATIONS` toàn cục) KHI `not failed`, một case đã
đỏ (kể cả D12) khiến `chay_cli` **bỏ qua hoàn toàn** lần gọi `chay_dot_bien()` thật — nên
`MUTATIONS` bị hỏng cũng KHÔNG BAO GIỜ được đọc lại trong CÙNG một lần chạy `python3
mcp_gh_test.py`. Tiến trình luôn thoát ngay sau đó (`sys.exit(chay_cli())` ở `__main__`).

**Kết luận của tôi: P2, không P1.** Đây là một vi phạm THẬT của quy ước cục bộ (đúng ba dòng phía
trên, `d11_chay_cli_khong_duoc_xanh_khi_d8_do` dùng `try/finally` cho đúng kiểu swap-restore này —
`d12` phá vỡ chính tiền lệ liền kề của nó), và là nợ kỹ thuật đáng vá (rẻ — bọc bằng `try/finally`
hoặc context manager). Nhưng nó KHÔNG P1 vì: không có đường thực thi nào — với mã hiện tại, với vị
trí hiện tại của `D12-duy-nhat` trong `CASES` — biến rò rỉ trạng thái này thành một kết quả SAI
(ĐẠT giả). Nếu tương lai có ai đổi mẫu đột biến của `d12` sang một chuỗi DUY NHẤT thật (để nó thực sự
đi vào nhánh `tempfile`/`nap_dot_bien`), hoặc chuyển `D12-duy-nhat` ra khỏi vị trí cuối cùng của
`CASES`, thì rủi ro này sống dậy — khuyến nghị vá TRƯỚC khi một trong hai điều đó xảy ra, nhưng không
cần chặn packet này.

## PHẢN CHỨNG BẮT BUỘC — đã chạy, kết quả

1. `python3 .claude/dev/mcp_gh_test.py` (chạy trong cây review tại `f31cdbf`, đo `$?` KHÔNG qua
   `tail`/pipe để tránh lỗi "MA=$? sau pipeline"): `CA 41/41 đạt · 0 đỏ · ĐẠT`, `ĐỘT BIẾN đã đo
   51/51 tập giết · ĐẠT`, `D8(a)(b)(c) ĐẠT`, `TỔNG: ĐẠT`, `rc=0`. **Khớp hoàn toàn khẳng định của PR.**
2. `wc -l .claude/dev/mcp_gh.py .claude/dev/mcp_gh_test.py` → `230` và `670` — hai số hạng đo RIÊNG,
   khớp `230+670=900`. Biên `<= 900` đúng bằng 0.
3. Răng bốn chốt mới, đo trên bản sao NGOÀI cây (`/tmp/.../scratchpad/mcp360/rang1..4`), mỗi chốt
   một thư mục riêng để không đè lẫn nhau:
   - `D10-main`: xoá lệnh gọi `fn()` thật trong `chay_cac_ca` → gọi case → `AssertionError`. **Đỏ.**
   - `d11_hau_to_dot_bien_xanh`: ép hậu tố `dong_dot_bien` luôn `"ĐẠT"`, chạy TOÀN BỘ
     `python3 mcp_gh_test.py` → `CA 40/41 · 1 đỏ · ĐỎ`, `ĐỎ D11-gate: AssertionError`, `TỔNG: ĐỎ`,
     `rc=1`. **Đỏ.**
   - `d11_hau_to_ca_xanh`: ép hậu tố dòng CA luôn `"ĐẠT"`, chạy toàn bộ → `CA 40/41 · 1 đỏ · ĐẠT`
     (dòng CA tự nó nói dối) nhưng `ĐỎ D11-gate: AssertionError` + `TỔNG: ĐỎ`, `rc=1`. **Đỏ — đúng
     kiểu "để lại vết" mà spec hứa, dù chính dòng bị ép vẫn nói dối.**
   - `d12_bo_chot_duy_nhat`: đổi `!= 1` → `< 1`, chạy toàn bộ → `CA 40/41 · 1 đỏ · ĐỎ`,
     `ĐỎ D12-duy-nhat: AssertionError`, `TỔNG: ĐỎ`, `rc=1`. **Đỏ.**
   Cả bốn chốt mới đều CÓ RĂNG — không chốt nào là cổng giả.
4. Quét toàn bộ 51 mục trong `MUTATIONS`, đo `src.count(old)` cho từng mục (không đọc, tính tay):
   **0 mục có count != 1.** Không có mẫu đột biến nào mất răng do trùng lặp — khớp với `ĐỘT BIẾN
   51/51 ĐẠT` và với việc `D12` không báo lỗi nào trong lần chạy thật.
5. Hai P1 của #319 (theo `ops/reviews/mcp-gh-cuu-ho-kiem-doc-lap-r6.md`, đọc từ nhánh
   `ops/cap-lease-tach-314` — tệp không có trên `f31cdbf`, đúng như lease đã ghi chú "hồ sơ có thẩm
   quyền nằm ở nhánh spec"):
   - N7 (dòng 657/CA không có đột biến canh) → **đóng**, xem phản chứng #3 dòng `d11_hau_to_ca_xanh`.
   - `D10-main` hồi quy về mệnh đề luôn đúng → **đóng**, xem phản chứng #3 dòng `D10-main`.
   - Khuyết tật NỀN (bộ chạy đột biến thiếu chốt duy-nhất) → **đóng**, xem phản chứng #1, #3 (dòng
     `d12_bo_chot_duy_nhat`), #4.
   **Cả hai P1 đã đóng bởi bản vá này, có bằng chứng chạy được cho từng cái — không phải suy luận.**
   Tôi KHÔNG hạ P2 mới tìm được (dong_d8, D9-gaming, d12-finally) xuống mức thấp hơn để "cho land dễ
   hơn"; ngược lại tôi cũng không nâng chúng thành P1 để giữ packet mở — cả ba đứng vững ở P2 theo lý
   lẽ đã trình bày ở từng mục.

## Findings

### dong-d8-thieu-canh-rieng  [P2]  Dòng hậu tố ĐẠT/ĐỎ thứ ba (D8(a)/(b)/(c)) không có canh riêng
TỆP/DÒNG: `.claude/dev/mcp_gh_test.py:459-465` (hàm `dong_d8`)
VẤN ĐỀ: `dong_d8` là dòng/tổ hợp dòng thứ BA (sau `dong_dot_bien` dòng 448 và dòng CA 657) sinh hậu
tố ĐẠT/ĐỎ theo một ternary có điều kiện (`f"ĐỎ {bad!r}" if bad else "ĐẠT"`), nhưng KHÔNG có MUTATIONS
entry dạng `d11_hau_to_...` canh nó, và cũng KHÔNG có assertion trực tiếp kiểu `dong_dot_bien(...).
endswith("ĐỎ")` như hai dòng kia mới được thêm ở lượt này. Nó chỉ được bắt một cách GIÁN TIẾP, nhờ
đúng kịch bản test có sẵn trong `d11_chay_cli_khong_duoc_xanh_khi_d8_do` (`kill_sets={"m": ()}`) vô
tình khiến D8(b) là nguồn "ĐỎ" DUY NHẤT trong báo cáo ở kịch bản đó — đúng hình dạng "có đường khác
bắt hộ không phải có phản chứng" mà chính `ops/reviews/mcp-gh-cuu-ho-kiem-doc-lap-r6.md` đã dùng để
buộc thêm canh cho dòng CA.
FAILURE_SCENARIO: nếu một lượt sửa sau này thay đổi kịch bản `kill_sets` trong bài test D11-gate
(vd. đổi `{"m": ()}` thành một trường hợp khác không kích D8(b)), thì việc ép `dong_d8` luôn trả
"ĐẠT" sẽ trở thành hoàn toàn vô hình — lặp lại đúng lỗi N7 mà packet #319/#360 này sinh ra để sửa,
chỉ ở một dòng khác.
ĐÃ THỬ VÁ: không — nằm ngoài write set của packet (`ops/specs/mcp-gh-cong-tu-canh-packet-issue-nhap.md`
chỉ giao 2 tệp, không phải việc mới); báo cáo để người giữ kho quyết định vá ngay hay ghi nợ.
ĐÃ THỬ NGHIỆM: có — trên bản sao ngoài cây (`rang2/`, dùng lại), ép ternary của `dong_d8` (dòng 464)
luôn `"ĐẠT"`, chạy `python3 mcp_gh_test.py`: `CA 40/41 · 1 đỏ · ĐẠT` (dòng CA tự nó không nói dối ở
đây), `ĐỎ D11-gate: AssertionError`, `TỔNG: ĐỎ`, `rc=1`. **Hiện tại VẪN bị bắt** — không phải một lỗ
hổng đang mở, mà là một canh MỎNG dựa trên trùng hợp kịch bản, đúng như lời khai mới của spec
("để lại vết") vẫn đúng ở đây.
ĐỘ TIN: cao (đọc mã trực tiếp + hai lần chạy phản chứng độc lập, một lần trong cây review một lần
ngoài cây).

### d9-nen-khoang-trang-danh-vao-phep-do  [P2]  Ngân sách 900/900 biên 0 đạt một phần bằng nén hình
thức, không phải giảm nội dung
TỆP/DÒNG: `.claude/dev/mcp_gh_test.py` (8 vị trí, các hàm mức module từ `d6_hop_dong_cli_0_2_3` đến
`d8_quy_trach_nhiem_ba_dieu_kien`)
VẤN ĐỀ: bản vá xoá dòng trắng phân cách 8 hàm mức module (PEP8 hai dòng trắng → không dòng nào),
trong khi 48 hàm khác trong CHÍNH tệp này vẫn giữ hai dòng trắng — tạo quy ước không nhất quán ngay
trong một tệp, chỉ để đưa tổng dòng về đúng `<= 900`. Kèm hai lệnh ghép bằng `;`
(`class Canh: CASES = (...)`, `out = sys.stdout = io.StringIO(); assert ...`).
FAILURE_SCENARIO: biên 0 tuyệt đối nghĩa là bất kỳ thêm-dòng nào trong tương lai (kể cả một dòng
assert hợp lệ) sẽ đỏ D9 ngay lập tức, và cám dỗ rẻ nhất để "vá" luôn sẵn có là nén thêm khoảng trắng
— một vòng xoáy làm tệp khó đọc dần trong khi con số 900 vẫn báo "trong ngân sách", đúng lớp lỗi
"một bất biến còn đúng không chứng minh các số hạng còn đúng" ở dạng biến thể (ở đây "số hạng" là
MẬT ĐỘ THÔNG TIN trên mỗi dòng, không phải chỉ số dòng).
ĐÃ THỬ VÁ: không — đây là câu hỏi chính sách cho người giữ kho (chấp nhận biên 0 và cấm nén thêm,
hay xét lại cách D9 đếm), không phải một lỗi có một cách vá "đúng" duy nhất.
ĐÃ THỬ NGHIỆM: có — đếm bằng `awk`: 48 hàm còn 2-dòng-trắng, 3 hàm zero-blank tiền-tồn-tại (đứng sau
dòng chú thích tiêu đề nhóm, không liên quan diff này), **8 hàm zero-blank MỚI do diff này** (dòng
442, 444, 449, 451, 459, 466, 477, 483 trên bản HEAD).
ĐỘ TIN: cao (đo trực tiếp bằng công cụ đếm, đối chiếu với bản trước diff qua `git show f461413a:...`).

### d12-thieu-try-finally  [P2]  Swap `MUTATIONS` toàn cục không có `try`/`finally`
TỆP/DÒNG: `.claude/dev/mcp_gh_test.py:528-532` (hàm `d12_mau_dot_bien_phai_duy_nhat`)
VẤN ĐỀ: xem phân tích đầy đủ ở "Trục 3" trên. Tóm tắt: cơ chế rò rỉ trạng thái toàn cục là THẬT (đã
tái hiện bằng phản chứng bên ngoài), nhưng KHÔNG khai thác được với mã/thứ tự case hiện tại (mẫu
`"def "` luôn không duy nhất → không bao giờ chạm nhánh có thể ném lỗi hệ thống; và `D12-duy-nhat` là
case CUỐI trong `CASES` nên dù có raise, `chay_cli` vẫn đúng cách bỏ qua lần gọi `chay_dot_bien()`
thật). Vi phạm quy ước cục bộ: đúng ba dòng phía trên, `d11_chay_cli_khong_duoc_xanh_khi_d8_do` dùng
`try/finally` cho đúng kiểu swap-restore (`cu_out = sys.stdout ... finally: sys.stdout = cu_out`).
FAILURE_SCENARIO: nếu một lượt sau đổi mẫu đột biến của `d12` sang một chuỗi thật sự duy nhất (để nó
đi vào nhánh `tempfile.TemporaryDirectory()`), HOẶC di chuyển `D12-duy-nhat` ra khỏi vị trí cuối cùng
trong `CASES`, một lỗi hệ thống (đĩa đầy, quyền `/tmp`) giữa chừng sẽ để `MUTATIONS` toàn cục ở trạng
thái 1-phần-tử cho các case CHẠY SAU trong CÙNG tiến trình — rủi ro thật nhưng chưa mở hôm nay.
ĐÃ THỬ VÁ: không — nằm ngoài write set của packet.
ĐÃ THỬ NGHIỆM: có, hai chiều — (a) tái hiện cơ chế rò rỉ bằng mock ném `RuntimeError` thay
`chay_dot_bien()`, xác nhận `MUTATIONS` ở lại `len==1` sau khi exception thoát ra ngoài; (b) đọc toàn
bộ thân `chay_dot_bien()` xác nhận MỌI exception trong nhánh xử lý mutation thật bị `except
Exception` nội bộ nuốt trước khi ra ngoài, và mẫu `"def "` của `d12` luôn bị chốt duy-nhất chặn
TRƯỚC khi chạm nhánh có thể raise; (c) xác nhận bằng `grep` rằng `D12-duy-nhat` là case CUỐI trong
`CASES`, nên dù giả định tệ nhất (raise thật) xảy ra, `chay_cli` vẫn bỏ qua đúng cách lần gọi
`chay_dot_bien()` thật nhờ `failed` non-empty.
ĐỘ TIN: cao (đọc mã đầy đủ + phản chứng tái hiện cơ chế + xác nhận vị trí case bằng công cụ, không
suy diễn).
