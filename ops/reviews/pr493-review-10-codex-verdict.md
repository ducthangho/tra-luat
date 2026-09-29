verdict: changes_requested
reviewed_sha: 9e78e19e5e3247d910c061a1171f4783ee0a3e10

**KHÔNG CÒN P1 · KHÔNG CÒN P2 trong phạm vi review · CÒN 3 P3. Điều kiện “tới hết P3” CHƯA ĐẠT.**

Reviewer: Codex/GPT-6 theo cấu hình phiên, provider `openai_codex`, execution surface agent API có shell cục bộ, transport `machine`. Phiên độc lập với executor Claude theo hồ sơ được giao; không có chứng thực độc lập backend/model thực phục vụ. Review khác nền theo §8 và chỉ thị trực tiếp lượt 10; không tự ghi state `cross_approved`, không cấp quyền merge. Hai trục đã xét: yêu cầu/phạm vi và tính đúng/nhất quán của hồ sơ cùng các cổng liên quan.

Exact tree: `69bd8742c5598bb6a6d27574b7cc7ec41a7745c5`. Base: `c00c88a02a29c057b0c59806760c35968e408dc4`. `cay-kho/` detached, full history, sạch trước và sau đo; giữ read-only. Cổng chạy trên `review10-current/`; đột biến trên `review10-mutant/`; tái dựng merge trên `review10-state/`. Tất cả nằm trong workspace, không mạng, không tự soạn payload đường dẫn. TMPDIR đặt trong workspace; thư mục actionlint 1.7.7 được thêm cuối PATH; ghim `core.abbrev=7` cho các phép chạy cổng.

Bằng chứng tự chạy lượt này: [measurements.json](review10-evidence/measurements.json), [gates.json](review10-evidence/gates.json), [probes.json](review10-evidence/probes.json), [extra.json](review10-evidence/extra.json), [final-checks.json](review10-evidence/final-checks.json). Script tái lập và stdout `.out` cùng thư mục. Không dùng kết quả chạy lượt trước thay kết quả lượt này. Dòng `muc-r360.md` cộng **287** là dòng CHANGELOG của exact head.

## ĐỐI CHIẾU LƯỢT TRƯỚC

- `cong-byte-co-rang-cong-claims-khong-dem-su-that`: **CHƯA VÁ** — tự chạy ba mutant riêng: `1016→1017` ở heading r358, `5→6` ở heading r360, `13 − 2 = 11→12` trong phép trừ. Mỗi ca thay đúng một byte, giữ **878940 byte** CHANGELOG; cả ba claims `rc=0, ok=true`. Release trên mutant đầu `rc=2`, failed chỉ CHANGELOG, `package_hash_match=false`. Mã claims không đổi từ `dd4a3ae`; nhận nợ không đóng hành vi.
- `phat-hien-them-da-co-trong-verdict-bay`: **VÁ HỜ** — bảng đã vá thật A2/A6/C3 thành “có”, B4 thành “không, không phải lỗi”; đếm **13 = 12 + 1**, đúng với địa chỉ verdict 7. Nhưng **heading hiện hành** `muc-r360.md:333` vẫn khai “13 vị trí, **4 tự tìm, 2 đứng vững**”; câu:371 tiếp tục dùng “bốn cái tự tìm ấy”. Heading không được gắn nhãn lời khai cũ đã rút, trái bảng và kết luận hiện hành:367–369,407–409. Giữ slug cũ cho phần sót, không đếm các ô đã sửa thành lỗi nữa.
- `bang-ba-luot-van-bi-goi-la-loi-da-va`: **ĐÃ VÁ THẬT** — `muc-r360.md:241–248` nay nói rõ nối dài bảng là mở rộng tóm tắt, không phải sửa lỗi; B4:361 và:376–378 đồng thuận. Bảng có chín hàng, SHA/verdict/bộ ba P1/P2/P3 đều khớp chín verdict. Những chữ “cùng LỚP”, “được vá cùng lớp” trong đoạn này là trích lời cũ để bác; không còn kết tội B4 hiện hành.
- `merge-khai-257-canh-bao-thuc-te-258`: **ĐÃ VÁ THẬT** — đính chính:386–394 neo đích danh **dd4a3ae**. Hai cách đếm cấu trúc độc lập cùng ra **258/103**; master `0721811` có **249/101**, cha thứ nhất `9349bb0` có **256/102**. Tập hàng xác nhận `249+9=258` và `256+2=258`, không mất hàng. Số hiện hành được đo riêng là **264/107**; không dùng nó bác số lịch sử đã ghim mốc. Message cũ vẫn có 257 nhưng đã được đính chính có neo.
- `luot-tam-khong-phai-lan-dau-va-ho-bang-khong`: **ĐÃ VÁ THẬT** — `muc-r360.md:268–277` và message `cc21507`:47–58 rút kết luận “lần đầu” và suy nhân quả từ chỉ số này. Tự đọc `VERDICT-LUOT-5.md:36`: **3 ĐÃ VÁ THẬT · 0 VÁ HỜ · 1 VÁ SINH LỖI MỚI · 13 CHƯA VÁ**; lượt 8 cũng 0 VÁ HỜ. Sai số phạm vi của chuỗi chín số mới được chấm riêng dưới đây, không phải tái mở câu “lần đầu”.

Tổng: **3 ĐÃ VÁ THẬT · 1 VÁ HỜ · 0 VÁ SINH LỖI MỚI · 1 CHƯA VÁ**. Có thêm **1 P3 mới** về tên đại lượng của chuỗi chín số.

## VÉT CÂU KHAI CÔNG VÀ KIỂM LẦN MERGE

**Chưa thể xác nhận “bỏ hẳn mọi câu khai công”.** Đã đọc ba hiện vật, vét cả đoạn sau chuẩn hoá khoảng trắng (`re.sub(r"\s+", " ", ...)`), không chỉ grep một dòng. Heading “quy về LỚP, rồi quét hết lớp — 13 vị trí, 4 tự tìm, 2 đứng vững” vẫn quảng bá phép phân hoạch cũ như tóm tắt hiện hành. Đây là phần sót có thể chỉ ra, thuộc finding inventory bên dưới. Bảng và kết luận đã đúng không tự sửa heading.

Trong `thong-diep-commit.txt`, các câu “Đó là bằng chứng cho cách vá theo lớp”, “tìm thêm được 2 lỗi thật” của **9349bb0**, và “8→12” của **025c6b2** vẫn còn nguyên byte. Chúng là thông điệp lịch sử đã được đoạn mới rút lại; không yêu cầu viết lại Git để xoá chúng, và không chấm thêm finding chỉ vì vẫn tìm thấy chuỗi chữ cũ. Message **cc21507** mới rút suy nhân quả nhưng có lỗi nhãn chuỗi số nêu dưới.

Câu “nhờ đó” trong thân PR:109 nói về sự kiện kích hoạt CI, không quy công cho vá theo lớp. Câu “sau khi cách vá đổi…” ở r360:285–286 nói về lượt 2→3 và việc vét bản chiếu. Câu r360:422–424 vẫn giữ **tiền lệ vá gốc lượt 5→6, bỏ bộ lọc đóng 11 finding**: không coi đó là bằng chứng cho phương pháp bắt đầu sau lượt 7. `VERDICT-LUOT-6.md:31` xác nhận riêng cả 11 slug cũ không thiếu input và việc bỏ lọc đóng chúng; phần đối chiếu của verdict đó liệt kê đủ 11. Đây là kết quả cụ thể có nguồn, khác suy ưu thế tổng quát từ xu hướng chín lượt. Không nâng riêng câu này thành P3 khi nguồn được giao hỗ trợ nó; cũng không nói rằng hiện vật đã bỏ mọi nhận xét về hiệu quả vá gốc.

**Chuỗi chín số khớp P3, không khớp tổng finding.** Đếm heading finding, không lấy con số ở lời mở đầu làm đáp án:

| lượt | SHA | verdict | P1 | P2 | P3 | tổng finding |
|---|---|---|---:|---:|---:|---:|
| 1 | 4af7e29 | changes_requested | 1 | 4 | 12 | **17** |
| 2 | 9484970 | changes_requested | 1 | 4 | 15 | **20** |
| 3 | fae2fb7 | changes_requested | 0 | 2 | 15 | **17** |
| 4 | b004da9 | changes_requested | 0 | 1 | 15 | **16** |
| 5 | f5098dd | approve | 0 | 0 | 14 | 14 |
| 6 | 2c57e99 | changes_requested | 0 | 0 | 10 | 10 |
| 7 | a4bc01d | changes_requested | 0 | 0 | 9 | 9 |
| 8 | 025c6b2 | changes_requested | 0 | 0 | 10 | 10 |
| 9 | dd4a3ae | changes_requested | 0 | 0 | 5 | 5 |

Bảng r360 chép đúng cả chín bộ ba. Câu tóm tắt mới lại bỏ nhãn **P3**, nên 12→15→15→15→14→10→9→10→5 không phải tổng số finding mà câu ấy gọi tên. Nhãn “tương quan, không nhân quả” không giải quyết sai phạm vi đại lượng.

**Inventory A1–C3:** đối chiếu địa chỉ trên **blob a4bc01d**, không lấy dòng đã trôi của head mới. Đơn vị là mệnh đề tại vị trí, không phải slug; B1 và C3 có thể cùng dòng mà vẫn là hai vị trí mệnh đề khác nhau.

| ID | địa chỉ lượt 7 đối chiếu | cột mới | kết quả |
|---|---|---|---|
| A1 | CHANGELOG:16–19, finding va chạm | có | Khớp |
| A2 | câu:173 trong vùng:168–179, finding nợ cổng | có | Khớp |
| A3 | khối printf:278–284 | có | Khớp |
| A4 | endpoint:294–296 | có | Khớp |
| A5 | nháp:139–146 | có | Khớp |
| A6 | nhãn:298 trong vùng:298–303 của finding nháp và printf | có | Khớp |
| B1 | thân PR:13, chỉ dẫn “dưới” | có | Khớp |
| B2 | thân PR:92–100, bảng cổng | có | Khớp |
| B3 | docstring bộ trích:6–11 | có | Khớp |
| B4 | bảng cũ:211–219; không có địa chỉ finding, verdict gọi tóm tắt chọn lọc | không; không phải lỗi | Khớp |
| C1 | CHANGELOG:14, nằm trong trường:14,28–31 | có | Khớp |
| C2 | CHANGELOG:28, cùng trường trên | có | Khớp |
| C3 | thân PR:13, địa chỉ finding B1 bao phủ nhưng chấm mệnh đề khác | có; chưa chứng minh lỗi C | Khớp |

Đếm 13 ID duy nhất: A=6, B=4, C=3; hàng D không có ID không cộng vào 13. **12 có + 1 không = 13**. Phần còn lại B4 không phải lỗi; **0 lỗi được chứng minh nằm ngoài địa chỉ** theo inventory. Bao phủ địa chỉ không chứng minh reviewer đã phát hiện đúng khuyết tật A2/A6/C3. Với thân PR và script ngoài Git, **KHÔNG ĐO ĐƯỢC nguyên byte bản cũ** chỉ từ kho; phép nối dựa trên địa chỉ/lời trích trong verdict được giao. A2/A6 có đối chứng blob Git nguyên byte.

**Tách bản vá và merge:** `dd4a3ae→cc21507` chỉ đổi CHANGELOG và manifest, **2 tệp +63/−29**. `cc21507→9e78e19` nhập master, **11 tệp +1167/−5**, gồm r363 và tám tệp verdict/receipt pr492. Không quy các hiện vật master thành sản phẩm riêng của bản vá. Master thêm **4 commit** từ 0721811; first-parent `c00c88a..HEAD` có **16 commit**, ghi đầy đủ trong measurements.json. Toàn PR so base mới: **8 tệp +1622/−26**, khớp awk và Git.

**Năm con số merge đều khớp:** r giảm dần `363→361→360→359→358→356`; **0** số r trùng; **264** hàng cảnh báo; **107** hàng mục lục; **0** hàng nguyên văn trùng ở **mỗi** bảng. Kiểm thêm khóa `(verdict_path, caveat_id)` cho cảnh báo và verdict_path cho mục lục: đều 0 trùng. Hai bộ đếm độc lập: một đi từ dòng phân cách tới hết khối hàng; một lấy khối bảng trong section tương ứng.

| mốc | cảnh báo | mục lục | trùng hàng cảnh báo/mục lục |
|---|---:|---:|---:|
| 9349bb0 | 256 | 102 | 0/0 |
| master 0721811 | 249 | 101 | 0/0 |
| dd4a3ae | **258** | 103 | 0/0 |
| cc21507, trước merge thứ ba | 258 | 103 | 0/0 |
| master c00c88a | 255 | 105 | 0/0 |
| 9e78e19 | **264** | **107** | **0/0** |

Hai phép cộng hiện hành: **255+9=264**, **258+6=264**; mục lục **105+2=107**, **103+4=107**. Mọi hàng master có mặt nguyên byte trên head. Đối chiếu toàn CHANGELOG theo heading: **r363, r361, r359 và mọi mục sau r358 khớp master nguyên byte**; r358 chỉ mang bản vá chủ ý của PR. Tám tệp pr492 mới của master cũng khớp nguyên byte. README so master chỉ thêm hàng của nhánh, không mất nội dung master. Không thấy hàng/mục r363 bị nuốt.

Lệnh literal `git diff origin/master HEAD -- ...` **KHÔNG ĐO ĐƯỢC** vì gói không có ref `origin/master` (`rev-parse --verify` rc128). Dùng OID đóng băng **c00c88a** thay thế, không tạo ref giả hoặc gọi mạng. Diff kiểm tra lưu ở [readme-vs-master.patch](review10-evidence/readme-vs-master.patch) và [changelog-vs-master.patch](review10-evidence/changelog-vs-master.patch).

**Tái hiện xung đột thật trên bản sao:** checkout cc21507, `git merge --no-commit --no-ff c00c88a` ⇒ rc1; chỉ `RELEASE_MANIFEST.json` unmerged, CHANGELOG và README auto-merge. Điền manifest đúng từ reviewed commit và stage ⇒ `git write-tree` bằng exact reviewed tree. Chạy riêng `release-manifest --deterministic --out ...` trên bản sao đã khôi phục ⇒ rc0, output **byte-exact** manifest. Xác minh được nội dung kết quả tái sinh, không chứng thực transcript thao tác tay của executor.

**Cổng biên nhận, hai chiều và đảo lại:** trên cây merge đã giải, HEAD=cc21507, MERGE_HEAD=c00c88a: df7ec13 không là tổ tiên HEAD (rc1), là tổ tiên MERGE_HEAD và 9e78e19 (rc0/0). Cổng trả **rc1, 4 vi phạm**, đúng bốn receipt pr492, 50 đạt v2/tổng107. Chỉ chuyển HEAD sang reviewed merge commit, bỏ MERGE_HEAD: **rc0, 0 vi phạm**, 54 đạt v2/tổng107. Đảo HEAD/MERGE_HEAD lại ⇒ **rc1, đúng 4 vi phạm**. Băm tập tệp trước/sau bằng nhau; index có đúng reviewed tree. Đây là tái dựng cơ chế, không phải log gốc của phiên executor.

**Có nên gọi là khuyết tật cổng?** Việc lặp lại xác nhận một **giới hạn áp dụng có thể gây nhầm khi kiểm cây chưa commit**: cổng đọc receipt từ working tree nhưng đo reachability từ HEAD (`ops/bien_nhan_v2.py:809–822`). Không nên chỉ ghi “tạo tác” rồi coi nó không cần giải thích. Tuy nhiên, cây tệp tự nó không có tổ tiên; ancestry là thuộc tính đồ thị commit. Hợp đồng hiện hành chủ ý xét HEAD, thông báo đỏ nói chính xác “không phải tổ tiên của HEAD”, và cả ba trạng thái tái dựng đều tuân thủ hợp đồng ấy. Chưa có bằng chứng cổng hứa validate ancestry của prospective merge hoặc xanh sai trên exact reviewed commit. Vì vậy **không thêm P3 chỉ do hiện tượng lặp lại**.

Nếu cần dùng cổng trước commit, hướng cải thiện là nhận một commit ứng viên rõ ràng hoặc báo trạng thái chưa đo được cho pha ấy, thay vì tự coi HEAD cũ là snapshot đang xét. Ca kiểm phải phân biệt commit ứng viên chứa đủ hai cha với cây chỉ chép byte mà không giữ ancestry; không sửa bằng cách nhận mọi object “có trên đĩa” hoặc OR mù với MERGE_HEAD. “Phải commit rồi mới đo” được hiểu hẹp là cần một **commit ứng viên có đồ thị đúng**, có thể là commit tạm cục bộ; không phải yêu cầu publish hoặc commit vào kho thật trước review.

## BẢNG ĐO

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Head/tree | 9e78e19 | SHA đầy đủ và tree69bd8742… đúng | Có |
| Base mới đã nhập | c00c88a; master thêm4 commit | ancestry rc0; rev-list=4 | Có |
| First-parent | chuỗi PR và các lần vá/merge | 16 commit; mới nhất9e78e19,cc21507 | Có |
| Delta so base mới | numstat/diff c00c88a | **8 tệp +1622/−26** | Có |
| Hai patch, numstat, message | trích Git | **4/4 byte-exact** | Có |
| Năm slice CHANGELOG | cắt heading thật | **5/5 byte-exact**, heading tại1/102/288/792/912 | Có |
| Bốn bản chiếu receipt/README/land | chép cây | **4/4 byte-exact** | Có |
| ARTIFACTS.sha256 | toàn vẹn gói | **3298/3298**, không sai băm | Có; không xác thực provenance GitHub |
| Ref snapshot | 322/322/322, lệch0 | ba tập tên+OID bằng nhau; live refs/heads cục bộ cũng khớp | Có cục bộ; máy chủ hiện tại KHÔNG ĐO ĐƯỢC |
| Bộ trích | 11 input,2687 dòng | **2687** dòng không rỗng,**1710** có số; tái chạy byte-exact | Có trong tập input |
| Bảng chín verdict | SHA/verdict/P1/P2/P3 | 9/9 khớp, xem bảng trên | Có |
| Chuỗi “finding” | 12,15,15,15,14,10,9,10,5 | khớp P3; tổng là17,20,17,16,14,10,9,10,5 | **Không đúng phạm vi gọi tên** |
| Inventory | 13 ID,12/1,0 lỗi ngoài địa chỉ | 13 ID duy nhất;12/1;B4 không phải lỗi | Có bảng/kết luận |
| Heading inventory | 13 vị trí,4 tự tìm,2 đứng vững | bảng đã rút4/2; còn1 địa chỉ không được nêu và0 lỗi ngoài địa chỉ | **Không** |
| Lượt8 lần đầu VÁ HỜ=0 | đã rút | verdict5:36 đã ghi0 | Có đính chính |
| Đính chính dd4a3ae | 258=249+9=256+2 | hai bộ đếm và tập hàng khớp | Có |
| Thứ tự r | 363→361→360→359→358→356 | đúng; toàn bộ dãy dev-side giảm dần | Có |
| Số r trùng | 0 | 0 | Có |
| Cảnh báo head | 264 | 264 | Có |
| Mục lục head | 107 | 107 | Có |
| Trùng nguyên hàng | 0 ở cả hai bảng | 0/0; trùng khóa cũng0/0 | Có |
| Bảo toàn master | giữ nội dung | đủ255/105 hàng; r363 nguyên byte;8 tệp pr492 nguyên byte | Có |
| Xung đột lần3 | chỉ manifest;hai tệp auto-merge | tái merge rc1, unmerged chỉ manifest | Có |
| Tái sinh manifest | đúng kết quả sau merge | release-manifest rc0, byte-exact | Có kết quả; thao tác lịch sử KHÔNG ĐO ĐƯỢC |
| ls-tree reviews/land | có491,không493 | có2verdict+2receipt491,land491;khôngpr493-review-* | Có; danh sách trong ls-tree.txt |
| Hai verdict491 | 35088/36958 byte, băm receipt | byte và hai băm khớp | Có |
| `python3 -B ops/bien_nhan_v2.py` | 0 vi phạm sau commit | **rc0;54v2+11legacy+42nợ=107;0 vi phạm;0 KHÔNG ĐO ĐƯỢC** | Có |
| Cổng trước commit | 4 vi phạm pr492/df7ec13 | rc1;50v2,tổng107;đúng4;đảo lại cũng4 | Có cơ chế |
| `python3 -B ops/lease_publish_test.py` | 146/146 ởcc21507 | **rc0;146/146;chạy146,bỏ0** trên head mới | Có số; đo head mới riêng |
| Catalog A0 trong lease | nội dung master | mẫu số37;giết34;SỐNG có chủ đích3;tín dụng giả0 | Khớp output suite |
| `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | xanh | **rc0;ok=true;180/180**,haihash_match=true,failed/extra/errors=[] | Có |
| `python3 scripts/tl.py doc-claims-check --strict --json` | xanh | **rc0;ok=true**,0vi phạm các lớp đang kiểm | Có trong phạm vi cổng |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | rc0 | **rc0;7tệp,0chép doctrine** | Có |
| `python3 .claude/dev/packet_loop.py adr-song --root .` | rc0 | **rc0;46ADR/46hàng,khớp1–1** | Có;ngoại lệ trạng thái0016 được output nêu |
| Ba mutant số | nợ vẫn mở | **3/3 claims rc0,ok=true**,mỗi ca1byte | Có;P3 còn |
| Release mutant | chặn byte sai | rc2;failed chỉCHANGELOG;size vẫn878940 | Có |
| Runtime/CI/approval/đọc ngược PR lịch sử | thuật lại và có nhãn giới hạn | thiếu log/raw response;không mạng | **KHÔNG ĐO ĐƯỢC độc lập** |
| Full-gate thân PR | ghim a4bc01d | không đem121/121 và49/102 ấy gán cho9e78e19 | Đúng phạm vi snapshot;không chạy lại lịch sử |

Không chạy lại full selftest sản phẩm hoặc CI từ xa: delta PR so base mới chỉ tám tệp hồ sơ, không đổi mã sản phẩm; sáu cổng được yêu cầu đã chạy đủ. Không coi những phép không chạy này là pass.

### cong-byte-co-rang-cong-claims-khong-dem-su-that  [P3]  Ba mệnh đề sai số vẫn qua cổng claims
LỚP: D
TỆP/DÒNG: CHANGELOG.md:480–493,723–729; scripts/tl_core/workflow.py:1163,1430,1488.
VẤN ĐỀ: Tiêu chí đóng nợ vẫn chưa đạt: ba đột biến làm mệnh đề hiện hành sai nhưng claims vẫn xanh. Đây là nợ đã có, không phải hồi quy của merge hoặc lỗi mã mới do PR hồ sơ gây ra. Chỉ thị “tới hết P3” yêu cầu giữ mở nó; ghi đúng nợ/ngoài write set không thay thế sửa hành vi.
CÙNG LỚP CÒN Ở ĐÂU: receipt-luot1.yaml:74–76; than-pr-493.md:68; thong-diep-commit.txt:64–66; đoạn nợ r360 ở hai địa chỉ trên. Đã vét ba mutant và các bản chiếu liên quan, chưa có bằng chứng đóng.
ĐÃ THỬ VÁ: không sửa sản phẩm; đã thử đột biến trên bản sao và khôi phục. Hướng vá ở `_doc_claims_check`/lớp kiểm định lượng trong scripts/tl_core/workflow.py bằng packet có write set mã phù hợp: đối chiếu mệnh đề có loại và mốc với nguồn Git/verdict hoặc phép tính, không hard-code số mẫu. Đây là nơi ra phán quyết, không vá bằng sửa nhãn trong CHANGELOG. Ca khoá: control xanh, cả ba mutant đỏ; thêm ca trích lời sai lịch sử đã rút không bị kết tội như mệnh đề hiện hành. Nguy cơ là kiểm nhầm trích dẫn, hứa kiểm mọi văn xuôi, hoặc nhầm băm byte với chân trị.
ĐÃ THỬ NGHIỆM: `python3 review10-evidence/probes.py`; cả3claims rc0/ok=true, mỗi ca thay1byte và giữ878940byte; release cađầu rc2,failed chỉCHANGELOG. Cổng xanh nền ghi ở gates.json.
ĐỘ TIN: cao

### phat-hien-them-da-co-trong-verdict-bay  [P3]  Heading vẫn quảng bá 4 tự tìm, 2 đứng vững sau khi bảng đã rút phân hoạch đó
LỚP: B
TỆP/DÒNG: CHANGELOG.md:620,658; muc-r360.md:333,371; đối chứng bảng:350–369 và kết luận:401–415.
VẤN ĐỀ: Bản chiếu rút gọn là heading chưa theo bản sửa. Nó vẫn đặt “4 tự tìm, 2 đứng vững” ngay sau “quy về LỚP, rồi quét hết lớp”, không gắn nhãn lịch sử/đã rút. Cột được định nghĩa là địa chỉ reviewer; bảng mới có12“có” và1“không”, kết luận0lỗi ngoài địa chỉ. Không thể lấy việc hai khuyết tật nằm trong vùng đã dẫn vẫn đáng sửa để giữ nguyên phân hoạch tự tìm4/2 của heading. Câu:371 có nhắc lượt8 nhưng vẫn dùng “bốn cái tự tìm ấy” không đánh dấu danh xưng sai; tối thiểu heading hiện hành chắc chắn còn lỗi. Điều này cũng bác tuyên bố “không còn câu nào ... khai công” ở:417 trong chính mục.
CÙNG LỚP CÒN Ở ĐÂU: heading và câu dẫn nêu trên; BANG_KHANG_DINH chứa bản trích tương ứng, không phải finding riêng. Message9349bb0/025c6b2 còn câu cũ nhưng là lịch sử đã được đính chính, không đòi rewrite. Đã vét thân PR, không thấy bản chiếu mới khác giữ4/2.
ĐÃ THỬ VÁ: không sửa hiện vật được review. Hướng vá rẻ: bỏ4/2 khỏi heading hoặc ghi rõ đó là số cũ bị rút; gọi đoạn:371 là “bốn vị trí từng bị xếp nhầm vào tự tìm”, rồi giữ kết luận12/1 và0ngoàiđịachỉ. Vét cả heading, đoạn dẫn và kết luận theo cùng inventory, vì sửa riêng ô đã tái để sót bản chiếu. Ca khoá: đếm13ID/12có/1không, kiểm không còn4/2 được phát biểu như phân hoạch hiện hành. Nguy cơ: xoá cả trích dẫn lịch sử cần giữ, hoặc đánh đồng “địa chỉ được dẫn” với “khuyết tật đã được reviewer nêu”.
ĐÃ THỬ NGHIỆM: `python3 review10-evidence/measure.py` và `python3 review10-evidence/extra.py`;13ID duy nhất,12/1, đối chiếu trường TỆP/DÒNG verdict7 và blob a4bc01d; đọc heading và vét nối dòng ba hiện vật. Bảng đã đúng; heading vẫn4/2.
ĐỘ TIN: cao

### chuoi-chin-luot-thieu-pham-vi-p3  [P3]  Chuỗi finding mới chỉ đếm P3 nhưng không khai bộ lọc mức độ
LỚP: F
TỆP/DÒNG: CHANGELOG.md:706–707; muc-r360.md:419–420; thong-diep-commit.txt:54–58 (message cc21507).
VẤN ĐỀ: Đại lượng được giới thiệu là “xu hướng finding qua chín lượt”, nhưng bốn số đầu12/15/15/15 chỉ lấy P3, bỏ các P1/P2 thật trong nguồn. Tổng đúng là17/20/17/16; từ lượt5 trở đi mới trùng vì không còn P1/P2. Đây là sai phạm vi tập được đếm của lời khai mới, không phải sai số trong bảng chín bộ ba. Bỏ 13 finding P1/P2 ở bốn điểm đầu làm đường số mang nghĩa khác; nhãn tương quan không nhân quả không sửa được bộ lọc không khai. Có thể giữ nguyên chuỗi nếu gọi đúng **số finding P3**.
CÙNG LỚP CÒN Ở ĐÂU: hai bản chiếu hiện hành r360 và messagecc21507 nêu trên; BANG_KHANG_DINH trích cả hai. Đã vét thân PR, không có chuỗi chín số đó. Bảng bộ ba từng lượt đúng, không chấm nó thành lỗi.
ĐÃ THỬ VÁ: không sửa sản phẩm/hồ sơ. Hướng rẻ: thêm nhãn “P3” tại câu r360 và đính chính có neo cho messagecc21507; hoặc nếu thực sự muốn tổngfinding thì dùng17→20→17→16→14→10→9→10→5. Ca khoá: parse heading `[P1]`/`[P2]`/`[P3]` của9verdict, xác nhận mỗi điểm bằng tổng hoặc bằng P3 theo nhãn được chọn. Nguy cơ: thay số trong bảng vốn đã đúng, suy mức nghiêm trọng từ tổng không trọng số, hoặc dùng đường số đã sửa để khôi phục kết luận nhân quả chưa chứng minh.
ĐÃ THỬ NGHIỆM: `python3 review10-evidence/measure.py` đếm heading cả9verdict; lượt1=1+4+12=17,lượt2=1+4+15=20,lượt3=0+2+15=17,lượt4=0+1+15=16. Bằng chứng đủ trong bảng trên và measurements.json, không dựa vào lời tự khai của executor.
ĐỘ TIN: cao
