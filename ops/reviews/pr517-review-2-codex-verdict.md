verdict: changes_requested
reviewed_sha: 458314a9c4792c96c513d62e462f68b13c1b3d63
reviewed_base: 46d9561c8cc4b0cf530fc7ca4015de8f07c6aeec
reviewed_files_sha256:
  CHANGELOG.md: 90815daa972140c064cf846bb3b9137802bc30553de50a1ab04b3d4d078aaac6
  RELEASE_MANIFEST.json: ff25b8bea5a060caef128d1fc982f80ada2bb838e85ccf1809195b25ab9e0804
  ops/reviews/README.md: 39234d4b6fdf6997b662b0a06e641941096af6f2e22cfc2a0f168053ff2ad27d
  ops/reviews/pr516-review-1-codex-verdict.md: 1a1235739ebf920811570f3a05b3799f8743aa8e7618b7f9099e001d4e8dc1f0
  ops/reviews/pr516-review-1-codex-verdict.receipt.yaml: 55cee89efeebed23acbf51a205692ca6c70c2bd8f63b4a4b185cdb54b8fdc9c7
  ops/reviews/pr516-review-2-codex-verdict.md: e2d0fc65a809cb7e2be27804f518d41a09a8329b672ae8ebfa438603cb0202fe
  ops/reviews/pr516-review-2-codex-verdict.receipt.yaml: 84273ab3e1c984e7e859b5753c967376c386ec613f704049789ce78eb68b499a
  ops/reviews/pr516-review-3-codex-verdict.md: 532e022c16f75ba5780de45e4e4056788f58ac275d6638a1fbb5c55088cda968
  ops/reviews/pr516-review-3-codex-verdict.receipt.yaml: 8cf325bdb2bf434fe4debfbdd3b363eb743a04d2bed2e3274fb62836393a441b
  ops/reviews/pr516-review-4-codex-verdict.md: 4d227acbc81641f2a25d68870ecf3dbb047a9df390b4382afd853e9452496ca4
  ops/reviews/pr516-review-4-codex-verdict.receipt.yaml: 0722c7ed458ea9e0dd673d037d6b297878d094e05ed74e18389b929daad6af42
  ops/reviews/pr516-review-5-codex-verdict.md: d66f58020aa0330c44597fe87635c9f70eb60d49e5db444cd09da7b24a82a38b
  ops/reviews/pr516-review-5-codex-verdict.receipt.yaml: 6e60586fdcdf10e7dee471ebc9643d1f67060e52cde3d0021566f37641766060
model_tu_khai: GPT-6 / Codex (tự khai theo ngữ cảnh phiên; không attestation độc lập backend)
review_round: 2
so_p1: 0
so_p2: 1
so_p3: 0
so_the_hien: 1
hint_sha256: f7de8c044f84fd89da8ed45e5dfa6c07887d787f195c28c3d4a70d9fdb9bfc62
previous_hint_sha256: 292c42b6fcf58b497539bab6b68536325cd31e05f9c80bb83b399ccd89e66245

**changes_requested — 0 lớp P1 / 1 lớp P2 / 0 lớp P3, 1 thể hiện còn lỗi.** Trong 21 thể hiện lượt trước, 20 ĐÃ VÁ THẬT; thể hiện CHANGELOG:32 trong lớp `tong-hop-doi-tap-doi-tuong` VÁ SINH LỖI MỚI. HINT lượt 1 đã thay chuỗi sai bằng chuỗi vẫn có một mốc sai: `r364` là mục lưu verdict PR #500, còn verdict ấy chấm PR #500/**r363**. Ba lớp còn lại ĐÃ VÁ THẬT.

Tác giả **đã áp nguyên HINT**, không tự thêm câu sai: replay 20/20 hunk, 6/6 tệp `cmp` bằng HEAD, không fuzz/offset/reject. Đây là lỗi của chính đề nghị reviewer lượt 1, phát hiện bằng cách đọc `CHANGELOG.md` tại `reviewed_sha` của verdict nguồn. Không sửa các verdict lịch sử nguyên byte. HINT lượt 2 có 1 hunk / 1 tệp, đổi `r364` → `r363`; manifest phải tái sinh bằng công cụ.

Phạm vi đánh giá là HEAD/base được giao, không tự chuyển sang master mới. **`origin/master` thực tế là `157b36868e13e24fd0c0a468c22941627d2cd0fe`, không phải `46d9561`.** Tuy nhiên merge-base `origin/master...HEAD` đúng `46d9561`, và toàn bộ diff ba chấm bằng byte diff `46d9561...HEAD`: 13 tệp, +1733/−5. Sai khác ref trong prompt/EVIDENCE là thông tin ngoài diff, không cộng finding.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Đối chiếu nguồn `nguon/VERDICT.rvhs517-1.md`: SHA-256 `a97d5d9499222223b1e54d479e70ba010dbc15a138e937839e6a9b922f714bc1`, khớp dòng cuối stdout run `a488739c` (333 B). HINT nguồn 56 938 B, băm đúng `previous_hint_sha256` ở đầu tệp. Bảng này đếm **21 thể hiện cũ**, khác với `so_the_hien: 1` là số thể hiện lỗi hiện tại.

Ký hiệu: CH = `CHANGELOG.md`; README = `ops/reviews/README.md`; Rn = `ops/reviews/pr516-review-n-codex-verdict.receipt.yaml`; Vn = verdict `.md` cạnh receipt, đã `cmp` byte với `nguon/VERDICT.rvhs516-n.md`. Mọi vị trí dưới đây là **dòng HEAD 458314a tự đếm**, không sao số dòng lượt trước. Cụ thể cảnh báo quota nằm README:31, launcher README:40, cảnh báo mutant README:42; README:29 là hàng tiêu đề bảng. Không coi sai tọa độ trong prompt/verdict cũ là finding mới của PR.

### nguon-thuat-lai-bi-nang-thanh-do — ĐÃ VÁ THẬT

10/10 thể hiện đã thu hẹp hoặc gắn đúng loại nguồn. Phân biệt **đo được log có thông điệp** với **chứng thực nội dung dự báo khả dụng của thông điệp**; chỉ vế đầu có hiện vật.

| Vị trí HEAD mới · khai sau HINT | Trạng thái | Bằng chứng tự đo |
|---|---|---|
| CH:1 · probe có `(b) tác giả thuật lại` | ĐÃ VÁ THẬT | Đọc tiêu đề có nhãn ngay trước probe; inventory nguồn chỉ có 5 run #516 và run review #517 lượt 1, không có log probe quota 02:3xZ. Không biến rc=0 thuật lại thành phép chạy tự đo. |
| CH:4–5 · run rc=1, stderr báo giới hạn; không chứng minh hiện không chạy được | ĐÃ VÁ THẬT | `nguon/runs/6c8b0629/run.json` ma_thoat=1; stdout 0 B; stderr:2243–2244 có hai lỗi usage limit. Không có phép đo khả dụng hiện tại trong run đó. Câu kết luận hiện không còn quota đã bỏ. |
| CH:22 · số Git/băm/byte/finding (a), runtime nguồn ngoài kho, sự kiện (b), sandbox cũ (c) | ĐÃ VÁ THẬT | Tự kiểm Git, băm verdict/HINT và finding từng lượt; đối chiếu timestamp/exit/duration/log với run.json. Tiêu đề không còn phủ toàn bộ bảng 26–30 bằng (b); không nâng các phép mutant/land cũ thành (a). |
| CH:65–71 · probe thuật lại, không đo được probe/độ dài quota | ĐÃ VÁ THẬT | Nhãn (b) mở đoạn lịch sử; câu đo được giới hạn đúng chuỗi stderr ở run 6c8b0629. Câu cũ suy “cửa sổ giới hạn” đã bỏ. Chưa có log probe; không kết luận probe sai hoặc chưa từng xảy ra. |
| CH:78–91 · Git/băm/byte (a), thao tác/thứ tự chạy cổng (b) | ĐÃ VÁ THẬT | Git xác nhận chuỗi 8fd3f48→896bfbf→86f87b2→458314a và blob; không chứng minh amend trước push hoặc thứ tự chạy gate. Nhãn mới phân biệt đúng hai loại, không coi HEAD gate xanh là bằng chứng lịch sử điều phối. |
| CH:102–103 · không đo được thời lượng giới hạn quota | ĐÃ VÁ THẬT | Đọc NỢ không còn “giới hạn ấy hoá ra ngắn”; giữ probe dưới (b). Cùng đối chứng run/log và inventory nêu trên. |
| R5:99 · stderr đo được; probe/việc chưa phóng lượt trọn là thuật lại | ĐÃ VÁ THẬT | YAML phân tích được; câu không còn “probe cho thấy giới hạn KHÔNG kéo dài tới 15-09”; có nhãn (b), thiếu log và giới hạn kết luận rõ. Mutant Q1 trả lại câu cũ làm kiểm nguồn đỏ. |
| README:31 · bản chiếu caveat quota R5 | ĐÃ VÁ THẬT | Ghép `mo_ta` + `phai_lam_gi_khi_chay_lai`, bỏ bold/escape Markdown, bằng nội dung hàng này. Cùng giới hạn nguồn như R5:99; không coi bản chiếu là chứng cứ độc lập. |
| README:15 · mutant sống được ghi `(c) Theo các verdict lượt 1–3` | ĐÃ VÁ THẬT | V1:323/325, V2:21/157, V3:94 thực ghi so_p2/verdict_bytes/assurance sống bốn cổng ở head mỗi lượt. Đoạn mới không tự nhận phép chạy lại tại r371. |
| README:423 · khối cmp/runtime/neo/mutant/land cũ có (c) | ĐÃ VÁ THẬT | Nhãn `(c) Các phép chạy dưới đây ... thuật lại từ verdict` đứng trước khối; V1 có các kết quả tương ứng. Runtime được đoạn cuối tách là đối chiếu nguồn ngoài kho; không nâng inventory/run #511 được kể lại thành raw hiện vật đã cấp trực tiếp. |

Không thấy câu mới về quota/probe sinh lỗi cùng lớp hoặc lớp khác. “Thông điệp lỗi ... (b)” trong CH:71 được đọc trong phạm vi nội dung nhà cung cấp thuật lại, không phủ nhận việc tự kiểm được byte stderr. Các lời khai `last.md` rỗng, ai tính băm và sự kiện GitHub giữ giới hạn chưa đo được bên dưới; HINT không tạo ra bằng chứng cho chúng.

### template-khong-khoa-theo-luot — ĐÃ VÁ THẬT

4/4 thể hiện đã gắn đúng lượt. Caveat launcher được **chuyển** sang R2, không nhân thêm một caveat.

| Vị trí HEAD mới · khai sau HINT | Trạng thái | Bằng chứng tự đo |
|---|---|---|
| R1:76 · nguồn PR #511; chưa có lượt trước PR #516 | ĐÃ VÁ THẬT | Prompt `a146d00d`:11–13 liệt kê 2 VERDICT/HINT #511, hai run #511, actionlint; là lượt 1 #516. HINT bỏ lời khai tồn tại các lượt #516 trước đó. Version binary lịch sử chỉ khớp mô tả prompt, không tái chạy binary. |
| R2:107–112 · caveat launcher, đã xoá khỏi R3 | ĐÃ VÁ THẬT | V2:23 có lời tự khai dấu kết thúc sai, xuất phần sau bảng, không dùng phần ấy và không tự nhận giữ trọn rào đọc. Toàn V3 không có `_TRANSPORT_CONTRACTS`; source owner=2, receipt owner=2. Không mở launcher. |
| README:40 · caveat launcher mang tên pr516-review-2 | ĐÃ VÁ THẬT | Đúng một hàng có cặp R2/id launcher; nội dung bằng caveat R2. Không còn hàng launcher gắn pr516-review-3. Mutant T1 chuyển cả receipt và hàng về lượt 3: kiểm owner nguồn đỏ dù t27 xanh. |
| R5:33 · HINT 0 hunk, 4 dòng ghi chú | ĐÃ VÁ THẬT | `nguon/HINT.rvhs516-5.patch`: 300 B, 4 LF, 4 splitlines, 0 `@@`; SHA `434746d1…` khớp YAML. HINT2/HINT3 mỗi tệp 1 dòng là nguồn của template cũ, không áp cho HINT5 nữa. |

### tong-hop-doi-tap-doi-tuong — VÁ SINH LỖI MỚI

5/6 thể hiện đã vá thật. Thể hiện còn lại thay tập mốc cũ bằng tập vẫn lẫn một **mục ghi sổ** với **PR được chấm**; token `r364` mới do HINT đưa vào.

| Vị trí HEAD mới · khai sau HINT | Trạng thái | Bằng chứng tự đo |
|---|---|---|
| R1:104 · khai 4 mutant ĐỎ, đúng 5 gồm 3 ĐỎ/2 SỐNG | ĐÃ VÁ THẬT | Parse 5 hàng `ops/reviews/pr511-review-1-codex-verdict.md`:358–362: M1/M2/M4 có ít nhất một rc≠0; M3/M5 cả bốn rc=0. Có 4 ô gate đỏ, chỉ 3 mutant bị giết. V1:284–286 mô tả đúng lỗi đó. |
| README:42 · bản chiếu thống kê mutant R1 | ĐÃ VÁ THẬT | Bằng nội dung R1 sau chuẩn hoá Markdown; giữ cả tổng 5 và thuộc tính ĐỎ/SỐNG 3/2. Không còn diễn giải sai tổng 4→5. |
| README:15 · thống kê mutant trong đoạn nguồn | ĐÃ VÁ THẬT | Đoạn mới cũng ghi đúng 5/3/2 và nói lời khai sai là “4 mutant ĐỎ”. Mutant S1 đổi 3 ĐỎ→4 ĐỎ đồng bộ receipt/README bị phép đếm từ bảng nguồn bác. |
| R3:98 · 4 pr511 bằng byte, 3 tệp tích hợp đổi | ĐÃ VÁ THẬT | So blob 5f45e6e→c98c33e: 2 verdict+2 receipt pr511 bằng byte; CH 1 001 730→1 042 451 B, README 341 484→390 677 B; manifest đều 30 336 B nhưng SHA khác. V4:24/45–62 khớp phạm vi này. |
| README:36 · bản chiếu 4 pr511/3 tệp tích hợp | ĐÃ VÁ THẬT | Nội dung bằng R3:98 + hướng dẫn chạy lại; cùng phép so 7 blob lịch sử. Không dùng 7/7 của hai lượt cùng c98c33e để nói 7/7 qua merge. |
| CH:32 · bốn PR `r364→r366→r367→r369` | VÁ SINH LỖI MỚI | Đọc `reviewed_sha` của verdict #500/#510/#511/#516, rồi dòng đầu CH tại mỗi SHA: **r363/r366/r367/r369**. #500 chấm 5a29d35, CH đầu là r363; CH hiện tại:987–991 nói r364 ghi sổ #500. R364 mới trong HINT vẫn là tập đối tượng sai. Xem finding duy nhất bên dưới. |

### dem-dong-cong-them-duoi-lf — ĐÃ VÁ THẬT

| Vị trí HEAD mới · khai sau HINT | Trạng thái | Bằng chứng tự đo |
|---|---|---|
| CH:53 · V5 đầy đủ 83 dòng, 7 577 B | ĐÃ VÁ THẬT | Source và blob verdict cùng 7 577 B, 83 LF, 83 splitlines, kết thúc LF. R5:25 cũng ghi 83; không cộng thêm dòng rỗng sau LF cuối. Không sửa verdict để làm khớp lời khai. |

## Bảng đo lại

“Khớp nguồn” dưới đây không chứng thực các sự kiện được nguồn thuật lại. Các lệnh đều là local; log và mã đo của **lượt 2 này** nằm `scratch/luot1/`.

| Khai / phép kiểm | Đo tại lượt 2 | Kết quả |
|---|---|---|
| HEAD/base/diff PR | HEAD đúng 458314a, base cố định 46d9561; 4 commit base..HEAD. origin/master khác lời khai nhưng merge-base đúng và hai diff ba chấm bằng byte. 13 tệp +1733/−5. | KHỚP phạm vi; ref origin/master khai sai ngoài diff |
| 13 băm tệp đầu verdict | Băm worktree bằng blob HEAD ở cả 13 tệp; lặp kiểm cuối cùng vẫn bằng băm ban đầu; status rỗng. | KHỚP |
| HINT lượt 1 áp nguyên | `patch --batch --fuzz=0 --verbose -p0` tại bản sao 86f87b2: rc0, 20 hunk succeeded, 0 fuzz/offset, 0 `.rej`; chạy `cmp` 6 tệp với HEAD đều rc0. | KHỚP kết quả replay; không chứng thực executor đã gõ gì trong lịch sử |
| Ngoài HINT trong 86f87b2..458314a | Sau replay, residual diff với HEAD chỉ RELEASE_MANIFEST.json, **2 hunk, +5/−5 dòng**. Tái sinh deterministic qua `--out` được 30 336 B, SHA `ff25b8bea5a060caef128d1fc982f80ada2bb838e85ccf1809195b25ab9e0804`, bằng byte HEAD. | KHỚP; 0 hunk nội dung ngoài HINT |
| Bản vá lượt 1, 7 tệp | Git numstat: CH +11/−10, README +6/−6, R1 +2/−2, R2 +6/−0, R3 +1/−7, R5 +2/−2, manifest +5/−5. | KHỚP |
| 5 verdict và 5 receipt | 5 verdict `cmp` bằng nguồn, băm/byte/HINT đúng; source reviewed_sha/base và băm 7 tệp mỗi V516 đối chiếu được với Git. Không thay 5 verdict trong commit 458314a. | KHỚP |
| Finding / assurance | V1 0/4/1; V2 0/0/0; V3 0/0/0; V4 0/1/0; V5 0/0/0. Assurance lần lượt reviewed/approved/approved/reviewed/reviewed. R4 dùng slug mô tả tương ứng P2-E01, không bắt bằng phép so chuỗi ID máy móc. | KHỚP nội dung nguồn |
| Runtime | So ID, prompt SHA thật, timestamp, hiệu thời gian, exit, trạng thái, transport, head, byte+SHA stdout/stderr giữa YAML/run.json/tệp log: mọi đối chiếu đã thực hiện khớp. Effort/model yêu cầu không chứng thực backend; số retry là attestation. | KHỚP các trường đo được |
| R5 kết thúc lỗi và verdict đầy đủ | ma_thoat=1, trạng thái wrapper=xong; stdout=0 B; hai dòng usage-limit ở stderr cuối; verdict 83 dòng có đầy đủ các mục và 7 băm bằng V4. `last.md` không được cấp. | KHỚP phần có hiện vật; không suy run sạch |
| README và CH | README 756 LF/406 046 B; CH 12 155 LF/1 054 164 B. README thêm 20 LF so base: 1 đoạn nguồn + 1 trống + 13 cảnh báo + 5 mục lục. | KHỚP |
| 13 caveat vận chuyển vào README | Phân bố R1…R5 = **2/4/2/2/3**, tổng 13; mỗi cặp verdict/id có đúng 1 hàng, cả 13 nội dung bằng receipt sau bỏ bold/escape `|`. | KHỚP cấu trúc và nội dung vận chuyển |
| (a)/(b)/(c) ở CH:22, README:15/423 | Đều tách số/Git/băm đo được, sự kiện/probe thuật lại, kết quả sandbox cũ thuật lại; runtime có nguồn ngoài kho. Giới hạn mutant đúng V1/V2/V3, không nhận là phép chạy mới của tác giả r371. | KHỚP; không có lỗi nguồn mới ở các câu sửa này |
| v2 trên HEAD | `python3 -B ops/bien_nhan_v2.py --root .`: rc0, **105 ĐẠT v2 · 11/11 legacy · 42 NỢ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 158**. | QUA |
| t26/t27 trên HEAD | Importlib `ops/lease_publish_test.py`, chọn duy nhất hàm `t26_` và `t27_` từ CA, gọi bằng Python `-B`: rc0/0. | QUA |
| Release strict HEAD | `python3 -B scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json`: rc0, ok=true, **180/180**, package hash expected=current=`262f26495c08881da8d6312237856f061c75bfc7ee3cdd3cb702c557e0fae3d9`; errors/missing/failed rỗng. | QUA |
| Whitespace | `git diff --check 46d9561...HEAD` rc0, không output. | QUA |
| HINT lượt 2 | 1 hunk/CH; áp thực không fuzz/offset; 6 kiểm nội dung đều qua; tái sinh manifest rồi v2/t26/t27/release/diff-check đều rc0. V2 vẫn105/0/158, release180/180. | QUA trên bản sao đề nghị |

Lệnh release đầu tiên của tôi thiếu đối số `RELEASE_MANIFEST.json`, nên parser trả rc2 trước khi kiểm. Đã sửa invocation và chạy lệnh đầy đủ ở hàng trên; không tính rc2 đó là lỗi PR hoặc là phép verify đã chạy.

### Byte, dòng, HINT và runtime năm nguồn

| Lượt | Verdict byte / LF | P1/P2/P3 | HINT byte / dòng / hunk | Hiệu timestamp (s) | ma_thoat / stdout byte | Bảng đo lại: khoảng / số dòng |
|---|---|---|---|---|---|---|
| 1 | 74068 / 353 | 0/4/1 | 28684 / 120 / 8 | 1089.259092 | 0 / 323 | 25–279 / 255 |
| 2 | 36923 / 237 | 0/0/0 | 82 / 1 / 0 | 682.561435 | 0 / 389 | 59–200 / 142 |
| 3 | 14796 / 106 | 0/0/0 | 100 / 1 / 0 | 462.237538 | 0 / 330 | 27–70 / 44 |
| 4 | 16275 / 163 | 0/1/0 | 853 / 9 / 0 | 631.034213 | 0 / 482 | 35–95 / 61 |
| 5 | 7577 / 83 | 0/0/0 | 300 / 4 / 0 | 260.011346 | 1 / 0 | 38–61 / 24 |

Số dòng Bảng đo lại đếm cả heading và dòng trống trong khoảng, không phải số hàng dữ liệu. Thời lượng YAML/run.json làm tròn 3 chữ số khớp hiệu timestamp ở bảng. `cross_approved` của R2/R3 phản ánh phạm vi nguồn; không hồi tố nó thành approve head c98c33e. Caveat mức P1 của R5 không phải finding P1 của V5 hoặc của lần review này.

### Ba lối land lên base 46d9561 — đã đo lại trên HEAD lượt 2

| Lối land | Commit mô phỏng | Cha | Neo 8fd3f48 | v2 |
|---|---|---|---|---|
| merge | `a3fdbc22453dad8cf6aa87d205de93ecc7b88594` | `46d9561c8cc4b0cf530fc7ca4015de8f07c6aeec 458314a9c4792c96c513d62e462f68b13c1b3d63` | còn là tổ tiên | 105/0/158, rc0 |
| ff | `458314a9c4792c96c513d62e462f68b13c1b3d63` | `86f87b2004f6054572cc787ae660518763b29b95` | còn là tổ tiên | 105/0/158, rc0 |
| squash | `8e4a831c560e3a0ecf91bd98ea5b0c1f54af972f` | `46d9561c8cc4b0cf530fc7ca4015de8f07c6aeec` | không còn là tổ tiên | 100/5/158, rc1 |

Merge và squash được dựng bằng `git commit-tree`, cùng tree HEAD; ff dùng chính HEAD hiện có. Squash chỉ có cha base; stderr chỉ tên đúng **5 receipt pr516** mất canonical ancestry. Không gán hai receipt pr511 của phép land lịch sử #516 thành số vi phạm của #517. Đây là mô phỏng local, không phải hành động land trên GitHub. Không lặp các bộ land lịch sử #516 của lượt 1.

## Findings theo lớp

### tong-hop-doi-tap-doi-tuong [P2]

**Hạng lớp: P2. Số thể hiện: 1.** Cơ chế: lấy số r của mục chứa hồ sơ để định danh PR mà verdict đang chấm. HINT cũ đã bỏ r371 ở cuối nhưng đưa r364 vào đầu từ chính mục ghi sổ #500; vậy phép thay chưa giữ đúng quan hệ verdict→reviewed_sha→r. Tên PR bị quy finding sai, dù tổng bốn PR và các băm/neo vẫn đúng. Không có sai số thẩm quyền hay cổng chốt bị tắt để xếp P1.

| Tệp:dòng | Khai | Đo |
|---|---|---|
| `CHANGELOG.md:32` | `r364→r366→r367→r369` là bốn PR hồ sơ ăn finding | Verdict PR #500 ghi reviewed_sha=5a29d358… tại dòng 4; `git show 5a29d35:CHANGELOG.md` dòng đầu là **r363**, không phải r364. CH hiện tại:987–991 tự mô tả **r364 ghi sổ #500**. Ba cặp sau đúng. |

Đối chứng bằng Git tại từng SHA, không chỉ đọc lời tổng hợp của lượt trước:

| PR có verdict finding | Tệp nguồn dưới ops/reviews | reviewed_sha | Dòng đầu CHANGELOG tại SHA đó |
|---|---|---|---|
| #500 | `pr500-review-1-codex-verdict.md` | `5a29d358649c9d70632cd2aa2e5cb8ac53884dc8` | **r363** |
| #510 | `pr510-review-1-codex-verdict.md` | `3349c8b2e2b544ce98c2ea088e6c09d71b1092f0` | **r366** |
| #511 | `pr511-review-1-codex-verdict.md` | `51466e6e468f0b92997baadb1f64dfa55a926859` | **r367** |
| #516 | `pr516-review-1-codex-verdict.md` | `899f305997544dc78947af6dd58aa490ed3538f3` | **r369** |

**Cách chữa chung:** lấy số r của **đối tượng được review** từ `CHANGELOG.md` tại `reviewed_sha` của verdict, không lấy heading nơi verdict được ghi sổ về sau. Chuỗi đúng ở câu này là **r363→r366→r367→r369**. Tổng bốn giữ nguyên; CH:70 nói bốn PR không liệt kê mốc sai nên không là thể hiện thứ hai.

**HINT theo lớp:** `HINT.patch`, khối `# LỚP tong-hop-doi-tap-doi-tuong [P2]`, 1 hunk đổi r364→r363 ở CH:32; sau áp chạy `python3 -B scripts/tl.py release-manifest --deterministic --out RELEASE_MANIFEST.json`. Không sửa manifest tay. Bản sao đã áp/thử xong nằm `scratch/luot1/replay/`; chỉ CH và manifest khác HEAD.

Không quy lỗi này cho tác giả tự thêm chữ: phép replay đã xác nhận nó có nguyên trong HINT reviewer lượt 1. Không sửa `nguon/VERDICT.rvhs517-1.md`, các HINT nguồn hoặc các verdict đã neo để che sai sót trước đó. Các nhắc r364 sai đối tượng đã có trong mục cũ ngoài diff được dùng làm dấu vết nguồn, không cộng thành finding PR này.

## Mutant đã chạy

Không lặp M1–M6 lượt 1. Các mutant dưới đây chỉ đổi lời khai mới hoặc đưa câu đã sửa trở lại. Mã `scratch/luot1/semantics.py` đối chiếu nguồn trực tiếp: stderr/probe attribution, nguồn self-report của launcher, 5 hàng JSON mutant, 7 blob qua merge, reviewed_sha→heading r, LF verdict5. Đây là phép kiểm của reviewer, **không phải cổng sản phẩm mới**; không nhận nó là bộ hiểu mọi câu tiếng Việt.

Đối chứng HEAD: năm kiểm nội dung qua, riêng `tap-reviewed-pr-chain` đã đỏ vì finding thật. Với Q1/T1/S1, ghi riêng **kiểm mới đỏ thêm**, tránh lấy failure sẵn có làm công của mutant. Mỗi mutant reset bản sao HEAD; khi đổi caveat, bản chiếu README cũng được đổi đồng bộ để tránh chỉ đo lỗi vận chuyển.

| Mutant · lớp được đo | Thay đổi trong bản sao | Phép đối chiếu nội dung | v2 | t26 | t27 | release strict |
|---|---|---|---|---|---|---|
| Q1-quota-nguon · nguồn | Trả đúng dòng `phai_lam_gi_khi_chay_lai` R5 về 86f87b2 và cùng nội dung README | `nguon-quota` mới đỏ: thiếu nguồn (b)/log caveat, lại suy thời lượng quota từ probe không có log | 0 | 0 | 0 | 0 |
| T1-launcher-sai-luot · template | Chuyển nguyên caveat R2→R3 và đổi tên verdict ở hàng README | `template-launcher-owner` mới đỏ: source owner=[2], receipt/README owner=[3] | 0 | 0 | 0 | 0 |
| S1-mutant-dem-do · tập đối tượng | Đổi số thực tế 3 ĐỎ→4 ĐỎ trong R1 và hai bản chiếu README | `tap-mutant-counts` mới đỏ: khai [5,4,2], 5 hàng nguồn suy ra [5,3,2] | 0 | 0 | 0 | 0 |
| S2-chain-regression · tập đối tượng, riêng bản đề nghị lượt 2 | Sau HINT lượt 2, đảo đúng r363→r364 ở CH:32 rồi phục hồi byte | Bản đề nghị 6/6 kiểm qua; mutant chỉ `tap-reviewed-pr-chain` đỏ, vì chuỗi khai khác bốn heading tại reviewed_sha | không chạy | không chạy | không chạy | không chạy |

Q1/T1/S1 giết được bằng đối chiếu nội dung, còn bốn cổng gốc xanh đúng giới hạn đã công khai: t27 kiểm cặp tên/id, không kiểm nội dung caveat có đúng lượt; release không bao phủ README/receipt. Không nâng giới hạn cũ thành finding P1 mới. S2 đo đúng câu HINT lượt 2; sau phục hồi, cả sáu kiểm nội dung lại qua. Bộ v2/t26/t27/release đã chạy trên bản đề nghị sau tái sinh manifest và đều qua.

Hiện vật chính: `logs/hint-summary.json`, `hint-apply.stdout`, `outside-hint.diff`, `audit.json`, `pr-chain.json`, `semantics-head.json`, `mutants-summary.json`, từng `*-semantics.json`/`.diff`/log cổng, `land-summary.json`, `round2-hint-summary.json`, `semantics-proposed.json`, `S2-chain-regression-semantics.json`, `final-state.json`, đều dưới `scratch/luot1/`. Lệnh có log stdout/stderr và metadata rc; các bảng so nội dung có actual/expected riêng để đọc lại.

## chua_do_duoc

- Không dùng mạng, không gọi `ls-remote`. Không xác thực CI/comment/review object/threads/resolve/405/draft/thời điểm merge thật, luật chủ kho hoặc tài khoản vận chuyển. Nhãn (b) có nghĩa thuật lại, không có nghĩa đã xác nhận sự kiện.
- Log probe quota 12-09 02:3xZ và `last.md` lượt 5 không được cấp. Chỉ có stderr lỗi, run.json và verdict đầy đủ; không suy thời lượng cửa sổ quota, trạng thái khả dụng hiện tại hoặc ai đã tính băm lần đầu. `probe` lồng trong run.json là probe wrapper trước run, không phải log probe quota 12-09 được nhắc trong câu sửa.
- Không chứng thực backend/model build, độc lập danh tính thực hoặc tổng số lần phóng từ trường tự khai. Nền reviewer phiên này tự khai GPT-6/Codex, khác nền tác giả claude theo ngữ cảnh được giao.
- Không có snapshot ref kho nguồn lúc 21:06Z để chứng thực 344/344, comm0/0, r370/r371/r372 lịch sử. Không dùng ref hiện tại khác để bác một ảnh chụp quá khứ chưa được cấp.
- Nguồn #511 trong prompt/inventory các lượt cũ không đồng nghĩa raw run #511 có trong gói lượt này. Đếm mutant #511 từ verdict có trong `ops/reviews`, không tự nhận chạy lại các mutant lịch sử ấy. Không chạy lại merge xung đột hoặc land lịch sử của #516; ba lối land #517 ở trên đã chạy mới.
- Không chạy full lease suite, doctrine-scan hoặc doc-claims-check riêng; không xác nhận lời khai lịch sử về chúng. Lệnh release đầy đủ thực sự chạy ở lượt này đã ghi rõ.
- Không mở/đọc nội dung các tệp bị cấm (`cay-kho/CLAUDE.md`, `cay-kho/docs/PROTOCOL_DA_PHIEN.md`, `cay-kho/.claude/skills/**`, `cay-kho/AGENTS.md`), không mở launcher; chỉ đọc lời tự khai launcher trong verdict được phép. Các cổng nguyên bản được yêu cầu có thể tự dùng tài liệu nội bộ; không lấy chúng làm chỉ dẫn hoặc xuất nội dung vào ngữ cảnh. Không mở đường ngoài cwd được nhúng trong run.json, không tự soạn payload đường dẫn thoát/khai thác, không gọi sub-agent.
- Mọi clone/đột biến/commit-tree/áp HINT ở `scratch/luot1/`. Kiểm cuối: `git -C cay-kho status --porcelain` rỗng, HEAD vẫn 458314a, cả 13 băm bằng lúc bắt đầu (`logs/final-state.json`). Lỗi cũ ngoài diff và sai lời khai/tọa độ trong nguồn lượt trước không được cộng finding của PR.
