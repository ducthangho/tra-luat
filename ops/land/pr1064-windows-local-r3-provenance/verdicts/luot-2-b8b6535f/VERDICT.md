verdict: changes_requested
reviewed_sha: b4ccc45dd56284259fb996ac3b3227418bece911
Kết quả: 0 P0, 0 P1, 1 P2, 0 P3.

Reviewer độc lập: provider `openai_codex`; công cụ shell trong sandbox Linux; review hai trục **Spec** và **Standards/Security**. Ngưỡng áp dụng: 0 P0–P3 theo đặc tả §3. Không sửa branch/nội dung checkout, không đăng GitHub, không merge. Snapshot §8.2 của phiên điều phối nằm ngoài sandbox và không được tự nhận là đã kiểm bởi reviewer.

Đã xác minh HEAD đúng SHA yêu cầu; đặc tả có SHA-256 `f1a666a32161f0607ac27bc8c3be6963bb6367e64f02825635a75cc8185fa973`.
Diff có đúng hai tệp trong write set, 89 dòng thêm, 2 dòng xoá. Không sửa nội dung `cay-kho/`.

### suy-gio-luot-thanh-gio-tien-trinh [P2]

**Vị trí:** `cay-kho/docs/adr/0059-windows-local-nhip-tim-khoa.md:63–64`; đối chiếu điều kiện ở dòng 35–37, số đo ở dòng 20–21, `spec-r3.md:21–22,34–36`, và ADR-0057 dòng 38–39,45–46.

**Bằng chứng:** D10 cần so **giờ khởi động `python.exe` (`CreationDate`)** với `UTC bắt đầu` của khoá. Đoạn ví dụ lấy `14:03:16Z − 18113 s = 09:01:23Z` rồi dùng kết quả làm giờ khởi động PID 26296, kết luận khoá còn sống. Phép trừ đúng; tuy nhiên số đo chỉ khai thời lượng **lượt selftest**, không khai `CreationDate`, không định nghĩa thời lượng ấy là tuổi của PID, cũng không chứng minh thời điểm bắt đầu lượt trùng thời điểm tạo tiến trình. Cột `thoi_luong_s` của ADR-0057 cũng không định nghĩa bất biến này.

Phản ví dụ chỉ dùng các quan hệ thời gian trong văn bản: cùng khoá bắt đầu `09:01:16Z`, cùng selftest bắt đầu `09:01:23Z`, chạy 18113 s và xong `14:03:16Z`; một tiến trình có thể đã được tạo lúc `09:01:15Z`, trước khi lượt bắt đầu. ADR-0057/0058/0059 không cấm quan hệ này. Khi đó `CreationDate > UTC bắt đầu khoá` là **sai**, trong khi nếu PID được tạo lúc `09:01:23Z` thì điều kiện là **đúng**. Cả hai cùng khớp các số đo được cung cấp. Đây là phản ví dụ giả định về độ đủ của bằng chứng, không phải lời khai PID thực tế khởi động lúc `09:01:15Z`.

Đã chạy `PYTHONDONTWRITEBYTECODE=1 python3 evidence/kiem-d10.py`, rc=0: hai khả năng đều có `process_exists_by_test_start: true`, nhưng `CreationDate_after_lock_start` lần lượt là `true` và `false`. Vì vậy ví dụ chưa chứng minh được kết quả bắt buộc “không tiếp nhận” bằng đúng điều kiện mà mục 2 đặt ra. Đọc giờ suy ra như `CreationDate` thì chặn; đọc đúng giới hạn số đo thì thiếu dữ kiện quyết định. Lỗi nằm ở lời chứng của ví dụ, không ở việc chép luật mục 2.

**Đề xuất sửa cụ thể:** sửa đoạn D10 dòng 63–64 để tách rõ “giờ bắt đầu lượt suy ra” khỏi “giờ khởi động tiến trình”. Bổ sung số đo/nguồn kiểm được cho `CreationDate` UTC của đúng PID 26296, hoặc nguồn chứng minh 18113 s thực sự đo từ lúc PID đó được tạo đến lúc kết thúc. Chỉ kết luận D10 thoả điều kiện khi nguồn đó chứng minh mốc khởi động sau `09:01:16Z`. Nếu không có nguồn thì khai thiếu phép đo và chưa chứng minh được ca D10; không trình bày phép trừ thời lượng như bằng chứng tương đương. Giữ nguyên bảng D10–D12 và quy tắc đã đóng băng; không tự đổi luật thành “thấy PID sống là chặn”.

**Ca kiểm đóng lớp và rủi ro của bản vá:** đối chiếu nguồn với đúng PID/lệnh/UTC; kiểm cả hai thời điểm tạo tiến trình ở phản ví dụ trên để bảo đảm không còn suy `CreationDate` chỉ từ thời lượng lượt. Nguồn bổ sung phải chứng minh ca thực, không chỉ thêm một giả định vào ví dụ. Bản vá không được mở rộng điều kiện chặn của đặc tả hay sửa ADR-0057/0058 ngoài write set.

**Quét cùng lớp:** đã quét `CreationDate|18113|09:01:23|26296|khởi động` trong cả ADR-0057/0058/0059 và đặc tả. Chỉ dòng 63–64 thực hiện phép đồng nhất hai loại mốc. Các lần nhắc 18113 s ở bảng D11 và phương án bị loại dòng 84–85 chỉ mô tả thời lượng lượt, không tự suy tuổi PID. Tổng: **1 lớp, 1 biểu hiện**, mức cao nhất P2, nguồn candidate SHA nêu trên; chưa có verdict r3 trước được giao để đối chiếu.

## Ba ca

Các bước dưới đây chỉ dùng luật và dữ kiện trong ADR-0057/0058/0059. Không giả định có công cụ khoá nguyên tử, không dùng việc các scanner xanh để suy ra luật đúng.

**(i) A ngắt → quá hạn, tiến trình A đã dừng → B tiếp nhận theo 3(a) → A kết nối lại.**

1. Quá hạn ghi trong dòng làm khoá A hết hiệu lực: ADR-0058 dòng 33–35. Lượt đang chạy khi mất truy cập phải ghi `ngat=co`, bỏ thời lượng khỏi rà soát và không tự đổi nguồn/ngủ: ADR-0059 dòng 40–43.
2. B chạy kiểm tải ADR-0057 §4 (dòng 38–39), rồi áp ADR-0059 mục 2 (dòng 33–39). Theo tiền đề không có tiến trình thoả điều kiện chặn; B ghi sổ nêu session/UTC khoá cũ và lý do (a), rồi mới thay nội dung bằng dòng B, đúng ADR-0058 dòng 38–40 và ADR-0059 dòng 39. Không dừng tiến trình của phiên khác.
3. A kết nối lại: ADR-0059 mục 4 dòng 44–48 buộc đọc trước khi ghi lại. Dòng hiện có mang ID B, nên A **không còn giữ khoá**; không được dùng quyền gia hạn dòng của chính mình ở dòng 49–51. B còn hạn thì A đợi.
4. Nếu A định nhả khoá cũ, mục 5 dòng 53 dẫn về mục 4; sau bước 3, A không phải phiên giữ khoá nên không được ghi rỗng dòng B.

Kết quả: **dòng B giữ nguyên**, đúng yêu cầu. Giới hạn đọc/ghi không nguyên tử ở dòng 52,70 được khai rõ, cũng nằm ngoài phạm vi đặc tả §5.

**(ii) Khoá A quá hạn, chưa ai tiếp nhận → A kết nối lại.**

1. A đọc theo mục 4 dòng 45: dòng vẫn mang ID A. Quá hạn theo ADR-0058 3(a) không làm mất khả năng gia hạn này: ADR-0059 dòng 49–51 nói rõ trường hợp đó được gia hạn.
2. A chạy bước kiểm tải ADR-0057 §4. Nếu chính tiến trình A vẫn chạy trong thư mục riêng theo §5, ADR-0059 dòng 50–51 nói nó không chặn gia hạn; mục 2 chỉ áp cho khoá của phiên khác. Bước kiểm tải của ADR-0057 ghi nhận tiến trình ngoài phiên và cấm tự dừng chúng, không tự đặt thêm một điều kiện cấm gia hạn.
3. Trước lần ghi lại vẫn phải thoả mục 4: ID hiện có là A. A giữ nguyên `UTC bắt đầu`, ghi nhịp tim hiện tại và hạn mới không quá 2 giờ kể từ lần ghi, theo dòng 26–32. Dòng 61 xác nhận cùng cách xử lý.

Kết quả: **A gia hạn được**, kể cả biến thể tiến trình chính A còn chạy. Không tiếp nhận lại khoá của phiên khác, không áp sai mục 2 vào A.

**(iii) D10.**

1. Dòng cũ không có hạn, UTC bắt đầu `09:01:16Z`; tới `13:58:02Z` đã quá 2 giờ, nên thuộc ADR-0058 3(b), không phải 3(c): ADR-0058 dòng 35–37, ADR-0059 dòng 20,62.
2. Mục 2 ADR-0059 đòi kiểm tải theo ADR-0057 §4. Ví dụ nêu PID 26296, lệnh `tl.py --selftest`, không phải MCP: dòng 62–63. Đây là tiến trình phải xét, không được tự dừng.
3. Điều kiện còn lại là `CreationDate` UTC **sau** `09:01:16Z`, theo dòng 35–37. Dòng 63–64 tính `14:03:16Z − 18113 s = 09:01:23Z` và xem đó là giờ khởi động tiến trình. Nếu chấp nhận phép đồng nhất này, điều kiện đúng: **không tiếp nhận**, ghi PID/lệnh vào sổ rồi đợi.
4. Nhưng số đo D10–D11 không cho `CreationDate` hoặc định nghĩa thời lượng theo tuổi PID. Với phản ví dụ `CreationDate=09:01:15Z`, cùng lượt chạy và các số đo vẫn khớp nhưng điều kiện chặn ở bước 3 sai; nếu không có tiến trình khác thoả điều kiện thì ADR-0058 cho tiếp nhận sau kiểm tải và ghi sổ. Với giờ tạo PID `09:01:23Z` thì chặn. Xem finding P2 và phản chứng số học đã chạy.

Kết quả: văn bản **viết ra** “không tiếp nhận”, nhưng chưa chứng minh được kết quả ấy từ số đo theo đúng điều kiện đã định. Ca D10 chưa đạt nghiệm thu chắc chắn; không đánh dấu pass dựa riêng vào câu kết luận của ví dụ.

Các biến thể gần đã đối chiếu:

| Biến thể | Bước/câu chi phối | Kết quả đọc được |
|---|---|---|
| A gia hạn khi chính tiến trình A còn chạy trong thư mục riêng | ADR-0059 dòng 49–51; ADR-0057 §4–5 | Kiểm tải rồi được gia hạn; tiến trình ấy không chặn |
| Dòng bốn trường ADR-0058 còn hạn | ADR-0059 dòng 31–32; ADR-0058 3(a) | Vẫn đọc như cũ; không tự coi thiếu nhịp tim là hết hiệu lực |
| Dòng bốn trường vẫn của A nhưng quá hạn | ADR-0059 dòng 45,49–51,26–30 | Kiểm tải, được gia hạn sang dạng năm trường, giữ UTC bắt đầu |
| Dòng bốn trường của B quá hạn, có Python khởi động sau mốc khoá và không phải MCP | ADR-0058 3(a); ADR-0059 mục 2 | Không tiếp nhận, ghi PID/lệnh rồi đợi |
| B đã tuyên bố bỏ, có tin nhắn/comment của chính B, nhưng Python còn chạy | ADR-0058 dòng 36–40; ADR-0059 dòng 38–39 | 3(c) miễn điều kiện chặn mục 2; vẫn kiểm tải, ghi sổ trước khi thay khoá, không dừng tiến trình |
| A định nhả nhưng dòng đang là B | ADR-0059 mục 5 dẫn mục 4 dòng 45–48 | A không còn giữ khoá; không ghi rỗng dòng B. Nếu sau này lấy lại hợp lệ thì đó là một lần lấy khoá mới |
| A đọc thấy tệp rỗng sau khi kết nối lại | ADR-0059 dòng 46–48 | A không còn giữ khoá; phải kiểm tải rồi lấy mới, không gia hạn trên giả định vẫn sở hữu |
| Chỉ có tiến trình MCP, hoặc giờ tạo Python đúng bằng UTC bắt đầu khoá | ADR-0059 dòng 35–38 | Riêng mục 2 không chặn: văn bản loại MCP và dùng “sau”, không dùng “bằng hoặc sau” |
| Lượt đỏ/bị bỏ nhưng dòng vẫn của chính phiên | ADR-0059 dòng 53–54 | Đọc lại xác nhận chủ khoá, nhả ngay bằng tệp 0 byte |

## Đối chiếu đặc tả và lời khai

| Yêu cầu | Đối chiếu trên candidate |
|---|---|
| Nhịp tim trường thứ năm, ít nhất một lần mỗi 30 phút, hạn ≤ 2 giờ kể từ lần ghi | ADR-0059 dòng 26–32 khớp đặc tả §2; giữ UTC bắt đầu, không thêm điều kiện hết hiệu lực, tương thích dòng bốn trường |
| Kiểm tải, Python khởi động sau UTC bắt đầu, loại MCP, không áp 3(c) | Dòng 33–39 chép đúng phạm vi luật; vấn đề riêng ở lời chứng ví dụ D10 đã báo P2 |
| Lượt bị ngắt, `ngat=co`, bỏ thời lượng khi rà ADR, không tự đổi nguồn/ngủ | Dòng 40–43 khớp đặc tả; ADR-0057 §10 tồn tại ở dòng 48–49; protocol §3.1 dòng 95–97 thực sự có cấm tự đổi power policy |
| Đọc lại, mất sở hữu khi dòng đổi/rỗng, lấy lại theo luật | Dòng 44–52 giữ cả hai ca (i)/(ii), gồm ngoại lệ gia hạn chính mình |
| Nhả khoá 0 byte, cả lượt đỏ/bỏ | Dòng 53–54; áp lại kiểm tra sở hữu ở mục 4 nên không xoá khoá phiên khác |
| Số đo D10–D12 | Cả ba **ô số đo khớp từng byte** với §1 đặc tả; toàn hàng khớp nếu bỏ khác biệt dấu backtick trình bày ở D11. Session, PID, timestamp và `356a27e` đều được giữ nguyên |
| Không cổng cưỡng chế, không chép doctrine vào protocol | ADR-0059 dòng 74–79 khai 0 cổng; sáu tệp cổng ở protocol §20 không khớp chuỗi liên quan khoá/sổ đo. Ba dòng thêm của protocol chỉ định tuyến/phạm vi ADR, không tạo nghĩa vụ mới |
| §20 và §10.2 | Đúng một hàng ADR-0059, cột cổng đúng `không cổng — kỷ luật executor`; hàng ADR-0058 chỉ đổi ô mô tả bằng hậu tố yêu cầu; câu dòng 1015 chỉ bổ sung tên ADR-0059, vẫn trung tính |
| Giữ nguyên các điểm khác | ADR-0057/0058 giống base từng byte. Phạm vi máy, cột sổ đo, cô lập, CI, quyền ghi và cấm dừng tiến trình không bị thay; tính không nguyên tử được giữ rõ |

Đã đối chiếu tham chiếu và độ đủ của bằng chứng:

- ADR-0058 có đúng §3 “Hạn khoá” (dòng 29–40), các nhánh 3(a)/(b)/(c) và thứ tự kiểm tải → ghi sổ → thay khoá. ADR-0057 có §3 Khoá, §4 Kiểm tải, §5 Cô lập và §10 Xem xét lại đúng như các con trỏ của ADR-0059.
- [Comment duyệt 6537481455](https://github.com/ducthangho/tra-luat/pull/1062#issuecomment-6537481455) đã đọc qua GitHub connector: actor `ducthangho`, đúng full spec hash, blob `93f1248aeca8c0d229f0f896434115f246e7b621`, head spec `471ad5391c2bcc1d0ee7871907233313db28e9b6`, r3 g1 và mission `gh-1035`. [Issue #1035](https://github.com/ducthangho/tra-luat/issues/1035) tồn tại, nội dung khai đúng Mission này. Như vậy trạng thái Accepted ở dòng 3–7 có nguồn duyệt khớp, không dựa vào tên nhánh.
- PR #1062 trả head spec đúng `471ad5391c2bcc1d0ee7871907233313db28e9b6`. Bản đặc tả trong ref lease khớp byte với `spec-r3.md`. Probe trên base/master không thấy đường dẫn spec (rc=128) là điều dự kiến, phù hợp câu tìm master trước rồi ref lease ở dòng 6–7. Không dùng hash cũ trong phần mô tả lịch sử của PR làm neo thay comment duyệt/băm đóng băng.
- Git object `356a27e1378b2162bbc0be2ec06ff08fdacbdead` tồn tại, subject thuộc wp1021; base là merge PR #1049, khớp đặc tả. Phần session/timestamp trong bảng được kiểm so với đặc tả đóng băng, **không** tự khai đã đọc sổ đo Windows thực tế. Không có số đo `CreationDate` PID 26296 trong nguồn ADR/đặc tả được giao. Readback PR #1046 trong checkout cũng chỉ xác nhận PID đang chạy; fetch riêng issue-comments #1046 không có comment chứa `26296|18113|CreationDate|09:01:23`.
- Số học D10: khoảng chồng `14:03:16 − 14:01:44 = 92 s` đúng “khoảng 1,5 phút”. D12: `2026-10-31 01:35:00Z − 2026-10-30 21:17:25Z = 15455 s = 4 giờ 17 phút 35 giây`, đúng “hơn 4 giờ”. Phép trừ 18113 s cũng đúng số học; giới hạn suy ra giờ tạo PID là finding duy nhất.

Giới hạn: review thực hiện trên Linux, không chạy Windows local, không đọc trực tiếp `KHOA.txt`/`do-luong.csv` trên ASUS-LAPTOP, không xác nhận CI hoặc quyền merge. Không có verdict trước được cấp nên đây là review độc lập trên candidate, không tự nhận đã hoàn thành bảng đối chiếu từng finding lượt trước. Kết quả cổng dưới đây chỉ chứng minh đúng phạm vi scanner, không đóng finding ngữ nghĩa.

## Đã chạy

Ba cổng chạy với cwd `cay-kho/`, dùng `python3`, môi trường `PYTHONDONTWRITEBYTECODE=1` để không tạo bytecode trong checkout. `core.abbrev=7` đã ghim trước khi chạy. Log stdout/stderr và JSON rc riêng nằm trong `evidence/`; stderr cả ba cổng đều rỗng.

| Lệnh | rc | Kết quả thật |
|---|---:|---|
| `git -C cay-kho config core.abbrev 7` | 0 | stdout rỗng; `git -C cay-kho config --get core.abbrev` rc=0, trả `7` |
| `python3 .claude/dev/packet_loop.py adr-song --root .` | 0 | `adr-song: sạch — 58 ADR trên đĩa, 58 dòng trong §20, khớp 1–1 (tha thiếu trạng thái: ['0016'])` |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine` |
| `python3 scripts/tl.py doc-claims-check --json` | 0 | `ok: true`, `files_scanned: 118`, `flags: []`, `claims_flagged: 381`, `advisory_count: 381`, `layers_skipped: {}`, `strict: false`. Không có flag/advisory thuộc ADR-0059 |

Trạng thái ba cổng: **passed**. `claims_flagged: 381` là trường trả về thật của công cụ, ở lượt này toàn bộ là advisory, không phải 381 flag cứng. Không gọi rc=0 là bằng chứng cho điều kiện `CreationDate` của D10. Log đầy đủ: [adr-song](evidence/adr-song.stdout), [doctrine-scan](evidence/doctrine-scan.stdout), [doc-claims-check JSON](evidence/doc-claims-check.stdout), các tệp `*.result.json` tương ứng có lệnh và rc.

Các lệnh dưới chạy từ thư mục sandbox hiện tại:

| Lệnh | rc | Kết quả thật |
|---|---:|---|
| `git -C cay-kho rev-parse HEAD` | 0 | `b4ccc45dd56284259fb996ac3b3227418bece911` ở cả đầu/cuối |
| `git -C cay-kho rev-parse HEAD^{tree}` | 0 | `2112d1f0d49ee846150623004d92616a1bf87910` ở cả đầu/cuối |
| `git -C cay-kho rev-parse --is-shallow-repository` | 0 | `false` |
| `sha256sum spec-r3.md` | 0 | `f1a666a32161f0607ac27bc8c3be6963bb6367e64f02825635a75cc8185fa973  spec-r3.md` |
| `git -C cay-kho show origin/ops/windows-local-may-chu-kho-r3-lease:ops/specs/WINDOWS-LOCAL-MAY-CHU-KHO-r3.md` qua `sha256sum` | 0 | Cùng SHA-256 trên; đối chiếu byte bằng Python cũng trả `fetched_spec_matches: true` |
| `git -C cay-kho merge-base --is-ancestor adb3d2e977daf9b5623bfc9c7b71b361ecbcf4fc b4ccc45dd56284259fb996ac3b3227418bece911` | 0 | Base là tổ tiên của head |
| `git -C cay-kho diff --numstat adb3d2e977daf9b5623bfc9c7b71b361ecbcf4fc b4ccc45dd56284259fb996ac3b3227418bece911` | 0 | Hai dòng numstat nguyên văn bên dưới |
| `git -C cay-kho diff --check adb3d2e977daf9b5623bfc9c7b71b361ecbcf4fc b4ccc45dd56284259fb996ac3b3227418bece911` | 0 | stdout/stderr rỗng |
| `PYTHONDONTWRITEBYTECODE=1 python3 evidence/kiem-spec.py` | 0 | `files: 2`, `additions: 89`, `deletions: 2`, `exact_write_set: true`, `diff_patch_byte_match: true`, `unchanged_0057_0058: true`; ba ô số đo khớp byte; mọi kiểm tra protocol đều true, đúng một hàng ADR-0059 |
| `PYTHONDONTWRITEBYTECODE=1 python3 evidence/kiem-d10.py` | 0 | `inferred_test_start: 2026-10-30T09:01:23+00:00`, chênh mốc khoá `7.0` s; hai khả năng CreationDate cho điều kiện chặn `true`/`false` |
| `git -C cay-kho cat-file -e adb3d2e977daf9b5623bfc9c7b71b361ecbcf4fc:ops/specs/WINDOWS-LOCAL-MAY-CHU-KHO-r3.md` | 128 | `fatal: path 'ops/specs/WINDOWS-LOCAL-MAY-CHU-KHO-r3.md' does not exist in 'adb3d2e977daf9b5623bfc9c7b71b361ecbcf4fc'`; probe âm dự kiến cho spec chưa có trên master/base, không phải gate thất bại |
| `PYTHONDONTWRITEBYTECODE=1 python3 evidence/kiem-checkout.py` | 0 | `before_files: 8771`, `after_files: 8771`, `content_delta: []`; HEAD/tree đúng, status rỗng, diff worktree/index rc=0 |

Numstat thực tế:

```text
3	2	docs/PROTOCOL_DA_PHIEN.md
86	0	docs/adr/0059-windows-local-nhip-tim-khoa.md
```

Tổng **2 tệp / 89 dòng thêm**, đạt trần **≤ 2 / ≤ 140**. Tập đường dẫn đúng write set của lease; không chạm ADR-0057/0058. Bản diff Git khớp `diff.patch` từng byte. Bằng chứng: [kiểm spec](evidence/spec-audit-final.json), [tham chiếu và băm ADR cũ](evidence/cross-references.json), [phản chứng D10](evidence/kiem-d10.json), [so checkout](evidence/readonly-comparison.json).

Quét cổng đã chạy nguyên văn, rc=1, stdout/stderr rỗng (nghĩa là **không có match**):

```sh
rg -n 'KHOA\.txt|do-luong\.csv|CreationDate|ngat=co' cay-kho/ops/lease_publish.py cay-kho/.claude/dev/packet_loop.py cay-kho/.claude/dev/launcher.py cay-kho/.claude/dev/gate_lifecycle.py cay-kho/.github/workflows/ci.yml cay-kho/.github/workflows/ops-publish-lease.yml
```

Quét lớp suy giờ đã chạy, rc=0; có các dòng D10/D11, quy tắc mục 2, ví dụ dòng 63–64, và các mô tả scanner/thời lượng nêu trong finding:

```sh
rg -n 'CreationDate|18113|09:01:23|26296|khởi động' cay-kho/docs/adr/0057-* cay-kho/docs/adr/0058-* cay-kho/docs/adr/0059-* spec-r3.md
```

Các phép đọc GitHub dùng connector, trạng thái `isError: false` (**không** gán mã thoát shell cho công cụ): `github_fetch_issue_comments(1062)` lọc đúng comment duyệt 6537481455; `github_fetch_issue(1035)`; `github_get_pr_info(1062)`; `github_fetch_issue_comments(1046)` lọc các chuỗi D10 kể trên. Hiện vật: [comment duyệt](evidence/github-authority-6537481455.json), [Mission](evidence/github-mission-1035.json), [PR đặc tả](evidence/github-pr-1062.json), [bộ lọc comment D10](evidence/github-d10-comments.json).

Kiểm checkout đầu/cuối bao gồm băm nội dung tracked, untracked và ignored; `.git` nằm ngoài phép so nội dung này. Cấu hình `core.abbrev=7` là thao tác cấu hình được prompt yêu cầu. So hai mốc chỉ chứng minh không có delta nội dung quan sát được; không chứng minh lịch sử giữa hai mốc hoặc thay cho snapshot bên ngoài của điều phối. Model/effort và receipt launcher thực tế không được tự đo từ trong lượt review này. Windows local và CI: **not_run**. Ba cổng đã yêu cầu: **passed**; ca (i)/(ii): đạt qua đọc từng bước; bằng chứng ca (iii): chưa đạt vì finding P2 còn mở.
