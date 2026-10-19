# Đính chính P3 — wp698 r14 (S2, M8) và wp685 r28 (O1…O7)

Packet `no-p3-ho-so` (#750), đặc tả `ops/specs/no-p3-ho-so-r2.md` sha256
`c5e3c45a99a567c36beb9f6e80067dade9afec124b429292d259f04ecea44410` (tìm ở `master` trước, chưa thấy thì nhánh
`claude/spec-no-p3`; thứ định danh đặc tả là băm, không phải tên nhánh). Hai spec gốc, đo tại `6f121a3`:

- `ops/specs/ci-g5-cong-cu-va-tiep-r14.md` · sha256 `ed027f410aac7eeedd60335459ba8cfef521a34730fea68c1255533bb56f1a21` · blob `b427f19d2949c73e2b8088e13999915e8114f186` · commit nguồn `d17ec09088acf674a05638345f7b3ec28ff03c6d`
- `ops/specs/launcher-con-song-esrch-r28.md` · sha256 `8007edf4e00aaefc298bf299bf19be9a71c54e73ff6a1610eb676a806773e156` · blob `fa07ca1bc3707bc273bf25349ffa6f3ca6ad6160` · commit nguồn `4a35f633e1b3f05be12eecf74ab9a8a17ef82c69`

Không sửa hai tệp ấy; đính chính sống ở đây. Cả hai đã đóng băng và có lease neo băm — sửa đè làm băm trong lease trỏ
vào thứ không còn tồn tại. Tệp này không đổi quyết định `landed` nào, không đóng mục `no_con_mo` nào của
`ops/land/pr721-wp698-land-evidence.yaml`, và không mở r15 hay r29.

## S2-r14

Mục nợ 1. Phép liệt kê cùng hình dạng trên blob `6f121a3` (đo 15-10-2026 ~10:40Z): cụm "neo `spec_hash` **của r11**"
có đúng 1 chỗ trong 5.374 dòng của r14, ở dòng 3262; không chỗ nào khác cần đính chính cùng lượt.

tệp: ops/specs/ci-g5-cong-cu-va-tiep-r14.md · sha256 ed027f410aac7eeedd60335459ba8cfef521a34730fea68c1255533bb56f1a21 · dòng 3261–3262

```text
- **S2:** lúc cấp lease, so tập tên+OID ref bị lệch, hoặc `ai-dang-giu ops/cong_cu_test.py` ≠
  `NGƯỜI_GIỮ 0`, hoặc chưa có comment chủ kho xác nhận closure neo `spec_hash` **của r11** (Q10)
```

chữ đúng: … hoặc chưa có comment chủ kho xác nhận closure neo `spec_hash` **của r14** (Q10)

Căn cứ: comment cấp quyền #698 `6091633467` của chủ kho, nguyên văn "Tôi đọc S2 theo depends_on (4): neo spec_hash
của r14" (`ops/land/pr721-wp698-provenance/readback-comment-6091633467.json`, trường `body`). Chữ "r11" là sót từ r11.

## M8-r14

Mục nợ 2. Phép liệt kê trên blob `6f121a3` (đo ~10:40Z): "độ dài mọi danh sách" ở r14 = 1 chỗ (dòng 2731);
"cùng đường, cùng loại" ở r14 = 0 chỗ.

tệp: ops/specs/ci-g5-cong-cu-va-tiep-r14.md · sha256 ed027f410aac7eeedd60335459ba8cfef521a34730fea68c1255533bb56f1a21 · dòng 2729–2731

```text
   - **Giữ răng:** hạng của **từng** dò trong tập đóng 419 trên g2 bằng hạng của cùng dò trên g1 (A10 (ii)); 54 canh vẫn GIẾT
     đúng ca đích (A5); A1–A8 vẫn đạt; (r12) số ô M1/M1b của cửa con `t53` bằng g1 (A10 (iv)); số ô, số kịch bản của năm lưới ở A10 (v)
     bằng g1, tập khoá `E698` chứa tập của g1, và (r13) tập khoá `KQ` của ba cửa con chứa tập của g1 với độ dài mọi danh sách và từ điển lồng không nhỏ hơn (A10 (v)).
```

chữ đúng: … tập khoá `KQ` của ba cửa con chứa tập của g1, cùng đường, cùng loại, độ dài không nhỏ hơn (A10 (v), cách tính r14).

Căn cứ: gợi ý của VERDICT review đặc tả lượt 14 (`ops/reviews/wp698-spec-review-14-claude-verdict.md`, sha256
`892eeb8a200cec3083b565ffdfe5e26e078ab4ccdafb861c7324b712028e76c7`, dòng 135). Đây là điều kiện CẦN, không đổi kết
luận đo nào — theo chính VERDICT ấy: "không cây nào đo được bị đổi kết luận vì dòng này"; A10 (v) vẫn là tiêu chí
nghiệm thu duy nhất.

## O1..O7-r28

Mục nợ 3. Nguồn: mục "QUAN SÁT KHÔNG XẾP LỚP" của VERDICT review lượt 5 wp685 r28, sha256
`d3f1d9db4896efe8c1b62112a3d0aa479b64c5dc110da1d323b3297d7e7c45fb` (68 dòng, 32.989 byte; không có trong kho), dòng
57–63, chép nguyên văn ở Phụ lục A của đặc tả `no-p3-ho-so` r2. Mỗi khối dưới đây BẰNG từng byte một dòng của Phụ lục A;
phiên thi hành có tệp VERDICT ở scratchpad điều phối và đo: `sha256sum` bằng băm trên, dòng 57–63 băm ra
`7ad7791d184f3734e0716312dea4164bc0ebb882dc0e2e3f5d620a660cc79ab1`, bằng băm của Phụ lục A (đo ~10:40Z).

Đếm trên tệp nguồn: mục ấy có **bảy** gạch đầu dòng (`grep -c "^- [*][*]O[0-9]"` = 7). Dòng 7, 12, 54 của VERDICT
nói "sáu"/"O1–O6" — đó là chữ của nguồn, trích nguyên, không sửa. Phạm vi lời khai, không mạnh hơn: với O1–O6,
VERDICT nói thẳng không cái nào đổi quyết định hay việc của executor (VERDICT dòng 7, 54) và diff r27 → r28 không chạm
acceptance hay closure (dòng 7); với O7, VERDICT chỉ xếp nó vào cùng mục "không xếp lớp" của một verdict `approve` 0
lớp và ghi "đã biết, không hồi quy" — không có câu riêng về acceptance hay closure. Các số `L<n>` trong khối là số dòng
r28, riêng `L168`, `L170` của O4 là số dòng r27.

### O1

```text
- **O1 — bảng "Thay đổi so với r27" hẹp hơn diff ở hai chỗ không chuẩn tắc** (kéo theo ba câu dựa vào bảng ấy: ô `thay_the_cho` mục (r28) *"danh sách đủ các chỗ đổi … là bảng 'Thay đổi so với r27'"*, MCR gạch 3 *"the places changed from r27 to r28 are listed in the spec's table of changes against r27"*, và vế r27 → r28 của ô `revision`). (a) Câu mới L172 *"Phiên soạn r28 đã rà băm rút gọn và trích dòng PROTOCOL bằng script; kết quả không phải acceptance và không ràng buộc ai."* không có ở cột "chỗ sửa trong r28" — hàng cuối chỉ ghi "bảng này", trong khi hàng tương ứng của bảng r26 (do r27 viết) ghi "bảng này và đoạn kiểm r27". (b) Ô "HINT lệch phép đo" của hàng `bam-rut-gon-lech-ban-day-du` (L188): bảng r28 khai "bỏ số đếm của VERDICT lượt 3"; word-diff (M2, M3) cho thấy còn bỏ vế "rà toàn tệp thêm" và thêm "ở cột bên trái … là phần ngoài HINT". Nghĩa giữ nguyên (VERDICT lượt 3 ghi đúng "Phần đầu r26: 71 băm rút gọn", đọc ở `../cr685-r26/goi/VERDICT.md`), chỉ bớt một lời khai phạm vi rà của phiên soạn r27 — đúng hướng chỉ thị. Vì sao không xếp lớp: cả hai nằm trong khối bảng/kiểm của r28, không chuẩn tắc; không đổi tiêu chí, closure, authority hay việc executor; phần r23 → r28 mà chủ kho dựa vào đo bằng nhau (M4, M5). Nếu có r29 vì lý do khác: hàng cuối "…; bảng này và câu kiểm r28 ngay dưới"; hàng 2 "…; ô 'HINT lệch phép đo' bỏ số đếm của VERDICT lượt 3 và vế 'rà toàn tệp thêm', nói ba chỗ sai đuôi là phần ngoài HINT".
```

dòng r28: 172 · 188

quyết định: ghi nhận kèm chữ đề nghị r29 — chữ đề nghị là câu "Nếu có r29 vì lý do khác: …" trong chính khối O1; packet này không mở r29.

### O2

```text
- **O2 — con trỏ "ở cột bên trái"** trong ô "HINT lệch phép đo" (L188, cột 5): ba chỗ sai đuôi được liệt kê ở cột 3 ("chỗ sửa trong r27"); cột liền trái (cột 4, "đo lại của phiên soạn r27") nay chỉ còn câu thu gọn. Đọc chặt thì con trỏ lệch một cột; đọc là "một cột phía trái" thì đúng. Ô lịch sử, không quyết định nào dựa vào. Nếu có r29: "ở cột 'chỗ sửa trong r27'".
```

dòng r28: 188

quyết định: ghi nhận kèm chữ đề nghị r29 — câu "Nếu có r29: …" trong khối O2; packet này không mở r29.

### O3

```text
- **O3 — bằng chứng cho phép sửa đuôi ngoài HINT chỉ còn ở r27.** Ba chỗ §1 L596, L630, §10 L3708 (`6f07a7cf…3ed8` → `…25e8`, sửa từ r27) nay không còn câu bằng chứng trong r28: câu *"Tệp test thử 'bytes' của rig r11 (`lt11_bytes.py`) có sha256 `6f07a7cfecea…3925e8`; bản 'latin-1' … `c4267574…7905`"* bị bỏ (M7: −1 mỗi chuỗi); bản đầy đủ `6f07a7cfecea40852ac0671f6dc9261ab811860ecb434b41fe66599b7b3925e8` chỉ có ở VERDICT lượt 4 M9. r28 vẫn khai việc sửa ("sửa đuôi … cho khớp băm đầy đủ", ô `revision`) và khai việc bỏ câu ("bỏ cả câu về tệp thử 'bytes' của rig r11", bảng r28 hàng 2). Vì sao không xếp lớp: con trỏ "chữ đầy đủ của r27 ở tệp r27" đúng (blob r27 `3cf7ddb8…ac25` không đổi ở HEAD), phép sửa đã được lượt 4 đo đúng, và băm rig §1/§10 không vào acceptance, closure hay việc executor.
```

dòng r28: 596 · 630 · 3708

quyết định: chỉ ghi nhận.

### O4

```text
- **O4 — con trỏ "chữ đầy đủ của r27 ở tệp r27" dẫn tới đúng hai lời khai mà lượt 4 đo là rộng hơn phép đo** (r27 L168 "(19 chỗ)"; L170 "8 … không có bản trong kho hay scratchpad", "25 … đo không được ở đây"). Chữ đã sửa (HINT lượt 4) chỉ còn ở `luot4/HINT.patch` và bản trung gian `acaa21e2…010d`, không ở kho; r28 nêu VERDICT/HINT lượt 4 chỉ bằng sha256, và VERDICT/HINT lượt 1–4 đều nằm ở scratchpad điều phối (M10), không có trong kho cục bộ (M18: 0/23 073 blob cùng kích thước với tám tệp ấy). VERDICT lượt 4 đã đăng lên GitHub chưa, và ref phía máy chủ: `KHÔNG ĐO ĐƯỢC` (lý do 5). Vì sao không xếp lớp: r28 đóng dấu các kết quả ấy "không phải acceptance và không ràng buộc ai"; không quyết định nào dựa vào chúng. Việc đáng làm thuộc ghi sổ, không thuộc đặc tả: lưu VERDICT/HINT các lượt vào nơi có băm trong kho, để con trỏ băm của r28 trỏ tới thứ đọc lại được.
```

dòng r28: 162–163 (con trỏ ngắt dòng, đọc nối)

quyết định: chỉ ghi nhận — `L168`, `L170` trong khối là dòng r27, không phải r28.

### O5

```text
- **O5 — phạm vi chỉ thị "bỏ mọi số đếm phép rà".** PROMPT.md tóm tắt chỉ thị là "bỏ mọi số đếm phép rà khỏi spec"; r28 chỉ thu gọn ô/đoạn của r27. Năm đoạn "Kiểm lúc soạn r22…r26" (r28 L307, L275, L254, L236, L209) và các ô "đo lại" của bảng r24, r25, r26 vẫn giữ số đếm lịch sử (ví dụ L232 "`diff -U0` r23 → r24: 14 hunk"). Lời tự mô tả của r28 khớp việc nó làm (`nguon_cap_viec` mục (r28): *"thu gọn phần tự khai phép rà của phiên soạn (không ghi số đếm phép rà vào đặc tả)"*; bảng r28: *"thu gọn chính các ô và đoạn ấy"*), và mỗi đoạn lịch sử tự khai phạm vi ("mọi số đếm dưới đây đo trên chính tệp rNN"). Nguyên văn chỉ thị giao cho phiên soạn r28: `KHÔNG ĐO ĐƯỢC` (lý do 3). Vì sao không xếp lớp: lịch sử, không ảnh hưởng quyết định; chỉ thị có ý rộng hơn hay không là việc điều phối tự quyết.
```

dòng r28: 209 · 232 · 236 · 254 · 275 · 307

quyết định: chỉ ghi nhận.

### O6

```text
- **O6 — câu tự khai mới L172.** Vế "đã rà băm rút gọn" có bằng chứng (`../wp685-r28/rg_r28.tsv`, 293 dòng, ghi trước commit r28); vế "trích dòng PROTOCOL" không có tệp đầu ra nào ⇒ `KHÔNG ĐO ĐƯỢC` (lý do 3). Đo thay: công cụ phiên soạn trên r28 `{'KHOP': 18, 'SO_CU': 1}` rc=0 và bộ đếm độc lập 13 chỗ chuỗi 597/598, cả 13 là chữ r27 đã đo đúng (M6). Vì sao không xếp lớp: câu tự đóng dấu không ràng buộc ai; không quyết định nào dựa vào nó.
```

dòng r28: 172

quyết định: chỉ ghi nhận.

### O7

```text
- **O7 — đã biết, không hồi quy:** ba giá trị YAML của lease nháp bị cắt ở " #" (M13); cổng lease không đọc `spec_sha256_required`, `spec_hash`, `plan_hash`, `write_set_hash`, `spec_path` (M11: D2, D3, D5–D7 rc=0) ⇒ chuỗi băm chỉ có phép đo tay, phải đo lại cả năm mắt xích sau mọi lần đổi byte. Mission r8 `spec_hash` của wp709 `f569b613…005c`: ngoài chuỗi wp685, không xét (HẸP).
```

dòng r28: — (khối không nêu dòng r28; nó nói về lease nháp và cổng lease)

quyết định: chỉ ghi nhận — vế "cổng lease không đọc `spec_sha256_required`, `spec_hash`, `plan_hash`, `write_set_hash`, `spec_path`" là mục nợ 4 của packet #751 (`ops/specs/no-p3-lease-spec-hash-r2.md` dòng 10, hàng `nguon_cap_viec`; sha256 `8f700b06b28e4c02c615b591b02a75a2fd901239746eb2a3fb8389dd9f549ec4`; tìm ở `master` trước, chưa thấy thì nhánh `claude/spec-no-p3`), không xử ở đây.
