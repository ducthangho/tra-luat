verdict: changes_requested
reviewed_sha: 73c91cb2cd0da6ec571ff736f5a715e223db35c5
P1: 0
P2: 1
P3 (khong chan land, ghi no): 1
finding_moi: 2

## Bối cảnh lượt review

Đây là lượt `cross_approved` ĐẦU TIÊN thật (reviewer_provider=claude, executor=codex). Ba lượt
`codex` trước trên chính PR này (`36cac457` · `0797458234` · `73c91cb2` "Breezy!") CÙNG nhà cung
cấp với executor nên KHÔNG thoả `assurance_target: cross_approved` mà lease đòi — coi là lời khai
cần kiểm, không phải bằng chứng.

Sandbox: clone độc lập `/tmp/.../scratchpad/review362/cay`, `origin` đã `set-url` về
`https://github.com/ducthangho/tra-luat`, detach đúng `73c91cb2…`, `core.autocrlf=false
core.eol=lf core.abbrev=7` đã ghim. `git status --porcelain` rỗng trên CẢ sandbox lẫn cây thật
trong suốt lượt review (kiểm lại lúc viết verdict này). Không `add`/`commit`/`push` nào được chạy.

## ĐỐI CHIẾU LƯỢT TRƯỚC (ba P2 để mở từ #357, cộng P1 "một ảnh chụp" của vòng 2 codex)

Bốn khẳng định của các lượt trước, tôi TỰ ĐO LẠI trên cây hiện tại — không nhận lời khai:

| finding lượt trước | phân loại | bằng chứng TỰ ĐO |
|---|---|---|
| `r3873588649` tìm gốc dự án | ĐÃ VÁ THẬT | `_goc_du_an()` mới, neo theo `Path(__file__).resolve().parents[2]` khớp launcher; mutant `goc_mac_dinh_theo_cwd` (đổi về `Path(ghi_de or ".").resolve()`) → `GIET THAT` qua `t13`, đo trực tiếp bằng `python3 mcp_github_doc_test.py --dot-bien` |
| `r3873588657` headers falsy | ĐÃ VÁ THẬT | `"headers" in muc` thay `or`; mutant `mcp_bo_kiem_kieu_headers` trong `launcher_test.py` (đổi `isinstance` check thành `if False`) → chạy trên bản sao ĐẦY ĐỦ (`.claude/dev` copy nguyên, không chỉ 4 tệp) → `t115` ĐỎ đúng dòng `headers falsy co mat khong bi tu choi` |
| `r3873588663` SSE nhiều dòng | ĐÃ VÁ THẬT | `_boc` viết lại buffer theo event/blank-line; mutant `sse_parse_tung_data` (lùi về nối `data:` từng dòng rời) → `GIET THAT` qua `t14`, đo trực tiếp |
| P1 vòng 2 "một ảnh chụp" (ABA đánh bại băm) | ĐÃ VÁ THẬT | Kiến trúc đổi: `_doc_mcp_json(kem_headers=True)` — MỘT lời gọi trả cả URL+headers. Mutant `goi_parser_hai_lan_ghep_hai_anh` (khôi phục HAI lời gọi tách rời) → `GIET THAT` qua `t16`, kịch bản A→B→A THẬT (ghi đè `.mcp.json` giữa chừng), đo trực tiếp |

Cả 4 đều ĐÃ VÁ THẬT, không phải VÁ HỜ — số đo là `GIET THAT`/`tin_dung_gia`/`song_sot` từ chính
runner phân loại lại của gói này (xem BẢNG ĐO), không phải chỉ đọc `rc=0`.

## BẢNG ĐO

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Chỉ chạm đúng `write_set` 4 tệp | 4 tệp | `git diff --numstat 693d68fd 73c91cb2` → đúng 4 tệp: `launcher.py` `launcher_test.py` `mcp_github_doc.py` `mcp_github_doc_test.py`, không tệp nào khác | khớp |
| Kích thước trong trần | ≤6 tệp/≤1000 dòng | 4 tệp; numstat riêng `mcp_github_doc*.py` (đơn vị ngân sách ghi trong lease) = 37+32+194+22 = 285 | khớp, dưới trần |
| `launcher_test.py`: 154/154 qua | N/N | `python3 launcher_test.py` trên sandbox → `154/154 ca DA CHAY QUA (tong 155, bo qua 1, hong 0)`; ca bị bỏ (`t62`) tự khai là fixture Windows-only, bản POSIX là `t63` (chạy được, không bỏ) | khớp |
| `mcp_github_doc_test.py`: N/N qua | N/N | `python3 mcp_github_doc_test.py` → `17/17 ca QUA (hong 0, bo qua 0)` | khớp |
| Mutant battery `mcp_github_doc.py` | "đủ răng" (khai gián tiếp qua đổi runner phân loại `giet_that/tin_dung_gia/song_sot`) | `python3 mcp_github_doc_test.py --dot-bien` → `GIET THAT (19)`, `TIN DUNG GIA (0)`, `SONG SOT (0)` — 19/19 | khớp, và đây là số THẬT không phải rc=0 |
| `doctor` giữ hợp đồng 4 giá trị cũ | "không hồi quy" | `python3 launcher.py doctor` trên sandbox chạy sạch, có dòng `mcp-endpoint=OK`, `KET LUAN: DU CONG CU BAT BUOC` | khớp |
| Arity đổi theo `kem_headers` đúng ở MỌI nhánh | 4 phần tử khi tắt, 5 khi bật | Tự viết probe gọi trực tiếp `_doc_mcp_json` trên **11 cấu hình** phủ **8 đường return** (thiếu tệp · JSON hỏng · gốc không phải object · thiếu khoá · `srv` không phải object · tên rỗng · tên trùng 2 · giá trị không object · thành công không headers · headers=None · headers hợp lệ) × 2 chế độ `kem_headers` → **22/22 đúng độ dài khai báo** | khớp — xem finding P2 bên dưới về PHẠM VI bảo vệ của khẳng định này |
| Không tệp nào khác đọc `/.mcp.json` hoặc ghép hai ảnh | ngụ ý (kiến trúc "một nguồn sự thật") | `grep -rn '\.mcp\.json'` toàn kho: chỉ `launcher.py` (đọc + đo) và `mcp_github_doc.py` (gọi launcher); `scripts/tl_core/release.py` chỉ liệt kê tên tệp để LOẠI khỏi manifest, không parse | khớp |
| Không chuỗi bỏ-qua-CI nguyên văn | ngụ ý (§ Bài học đắt giá) | `git diff` + `git log --format=%B` trên 3 commit: không khớp | khớp |

## P2 — `sensitive`: một trong 8 nhánh return-sớm của `_doc_mcp_json` KHÔNG có mutant nào bắt được ở CẢ HAI bộ test, vi phạm điều kiện lease (3)

TỆP/DÒNG: `.claude/dev/launcher.py:2882-2885` (nhánh JSON parse lỗi, `except (OSError, ValueError) as
e: return (..., None, None) + rong`).

VẤN ĐỀ: Lease `canh_bao_cho_nguoi_thi_hanh (3)` đòi *"Mỗi chốt phải có ĐỘT BIẾN RIÊNG làm ca đích
ĐỎ; chốt không có mutant là chốt sẽ hở lại."* Chốt mới ở đây là bất biến "MỌI đường `return` của
`_doc_mcp_json` phải nối `+ rong` khi `kem_headers=True`, nếu không caller 5-biến ở
`mcp_github_doc.py` ném `ValueError` không được bắt (chỉ `except OSError` bọc ngoài, không bắt
`ValueError`)". Tôi đã kiểm THẬT (không đọc mã suông) 8 nhánh:
- 7/8 nhánh CÓ bảo vệ — nhưng bảo vệ đó là TÌNH CỜ, tới từ các test cấu hình lỗi có sẵn của
  `mcp_github_doc_test.py` (`t01` phủ "thiếu tệp"/"gốc là mảng"/"tên không khớp"/"giá trị không
  object"/"thiếu khoá"; `t10` phủ "srv không phải object"; `t11` phủ "tên trùng 2") — KHÔNG phải từ
  một mutant thiết kế riêng cho bất biến arity.
- **1/8 nhánh (`json_hong` — JSON parse lỗi) KHÔNG được test nào chạm tới ở CẢ HAI tệp test.**

ĐÃ THỬ NGHIỆM (mutant trên bản sao ngoài cây, KHÔNG đụng sandbox review):
```
D=.../scratchpad/review362/mutant_json   # cp -r .claude/dev/. đầy đủ, không chỉ 4 tệp
# xoá "+ rong" khỏi đúng nhánh json_hong trong launcher.py
python3 launcher_test.py --lap-ca t115_... --lan 1        # => 1/1 QUA (khong bat duoc)
python3 mcp_github_doc_test.py                             # => 17/17 QUA (khong bat duoc)
```
Cả hai bộ test đều XANH với mutant này. Bằng chứng hậu quả thật (không phải suy diễn):
```python
doc._doc_cau_hinh(Path(td))   # .mcp.json chứa "{ nay khong phai json hop le"
# => VALUEERROR KHONG DUOC BAT: not enough values to unpack (expected 5, got 4)
```
Đây đúng lớp lỗi packet này sinh ra để triệt — không phải "hai ảnh chụp" nữa, mà là "arity trôi ở
MỘT trong tám nhánh gần-giống-hệt-nhau", và một sửa vô hại kiểu "gọn hoá 8 dòng lặp bằng helper" ở
lượt sau rất dễ bỏ sót đúng nhánh không ai đo.

ĐÃ THỬ VÁ: không (đúng vai trò reviewer, không sửa cây).

ĐỘ TIN: cao — có phản chứng chạy được hai chiều (mutant đỏ về mặt LÝ THUYẾT nếu đo đúng chỗ; đo
bằng CẢ HAI bộ test hiện có thì XANH; và có bằng chứng hậu quả runtime thật).

ĐỀ XUẤT (không phải patch-as-hint, chỉ mô tả hướng — mô tả bằng lời theo đúng giới hạn "packet
`sensitive`" của §8 cho `launcher.py`): thêm một ca kiểu `t115` gọi
`m._doc_mcp_json(td, kem_headers=True)` sau khi ghi `.mcp.json` với nội dung JSON không hợp lệ
(vd `"{ khong hop le"`), khẳng định `len(kq) == 5 and kq[4] is None`; thêm mutant tương ứng xoá
`+ rong` ở đúng dòng 2885. Đây là nợ CÓ TÊN — không chặn land theo luật "chỉ P1 chặn", nhưng phải
được khai trong handoff/land, không được im lặng bỏ qua.

## P3 (ghi nợ, không chặn) — `except OSError` bọc ngoài lời gọi `_doc_mcp_json` trong `mcp_github_doc.py` có vẻ là code chết

TỆP/DÒNG: `.claude/dev/mcp_github_doc.py:57-62`.

VẤN ĐỀ: `_doc_mcp_json` đã tự bắt `(OSError, ValueError)` nội bộ quanh `tep.read_text(...)` và
`tep.is_file()` (theo tài liệu Python) không truyền `OSError` ra ngoài — nên `except OSError:` ở
`_doc_cau_hinh` dường như không còn đường nào kích hoạt được trong mã THẬT (không mutant).

ĐÃ THỬ NGHIỆM: xoá hẳn khối `try/except OSError` trên bản sao ngoài cây
(`.../mutant_oserror`) → `python3 mcp_github_doc_test.py` vẫn `17/17 QUA`, và
`python3 mcp_github_doc_test.py --dot-bien` vẫn 17/17 (2/19 mutant khác mất ANCHOR text vì trùng
đoạn vừa xoá — nhiễu của chính thao tác review, không phải lỗi dự án, không tính vào kết luận).

ĐỘ TIN: vừa — tôi không REVIEW được toàn bộ đường gọi `_doc_mcp_json` để loại trừ 100% một lối vào
OSError nào đó tôi chưa nghĩ ra; đây là quan sát "có vẻ chết", không phải khẳng định tuyệt đối.
Không chặn land — nếu đúng là code chết thì vô hại (fail-safe thừa), chỉ đáng dọn ở packet khác.

## Trục 3 — `launcher.py`/`launcher_test.py`

- `doctor` chạy sạch trên sandbox, `mcp-endpoint=OK`, không hồi quy quan sát được so với hợp đồng
  4-giá-trị cũ (đo bằng cách GỌI THẬT, không đọc chú thích — đúng bài học của kho).
- `t117` (mỗi mẫu `DOT_BIEN` phải khớp ĐÚNG MỘT chỗ trong `launcher.py`) chạy trong suite đầy đủ,
  không nằm trong danh sách hỏng (154/154 qua) — tệp nóng không mất tính duy nhất mẫu đột biến.
- 17 dòng test mới cho hàm 8-đường × 2-chế-độ: ĐỦ về mặt "không crash", KHÔNG ĐỦ về mặt "mỗi
  đường có mutant riêng" — xem P2 ở trên. Không đếm dòng để kết luận, đã đo bằng đột biến.
- `launcher_test.py` là bộ phụ thuộc NỀN (Linux bỏ qua 1 ca `t62`, đúng như tài liệu kho khai; đo
  trên container Linux của phiên này nên KHÔNG xác nhận được số liệu Windows — ghi
  `KHÔNG ĐO ĐƯỢC` cho nhánh Windows, không suy diễn từ số liệu CI cũ).

## Trục 4 — nghi vấn "có MẶT mà không có ĐO" trong 194 dòng test mới

Xét riêng bốn ca mới (`t13` `t15` `t16` `t17`): không ca nào có nhánh "không tìm thấy thì thoát êm,
vẫn tính ĐẠT" kiểu `t24`. Ca `t17` (khoá `Path.read_bytes` để ép `OSError`) LÚC ĐẦU tôi ngờ là ca
"không đo gì" vì mã thật không gọi `read_bytes` ở đường đó — nhưng mutant tương ứng
(`doc_he_tep_sau_phan_tich`) tiêm một lời gọi `.read_bytes()` giả vào ĐÚNG vị trí rồi đo `t17` có
bắt được không, và `--dot-bien` xác nhận `GIET THAT`. Đây là ca đo "không có lần đọc tệp THỨ HAI
nào len vào sau khi đã phân tích", tức đúng lớp phòng ngừa hồi quy "hai ảnh chụp" — không phải ca
rỗng. Rút lại nghi vấn ban đầu sau khi đo, không giữ nguyên phỏng đoán.

## Trục 1 — kết luận về câu hỏi kiến trúc (đổi arity theo cờ có đáng hay không)

Có bằng chứng cho CẢ hai phía, không có câu trả lời sạch:
- Đáng: đổi arity dồn TOÀN BỘ tri thức "URL/headers phải cùng một lần đọc" vào MỘT hàm, MỘT lần gọi
  — số nơi có thể lệch giảm từ "hai lệnh gọi trong `mcp_github_doc.py`" xuống "một cấu trúc
  return trong `launcher.py`", và cấu trúc ấy được `t115`+`t16` đo trực tiếp.
- Không đáng hoàn toàn: nó THẬT SỰ dời lớp lỗi từ "hai lần đọc" (dễ thấy, một P1 rõ ràng vòng 2 đã
  bắt) sang "8 điểm gần-giống-hệt-nhau phải đồng bộ tay" (khó thấy hơn — P2 ở trên chứng minh đúng
  một trong tám đã trôi khỏi vùng phủ test dù CHƯA trôi khỏi mã).

Không có cách nào đóng khung này bằng một câu "đáng/không đáng" chắc chắn từ dữ liệu hiện có — cả
hai lớp lỗi đều có phản chứng thật trong cùng packet. Ghi lại làm nợ nhận thức cho packet sau nếu
`_doc_mcp_json` còn phình thêm nhánh return.

## KHÔNG ĐO ĐƯỢC

- Hành vi trên Windows của `launcher_test.py` (bỏ qua bao nhiêu ca) — container review chỉ có
  Linux; không suy diễn từ số liệu CI cũ trong tài liệu vì đó là số của lượt CHẠY KHÁC.
- Trạng thái GitHub trực tiếp của PR #362 (check runs, mergeable_state) — sandbox không có đường ra
  mạng cho REST/`gh`; không kiểm chứng được từ đây, đăng verdict qua MCP/`gh` (xem dưới) là nơi có
  thẩm quyền, không phải suy luận trong sandbox.

## Kết luận

`changes_requested`, nhưng CHỈ vì một P2 (nợ có tên, không chặn land theo luật "chỉ P1 chặn").
Ba P2 cũ và P1 vòng 2 đều ĐÃ VÁ THẬT có phản chứng. Nếu chủ kho quyết định land: ghi P2
`json-hong-thieu-mutant-arity` thành nợ tường minh trong handoff/land record, không âm thầm đóng.
