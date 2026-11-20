# KẾ HOẠCH NGUỒN r4 — hợp nhất r2 gốc, r3, nháp PR0 và phản biện Proxima (Mission #1172) — bản sửa 7

## 1. Trạng thái và nguồn

- **Trạng thái: `proposed`.** Chưa duyệt, chưa cài. Băm do phiên điều phối ghi khi đóng băng; chỉ có hiệu lực khi chủ
  kho duyệt băm và một Mission revision cài nó. Cho tới lúc ấy **r3 vẫn là kế hoạch hiện hành** (Mission r81/r82).
- **r4 không xoá r3 và không hồi sinh r2.** r4 = r3 (giữ nguyên tám packet, bất biến I1–I6, chín phương án loại, số nền,
  G1–G6) **cộng** các chốt siết A+1…A+5 cho packet làn A CHƯA mở, **cộng** làn bảo đảm B, **cộng** làn chính sách C có
  điều kiện. Câu nào của r3 không được nhắc ở đây là giữ nguyên.
- **Không hồi tố.** PR1 (#1448, spec `5014de59…`, lease `wp1448-r2-g1-claude`) chạy đúng hợp đồng đóng băng của nó; mọi
  bổ sung của r4 áp từ packet KẾ TIẾP. Không bổ sung nào được nhét vào PR1.
- **Bản sửa 2** xử lý 13 finding của review Codex `wp1172-plan-r4-review-1` (2 P1, 11 P2) trên bản sửa 1 (`76b836fa…`,
  `d5bc154`). **Bản sửa 3** xử lý 6 P2 + 1 P3 của `wp1172-plan-r4-review-2` trên bản sửa 2 (`5a34f1e9…`, `3f3f4ab`);
  **Bản sửa 4** xử lý 1 P1 + 1 P2 của `wp1172-plan-r4-review-3` trên bản sửa 3 (`1082c645…`, `a6f7195`); bản sửa 4
  đã qua review lượt 4 (`wp1172-plan-r4-review-4`, còn 1 P1 R4-19). Bản sửa 5 qua review lượt 5 (2 P1 + 3 P2, cùng một
  lớp: uỷ quyền chủ kho do máy kiểm). **Bản sửa 6 BỎ lớp ấy** thay vì vá tiếp (xem §11) và đã qua review lượt 6
  (`wp1172-plan-r4-review-6`, trên `bf16c5d`, tệp `a7fea4f3…`): còn 1 P1 + 2 P2 + 2 P3 (R4-25…R4-29).
- **Bản sửa 7** xử lý cả năm finding ấy, GIỮ quyết định không có kho uỷ quyền do máy kiểm, và CHƯA được review lại.
  Chủ kho đã quyết định tiếp tục review cho tới khi còn 0 finding P0–P3. Điểm đổi chính: công tắc A+1 trở lại MẶC ĐỊNH
  ĐÓNG (chỉ đúng một chuỗi cho phép mới giảm G5 — r3 I3, r2 §5.5); bên tiêu dùng `kiem-merge` đọc giá trị HIỆN TẠI của
  công tắc, không dùng log cũ; và chỗ nào chỉ là quy trình của người thì được gọi đúng tên là quy trình, kèm rủi ro tồn
  dư để chủ kho quyết (§4 A+1, §5 B3, Q7, Q9).
- **Nguồn (lưu nguyên byte tại `ops/specs/wp1172-source-plan-r4/nguon/`, `.gitattributes` `-text`):**

| Nguồn | sha256 | Vai trò |
|---|---|---|
| r2 gốc `KE_HOACH_TOI_UU_MUTATION_TESTING_r2_2026-11-03.md` (31 028 byte) | `f4611b0f0c79f33d56b293f5fcb854eeeae2fcbb6acbdfd59d6134dcbfbdcb8f` | Khớp `source_plan_status.r2_sha256` của Mission; chủ kho tìm lại và nộp 2026-11-20 |
| Nháp PR0 `PACKET_DRAFT_CI_FULL_AUDIT_PIN_SHA_2026-11-03.md` | `621026692cda1be04d8f1df1a47828d19d01c087dcb484f7c3b2fbf58a900e8e` | Tiêu chí A1–A6 của PR0 |
| Phản biện Proxima `proxima-mutation-policy-review-20261103.txt` | `122fadcab2dbf34303edafc3cd6e93ae08aeba7f3593ce715eeba7ef1d05cec8` | Tư vấn chính sách tổng quát, KHÔNG phải audit kho |
| r3 `ops/specs/wp1172-source-plan-r3/KE_HOACH_NGUON_R3.md` (nhánh `ops/wp1172-plan-r3`@`c032656`) | `2e9fb13f1ab3f299c2d2dc1e5a6e407ff0aadb8aee1f6ffd00d88fc02b146f89` | Xương sống; cài ở r81 (kèm đính chính làm tròn 3,4–5,6 triệu s của r82) |
| BASELINE #1434 `ops/specs/wp1434-r3/do/BASELINE.json` @ `5e5d2cc` | `6100c8e18907f59b1abbdc44195861cc2310c654ce8dcfa2e74ca4ffa155f54c` | Nền số |

## 2. Kế thừa — việc đã làm và nơi nó được dùng tiếp

| Việc | Trạng thái đo được | Dùng tiếp ở r4 |
|---|---|---|
| PR0 #1166 → PR #1412 | accepted rev12 H3 `b79cbf5`; merged `f8b9cdd`; M8 `landed: false` | Nền của làn B. Đối chiếu từng tiêu chí của nháp ở bảng §8.2 — KHÔNG coi là "nháp đã đạt" |
| `ops-do-workflow-definition.yml` (#1094) | trên master | B1/B3 dùng để đo định danh workflow definition, không dựng đường mới |
| Đo nền #1434 | merged `5e5d2cc`; ảnh chụp thô thu lại 2026-11-20 cùng T0/T1 | Nền G1–G6; đầu vào nghiệm thu PR1 mục 5 |
| r3 (4 vòng review Codex) | installed r81 | Làn A |
| PR1 #1448 | leased, đang thực thi lượt 1/3 | Giữ nguyên; bóng 14 ngày của nó là đầu vào PR3/PR4 và phép đo overhead A+5 |
| #1308, #1370, #1393, #1422 | accepted/merged | Sửa vòng đời, admission, biên nhận công bố. KHÔNG tính là tiết kiệm thời gian |
| #1143/#1155, wp892, wp1343/wp1353, WP748 | landed | Tiền lệ và cơ chế mà r3 PR3/PR6 mở rộng; không làm lại |

## 3. Phản biện ba nguồn

**r2.** Đúng: bằng chứng full audit ghim SHA và không bị thay chỗ; tách `cancelled`/`timed_out`/`infrastructure_error`/
`not_run` khỏi đạt; tự kiểm harness bằng lỗi cài cố ý; watchdog ĐỘC LẬP; release kiểm đúng candidate; rollback tức
thời, không chờ PR. Sai theo số đo về sau: r2 coi khoản lớn là full audit và nhắm cắt M9; full audit chỉ 700 504 s = 4,7 %
`[r3 DX-5]`, còn bước G5 trên lượt `ci.yml` là 52,8 % `[B: M2.theo_buoc…G5]`. Mục tiêu "preflight p50 ≤ 2 phút" của r2
không có phép đo nền và là mục tiêu cho MỘT làn mới chưa tồn tại.

**r3.** Đúng: dựng trên số đo; nhắm khoản lớn; giữ M9 (I1); fail-closed ba trạng thái; bóng ≥ 14 ngày trước khi bật.
Thiếu (soạn khi r2 bị coi là mất): watchdog/freshness cho full audit mà I1/I5 dựa vào; cổng release; quy trình audit đỏ;
rollback của PR3/PR6 cần một PR; điều kiện bật PR3 không có lỗi cài cố ý; kết cục không có tầng thực thi tường minh;
không đo RSS và overhead.

**Proxima.** Chỉ dùng làm danh mục kiểm. Bốn điểm chưa có trong r3: audit dở không bao giờ xanh + cảnh báo quá hạn; tự
kiểm harness; release gate; đo cả lỗi BỎ SÓT bằng holdout/seeded. Proxima cũng nói "audit tuần không thay được kiểm chứng
tại thời điểm merge" — ủng hộ I1 của r3.

**Xung đột duy nhất:** r2 PR8 (M9 theo rủi ro) ↔ r3 §6 phương án loại 3. Giải: giữ I1 mặc định; phần của r2 thành làn C
hai cửa (Q8a cho NGHIÊN CỨU, Q8b cho ĐỔI M9 chỉ sau kết quả C1).

## 4. Làn A — giảm chi phí (r3) + năm chốt siết

PR1 → PR2 → PR3 → PR4 → PR5 → PR6 → PR7 → PR8 đúng r3 §5. Năm chốt áp vào đặc tả packet tương ứng khi tới lượt.

**Không có kho uỷ quyền do máy kiểm.** Ba lượt review (R4-08 → R4-19 → R4-20…R4-24) cho thấy mọi cách để máy chứng minh
"chủ kho đã cấp quyền" (biến có thế hệ, comment, tệp git do chủ kho merge) đều mở thêm lỗ, vì quy tắc thường trực "chủ kho
bấm mọi merge" làm `merged_by` mất nghĩa cấp quyền. r4 vì vậy chỉ dựa vào hai thứ có thẩm quyền rõ ràng: (1) **quyền quản
lý biến Actions** của kho (đo tập chủ thể VÀ credential ghi được); (2) **mã đã merge qua review** như mọi thay đổi cổng
khác. Giảm G5 cần CẢ HAI cùng lúc (A+1); thiếu một ⇒ chạy đủ. Giá trị biến không tự nới được gì: nó chỉ cho phép phần
giảm mà mã đã merge định nghĩa, và mọi trạng thái khác của nó đều dẫn về đủ. Máy KHÔNG chứng minh được người nào đã
quyết định đặt biến; phần ấy là quy trình của chủ kho, khai là rủi ro tồn dư ở Q9, không trình bày như một chốt.

- **A+1 (PR3, PR6, C2) — công tắc CHO PHÉP, mặc định ĐÓNG (đúng r3 I3 và r2 §5.5).**
  - **Hai khoá, phải có cả hai.** Một lượt chỉ được giảm khi ĐỒNG THỜI: (a) mã của lớp giảm ấy đã merge qua review; (b)
    Actions repository variable mức kho CỦA LỚP ẤY mang ĐÚNG MỘT chuỗi cho phép (ký hiệu chung `CHO_PHEP`), so khớp từng
    byte, không cắt khoảng trắng, không đổi hoa thường. Có ba lớp giảm — bỏ mới (PR3), chế độ đích (PR6), M9 theo rủi ro
    (C2) — mỗi lớp một biến và một chuỗi RIÊNG: B4 đóng băng cặp tên/chuỗi của PR3 và của PR6 (để PR6 không phải sửa
    `kiem-merge`), đặc tả C2 thêm cặp của nó. Đặt `CHO_PHEP` cho lớp này không bật lớp khác; mã PR6 merge khi biến của
    nó chưa mang chuỗi thì PR6 vẫn chạy đủ. Mọi trạng thái khác của biến ⇒ **KHÔNG giảm** cho lớp ấy: biến vắng (ngữ
    cảnh `vars` khi ấy trả chuỗi rỗng), rỗng, sai một ký tự, giá trị lạ, không đọc được, phản hồi sai lược đồ. Biến chưa
    từng được tạo cũng là KHÔNG giảm, nên "bật" một lớp gồm hai việc tách rời: merge mã (với PR3: năm điều kiện bật của
    r3 cùng A+2 và A+5 giữ nguyên, kiểm trong PR), rồi chủ kho đặt `CHO_PHEP` của lớp ấy.
  - **KHÔNG giảm nghĩa là gì (đính chính phạm vi của bản sửa 6).** Lớp nào KHÔNG giảm thì phần giảm MỚI của lớp ấy tắt
    và cổng về đúng luật hôm nay: PR3 ⇒ `cong_cu=chay`; PR6 ⇒ chế độ đủ; C2 ⇒ full M9 theo K7 hiện hành. Ngoại lệ
    `duong_nhanh` ĐANG CÓ (wp892, #674; r3 I5(a)) không bị thu hồi: nó có chốt fail-closed riêng bằng đúng chuỗi
    `duong_nhanh` và không phải thứ r4 thêm vào. Bản sửa 6 viết "`FULL` ⇒ mọi lượt PR chạy G5 đủ, bất kể bộ phân loại
    nói gì"; câu ấy rộng hơn cả r2 §5.5 (tắt targeted approval ⇒ PR thuộc vùng M9 đòi full) lẫn r3 (PR3: công tắc cho bộ
    phân loại luôn trả `chay`; PR6: đưa PR về chế độ đủ). Nếu giữ câu ấy khi KHÔNG giảm đã là trạng thái MẶC ĐỊNH thì từ
    lúc B4 land mọi PR hồ sơ phải có 8 mảnh G5 trước merge (ước ≈ 3,9 triệu s/30 ngày, §13), và máy chạy `kiem-merge`
    nào không đọc được biến sẽ đòi G5 đủ cho cả PR hồ sơ. Câu ấy được RÚT; phương án rộng ghi ở §12 (16) và chủ kho xác
    nhận phạm vi ở Q9(c). Nhu cầu "buộc đủ bất kể bộ phân loại nói gì" giữ ở mức TỪNG PR bằng cờ siết của `kiem-merge`
    (dưới).
  - **Bên tiêu dùng có thẩm quyền, và nó xét trạng thái HIỆN TẠI.** Thẩm quyền không nằm ở job trong cây PR (trên
    `pull_request`, PR sửa được chính `ci.yml` hay bộ phân loại) mà ở cổng merge chạy từ cây TIN CẬY: `kiem-merge`, chạy
    từ bản `origin/master` đã fetch, không từ head PR. B4 thêm hai phép tự kiểm chống chạy NHẦM cây: tệp `kiem-merge`
    đang chạy phải trùng blob của nó tại `origin/master`, và `origin/master` cục bộ phải trùng đầu `master` đọc sống
    bằng `git ls-remote`; lệch ⇒ từ chối. Hai phép ấy bắt sai sót, không chống được người cố ý sửa công cụ. Ở mỗi lượt
    xét merge: bằng chứng trên H có G5 đủ `success` (8 mảnh + job gom, chế độ đủ) ⇒ phần này đạt, không cần đọc công
    tắc. Bằng chứng KHÔNG có G5 đủ ⇒ chỉ được chấp nhận trong đúng hai trường hợp, cả hai TÍNH LẠI từ diff bằng bộ phân
    loại của mã trên master, không lấy từ output của lượt PR: (α) mã master xếp PR vào ngoại lệ `duong_nhanh` đang có
    (tập PR được hưởng không đổi, không liên quan công tắc); (β) mã master xếp PR vào một lớp giảm mới (PR3: diff ngoài
    bao đóng; PR6: diff trọn trong vùng K7 và đã có audit đủ trên H) VÀ công tắc của lớp ấy, do chính `kiem-merge` đọc
    SỐNG trong lượt gọi ấy, đúng `CHO_PHEP`. Ngoài hai trường hợp ấy ⇒ đỏ, bất kể job PR nói gì. Không tính lại được (bộ
    phân loại của master không chạy được, đầu ra lạ) ⇒ không có (α) lẫn (β) ⇒ đỏ. Nhờ thế một PR sửa chính bộ phân loại
    không tự xếp được mình vào làn nhẹ ở cổng merge.
  - **Đọc sống nghĩa là gì.** Trong chính lượt gọi, `kiem-merge` gửi một lời GET tới REST biến mức kho
    (`/repos/<kho>/actions/variables/<tên>`), giống cách K0 hôm nay đọc sống head PR bằng `git ls-remote`. Giá trị dùng
    để CHO GIẢM không bao giờ lấy từ tham số, tệp readback do người gọi đưa, bộ đệm, hay log CI; `kiem-merge` không giữ
    trạng thái giữa các lượt gọi. Lời đọc chỉ tính là đọc được khi có dấu hiệu dương: HTTP 200 kèm header `X-GitHub-*`
    (proxy của phiên có thể tự trả 200 không phải từ GitHub — CLAUDE.md §Gọi agent đa nền), thân JSON mang đúng tên biến
    và `value` kiểu chuỗi. Bị từ chối (401/403/404), hết giờ, 200 mà thân lạ hay rỗng, JSON hỏng ⇒ không đọc được ⇒
    KHÔNG giảm. Quyết định vì thế chỉ phụ thuộc trạng thái hiện tại (công tắc đọc sống + mã master) và bằng chứng trên
    H; lịch sử giá trị công tắc không tham gia. Bản sửa 6 cho log job của lượt CI trên H làm nguồn dự phòng khi REST
    không đọc được — RÚT (R4-25; §12 (17)): một log cũ đúng từng byte vẫn không nói được giá trị hiện tại. Job CI vẫn IN
    giá trị nó thấy, chỉ để truy vết.
  - **Trong CI (gợi ý, không phải thẩm quyền).** `chuan-bi` đọc ngữ cảnh `vars`; biến của lớp nào đúng `CHO_PHEP` thì bộ
    phân loại mới được xuất quyết định giảm của lớp ấy; rỗng, lạ, vắng ⇒ `chay`. Đọc `vars` trong `ci.yml` không trao
    quyền gì cho tác giả PR: họ thấy giá trị (không bí mật) và có thể sửa `ci.yml` của chính PR để lờ nó đi, nhưng diff
    ấy chạm bao đóng nên `kiem-merge` không nhận trường hợp (β). Không dùng `pull_request_target` chạy mã PR.
  - **Giá phải trả về tính sẵn sàng (nói trước).** Máy chạy `kiem-merge` không đọc được biến ⇒ mọi PR thuộc trường hợp
    (β) bị đòi một lượt G5 đủ trên H cuối trước merge; lợi ích của PR3/PR6 khi ấy chỉ còn ở các lần đẩy trung gian. Lối
    ra chỉ có hai: cấp cho máy ấy quyền CHỈ ĐỌC biến (Variables: read), hoặc chủ kho chấp nhận mất phần lợi ích đó
    (Q9(b)). Khả năng đọc phải được đo trên TỪNG máy sẽ chạy `kiem-merge` TRƯỚC khi đóng băng đặc tả B4. Phép tính lại
    (α) là điều kiện MỚI ở cổng merge cho PR hồ sơ (hôm nay chỉ có K2): bộ phân loại của master không chạy được trên máy
    ấy ⇒ PR hồ sơ cũng chờ; tỷ lệ chạy được trên các PR hồ sơ gần đây cũng phải đo trước khi đóng băng.
  - **Khoảng hở còn lại giữa lúc đọc và lúc merge.** r4 không dựng cổng nào phía máy chủ đọc biến tại đúng lúc merge:
    chủ kho bấm merge sau khi `kiem-merge` xanh — đây là mô hình K0–K7 hiện hành, r4 không đổi. `kiem-merge` in thời
    điểm đọc, giá trị và `updated_at` của biến (dấu vết, KHÔNG phải vị từ). Runbook: `kiem-merge` là bước cuối trước khi
    đề nghị merge; phán quyết chỉ dùng trong một cửa sổ ngắn (đề xuất 30 phút; đặc tả B4 chốt), quá thì chạy lại; ai đổi
    công tắc thì mọi phán quyết xanh đang chờ merge coi như hết hiệu lực. Cửa sổ ấy là QUY TRÌNH, máy không cưỡng chế
    (Q9(d)). Lớp bù không đổi: lượt push của merge commit là `day_du` và chạy G5 đủ (r3 I5; điều kiện bật (4) của PR3) —
    phát hiện SAU merge, không ngăn trước merge.
  - **Ai đặt được `CHO_PHEP`.** Tập W = mọi chủ thể VÀ credential ghi được biến mức kho. Giả thuyết "kho cá nhân thì chỉ
    chủ kho" của các bản trước KHÔNG được coi là đúng: verdict lượt 6 dẫn tài liệu GitHub rằng cộng tác viên của kho
    cũng tạo được biến, và credential mang Variables:write là một đường ghi khác. W được liệt kê bằng phép ĐO trong bước
    chuẩn bị đặc tả B4 (trước Q9), không suy từ quyền sở hữu kho: cộng tác viên và vai trò; GitHub App đã cài và quyền
    của từng App; các token đang dùng được, gồm token GitHub thật có trong môi trường phiên AI và trên máy deploy (quyền
    của chúng với biến: CHƯA ĐO) và `GITHUB_TOKEN` của workflow. Phần liệt kê cần quyền quản trị thì chủ kho tự chạy.
    Chủ kho xác nhận W ở Q9(a) và thu hẹp tới mức làm được. Bất kỳ thành viên nào của W cũng đặt được `CHO_PHEP`; máy
    không phân biệt lần đặt do chủ kho quyết với lần ghi của người hay credential khác. Chưa đo xong W, hoặc W còn thành
    viên chủ kho không chấp nhận ⇒ không đặt `CHO_PHEP`; PR3/PR6 nằm im ở chạy đủ.
  - **Đóng ngay, không chờ PR; bật lại là QUY TRÌNH của chủ kho (r2 §5.5).** Đóng một lớp = xoá biến của lớp ấy hoặc đặt
    bất kỳ giá trị nào khác `CHO_PHEP`; có hiệu lực ở lượt CI kế tiếp và ở lần `kiem-merge` kế tiếp, không cần merge gì.
    Runbook công tắc (tài liệu dev-side, write set B4) ghi: (1) điều kiện phải đóng ngay, lấy từ r2 §5.5: lỗi P0/P1 lọt
    qua một lượt giảm; bộ phân loại hoặc job gom kết luận sai; release dùng sai H; watchdog B2 báo `stale_or_missing`;
    cộng audit đỏ chưa khoanh được vùng (B3) — không khoanh được sự cố thuộc lớp nào thì đóng MỌI lớp; (2) sau khi đóng:
    đọc lại giá trị (readback) và ghi vào Issue sự cố; (3) điều kiện BẬT LẠI: điều tra có kết luận ghi trong Issue sự
    cố; full audit (`ci-dot-bien-du.yml`) `success` trên các H bị ảnh hưởng đã khoanh trong Issue ấy và trên đầu
    `master` lúc bật lại — khi full audit chưa mang G5 (trước PR5) thì kèm G5 đủ `success` trên chính các H ấy; và quyết
    định mới bằng văn bản của chủ kho; (4) phiên AI không ghi biến công tắc. Cả bốn mục là quy trình có người: KHÔNG
    cổng nào kiểm rằng (3) đã xong trước khi `CHO_PHEP` xuất hiện lại. Với (4), r4 không hứa luật hook nào: hook
    PreToolUse hiện chỉ HỎI LẠI khi lệnh `Bash` của Claude Code là `gh api` với phương thức ghi, không bắt `gh variable`
    hay lời gọi HTTP trực tiếp — mà đó mới là đường ghi thực tế của một phiên không có `gh`. Watchdog B2 không tự ghi
    biến (không workflow nào được cấp Variables:write). Tất cả là rủi ro tồn dư chủ kho chấp nhận ở Q9(d).
  - **Siết không cần quyền ghi biến.** `kiem-merge` có một cờ siết: đòi G5 đủ `success` trên đúng H cho PR đang xét, bất
    kể công tắc và bộ phân loại nói gì (tắt cả (α) lẫn (β)). Ai chạy `kiem-merge` cũng dùng được, vì siết không cần thẩm
    quyền; điều phối dùng nó khi có sự cố rồi báo chủ kho đóng công tắc. PR thiếu bằng chứng đủ thì CHỜ tới khi có một
    lượt `ci.yml` trên đúng H chạy G5 đủ `success`. Cách tạo lượt ấy cho từng loại PR (đóng rồi mở lại PR sau khi công
    tắc đã đóng; dispatch `che_do=day_du` cho PR `duong_nhanh`, vốn kéo theo job Windows) do đặc tả B4 chốt từ phép đo
    (iv) dưới đây, không được ngầm phá quy tắc không Windows CI.
  - **Packet B4 — công tắc cho phép và bên tiêu dùng tin cậy** (sensitive; sau Q9; land TRƯỚC PR3). Mã tiêu dùng tin cậy
    KHÔNG nằm trong write set r3 của PR3/PR6. Write set dự kiến (đo lại trước lease): `.claude/dev/packet_loop.py`,
    `.claude/dev/packet_loop_test.py` (và tệp chia mảnh của bộ test nếu trọng số phải đổi), runbook công tắc (tài liệu
    dev-side mới; nếu `docs/PROTOCOL_DA_PHIEN.md` hoặc adapter `land-packets` phải trỏ tới nó thì các tệp ấy vào write
    set), đặc tả. Phần đọc `vars` ở `chuan-bi` và truyền cho bộ phân loại KHÔNG thuộc B4: nó nằm trong write set r3 của
    PR3 (`.github/workflows/ci.yml`, `ops/ci_duong_nhanh.py` + test), PR6 dùng lại; ca ba trạng thái và đột biến "rỗng
    hoặc lạ ⇒ giảm" của phía CI thuộc năm phép chứng minh của PR3. B4 land khi master chưa có bao đóng, nên `kiem-merge`
    gọi bộ phân loại của master qua điểm vào sẵn có của `ops/ci_duong_nhanh.py` (B4 không sửa tệp này): đầu ra thiếu
    quyết định giảm ⇒ không có trường hợp (β); lời gọi lỗi hoặc đầu ra lạ ⇒ không có cả (α) lẫn (β). B4 đóng băng luôn
    hai hợp đồng mà PR3 và PR6 phải theo trong write set của chính chúng: đầu ra của bộ phân loại (giá trị nào thuộc lớp
    giảm nào; giá trị ngoài hợp đồng là "lạ"), và cách `kiem-merge` nhận biết chế độ THỰC CHẠY của lượt trên H (đủ,
    đích, bỏ) từ bằng chứng job gom để lại — không đọc được chế độ thì coi như KHÔNG có G5 đủ. Trước PR3 vì vậy mọi PR
    không `duong_nhanh` vẫn bị đòi G5 đủ, đúng hiện trạng.
  - **Đo TRƯỚC khi đóng băng đặc tả B4 (bước chuẩn bị, trước Q9; chỉ đọc, trừ biến thử do chủ kho tự đặt):** (i) tập W;
    (ii) từ từng máy sẽ chạy `kiem-merge`: đọc được biến không, và sau khi chủ kho đổi giá trị thì lần đọc kế tiếp có ra
    đúng giá trị mới không (không dính bản đệm) — đo trên một biến THỬ, tên và giá trị không dùng lại cho công tắc thật,
    xong thì xoá; (iii) API trả gì cho giá trị có khoảng trắng hay xuống dòng ở đầu và cuối; (iv) lượt chạy lại (re-run)
    và lượt mở lại PR có đọc lại `vars` không; (v) `vars` ở `chuan-bi` đúng là biến mức kho, không bị biến mức
    environment che; (vi) `kiem-merge` chạy được bộ phân loại của master cho các PR hồ sơ gần đây không. Mục nào không
    đo được ⇒ ghi `khong_do_duoc` và thiết kế theo nhánh bảo thủ.
  - **Nghiệm thu B4** (đồ giả REST phải GIỮ trạng thái, đổi được giá trị giữa hai lần đọc; không diễn kịch bản). Fixture
    chính: một PR thuộc trường hợp (β) mà bằng chứng trên H là lượt giảm đã xanh, KHÔNG có G5 đủ. Trên fixture ấy: đúng
    `CHO_PHEP` ⇒ đạt; rồi đổi sang giá trị khác, xoá biến, để rỗng, sai một ký tự, khác hoa thường, thừa khoảng trắng ⇒
    đỏ vì thiếu G5 đủ; REST bị từ chối, hết giờ, 200 thân lạ, 200 thiếu header GitHub, JSON hỏng ⇒ đỏ; log CI cũ in
    `CHO_PHEP` trong khi giá trị hiện tại khác hoặc không đọc được ⇒ đỏ (ca của R4-25); chạy lại ở tiến trình mới ⇒ cùng
    kết quả; tham số hay tệp do người gọi đưa không làm nới được; PR sửa `ci.yml` hoặc bộ phân loại để lờ công tắc ⇒ đỏ;
    cờ siết ⇒ đỏ dù đang `CHO_PHEP`; lời gọi bộ phân loại lỗi ⇒ đỏ; chạy từ cây có `packet_loop.py` khác blob master,
    hoặc `origin/master` cục bộ đã cũ ⇒ từ chối; `CHO_PHEP` của lớp KHÁC (biến PR3 bật, PR thuộc lớp PR6) ⇒ đỏ; đóng rồi
    đặt lại đúng `CHO_PHEP` ⇒ đạt trở lại (máy cố ý không nhớ lịch sử: điều kiện bật lại sau sự cố nằm ở runbook, không
    ở mã). Đối chứng: cùng PR nhưng bằng chứng CÓ G5 đủ ⇒ đạt ở mọi trạng thái công tắc, kể cả REST lỗi; PR mà mã master
    xếp `duong_nhanh` ⇒ đạt như trước B4; lượt PR tự xếp `duong_nhanh` trong khi mã master không xếp thế ⇒ đỏ. Mỗi chốt
    một đột biến RIÊNG phải làm đúng ca đích đỏ: "giá trị lạ ⇒ giảm", "không đọc được ⇒ giảm", "so khớp bỏ hoa thường
    hoặc cắt khoảng trắng", "REST lỗi thì lấy log", "bỏ tính lại bằng mã master", "đọc nhầm biến của lớp khác", "bỏ tự
    kiểm cây", "bỏ cờ siết". Phần quy trình (đóng, bật lại, cửa sổ merge) không có ca máy; nghiệm thu của nó là runbook
    được chủ kho duyệt.
- **A+2 (điều kiện bật PR3 thứ sáu) — lỗi cài cố ý.** Tập lỗi KHÓA TRƯỚC bởi oracle độc lập (không do bộ phân loại sinh),
  mỗi lỗi ở một thành phần bao đóng (`ops/` thường, `.claude/dev/`, `scripts/*.py`, `.github/`, cấu hình gốc, tệp đọc qua
  object git) ⇒ bóng phải `chay` cho 100 %. Cộng các PR lịch sử trong cohort có G5 đỏ không do hạ tầng (ghi đúng số tìm
  được; tìm được 0 thì ghi 0, không bịa) ⇒ bóng `chay`.
- **A+3 (PR2, PR5, B1) — kết cục theo tầng, không gộp.** Bốn trường tách biệt:
  `trang_thai_thuc_thi` ∈ {`hoan_tat`, `timed_out`, `infrastructure_error`, `cancelled`, `not_run`} ·
  `quan_sat_ca` (mỗi ca: `passed`/`failed`) · `phan_hang_dot_bien` ∈ {`giet`, `song`, `tin_dung_gia`,
  `equivalent_reviewed` (bắt buộc `ly_do` + `nguoi_xac_nhan`; không bao giờ đếm là giết)} · `ket_luan_tong` ∈ {`xanh`,
  `do`, `khong_ket_luan`}. Luật: `ket_luan_tong = xanh` chỉ khi mọi mục `hoan_tat`, ca nền `passed`, và mọi đột biến
  được phân hạng theo đúng bộ phân hạng hiện có (I2, không đổi); ca KHÔNG phải đích sống sót là bình thường, không làm
  đỏ. Fixture bắt buộc: nền khoẻ · ca không đích sống · giết đúng đích · tín dụng giả · tương đương có xét duyệt ·
  timeout/hạ tầng. Kiểm hai chiều: bên đọc cũ vẫn đọc được; số giết không đổi trên cùng SHA.
- **A+4 (PR7b) — bộ nhớ.** RSS đỉnh theo TỪNG tiến trình con bằng `os.wait4` (rusage riêng của con vừa thu, đơn vị KiB
  trên Linux, gồm cháu đã được con thu); nhu cầu ĐỒNG THỜI đo riêng qua cgroup (`memory.peak`) khi có. Không có ⇒
  `khong_do_duoc`. Không dùng `RUSAGE_CHILDREN` (giữ mức cao nhất qua các con đã thu). Ca: con tuần tự khác cỡ, con
  chồng nhau.
- **A+5 (điều kiện bật PR3 thứ bảy) — overhead của phần đo PR1.** Đo GHÉP CẶP bật/tắt trên CÙNG ảnh chụp bất biến (sản
  phẩm, test, đột biến, môi trường), hai vế của mỗi cặp chạy xen kẽ; cần một công tắc môi trường tắt phần đo — thêm
  trong write set của PR3 (`ops/cong_cu_test.py`), không sửa PR1. Ca kiểm có overhead nhân tạo biết trước.
  - **Một hợp đồng lặp duy nhất.** Cả 8 mảnh, MỖI mảnh ≥ 3 cặp ⇒ tối thiểu 8 × 3 = 24 cặp = 48 lượt mảnh. Mức "≥ 5 cặp
    trên một mảnh" của bản sửa 3 đã bị mức này THAY và không còn hiệu lực. Đặc tả PR3 được tăng số cặp (tăng đều cho cả
    8 mảnh), không được giảm.
  - **Ước lượng.** Theo mảnh: trung vị hiệu ghép cặp. Toàn cục: tổng trung vị hiệu ghép cặp của 8 mảnh / tổng trung vị
    thời gian bản tắt của 8 mảnh (tức có trọng số theo thời gian từng mảnh); kèm ca kiểm "mảnh không đồng nhất"
    (overhead tập trung ở một mảnh).
  - **Ngân sách — ƯỚC LƯỢNG, chưa đo.** Đo trong môi trường đo cố định (container), không dùng lượt CI thêm. Thời lượng
    một lượt mảnh trong môi trường ấy CHƯA ĐO; con số "≈ 10 giờ máy" của các bản trước không có phép đo nào đỡ và được
    RÚT. Mốc tham khảo duy nhất có nguồn là trung vị bước G5 trên runner CI, 1057 s `[B: M2.theo_buoc…G5]`: NẾU
    container chạy ngang runner CI (giả định chưa kiểm) thì 48 lượt ≈ 48 × 1057 = 50 736 s ≈ 14,1 giờ máy. Trước khi
    đóng băng đặc tả PR3: chạy mỗi mảnh MỘT lượt trong đúng môi trường đo (8 lượt, bản trên master sau PR1, không ghép
    cặp, KHÔNG dùng làm số liệu overhead; cùng giả định ≈ 8 456 s ≈ 2,3 giờ) rồi thay giả định bằng số đo ấy. Tổng 48 +
    8 = 56 lượt mảnh, tính vào ngân sách của PR3.
  - **Kết luận.** Đo không đủ 8 mảnh thì chỉ báo mảnh đã đo và ngưỡng toàn cục là `khong_do_duoc` ⇒ điều kiện bật thứ
    bảy CHƯA đạt. Overhead ≤ 5 % ⇒ giữ; > 5 % ⇒ chuyển phần đo sang lấy mẫu ngoài cổng, không xoá tín hiệu (r2 §5.1). So
    sánh trước/sau theo cohort 14 ngày chỉ là giám sát vận hành, KHÔNG phải phép đo overhead.

## 5. Làn B — bảo đảm bằng chứng (không đổi quyết định cổng `ci.yml`, không nới M9)

### B1 — Hợp đồng biên nhận full audit (bên sản xuất) + canary A3 + A4

- **Hợp đồng `bien_nhan_audit.v1` (đóng băng TRƯỚC B2/B3).** Trường: kho; đường dẫn workflow; định danh definition
  (`github.workflow_sha` + blob/sha256 của tệp tại OID ấy, hoặc `not_measured`); sự kiện; khung cron (nếu `schedule`);
  SHA sự kiện; SHA/tree checkout từng job; run_id, attempt của lượt và attempt của TỪNG bên sản xuất mảnh (giữ dòng
  chạy-lại-mảnh đang được phép từ PR0, không cấm cũng không tin mù); danh sách job/mục KỲ VỌNG lập độc lập từ mã tại
  SHA ấy và tập thực có; kết luận cuối từng job; artifact id + digest; Python/OS/digest phụ thuộc (`requirements*.txt`,
  phiên bản công cụ); kết cục theo A+3; giây và bộ nhớ từng mảnh; dấu hiệu dương.
- **A3 — canary concurrency.** Hai `workflow_dispatch` khác run_id trên CÙNG SHA, chồng thời gian ⇒ HAI biên nhận audit
  hoàn tất, không lượt nào `cancelled` vì concurrency; cộng một quan sát RIÊNG: một lượt push `ci.yml` chạy trong lúc ấy
  (ghi run_id, queue/start/end, số job chạy thật) không huỷ lượt audit nào. Push không kích hoạt `ci-dot-bien-du.yml`;
  không thêm trigger push. (Muốn ba lượt audit thì phải là dispatch thứ ba, tính vào ngân sách.)
- **A4.** Gọi `ops-do-workflow-definition.yml` cho mỗi lượt canary; hợp đồng cho phép `not_measured` ở bên sản xuất, nhưng
  bên tiêu dùng B3 thì không (xem B3).
- Write set: `.github/workflows/ci-dot-bien-du.yml`, `.claude/dev/ci_dang_ky_test.py`, đặc tả mới. Trước PR5 (cùng write set).

### B2 — Watchdog freshness (bên tiêu dùng đọc báo cáo)

- Workflow MỚI, lịch riêng **mỗi 6 giờ** + `workflow_dispatch`; quyền: đọc Actions, ghi Issue. Đọc REST (phân trang có
  giới hạn) các lượt `ci-dot-bien-du.yml`, kiểm biên nhận B1 theo hợp đồng v1.
- Ba trạng thái như r2 §4: `fresh` · `due_in_progress` · `stale_or_missing`. Tuổi tính từ khung/snapshot gốc; chạy lại
  cùng SHA cũ KHÔNG làm mới. Đọc API lỗi ⇒ `khong_do_duoc` (không bao giờ thành `fresh`).
- `stale_or_missing` hoặc `khong_do_duoc` ⇒ mở/cập nhật MỘT Issue theo dõi rồi ĐỌC LẠI Issue; ghi Issue lỗi ⇒ job đỏ.
  Job đỏ KHÔNG đồng nghĩa chủ kho đã nhận tin (định tuyến thông báo phụ thuộc người kích hoạt lịch và cài đặt). Điều kiện
  bật B2: chủ kho theo dõi (subscribe) Issue theo dõi và một lần thử giao tin thật được xác nhận; chưa xác nhận ⇒ kênh
  giao tin ghi `chua_do`.
- Nhịp tim: mỗi lượt watchdog ghi dấu thời gian lên Issue theo dõi; lượt kế tiếp và B3 đọc dấu ấy và báo khi cũ hơn 24
  giờ; phiên điều phối kiểm nó bằng TAY ở đầu mỗi phiên theo một runbook dev-side (không sửa `doctor`). Đây là giám sát
  chéo, không phải SLA cứng (cùng chịu rủi ro lịch GitHub).
- Báo cáo hiện cả SHA đầu `master` hiện tại, SHA đã audit và khoảng cách giữa hai bên; không bao giờ ghi "master hiện tại
  đã đủ" khi hai SHA khác nhau (r2 §4).
- **G7 phát biểu đúng phạm vi:** cảnh báo trong ≤ khung + 36 h + 6 h (chu kỳ) + độ trễ lịch đã khai; là best-effort có
  giám sát chéo, chủ kho chấp nhận ở Q6.
- **Thứ tự:** SAU B1 (cần hợp đồng v1). Ban đầu chỉ báo cáo, không chặn merge.
- Write set: workflow mới, script `ops/` mới + test, VÀ `.claude/dev/ci_dang_ky_test.py` (đăng ký bộ test mới vào
  registry theo đường thông thường) — nên xếp nối tiếp với B1/PR2. Ca: biên thời gian, khung vắng, chạy lại SHA cũ, API
  bị từ chối, ghi Issue lỗi, lượt watchdog vắng.

### B3 — Cổng release đúng candidate + quy trình audit đỏ

- **"Release"** = đẩy Package (`scripts/deploy-package.sh --push`, `scripts/deploy-package.ps1 -Push`).
- **Ràng buộc byte:** trước khi build, ghi H và tree; đòi cây sạch (không tệp theo dõi bị sửa, không tệp chưa theo dõi
  lọt vào tập phát hành; tệp trạng thái deploy bị ignore được phép nhưng không vào gói); build từ ảnh chụp đã kiểm của H
  (ví dụ `git archive H`) HOẶC so tập tệp + byte phát hành với blob tại H; tính digest gói và GẮN vào bằng chứng; ngay
  trước `drive-push` kiểm lại H, tree, digest.
- **Ref phát hành và CI bắt buộc:** ref phát hành = `master`. Trạng thái bảo vệ của `master` (cấm force-push/xoá, ai
  vượt được) là ĐIỀU KIỆN TIÊN QUYẾT đo một lần lúc bật B3 bằng quyền quản trị của chủ kho, ghi hồ sơ, đo lại theo
  runbook hằng tháng; B3 KHÔNG đọc nó lúc deploy (token chỉ đọc không đủ quyền), và rủi ro trôi cấu hình giữa hai lần đo
  là rủi ro tồn dư chủ kho chấp nhận ở Q7. H phải là commit trên `master` (bằng đầu nhánh hoặc tổ tiên của nó, đo bằng git trên bản
  sao đủ lịch sử); mọi check bắt buộc của lượt push `ci.yml` trên đúng H phải `success` (đọc REST, nguồn gốc khớp). "Không
  tụt sau master" KHÔNG đồng nghĩa "được phép phát hành". Ca: H sạch, đi trước master, audit xanh nhưng một check bắt
  buộc đỏ/vắng ⇒ chặn; ref di chuyển giữa lúc kiểm và lúc đẩy ⇒ chặn.
- **Kiểm biên nhận (bên tiêu dùng B1 v1):** đúng kho, đúng workflow, definition ĐO ĐƯỢC (khi biên nhận ghi `not_measured`:
  một người vận hành được uỷ quyền chạy A4 TRƯỚC cho đúng lượt ấy; B3 chỉ ĐỌC artifact A4 bằng quyền chỉ đọc; artifact vắng,
  cũ, GraphQL null hoặc hết giờ ⇒ chặn, không hạ xuống cảnh báo sau khi chế độ chặn đã bật), SHA = H, mọi job kỳ vọng có mặt và `success`, kết cục `xanh`, artifact digest khớp, dòng
  attempt hợp lệ. Bất kỳ trường bắt buộc nào vắng/lạ/không đọc được ⇒ chặn.
- **Xác thực trên máy deploy — bảng năng lực:** B3 chỉ gọi: danh sách lượt + job + artifact của workflow (Actions:
  read), check run của commit (Checks: read), nội dung/so sánh commit (Contents: read). Không cần quyền PR metadata, bảo
  vệ nhánh, biến hay dispatch. Đo TỪNG endpoint từ CẢ HAI máy deploy (403/404, phân trang thiếu, chuyển hướng artifact)
  trước khi bật chế độ chặn; chưa đo ⇒ `warning_only`, ghi rõ; sau khi bật chặn, mọi lỗi đọc ⇒ chặn.
- **Không có ngoại lệ do máy cấp.** Thiếu biên nhận audit trên H ⇒ đường bình thường là chạy full audit trên H (dispatch
  bởi người có quyền) rồi deploy. Trường hợp khẩn cấp: CHỈ chủ kho, tự tay chạy deploy trên máy của mình với cờ khẩn cấp
  (tên cờ ở hai nền đóng băng trong đặc tả B3). Đây là quy trình có người, không phải bằng chứng máy — nói thẳng ra ở
  Q7. Ba lớp quanh cờ ấy, mỗi lớp nói đúng mức của nó:
  1. *Trong chính script (write set B3) — máy cưỡng chế, nhưng không chứng minh danh tính.* Cờ khẩn cấp chỉ chạy khi
     stdin và stdout là TTY tương tác và người chạy gõ lại đúng đủ 40 ký tự của H; không TTY hoặc gõ sai ⇒ thoát khác 0,
     không đẩy. Script ghi biên bản (H, digest gói, lý do) vào log deploy và in cảnh báo; G8 đếm lần ấy là
     `owner_emergency`. Một tiến trình dựng được pty giả, nên TTY không chứng minh người gõ là ai.
  2. *Hook PreToolUse — lớp HỎI LẠI, không phải chặn cứng.* Hành vi thật của hook hôm nay
     (`.claude/hooks/pretooluse_guard.py`): chỉ xét lời gọi công cụ `Bash` của Claude Code; lệnh khớp bảng `RISKY` ⇒ trả
     `permissionDecision=ask`, tức đề nghị hỏi người ngồi phiên, và người ấy CÓ THỂ đồng ý — `--apply` cũng chỉ ở mức
     này; `deny` chỉ áp cho agent chỉ-đọc. Từng chế độ quyền và phiên không tương tác xử lý `ask` ra sao: r4 CHƯA ĐO,
     đặc tả B3 đo trước khi khai gì thêm. Bản sửa 6 viết như thể hook cấm được cờ khẩn cấp và không giao tệp hook cho
     packet nào; sửa: B3 thêm hai cách viết cờ (dạng `sh` và dạng PowerShell) vào `RISKY`, nên hook sẽ trả `ask` khi một
     phiên Claude Code định chạy deploy khẩn cấp qua `Bash`; có được đồng ý thì lệnh vẫn gặp chốt TTY của lớp 1.
     PowerShell nhận tên tham số viết tắt theo tiền tố và không phân biệt hoa thường, nên đặc tả B3 phải chốt luật khớp
     và ca test cho các dạng ấy. Lớp này KHÔNG phủ: Codex và nền agent khác; lệnh nằm trong tệp script hoặc ghép qua
     biến; phiên mà hook không được nạp; terminal của người.
  3. *Cấm theo quy trình — KHÔNG do máy cưỡng chế.* Phiên AI không dùng cờ khẩn cấp, kể cả khi được hỏi lại và được
     đồng ý; ghi trong tài liệu quy trình của B3. Đây là lớp duy nhất phủ mọi nền, và nó là cam kết vận hành chứ không
     phải chốt — chủ kho chấp nhận ở Q7(c).
- **Thứ tự và ca kiểm của đường khẩn cấp.** Cờ và luật hook land trong CÙNG packet B3, nên không có lúc nào chế độ khẩn
  cấp tồn tại mà thiếu lớp 2. Ca: hai cách viết cờ ⇒ hook trả `ask`; lệnh deploy thường (`--push`, `-Push`,
  `--force-older`, `-ForceOlder`) ⇒ quyết định của hook KHÔNG đổi so với trước B3; đột biến gỡ luật mới ⇒ ca đích đỏ;
  script: không TTY ⇒ từ chối, TTY + H sai ⇒ từ chối, TTY + H đúng ⇒ đi tiếp và ghi `owner_emergency` (bước đẩy trong
  test dùng đồ giả); `--force-older`/`-ForceOlder` vẫn chỉ là ghi đè phiên bản, không miễn audit.
- **Hai nền:** chạy thật `sh` trên Linux và `ps1` trên **Windows thật** (máy Windows của chủ kho), đối chiếu parity cùng đầu
  vào, base và candidate (bài học r244). `pwsh` trong container Linux chỉ là bằng chứng phụ. Không dùng Windows CI (quy
  tắc thường trực); hoặc chủ kho miễn Windows-local cho B3 bằng văn bản, nêu rủi ro tồn dư.
- **Quy trình audit đỏ** (tài liệu dev-side): owner = chủ kho; xác nhận ≤ 2 giờ làm việc; ≤ 1 ngày làm việc có Issue nêu
  H, ID đỏ, phân loại code/test/hạ tầng, tái hiện tối thiểu hoặc lý do chưa tái hiện; tối đa 1 lần chạy lại hạ tầng, giữ
  attempt đỏ; bisect chỉ trên commit dựng được, không dựng được ghi `not_testable`; trong lúc chưa khoanh được vùng,
  đóng công tắc A+1 của mọi lớp (khi A+1 đã có; theo runbook công tắc) và không merge thay đổi cùng vùng; release bị
  chặn tới khi có audit xanh đúng candidate, hoặc chủ kho dùng đường khẩn cấp nêu trên.
- Phụ thuộc B1. Lớp sensitive. Write set dự kiến (đo lại trước lease): `scripts/deploy-package.sh`,
  `scripts/deploy-package.ps1`, `scripts/deploy-guard.ps1` (chốt chống thụt lùi của đường Windows đang nằm ở đây),
  `.claude/hooks/pretooluse_guard.py` + `.claude/hooks/pretooluse_guard_test.py` (lớp 2 ở trên; bộ test này đã có trong
  registry), tài liệu quy trình, đặc tả. Test của hai script đặt ở nơi đặc tả B3 chốt, và write set phải gồm luôn nơi
  đăng ký tương ứng: ca `rXX_` trong `scripts/tl_selftest.py` như các ca deploy hiện có (tệp nằm trong manifest ⇒ kèm tái
  sinh `RELEASE_MANIFEST.json`), hoặc một bộ dev-side mới (⇒ thêm `.claude/dev/ci_dang_ky_test.py` và xếp nối tiếp với
  B1/B2/PR2).

### B4 — Công tắc cho phép và bên tiêu dùng tin cậy

Mô tả đầy đủ ở §4 A+1 (hai khoá, `kiem-merge` đọc sống, tập W, runbook, write set, phép đo trước khi đóng băng, nghiệm
thu). Không lặp lại ở đây để chỉ có MỘT bản.

## 6. Làn C — chính sách M9 (r2 PR7/PR8), mặc định ĐÓNG, hai cửa

- **Cửa Q8a — được NGHIÊN CỨU** (chỉ khi làn A PR8 đo xong 30 ngày và B1–B3 đã land). C1: shadow cặp đủ/đích trên CÙNG
  snapshot (sản phẩm, đầu vào, kiểm kê, môi trường); lỗi lịch sử, lỗi cài cố ý và holdout KHÓA TRƯỚC khi chỉnh bộ chọn;
  vòng 1 = 6 replay lịch sử + 4 PR mã live (10 cặp), trần 50 runner giờ, mốc sau 5 cặp; vòng 2 cần quyết định mới, tối
  đa 30 cặp / 150 runner giờ hoặc 2 tuần; đơn vị đếm = cụm nguyên nhân gốc/PR; báo bỏ sót tương đối so với đủ theo tầng
  rủi ro; tiêu chí: **0 P0/P1 lịch sử/seeded bị bỏ sót**; khoảng tin cậy chỉ khi giả định lấy mẫu đạt (r2 §5.2–§5.3).
- **Cửa Q8b — được ĐỔI M9** chỉ sau kết quả C1 và quyết định văn bản của chủ kho. C2 sửa ADR-0060/K7 theo rủi ro, dùng
  A+1 làm công tắc (chỉ đúng `CHO_PHEP` của lớp C2 mới áp M9 theo rủi ro; vắng, lạ, mất đọc = full M9), kiểm âm trước
  merge khi PR rollback chưa land (r2 PR8).
- Mục tiêu preflight p50 ≤ 2 phút / p95 ≤ 5 phút chỉ thuộc làn C.

## 7. Thứ tự và phụ thuộc (một executor tại một thời điểm)

1. **PR1** (đang chạy) → land; bóng 14 ngày bắt đầu.
2. **B1** (hợp đồng v1 + canary A3/A4).
3. **B2** (sau B1).
4. **PR2** (Q3 quyết trước).
5. **B4** (công tắc A+1 mặc định đóng + tiêu dùng tin cậy trong `kiem-merge` + runbook công tắc). Trình tự: phép đo
   chuẩn bị (§4 A+1) → Q9 → đóng băng đặc tả → lease.
6. **PR3** (sau ≥ 14 ngày bóng, Q1, B4 đã land, A+2, A+5). Merge PR3 chưa làm giảm gì: phần giảm chỉ có hiệu lực khi chủ
   kho đặt `CHO_PHEP` của lớp PR3 sau đó (A+1); PR6 cũng vậy, với biến riêng của nó. Các mốc "sau PR3" và "sau PR6" của
   r3 (kiểm 14 ngày, mục tiêu G1–G4) tính từ lúc `CHO_PHEP` tương ứng được đặt, không từ lúc merge.
7. **B3** (sau B1; Q7).
8. **PR4** → **PR5** (sau B1) → **PR6** → **PR7** → **PR8**.
9. **Làn C** chỉ khi Q8a/Q8b mở.

Ba packet chung tệp `.claude/dev/ci_dang_ky_test.py` (B1, B2, PR2) xếp nối tiếp, cộng B3 nếu đặc tả của nó chọn bộ test
dev-side mới; B4 đụng `.claude/dev/packet_loop.py` (tệp nóng, sensitive) và B3 đụng `.claude/hooks/pretooluse_guard.py`
(sensitive) nên kiểm lease toàn kho trước khi cấp; effective write set đo lại trước mỗi lease. B1/B2/PR2 lấp khoảng chờ
bóng 14 ngày. Chủ kho từ chối làn B ⇒ không có B4, tức không có công tắc A+1: làn A khi ấy là đúng r3 đang cài (PR3/PR6
hoàn tác bằng công tắc một dòng trong mã hoặc revert), làn C2 không mở vì r2 đòi công tắc không chờ PR, và chỉ giữ
A+2…A+5 nếu Q6 cho phép.

## 8. Truy vết đầy đủ

### 8.1 r2 → r4 (từng yêu cầu chuẩn tắc)

| Mục r2 | Yêu cầu | Đích r4 | Trạng thái |
|---|---|---|---|
| §3 PR0 | ghim SHA, group theo run, không huỷ, chốt cấu trúc | PR0 (mã) + bảng §8.2 + B1 | mã có; đo còn nợ |
| §3 PR1 | đo theo ca/mutant/tiến trình con, wall/CPU | PR1 (chỉ G5) | đang thực thi |
| §3 PR1 | RSS đỉnh | A+4 | đích |
| §3 PR1 | runner OS/Python/digest phụ thuộc | trường của B1 v1 | đích |
| §3 PR1 | overhead ≤ 5 % hoặc tách khỏi cổng | A+5 (ghép cặp bật/tắt, cùng ảnh chụp) | đích |
| §3 PR1 | 1 full + 3 targeted cùng SHA, khớp ID/kết cục | PR1 nghiệm thu 1 (A/B 8 mảnh hai vế, toàn bộ định danh) cho G5; phần targeted thuộc C1 | thu hẹp, có lý do: chưa có làn targeted |
| §3 PR1 | phủ `packet_loop_test`, `nhanh_don_duoc_test` | Không đưa vào làn A/B: hai bộ đã có làn riêng (wp1353 hằng đêm; WP748 đích/đủ) và ngoài khoản lớn; C1 có thể gồm | loại khỏi A/B — chủ kho xác nhận ở Q6 |
| §3 PR1/§4 | tách kết cục; tương đương có xét duyệt | A+3 | đích |
| §3 PR2 | fixture âm cho runner/parser/selector/aggregator | PR1 fixture G4b · PR5 ca âm · A+2 · A+3 fixture · B1/B3 ca âm | đích, phân tán theo packet |
| §3 PR3 | cache | r3 §6 mục 7 | loại, giữ |
| §3 PR3 | fixture bất biến, giảm startup, cô lập state | Q4 (r3 khuyến nghị không) | chờ quyết |
| §3 PR3 | cân mảnh theo runtime, ràng buộc RSS | PR7b + A+4 | đích |
| §3 PR3/§4 | reference đóng băng, cold/warm, hai runner, oracle seeded | Chỉ cần khi tối ưu harness (Q4); A+2 dùng oracle khóa trước | phụ thuộc Q4 |
| §3 PR4 | selector theo phụ thuộc/rủi ro; không biết ⇒ rộng; manifest quyết định | r3 PR3 (bao đóng bảo thủ, dòng bóng có lý do) + PR4 + PR6 | đích; manifest ID chọn chỉ ở PR6 |
| §3 PR4 | PR sửa chính bộ chọn không tự xếp làn nhẹ | bao đóng bảo thủ gồm `ops/`, `.github/` + `kiem-merge` tính lại (α)/(β) bằng mã master (A+1, B4) | đích |
| §3 PR5/§4 | freshness 36 h/8 ngày, watchdog độc lập, retry hạ tầng ≤ 1 | B2 + B3 quy trình | đích (G7 best-effort, Q6) |
| §3 PR5 | release đúng candidate, definition OID | B3 + B1 (A4 do người vận hành chạy trước, B3 chỉ đọc) | đích |
| §4 release | ref phát hành được bảo vệ + check bắt buộc trên H | B3 (ref = `master`, đo bảo vệ, check push `ci.yml` trên H) | đích |
| §4 thời gian | bảng điều khiển hiện SHA master hiện tại so với SHA đã audit | B2 báo cáo | đích |
| §3 PR6 | trigger rộng theo rủi ro | mặc định làn A: chạm bao đóng ⇒ đủ | đích |
| §3 PR6/§5 | audit đỏ: owner, 2 giờ, 1 ngày, tái hiện, bisect, chặn cả candidate | B3 quy trình | đích |
| §3 PR7/§5.2–5.3 | shadow cặp, holdout, seeded, bỏ sót tương đối, trần 10 cặp/50 h, 30/150 | C1 (Q8a) + A+2 | có điều kiện |
| §3 PR8/§5.4 | M9 theo rủi ro, cutover cho Packet mới, không hồi tố | C2 (Q8b), dùng công tắc A+1 | có điều kiện |
| §3 PR8/§5.5 | công tắc bảo thủ: nguồn tin cậy ngoài diff PR, không dùng output bộ chọn làm quyền, do owner/trusted operator kiểm soát | A+1: biến Actions mức kho; `kiem-merge` chạy từ master, tính lại bằng mã master và đọc sống (B4) | đích; "ai kiểm soát" = tập W phải ĐO và chủ kho xác nhận (Q9(a)) |
| §5.5 | trạng thái vắng/lỗi/mơ hồ = full | A+1: chỉ đúng `CHO_PHEP` mới giảm; vắng, rỗng, lạ, không đọc được ⇒ đủ | đích, máy cưỡng chế (B4; phía CI ở PR3) |
| §5.5, §3 PR8 | tắt ngay không chờ PR rollback, ghi readback; test vế này trước merge | A+1: đóng công tắc + cờ siết của `kiem-merge`; nghiệm thu B4 (đổi công tắc sau khi lượt giảm đã xanh ⇒ đỏ) | đích; khoảng giữa `kiem-merge` và lúc bấm merge là tồn dư (Q9(d)) |
| §5.5, §3 PR8 | bật lại: điều tra + full audit H bị ảnh hưởng + quyết định mới của chủ kho | runbook công tắc (B4), mục (3) | QUY TRÌNH của chủ kho, KHÔNG do máy cưỡng chế — tồn dư ở Q9(d) |
| §5.5, §4 bảng freshness | P0/P1 lọt, bộ chọn/gom sai, release sai H, `stale_or_missing` ⇒ tắt targeted approval | runbook công tắc (B4), mục (1); watchdog B2 chỉ báo, không tự ghi biến | quy trình |
| §4 release | ngoại lệ thành phần cần manifest + audit thành phần hoặc waiver cụ thể | B3: không ngoại lệ do máy; waiver = đường khẩn cấp của chủ kho, là quy trình có người (Q7); ngoại lệ thành phần: không áp (gói là một khối) | đích; waiver là quy trình |
| §6 | ngưỡng p95 ≤ 5 phút, 0 P0/P1 lọt | làn C | có điều kiện |
| §6 mục 3 | ai được tắt ngay targeted, ai được waiver | Q7, Q9 | chờ quyết |

### 8.2 Nháp PR0 → r4 (từng tiêu chí; không suy "đạt" từ accept của spec hẹp hơn)

| ID | Điều kiện của nháp | Hiện trạng | Đích |
|---|---|---|---|
| A1 | actionlint, registry, test workflow đạt trên H | mã và chốt tĩnh (`loi_ghim_sha_du`, `chon_bien_nhan_du`, `loi_bien_nhan_du`) có trên master; kết quả trên H3 nằm trong hồ sơ accept rev12, r4 CHƯA đối chiếu từng mục | B1 ghi lại |
| A2 | dispatch trên H: mọi checkout/artifact = H, 10/10 job, K7 rc 0 | CHƯA XÁC MINH trong r4 (cần đọc hồ sơ accept rev12 và #1412) | B1 canary tạo bằng chứng mới |
| A3 | hai dispatch cùng SHA + một push, không lượt nào bị thay chỗ | `not_run` | B1 (thiết kế đã sửa) |
| A4 | definition OID tách khỏi source OID | `not_measured` | B1/B3 |
| A5 | Windows exact H, full audit, CI PR, `kiem-merge` | Windows: MIỄN theo quy tắc thường trực (r67); phần còn lại CHƯA XÁC MINH trong r4 | ghi lại trong hồ sơ B1 |
| A6 | review độc lập, land, hậu merge readback | merged; M8 `landed: false` (§10.2.2 không đo được) | nợ đo, B1 ghi lại |
| §3.5 | biên nhận máy đọc | chưa có | B1 v1 |

### 8.3 Proxima → r4

Concurrency riêng không huỷ (PR0, B1 A3) · tách kết cục (A+3) · audit dở không xanh + cảnh báo quá hạn (B2) · tự kiểm
harness (A+2, A+3, PR5) · nhóm rủi ro buộc rộng (bao đóng bảo thủ) · release gate (B3) · audit đỏ mở Issue có owner, tạm
dừng merge cùng vùng (B3) · paired full/targeted + holdout + seeded + bỏ sót (A+2, C1) · ba giai đoạn (bóng → bật có kiểm
chứng → làn C có điều kiện).

## 9. Chỉ số

G1–G6 giữ nguyên r3 §3. Thêm:

| # | Chỉ số | Nền | Mục tiêu |
|---|---|---|---|
| G7 | Khung cron vắng/đỏ được cảnh báo trong ≤ khung + 36 h + 6 h + độ trễ lịch | CHƯA ĐO | 100 % sau B2, best-effort có giám sát chéo (Q6) |
| G8 | Lần đẩy Package, báo TÁCH ba dòng: `audit_passed` · `owner_emergency` · `warning_only` | CHƯA ĐO | sau B3 chế độ chặn: `warning_only` = 0; `audit_passed` + `owner_emergency` = 100 %; mỗi `owner_emergency` có biên bản |
| G9 | Đầu-cuối p50/p95 (CHỈ BÁO CÁO) | quần thể: `pull_request`, luật cũ `day_du`, `success`, một attempt, đầu-cuối suy từ job, sau 17-11: trung vị 1775 s, p25 1590 `[r3 DX-4]` | không mục tiêu ở A/B; báo riêng `cancelled`/`failure` và thời gian xếp hàng; quần thể rộng hơn cần nền riêng |

## 10. Câu hỏi chủ kho

Q1–Q5 giữ nguyên r3 §7. Thêm:
- **Q6.** Chấp nhận làn B và A+2…A+5; chấp nhận G7 là best-effort có giám sát chéo; chấp nhận loại `packet_loop_test`/
  `nhanh_don_duoc_test` khỏi A/B? Khuyến nghị: CÓ.
- **Q7.** B3: chặn hay cảnh báo 30 ngày đầu; chấp nhận (a) KHÔNG có ngoại lệ do máy, khẩn cấp chỉ là chủ kho tự chạy với
  cờ có xác nhận TTY; (b) bảo vệ `master` đo lúc bật + hằng tháng (trôi giữa hai lần là rủi ro tồn dư); và (c) quanh cờ
  khẩn cấp chỉ có hai lớp máy, không lớp nào chứng minh danh tính — chốt TTY trong script, và lớp HỎI LẠI (`ask`, không
  chặn cứng) của hook PreToolUse cho lệnh `Bash` của Claude Code, không phủ nền khác — còn "phiên AI không dùng cờ khẩn
  cấp" là cấm theo quy trình? Khuyến nghị: chặn khi đã đo xong năng lực đọc trên cả hai máy deploy; chấp nhận (a), (b)
  và (c).
- **Q8a / Q8b.** Cho nghiên cứu C1 sau PR8 (Q8a)? Đổi M9 chỉ sau C1 (Q8b)? Khuyến nghị: quyết Q8a sau PR8, Q8b sau C1.
- **Q9.** Công tắc A+1 (mỗi lớp giảm một biến riêng, cùng một hợp đồng) — bốn điều cần chủ kho quyết hoặc chấp nhận:
  - **(a) Tập W.** Xác nhận tập chủ thể và credential ghi được biến công tắc đã ĐO ở bước chuẩn bị đặc tả B4 (không
    dùng giả thuyết "chỉ chủ kho"), và thu hẹp tới mức làm được. Khuyến nghị: chỉ còn chủ kho; gỡ Variables:write khỏi
    mọi App và token không cần nó; chưa đo xong W thì không đặt `CHO_PHEP`.
  - **(b) Mặc định đóng và giá của nó.** Chỉ đúng `CHO_PHEP` mới giảm; vắng, rỗng, lạ, không đọc được ⇒ chạy đủ. Giá:
    gõ sai hoặc xoá nhầm biến ⇒ mất phần tiết kiệm cho tới khi sửa; máy chạy `kiem-merge` không đọc được biến ⇒ mất lợi
    ích ở bước merge, trừ khi cấp cho máy ấy quyền chỉ đọc biến; cổng merge thêm phép tính lại bằng mã master cho cả PR
    hồ sơ, tính lại lỗi thì PR hồ sơ chờ (§13). Khuyến nghị: CÓ.
  - **(c) Phạm vi của KHÔNG giảm.** KHÔNG giảm ở một lớp chỉ tắt phần giảm MỚI của lớp ấy (PR3, PR6 hoặc C2) và giữ
    ngoại lệ `duong_nhanh` đang có; buộc đủ bất kể bộ phân loại chỉ ở mức từng PR, bằng cờ siết. Khuyến nghị: CÓ. Nếu chủ
    kho chọn phương án rộng của §12 (16) thì r4 phải sửa lại A+1 và §13 trước khi đóng băng B4.
  - **(d) Rủi ro tồn dư, vì r4 không có kho uỷ quyền do máy kiểm.** (i) Máy không chứng minh được lần đặt `CHO_PHEP` là
    quyết định của chủ kho: mọi thành viên của W đều đặt được. (ii) Điều kiện bật lại sau sự cố của r2 §5.5 (điều tra,
    bằng chứng đủ trên H bị ảnh hưởng, quyết định mới) là runbook; không cổng nào kiểm. (iii) Giữa lúc `kiem-merge` đọc
    công tắc và lúc bấm merge có một khoảng máy không canh; lớp bù là lượt push `day_du` sau merge, tức phát hiện sau.
    (iv) "Phiên AI không ghi biến công tắc" là cấm theo quy trình. Khuyến nghị: chấp nhận, với W đã thu hẹp ở (a).
  Không chấp nhận (b) hoặc (d) ⇒ không đặt `CHO_PHEP`: PR3/PR6 không được bật (mã có merge thì cũng nằm im ở chạy đủ)
  và làn C2 không mở, cho tới khi chủ kho quyết khác bằng một bản kế hoạch mới. Điều phối siết bằng cờ của `kiem-merge`,
  không cần quyền ghi biến.

## 11. Xử lý review `wp1172-plan-r4-review-1`

| Finding | Mức | Xử lý |
|---|---|---|
| R4-01 khai quá về A2/A5/A6 | P2 | §2, bảng §8.2 từng tiêu chí: delivered/not_run/not_measured/miễn/chưa xác minh |
| R4-02 truy vết mất mát | P2 | §8.1 tách từng yêu cầu; overhead ⇒ A+5; digest ⇒ B1; SLA 2 giờ/1 ngày, tái hiện tối thiểu, dừng merge cùng vùng ⇒ B3; C1 giữ trần và tiêu chí 0 P0/P1; Q8 tách a/b |
| R4-03 kết cục gộp tầng | P2 | A+3 bốn trường, giữ `equivalent_reviewed`, fixture và kiểm tương thích |
| R4-04 RSS không theo từng con | P2 | A+4 dùng `os.wait4` + cgroup; bỏ `RUSAGE_CHILDREN` |
| R4-05 canary ba biên nhận bất khả | P2 | B1 A3: hai biên nhận audit + một quan sát push riêng |
| R4-06 B2 trước B1, thiếu đăng ký test | P2 | B2 sau B1; write set gồm `ci_dang_ky_test.py`; xếp nối tiếp |
| R4-07 SLA watchdog | P2 | chu kỳ 6 h, đọc lại Issue, ghi lỗi ⇒ đỏ, nhịp tim chéo; G7 best-effort |
| R4-08 thẩm quyền công tắc | P2 | A+1: đo người ghi, tiêu dùng có thẩm quyền ở `kiem-merge` từ cây tin cậy, vô hiệu bằng chứng cũ khi tắt |
| R4-09 biên nhận release thiếu provenance | P1 | B1 hợp đồng v1 đóng băng trước B2/B3; B3 từ chối mọi trường bắt buộc vắng; A4 cho chính lượt; token đo trước khi chặn |
| R4-10 HEAD không ràng buộc byte gói | P1 | B3 ràng buộc byte: cây sạch, build từ ảnh chụp H, digest gói, kiểm lại trước push |
| R4-11 cờ ghi đè không phải waiver | P2 | B3 ngoại lệ chỉ do chủ kho, kiểm REST; G8 ba dòng |
| R4-12 pwsh Linux không phải Windows | P2 | B3 parity trên Windows thật hoặc miễn văn bản |
| R4-13 quần thể G9 | P2 | G9 nêu đủ bộ lọc, báo riêng huỷ/đỏ/xếp hàng |

Review lượt 2 (`wp1172-plan-r4-review-2`, trên `3f3f4ab`): 9 finding lượt 1 đóng, 4 đóng một phần; thêm 4 finding mới.

| Finding | Mức | Xử lý ở bản sửa 3 |
|---|---|---|
| R4-02 (phần còn lại) ref phát hành, CI bắt buộc, hiển thị master so snapshot | P2 | B3 "Ref phát hành và CI bắt buộc"; B2 báo cáo hai SHA; hai dòng mới ở §8.1 |
| R4-07 (phần còn lại) job đỏ ≠ đã báo chủ kho | P2 | B2: điều kiện bật = chủ kho subscribe + thử giao tin thật; chưa xác nhận ⇒ `chua_do` |
| R4-08 (phần còn lại) App ghi được biến; bật lại không do chủ kho | P2 | A+1: biến chỉ tắt; bật = bản ghi thế hệ của OWNER; Q9 gồm App; không đo được ⇒ đủ |
| R4-14 overhead bị nhiễu | P2 | A+5 ghép cặp bật/tắt cùng ảnh chụp, xen kẽ lặp, ca overhead nhân tạo; cohort chỉ giám sát |
| R4-15 B3 thiếu quyền gọi A4 | P2 | A4 do người vận hành chạy trước; B3 chỉ đọc; thiếu ⇒ chặn |
| R4-16 bên tiêu dùng chưa có write set | P2 | Packet B4 (`packet_loop.py` + test) trước PR3; nhịp tim ở phiên điều phối là runbook thủ công, không sửa `doctor` |
| R4-17 chi phí canary chỉ là mảnh | P3 | §13 ghi rõ là tổng phụ 8 mảnh, phần còn lại ước sau |

Review lượt 3 (`wp1172-plan-r4-review-3`, trên `a6f7195`): 16 finding trước đóng; R4-08 đóng một phần; thêm R4-18.

| Finding | Mức | Xử lý ở bản sửa 4 |
|---|---|---|
| R4-08 (phần còn lại) bản ghi kích hoạt bị phát lại sau tắt/bật | P1 | A+1: vị từ bật đòi `updated_at` của biến (do máy chủ đặt) sớm hơn `created_at` của bản ghi OWNER; mọi lần ghi biến tiêu thụ thế hệ; không trạng thái nên sống qua khởi động lại; ca phát lại bắt buộc ở B4; đo trước rằng REST trả `updated_at` |
| R4-18 overhead chỉ đo một mảnh | P2 | A+5 phủ cả 8 mảnh × ≥ 3 cặp, ước lượng có trọng số, ca mảnh không đồng nhất, ngân sách ~10 giờ máy trong PR3; thiếu phủ ⇒ `khong_do_duoc` |

Review lượt 4 (`wp1172-plan-r4-review-4`, trên `b764ed6`): R4-08 và R4-18 đóng; mọi finding trước giữ đóng; thêm R4-19.

| Finding | Mức | Xử lý ở bản sửa 5 |
|---|---|---|
| R4-19 comment của OWNER sửa được, không phải uỷ quyền | P1 | Bản ghi uỷ quyền chuyển thành tệp git bất biến trong `ops/uy_quyen/` trên `master`, `merged_by` = OWNER, mốc `merged_at`; điều kiện tin = `master` cấm force-push/xoá (đo); thế hệ lớn nhất thắng, xoá không làm sống lại bản cũ; áp cho cả A+1 và B3; B4 đo thêm thứ tự đồng hồ, ghi không đổi giá trị và cấu hình bảo vệ trước khi đóng băng |

Review lượt 5 (`wp1172-plan-r4-review-5`, trên `c7cf78d`): R4-19 "vá sinh lỗi mới"; thêm R4-20…R4-24, cả năm cùng lớp
"uỷ quyền chủ kho do máy kiểm" — lớp ấy đã sinh finding qua R4-08, R4-11, R4-19, R4-20…R4-24. Theo bài học kho "cùng một
hình dạng lặp ba lần trở lên thì câu hỏi đúng là có nên làm việc này không", bản sửa 6 BỎ cả lớp thay vì vá:

| Finding | Mức | Xử lý ở bản sửa 6 |
|---|---|---|
| R4-20 merge thường của chủ kho không phải cấp quyền | P1 | Không còn kho uỷ quyền; A+1 chỉ SIẾT (`FULL`), nới chỉ bằng mã đã merge qua review |
| R4-21 REST không chứng minh người đẩy | P2 | Bỏ đường commit trực tiếp cùng cả kho uỷ quyền |
| R4-22 xoá bản mới làm sống bản cũ | P1 | Không còn thế hệ/bản ghi để sống lại |
| R4-23 bản miễn trên master làm H tụt | P2 | B3 không có ngoại lệ do máy; khẩn cấp = chủ kho tự chạy, có xác nhận TTY, không ghi master |
| R4-24 token đọc không đủ cho phép kiểm mới | P2 | B3 bảng năng lực chỉ Actions/Checks/Contents read; bảo vệ nhánh là điều kiện tiên quyết đo lúc bật + hằng tháng (Q7) |
| R4-08, R4-11, R4-19 (lớp uỷ quyền) | — | Đóng theo kiến trúc: không cơ chế nào nới cổng ngoài mã; bật lại sau `FULL` là quyền quản lý biến (Q9) |

Review lượt 6 (`wp1172-plan-r4-review-6`, trên `bf16c5d`, tệp `a7fea4f3…`): R4-20…R4-24 đóng; lớp công tắc (R4-08), lớp
truy vết nguồn (R4-02) và lớp "chốt chưa có write set" (R4-16) mở lại ở biểu hiện mới; thêm R4-25…R4-29 (1 P1, 2 P2, 2
P3). Chủ kho quyết định review tiếp tới khi còn 0 finding P0–P3. Bản sửa 7 KHÔNG dựng lại kho uỷ quyền. Dòng cuối của
bảng bản sửa 6 ngay trên ("không cơ chế nào nới cổng ngoài mã; bật lại sau `FULL` là quyền quản lý biến") là lịch sử của
bản sửa 6 và KHÔNG còn mô tả bản sửa 7: từ bản này giá trị biến là khoá thứ hai, bắt buộc, bên cạnh mã đã merge, và
điều kiện bật lại là quy trình của chủ kho.

| Finding | Mức | Xử lý ở bản sửa 7 |
|---|---|---|
| R4-25 log CI cũ không cho biết giá trị công tắc hiện tại | P1 | §4 A+1 "Bên tiêu dùng…" và "Đọc sống nghĩa là gì": `kiem-merge` tự đọc REST trong chính lượt gọi; BỎ nguồn dự phòng là log; không đọc được ⇒ KHÔNG giảm; giá về tính sẵn sàng nêu rõ, khả năng đọc đo trên từng máy trước khi đóng băng đặc tả B4; nghiệm thu B4 có ca đổi công tắc sau khi lượt giảm đã xanh, với REST bị từ chối, hết giờ, biến bị xoá, tiến trình mới; §12 (17) |
| R4-26 bỏ kho uỷ quyền làm mất luôn mặc định fail-closed và điều kiện bật lại | P2 | §4 A+1 "Hai khoá": chỉ đúng `CHO_PHEP` mới giảm; vắng, rỗng, lạ, không đọc được ⇒ đủ (r3 I3, r2 §5.5); mỗi lớp giảm một biến riêng. Điều kiện bật lại của r2 (điều tra, bằng chứng đủ trên H bị ảnh hưởng, quyết định mới) vào runbook B4 và được gọi đúng tên là QUY TRÌNH. Tập W phải đo, thay cho giả thuyết "chỉ chủ kho". §8.1 tách các yêu cầu của r2 §5.5 kèm nhãn "máy cưỡng chế" hay "quy trình". Q9(a)–(d) đưa mặc định, phạm vi và rủi ro tồn dư cho chủ kho quyết |
| R4-27 chốt hook cho cờ khẩn cấp không thuộc write set nào | P2 | §5 B3: tệp hook và bộ test của nó vào write set B3 (sensitive, land cùng cờ). Mô tả đúng hành vi hook: chỉ lệnh `Bash` của Claude Code, trả `ask` chứ không chặn cứng; liệt kê phần không phủ. "Phiên AI không dùng cờ" được gọi là cấm theo quy trình. Ca cho hai cách viết cờ, TTY và không TTY, lệnh deploy thường. Q7(c). B3 nêu luôn nơi đăng ký test của hai script |
| R4-28 mức tối thiểu và ngân sách A+5 lệch nhau | P3 | §4 A+5: một hợp đồng lặp (8 mảnh × ≥ 3 cặp = 48 lượt mảnh); mức "≥ 5 cặp trên một mảnh" ghi rõ là đã bị thay; "≈ 10 giờ" rút; thời lượng gắn nhãn ƯỚC LƯỢNG kèm giả định (48 × 1057 s ≈ 14,1 giờ) và 8 lượt ước trong môi trường đo trước khi đóng băng PR3 (tổng 56 lượt mảnh) |
| R4-29 "không tăng giây `ci.yml`" bỏ sót chế độ bảo thủ | P3 | §13 rút câu ấy; thay bằng bảng giây `ci.yml` theo trạng thái công tắc (so với hôm nay và so với trạng thái đã bật), chi phí khi máy tiêu dùng không đọc được biến, giây test mới của B1–B4 (CHƯA ĐO) và chi phí của phương án rộng (≈ 3,9 triệu s/30 ngày) |
| R4-02, R4-08, R4-16 (mở lại) | — | R4-02: năm dòng §5.5 mới ở §8.1. R4-08: như R4-25 và R4-26. R4-16: như R4-27, cộng B4 nêu phần nào thuộc write set của nó và phần nào thuộc PR3 |

Bốn thay đổi có chủ đích NGOÀI chữ của năm finding, nêu ra để lượt review sau soi:
1. Phạm vi của trạng thái KHÔNG giảm thu về "tắt phần giảm MỚI" (bản sửa 6: buộc mọi PR chạy G5 đủ, kể cả PR hồ sơ). Lý
   do và chi phí ở §4 A+1, §12 (16), §13; chủ kho quyết ở Q9(c).
2. Mỗi lớp giảm (PR3, PR6, C2) một biến riêng, để merge mã của lớp sau không tự bật nhờ `CHO_PHEP` đã đặt cho lớp trước.
3. `kiem-merge` tính lại bằng mã master cho CẢ ngoại lệ `duong_nhanh` đang có (trường hợp (α)) và tự kiểm nó đang chạy
   từ cây master: đây là siết, có giá về tính sẵn sàng nêu ở §4 A+1 và Q9(b).
4. Write set B3 nêu thêm `scripts/deploy-guard.ps1` và nơi đăng ký test của hai script; write set B4 nêu điều kiện kéo
   theo tệp protocol/adapter.


## 12. Phương án loại

Giữ chín phương án của r3 §6. Thêm: (10) khôi phục nguyên r2 — nhắm khoản 4,7 % và đổi lấy M9; (11) sửa spec PR1 đang
chạy — hồi tố; (12) watchdog là một bước trong full audit — lượt vắng không chạy được bước của nó; (13) thêm trigger push
cho full audit chỉ để đủ canary — đổi tần suất và chi phí; (14) `pull_request_target` chạy mã PR để đọc công tắc — mở
quyền cho mã chưa duyệt; (15) kho uỷ quyền chủ kho do máy kiểm (biến có thế hệ, comment, tệp git do chủ kho merge) — ba
lượt review cho thấy lớp này tự sinh lỗ vì chủ kho bấm mọi merge; (16) trạng thái KHÔNG giảm buộc MỌI PR chạy G5 đủ, kể
cả PR `duong_nhanh` (bản sửa 6) — không nguồn nào đòi (r2 §5.5 và r3 chỉ đòi tắt phần giảm mới), thu hồi ngoại lệ đã
duyệt của r3 I5(a), và khi KHÔNG giảm là mặc định thì tốn ≈ 3,9 triệu s/30 ngày cùng một lượt G5 trước merge cho mọi PR
hồ sơ; nhu cầu buộc đủ từng PR giữ bằng cờ siết của `kiem-merge`; chủ kho vẫn có thể chọn nó ở Q9(c); (17) lấy log CI
của lượt trên H làm nguồn dự phòng cho giá trị công tắc — log cũ không nói được giá trị hiện tại (R4-25).

## 13. Ngân sách và rủi ro

Làn B ước bốn packet (B1–B4; lớp review do đặc tả từng packet chốt theo protocol, riêng B1, B3, B4 đã biết là sensitive);
mỗi packet 1–3 lượt thực thi, 1–3 review Codex, 1–3 CI PR Ubuntu, K7 khi chạm vùng M9, 0 Windows CI; B3 thêm một lần chạy
Windows-local trên máy chủ kho (hoặc miễn). Canary A3 = 2 lượt full audit thêm; riêng 8 job mảnh ≈ 2 × 13 282 = 26 564 s
giây job (trung vị 8 mảnh
`[B: M1.luot_du_8_manh_success.tong_giay_8_job_manh_moi_luot]`, CHƯA gồm job registry, job gom, A4 và quan sát push — ước
lại từ cùng tập lượt sau B1, không chạy thêm audit chỉ để ước). A+5: 56 lượt mảnh trong môi trường đo cố định, ngoài CI;
thời lượng là ước lượng (xem A+5). Chi phí thường xuyên NGOÀI `ci.yml` (ƯỚC LƯỢNG, chưa đo): B1 vài giây mỗi lượt audit;
B2 4 job nhỏ/ngày; B3 vài lời gọi REST mỗi lần deploy; B4 một lời GET ở mỗi lượt `kiem-merge` phải đọc công tắc.

**Giây `ci.yml`.** Bản sửa 6 viết "không bổ sung nào tăng giây CI của `ci.yml`"; câu ấy sai và được RÚT. Các chỗ r4 làm
tăng, hoặc làm mất phần tiết kiệm:

| Nguồn | So với HÔM NAY | So với trạng thái đã bật (sau PR3/PR6) |
|---|---|---|
| Công tắc ở `CHO_PHEP` (vận hành bình thường) | +0 job; thêm một lần đọc `vars` ở `chuan-bi` | — |
| Công tắc KHÔNG giảm: mặc định trước khi chủ kho bật; sau sự cố; gõ sai hoặc xoá nhầm biến | +0, `ci.yml` chạy đúng luật hôm nay (không kể overhead phần đo của PR1, xét ở A+5) | mất phần tiết kiệm G5 chừng nào còn ở trạng thái ấy. r3 §5 minh hoạ, chưa đo: 0,57–2,00 triệu s/30 ngày khi chỉ có PR3; 3,05–4,72 khi có PR6 (đã trừ 0,46 chi phí audit thêm của PR5; khoản ấy vẫn chi khi công tắc đóng) |
| PR đang mở có lượt CI gần nhất đã giảm, rồi công tắc đóng | — | mỗi PR cần MỘT lượt `ci.yml` nữa trên H trước merge, ≈ 13 716 s giây thực thi (trung bình lượt PR `day_du` của cohort; mốc sau 17-11: 10 659 s); số PR như vậy tại một thời điểm: CHƯA ĐO |
| Máy chạy `kiem-merge` không đọc được biến | +0 | mỗi PR thuộc trường hợp (β) cần một lượt G5 đủ trên H cuối trước merge, cùng đơn giá; lợi ích chỉ còn ở các lần đẩy trung gian; phần mất: CHƯA ĐO (tuỳ số lần đẩy mỗi PR) |
| PR hồ sơ (`duong_nhanh`), ở mọi trạng thái công tắc | +0 giây `ci.yml`: CI của chúng không đọc công tắc; cổng merge thêm phép tính lại (α), không phải job CI | như cột bên |
| Cờ siết của `kiem-merge` trên một PR | PR `duong_nhanh`: một lượt `ci.yml` đủ trên H, kéo theo job Windows; PR khác: +0 | một lượt `ci.yml` đủ trên H cho PR ấy, cùng đơn giá |
| Test mới của B1–B4 chạy trong `ci.yml` (registry, packet-loop, selftest) | CHƯA ĐO; mỗi đặc tả packet phải báo delta theo thời gian job/bước | như cột bên |
| Các lượt PR của B3 (chạm tệp hook) | bộ `pretooluse_guard_test` chạy chế độ đủ: trung vị 1009 s thay vì 26 s mỗi lượt | như cột bên |
| Phương án rộng §12 (16), CHỈ khi chủ kho chọn ở Q9(c) | khi KHÔNG giảm: ≈ 3,9 triệu s/30 ngày (ƯỚC LƯỢNG: 454 lượt × 8 mảnh × 1068 s = 3 878 976 s, giả định mọi lượt chạy trọn và tốn bằng trung vị) | như cột bên, cộng phần mất ở dòng hai |

Nguồn số của bảng: 13 716 s = 9 669 927 / 705 `[B: M2.moi_luot.theo_su_kien_va_lan."pull_request | day_du".giay_thuc_thi]`;
10 659 s `[r3 DX-4]`; 454 lượt `[B: M2.moi_luot.theo_su_kien_va_lan."pull_request | duong_nhanh".so_luot]`; 1068 s
`[B: M2.theo_job.bang."gate-cong-cu | ubuntu-latest | day_du".trung_vi]`; 1009 s và 26 s (1009,181 và 25,953)
`[B: M2b.bang."gate-registry | ubuntu-latest | .claude/hooks/pretooluse_guard_test.py".che_do]`; các khoảng tiết kiệm lấy
nguyên từ bảng "Tiết kiệm G5 tính CHUNG" của r3 §5.

Rủi ro: B1 đụng workflow M9 (sensitive, chỉ siết); B3 có thể chặn deploy khi chưa có audit trên H — chủ đích, có đường
khẩn cấp của chủ kho; B4 có thể chặn merge khi không đọc được công tắc — chủ đích, lối ra là một lượt G5 đủ trên H. Rủi
ro tồn dư vì không có kho uỷ quyền do máy kiểm: Q7(c) và Q9(d).
