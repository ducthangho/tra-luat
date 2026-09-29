verdict: changes_requested
reviewed_sha: c43347d1e2c2f76bb21dc2d9d28bd6bfa153d355
base_da_review_truoc: 0bc6e56e1a1fd21cedfc18557320941d51db866c
so_lan_luot_nay_bi_chet_va_phong_lai: 0

Kết luận: **changes_requested — 1 P1, 1 P2, 0 P3**. P1 vẫn mở trước 14:30:07Z; ba P2 văn bản đã vá thật; P2 manifest được sửa ở gói gốc nhưng sinh lại trong bản sao phục dựng. Đã ghi kết luận dần trong phiên, rồi hoàn tất bản này cùng cây gợi ý.

Reviewer: Codex / OpenAI, phiên độc lập qua API, shell cục bộ; transport: tệp trong sandbox. `GATE`/`LO` dưới đây là hai đặc tả tương ứng trong `cay-kho/ops/specs/`; các đường `ops/...` tính từ `cay-kho/`. Nguồn đo và script ở `do-review10/`. Không có lần reviewer chết/phóng lại; lỗi thiết lập và lỗi script đo đã sửa không được tính thành lỗi PR hoặc lần phóng reviewer mới.

## ĐỐI CHIẾU LƯỢT TRƯỚC

- `bia-mo-mot-ref-khong-thu-hoi-moi-ban`: **CHƯA VÁ** — 11:29:38Z 07-09-2026, hàm CLI thật với nguồn ref là mirror offline: registry `NGƯỜI_GIỮ 2` (#456 + exec-1r4), workflow `NGƯỜI_GIỮ 1` (exec-1r4), cả hai rc=11 (có người giữ). `check` r4 rc=0 không phát hiện giao write set. Snapshot có thêm `ops/lease-wp461-g2` ngoài 9 tên được giao; không tính `HEAD` là nhánh máy chủ độc lập. `do-review10/leases.json`.
- `a2-neo-nen-cu-trai-write-set-hien-tai`: **ĐÃ VÁ THẬT** — hàng thứ tự GATE:395 chỉ định nền A2 tại `start_from_sha`; hai run 39 bước chỉ còn đối chiếu lịch sử A1/A5. Mô hình cùng base/event/lane giữ 88/88 bộ ba dispatch và 44/44 PR; bỏ receipt-v2 mất 2/1 bộ ba và bị bác. So khác lane vẫn +4/−4. Nền PR `82e01a4` có ci.yml bằng byte nền lease `d28c4b1`. `do-review10/contracts.json`.
- `bien-do-khac-head-khong-phai-nhieu-runner`: **ĐÃ VÁ THẬT** — tự tính từ 2062 hàng của `buoc_master.tsv`, chọn đúng 11 run: 5 push/master + 3 PR/nhánh + 3 dispatch/nhánh; 10×40 + 1×39 bước YAML. Biên độ 10,283333 phút; 28/28 ô hệ số và 12/12 đầu dải làm tròn khớp. GATE:103–108, :454–456, :540–542 phân biệt chênh khác event/lane với biên thiết kế; nợ runner vẫn mở tại :630–637. Không còn dùng mẫu trộn để nới A1/A5. `do-review10/costs.json`.
- `quyet-dinh-tiep-h-con-bi-phu-dinh`: **ĐÃ VÁ THẬT** — kiểm nội dung mở đầu, hàng H, quyết định §12, tiêu đề thiết kế, Issue và `ly_do_cap`: cùng lựa chọn 1; URL khớp 3/3; đủ Đ1–Đ5; lease nháp vẫn 5 null. Hai khối Python H bằng byte với base. Hai grep thật đều in 0 và rc=1 (không có dòng khớp); kết luận dựa cả nội dung thay thế, không chỉ grep. `do-review10/contracts.json`.
- `manifest-luot8-liet-ke-hien-vat-khong-duoc-giao`: **VÁ SINH LỖI MỚI** — bản lượt 8 thật đã đạt rc=0, 69/69, nhưng bản sao `pr468-hoso-4-packet-review-9-codex/artifact-repair/` vừa thêm mang cùng manifest lại rc=1, 50/69, thiếu 19 tệp. Đo 2026-09-07T11:26:40Z; `do-review10/static.json`.

Lượt 7/8 tái phát: không tìm được slug đóng nào tái phát trong phạm vi phép ngắn. `bia-mo-mot-ref-khong-thu-hoi-moi-ban` là lỗi **liên tục còn mở**, không phải đã đóng rồi tái phát. Đã tự kiểm thêm: `issue-lo-neo-commit-cu-kem-bam-moi` vẫn đóng (4/4 spec = hash lease = blob Issue neo); `thieu-hien-vat-quyet-dinh-h-va-chi-phi` vẫn đóng ở nguồn hiện hành (bảng số khớp, nguồn gốc lượt 6 còn đủ); `span-rong-nuot-ti-le-vo-can` không tái phát nghĩa vụ bản in thứ tám (8/8 stdout đã lưu có rc0, băm khớp, BASE/H replay 0/8 bị bác); `a9-khai-sai-base-ngoai-le` không tái phát (4 fixture nguyên byte: hai cặp CA BASE=H=ValueError, hai cặp mutant BASE=0/H=ValueError). Không khai replay thành suite mới chạy hoặc chứng minh H đã thi công.

## BẢNG ĐO

| khẳng định | hồ sơ khai | tôi đo được | khớp? |
|---|---|---|---|
| Exact HEAD; sạch | c43347d | c43347d1e2c2f76bb21dc2d9d28bd6bfa153d355; status rỗng | có |
| Manifest lượt 6 | đủ | rc=0, 62/62 | có |
| Manifest lượt 7 | đủ | rc=0, 66/66 | có |
| Manifest lượt 8 | 69/69 | rc=0, 69/69 | có |
| Manifest `lượt9/artifact-repair` | 69 tệp theo manifest | rc=1, 50/69 | không |
| Lease r4; snapshot hiện tại | registry 2; workflow 1 | 2 / 1 lúc 11:29:38Z; rc=11 / 11 | có; P1 mở |
| Ref giữ blob #456 cũ | 9 nhánh lúc 10:2xZ | 10 tên nhánh + `HEAD` trong mirror được giao; thêm `ops/lease-wp461-g2`, tip 11:20:33Z | danh sách cũ thiếu 1 so snapshot mới; chưa chứng minh sai lúc 10:2xZ |
| r3 và r4 đều thêm sau base lượt 9 | lời giao nhiệm vụ | r3 đã có tại 0bc6e56; chỉ r4 mới thêm | không |
| Hết hạn #456 | 14:30:07Z | mô hình thời gian 14:30:06/07/08 cho registry 2/1/1 | chỉ mô phỏng |
| Diff / số commit | 141 tệp, +34464/−23, 3 commit | khớp byte cả patch lẫn numstat; 0 đường ngoài ops | có |
| Hai grep loại câu cũ | mỗi phép in 0 | LO: 0, rc=1; GATE: 0, rc=1 | có; chỉ là kiểm chuỗi |
| A2 đủ bước / thiếu receipt-v2 | cùng base/event/lane | dispatch 88/88 QUA; bỏ 2 bộ ba ĐỎ; PR 44/44 QUA; bỏ 1 bộ ba ĐỎ | có trong mô hình |
| A2 so sai lane | khác 4 bộ ba thêm/4 mất | +4/−4 dù ci.yml bằng byte | có |
| Quyết định H | lựa chọn 1; Đ1–Đ5; nháp chưa cấp | lời chọn nhất quán 6 vị trí, URL 3/3, 5 điều kiện, 5 null; 2 khối Python không đổi | có |
| Spec/lease/commit Issue #463–466 | băm đóng băng khớp | 4/4 đúng; #463/#464 neo 1a330305e20a0667fff4954f8542aadd5e375b50 | có |
| Nguồn mẫu chính | 11 run, 5 master + 6 nhánh | 5 push/master + 3 pull_request/nhánh + 3 workflow_dispatch/nhánh; 1×39 + 10×40 bước YAML | có |
| Windows min/max/range/median/mean (phút) | 40,20 / 50,48 / 10,28 / 46,02 / 45,84 | 40,2 / 50,4833333333 / 10,2833333333 / 46,0166666667 / 45,8378787879 | có |
| `test registry`: n/min/max/median; dải trung vị | 11 / 1,07 / 1,71 / 1,21; 1,21–1,21 | median 1,2125435540; dải 1,2112594312–1,2138291691; 4 ô khớp | có |
| `tl selftest`: n/min/max/median; dải | 11 / 1,41 / 2,26 / 1,83; 1,82–1,84 | median 1,8305084746; dải 1,8185654008–1,8425531915; 4 ô khớp | có |
| `packet-loop selftest`: n/min/max/median; dải | 11 / 1,88 / 2,89 / 2,37; 2,36–2,38 | median 2,3692946058; dải 2,3623188406–2,3762993763; 4 ô khớp | có |
| `G5 kiem ban ke`: n/min/max/median; dải | 11 / 1,91 / 3,09 / 2,40; 2,37–2,43 | median 2,3965517241; dải 2,3675213675–2,4260869565; 4 ô khớp | có |
| `lease-publish selftest`: n/min/max/median; dải | 11 / 2,42 / 3,84 / 2,94; 2,91–2,97 | median 2,9420289855; dải 2,9136690647–2,9708029197; 4 ô khớp | có |
| `bien-nhan v2 selftest`: n/min/max/median; dải | 10 / 7,07 / 9,74 / 7,79; 7,71–7,88 | median 7,7929292929; dải 7,7051777052–7,8824863416; 4 ô khớp | có |
| Job trọn: n/min/max/median | 11 / 1,52 / 2,36 / 1,73 | median 1,7267041901; 4 ô khớp | có |
| 19 job Ubuntu success của TSV gốc | 20,93–28,42; median 26,52 | n=19; 20,933333–28,416667; median 26,516667 | có |
| Bảng nền trong JSON lượt 9 và GATE r4 | cùng số | 7/7 số n và median JSON khớp tính độc lập; 28/28 ô bảng, 12/12 đầu dải khớp | có |
| Nguồn lượt 6 so TSV được giao | đủ tái tính nguồn hiện hành | 1054 hàng bước giao nhau không lệch giây/conclusion; 86 hàng của run 34045664423 chỉ có trong nguồn lượt 6 | có; không gộp hai nguồn |
| Dự toán cũ run 34045664423 | 43,20→21,03; 110,65→126,22; +14,1% | 43,2→21,033333; 110,65→126,233333 từ giây; 126,22 theo bảng cộng số phút đã làm tròn; +14,083446% | khớp độ làm tròn đã khai |
| Mốc quyết định A1/A5 | ≤25,00 / ≤135,00 | ngưỡng nguyên trạng; được gọi là biên thiết kế, có nghĩa vụ đo lại và báo ĐỎ | có; chưa đo nghiệm thu thật |
| Nguồn phục dựng `artifact-repair` | phép thử lượt 9 khôi phục lượt 8 | 50/50 tệp hiện có giống byte gói lượt 8; cả 19 thiếu có nguồn đúng băm tại gói lượt 8 | có về nguồn; bản chép thiếu |
| Metadata stdout/stderr trong gói lượt 9 | byte/hash đã ghi | 16 tệp metadata có trường byte/hash đối chiếu được; 0 lệch | có; không phải chạy lại suite |
| Verdict lượt 9 được chép và neo | 29806 B; fa11cdcf… | bằng byte VERDICT-luot9.md được giao; băm/bytes receipt đúng | có; không kiểm model identity trực tiếp |
| Cổng ngắn | read-only | doc-claims rc0: 0 cờ cứng, 367 advisory, 106 tệp; doctrine rc0: 7 tệp/0 chỗ chép; adr-song rc0: 46/46 | có trong phạm vi từng cổng |
| Cây gợi ý P2 | bổ sung đủ byte thiếu | rc0, 69/69; phục dựng 19 tệp; 72 tệp kèm băm nguồn/nền/đầu ra và hunk→slug đúng | có; chỉ cây ngoài checkout |

### bia-mo-mot-ref-khong-thu-hoi-moi-ban  [P1]  Bản #456 chưa bia mộ vẫn giữ registry cùng r4 trước hạn

TỆP/DÒNG: `ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md:579` (A9), `:586` (cấp trước hạn); `ops/leases/gate-tach-job-cat-chi-phi-exec-1r4-claude-20260906.yaml:39`, `:124`; `ops/issues/463-GATE-TACH-JOB-CAT-CHI-PHI.md:116`, `:132`; blob #456 `8b2103c06687546379a17f6deafc97f1fe0173fd` trên 10 tên nhánh trong snapshot.

VẤN ĐỀ: Bia mộ chuỗi chỉ kết thúc bản cụ thể có khóa đó, không thu hồi bản #456 còn hạn trên ref khác. Chuỗi hiện tại đúng hai chiều nhưng bất biến một write set/một lease không đạt. R3 cấp 09:44:51Z (đã nằm trong base lượt 9), r4 cấp 10:17:12Z; mô hình cây tại từng commit cấp cộng blob #456 cũ đều cho 2/1. Không có miễn trừ “cùng một lần cấp liên tục” trong A9 hoặc Protocol §1.2/§5. Riêng điều kiện A9 “TRƯỚC khi bắt tay” không chứng minh executor đã sửa runtime trái phép: hồ sơ nói đang bị chặn, và diff lượt này không đụng runtime. Việc cấp r3/r4 là các sự kiện cấp mới trong khi trạng thái loại trừ chưa đạt; ghi vào cùng slug, không nhân finding.

ĐÃ THỬ VÁ: mô phỏng chỉ thay thời điểm, giữ nguyên toàn bộ dữ liệu/ref, cho registry 2 → 1 đúng 14:30:07Z. Đường chờ hết hạn được A9 chấp nhận để đóng trạng thái sau readback thật; không xóa được lịch sử cấp sớm và không phải bản vá. Tại giờ review vẫn chưa hết hạn.

GÓI VÁ: `goi-y/cay/ops/issues/463-GATE-TACH-JOB-CAT-CHI-PHI.md` đã bổ sung trạng thái chặn, danh sách ref hiện đo và thủ tục ghi nhận đóng bằng thời gian. Hunk được neo về slug này trong `goi-y/hint_provenance.json`, có `source_sha256` của Issue nền. Đây là sửa hồ sơ, **không đóng P1 bằng một bản vá tệp**: đường chủ kho chọn còn cần hết hạn thật và readback đủ ref. Không thay, cấp, thu hồi lease hoặc tạo timestamp sự kiện tương lai. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python3 -B do-review10/measure_leases.py` rc=0; gọi `main(ai-dang-giu)` và `main(check)` của module thật. Adapter chỉ thay giao tiếp `ls-remote origin` bằng mirror sandbox và loại mục `HEAD` theo quy tắc bỏ `*/HEAD` của scanner. Tự quét 288 cặp blob/path; các chốt kiểm đầy đủ ref/tụt sau vẫn chạy. GitHub trực tiếp và readback tương lai: **KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho)**.

ĐỘ TIN: cao với snapshot và ngữ nghĩa mã; không chứng nhận số nhánh GitHub hiện hành hay thời điểm cấp lịch sử trên máy chủ.

### manifest-luot8-liet-ke-hien-vat-khong-duoc-giao  [P2]  Bản sao phục dựng lượt 8 trong gói lượt 9 lại thiếu 19 tệp

TỆP/DÒNG: `ops/reviews/pr468-hoso-4-packet-review-9-codex/artifact-repair/ARTIFACTS.sha256:48` đến dòng 66 (đúng 19 đường `rig/`); phép thử lịch sử ở `ops/reviews/pr468-hoso-4-packet-review-9-codex/artifact_checks.py:12`.

VẤN ĐỀ: Bản lượt 8 gốc đã được phục dựng đúng, nhưng cùng cam kết 69 tệp được chép vào thư mục thử phục dựng của lượt 9, chỉ có 50 tệp khớp. Đây là lỗi toàn vẹn trong hiện vật mới, không phải phủ nhận kết quả lịch sử của reviewer lượt 9.

ĐÃ THỬ VÁ: giữ nguyên manifest, phục dựng 19 tệp bằng byte từ `pr468-hoso-4-packet-review-8-codex/rig/` đã kiểm đủ. Bản gợi ý đạt rc0, 69/69. Thêm README phân biệt đây là bản thử phục dựng lượt 8 trong review lượt 9; các số lịch sử vẫn giữ nguyên. Không sửa hash để che tệp thiếu.

GÓI VÁ: cây đủ để kiểm checksum tại `goi-y/cay/ops/reviews/pr468-hoso-4-packet-review-9-codex/artifact-repair/`. `goi-y/hint_provenance.json` ghi từng hunk thêm→slug, dòng manifest, `source_path`, `source_sha256` và băm đầu ra. Tệp đích vốn chưa có được ghi rõ `target_base_sha256: null`; 50 tệp và manifest nguyên trạng chỉ là ngữ cảnh để kiểm độc lập. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `sha256sum --check` trên cả 4 manifest tìm được trong `ops/reviews/**`: 3 xanh, 1 đỏ. `python3 -B do-review10/verify_artifacts.py` rc0: 50/50 tệp hiện có bằng nguồn lượt 8, 19/19 thiếu phục dựng được đúng băm. `python3 -B do-review10/build_hints.py` rc0: bản gợi ý 69/69, băm nguồn/nền/đầu ra và mapping từng hunk đều khớp. Log: `static.json`, `artifacts.json`, `hint-manifest.stdout`, `hint-validation.json` trong `do-review10/`.

ĐỘ TIN: cao; đo trên byte tại exact reviewed SHA.

## LEASE — trả lời ba câu trọng tâm

**(a) Chín tên được giao đều có blob cũ, nhưng chưa đủ cho snapshot lượt 10.** Quét 303 mục `refs/heads/*` của `kho.git` tìm thấy 11 mục mang cùng blob #456: chín tên đã nêu, `ops/lease-wp461-g2`, và `HEAD`. `HEAD` bằng master, đồng thời checkout có `origin/HEAD` là symbolic ref tới `origin/master`; không tính đó là nhánh máy chủ độc lập. Kết quả là **10 tên nhánh** trong snapshot. Tip `ops/lease-wp461-g2` là `3c4c5875c9dbc4b6d9a1142c99edde49ab74db6f`, giờ commit **11:20:33Z**, muộn hơn phép đo điều phối 10:2xZ. Vì vậy tôi xác nhận danh sách cần thêm nhánh này **ở snapshot được giao**, không kết luận người đo đã bỏ sót nó vào 10:2xZ. Thời điểm tạo nhánh và tính đầy đủ GitHub lúc đó/hiện tại: **KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho)**.

**(b) R3/r4 là cấp mới, chuỗi bia mộ không miễn kiểm giao write set.** R3 có `event: executor_lease_granted`, lease_id mới, mốc cấp 09:44:51Z/hạn mới và commit `3ef7d2a37d833ae62ff8d2848e146a945360e64d`; nó **đã có trong 0bc6e56**. R4 có cùng loại event, lease_id khác, cấp 10:17:12Z/hạn mới trong `1a330305e20a0667fff4954f8542aadd5e375b50`. Cùng generation=1 không biến hai sự kiện đó thành một sự kiện bất biến. Bốn cạnh #456→r1→r2→r3→r4 trên cây hiện tại đúng hai chiều; `_bia_mo_doi_xung` tại `ops/lease_publish.py:570` kiểm khóa của **bản đang xét**, không truyền bia mộ sang blob #456 không có khóa ấy.

Theo **bất biến §1 mục 2 và quy tắc tính giao trước cấp ở Protocol §5**, mỗi lần cấp lại còn giao #456 đều lặp việc cấp khi điều kiện loại trừ chưa đạt. Theo **A9 nhánh cấp trước hạn** (:586–589), chuỗi riêng trên PR cũng chưa đủ: còn phải xử mọi ref giữ bản cũ và readback. Mô hình tại từng commit cấp + blob #456 cũ cho registry=2/workflow=1 ở cả r3 lẫn r4. Đây là lịch sử tiếp diễn của cùng P1, không cộng thêm hai P1. Riêng việc **bắt tay thi công runtime** trái mệnh đề mở đầu A9 chưa có bằng chứng: Issue vẫn ghi bị chặn, và 141 đường thay đổi lần này đều ở `ops/`. Không đánh đồng có lease với đã chạy executor.

**(c) Hết hạn được hợp đồng nhận để chấm dứt trạng thái giữ; không hồi tố hợp lệ hóa cấp sớm.** `_phan_loai_lease` tại `ops/lease_publish.py:547` dùng `han <= bay_gio`, nên tại đúng 14:30:07Z, với cùng tập ref và r4 còn hiệu lực, #456 thành `HẾT_HẠN`; registry giảm 2→1. A9 chấp nhận dòng tiền nhiệm có `HẾT_HẠN`. Nhưng đường (a) nguyên thủy nói **cấp sau hạn** và dùng `thay_the_cho: []`; r4 đã cấp trước, thay r3, nên không được đổi nhãn lịch sử thành “đã thực hiện đường (a) ngay lúc cấp”. Điều có thể đóng sau readback là **trạng thái chồng lease hiện hành**. Vi phạm/cửa sổ cấp sớm vẫn phải được ghi đúng và không lặp thêm.

Tại reviewed SHA, `Issue #463:116–124`, README review lượt 9 và receipt cũ đều giữ P1 mở, nhắc hết hạn/mô phỏng; **không thấy lời khai P1 đã đóng bằng bản vá**. Hồ sơ chưa có readback sau hạn, cũng chưa thể có kết quả tôi tự đo ở tương lai. Cây gợi ý bổ sung cách ghi “đóng bằng hết hạn tự nhiên + readback”, không ghi kết quả trước. P1 **CHƯA VÁ** trong lượt này; không chờ ba giờ rồi dùng đồng hồ để đổi verdict mà thiếu readback mới.

## MẪU 11 RUN — ý nghĩa còn lại của phép sửa

Tái tính trực tiếp `buoc_master.tsv` (2062 hàng, 30 run), nối metadata 11 run với `mau-11-run-event-branch.txt`, rồi kiểm chéo metadata đã lưu trong nguồn lượt 6. Mọi tỉ lệ lấy **cùng run/head, cùng bước theo tiền tố, cả hai job và hai bước success**; trung vị là trung vị các thương `w/u`, không phải thương hai trung vị. Với receipt-v2, một run chưa có bước này nên n=10. Dải trong bảng là trung vị các cận `(w−0,5)/(u+0,5)` và `(w+0,5)/(u−0,5)` theo quy ước sai số làm tròn ±0,5 giây mà spec khai; **không phải khoảng tin cậy thống kê**. Đủ từng cặp giây, cận và phân nhóm event trong `do-review10/costs.json`.

**Vẫn có nghĩa:** min/max/range/median/mean mô tả đúng 11 quan sát được chọn; tỉ lệ từng cặp mô tả Windows/Ubuntu ở bước và run cụ thể; `1,73×` là trung vị mô tả của job trong mẫu này. Chúng cho thấy không thể áp một hệ số duy nhất cho mọi bước. Phân nhóm cùng dữ liệu cho trung vị job push≈1,679666, PR≈1,601705, dispatch≈1,919518; đây cũng chỉ là thống kê nhóm nhỏ, không xác định nguyên nhân event hay nền.

**Không suy được:** nhiễu runner riêng, phương sai runner tại cùng tải, ảnh hưởng nhân quả của hệ điều hành/event, hệ số phổ quát cho vòng đột biến chưa được đo, mức tiết kiệm thực tế sau tách, hay hóa đơn thật. Mẫu trộn ba event, hai lane và tải 39/40 bước; dải 10,28 không tách các thành phần đó. Các tỉ lệ theo bước vẫn mô tả được vì mỗi cặp giữ run/head, nhưng gộp qua head không tạo mẫu kiểm soát.

**Bản sửa phân biệt đúng các giới hạn cần cho quyết định hiện hành.** GATE:103–108 rút kết luận nhiễu thuần ở hai run cùng tree; :141–145 không dùng biên độ để nới ngưỡng; :209–216 giới hạn tỉ lệ vào mẫu tiện tay, không suy vòng mutant; :630–637 giữ nợ `NHIEU-RUNNER-CHUA-TACH-KHOI-TAI`. A1/A5 nói rõ biên thiết kế và đo lại trước nghiệm thu. Vì thế đây là sửa nội dung kết luận, không chỉ đổi nhãn master thành nhánh.

**Giữ A1≤25,00 và A5≤135,00 là đúng đối với hợp đồng đang đóng băng.** Mẫu trộn không cung cấp căn cứ để nới hoặc siết chúng. Hai ngưỡng là yêu cầu thiết kế phải đo, không phải ước lượng nhiễu; nghiệm thu thật có thể ĐỎ và phải báo đúng. `21,03` và dự toán billing dùng run nhánh **34045664423**, khác mẫu 11 run: run ấy vắng khỏi TSV 30 run được giao nhưng có đủ 86 hàng bước và hai job trong `ops/reviews/pr468-hoso-4-packet-review-6-codex/nen-a1-a5/`. Tính giây cho 21,033333/126,233333; dùng số phút đã làm tròn như bảng spec cho 21,03/126,22. Không lấy trung vị 1,73 hay biên độ 10,28 để nhân ngưỡng. Chi phí sau tách, A1/A5 thực tế và hệ số billing hiện hành: **KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho)**.

## HIỆN VẬT — phân biệt lịch sử với nguồn hiện hành

Đã kiểm **mọi** `*.sha256` trong `cay-kho/ops/reviews/**`: đúng 4 manifest. Chỉ manifest lồng `lượt9/artifact-repair` đỏ. Các tệp gốc lượt 8 mới được đưa vào cây khớp đúng 19 băm thiếu; bản sửa gốc đạt thật 69/69. Cũng đã kiểm 16 metadata stdout/stderr có byte/hash đối chiếu được trong gói lượt 9, 0 lệch; JSON `costs.json` khớp bảng GATE hiện hành; bốn đặc tả khớp hash lease và commit Issue neo. Bản verdict lượt 9 trong kho bằng byte bản được giao, 29806 byte/băm fa11cdcf… đúng receipt.

`artifact-repair/` **đúng là bản thử khôi phục hiện vật lượt 8 do reviewer lượt 9 tạo**, suy ra từ `artifact_checks.py`, manifest và 50/50 tệp còn có bằng byte gói lượt 8. Nó được giữ ở thư mục riêng, không ghi đè root hiện vật lượt 9. `artifact-checks.json` khai `original_rc=1` và `repaired_copy_rc=0` là kết quả **lúc review base 0bc6e56**, không phải khẳng định bản chép hiện tại đạt. Vì thế lỗi xác nhận được là **chép thiếu thư mục thử**, không có bằng chứng đã ngụy trang một phép thử thành kết quả gốc. Gợi ý thêm README để ranh giới ấy rõ ngay khi mở thư mục.

Không lấy `state.json`, `static.json`, `final-check.json` lịch sử hoặc stdout cũ để khai test chạy ở c43347d. README mục lượt 9 ghi rõ head 0bc6e56 và còn P1; GATE r4 trích kết quả +4/−4 của reviewer lượt 9 và phép đó đã được tôi tái lập trong mô hình. Không tìm được lời khai chưa đo mới nào được nâng thành đã đo trong các đường trích dẫn đã kiểm. Các câu lịch sử “chưa có 2062 hàng”, “gói gốc thiếu 19 tệp” vẫn là lịch sử tại lượt tương ứng, không phải mô tả trạng thái hiện hành.

## GIỚI HẠN VÀ BÀN GIAO

Không chạy bộ test dài, không gọi CI/workflow_dispatch, không tự soạn chuỗi nhạy cảm. Replay H dùng **byte fixture/stdout sẵn có**, nạp module registry và gọi hàm với `chay_mot` giả; không thực thi các suite mà tên fixture nhắc tới. `doc-claims-check` mặc định chỉ quét các root nó tự khai, **không có ops/**, nên rc0 của nó không chứng minh đặc tả hoặc gói hiện vật này đúng; các phép nội dung/checksum riêng mới là bằng chứng liên quan.

Các phép tự đo hoàn tất rc0: `measure_leases.py`, `measure_costs.py`, `measure_contracts.py`, `verify_artifacts.py`, `build_hints.py` trong `do-review10/`; ba cổng ngắn có stdout/stderr riêng. Lần gọi CLI thô đầu trả rc12 vì origin vẫn trỏ GitHub và kết nối thất bại; không dùng nó để suy người giữ=0. Phép lease dùng được là gọi module thật với transport mirror đã mô tả, có log `offline-ai-dang-giu-{registry,workflow}.stdout`. Các bộ đếm/bia mộ không bị thay bằng dữ liệu dựng.

GitHub trực tiếp, lịch sử tạo ref, quyền/nội dung gốc comment chủ kho, model identity của lượt cũ, readback sau 14:30:07Z, Windows thật, toàn bộ suite, Đ4/Đ5 của H sau thi công: **KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho)**. Không đổi mục nào thành pass.

Cây gợi ý: `goi-y/cay/`; hướng dẫn: `goi-y/README.md`; provenance: `goi-y/hint_provenance.json`. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Gói là tệp ngoài checkout, không phải lease, receipt hoặc authorization. Kết quả kiểm cuối được ghi ở `do-review10/final-check.json`.
